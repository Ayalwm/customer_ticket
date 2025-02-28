from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from database import get_db  
from app import models 


SECRET_KEY = os.getenv("JWT_SECRET", "mysecretkey")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta: 
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire.timestamp()})  

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("Received Token:", token) 

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  
        role: str = payload.get("role")  
        exp: int = payload.get("exp", None)   

        if not email or not role:
            raise credentials_exception

        
        if exp is not None and datetime.utcnow().timestamp() > exp:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

    except JWTError:
        raise credentials_exception 
 
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        raise credentials_exception  

    return user  


def get_admin_user(current_user: models.User = Depends(get_current_user)):
    if not current_user or current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    print("User Role:", current_user.role)  
    return current_user  
