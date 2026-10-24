# Reproducibility Guide

This guide provides step-by-step instructions to reproduce the entire experimental pipeline, from dataset audit and model training to evaluation, explainability, and document generation.

---

## 1. Environment Setup

### 1.1 Python Environment
Ensure Python 3.10+ (tested on Python 3.11) is installed. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate
```

### 1.2 Install Dependencies
Install all pinned dependencies:

```bash
pip install -r requirements.txt
```

---

## 2. Experimental Pipeline Execution

Run each stage using the modular entry points:

### Stage 1: Dataset Audit
Validates dataset integrity, checks participant counts, and verifies CDR distributions:
```bash
python -m src.data_loader
```
*Output:* `results/metrics/dataset_audit.json`

### Stage 2: Model Training & Cross-Validation
Trains all 6 classifiers, executes 5-fold stratified cross-validation, fits on the training partition ($N=188$), and evaluates on the held-out test partition ($N=47$):
```bash
python -m src.train
```
*Outputs:*
- `results/metrics/model_comparison_test.csv`
- `results/metrics/cv_results.csv`
- `results/metrics/modality_comparison.csv`
- `results/metrics/test_predictions.csv`
- `results/metrics/saved_models/*.joblib`

### Stage 3: Scientific Evaluation & Plotting
Generates high-resolution figures (ROC curves, confusion matrices, comparative metrics, and modality ablation):
```bash
python -m src.evaluate
```
*Outputs:* `results/figures/*.png`

### Stage 4: Explainable AI with SHAP
Initializes TreeExplainer on the trained Random Forest model and generates beeswarm, feature ranking, and local waterfall explanations:
```bash
python -m src.explain
```
*Outputs:*
- `results/figures/shap_summary_beeswarm.png`
- `results/figures/shap_global_bar.png`
- `results/figures/shap_waterfall_demented.png`
- `results/figures/shap_waterfall_control.png`
- `results/figures/shap_dependence_*.png`

### Stage 5: Unit Tests
Verify data loading, preprocessing pipelines, and mathematical metrics:
```bash
python -m pytest -q
```
All 7 unit tests should pass.

---

## 3. Configuration Customization
Hyperparameters, data paths, test split ratios, and random seeds can be adjusted in `config/experiment_config.yaml`.
