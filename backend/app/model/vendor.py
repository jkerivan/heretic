

from typing import List, Optional
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin


class Vendor(SQLModel, TimeMixin, table=True):
    __tablename__ = "vendor"

    id: UUID = Field(None, primary_key=True, nullable=False)
    name: str

    users: Optional["Users"] = Relationship(sa_relationship_kwargs={'uselist': False}, back_populates="vendor")

    products: Optional[List["Product"]] = Relationship(back_populates="vendors")
