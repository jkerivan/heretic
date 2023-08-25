
import email
from multiprocessing import synchronize
from uuid import UUID
from app.model.vendor import Vendor
from app.schema import ProductCreateSchema
from sqlalchemy import update as sql_update
from sqlalchemy.future import select

from app.model.product import Product

from app.config import db
from app.repository.base_repo import BaseRepo


class ProductRepository(BaseRepo):
    model = Product

    @staticmethod
    async def get_products_by_vendor(vendor_id: UUID):
        query = select(Product).join(Vendor).where(Vendor.id == vendor_id)

        products = await db.execute(query)
        return products.scalars().all()