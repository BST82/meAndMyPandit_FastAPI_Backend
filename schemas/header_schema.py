from pydantic import BaseModel
from typing import List, Optional


class PlaceCreate(BaseModel):
    name: str
    slug: str


class CityCreate(BaseModel):
    name: str
    slug: str
    places: Optional[List[PlaceCreate]] = []


class HeaderCreate(BaseModel):
    name: str
    slug: str
    type: str  # page | dropdown
    cities: Optional[List[CityCreate]] = []
