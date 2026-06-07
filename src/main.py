from fastapi import FastAPI

from src.api.router import api_router
from src.core.settings import settings

from src.models.auth.user import User
from src.models.auth.login_session import Login
from src.models.auth.register_session import Registration

# Create FastAPI application
app = FastAPI(
    debug=settings.debug,
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)

app.include_router(api_router, prefix="/api/v1")
