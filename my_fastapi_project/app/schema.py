from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    nom: str

class CoordBase(BaseModel):
    nom: str
    longitude: float
    latitude: float
    date1: datetime
    

class CoordCreate(BaseModel):
    nom: str
    longitude: float
    latitude: float
    date1: datetime

class CoordResponse(CoordBase):
    id: int

    class Config:
        orm_mode = True
