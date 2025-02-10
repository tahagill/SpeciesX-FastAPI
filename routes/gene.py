from fastapi import APIRouter, Request, HTTPException, Query, Form , Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from config.db import db
import httpx
from typing import Optional
from bson import ObjectId
from models.gene import Gene
from models.users import User
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from utils.auth import decode_token


# Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="templates")
API_KEY = 'lwDW7CBQoNtS0iOxfGSzD2wQvnaAuGo7ikma5d2FPnBt7KrNPxqBDHVQ'  # Keep this secure!
oauth2_schemes = OAuth2PasswordBearer(tokenUrl='token')

@router.get("/some_protected_route")
async def protected_route(token: str = Depends(oauth2_schemes)):
    user = await decode_token(token)  # Use the decode_token function
    return {"message": f"Welcome, {user.username}!"}

async def get_current_user(token: Annotated[str, Depends(oauth2_schemes)]):
    user = await decode_token(token)  # Use the decode_token function to get the current user
    return user
@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.get("/home/")
async def read_items(token:Annotated[str, Depends(oauth2_schemes)]):
    return {"'token" : token}




@router.post("/delete/{gene_id}")
async def delete_gene(gene_id: str):
    # Convert string ID to ObjectId
    try:
        object_id = ObjectId(gene_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Object ID")
    
    # Delete the gene entry from the database
    result = await db.dummy01.delete_one({"_id": object_id})
    
    if result.deleted_count == 1:
        return RedirectResponse(url="/archive?delete_success=true", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Gene not found")

@router.get("/edit/{gene_id}", response_class=HTMLResponse)
async def edit_gene(request: Request, gene_id: str):
    # Fetch the gene entry by ID
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
    # Convert string ID to ObjectId
    try:
        object_id = ObjectId(gene_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Object ID")

    # Create a dictionary with the updated values
    gene_data = {
        "species_name": species_name,
        "dna_sequence": dna_sequence,
        "description": description
    }

    # Update the gene entry in the database
    result = await db.dummy01.update_one({"_id": object_id}, {"$set": gene_data})

    if result.modified_count == 1:
        return RedirectResponse(url="/archive?edit_success=true", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Gene not found or no changes made")

@router.get("/archive", response_class=HTMLResponse)
async def archive(request: Request, search: Optional[str] = Query(None), delete_success: Optional[bool] = Query(False), edit_success: Optional[bool] = Query(False)):
    # Fetch all gene entries from the dummy01 collection
    genes = await db.dummy01.find().to_list(length=None)
    newGenes = []

    for gene in genes:
        newGenes.append({
            "id": str(gene["_id"]),
            "species_name": gene.get("species_name"),
            "dna_sequence": gene.get("dna_sequence"),
            "description": gene.get("description")
        })

    # Filter results based on search query
    if search:
        newGenes = [gene for gene in newGenes if search.lower() in gene["species_name"].lower()]

    # Return the archive template with the fetched gene entries and alert messages
    return templates.TemplateResponse("archive.html", {
        "request": request,
        "newGenes": newGenes,
        "search": search,
        "delete_success": delete_success,
        "edit_success": edit_success
    })

# Consolidated home route to avoid redundancy
@router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    # Fetch random images using the Pexels API
    images = await fetch_random_images("dna", 8)
    
    # Return the index.html template with images and request
    return templates.TemplateResponse("index.html", {
        "request": request,
        "images": images
    })

# Helper function to fetch random images from Pexels API
async def fetch_random_images(query: str, num_images: int = 8):
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

@router.post("/home")
async def create_item(request: Request):
    # Fetch form data and insert it into the database
    form = await request.form()
    try:
        await db.dummy01.insert_one(dict(form))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database insert failed: {e}")

    # Redirect to the home page with a success message
    return RedirectResponse(url="/home?success=true", status_code=303)
