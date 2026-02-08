from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class HeaderMenu(Base):
    __tablename__ = "headermenu"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    type = Column(String(20), nullable=False)  # page | dropdown
    is_active = Column(Boolean, default=True)
