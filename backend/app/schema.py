

from datetime import datetime
from app.model.product import ProductState
from fastapi import File, Form, HTTPException, UploadFile
import logging
import re
from typing import TypeVar, Optional, Generic, List
import uuid
from pydantic import BaseModel, Field, validator
from sqlalchemy import false
from pydantic.generics import GenericModel


T = TypeVar('T')

logger = logging.getLogger(__name__)


class RegisterSchema(BaseModel):
    username: str
    email: str
    name: str
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str


class ForgotPasswordSchema(BaseModel):
    email: str
    new_password: str


class DetailSchema(BaseModel):
    status: str
    message: str
    result: Optional[T] = None


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None


class PageResponse(GenericModel, Generic[T]):
    """ The response for a pagination query. """

    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]


class ProductCreateSchema(BaseModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    image: Optional[str]
    title: str
    description: str 
    vendor_id: uuid.UUID

    class Config:
        orm_mode = True

class ProductSchema(BaseModel):
    id: uuid.UUID
    image: str
    title: str
    description: str
    vendor_id: uuid.UUID
    created_at: datetime
    modified_at: datetime
    state: ProductState
    image_data: str = ""

    class Config:
        orm_mode = True

class RoleResponseSchema(BaseModel):
    id: uuid.UUID
    role_name: str

    class Config:
        orm_mode = True


class UserResponseSchema(BaseModel):

    id: uuid.UUID
    username: str
    email: str
    password: str
    vendor_id: Optional[uuid.UUID]
    roles: List[RoleResponseSchema]  # You can replace RoleResponseSchema with the appropriate schema

    class Config:
        orm_mode = True


