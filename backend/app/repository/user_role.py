from typing import List
import uuid
from app.model.role import Role
from app.model.user_role import UsersRole
from app.repository.base_repo import BaseRepo
from app.config import db
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class UsersRoleRepository(BaseRepo):
    model = UsersRole
