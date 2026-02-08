from pydantic import BaseModel
from typing import List, Optional


class Mantra(BaseModel):
    name: str
    mantraName: str
    mantraValue: str


class HomeData(BaseModel):
    name: str       # heading
    content: str    # content text


class HomeCreate(BaseModel):
    mantras: List[Mantra]
    data: List[HomeData]
