from fastapi import FastAPI
from fastapi import Depends, HTTPException,  Header
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import sessionmaker
import uvicorn
from passlib.context import CryptContext
from app.database import crud
from app.operations import *
from app.models import *
from .database.models import *
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
import os

app = FastAPI()

# Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Example of hashing a password
hashed_password = pwd_context.hash("user_password")


app = FastAPI()


# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Replace with your list of allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Replace with the allowed HTTP methods (e.g., ["GET", "POST"])
    allow_headers=["Authorization",  "Content-Type"]  # Replace with the allowed HTTP headers
)

# Define a rate limiting decorator
def rate_limit(limit: int, interval: int):
    """
    A decorator for rate limiting.
    :param limit: The maximum number of requests allowed within the interval.
    :param interval: The time interval (in seconds).
    """
    def decorator(func):
        func = lru_cache(maxsize=limit)(func)

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


# Get environment variables or use default values
db_username = os.environ.get('DB_USERNAME', 'root')
db_password = os.environ.get('DB_PASSWORD', 'AshaShiva#08')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = int(os.environ.get('DB_PORT', '3306'))
db_schema = os.environ.get('DB_SCHEMA', 'zonmart')

# Database connection string
DATABASE_URL = f"mysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_schema}"

# SQLAlchemy database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a Session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User authentication route
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = crud.get_user_by_username(db, form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not Hasher.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



# User registration route
@app.post("/create_user/") #response_model=UserResponse)
async def create_user(user: User, db: Session = Depends(get_db)): 
                    # authorization: str = Header(None, description="Access Token")):
    
    # if not authorization:
    #     raise HTTPException(status_code=401, detail="Missing access token")
    
    # if not verify_token(authorization):
    #     raise HTTPException(status_code=401, detail="Invalid access token")
    
    db_user = crud.get_user_by_username(db, user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = crud.create_user(db, user)

    return db_user


@app.get("/users/{user_id}")#, response_model=UserResponse)
async def read_user(user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}")
async def update_user(
        user_id: str,
        new_data: dict,
        current_version: int, 
        db: Session = Depends(get_db)
        ):

    updated_user = crud.update_user(db, user_id, new_data, current_version)
    db.close()
    
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found or version mismatch")
    
    return updated_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id)
    db.close()
    return {"message": "User deleted"}


# Product creation route
@app.post("/create_product/", response_model=Product)
async def create_product(product: Product, db: Session = Depends(get_db)):
    db_product = crud.create_product(db, product)
    return db_product

# Add a product to a user's cart route
@app.post("/user_carts/", response_model=UserCart)
async def add_product_to_cart(user_cart: UserCart, db: Session = Depends(get_db)):
    db_user_cart = crud.create_user_cart(db, user_cart)
    return db_user_cart


@app.post("/home")
async def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip, limit)
    return products


@app.post("/orders/")
async def create_order(
        user_id: str,
        product_id: str,
        quantity: int,
        db: Session = Depends(get_db)
        ):
    order = crud.create_order(db, user_id, product_id, quantity)
    db.close()
    return order

@app.get("/users/{user_id}/orders")
async def get_user_orders(user_id: str, db: Session = Depends(get_db)):
    orders = crud.get_user_orders(db, user_id)
    db.close()
    return orders

@app.put("/orders/{order_id}/cancel")
async def cancel_order(order_id: int, db: Session = Depends(get_db)):
    cancelled_order = crud.cancel_order(db, order_id)
    db.close()
    if cancelled_order is None:
        raise HTTPException(status_code=404, detail="Order not found or already cancelled")
    return cancelled_order


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
