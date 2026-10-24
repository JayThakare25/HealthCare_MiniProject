"""
Unit tests for data splitting and preprocessing pipelines.
"""

import pytest
import numpy as np
import pandas as pd
from src.data_loader import get_clean_classification_data
from src.preprocessing import create_leakage_free_splits, get_processed_feature_matrix

def test_leakage_free_splits():
    clean_df = get_clean_classification_data("data/oasis_cross-sectional.csv")
    train_df, test_df = create_leakage_free_splits(clean_df, test_size=0.20, random_state=42)
    
    # 1. Total counts match
    assert len(train_df) + len(test_df) == len(clean_df)
    assert len(train_df) == 188
    assert len(test_df) == 47
    
    # 2. Strict participant isolation (zero intersection)
    overlap = set(train_df['ID']).intersection(set(test_df['ID']))
    assert len(overlap) == 0, f"Data leakage detected! Overlapping subjects: {overlap}"
    
    # 3. Class balance preserved
    train_prop = train_df['target'].mean()
    test_prop = test_df['target'].mean()
    assert abs(train_prop - test_prop) < 0.05

def test_preprocessing_pipeline_no_nan():
    clean_df = get_clean_classification_data("data/oasis_cross-sectional.csv")
    train_df, test_df = create_leakage_free_splits(clean_df, test_size=0.20, random_state=42)
    
    feature_cols = ["Age", "M/F", "Educ", "SES", "MMSE", "eTIV", "nWBV", "ASF"]
    X_train, X_test, y_train, y_test, preprocessor, feature_names = get_processed_feature_matrix(
        train_df, test_df, feature_cols
    )
    
    # Verify no NaN values in processed matrices
    assert not X_train.isnull().any().any(), "NaN found in X_train"
    assert not X_test.isnull().any().any(), "NaN found in X_test"
    
    # Verify shapes
    assert X_train.shape == (188, 8)
    assert X_test.shape == (47, 8)
    assert len(y_train) == 188
    assert len(y_test) == 47
