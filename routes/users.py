# users.py
from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth import create_access_token, verify_password, get_password_hash
from models.users import UserInDB
from config.db import db
import os

# Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# --------------------------
# Route: Login Page
# --------------------------
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Render the login page.
    """
    return templates.TemplateResponse("login.html", {"request": request})

# --------------------------
# Route: Register Page
# --------------------------
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """
    Render the registration page.
    """
    return templates.TemplateResponse("signup.html", {"request": request})

# --------------------------
# Route: Logout
# --------------------------
@router.post("/logout")
async def logout():
    """
    Handle user logout by redirecting to the login page.
    """
    response = RedirectResponse(url="/login", status_code=303)
    return response

# --------------------------
# Route: Register User
# --------------------------
@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """
    Handle user registration.
    """
    try:
        # Check if user already exists
        existing_user = await db.dummy_users.find_one({"username": username})
        if existing_user:
            return RedirectResponse(url="/register?error=username_taken", status_code=303)
        
        # Hash password and create user
        hashed_password = get_password_hash(password)
        user = UserInDB(
            username=username,
            hashed_password=hashed_password,
            full_name="",
            disabled=False
        )
        
        # Insert user into database
        await db.dummy_users.insert_one(user.dict())
        
        # Redirect to login with success message
        return RedirectResponse(url="/login?registered=true", status_code=303)
    
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return RedirectResponse(url="/register?error=server_error", status_code=303)

# --------------------------
# Route: Login Handler
# --------------------------
@router.post("/token")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Handle user login and set access token as a cookie.
    """
    try:
        # Find user
        user = await db.dummy_users.find_one({"username": form_data.username})
        if not user:
            return RedirectResponse(url="/login?error=invalid_credentials", status_code=303)
        
        # Verify password
        if not verify_password(form_data.password, user["hashed_password"]):
            return RedirectResponse(url="/login?error=invalid_credentials", status_code=303)
        
        # Create token
        access_token = create_access_token(data={"sub": user["username"]})
        
        # Redirect to home page and set token as a cookie
        response = RedirectResponse(url="/home", status_code=303)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=1800  # Token expires in 30 minutes
        )
        return response
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return RedirectResponse(url="/login?error=server_error", status_code=303)