"""
Preprocessing and leakage-free dataset splitting for Alzheimer's ML pipeline.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.utils import load_config, setup_logger

logger = setup_logger()

def create_leakage_free_splits(
    df: pd.DataFrame,
    test_size: float = 0.20,
    random_state: int = 42,
    target_col: str = "target"
):
    """
    Split dataset strictly at the participant level to prevent data leakage.
    Ensures that no participant appears in both training and testing partitions.
    """
    # Verify participant uniqueness
    if df['ID'].nunique() != len(df):
        logger.warning("Duplicate subject IDs detected! Performing grouped participant split.")
        unique_ids = df['ID'].unique()
        id_train, id_test = train_test_split(
            unique_ids, test_size=test_size, random_state=random_state
        )
        train_df = df[df['ID'].isin(id_train)].copy()
        test_df = df[df['ID'].isin(id_test)].copy()
    else:
        train_df, test_df = train_test_split(
            df,
            test_size=test_size,
            random_state=random_state,
            stratify=df[target_col]
        )
        train_df = train_df.copy()
        test_df = test_df.copy()
        
    logger.info(
        f"Data split completed: Train={len(train_df)} subjects, Test={len(test_df)} subjects. "
        f"Train target dist: {dict(train_df[target_col].value_counts())}, "
        f"Test target dist: {dict(test_df[target_col].value_counts())}"
    )
    return train_df, test_df

def build_preprocessor(numerical_cols: list, categorical_cols: list) -> ColumnTransformer:
    """
    Build a scikit-learn ColumnTransformer that fits imputation and scaling
    strictly on training data.
    """
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_pipeline, numerical_cols),
            ('cat', cat_pipeline, categorical_cols)
        ],
        remainder='drop'
    )
    return preprocessor

def get_processed_feature_matrix(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    feature_cols: list,
    categorical_cols: list = None
):
    """
    Fits preprocessor on train_df feature columns and transforms both train and test.
    Returns X_train, X_test as DataFrames with informative column names, and y_train, y_test as Series.
    """
    if categorical_cols is None:
        categorical_cols = ["M/F"] if "M/F" in feature_cols else []
        
    num_cols = [c for c in feature_cols if c not in categorical_cols]
    cat_cols = [c for c in feature_cols if c in categorical_cols]
    
    preprocessor = build_preprocessor(num_cols, cat_cols)
    
    # Fit strictly on train
    X_train_arr = preprocessor.fit_transform(train_df[feature_cols])
    X_test_arr = preprocessor.transform(test_df[feature_cols])
    
    # Generate feature names
    feature_names = []
    if num_cols:
        feature_names.extend(num_cols)
    if cat_cols:
        # e.g., M/F -> M/F_M
        cat_encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
        encoded_cat_names = cat_encoder.get_feature_names_out(cat_cols)
        feature_names.extend(list(encoded_cat_names))
        
    X_train = pd.DataFrame(X_train_arr, columns=feature_names, index=train_df.index)
    X_test = pd.DataFrame(X_test_arr, columns=feature_names, index=test_df.index)
    
    y_train = train_df['target'].values
    y_test = test_df['target'].values
    
    return X_train, X_test, y_train, y_test, preprocessor, feature_names
