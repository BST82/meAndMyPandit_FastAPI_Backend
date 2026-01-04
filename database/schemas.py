from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    full_name: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "jdoe",
                "email": "jdoe@example.com",
                "full_name": "John Doe"
            }
        }

class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    full_name: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "username": "jdoe_new",
                "full_name": "John D."
            }
        }