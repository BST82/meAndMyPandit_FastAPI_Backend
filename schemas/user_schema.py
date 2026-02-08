from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserRoleEnum(str, Enum):
    Admin = "Admin"
    Manager = "Manager"
    User = "User"
    Astrologer = "Astrologer"
    Pandit = "Pandit"
    Shopkeeper = "Shopkeeper"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    role: UserRoleEnum
    password: str 

class UserResponse(BaseModel):
    id: str = Field(alias="_id") # MongoDB uses _id
    name: str
    email: str
    role: str
    priority: int

    class Config:
        populate_by_name = True