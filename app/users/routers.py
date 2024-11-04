from datetime import timedelta, datetime

from app.users.auth import get_password_hash, verify_password, create_access_token
from app.config import settings
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from app.users.service import UserService
from app.users.schemas import SUserCreateModel, SUserModel, SUserLoginModel
from app.users.dependencies import RefreshTokenBearer

auth_router = APIRouter()
user_service = UserService()
refresh_token_service = RefreshTokenBearer()


@auth_router.post("/signup", response_model=SUserModel)
async def create_user_account(user_data: SUserCreateModel):
    email = user_data.email

    exist_user = await user_service.user_exists(email=email)
    if exist_user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User is already registered"
        )
    hashed_password = get_password_hash(user_data.password)

    new_user = await user_service.create_user(email=email, hashed_password=hashed_password, username=user_data.username)

    return SUserModel(
        username=new_user.username,
        email=new_user.email,
        auto_reply_enabled=new_user.auto_reply_enabled,
        auto_reply_delay=new_user.auto_reply_delay
    )


@auth_router.post("/login")
async def login_users(user_login_data: SUserLoginModel):

    email = user_login_data.email
    password = user_login_data.password

    user = await user_service.get_user_by_email(email=email)
    if user:
        password_valid = verify_password(password, user.hashed_password)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "username": user.username,
                    "id": str(user.id),
                }
            )

            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "username": user.username,
                    "id": str(user.id),
                },
                refresh=True,
                expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            )

            return JSONResponse(
                content={
                    "message": "You are now logged in",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            )
    else:
        return JSONResponse(
            status_code = status.HTTP_401_UNAUTHORIZED,
            content = {
                "message": "Invalid email or password",
            }
        )


@auth_router.get("/refresh-token/")
async def get_new_access_token(token_details:dict = Depends(refresh_token_service)):

    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details["user"]
        )

        refresh_token = create_access_token(
            user_data=token_details["user"],
            refresh=True,
            expire=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return JSONResponse(
            content = {
                "access_token": new_access_token,
                "refresh_token": refresh_token,
            }
        )
    raise HTTPException(
        status_code = status.HTTP_400_BAD_REQUEST,
        detail = "Token invalid or expired"
    )
