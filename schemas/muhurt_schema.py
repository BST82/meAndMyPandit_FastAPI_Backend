from pydantic import BaseModel
from datetime import date, time
from typing import List


class MuhurtRequest(BaseModel):
    date: date
    latitude: float
    longitude: float


class ChoghadiyaItem(BaseModel):
    start_time: str
    end_time: str
    type: str


class MuhurtResponse(BaseModel):
    date: str
    sunrise: str
    sunset: str
    day_choghadiya: list[ChoghadiyaItem]
    night_choghadiya: list[ChoghadiyaItem]
    special_muhurts: list[str]
