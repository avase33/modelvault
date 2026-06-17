from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.training_job import TrainingJob, JobStatus, ComputeType
from app.api.deps import get_current_user

router = APIRouter(prefix="/training", tags=["Training"])


class TrainingJobCreate(BaseModel):
    name: str
    framework: str
    compute_type: ComputeType = ComputeType.CPU
    model_id: Optional[UUID] = None
    dataset_id: Optional[UUID] = None
    hyperparameters: Dict[str, Any] = {}
    environment_vars: Dict[str, Any] = {}
    max_epochs: Optional[int] = None
    early_stopping_patience: Optional[int] = None
    docker_image: Optional[str] = None


class TrainingJobResponse(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    status: JobStatus
    compute_type: ComputeType
    framework: str
    model_id: Optional[UUID]
    dataset_id: Optional[UUID]
    hyperparameters: Dict[str, Any]
    current_epoch: int
    progress_percent: float
    final_metrics: Dict[str, Any]
    error_message: Optional[str]
    queued_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration_seconds: Optional[int]

    class Config:
        from_attributes = True


@router.get("", response_model=List[TrainingJobResponse])
async def list_jobs(
    status: Optional[JobStatus] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(TrainingJob).where(TrainingJob.owner_id == current_user.id)
    if status:
        query = query.where(TrainingJob.status == status)
    query = query.order_by(TrainingJob.queued_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("", response_model=TrainingJobResponse, status_code=201)
async def create_job(
    data: TrainingJobCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    job = TrainingJob(owner_id=current_user.id, **data.model_dump())
    db.add(job)
    await db.commit()
    await db.refresh(job)
    # In production: dispatch to Celery
    # from app.workers.tasks import run_training_job
    # run_training_job.delay(str(job.id))
    return job


@router.get("/{job_id}", response_model=TrainingJobResponse)
async def get_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TrainingJob).where(
            TrainingJob.id == job_id, TrainingJob.owner_id == current_user.id
        )
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/{job_id}/cancel", response_model=TrainingJobResponse)
async def cancel_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TrainingJob).where(
            TrainingJob.id == job_id, TrainingJob.owner_id == current_user.id
        )
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status not in (JobStatus.QUEUED, JobStatus.RUNNING):
        raise HTTPException(status_code=400, detail="Job cannot be cancelled")
    job.status = JobStatus.CANCELLED
    await db.commit()
    await db.refresh(job)
    return job


@router.get("/{job_id}/logs")
async def get_job_logs(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TrainingJob).where(
            TrainingJob.id == job_id, TrainingJob.owner_id == current_user.id
        )
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"logs": job.logs or "", "metrics_history": job.metrics_history}
