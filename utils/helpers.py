"""
Utility helpers for ModelVault.
Provides common operations for model file management and metadata handling.
"""

import os
import hashlib
import json
from datetime import datetime
from pathlib import Path


def compute_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """
    Compute a cryptographic hash of a file.

    Args:
        file_path: Path to the file.
        algorithm: Hash algorithm to use ('sha256', 'md5', etc.).

    Returns:
        Hexadecimal digest string.
    """
    h = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def get_model_size_mb(file_path: str) -> float:
    """Return the size of a model file in megabytes."""
    return os.path.getsize(file_path) / (1024 * 1024)


def build_model_metadata(
    name: str, version: str, file_path: str, framework: str, tags: list[str] | None = None
) -> dict:
    """
    Build a standardised metadata dictionary for a model artifact.

    Args:
        name: Human-readable model name.
        version: Semantic version string (e.g. '1.0.0').
        file_path: Absolute or relative path to the model file.
        framework: ML framework used (e.g. 'pytorch', 'tensorflow', 'sklearn').
        tags: Optional list of descriptor tags.

    Returns:
        Metadata dict ready for JSON serialisation.
    """
    return {
        "name": name,
        "version": version,
        "framework": framework,
        "file_path": str(Path(file_path).resolve()),
        "file_size_mb": get_model_size_mb(file_path) if os.path.exists(file_path) else None,
        "sha256": compute_file_hash(file_path) if os.path.exists(file_path) else None,
        "tags": tags or [],
        "created_at": datetime.utcnow().isoformat() + "Z",
    }


def save_metadata(metadata: dict, output_path: str) -> None:
    """Serialise model metadata to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def load_metadata(metadata_path: str) -> dict:
    """Load model metadata from a JSON file."""
    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)
