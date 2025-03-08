# auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Request, Response
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from models.users import UserInDB, User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Load environment variables
load_dotenv()

# --------------------------
# OAuth2 Setup with Cookie Support
# --------------------------
class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    """
    Custom OAuth2 password bearer that reads the token from cookies.
    """
    async def __call__(self, request: Request) -> Optional[str]:
        authorization: Optional[str] = request.cookies.get("access_token")
        if not authorization:
            return None
        # Split "Bearer <token>"
        return authorization.split("Bearer ")[1] if "Bearer " in authorization else None

# Initialize OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

# --------------------------
# Application Settings
# --------------------------
class Settings(BaseModel):
    """
    Application settings loaded from environment variables.
    """
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    mongo_uri: str
    mongo_db: str

def get_settings() -> Settings:
    """
    Load and validate application settings from environment variables.
    """
    secret_key = os.getenv("SECRET_KEY")
    mongo_uri = os.getenv("MONGO_URI")
    
    if not secret_key or not mongo_uri:
        raise ValueError("Missing required environment variables")
    
    return Settings(
        secret_key=secret_key,
        algorithm=os.getenv("ALGORITHM", "HS256"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)),
        mongo_uri=mongo_uri,
        mongo_db=os.getenv("MONGO_DB", "dummy_gene")
    )

# Initialize settings
settings = get_settings()

# --------------------------
# Database Connection
# --------------------------
client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.mongo_db]

# --------------------------
# Password Hashing and Verification
# --------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a plain password.
    """
    return pwd_context.hash(password)

# --------------------------
# Token Creation and Validation
# --------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

async def decode_token(token: str) -> User:
    """
    Decode a JWT token and return the associated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub") or ""
        if not username:
            raise credentials_exception
            
        user_in_db = await get_user(username)
        if not user_in_db:
            raise credentials_exception
            
        return User(**user_in_db.dict())
    except (JWTError, Exception):
        raise credentials_exception

# --------------------------
# User Authentication
# --------------------------
async def get_user(username: str) -> Optional[UserInDB]:
    """
    Retrieve a user from the database by username.
    """
    user = await db.dummy_users.find_one({"username": username})
    return UserInDB(**user) if user else None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current authenticated user from the JWT token.
    """
    try:
        return await decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# --------------------------
# Logout Functionality
# --------------------------
async def logout_user(response: Response):
    """
    Invalidate the user's session by deleting the access token cookie.
    """
    response.delete_cookie("access_token")
    return response