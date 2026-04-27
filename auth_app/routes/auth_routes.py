from fastapi import APIRouter, Response, Cookie

from auth_app.schemas import RegisterRequest, LoginRequest
from auth_app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth_app.services.auth_service import auth_service


router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)


@router.post("/register")
def register(data: RegisterRequest):
    return auth_service.register_user(
        username=data.username,
        password=data.password
    )


@router.post("/login")
def login(data: LoginRequest, response: Response):
    access_token = auth_service.login_user(
        username=data.username,
        password=data.password
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(response: Response, access_token: str | None = Cookie(default=None)):
    result = auth_service.logout_user(access_token)

    response.delete_cookie("access_token")

    return result