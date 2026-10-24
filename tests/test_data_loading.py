"""
Unit tests for data loading and dataset auditing.
"""

import pytest
import os
import pandas as pd
from src.data_loader import load_raw_oasis_data, audit_dataset, get_clean_classification_data

def test_load_raw_oasis_data():
    df = load_raw_oasis_data("data/oasis_cross-sectional.csv")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 436
    assert "ID" in df.columns
    assert "CDR" in df.columns
    assert "MMSE" in df.columns
    assert "nWBV" in df.columns

def test_audit_dataset():
    df = load_raw_oasis_data("data/oasis_cross-sectional.csv")
    audit = audit_dataset(df)
    assert audit["total_records"] == 436
    assert audit["unique_subjects"] == 436
    assert audit["clinically_evaluated_cohort_count"] == 235
    assert audit["unassessed_young_controls_count"] == 201
    assert audit["binary_class_counts"]["control_count"] == 135
    assert audit["binary_class_counts"]["dementia_indicative_count"] == 100

def test_get_clean_classification_data():
    clean_df = get_clean_classification_data("data/oasis_cross-sectional.csv")
    assert len(clean_df) == 235
    assert "target" in clean_df.columns
    assert set(clean_df["target"].unique()) == {0, 1}
    assert (clean_df["target"] == 0).sum() == 135
    assert (clean_df["target"] == 1).sum() == 100
