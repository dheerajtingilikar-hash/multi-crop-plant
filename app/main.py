from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os

app = FastAPI()

# ✅ Allow only your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://multi-crop-frontend.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is running!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Dummy prediction (replace with ML model)
        result = {"crop": "Wheat", "confidence": 0.92}

        # Remove temp file
        os.remove(file_location)

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://multi-crop-frontend.vercel.app"],  # frontend on Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
