from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class Role(str, enum.Enum):
    student = "student"
    admin = "admin"
    instructor = "instructor"  # Added instructor if you need it

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role, name='user_role'), default=Role.student, nullable=False)  # ✅ Added name='user_role'
    created_at = Column(DateTime(timezone=True), server_default=func.now())