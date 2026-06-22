"""
ModelVault -- Model Performance Metrics Utilities
"""

from typing import List
import math


def accuracy(y_true: List[int], y_pred: List[int]) -> float:
    """Compute classification accuracy."""
    if not y_true:
        return 0.0
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    return round(correct / len(y_true), 4)


def precision_recall_f1(y_true: List[int], y_pred: List[int], positive_label: int = 1) -> dict:
    """Compute precision, recall, and F1 score."""
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == positive_label and p == positive_label)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t != positive_label and p == positive_label)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == positive_label and p != positive_label)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    return {"precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}


def rmse(y_true: List[float], y_pred: List[float]) -> float:
    """Root Mean Squared Error."""
    if not y_true:
        return 0.0
    mse = sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / len(y_true)
    return round(math.sqrt(mse), 4)


def mae(y_true: List[float], y_pred: List[float]) -> float:
    """Mean Absolute Error."""
    if not y_true:
        return 0.0
    return round(sum(abs(t - p) for t, p in zip(y_true, y_pred)) / len(y_true), 4)


def format_metric_report(metrics: dict, model_name: str = "Model") -> str:
    """Format metrics dict into a readable report."""
    lines = [f"=== {model_name} Performance Report ==="]
    for k, v in metrics.items():
        label = k.replace("_", " ").title()
        value = f"{v:.4f}" if isinstance(v, float) else str(v)
        lines.append(f"  {label:<20} {value}")
    return "\n".join(lines)
