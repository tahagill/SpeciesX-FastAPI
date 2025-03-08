from fastapi import APIRouter, Request, HTTPException, Query, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from config.db import db
import httpx
from typing import Optional
from bson import ObjectId
from models.gene import Gene
from models.users import User
from fastapi.security import OAuth2PasswordBearer
from utils.auth import decode_token, get_current_user

# --------------------------
# Initialize Router and Templates
# --------------------------
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Pexels API key (keep this secure!)
API_KEY = 'lwDW7CBQoNtS0iOxfGSzD2wQvnaAuGo7ikma5d2FPnBt7KrNPxqBDHVQ'

# OAuth2 scheme for token authentication
oauth2_schemes = OAuth2PasswordBearer(tokenUrl='token')

# --------------------------
# Protected Route Example
# --------------------------
@router.get("/some_protected_route")
async def protected_route(token: str = Depends(oauth2_schemes)):
    """
    Example of a protected route that requires authentication.
    """
    user = await decode_token(token)
    return {"message": f"Welcome, {user.username}!"}

# --------------------------
# Gene Management Routes
# --------------------------
@router.post("/delete/{gene_id}")
async def delete_gene(gene_id: str):
    """
    Delete a gene entry by its ID.
    """
    try:
        object_id = ObjectId(gene_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Object ID")
    
    result = await db.dummy01.delete_one({"_id": object_id})
    
    if result.deleted_count == 1:
        return RedirectResponse(url="/archive?delete_success=true", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Gene not found")

@router.get("/edit/{gene_id}", response_class=HTMLResponse)
async def edit_gene(request: Request, gene_id: str):
    """
    Render the edit page for a specific gene entry.
    """
    gene = await db.dummy01.find_one({"_id": ObjectId(gene_id)})
    
    if not gene:
        raise HTTPException(status_code=404, detail="Gene not found")
    
    return templates.TemplateResponse("edit.html", {
        "request": request,
        "gene": gene
    })

@router.post("/update/{gene_id}")
async def update_gene(
    gene_id: str,
    species_name: str = Form(...),
    dna_sequence: str = Form(...),
    description: str = Form(...)
):
    """
    Update a gene entry with new data.
    """
    try:
        object_id = ObjectId(gene_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Object ID")

    gene_data = {
        "species_name": species_name,
        "dna_sequence": dna_sequence,
        "description": description
    }

    result = await db.dummy01.update_one({"_id": object_id}, {"$set": gene_data})

    if result.modified_count == 1:
        return RedirectResponse(url="/archive?edit_success=true", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Gene not found or no changes made")

# --------------------------
# Archive Route
# --------------------------
@router.get("/archive", response_class=HTMLResponse)
async def archive(
    request: Request,
    search: Optional[str] = Query(None),
    delete_success: Optional[bool] = Query(False),
    edit_success: Optional[bool] = Query(False)
):
    """
    Render the archive page with a list of gene entries.
    """
    genes = await db.dummy01.find().to_list(length=None)
    newGenes = []

    for gene in genes:
        newGenes.append({
            "id": str(gene["_id"]),
            "species_name": gene.get("species_name"),
            "dna_sequence": gene.get("dna_sequence"),
            "description": gene.get("description")
        })

    if search:
        newGenes = [gene for gene in newGenes if search.lower() in gene["species_name"].lower()]

    return templates.TemplateResponse("archive.html", {
        "request": request,
        "newGenes": newGenes,
        "search": search,
        "delete_success": delete_success,
        "edit_success": edit_success
    })

# --------------------------
# Home Route
# --------------------------
@router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    """
    Render the home page with random images from the Pexels API.
    """
    images = await fetch_random_images("dna", 8)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "images": images
    })

@router.post("/home")
async def create_item(request: Request):
    """
    Handle form submission to create a new gene entry.
    """
    form = await request.form()
    try:
        await db.dummy01.insert_one(dict(form))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database insert failed: {e}")

    return RedirectResponse(url="/home?success=true", status_code=303)

# --------------------------
# Helper Functions
# --------------------------
async def fetch_random_images(query: str, num_images: int = 8):
    """
    Fetch random images from the Pexels API.
    """
    url = f'https://api.pexels.com/v1/search?query={query}&per_page={num_images}&page=1'
    headers = {
        'Authorization': API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [photo['src']['original'] for photo in data['photos']]
    else:
        raise HTTPException(status_code=response.status_code, detail="Could not fetch images from Pexels.")

# --------------------------
# About and Contact Routes
# --------------------------
@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, user: User = Depends(get_current_user)):
    """
    Render the about page.
    """
    return templates.TemplateResponse("about.html", {"request": request, "user": user})

@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request, user: User = Depends(get_current_user)):
    """
    Render the contact page.
    """
    return templates.TemplateResponse("contact.html", {"request": request, "user": user})