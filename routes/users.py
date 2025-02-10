from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from config.db import db
from utils.auth import create_access_token, get_password_hash, verify_password, decode_token
from models.users import UserInDB
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="templates")  # Initialize templates

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/register")
async def register(username: str, password: str):
    hashed_password = get_password_hash(password)
    user = UserInDB(username=username, hashed_password=hashed_password)
    await db.user_collection.insert_one(user.dict())
    return {"msg": "User created successfully"}

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.user_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    return user
