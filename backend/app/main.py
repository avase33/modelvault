from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import router as api_v1_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting ModelVault API...")
    await init_db()
    logger.info("Database initialized.")
    yield
    logger.info("Shutting down ModelVault API.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## ModelVault — AI/ML Model Management Platform

A production-grade platform for:
- **Model Registry**: Upload, version, and manage ML models
- **Dataset Management**: Store and share training datasets
- **Training Jobs**: Orchestrate and monitor training runs
- **Inference API**: Deploy models and run predictions at scale
- **API Keys**: Programmatic access for integrations

Built with FastAPI + PostgreSQL + Redis + React.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(api_v1_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "healthy", "version": settings.APP_VERSION, "app": settings.APP_NAME}


@app.get("/")
async def root():
    return {
        "message": "Welcome to ModelVault API",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }
