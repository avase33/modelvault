from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional, List
import re
import aiofiles
import os
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.models.ml_model import MLModel, ModelVersion, ModelStatus
from app.schemas.ml_model import (
    ModelCreate, ModelUpdate, ModelResponse, ModelListResponse,
    ModelVersionCreate, ModelVersionResponse
)
from app.api.deps import get_current_user, get_current_user_or_api_key

router = APIRouter(prefix="/models", tags=["Models"])


def make_slug(name: str, owner_id: str) -> str:
    base = re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")
    return f"{base}"


@router.get("", response_model=List[ModelListResponse])
async def list_models(
    search: Optional[str] = None,
    framework: Optional[str] = None,
    task: Optional[str] = None,
    is_public: bool = True,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List public models with filtering and search."""
    query = select(MLModel).where(MLModel.is_public == is_public)
    if search:
        query = query.where(
            or_(MLModel.name.ilike(f"%{search}%"), MLModel.description.ilike(f"%{search}%"))
        )
    if framework:
        query = query.where(MLModel.framework == framework)
    if task:
        query = query.where(MLModel.task == task)
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("", response_model=ModelResponse, status_code=201)
async def create_model(
    data: ModelCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    slug = make_slug(data.name, str(current_user.id))
    model = MLModel(
        owner_id=current_user.id,
        slug=slug,
        **data.model_dump(),
    )
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model


@router.get("/my", response_model=List[ModelListResponse])
async def list_my_models(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(MLModel).where(MLModel.owner_id == current_user.id))
    return result.scalars().all()


@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(
    model_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(MLModel).where(MLModel.id == model_id))
    model = result.scalar_one_or_none()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@router.patch("/{model_id}", response_model=ModelResponse)
async def update_model(
    model_id: str,
    data: ModelUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MLModel).where(MLModel.id == model_id, MLModel.owner_id == current_user.id)
    )
    model = result.scalar_one_or_none()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(model, field, value)
    await db.commit()
    await db.refresh(model)
    return model


@router.delete("/{model_id}", status_code=204)
async def delete_model(
    model_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MLModel).where(MLModel.id == model_id, MLModel.owner_id == current_user.id)
    )
    model = result.scalar_one_or_none()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    await db.delete(model)
    await db.commit()


@router.post("/{model_id}/versions", response_model=ModelVersionResponse, status_code=201)
async def create_version(
    model_id: str,
    data: ModelVersionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MLModel).where(MLModel.id == model_id, MLModel.owner_id == current_user.id)
    )
    model = result.scalar_one_or_none()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    # Unset previous latest
    result2 = await db.execute(
        select(ModelVersion).where(ModelVersion.model_id == model_id, ModelVersion.is_latest == True)
    )
    for v in result2.scalars().all():
        v.is_latest = False
    version = ModelVersion(model_id=model_id, is_latest=True, **data.model_dump())
    db.add(version)
    await db.commit()
    await db.refresh(version)
    return version


@router.post("/{model_id}/versions/{version_id}/upload")
async def upload_model_file(
    model_id: str,
    version_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ModelVersion).where(
            ModelVersion.id == version_id, ModelVersion.model_id == model_id
        )
    )
    version = result.scalar_one_or_none()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    upload_dir = os.path.join(settings.LOCAL_STORAGE_PATH, "models", model_id, version_id)
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    version.file_path = file_path
    version.file_size_bytes = len(content)
    await db.commit()
    return {"message": "File uploaded successfully", "file_path": file_path, "size_bytes": len(content)}
