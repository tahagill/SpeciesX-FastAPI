from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
import os
from utils.auth import get_current_user
from models.users import User
from routes import users, gene

# --------------------------
# Initialize FastAPI App
# --------------------------
app = FastAPI()

# --------------------------
# Mount Static Files
# --------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# --------------------------
# MongoDB Connection
# --------------------------
mongo_client = None
mongo_db = None

@app.on_event("startup")
async def startup_db_client():
    """
    Initialize the MongoDB client on application startup.
    """
    global mongo_client, mongo_db
    mongo_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    mongo_db = mongo_client[os.getenv("MONGO_DB", "dummy_gene")]
    print("Connected to MongoDB!")

# --------------------------
# Root Route
# --------------------------
@app.get("/")
async def root(request: Request, user: User = Depends(get_current_user)):
    """
    Redirect to the home page if the user is authenticated, otherwise redirect to the login page.
    """
    if not user:
        return RedirectResponse(url="/login")
    return RedirectResponse(url="/home")

# --------------------------
# Include Routers
# --------------------------
app.include_router(users.router)
app.include_router(gene.router, prefix="", tags=["genes"])