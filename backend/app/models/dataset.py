import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Integer, Text, ForeignKey, JSON, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.core.database import Base


class DatasetType(str, enum.Enum):
    TABULAR = "tabular"
    IMAGE = "image"
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    MULTIMODAL = "multimodal"
    TIME_SERIES = "time_series"


class DatasetStatus(str, enum.Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(250), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    dataset_type: Mapped[DatasetType] = mapped_column(SAEnum(DatasetType), nullable=False)
    status: Mapped[DatasetStatus] = mapped_column(SAEnum(DatasetStatus), default=DatasetStatus.UPLOADING)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    tags: Mapped[dict] = mapped_column(JSON, default=list)
    license: Mapped[str] = mapped_column(String(100), nullable=True)

    # Stats
    file_path: Mapped[str] = mapped_column(String(1000), nullable=True)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=True)
    num_rows: Mapped[int] = mapped_column(Integer, nullable=True)
    num_columns: Mapped[int] = mapped_column(Integer, nullable=True)
    num_files: Mapped[int] = mapped_column(Integer, nullable=True)
    schema_info: Mapped[dict] = mapped_column(JSON, default=dict)
    statistics: Mapped[dict] = mapped_column(JSON, default=dict)
    sample_data: Mapped[dict] = mapped_column(JSON, default=dict)

    download_count: Mapped[int] = mapped_column(Integer, default=0)
    readme: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    owner = relationship("User", back_populates="datasets")
