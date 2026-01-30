from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.dependencies.auth_dependencies import get_db
from app.schemas.user import UserCreate, User
from app.schemas.token import Token
from app.models.user import User as UserModel, Role
from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check BYTE length, not character length (bcrypt limit is 72 BYTES)
    password_bytes = len(user.password.encode('utf-8'))
    if password_bytes > 72:
        raise HTTPException(
            status_code=400, 
            detail=f"Password too long ({password_bytes} bytes). Maximum is 72 bytes."
        )
    
    # Check if password looks like it's already hashed
    if user.password.startswith('$2a$') or user.password.startswith('$2b$') or user.password.startswith('$2y$'):
        raise HTTPException(
            status_code=400,
            detail="Invalid password format. Please send plain text password."
        )
    
    # Check if email exists
    result = await db.execute(select(UserModel).where(UserModel.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role if user.role else Role.student
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user