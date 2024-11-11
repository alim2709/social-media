from pydantic import BaseModel, EmailStr, Field


class SUserCreateModel(BaseModel):
    username: str = Field(max_length=20)
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8)

class SUserLoginModel(BaseModel):
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8)


class SUserModel(BaseModel):
    username: str
    email: EmailStr
    auto_reply_enabled: bool
    auto_reply_delay: int

class SUserEnableAutoReplyModel(BaseModel):
    auto_reply_enabled: bool
    auto_reply_delay: int | None = None