from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field

class AuthMode(str, Enum):
    SIMPLE = "Simple local login"
    SERVER = "Server auth"

class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    access_key: str
    role: str = "user"
