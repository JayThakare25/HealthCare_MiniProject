"""
Feature engineering and modality subset partitioning for clinical and neuroimaging data.
"""

import pandas as pd
import numpy as np

def get_modality_feature_sets():
    """
    Returns verified feature columns for:
    1. Clinical-only: Demographic and psychometric cognitive evaluation variables.
    2. Structural MRI-only: Quantitative brain volumetric and stereotaxic atlas scaling factors.
    3. Multimodal: Joint integration of clinical psychometrics and structural neuroimaging.
    """
    clinical_features = ["Age", "M/F", "Educ", "SES", "MMSE"]
    mri_features = ["eTIV", "nWBV", "ASF"]
    combined_features = ["Age", "M/F", "Educ", "SES", "MMSE", "eTIV", "nWBV", "ASF"]
    
    return {
        "clinical_only": clinical_features,
        "mri_only": mri_features,
        "multimodal_combined": combined_features
    }

def add_derived_morphometric_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes biologically grounded derived morphometric features:
    - Atrophy_Index: 1.0 - nWBV (fraction of intracranial space lost to brain parenchymal atrophy / CSF expansion)
    - Brain_Parenchyma_Volume_Est: eTIV * nWBV (absolute estimated brain tissue volume in cm3/mm3)
    """
    df_feat = df.copy()
    if 'nWBV' in df_feat.columns:
        df_feat['Atrophy_Index'] = 1.0 - df_feat['nWBV']
    if 'eTIV' in df_feat.columns and 'nWBV' in df_feat.columns:
        df_feat['Brain_Tissue_Vol_Est'] = df_feat['eTIV'] * df_feat['nWBV']
    return df_feat
