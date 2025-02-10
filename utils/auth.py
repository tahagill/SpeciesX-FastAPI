
from datetime import datetime, timedelta
from typing import Optional
import jwt 
from passlib.context import CryptContext
from fastapi import HTTPException, status
from models.users import UserInDB
from jose import JWTError
from motor.motor_asyncio import AsyncIOMotorClient

# Replace with your MongoDB connection string
client = AsyncIOMotorClient("mongodb+srv://tahagill99:N8FadUL9LvSu85dB@cluster0.cajih.mongodb.net/dummy_gene")
db = client['dummy_gene'] 

# Secret key for JWT
SECRET_KEY = "377205720c84d8b6b95ad12f75e1f4cf993779acd14ccfd6f913931292065b3c"  # Replace with your actual secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_from_db(username: str) -> Optional[UserInDB]:  # Change return type to Optional[UserInDB]
    user = await db.dummy_users.find_one({"username": username})  # Now `db` is defined
    if user:
        return UserInDB(**user)  # Create UserInDB from the retrieved user data
    return None  # This is now acceptable as the return type allows None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

async def decode_token(token: str) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        user = await get_user_from_db(username)  # Use the MongoDB function
        if user is None:
            raise credentials_exception
        
        return UserInDB(
            username=user.username,
            full_name=user.full_name,
            disabled=user.disabled,
            hashed_password=user.hashed_password
        )
    except JWTError:
        raise credentials_exception
