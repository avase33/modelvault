# Model registry service -- 2026-06-26 09:03:30
import os
import json
import joblib
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

ARTIFACT_DIR = Path(os.getenv("ARTIFACT_DIR", "./artifacts"))

class ModelRegistry:
    def __init__(self):
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    def save_artifact(self, model_id: str, model_obj: Any, metadata: Dict) -> str:
        model_dir = ARTIFACT_DIR / model_id
        model_dir.mkdir(exist_ok=True)
        artifact_path = model_dir / "model.joblib"
        joblib.dump(model_obj, artifact_path)
        meta_path = model_dir / "metadata.json"
        metadata["saved_at"] = datetime.utcnow().isoformat()
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2)
        return str(artifact_path)

    def load_artifact(self, model_id: str) -> Any:
        artifact_path = ARTIFACT_DIR / model_id / "model.joblib"
        if not artifact_path.exists():
            raise FileNotFoundError(f"Artifact not found for model {model_id}")
        return joblib.load(artifact_path)

    def get_metadata(self, model_id: str) -> Optional[Dict]:
        meta_path = ARTIFACT_DIR / model_id / "metadata.json"
        if not meta_path.exists():
            return None
        with open(meta_path) as f:
            return json.load(f)

    def list_artifacts(self):
        return [d.name for d in ARTIFACT_DIR.iterdir() if d.is_dir()]

    def delete_artifact(self, model_id: str) -> bool:
        import shutil
        model_dir = ARTIFACT_DIR / model_id
        if model_dir.exists():
            shutil.rmtree(model_dir)
            return True
        return False

registry = ModelRegistry()