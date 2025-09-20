from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt, datetime

from app import models, database

app = FastAPI()

# Database setup
models.Base.metadata.create_all(bind=database.engine)

# Auth setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "your-secret-key"

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register
@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = pwd_context.hash(password)
    new_user = models.User(username=username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered"}

# Login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"sub": user.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY, algorithm="HS256"
    )
    return {"access_token": token, "token_type": "bearer"}

# Get user info
@app.get("/me")
def get_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"username": payload["sub"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
