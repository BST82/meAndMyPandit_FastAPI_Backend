from sqlalchemy import Column, Integer, String, Enum
from database import Base
from pydantic import BaseModel, EmailStr, Field
import enum

class UserRole(str, enum.Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    USER = "User"
    ASTROLOGER = "Astrologer"
    PANDIT = "Pandit"
    SHOPKEEPER = "Shopkeeper"

# Priority Mapping
ROLE_PRIORITY = {
    UserRole.ADMIN: 1,
    UserRole.MANAGER: 2,
    UserRole.ASTROLOGER: 3,
    UserRole.PANDIT: 4,
    UserRole.SHOPKEEPER: 5,
    UserRole.USER: 6
}

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    role = Column(String)
    priority = Column(Integer)  # Lower number = Higher priority
    password: str = Field(..., min_length=6)