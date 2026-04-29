from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_app.models import User
from auth_app.security import (
    hash_password,
    jwt_service,
    verify_password,
)
from auth_app.storage import BLACKLISTED_TOKENS


class AuthenticationService:
    def __init__(self):
        self.blacklisted_tokens = BLACKLISTED_TOKENS

    async def get_user_by_username(
        self,
        db: AsyncSession,
        username: str,
    ):
        result = await db.execute(
            select(User).where(User.username == username)
        )

        return result.scalar_one_or_none()

    async def register_user(
        self,
        db: AsyncSession,
        username: str,
        password: str,
    ):
        username = username.strip()

        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username and password are required",
            )

        existing_user = await self.get_user_by_username(db, username)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        new_user = User(
            username=username,
            hashed_password=hash_password(password),
        )

        db.add(new_user)

        await db.commit()
        await db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "username": new_user.username,
        }

    async def login_user(
        self,
        db: AsyncSession,
        username: str,
        password: str,
    ):
        user = await self.get_user_by_username(db, username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        password_is_correct = verify_password(
            password,
            user.hashed_password,
        )

        if not password_is_correct:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        access_token = jwt_service.create_access_token(
            data={
                "sub": user.username,
            }
        )

        return access_token

    async def get_current_user(
        self,
        db: AsyncSession,
        access_token: str | None,
    ):
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not logged in",
            )

        if access_token in self.blacklisted_tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been logged out",
            )

        username = jwt_service.decode_access_token(access_token)

        user = await self.get_user_by_username(db, username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return user

    def logout_user(self, access_token: str | None):
        if access_token:
            self.blacklisted_tokens.add(access_token)

        return {
            "message": "Logout successful",
        }

    async def list_registered_users(
        self,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(User.username)
        )

        return list(result.scalars().all())


auth_service = AuthenticationService()