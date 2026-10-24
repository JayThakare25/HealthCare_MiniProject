"""
Data loading and dataset auditing for OASIS-1 Cross-Sectional MRI study.
"""

import os
import pandas as pd
import numpy as np
from src.utils import load_config, setup_logger, save_json

logger = setup_logger()

def load_raw_oasis_data(csv_path: str = "data/oasis_cross-sectional.csv") -> pd.DataFrame:
    """Load raw OASIS-1 cross-sectional CSV dataset."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset CSV not found at: {csv_path}")
    df = pd.read_csv(csv_path)
    logger.info(f"Loaded raw dataset with {len(df)} records and {len(df.columns)} columns.")
    return df

def audit_dataset(df: pd.DataFrame) -> dict:
    """
    Perform rigorous dataset audit verifying subject counts, clinical cohorts,
    missing values, and demographic distributions without fabricating any statistics.
    """
    total_records = len(df)
    unique_subjects = df['ID'].nunique()
    
    # Analyze CDR availability
    evaluated_mask = df['CDR'].notna()
    young_controls_mask = df['CDR'].isna()
    
    evaluated_df = df[evaluated_mask].copy()
    young_df = df[young_controls_mask].copy()
    
    cdr_dist = df['CDR'].value_counts(dropna=False).to_dict()
    # Convert keys to string for JSON serialization
    cdr_dist_str = {str(k): int(v) for k, v in cdr_dist.items()}
    
    evaluated_cdr_dist = evaluated_df['CDR'].value_counts().to_dict()
    evaluated_cdr_dist_str = {str(k): int(v) for k, v in evaluated_cdr_dist.items()}
    
    # Binary target breakdown in evaluated cohort
    n_control = int((evaluated_df['CDR'] == 0.0).sum())
    n_dementia = int((evaluated_df['CDR'] > 0.0).sum())
    
    audit_results = {
        "dataset_name": "OASIS-1 Cross-Sectional MRI Dataset",
        "official_source": "https://www.oasis-brains.org/#oasis1",
        "citation": "Marcus et al., J. Cognitive Neuroscience, 2007",
        "total_records": total_records,
        "unique_subjects": unique_subjects,
        "unassessed_young_controls_count": int(young_controls_mask.sum()),
        "unassessed_young_age_range": [float(young_df['Age'].min()), float(young_df['Age'].max())],
        "clinically_evaluated_cohort_count": int(evaluated_mask.sum()),
        "evaluated_age_range": [float(evaluated_df['Age'].min()), float(evaluated_df['Age'].max())],
        "cdr_distribution_full": cdr_dist_str,
        "cdr_distribution_evaluated": evaluated_cdr_dist_str,
        "binary_target_definition": {
            "negative_class_0": "Control / Nondemented (CDR = 0.0)",
            "positive_class_1": "Dementia-Indicative (CDR > 0.0: 0.5 Very Mild, 1.0 Mild, 2.0 Moderate)"
        },
        "binary_class_counts": {
            "control_count": n_control,
            "dementia_indicative_count": n_dementia,
            "control_ratio": round(n_control / len(evaluated_df), 4),
            "dementia_ratio": round(n_dementia / len(evaluated_df), 4)
        },
        "gender_breakdown_evaluated": {
            str(k): int(v) for k, v in evaluated_df['M/F'].value_counts().items()
        },
        "missing_values_evaluated": {
            k: int(v) for k, v in evaluated_df.isnull().sum().items()
        },
        "morphometric_variables": {
            "eTIV": "Estimated Total Intracranial Volume (cm3 / mm3)",
            "nWBV": "Normalized Whole Brain Volume (proportion of total intracranial volume)",
            "ASF": "Atlas Scaling Factor (scaling factor required to transform brain to Talairach atlas space)"
        },
        "clinical_variables": {
            "Age": "Subject age in years",
            "M/F": "Gender (M: Male, F: Female)",
            "Educ": "Education level (1 to 5)",
            "SES": "Socioeconomic status (1 to 5, Hollingshead Index)",
            "MMSE": "Mini-Mental State Examination score (0 to 30)"
        }
    }
    return audit_results

def get_clean_classification_data(csv_path: str = "data/oasis_cross-sectional.csv") -> pd.DataFrame:
    """
    Extract and format the clean cohort for the binary dementia classification task.
    Filters to subjects with verified CDR evaluations, creates target column, and
    preserves ID for participant-level splitting.
    """
    df = load_raw_oasis_data(csv_path)
    
    # Filter to clinically assessed cohort
    clean_df = df[df['CDR'].notna()].copy()
    
    # Define binary target
    clean_df['target'] = (clean_df['CDR'] > 0.0).astype(int)
    
    logger.info(
        f"Filtered evaluated cohort: {len(clean_df)} subjects "
        f"({(clean_df['target'] == 0).sum()} Controls, {(clean_df['target'] == 1).sum()} Dementia-Indicative)"
    )
    return clean_df

if __name__ == "__main__":
    config = load_config()
    raw_path = config["data"]["raw_csv_path"]
    df = load_raw_oasis_data(raw_path)
    audit = audit_dataset(df)
    
    metrics_dir = config["outputs"]["metrics_dir"]
    audit_file = os.path.join(metrics_dir, "dataset_audit.json")
    save_json(audit, audit_file)
    
    print("\n" + "="*60)
    print("OASIS-1 DATASET AUDIT SUMMARY")
    print("="*60)
    print(f"Total Records: {audit['total_records']}")
    print(f"Clinically Evaluated Cohort: {audit['clinically_evaluated_cohort_count']} subjects")
    print(f"  - Non-Demented Controls (CDR = 0): {audit['binary_class_counts']['control_count']} ({audit['binary_class_counts']['control_ratio']*100:.1f}%)")
    print(f"  - Dementia-Indicative (CDR > 0): {audit['binary_class_counts']['dementia_indicative_count']} ({audit['binary_class_counts']['dementia_ratio']*100:.1f}%)")
    print(f"Young Controls (Unassessed CDR): {audit['unassessed_young_controls_count']} (Ages {audit['unassessed_young_age_range'][0]}-{audit['unassessed_young_age_range'][1]})")
    print(f"Missing Values in Evaluated Cohort: {audit['missing_values_evaluated']}")
    print(f"Audit saved to: {audit_file}")
    print("="*60 + "\n")
