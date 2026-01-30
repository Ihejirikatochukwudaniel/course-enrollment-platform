from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.dependencies.auth_dependencies import get_db, get_current_admin
from app.schemas.course import Course, CourseCreate, CourseUpdate
from app.models.course import Course as CourseModel
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[Course])
async def read_courses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CourseModel).offset(skip).limit(limit))
    courses = result.scalars().all()
    return courses

@router.post("/", response_model=Course)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    # Check unique code
    result = await db.execute(select(CourseModel).where(CourseModel.code == course.code))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Course code already exists")
    db_course = CourseModel(**course.dict())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

@router.put("/{course_id}", response_model=Course)
async def update_course(course_id: int, course: CourseUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    db_course = result.scalar_one_or_none()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    update_data = course.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_course, key, value)
    await db.commit()
    await db.refresh(db_course)
    return db_course

@router.delete("/{course_id}")
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    result = await db.execute(select(CourseModel).where(CourseModel.id == course_id))
    db_course = result.scalar_one_or_none()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    await db.delete(db_course)
    await db.commit()
    return {"message": "Course deleted"}