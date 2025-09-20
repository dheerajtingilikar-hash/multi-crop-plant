from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import requests, base64
from app.config import PLANT_ID_API_KEY
from app.database import SessionLocal
from app import crud, schemas
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict", response_model=schemas.PlantPredictionOut)
async def identify_plant(file: UploadFile = File(...), db: Session = Depends(get_db)):
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # ✅ Correct Plant.id endpoint
    url = "https://api.plant.id/v2/identify"
    headers = {"Api-Key": PLANT_ID_API_KEY, "Content-Type": "application/json"}
    payload = {
        "images": [image_base64],
        "modifiers": ["crops_fast", "similar_images"],
        "plant_language": "en",
        "plant_details": ["common_names"]
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    if not data.get("suggestions"):
        raise HTTPException(status_code=404, detail="No plant identified")

    best_match = data["suggestions"][0]

    # ✅ Save to DB
    prediction_data = schemas.PlantPredictionCreate(
        plant_name=best_match["plant_name"],
        probability=best_match["probability"],
        common_names=", ".join(best_match.get("plant_details", {}).get("common_names", [])),
    )
    db_record = crud.create_prediction(db=db, prediction=prediction_data)

    return db_record


# ✅ New endpoint: fetch history
@router.get("/history", response_model=List[schemas.PlantPredictionOut])
def get_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    predictions = crud.get_predictions(db=db, skip=skip, limit=limit)
    return predictions
