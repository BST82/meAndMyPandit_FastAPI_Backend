from pydantic import BaseModel


class FooterCreate(BaseModel):
    name: str
    slug: str
