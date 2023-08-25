import base64
from uuid import UUID
import uuid
from app.model.product import Product, ProductState
from app.repository.product import ProductRepository
from app.repository.user_role import UsersRoleRepository
from app.repository.vendor import VendorRepository
from app.service.auth_service import UserCredentials, get_current_user, is_admin_user
from fastapi import APIRouter,Depends, File, Form, UploadFile

from app.schema import ProductCreateSchema, ProductSchema, ResponseSchema
from app.service.users import UserService
from fastapi import Depends

router = APIRouter(
    prefix="/products",
    tags=['product']
)

@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_products(user_credentials: UserCredentials = Depends(get_current_user)): 
    user = await UserService.get_user_profile(user_credentials.username)

    vendor_products = []
    if user_credentials.is_admin:
        vendor_products = await ProductRepository.get_all()
    else:
        vendor_products = await ProductRepository.get_products_by_vendor(user.vendor_id)
    
    results = []
    for product in vendor_products:
        schema = ProductSchema.from_orm(product)
        
        # Open the image file and encode it as base64
        with open(product.image, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        
        schema.image_data = encoded_image  # Include the encoded image data in the response
        results.append(schema)
        
    return ResponseSchema(detail="Successfully fetch data!", result=results)

@router.post("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_product(title: str = Form(...), 
                         description: str = Form(...), 
                         vendor_id: str = Form(...),
                         image: UploadFile = File(...), user_credentials: UserCredentials = Depends(get_current_user)):

    image_path = f"admin/backend/media/{image.filename}"  
    with open(image_path, "wb") as image_file:
        image_file.write(image.file.read())

    product_data = ProductCreateSchema(image=image_path, title=title, description=description, vendor_id=UUID(vendor_id))
    created_product = await ProductRepository.create(**product_data.dict())

    return ResponseSchema(detail="Successfully created data!", result=created_product)


@router.post("/{product_id}/approve", response_model=ResponseSchema, response_model_exclude_none=True)
async def approve(product_id: str, is_admin: None = Depends(is_admin_user), user_credentials: UserCredentials = Depends(get_current_user)):
    product = await ProductRepository.update(UUID(product_id), state=ProductState.APPROVED)
    return ResponseSchema(detail="Successfully approved!", result=product)