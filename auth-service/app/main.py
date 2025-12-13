from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
import os
import logging

from app import models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "MYSECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------
# NEW: Create service user automatically on startup
# ---------------------------------------------------------
SERVICE_EMAIL = os.getenv("ALARM_USER_EMAIL", "alarm_service@example.com")
SERVICE_PASSWORD = os.getenv("ALARM_PASSWORD", "StrongServicePass123")

@app.on_event("startup")
def create_service_user():
    logging.info("Checking for service user...")

    db: Session = next(get_db())
    existing = db.query(models.User).filter(models.User.email == SERVICE_EMAIL).first()

    if existing:
        logging.info(f"Service user '{SERVICE_EMAIL}' already exists.")
        return

    hashed_pw = pwd_context.hash(SERVICE_PASSWORD[:72])

    new_user = models.User(
        email=SERVICE_EMAIL,
        password_hash=hashed_pw
    )
    db.add(new_user)
    db.commit()

    logging.info(f"Created service user '{SERVICE_EMAIL}' successfully.")
# ---------------------------------------------------------


@app.post("/register")
def register(user: models.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(user.password[:72])  # bcrypt limit
    new_user = models.User(email=user.email, password_hash=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created", "id": new_user.id}


@app.post("/login")
def login(user: models.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token}


@app.get("/me")
def get_me(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id, "email": user.email}


@app.get("/internal/users")
def internal_get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return [{"id": u.id, "email": u.email} for u in users]
