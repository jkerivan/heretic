
from sqlalchemy.future import select
from app.model import Users, Vendor
from app.config import db
from sqlalchemy.orm import joinedload

class UserService:

    @staticmethod
    async def get_user_profile(username:str):
        query = select(Users).where(Users.username == username).options(joinedload(Users.roles))
        return (await db.execute(query)).unique().scalar_one_or_none()
