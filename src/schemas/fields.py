
from typing import Annotated
from datetime import datetime

from pydantic import Field, BeforeValidator, AfterValidator, EmailStr

from src.core.settings import settings

