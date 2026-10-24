"""
Utility functions for configuration, logging, metrics computation, and serialization.
"""

import os
import json
import yaml
import logging
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    balanced_accuracy_score,
    average_precision_score
)

def load_config(config_path: str = "config/experiment_config.yaml") -> dict:
    """Load YAML experiment configuration."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config

def setup_logger(log_file: str = "results/logs/experiment.log") -> logging.Logger:
    """Initialize structured logger."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger("AlzheimerML")
    logger.setLevel(logging.INFO)
    
    # Avoid adding duplicate handlers
    if not logger.handlers:
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(log_file, encoding="utf-8")
        
        fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        c_handler.setFormatter(fmt)
        f_handler.setFormatter(fmt)
        
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
    return logger

def compute_all_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray = None) -> dict:
    """
    Calculate comprehensive evaluation metrics from genuine predictions.
    
    Metrics:
      - Accuracy
      - Precision (Positive class = 1, Demented)
      - Recall / Sensitivity (True Positive Rate)
      - Specificity (True Negative Rate)
      - F1-score
      - Balanced Accuracy
      - ROC-AUC (if probabilities provided)
      - PR-AUC (Average Precision)
      - Confusion Matrix entries (TP, TN, FP, FN)
    """
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "specificity": float(specificity),
        "f1_score": float(f1_score(y_true, y_pred, zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "true_positives": int(tp),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "total_samples": int(len(y_true))
    }
    
    if y_prob is not None:
        try:
            metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob))
            metrics["pr_auc"] = float(average_precision_score(y_true, y_prob))
        except Exception:
            metrics["roc_auc"] = None
            metrics["pr_auc"] = None
    else:
        metrics["roc_auc"] = None
        metrics["pr_auc"] = None
        
    return metrics

def save_json(data: dict, filepath: str):
    """Save dictionary as formatted JSON."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
def save_dataframe(df: pd.DataFrame, filepath: str):
    """Save pandas DataFrame to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
