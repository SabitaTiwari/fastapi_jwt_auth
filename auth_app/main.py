from fastapi import FastAPI

from auth_app.routes import auth_routes, user_routes


auth_app = FastAPI(
    title="JWT Authentication Backend Task1"
)


auth_app.include_router(auth_routes.router)
auth_app.include_router(user_routes.router)


@auth_app.get("/")
def home():
    return {
        "message": "FastAPI JWT authentication backend is running"
    }