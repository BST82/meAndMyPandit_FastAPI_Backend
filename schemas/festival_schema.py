from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class FestivalCreate(BaseModel):
    name: str
    date: date
    month: int = Field(..., ge=1, le=12)
    year: int
    description: Optional[str] = None


class FestivalUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[date] = None
    month: Optional[int] = None
    year: Optional[int] = None
    description: Optional[str] = None
