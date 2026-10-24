"""
Explainable AI (XAI) using SHAP (SHapley Additive exPlanations) on trained tree-based ensemble.
"""

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap

from src.utils import load_config, setup_logger, save_dataframe, save_json

logger = setup_logger()

# Publication styling
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

def run_shap_analysis():
    """
    Compute TreeExplainer SHAP values and generate publication figures.
    """
    config = load_config()
    metrics_dir = config["outputs"]["metrics_dir"]
    figures_dir = config["outputs"]["figures_dir"]
    os.makedirs(figures_dir, exist_ok=True)
    
    # Load model and data
    model_path = os.path.join(metrics_dir, "saved_models", "random_forest.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at: {model_path}. Please run train.py first.")
        
    model = joblib.load(model_path)
    X_train = pd.read_csv(os.path.join(metrics_dir, "X_train_processed.csv"))
    X_test = pd.read_csv(os.path.join(metrics_dir, "X_test_processed.csv"))
    y_test = np.load(os.path.join(metrics_dir, "y_test.npy"))
    
    # Create descriptive feature labels for visualization
    feature_rename_map = {
        "Age": "Age (Years)",
        "Educ": "Education Level (1-5)",
        "SES": "Socioeconomic Status (1-5)",
        "MMSE": "MMSE Cognitive Score (0-30)",
        "eTIV": "Estimated Total Intracranial Vol (eTIV)",
        "nWBV": "Normalized Whole Brain Vol (nWBV)",
        "ASF": "Atlas Scaling Factor (ASF)",
        "M/F_M": "Gender (Male = 1, Female = 0)"
    }
    
    X_test_renamed = X_test.rename(columns=feature_rename_map)
    feature_names_display = list(X_test_renamed.columns)
    
    logger.info("Initializing SHAP TreeExplainer for Random Forest...")
    explainer = shap.TreeExplainer(model)
    
    # Compute SHAP values
    shap_values = explainer.shap_values(X_test)
    
    # Handle multidimensional output formats across SHAP versions
    # For binary classification: class 1 (Demented) is usually shap_values[1] or shap_values[:, :, 1]
    if isinstance(shap_values, list):
        # List of length 2 [class 0, class 1]
        shap_vals_class1 = shap_values[1]
        expected_val = explainer.expected_value[1] if hasattr(explainer.expected_value, '__len__') else explainer.expected_value
    elif isinstance(shap_values, np.ndarray) and len(shap_values.shape) == 3:
        # Array of shape (n_samples, n_features, 2)
        shap_vals_class1 = shap_values[:, :, 1]
        expected_val = explainer.expected_value[1] if hasattr(explainer.expected_value, '__len__') else explainer.expected_value
    else:
        shap_vals_class1 = shap_values
        expected_val = explainer.expected_value
        
    logger.info(f"SHAP values computed: shape={shap_vals_class1.shape}")
    
    # 1. Compute Mean Absolute SHAP Importance
    mean_abs_shap = np.mean(np.abs(shap_vals_class1), axis=0)
    importance_df = pd.DataFrame({
        "feature_raw": X_test.columns,
        "feature_name": feature_names_display,
        "mean_abs_shap": mean_abs_shap
    }).sort_values(by="mean_abs_shap", ascending=False)
    
    save_dataframe(importance_df, os.path.join(metrics_dir, "shap_feature_importance.csv"))
    save_json(importance_df.to_dict(orient="records"), os.path.join(metrics_dir, "shap_feature_importance.json"))
    
    # 2. Global SHAP Bar Plot
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    y_pos = np.arange(len(importance_df))
    sorted_df = importance_df.sort_values(by="mean_abs_shap", ascending=True)
    ax.barh(np.arange(len(sorted_df)), sorted_df['mean_abs_shap'], color="#008080", edgecolor='black', alpha=0.9)
    ax.set_yticks(np.arange(len(sorted_df)))
    ax.set_yticklabels(sorted_df['feature_name'], fontsize=11)
    ax.set_xlabel("Mean |SHAP Value| (Impact on Model Log-Odds Output)", fontsize=12)
    ax.set_title("Global Feature Importance (SHAP Analysis)", fontsize=13, fontweight='bold', pad=12)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    for i, v in enumerate(sorted_df['mean_abs_shap']):
        ax.text(v + 0.005, i, f"{v:.4f}", va='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    bar_path = os.path.join(figures_dir, "shap_global_bar.png")
    plt.savefig(bar_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved SHAP bar plot to {bar_path}")
    
    # 3. Global Beeswarm / Summary Plot
    fig = plt.figure(figsize=(10, 6), dpi=300)
    shap.summary_plot(
        shap_vals_class1,
        X_test_renamed,
        plot_type="dot",
        show=False,
        alpha=0.85
    )
    plt.title("SHAP Beeswarm Summary: Feature Impact on Dementia Classification", fontsize=13, fontweight='bold', pad=14)
    plt.xlabel("SHAP Value (Impact on Dementia Likelihood)", fontsize=11)
    plt.tight_layout()
    summary_path = os.path.join(figures_dir, "shap_summary_beeswarm.png")
    plt.savefig(summary_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved SHAP summary beeswarm plot to {summary_path}")
    
    # 4. Local Explanation: High Risk Demented Patient (True Positive)
    # Find patient with highest probability of dementia
    y_prob = model.predict_proba(X_test)[:, 1]
    tp_indices = np.where((y_test == 1) & (y_prob > 0.8))[0]
    idx_tp = tp_indices[0] if len(tp_indices) > 0 else 0
    
    # Find patient with lowest probability of dementia (True Negative)
    tn_indices = np.where((y_test == 0) & (y_prob < 0.2))[0]
    idx_tn = tn_indices[0] if len(tn_indices) > 0 else 1
    
    # Create Explanation objects for waterfall plots
    explanation_tp = shap.Explanation(
        values=shap_vals_class1[idx_tp],
        base_values=expected_val,
        data=X_test_renamed.iloc[idx_tp].values,
        feature_names=feature_names_display
    )
    
    fig = plt.figure(figsize=(9, 5.5), dpi=300)
    shap.plots.waterfall(explanation_tp, show=False)
    plt.title(f"Local Patient Explanation: Demented Patient (Pred Prob={y_prob[idx_tp]:.2f}, True=1)", fontsize=12, fontweight='bold', pad=10)
    plt.tight_layout()
    tp_path = os.path.join(figures_dir, "shap_waterfall_demented.png")
    plt.savefig(tp_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved local demented explanation to {tp_path}")
    
    explanation_tn = shap.Explanation(
        values=shap_vals_class1[idx_tn],
        base_values=expected_val,
        data=X_test_renamed.iloc[idx_tn].values,
        feature_names=feature_names_display
    )
    
    fig = plt.figure(figsize=(9, 5.5), dpi=300)
    shap.plots.waterfall(explanation_tn, show=False)
    plt.title(f"Local Patient Explanation: Normal Control (Pred Prob={y_prob[idx_tn]:.2f}, True=0)", fontsize=12, fontweight='bold', pad=10)
    plt.tight_layout()
    tn_path = os.path.join(figures_dir, "shap_waterfall_control.png")
    plt.savefig(tn_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved local control explanation to {tn_path}")
    
    # 5. Dependence Plot: nWBV (Normalized Whole Brain Volume)
    fig, ax = plt.subplots(figsize=(7.5, 5), dpi=300)
    nwbv_idx = list(X_test.columns).index("nWBV")
    ax.scatter(X_test["nWBV"], shap_vals_class1[:, nwbv_idx], color="#1B365D", alpha=0.85, edgecolors='black', s=55)
    ax.axhline(0, color='gray', linestyle='--', alpha=0.7)
    ax.set_title("SHAP Dependence Plot: Normalized Whole Brain Volume (nWBV)", fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel("Normalized Whole Brain Volume (Standardized z-score)", fontsize=11)
    ax.set_ylabel("SHAP Value for Dementia Class", fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    dep_nwbv_path = os.path.join(figures_dir, "shap_dependence_nwbv.png")
    plt.savefig(dep_nwbv_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved nWBV dependence plot to {dep_nwbv_path}")
    
    # 6. Dependence Plot: MMSE
    fig, ax = plt.subplots(figsize=(7.5, 5), dpi=300)
    mmse_idx = list(X_test.columns).index("MMSE")
    ax.scatter(X_test["MMSE"], shap_vals_class1[:, mmse_idx], color="#E05A47", alpha=0.85, edgecolors='black', s=55)
    ax.axhline(0, color='gray', linestyle='--', alpha=0.7)
    ax.set_title("SHAP Dependence Plot: MMSE Cognitive Examination Score", fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel("MMSE Score (Standardized z-score)", fontsize=11)
    ax.set_ylabel("SHAP Value for Dementia Class", fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    dep_mmse_path = os.path.join(figures_dir, "shap_dependence_mmse.png")
    plt.savefig(dep_mmse_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved MMSE dependence plot to {dep_mmse_path}")

    print("\n" + "="*60)
    print("SHAP EXPLAINABILITY ANALYSIS COMPLETED")
    print("Top Predictive Biomarkers by Mean |SHAP|:")
    for idx, row in importance_df.iterrows():
        print(f"  {row['feature_name']}: {row['mean_abs_shap']:.4f}")
    print(f"Figures saved to: {figures_dir}")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_shap_analysis()
