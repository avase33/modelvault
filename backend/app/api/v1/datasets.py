from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional, List
import re
import aiofiles
import os
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.models.dataset import Dataset, DatasetType, DatasetStatus
from app.api.deps import get_current_user

router = APIRouter(prefix="/datasets", tags=["Datasets"])


class DatasetCreate(BaseModel):
    name: str
    description: Optional[str] = None
    dataset_type: DatasetType
    is_public: bool = False
    tags: List[str] = []
    license: Optional[str] = None
    readme: Optional[str] = None


class DatasetResponse(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    slug: str
    description: Optional[str]
    dataset_type: DatasetType
    status: DatasetStatus
    is_public: bool
    tags: List[str]
    file_size_bytes: Optional[int]
    num_rows: Optional[int]
    num_columns: Optional[int]
    num_files: Optional[int]
    download_count: int
    created_at: datetime

    class Config:
        from_attributes = True


def make_slug(name: str) -> str:
    return re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")


@router.get("", response_model=List[DatasetResponse])
async def list_datasets(
    search: Optional[str] = None,
    dataset_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Dataset).where(Dataset.is_public == True)
    if search:
        query = query.where(
            or_(Dataset.name.ilike(f"%{search}%"), Dataset.description.ilike(f"%{search}%"))
        )
    if dataset_type:
        query = query.where(Dataset.dataset_type == dataset_type)
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("", response_model=DatasetResponse, status_code=201)
async def create_dataset(
    data: DatasetCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    dataset = Dataset(
        owner_id=current_user.id,
        slug=make_slug(data.name),
        **data.model_dump(),
    )
    db.add(dataset)
    await db.commit()
    await db.refresh(dataset)
    return dataset


@router.get("/my", response_model=List[DatasetResponse])
async def list_my_datasets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Dataset).where(Dataset.owner_id == current_user.id))
    return result.scalars().all()


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


@router.post("/{dataset_id}/upload")
async def upload_dataset_file(
    dataset_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Dataset).where(Dataset.id == dataset_id, Dataset.owner_id == current_user.id)
    )
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    upload_dir = os.path.join(settings.LOCAL_STORAGE_PATH, "datasets", dataset_id)
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    dataset.file_path = file_path
    dataset.file_size_bytes = len(content)
    dataset.status = DatasetStatus.READY
    await db.commit()
    return {"message": "Dataset uploaded", "size_bytes": len(content)}


@router.delete("/{dataset_id}", status_code=204)
async def delete_dataset(
    dataset_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Dataset).where(Dataset.id == dataset_id, Dataset.owner_id == current_user.id)
    )
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    await db.delete(dataset)
    await db.commit()
