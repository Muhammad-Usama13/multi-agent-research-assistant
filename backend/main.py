"""
Multi-Agent Research Assistant — FastAPI Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routers import analysis, upload, health

app = FastAPI(
    title="Multi-Agent Research Assistant",
    description="AI-powered research paper analysis using multiple specialized agents",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,   prefix="/api",          tags=["Health"])
app.include_router(upload.router,   prefix="/api/upload",   tags=["Upload"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])


@app.get("/")
async def root():
    return {
        "message": "Multi-Agent Research Assistant API",
        "docs": "/docs",
        "status": "running",
    }