from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text
from app.core.config import engine
from app.api import auth, users, courses, enrollments

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Test database connection
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise
    yield

app = FastAPI(title="Course Enrollment Platform", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])