import base64
from datetime import datetime
from typing import List
from uuid import uuid4
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials

from passlib.context import CryptContext
from app.schema import RegisterSchema
from app.model import Vendor, Users, UsersRole, Role
from app.repository.role import RoleRepository
from app.repository.users import UsersRepository
from app.repository.vendor import VendorRepository
from app.repository.user_role import UsersRoleRepository
from app.schema import LoginSchema, ForgotPasswordSchema
from app.repository.auth_repo import JWTBearer, JWTRepo


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    async def register_service(register: RegisterSchema):

        _vendor_id = str(uuid4())
        _users_id = str(uuid4())

        _vendor = Vendor(id=_vendor_id, name=register.username)

        _users = Users(id=_users_id, username=register.username, email=register.email,
                       password=pwd_context.hash(register.password),
                       vendor_id=_vendor_id)

        # Everyone who registers through our registration page makes the default as a vendor
        _role = await RoleRepository.find_by_role_name("vendor")
        _users_role = UsersRole(users_id=_users_id, role_id=_role.id)

        _username = await UsersRepository.find_by_username(register.username)
        if _username:
            raise HTTPException(
                status_code=400, detail="Username already exists!")

        _email = await UsersRepository.find_by_email(register.email)
        if _email:
            raise HTTPException(
                status_code=400, detail="Email already exists!")

        else:
            await VendorRepository.create(**_vendor.dict())
            await UsersRepository.create(**_users.dict())
            await UsersRoleRepository.create(**_users_role.dict())

    @staticmethod
    async def login_service(login: LoginSchema):
        _user = await UsersRepository.find_by_username(login.username)
        if _user is not None:
            if not pwd_context.verify(login.password, _user.password):
                raise HTTPException(
                    status_code=400, detail="Invalid Password!")
            
            is_admin = any(role.role_name == "admin" for role in _user.roles)
            return JWTRepo(data={"username": _user.username, "is_admin": is_admin }).generate_token()
        raise HTTPException(status_code=404, detail="Username not found!")

    @staticmethod
    async def forgot_password_service(forgot_password: ForgotPasswordSchema):
        _email = await UsersRepository.find_by_email(forgot_password.email)
        if _email is None:
            raise HTTPException(status_code=404, detail="Email not found!")
        await UsersRepository.update_password(forgot_password.email, pwd_context.hash(forgot_password.new_password))


class UserCredentials:
    def __init__(self, username: str, is_admin: bool):
        self.username = username
        self.is_admin = is_admin


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    _token = JWTRepo.extract_token(credentials)
    _username = _token['username']
    _is_admin= _token['is_admin']
    return UserCredentials(username=_username, is_admin=_is_admin)


def is_admin_user(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    _token = JWTRepo.extract_token(credentials)
    _is_admin= _token['is_admin']
    if not _is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return True

# Generate roles manually
async def generate_roles():
    _role = await RoleRepository.find_by_list_role_name(["admin", "vendor"])
    if not _role:
        await RoleRepository.create_list(
            [Role(id=str(uuid4()), role_name="admin"), Role(id=str(uuid4()), role_name="vendor")])
        
    _vendor_id = str(uuid4())
    _users_id = str(uuid4())
    _vendor = Vendor(id=_vendor_id, name="admin")

    _users = Users(id=_users_id, username='admin', email='admin@gmail.com',
                       password=pwd_context.hash('admin'),
                       vendor_id=_vendor_id)

    _role = await RoleRepository.find_by_role_name("vendor")
    _role1 = await RoleRepository.find_by_role_name("admin")
    _users_role = UsersRole(users_id=_users.id, role_id=_role.id)
    _users_role1 = UsersRole(users_id=_users.id, role_id=_role1.id)
    await VendorRepository.create(**_vendor.dict())
    await UsersRepository.create(**_users.dict())
    await UsersRoleRepository.create(**_users_role.dict())
    await UsersRoleRepository.create(**_users_role1.dict())