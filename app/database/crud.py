from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from app.database.models import *
from app import database
from app.models import *
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

# Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: User):
    hashed_password = pwd_context.hash(user.password)
    while True:
        try:
            db_user = UserTable(username=user.username, password=hashed_password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            db.rollback()
            # Handle the duplicate key error
            # Generate a new unique ID and assign it to the user
            user.id = str(uuid.uuid4())  # Generate a new UUID as the ID    

def get_user_by_id(db: Session, user_id: str):
    return db.query(database.models.UserTable).filter(database.models.UserTable.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(database.models.UserTable).filter(database.models.UserTable.username == username).first()

def update_user(db: Session, user_id: str, new_data: dict, current_version: int):
    user = db.query(database.models.UserTable).filter(database.models.UserTable.id == user_id, database.models.UserTable.version == current_version).first()
    
    if user is None:
        return None  # Return None if the user doesn't exist or the version doesn't match

    # Update user data based on new_data dictionary
    for key, value in new_data.items():
        setattr(user, key, value)
    
    # Increment the version to indicate the update
    user.version += 1

    db.commit()
    return user

def delete_user(db: Session, user_id: str):
    user = db.query(database.models.UserTable).filter(database.models.UserTable.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def create_product(db: Session, product: Product):
    db_product = ProductTable(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_user_cart(db: Session, user_cart: UserCart):
    db_user_cart = UserCartTable(**user_cart.dict())
    db.add(db_user_cart)
    db.commit()
    db.refresh(db_user_cart)
    return db_user_cart

def get_products(db: Session, skip: int = 0, limit: int = 10):
    products = db.query(database.models.ProductTable).offset(skip).limit(limit).all()
    return products


def create_order(db: Session, user_id: str, product_id: str, quantity: int):
    order = database.models.OrderTable(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_user_orders(db: Session, user_id: str):
    return db.query(database.models.OrderTable).filter(database.models.OrderTable.user_id == user_id).all()

def cancel_order(db: Session, order_id: int):
    order = db.query(database.models.OrderTable).filter(database.models.OrderTable.id == order_id, database.models.OrderTable.status == "active").first()
    if order:
        order.status = "cancelled"
        db.commit()
        db.refresh(order)
    return order
