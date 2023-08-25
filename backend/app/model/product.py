

from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Enum, table
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin


class ProductState(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"

class Product(SQLModel, TimeMixin, table=True):
    __tablename__ = "product"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    image: str = Field(None, nullable=False)
    title: str = Field(None, nullable=False)
    description: str = Field(None, nullable=False)
    state: ProductState = Field(ProductState.PENDING, nullable=False)
    vendor_id: Optional[UUID] = Field(default=None, foreign_key="vendor.id")

    vendors: Optional["Vendor"] = Relationship(back_populates="products")
