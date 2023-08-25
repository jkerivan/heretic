import uuid
from app.model.vendor import Vendor
from app.repository.base_repo import BaseRepo
from sqlalchemy import select
from app.config import db, commit_rollback

class VendorRepository(BaseRepo):
    model = Vendor

    @staticmethod
    async def find_by_vendor_id(id: uuid.UUID):
        query = select(Vendor).where(Vendor.id == id)
        return (await db.execute(query)).scalar_one_or_none()