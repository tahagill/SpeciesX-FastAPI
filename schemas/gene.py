from fastapi import APIRouter, Request, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from config.db import db
from models.users import User
from bson.objectid import ObjectId
from utils.auth import decode_token
from typing import Annotated
import os

# --------------------------
# Initialize Router and Templates
# --------------------------
router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --------------------------
# Dependency: Get Current User
# --------------------------
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current authenticated user from the JWT token.
    """
    return await decode_token(token)

# --------------------------
# Gene Management Routes
# --------------------------
@router.get("/edit/{gene_id}", response_class=HTMLResponse)
async def edit_gene(
    request: Request,
    gene_id: str,
    user: User = Depends(get_current_user)  # Ensure user is authenticated
):
    """
    Render the edit page for a specific gene entry.
    """
    try:
        gene = await db.dummy01.find_one({"_id": ObjectId(gene_id)})
        if not gene:
            raise HTTPException(status_code=404, detail="Gene not found")
        
        gene["id"] = str(gene["_id"])  # Convert ObjectId to string
        return templates.TemplateResponse("edit.html", {
            "request": request,
            "gene": gene,
            "user": user
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/delete/{gene_id}")
async def delete_gene(
    gene_id: str,
    user: User = Depends(get_current_user)  # Ensure user is authenticated
):
    """
    Delete a gene entry by its ID.
    """
    try:
        result = await db.dummy01.delete_one({"_id": ObjectId(gene_id)})
        if result.deleted_count == 1:
            return RedirectResponse(url="/archive?delete_success=true", status_code=303)
        raise HTTPException(status_code=404, detail="Gene not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/update/{gene_id}")
async def update_gene(
    gene_id: str,
    species_name: str = Form(...),
    dna_sequence: str = Form(...),
    description: str = Form(...),
    user: User = Depends(get_current_user)  # Ensure user is authenticated
):
    """
    Update a gene entry with new data.
    """
    try:
        gene_data = {
            "species_name": species_name,
            "dna_sequence": dna_sequence,
            "description": description
        }
        result = await db.dummy01.update_one(
            {"_id": ObjectId(gene_id)},
            {"$set": gene_data}
        )
        if result.modified_count == 1:
            return RedirectResponse(url="/archive?edit_success=true", status_code=303)
        raise HTTPException(status_code=404, detail="Gene not found or no changes made")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --------------------------
# User Route
# --------------------------
@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Return the current authenticated user's details.
    """
    return current_user