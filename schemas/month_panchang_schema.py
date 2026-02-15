from pydantic import BaseModel
from typing import List

class Muhurat(BaseModel):
    name: str
    start: str
    end: str
    is_auspicious: bool

class PanchangResponse(BaseModel):
    date: str
    tithi: str
    nakshatra: str
    sunrise: str
    sunset: str
    is_shubh_day: bool  # <-- Add this line!
    shubh_muhurat: List[Muhurat]