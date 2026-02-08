from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    header_id = Column(Integer, ForeignKey("header_menu.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
