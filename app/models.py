from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.database import Base

class PlantPrediction(Base):
    __tablename__ = "plant_predictions"

    id = Column(Integer, primary_key=True, index=True)
    plant_name = Column(String, index=True)
    probability = Column(Float)
    common_names = Column(String)
    image_url = Column(String, nullable=True)  # optional if storing image path
    created_at = Column(DateTime(timezone=True), server_default=func.now())
