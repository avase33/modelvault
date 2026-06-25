# Model schema -- 2026-06-25 12:05:42
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum

class ModelStatus(str, Enum):
    REGISTERED = "registered"
    TRAINING = "training"
    TRAINED = "trained"
    DEPLOYED = "deployed"
    DEPRECATED = "deprecated"
    FAILED = "failed"

class ModelFramework(str, Enum):
    SKLEARN = "sklearn"
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"
    ONNX = "onnx"
    CUSTOM = "custom"

class ModelCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="")
    framework: ModelFramework = ModelFramework.SKLEARN
    version: str = Field(default="1.0.0")
    tags: List[str] = Field(default_factory=list)
    hyperparameters: Dict[str, Any] = Field(default_factory=dict)
    dataset_info: Optional[Dict[str, Any]] = None

class ModelResponse(ModelCreate):
    id: str
    status: ModelStatus = ModelStatus.REGISTERED
    created_at: datetime
    updated_at: datetime
    metrics: Optional[Dict[str, float]] = None
    artifact_path: Optional[str] = None

    class Config:
        from_attributes = True