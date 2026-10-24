"""
Evaluation and scientific visualization generator for Alzheimer's ML experiment.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, confusion_matrix

from src.utils import load_config, setup_logger

logger = setup_logger()

# Set high-quality publication styling
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

PALETTE = {
    "navy": "#1B365D",
    "teal": "#008080",
    "coral": "#E05A47",
    "gold": "#D4AF37",
    "purple": "#6A4C93",
    "gray": "#6C757D"
}

def plot_dataset_distribution(output_dir: str):
    """Plot OASIS-1 clinical cohort and dementia severity distribution."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
    
    # Left: Evaluated vs Young cohort
    cohort_labels = ['Clinically Evaluated\n(Age 60-96, CDR Assessed)', 'Young Normal Controls\n(Age 18-59, CDR NaN)']
    cohort_counts = [235, 201]
    axes[0].bar(cohort_labels, cohort_counts, color=[PALETTE["navy"], PALETTE["teal"]], width=0.5, edgecolor='black', alpha=0.9)
    axes[0].set_title("OASIS-1 Cohort Composition (N = 436)", fontsize=13, fontweight='bold', pad=12)
    axes[0].set_ylabel("Number of Participants", fontsize=11)
    for i, v in enumerate(cohort_counts):
        axes[0].text(i, v + 4, f"{v} ({v/436*100:.1f}%)", ha='center', fontsize=10, fontweight='bold')
    axes[0].set_ylim(0, 270)
    axes[0].grid(axis='y', linestyle='--', alpha=0.5)
    
    # Right: Severity breakdown in evaluated cohort
    severity_labels = ['Control\nCDR 0.0', 'Very Mild\nCDR 0.5', 'Mild\nCDR 1.0', 'Moderate\nCDR 2.0']
    severity_counts = [135, 70, 28, 2]
    colors = [PALETTE["teal"], "#E5A93C", PALETTE["coral"], "#8B0000"]
    bars = axes[1].bar(severity_labels, severity_counts, color=colors, width=0.55, edgecolor='black', alpha=0.9)
    axes[1].set_title("Clinical Dementia Rating (CDR) Severity (N = 235)", fontsize=13, fontweight='bold', pad=12)
    axes[1].set_ylabel("Number of Participants", fontsize=11)
    for bar in bars:
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 3, f"{int(height)}", ha='center', fontsize=10, fontweight='bold')
    axes[1].set_ylim(0, 160)
    axes[1].grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "dataset_distribution.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved dataset distribution plot to {fig_path}")

def plot_roc_curves(pred_df: pd.DataFrame, output_dir: str):
    """Plot multi-model ROC Curves from authentic predictions."""
    y_true = pred_df['y_true'].values
    
    prob_cols = [c for c in pred_df.columns if c.endswith("_prob")]
    
    fig, ax = plt.subplots(figsize=(8, 6.5), dpi=300)
    
    color_map = {
        "Logistic Regression": PALETTE["navy"],
        "Random Forest": PALETTE["teal"],
        "Support Vector Machine": PALETTE["gold"],
        "Gradient Boosting": PALETTE["coral"],
        "Soft Voting Ensemble": PALETTE["purple"],
        "Dummy (Baseline)": PALETTE["gray"]
    }
    
    # Plot baseline diagonal
    ax.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Random Guess (AUC = 0.500)')
    
    for col in prob_cols:
        model_name = col.replace("_prob", "")
        y_prob = pred_df[col].values
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        roc_auc = auc(fpr, tpr)
        color = color_map.get(model_name, PALETTE["navy"])
        lw = 2.4 if "Ensemble" in model_name or "Gradient" in model_name else 1.8
        ax.plot(fpr, tpr, label=f"{model_name} (AUC = {roc_auc:.3f})", color=color, linewidth=lw)
        
    ax.set_title("ROC Curves on Held-Out Test Cohort (N = 47)", fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=12)
    ax.set_ylabel("True Positive Rate (Sensitivity / Recall)", fontsize=12)
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc="lower right", frameon=True, fontsize=10, shadow=True)
    
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "roc_curves.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved ROC curves plot to {fig_path}")

def plot_confusion_matrices(pred_df: pd.DataFrame, output_dir: str):
    """Plot 2x3 confusion matrix grid for all models."""
    y_true = pred_df['y_true'].values
    pred_cols = [c for c in pred_df.columns if c.endswith("_pred")]
    
    fig, axes = plt.subplots(2, 3, figsize=(14, 8.5), dpi=300)
    axes = axes.flatten()
    
    for i, col in enumerate(pred_cols):
        model_name = col.replace("_pred", "")
        y_pred = pred_df[col].values
        cm = confusion_matrix(y_true, y_pred)
        
        sns.heatmap(
            cm, annot=True, fmt='d', cmap='Blues', ax=axes[i],
            cbar=False, annot_kws={'size': 14, 'weight': 'bold'},
            xticklabels=['Control (0)', 'Demented (1)'],
            yticklabels=['Control (0)', 'Demented (1)']
        )
        axes[i].set_title(f"{model_name}", fontsize=12, fontweight='bold', pad=8)
        axes[i].set_xlabel("Predicted Diagnosis", fontsize=10)
        axes[i].set_ylabel("True Diagnosis", fontsize=10)
        
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "confusion_matrices.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved confusion matrices to {fig_path}")

