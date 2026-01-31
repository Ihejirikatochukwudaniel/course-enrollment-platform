from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class EnrollmentBase(BaseModel):
    user_id: UUID
    course_id: UUID

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: UUID  # Changed from int to UUID
    enrolled_at: datetime

    model_config = ConfigDict(from_attributes=True)