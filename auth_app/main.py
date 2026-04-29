from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth_app.database import create_tables
from auth_app.routes import auth_routes, user_routes

# Important: importing models registers the User table with SQLAlchemy
from auth_app import models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


auth_app = FastAPI(
    title="JWT Authentication Backend Task1",
    lifespan=lifespan,
)


auth_app.include_router(auth_routes.router)
auth_app.include_router(user_routes.router)


@auth_app.get("/")
async def home():
    return {
        "message": "FastAPI JWT authentication backend is running",
    }