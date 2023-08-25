from app.service.auth_service import UserCredentials, get_current_user
from fastapi import APIRouter,Depends

from app.schema import ResponseSchema, UserResponseSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.service.users import UserService

router = APIRouter(
    prefix="/users",
    tags=['user'],
    dependencies=[Depends(JWTBearer())]
)
 

@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(user_credentials: UserCredentials = Depends(get_current_user)):
    result = await UserService.get_user_profile(user_credentials.username)
    user_response = UserResponseSchema(**result.__dict__)
    return ResponseSchema(detail="Successfully fetch data!", result=user_response)