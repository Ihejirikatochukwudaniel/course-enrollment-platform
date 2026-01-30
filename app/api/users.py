from fastapi import APIRouter, Depends
from app.dependencies.auth_dependencies import get_current_active_user
from app.schemas.user import User
from app.models.user import User as UserModel

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user