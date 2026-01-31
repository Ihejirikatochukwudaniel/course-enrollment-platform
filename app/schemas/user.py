from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field
from typing import Optional
from uuid import UUID
from app.models.user import Role

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72)
    role: Optional[Role] = Role.student
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        # Check byte length (bcrypt has 72-byte limit)
        password_bytes = len(v.encode('utf-8'))
        if password_bytes > 72:
            raise ValueError(f'Password is too long ({password_bytes} bytes). Maximum is 72 bytes.')
        
        # Check if it looks like an already-hashed password
        if v.startswith('$2a$') or v.startswith('$2b$') or v.startswith('$2y$'):
            raise ValueError('Please provide a plain text password, not a hashed one.')
        
        # Minimum length check
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[Role] = None

class User(UserBase):
    id: UUID  # ✅ Changed from int to UUID
    is_active: bool
    role: Role

    model_config = ConfigDict(from_attributes=True)