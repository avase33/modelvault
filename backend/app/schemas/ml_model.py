from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from app.models.ml_model import ModelFramework, ModelTask, ModelStatus


class ModelCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    framework: ModelFramework
    task: ModelTask
    is_public: bool = False
    tags: List[str] = []
    license: Optional[str] = None
    paper_url: Optional[str] = None
    github_url: Optional[str] = None
    readme: Optional[str] = None


class ModelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ModelStatus] = None
    is_public: Optional[bool] = None
    tags: Optional[List[str]] = None
    license: Optional[str] = None
    paper_url: Optional[str] = None
    github_url: Optional[str] = None
    readme: Optional[str] = None


class ModelVersionCreate(BaseModel):
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    metrics: Dict[str, Any] = {}
    hyperparameters: Dict[str, Any] = {}
    input_schema: Dict[str, Any] = {}
    output_schema: Dict[str, Any] = {}
    training_dataset_id: Optional[UUID] = None
    changelog: Optional[str] = None


class ModelVersionResponse(BaseModel):
    id: UUID
    model_id: UUID
    version: str
    file_size_bytes: Optional[int]
    checksum: Optional[str]
    metrics: Dict[str, Any]
    hyperparameters: Dict[str, Any]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    changelog: Optional[str]
    is_latest: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ModelResponse(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    slug: str
    description: Optional[str]
    framework: ModelFramework
    task: ModelTask
    status: ModelStatus
    is_public: bool
    tags: List[str]
    license: Optional[str]
    paper_url: Optional[str]
    github_url: Optional[str]
    download_count: int
    inference_count: int
    star_count: int
    readme: Optional[str]
    created_at: datetime
    updated_at: datetime
    versions: List[ModelVersionResponse] = []

    class Config:
        from_attributes = True


class ModelListResponse(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    slug: str
    description: Optional[str]
    framework: ModelFramework
    task: ModelTask
    status: ModelStatus
    is_public: bool
    tags: List[str]
    download_count: int
    inference_count: int
    star_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class InferenceRequest(BaseModel):
    inputs: Dict[str, Any]
    parameters: Dict[str, Any] = {}


class InferenceResponse(BaseModel):
    model_id: str
    version: str
    outputs: Dict[str, Any]
    latency_ms: float
    timestamp: datetime
