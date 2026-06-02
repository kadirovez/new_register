from typing import Generic, TypeVar, Type, Optional, List

from fastapi import HTTPException
from sqlalchemy import select, func, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.core.database import Base

import csv
import io
from fastapi import UploadFile
from fastapi.responses import StreamingResponse

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def _coerce_value(value: str, col_type) -> any:
    """Convert CSV string values to correct Python types."""
    if value is None or value == "":
        return None

    from sqlalchemy import Boolean as SABoolean
    if isinstance(col_type, SABoolean):
        return value.lower() in ("true", "1", "yes")

    return value

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD operations for all models."""

    def __init__(self, model: Type[ModelType], load_options: list | None = None):
        self.model = model
        self.load_options = load_options or []

        # Single unique fields (col.unique = True)
        self._unique_fields = [
            col.name
            for col in inspect(model).columns
            if col.unique and col.name != "id"
        ]

        # Composite unique fields from table indexes
        self._unique_composite = []
        mapper = inspect(model)
        for index in mapper.persist_selectable.indexes:
            if index.unique:
                cols = [col.name for col in index.columns]
                if len(cols) > 1:
                    self._unique_composite.append(cols)

    def _apply_load_options(self, query):
        """Apply selectin load options to query if defined."""
        for option in self.load_options:
            query = query.options(option)
        return query

    async def _check_unique_fields(
            self,
            db: AsyncSession,
            data: dict,
            exclude_id: int | None = None,
    ) -> None:
        """Check unique constraints and raise 409 if violated."""
        for field in self._unique_fields:
            if field not in data or data[field] is None:
                continue

            query = select(self.model).where(
                getattr(self.model, field) == data[field]
            )

            if exclude_id is not None:
                query = query.where(self.model.id != exclude_id)

            result = await db.execute(query)
            existing = result.scalar_one_or_none()

            if existing:
                raise HTTPException(
                    status_code=409,
                    detail=f"{self.model.__tablename__} with {field}='{data[field]}' already exists"
                )

    async def get(
            self,
            db: AsyncSession,
            id: int,
    ) -> Optional[ModelType]:
        """Get record by ID. Raises 404 if record not found."""
        query = select(self.model).where(self.model.id == id)
        query = self._apply_load_options(query)
        result = await db.execute(query)
        db_obj = result.scalar_one_or_none()

        if db_obj is None:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__tablename__} not found"
            )
        return db_obj

    async def get_all(
            self,
            db: AsyncSession,
            skip: int = 0,
            limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination."""
        query = select(self.model).offset(skip).limit(limit).order_by(self.model.id.desc())
        query = self._apply_load_options(query)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(
            self,
            db: AsyncSession,
            obj_in: CreateSchemaType
    ) -> ModelType:
        """Create new record."""
        obj_in_data = obj_in.model_dump()
        await self._check_unique_fields(db=db, data=obj_in_data)

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()

        query = select(self.model).where(self.model.id == db_obj.id)
        query = self._apply_load_options(query)
        result = await db.execute(query)
        return result.scalar_one()

    async def update(
            self,
            db: AsyncSession,
            id: int,
            obj_in: UpdateSchemaType
    ) -> ModelType:
        """Update existing record."""
        db_obj = await self.get(db=db, id=id)
        obj_data = obj_in.model_dump(exclude_unset=True)
        await self._check_unique_fields(db=db, data=obj_data, exclude_id=db_obj.id)

        for field, value in obj_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()

        query = select(self.model).where(self.model.id == db_obj.id)
        query = self._apply_load_options(query)
        result = await db.execute(query)
        return result.scalar_one()

    async def delete(
            self,
            db: AsyncSession,
            id: int,
    ) -> Optional[ModelType]:
        """Delete record by ID."""
        db_obj = await self.get(db=db, id=id)
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    async def count(
            self,
            db: AsyncSession
    ) -> int:
        """Count total records."""
        result = await db.execute(select(func.count(self.model.id)))
        return result.scalar_one()

    async def export_csv(self, db: AsyncSession) -> StreamingResponse:
        """Export all records to CSV."""
        records = await self.get_all(db=db, limit=100000)

        if not records:
            columns = [col.name for col in inspect(self.model).columns]
        else:
            columns = [col.name for col in inspect(self.model).columns]

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()

        for record in records:
            writer.writerow({col: getattr(record, col) for col in columns})

        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={self.model.__tablename__}.csv"}
        )

    async def import_csv(
            self,
            db: AsyncSession,
            file: UploadFile,
    ) -> dict:

        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="File must be a CSV")

        columns = [col.name for col in inspect(self.model).columns
                   if col.name not in ("id", "created_at", "updated_at")]

        # Build column type map for coercion
        col_types = {col.name: col.type for col in inspect(self.model).columns}

        content = await file.read()
        reader = csv.DictReader(io.StringIO(content.decode("utf-8")))

        if not reader.fieldnames:
            raise HTTPException(status_code=400, detail="CSV file is empty or has no headers")

        if self._unique_composite:
            lookup_fields = self._unique_composite[0]
        elif self._unique_fields:
            lookup_fields = [self._unique_fields[0]]
        else:
            lookup_fields = [reader.fieldnames[0]]

        added = []
        updated = []
        skipped = []
        rejected = []
        seen_in_csv = set()

        for row in reader:
            missing = [col for col in columns if col not in row]
            if missing:
                rejected.append({"row": row, "reason": f"Missing columns: {missing}"})
                continue

            try:
                key_label = ".".join(str(row[f]) for f in lookup_fields)

                if key_label in seen_in_csv:
                    rejected.append({"row": row, "reason": f"Duplicate key in CSV: {key_label}"})
                    continue
                seen_in_csv.add(key_label)

                query = select(self.model)
                for field in lookup_fields:
                    query = query.where(getattr(self.model, field) == row[field])

                result = await db.execute(query)
                existing = result.scalar_one_or_none()

                if existing:
                    changes = {}
                    for field, value in row.items():
                        if field in columns and field not in lookup_fields:
                            coerced = _coerce_value(value, col_types.get(field))
                            current = getattr(existing, field)
                            if str(current) != str(coerced):
                                changes[field] = coerced

                    if changes:
                        for field, value in changes.items():
                            setattr(existing, field, value)
                        db.add(existing)
                        await db.commit()
                        updated.append(key_label)
                    else:
                        skipped.append(key_label)
                else:
                    obj_data = {
                        col: _coerce_value(row.get(col), col_types.get(col))
                        for col in columns
                    }
                    db_obj = self.model(**obj_data)
                    db.add(db_obj)
                    await db.commit()
                    added.append(key_label)

            except Exception as e:
                await db.rollback()
                rejected.append({"row": row, "reason": str(e)})

        return {
            "added": len(added),
            "updated": len(updated),
            "skipped": len(skipped),
            "rejected": len(rejected),
            "added_keys": added,
            "updated_keys": updated,
            "skipped_keys": skipped,
            "rejected_keys": rejected,
        }
