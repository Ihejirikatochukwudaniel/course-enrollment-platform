# Course Enrollment Platform API

A modern **FastAPI + PostgreSQL (Supabase)** backend for managing users, authentication, courses, and enrollments. Built with async SQLAlchemy, JWT authentication, and UUID-based primary keys for scalability and security.

**Author:** Tochukwu Ihejirika

---

## 🚀 Tech Stack

* **FastAPI** – high‑performance Python web framework
* **PostgreSQL (Supabase)** – production‑ready database
* **SQLAlchemy (Async)** – ORM with async support
* **Alembic** – database migrations
* **JWT (OAuth2)** – secure authentication
* **Pydantic v2** – data validation
* **Uvicorn** – ASGI server

---

## 📁 Project Structure

```
app/
├── api/
│   ├── auth.py
│   ├── users.py
│   ├── courses.py
│   └── enrollments.py
├── core/
│   ├── config.py
│   └── security.py
├── models/
│   ├── user.py
│   ├── course.py
│   └── enrollment.py
├── schemas/
│   ├── user.py
│   ├── token.py
│   └── course.py
├── dependencies/
│   └── auth_dependencies.py
├── main.py
└── db/
    └── base.py

alembic/
├── versions/
└── env.py

.env
requirements.txt
README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/course-enrollment-platform.git
cd course-enrollment-platform
```

---

### 2️⃣ Create and Activate Virtual Environment

**Windows (PowerShell)**

```bash
python -m venv venv
venv\Scripts\Activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure the following are installed:

* fastapi
* uvicorn
* sqlalchemy
* asyncpg
* alembic
* python-jose
* passlib[bcrypt]
* python-multipart

---

### 4️⃣ Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@db.supabase.co:5432/postgres
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

⚠️ Never commit `.env` files to GitHub.

---

## 🗄️ Database & Migrations (Alembic)

### 1️⃣ Initialize Alembic (Already Done)

If not initialized:

```bash
alembic init alembic
```

---

### 2️⃣ Create a New Migration

Whenever you change a model:

```bash
alembic revision --autogenerate -m "describe your change"
```

Example:

```bash
alembic revision --autogenerate -m "add enrollments table"
```

---

### 3️⃣ Apply Migrations

```bash
alembic upgrade head
```

---

### 4️⃣ Reset Database (Development Only)

```bash
alembic downgrade base
alembic upgrade head
```

⚠️ This will delete data.

---

## ▶️ Running the Application

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

Interactive API docs:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

---

## 🔐 Authentication Flow

1. Register user → `/auth/register`
2. Login → `/auth/login`
3. Receive JWT access token
4. Pass token in headers:

```http
Authorization: Bearer <access_token>
```

---

## 🧪 Running Tests

### 1️⃣ Install Test Dependencies

```bash
pip install pytest pytest-asyncio httpx
```

---

### 2️⃣ Run All Tests

```bash
pytest
```

---

### 3️⃣ Run Tests Verbosely

```bash
pytest -v
```

---

### 4️⃣ Test Coverage (Optional)

```bash
pip install pytest-cov
pytest --cov=app
```

---

## ✅ What Successful Tests Look Like

* All endpoints return correct HTTP status codes
* Authentication returns valid JWT tokens
* Protected routes reject unauthorized access
* Database records are created correctly

Example success output:

```
================== test session starts ==================
collected 12 items

✔ test_register_user
✔ test_login_user
✔ test_create_course
✔ test_enroll_user

================== 12 passed in 2.34s ==================
```

---

## 🧠 Best Practices Used

* UUID primary keys for security
* Async database sessions
* Password hashing with bcrypt
* JWT-based authentication
* Clean separation of concerns

---

## 📌 Future Improvements

* Role-based access control (RBAC)
* Admin dashboard
* Pagination and filtering
* Email verification
* Rate limiting

---

## 🤝 Author

**Tochukwu Ihejirika**
Backend Developer | FastAPI | PostgreSQL | Supabase

---

If you have questions or want to extend this project, feel free to reach out or fork the repository.
