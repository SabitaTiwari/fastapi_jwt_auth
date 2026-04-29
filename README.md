# FastAPI JWT Authentication with Async PostgreSQL

This is a FastAPI authentication backend project using JWT authentication and asynchronous PostgreSQL database connection.

The project was first built using in-memory storage, and later updated to store users in PostgreSQL asynchronously using SQLAlchemy Async and asyncpg.

## Features

- User registration
- User login
- JWT token generation
- JWT token stored in HTTP-only cookie
- Protected `/me` route
- Protected `/users` route
- Password hashing
- Asynchronous PostgreSQL database connection
- SQLAlchemy AsyncSession
- Clean separation of routes, services, models, database, config, and security logic

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy Async
- asyncpg
- PyJWT
- pwdlib
- Uvicorn

## Project Structure

```text
auth_task/
│
├── auth_app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── storage.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── user_routes.py
│   │
│   └── services/
│       └── auth_service.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/SabitaTiwari/fastapi_jwt_auth.git
cd fastapi_jwt_auth
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

For Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=change-this-secret-key-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/fastapi_auth_db
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_auth_db
```

The `.env` file should not be pushed to GitHub.

## PostgreSQL Setup

Open PostgreSQL shell and create the database:

```sql
CREATE DATABASE fastapi_auth_db;
```

Connect to the database:

```sql
\c fastapi_auth_db
```

The `users` table will be created automatically when the FastAPI application starts.

## Run the Application

Start the server:

```bash
uvicorn auth_app.main:auth_app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Home

```http
GET /
```

Response:

```json
{
  "message": "FastAPI JWT authentication backend is running"
}
```

### Register

```http
POST /api/register
```

Request body:

```json
{
  "username": "ishwor",
  "password": "secret123"
}
```

Response:

```json
{
  "message": "User registered successfully",
  "username": "ishwor"
}
```

### Login

```http
POST /api/login
```

Request body:

```json
{
  "username": "ishwor",
  "password": "secret123"
}
```

Response:

```json
{
  "message": "Login successful",
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

The access token is also stored in an HTTP-only cookie.

### Current User

```http
GET /me
```

Response:

```json
{
  "logged_in": true,
  "message": "You are logged in",
  "username": "ishwor"
}
```

### List Users

```http
GET /users
```

Response:

```json
{
  "users": [
    "ishwor"
  ]
}
```

### Logout

```http
POST /api/logout
```

Response:

```json
{
  "message": "Logout successful"
}
```

## Database Table

The project creates a `users` table with the following fields:

```text
id
username
hashed_password
```

The password is not stored directly. It is hashed before saving to the database.

Example:

```text
secret123
```

is stored as a secure hash like:

```text
$argon2id$v=19$m=65536,t=3,p=4$...
```

## What I Learned

In this project, I learned how to connect a FastAPI authentication system with an asynchronous PostgreSQL database.

Previously, users were stored in an in-memory dictionary, which meant data disappeared when the server restarted. Now, users are saved permanently in PostgreSQL.

I also learned how to use:

- `create_async_engine`
- `AsyncSession`
- `async_sessionmaker`
- `await db.execute()`
- `await db.commit()`
- `await db.refresh()`
- password hashing
- JWT token creation and verification
- HTTP-only cookies
- protected routes

## Main Request Flow

```text
Client request
    ↓
FastAPI route
    ↓
Authentication service
    ↓
Async SQLAlchemy session
    ↓
PostgreSQL database
    ↓
Response
```

## Important Async Database Code

```python
result = await db.execute(
    select(User).where(User.username == username)
)
```

```python
await db.commit()
```

```python
await db.refresh(new_user)
```

These lines show that the project is using asynchronous database operations.

## Future Improvements

- Move logout token blacklist to database or Redis
- Add Alembic migrations
- Add email validation
- Add user roles
- Add refresh tokens
- Add unit tests
- Add Docker support
- Improve environment-based configuration