
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from .models import *
import jwt
from jwt import PyJWTError

# Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Secret key for JWT token (use a strong, unique secret)
SECRET_KEY = "secret-key"

# Algorithm for JWT token
ALGORITHM = "HS256"

# Token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Hasher:
    def get_password_hash(password):
        return pwd_context.hash(password)
    def verify_password(plain_password):
        hashed_password = Hasher.get_password_hash(plain_password)
        return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_data = Token(**payload)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_data


# Function to verify the JWT token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except PyJWTError:
        return None
