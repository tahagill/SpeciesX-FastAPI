from fastapi import FastAPI
from routes import gene, users
import uvicorn

app = FastAPI()
app.include_router(gene.router)
app.include_router(users.router)

