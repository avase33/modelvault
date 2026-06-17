import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer, Float, Text, ForeignKey, JSON, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.core.database import Base


class JobStatus(str, enum.Enum):
    QUEUED = "queued"
    PREPARING = "preparing"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ComputeType(str, enum.Enum):
    CPU = "cpu"
    GPU_T4 = "gpu_t4"
    GPU_A100 = "gpu_a100"
    GPU_V100 = "gpu_v100"


class TrainingJob(Base):
    __tablename__ = "training_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ml_models.id"), nullable=True)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("datasets.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[JobStatus] = mapped_column(SAEnum(JobStatus), default=JobStatus.QUEUED)
    compute_type: Mapped[ComputeType] = mapped_column(SAEnum(ComputeType), default=ComputeType.CPU)

    # Config
    framework: Mapped[str] = mapped_column(String(100), nullable=False)
    script_path: Mapped[str] = mapped_column(String(500), nullable=True)
    docker_image: Mapped[str] = mapped_column(String(500), nullable=True)
    hyperparameters: Mapped[dict] = mapped_column(JSON, default=dict)
    environment_vars: Mapped[dict] = mapped_column(JSON, default=dict)
    max_epochs: Mapped[int] = mapped_column(Integer, nullable=True)
    early_stopping_patience: Mapped[int] = mapped_column(Integer, nullable=True)

    # Runtime info
    celery_task_id: Mapped[str] = mapped_column(String(200), nullable=True)
    current_epoch: Mapped[int] = mapped_column(Integer, default=0)
    progress_percent: Mapped[float] = mapped_column(Float, default=0.0)
    metrics_history: Mapped[dict] = mapped_column(JSON, default=list)
    final_metrics: Mapped[dict] = mapped_column(JSON, default=dict)
    logs: Mapped[str] = mapped_column(Text, nullable=True)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)

    # Timing
    queued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=True)

    owner = relationship("User", back_populates="training_jobs")
