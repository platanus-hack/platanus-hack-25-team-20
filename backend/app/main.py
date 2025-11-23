from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.admin.admin import setup_admin
from app.config import settings
from app.database.setup import init_db
from app.routers import (
    user_router,
    user_profile_router,
    project_router,
    user_skills_router,
    template_router,
    cv_router,
    application_router,
    extraction_router,
    job_offering_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="CV Generator API",
    description="Backend API for CV generation with AI - Hackaton Platanus 2025",
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:4173",  # Vite preview
        "http://localhost:3000",  # Alternative dev port
        "http://localhost",       # Docker frontend (port 80)
        "http://localhost:80",    # Docker frontend (explicit port)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, prefix="/api/v1", tags=["users"])
app.include_router(user_profile_router.router, prefix="/api/v1", tags=["profiles"])
app.include_router(project_router.router, prefix="/api/v1", tags=["projects"])
app.include_router(user_skills_router.router, prefix="/api/v1", tags=["skills"])
app.include_router(template_router.router, prefix="/api/v1", tags=["templates"])
app.include_router(cv_router.router, prefix="/api/v1", tags=["cvs"])
app.include_router(application_router.router, prefix="/api/v1", tags=["applications"])
app.include_router(extraction_router.router, prefix="/api/v1", tags=["extraction"])
app.include_router(job_offering_router.router, prefix="/api/v1", tags=["job_offerings"])

setup_admin(app)


@app.get("/")
async def root():
    return {
        "message": "CV Generator API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment
    }

