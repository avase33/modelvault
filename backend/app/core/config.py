from pydantic_settings import BaseSettings
from typing import Optional, List
import secrets


class Settings(BaseSettings):
    # App
    APP_NAME: str = "ModelVault"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/modelvault"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Storage (S3-compatible)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_MODELS: str = "modelvault-models"
    S3_BUCKET_DATASETS: str = "modelvault-datasets"
    USE_LOCAL_STORAGE: bool = True
    LOCAL_STORAGE_PATH: str = "./storage"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: str = "noreply@modelvault.ai"

    # Limits
    MAX_MODEL_SIZE_MB: int = 5000
    MAX_DATASET_SIZE_MB: int = 10000
    FREE_TIER_MODEL_LIMIT: int = 5
    FREE_TIER_API_CALLS_PER_DAY: int = 1000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
