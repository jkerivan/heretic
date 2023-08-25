

from typing import List, Optional
from uuid import UUID
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field, Relationship

from app.model.mixins import TimeMixin
from app.model.user_role import UsersRole

class Users(SQLModel,TimeMixin,table=True):
    __tablename__= "users"

    id: UUID = Field(None, primary_key=True, nullable=False)
    username: str = Field(sa_column=Column("username", String, unique=True))
    email: str = Field(sa_column=Column("email", String, unique=True))
    password: str
    vendor_id: Optional[UUID] = Field(default=None, foreign_key="vendor.id")
    vendor: Optional["Vendor"] = Relationship(back_populates="users")

    roles: List["Role"] = Relationship(back_populates="users", link_model=UsersRole)