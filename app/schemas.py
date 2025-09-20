from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlantPredictionBase(BaseModel):
    plant_name: str
    probability: float
    common_names: Optional[str] = None
    image_url: Optional[str] = None

class PlantPredictionCreate(PlantPredictionBase):
    pass

class PlantPredictionOut(PlantPredictionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
