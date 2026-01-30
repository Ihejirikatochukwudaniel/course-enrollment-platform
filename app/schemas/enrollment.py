from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int
    enrolled_at: datetime

    model_config = ConfigDict(from_attributes=True)