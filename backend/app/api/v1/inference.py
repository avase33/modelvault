from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
import time
from typing import Dict, Any

from app.core.database import get_db
from app.models.user import User
from app.models.ml_model import MLModel, ModelVersion
from app.schemas.ml_model import InferenceRequest, InferenceResponse
from app.api.deps import get_current_user_or_api_key

router = APIRouter(prefix="/inference", tags=["Inference"])


@router.post("/{model_id}/predict", response_model=InferenceResponse)
async def predict(
    model_id: str,
    request: InferenceRequest,
    current_user: User = Depends(get_current_user_or_api_key),
    db: AsyncSession = Depends(get_db),
):
    """Run inference on a deployed model."""
    result = await db.execute(select(MLModel).where(MLModel.id == model_id))
    model = result.scalar_one_or_none()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    if not model.is_public and model.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Get latest version
    result = await db.execute(
        select(ModelVersion).where(
            ModelVersion.model_id == model_id, ModelVersion.is_latest == True
        )
    )
    version = result.scalar_one_or_none()
    if not version:
        raise HTTPException(status_code=404, detail="No model version found")

    start = time.perf_counter()

    # Mock inference — in production: load model and run
    outputs = _mock_inference(model.task.value, request.inputs)

    latency_ms = (time.perf_counter() - start) * 1000

    # Increment inference count
    model.inference_count += 1
    await db.commit()

    return InferenceResponse(
        model_id=model_id,
        version=version.version,
        outputs=outputs,
        latency_ms=round(latency_ms, 3),
        timestamp=datetime.now(timezone.utc),
    )


def _mock_inference(task: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Placeholder inference — replace with real model loading."""
    if task == "classification":
        return {"label": "class_0", "confidence": 0.92, "probabilities": {"class_0": 0.92, "class_1": 0.08}}
    elif task == "regression":
        return {"prediction": 42.7, "uncertainty": 1.2}
    elif task == "text_generation":
        return {"generated_text": "This is a generated response from the model.", "tokens": 12}
    elif task == "object_detection":
        return {"detections": [{"label": "object", "confidence": 0.87, "bbox": [10, 20, 100, 150]}]}
    else:
        return {"result": "ok", "inputs_received": len(inputs)}


@router.get("/{model_id}/stats")
async def inference_stats(
    model_id: str,
    current_user: User = Depends(get_current_user_or_api_key),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(MLModel).where(MLModel.id == model_id))
    model = result.scalar_one_or_none()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return {
        "model_id": model_id,
        "total_inferences": model.inference_count,
        "total_downloads": model.download_count,
    }
