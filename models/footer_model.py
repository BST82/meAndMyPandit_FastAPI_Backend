from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class FooterPage(Base):
    __tablename__ = "footer_pages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(150), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
