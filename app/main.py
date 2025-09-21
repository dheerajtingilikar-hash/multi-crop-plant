from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil, os, requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PLANT_ID_API_KEY = os.getenv("PLANT_ID_API_KEY")

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------
# PREDICT ROUTE
# -------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not PLANT_ID_API_KEY:
        return {"error": "PLANT_ID_API_KEY not set in environment"}

    # Save uploaded image temporarily
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call Plant.id API
    url = "https://api.plant.id/v2/identify"
    headers = {"Api-Key": PLANT_ID_API_KEY}
    files = [("images", open(temp_file, "rb"))]

    response = requests.post(url, headers=headers, files=files, data={"organs": '["leaf"]'})
    os.remove(temp_file)  # cleanup

    return response.json()
