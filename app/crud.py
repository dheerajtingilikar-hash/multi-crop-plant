from sqlalchemy.orm import Session
from app import models, schemas

def create_prediction(db: Session, prediction: schemas.PlantPredictionCreate):
    db_prediction = models.PlantPrediction(**prediction.dict())
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

def get_predictions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PlantPrediction).offset(skip).limit(limit).all()
