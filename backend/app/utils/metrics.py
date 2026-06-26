# ML metrics utilities -- 2026-06-26 09:08:03
import numpy as np
from typing import List, Optional, Dict
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, r2_score,
    roc_auc_score, confusion_matrix, classification_report
)

def classification_metrics(y_true: List, y_pred: List, y_prob: Optional[List] = None) -> Dict:
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
    }
    if y_prob is not None:
        try:
            metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob, multi_class="ovr", average="weighted"))
        except Exception:
            pass
    return metrics

def regression_metrics(y_true: List, y_pred: List) -> Dict:
    y_true_arr = np.array(y_true)
    y_pred_arr = np.array(y_pred)
    mse = mean_squared_error(y_true_arr, y_pred_arr)
    return {
        "mse": float(mse),
        "rmse": float(np.sqrt(mse)),
        "mae": float(mean_absolute_error(y_true_arr, y_pred_arr)),
        "r2": float(r2_score(y_true_arr, y_pred_arr)),
        "mape": float(np.mean(np.abs((y_true_arr - y_pred_arr) / (y_true_arr + 1e-8))) * 100),
    }

def compute_drift_score(reference: List[float], current: List[float]) -> float:
    ref = np.array(reference)
    cur = np.array(current)
    ref_mean, ref_std = ref.mean(), ref.std() + 1e-8
    cur_mean = cur.mean()
    return float(abs(cur_mean - ref_mean) / ref_std)