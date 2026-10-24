"""
Unit tests for metric computations.
"""

import pytest
import numpy as np
from src.utils import compute_all_metrics

def test_compute_all_metrics_perfect():
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.8, 0.9])
    
    metrics = compute_all_metrics(y_true, y_pred, y_prob)
    assert metrics["accuracy"] == 1.0
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["specificity"] == 1.0
    assert metrics["f1_score"] == 1.0
    assert metrics["balanced_accuracy"] == 1.0
    assert metrics["roc_auc"] == 1.0
    assert metrics["true_positives"] == 2
    assert metrics["true_negatives"] == 2
    assert metrics["false_positives"] == 0
    assert metrics["false_negatives"] == 0

def test_compute_all_metrics_known_imperfect():
    # 2 true negatives, 1 false positive, 1 false negative, 2 true positives
    # TN=2, FP=1, FN=1, TP=2 (Total = 6)
    # y_true = [0, 0, 0, 1, 1, 1]
    # y_pred = [0, 0, 1, 0, 1, 1]
    y_true = np.array([0, 0, 0, 1, 1, 1])
    y_pred = np.array([0, 0, 1, 0, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.6, 0.4, 0.8, 0.9])
    
    metrics = compute_all_metrics(y_true, y_pred, y_prob)
    assert metrics["accuracy"] == pytest.approx(4/6)
    assert metrics["precision"] == pytest.approx(2/3)
    assert metrics["recall"] == pytest.approx(2/3)
    assert metrics["specificity"] == pytest.approx(2/3)
    assert metrics["f1_score"] == pytest.approx(2/3)
    assert metrics["true_positives"] == 2
    assert metrics["true_negatives"] == 2
    assert metrics["false_positives"] == 1
    assert metrics["false_negatives"] == 1
