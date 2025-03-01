from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app import models, schemas, auth
from database import SessionLocal
from app.models import User, UserRole

router = APIRouter()
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_user2 = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user2:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = auth.hash_password(user_data.password)
    try:
      role_enum = UserRole(user_data.role) if user_data.role else UserRole.USER
    except ValueError:
      raise HTTPException(status_code=400, detail="Invalid role")
    new_user = models.User(
        email=user_data.email, 
        username=user_data.username or "guest", 
        hashed_password=hashed_password, 
        role=role_enum
    )

    db.add(new_user)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    db.refresh(new_user)
    return new_user

@router.post("/login")
def login_user(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print("🔹 Login Attempt: ", user_data.username) 
    
    user = db.query(models.User).filter(models.User.email == user_data.username).first()
    print("🔹 Found User: ", user) 
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not auth.verify_password(user_data.password, user.hashed_password):
  
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role.value},  
    )


    return {"access_token": access_token, "token_type": "bearer"}
