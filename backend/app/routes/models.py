# Model API routes -- 2026-06-22 13:05:37
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List, Optional
from datetime import datetime
from app.schemas.model import ModelCreate, ModelResponse, ModelStatus
from app.services.registry import registry

router = APIRouter(prefix="/api/models", tags=["models"])

# In-memory store (replace with DB in production)
_models: dict = {}

@router.get("/", response_model=List[ModelResponse])
async def list_models(status: Optional[str] = None, framework: Optional[str] = None):
    models = list(_models.values())
    if status:
        models = [m for m in models if m["status"] == status]
    if framework:
        models = [m for m in models if m["framework"] == framework]
    return models

@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(model_id: str):
    if model_id not in _models:
        raise HTTPException(status_code=404, detail="Model not found")
    return _models[model_id]

@router.post("/", response_model=ModelResponse, status_code=201)
async def create_model(body: ModelCreate):
    import uuid
    model_id = str(uuid.uuid4())
    now = datetime.utcnow()
    model = {
        "id": model_id,
        "status": ModelStatus.REGISTERED,
        "created_at": now,
        "updated_at": now,
        **body.dict()
    }
    _models[model_id] = model
    return model

@router.patch("/{model_id}/status")
async def update_status(model_id: str, status: ModelStatus):
    if model_id not in _models:
        raise HTTPException(status_code=404, detail="Model not found")
    _models[model_id]["status"] = status
    _models[model_id]["updated_at"] = datetime.utcnow()
    return _models[model_id]

@router.delete("/{model_id}", status_code=204)
async def delete_model(model_id: str):
    if model_id not in _models:
        raise HTTPException(status_code=404, detail="Model not found")
    registry.delete_artifact(model_id)
    del _models[model_id]