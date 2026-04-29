from fastapi import APIRouter, Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth_app.database import get_db
from auth_app.services.auth_service import auth_service


router = APIRouter(
    tags=["Users"],
)


@router.get("/me")
async def me(
    access_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    current_user = await auth_service.get_current_user(
        db=db,
        access_token=access_token,
    )

    return {
        "logged_in": True,
        "message": "You are logged in",
        "username": current_user.username,
    }


@router.get("/users")
async def users(
    access_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    await auth_service.get_current_user(
        db=db,
        access_token=access_token,
    )

    registered_users = await auth_service.list_registered_users(db)

    return {
        "users": registered_users,
    }