from pydantic import BaseModel
from datetime import datetime


class Base(BaseModel):
    user_code: str | None = None
    firstname: str | None = None
    lastname: str
    phone_number: str | None = None
    email: str
    role: str


class Create(Base):
    password: str | None = None


class Read(Base):
    password_is_change: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Schema(Read):
    class Config:
        from_attributes = True
