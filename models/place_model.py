from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))
    name = Column(String(150), nullable=False)
    slug = Column(String(150), nullable=False)
    is_active = Column(Boolean, default=True)
