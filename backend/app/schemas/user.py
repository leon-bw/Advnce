from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    id: UUID = Field(description="The ID of the user")
    email: EmailStr = Field(description="The email of the user")
    is_active: bool = Field(description="Whether the user is active")
    created_at: datetime = Field(description="The date and time the user was created")
    updated_at: datetime = Field(description="The date and time the user was updated")

    model_config = {
        "from_attributes": True,
    }
