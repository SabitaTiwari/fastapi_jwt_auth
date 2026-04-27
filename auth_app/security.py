from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

from auth_app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


class JWTService:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: dict):
        token_data = data.copy()

        expire_time = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_token_expire_minutes
        )

        token_data.update({
            "exp": expire_time
        })

        encoded_jwt = jwt.encode(
            token_data,
            self.secret_key,
            algorithm=self.algorithm
        )

        return encoded_jwt

    def decode_access_token(self, token: str):
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            username = payload.get("sub")

            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )

            return username

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )


jwt_service = JWTService()