def plot_comparative_metrics_bar(metrics_file: str, output_dir: str):
    """Plot grouped bar chart for comparative model performance."""
    df = pd.read_csv(metrics_file)
    
    # Filter out dummy for cleaner comparison chart or keep all
    df_eval = df[df['model'] != "Dummy (Baseline)"].copy()
    
    metrics = ["accuracy", "precision", "recall", "specificity", "f1_score", "roc_auc"]
    metric_labels = ["Accuracy", "Precision", "Recall", "Specificity", "F1-Score", "ROC-AUC"]
    
    x = np.arange(len(df_eval['model']))
    width = 0.13
    
    fig, ax = plt.subplots(figsize=(14, 6.5), dpi=300)
    
    colors = [PALETTE["navy"], PALETTE["teal"], PALETTE["coral"], PALETTE["gold"], PALETTE["purple"], "#4A90E2"]
    
    for i, m in enumerate(metrics):
        offset = (i - len(metrics)/2 + 0.5) * width
        rects = ax.bar(x + offset, df_eval[m], width, label=metric_labels[i], color=colors[i], edgecolor='black', alpha=0.85)
        
    ax.set_title("Comparative Model Performance on Held-Out Test Set (N = 47)", fontsize=14, fontweight='bold', pad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(df_eval['model'], fontsize=11, fontweight='bold')
    ax.set_ylabel("Metric Score", fontsize=12)
    ax.set_ylim([0.5, 1.02])
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(loc='lower left', ncol=6, fontsize=9.5, frameon=True)
    
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "comparative_metrics_bar.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved comparative metrics bar chart to {fig_path}")

def plot_modality_comparison(modality_file: str, output_dir: str):
    """Plot modality comparison (Clinical vs MRI vs Multimodal Combined)."""
    df = pd.read_csv(modality_file)
    
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
    
    for i, clf in enumerate(["Random Forest", "Logistic Regression"]):
        sub = df[df['classifier'] == clf].copy()
        
        # Replace modality names with human-readable labels
        labels = {
            "clinical_only": "Clinical Only\n(Age, Sex, Educ, SES, MMSE)",
            "mri_only": "Structural MRI Only\n(eTIV, nWBV, ASF)",
            "multimodal_combined": "Multimodal Combined\n(Clinical + MRI)"
        }
        sub['label'] = sub['modality'].map(labels)
        
        x = np.arange(len(sub))
        w = 0.22
        
        axes[i].bar(x - w, sub['accuracy'], w, label='Accuracy', color=PALETTE["navy"], edgecolor='black')
        axes[i].bar(x, sub['f1_score'], w, label='F1-Score', color=PALETTE["teal"], edgecolor='black')
        axes[i].bar(x + w, sub['roc_auc'], w, label='ROC-AUC', color=PALETTE["coral"], edgecolor='black')
        
        axes[i].set_title(f"Ablation Analysis: {clf}", fontsize=13, fontweight='bold', pad=10)
        axes[i].set_xticks(x)
        axes[i].set_xticklabels(sub['label'], fontsize=9.5)
        axes[i].set_ylim(0.5, 1.0)
        axes[i].set_ylabel("Score", fontsize=11)
        axes[i].grid(axis='y', linestyle='--', alpha=0.5)
        axes[i].legend(loc='lower right', fontsize=9)
        
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "modality_comparison_bar.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved modality ablation plot to {fig_path}")

def plot_correlation_heatmap(raw_csv_path: str, output_dir: str):
    """Plot correlation heatmap across clinical, MRI morphometric, and target variables."""
    from src.data_loader import get_clean_classification_data
    df = get_clean_classification_data(raw_csv_path)
    
    cols = ['Age', 'Educ', 'SES', 'MMSE', 'eTIV', 'nWBV', 'ASF', 'target']
    labels = ['Age', 'Education', 'SES', 'MMSE', 'eTIV (Vol)', 'nWBV (Brain)', 'ASF (Scale)', 'Dementia Target']
    
    corr = df[cols].corr()
    
    fig, ax = plt.subplots(figsize=(8.5, 7), dpi=300)
    sns.heatmap(
        corr, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1.0, vmax=1.0,
        xticklabels=labels, yticklabels=labels, ax=ax, cbar_kws={'label': 'Pearson Correlation'}
    )
    ax.set_title("Correlation Matrix: Clinical & Morphometric Variables", fontsize=13, fontweight='bold', pad=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "correlation_heatmap.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Saved correlation heatmap to {fig_path}")

def run_evaluation_figures():
    """Execute all scientific figure generations."""
    config = load_config()
    metrics_dir = config["outputs"]["metrics_dir"]
    figures_dir = config["outputs"]["figures_dir"]
    raw_path = config["data"]["raw_csv_path"]
    os.makedirs(figures_dir, exist_ok=True)
    
    pred_path = os.path.join(metrics_dir, "test_predictions.csv")
    metrics_path = os.path.join(metrics_dir, "model_comparison_test.csv")
    modality_path = os.path.join(metrics_dir, "modality_comparison.csv")
    
    pred_df = pd.read_csv(pred_path)
    
    plot_dataset_distribution(figures_dir)
    plot_roc_curves(pred_df, figures_dir)
    plot_confusion_matrices(pred_df, figures_dir)
    plot_comparative_metrics_bar(metrics_path, figures_dir)
    plot_modality_comparison(modality_path, figures_dir)
    plot_correlation_heatmap(raw_path, figures_dir)
    
    print("\n" + "="*60)
    print("ALL EVALUATION FIGURES GENERATED SUCCESSFULLY")
    print(f"Directory: {figures_dir}")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_evaluation_figures()
