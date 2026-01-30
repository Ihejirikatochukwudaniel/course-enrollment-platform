from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.dependencies.auth_dependencies import get_db, get_current_student, get_current_admin
from app.schemas.enrollment import Enrollment, EnrollmentCreate
from app.models.enrollment import Enrollment as EnrollmentModel
from app.models.course import Course
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Enrollment)
async def enroll_course(enrollment: EnrollmentCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_student)):
    if current_user.id != enrollment.user_id:
        raise HTTPException(status_code=403, detail="Cannot enroll others")
    # Check course exists and active
    result = await db.execute(select(Course).where(Course.id == enrollment.course_id))
    course = result.scalar_one_or_none()
    if not course or not course.is_active:
        raise HTTPException(status_code=400, detail="Course not available")
    # Check capacity
    enrolled_count_result = await db.execute(
        select(func.count(EnrollmentModel.id)).where(EnrollmentModel.course_id == enrollment.course_id)
    )
    enrolled_count = enrolled_count_result.scalar()
    if enrolled_count >= course.capacity:
        raise HTTPException(status_code=400, detail="Course is full")
    # Check not already enrolled
    result = await db.execute(
        select(EnrollmentModel).where(
            EnrollmentModel.user_id == enrollment.user_id,
            EnrollmentModel.course_id == enrollment.course_id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already enrolled")
    db_enrollment = EnrollmentModel(**enrollment.dict())
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)
    return db_enrollment

@router.delete("/{enrollment_id}")
async def deregister_course(enrollment_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_student)):
    result = await db.execute(select(EnrollmentModel).where(EnrollmentModel.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    if not enrollment or enrollment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    await db.delete(enrollment)
    await db.commit()
    return {"message": "Deregistered"}

@router.get("/", response_model=list[Enrollment])
async def read_enrollments(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    result = await db.execute(select(EnrollmentModel).offset(skip).limit(limit))
    enrollments = result.scalars().all()
    return enrollments