from datetime import datetime, timedelta
from typing import Union
from jose import JWTError
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from model import User
from sqlalchemy.orm import Session
from database import SessionLocal

# Secret key and algorithm for JWT token creation (keep it safe!)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Access token expiry time (in minutes)

# OAuth2PasswordBearer is used to extract the token from request headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Passlib for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create a new session instance for database interaction
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility function to hash passwords
def hash_password(password: str):
    return pwd_context.hash(password)

# Utility function to verify password against a hashed one
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Utility function to create access tokens
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()  # Ensure the dictionary is copied
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})  # Adding expiration time for token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Utility function to decode and verify token
def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception
