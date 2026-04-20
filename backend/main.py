from fastapi import FastAPI
from app.api import api_router

app = FastAPI(title="VISI-SDLC-GenAI-POC Backend API")

app.include_router(api_router, prefix="/api")
