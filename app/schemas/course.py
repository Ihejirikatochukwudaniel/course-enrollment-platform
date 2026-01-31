from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class CourseBase(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    capacity: int = Field(..., gt=0, description="Capacity must be greater than 0")  # ✅ Validates > 0

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)  # ✅ Also validate on update
    is_active: Optional[bool] = None

class Course(CourseBase):
    id: UUID  # ✅ Changed from int to UUID to match database
    is_active: bool
    created_at: datetime  # ✅ Added created_at field

    model_config = ConfigDict(from_attributes=True)