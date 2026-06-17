import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Integer, Float, Text, ForeignKey, JSON, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.core.database import Base


class ModelFramework(str, enum.Enum):
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    SKLEARN = "sklearn"
    ONNX = "onnx"
    HUGGINGFACE = "huggingface"
    XGBOOST = "xgboost"
    CUSTOM = "custom"


class ModelTask(str, enum.Enum):
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    OBJECT_DETECTION = "object_detection"
    NLP_CLASSIFICATION = "nlp_classification"
    TEXT_GENERATION = "text_generation"
    IMAGE_SEGMENTATION = "image_segmentation"
    RECOMMENDATION = "recommendation"
    ANOMALY_DETECTION = "anomaly_detection"
    CUSTOM = "custom"


class ModelStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class MLModel(Base):
    __tablename__ = "ml_models"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(250), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    framework: Mapped[ModelFramework] = mapped_column(SAEnum(ModelFramework), nullable=False)
    task: Mapped[ModelTask] = mapped_column(SAEnum(ModelTask), nullable=False)
    status: Mapped[ModelStatus] = mapped_column(SAEnum(ModelStatus), default=ModelStatus.DRAFT)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    tags: Mapped[dict] = mapped_column(JSON, default=list)
    license: Mapped[str] = mapped_column(String(100), nullable=True)
    paper_url: Mapped[str] = mapped_column(String(500), nullable=True)
    github_url: Mapped[str] = mapped_column(String(500), nullable=True)
    download_count: Mapped[int] = mapped_column(Integer, default=0)
    inference_count: Mapped[int] = mapped_column(Integer, default=0)
    star_count: Mapped[int] = mapped_column(Integer, default=0)
    readme: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    owner = relationship("User", back_populates="models")
    versions = relationship("ModelVersion", back_populates="model", cascade="all, delete-orphan")
    deployments = relationship("ModelDeployment", back_populates="model", cascade="all, delete-orphan")


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ml_models.id"), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=True)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=True)
    checksum: Mapped[str] = mapped_column(String(128), nullable=True)
    metrics: Mapped[dict] = mapped_column(JSON, default=dict)
    hyperparameters: Mapped[dict] = mapped_column(JSON, default=dict)
    input_schema: Mapped[dict] = mapped_column(JSON, default=dict)
    output_schema: Mapped[dict] = mapped_column(JSON, default=dict)
    training_dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    changelog: Mapped[str] = mapped_column(Text, nullable=True)
    is_latest: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    model = relationship("MLModel", back_populates="versions")


class ModelDeployment(Base):
    __tablename__ = "model_deployments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ml_models.id"), nullable=False)
    version_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("model_versions.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    endpoint_url: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    replicas: Mapped[int] = mapped_column(Integer, default=1)
    cpu_limit: Mapped[str] = mapped_column(String(20), default="500m")
    memory_limit: Mapped[str] = mapped_column(String(20), default="512Mi")
    avg_latency_ms: Mapped[float] = mapped_column(Float, nullable=True)
    requests_per_second: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    model = relationship("MLModel", back_populates="deployments")
