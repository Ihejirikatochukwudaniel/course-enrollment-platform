# Course Enrollment Platform Backend

A FastAPI backend for managing course enrollments with JWT authentication and role-based access control.

## Features

- User registration and login with JWT tokens
- Role-based access control (student/admin)
- CRUD operations for courses (admin only)
- Enrollment management for students
- Input validation with Pydantic
- Async database operations with SQLAlchemy and PostgreSQL

## Setup

1. Install Python 3.8+

2. Clone or download the project

3. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   Copy `.env.example` to `.env` and fill in your database URL and secret key.

6. Run database migrations:
   ```bash
   alembic upgrade head
   ```

7. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

8. Run tests:
   ```bash
   pytest
   ```

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.