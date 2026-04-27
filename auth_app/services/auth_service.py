import hmac

from fastapi import HTTPException, status

from auth_app.storage import USERS, BLACKLISTED_TOKENS
from auth_app.security import jwt_service


class AuthenticationService:
    def __init__(self):
        self.users = USERS
        self.blacklisted_tokens = BLACKLISTED_TOKENS

    def register_user(self, username: str, password: str):
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username and password are required"
            )

        if username in self.users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        self.users[username] = {
            "username": username,
            "password": password
        }

        return {
            "message": "User registered successfully",
            "username": username
        }

    def login_user(self, username: str, password: str):
        user = self.users.get(username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        password_is_correct = hmac.compare_digest(
            password,
            user["password"]
        )

        if not password_is_correct:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        access_token = jwt_service.create_access_token(
            data={
                "sub": user["username"]
            }
        )

        return access_token

    def get_current_user(self, access_token: str | None):
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not logged in"
            )

        if access_token in self.blacklisted_tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been logged out"
            )

        username = jwt_service.decode_access_token(access_token)

        user = self.users.get(username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user

    def logout_user(self, access_token: str | None):
        if access_token:
            self.blacklisted_tokens.add(access_token)

        return {
            "message": "Logout successful"
        }

    def list_registered_users(self):
        return list(self.users.keys())


auth_service = AuthenticationService()