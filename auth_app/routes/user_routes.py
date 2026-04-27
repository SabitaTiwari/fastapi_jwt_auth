from fastapi import APIRouter, Cookie

from auth_app.services.auth_service import auth_service


router = APIRouter(
    tags=["Users"]
)


@router.get("/me")
def me(access_token: str | None = Cookie(default=None)):
    current_user = auth_service.get_current_user(access_token)

    return {
        "logged_in": True,
        "message": "You are logged in",
        "username": current_user["username"]
    }


@router.get("/users")
def users(access_token: str | None = Cookie(default=None)):
    auth_service.get_current_user(access_token)

    return {
        "users": auth_service.list_registered_users()
    }