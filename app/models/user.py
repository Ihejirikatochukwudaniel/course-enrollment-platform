from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum
import uuid

Base = declarative_base()

class Role(str, enum.Enum):
    student = "student"
    admin = "admin"
    instructor = "instructor"

class User(Base):
    __tablename__ = "users"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # ✅ Changed to UUID
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role, name='user_role'), default=Role.student, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())