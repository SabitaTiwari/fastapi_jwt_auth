from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth_app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from auth_app.database import get_db
from auth_app.schemas import LoginRequest, RegisterRequest
from auth_app.services.auth_service import auth_service


router = APIRouter(
    prefix="/api",
    tags=["Authentication"],
)


@router.post("/register")
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    return await auth_service.register_user(
        db=db,
        username=data.username,
        password=data.password,
    )


@router.post("/login")
async def login(
    data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    access_token = await auth_service.login_user(
        db=db,
        username=data.username,
        password=data.password,
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    response: Response,
    access_token: str | None = Cookie(default=None),
):
    result = auth_service.logout_user(access_token)

    response.delete_cookie("access_token")

    return result