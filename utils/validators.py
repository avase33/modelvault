"""
Validation helpers for ModelVault.
Ensures model artifacts and metadata conform to expected schemas before storage.
"""

import os
from pathlib import Path

SUPPORTED_FRAMEWORKS = {"pytorch", "tensorflow", "sklearn", "onnx", "jax", "keras"}
SUPPORTED_EXTENSIONS = {".pt", ".pth", ".pkl", ".joblib", ".h5", ".onnx", ".bin", ".safetensors"}


def validate_model_file(file_path: str) -> tuple[bool, str]:
    """
    Check that a model file exists and has a recognised extension.

    Returns:
        (is_valid, error_message) — error_message is empty string on success.
    """
    p = Path(file_path)
    if not p.exists():
        return False, f"File not found: {file_path}"
    if p.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported extension '{p.suffix}'. Supported: {SUPPORTED_EXTENSIONS}"
    if p.stat().st_size == 0:
        return False, "File is empty."
    return True, ""


def validate_version_string(version: str) -> bool:
    """Return True if version follows semantic versioning (MAJOR.MINOR.PATCH)."""
    parts = version.split(".")
    if len(parts) != 3:
        return False
    return all(part.isdigit() for part in parts)


def validate_framework(framework: str) -> bool:
    """Return True if the framework is in the supported set."""
    return framework.lower() in SUPPORTED_FRAMEWORKS


def validate_metadata(metadata: dict) -> tuple[bool, list[str]]:
    """
    Validate a metadata dictionary against required fields and constraints.

    Returns:
        (is_valid, list_of_errors)
    """
    errors = []
    required = ["name", "version", "framework", "file_path"]
    for field in required:
        if field not in metadata or not metadata[field]:
            errors.append(f"Missing or empty required field: '{field}'")

    if "version" in metadata and not validate_version_string(str(metadata["version"])):
        errors.append("'version' must follow semantic versioning (e.g. '1.0.0')")

    if "framework" in metadata and not validate_framework(str(metadata["framework"])):
        errors.append(f"'framework' must be one of: {SUPPORTED_FRAMEWORKS}")

    return len(errors) == 0, errors
