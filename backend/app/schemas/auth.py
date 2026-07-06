from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr = Field(description="The email of the user")
    password: str = Field(
        min_length=8, max_length=128, description="The password of the user"
    )


class LoginRequest(BaseModel):
    email: EmailStr = Field(description="The email of the user")
    password: str = Field(
        min_length=8, max_length=128, description="The password of the user"
    )


class TokenResponse(BaseModel):
    access_token: str = Field(description="The access token")
    token_type: str = Field(description="The token type")
