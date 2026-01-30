from pydantic import BaseModel, ConfigDict
from typing import Optional

class CourseBase(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    capacity: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None

class Course(CourseBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)