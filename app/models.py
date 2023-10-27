from pydantic import BaseModel

# Pydantic models
class User(BaseModel):
    username: str
    password: str
    address: str

class UserResponse(BaseModel):
    id: str
    username: str
    password: str
    version: int
    address: str

    class Config:
        orm_mode = True    

class Product(BaseModel):
    name: str
    description: str
    price: float

class UserInDB(User):
    username: str
    hashed_password: str

class UserCart(BaseModel):
    user_id: int
    product_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None    
