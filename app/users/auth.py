import logging
import jwt
from app.config import settings
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
        user_data: dict,
        expire : timedelta = None,
        refresh: bool = False
) -> str:
    payload = {
        "user": user_data,
        "exp":
            datetime.now(timezone.utc) + (
                expire if expire else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            ),
        "refresh": refresh
    }

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def decode_token(token: str) -> dict | None:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
