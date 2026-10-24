# Experimental Results & Artifacts

This directory contains empirical experimental outputs produced by the training, evaluation, and explainability pipelines.

## 1. Directory Structure

- `metrics/`:
  - `dataset_audit.json`: Detailed cohort demographic and missingness audit.
  - `cv_results.csv` & `.json`: 5-fold stratified cross-validation scores on training partition ($N=188$).
  - `model_comparison_test.csv` & `.json`: Performance metrics on held-out test partition ($N=47$).
  - `modality_comparison.csv` & `.json`: Performance of Clinical-only vs Structural MRI-only vs Multimodal models.
  - `test_predictions.csv`: Participant-level predictions and predicted probabilities.
  - `shap_feature_importance.csv` & `.json`: Mean absolute SHAP values and feature rankings.
  - `saved_models/`: Serialized models and ColumnTransformer preprocessors.

- `figures/`:
  - `dataset_distribution.png`: Cohort composition and CDR severity breakdown.
  - `methodology_flowchart.png`: End-to-end experimental pipeline architecture.
  - `model_architecture_diagram.png`: Soft-voting multi-classifier ensemble architecture.
  - `roc_curves.png`: Multi-classifier ROC curves with AUC values.
  - `confusion_matrices.png`: Confusion matrices grid for all 6 models.
  - `comparative_metrics_bar.png`: Grouped comparative bar chart across models.
  - `modality_comparison_bar.png`: Ablation chart comparing feature modalities.
  - `correlation_heatmap.png`: Pearson correlation matrix across clinical and imaging variables.
  - `shap_global_bar.png`: Global mean absolute SHAP feature ranking.
  - `shap_summary_beeswarm.png`: Beeswarm plot of feature attributions across test cohort.
  - `shap_waterfall_demented.png`: Local waterfall attribution for a high-risk dementia patient.
  - `shap_waterfall_control.png`: Local waterfall attribution for a normal control participant.
  - `shap_dependence_nwbv.png`: Partial dependence of normalized Whole Brain Volume on dementia risk.
  - `shap_dependence_mmse.png`: Partial dependence of MMSE score on dementia risk.

- `logs/`:
  - `experiment.log`: Structured execution log with timestamps.
