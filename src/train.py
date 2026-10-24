"""
Model training and evaluation pipeline for Alzheimer's classification on OASIS-1.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold, cross_validate

from src.utils import load_config, setup_logger, compute_all_metrics, save_json, save_dataframe
from src.data_loader import get_clean_classification_data
from src.preprocessing import create_leakage_free_splits, get_processed_feature_matrix
from src.feature_engineering import get_modality_feature_sets

logger = setup_logger()

def get_model_instances(random_state: int = 42):
    """Instantiate classical ML and ensemble classifiers."""
    dummy = DummyClassifier(strategy="most_frequent")
    
    lr = LogisticRegression(
        C=1.0, max_iter=1000, solver="liblinear", random_state=random_state
    )
    
    rf = RandomForestClassifier(
        n_estimators=100, max_depth=5, min_samples_split=4, random_state=random_state
    )
    
    svm = SVC(
        C=1.0, kernel="rbf", probability=True, random_state=random_state
    )
    
    gb = GradientBoostingClassifier(
        n_estimators=100, learning_rate=0.1, max_depth=3, random_state=random_state
    )
    
    ensemble = VotingClassifier(
        estimators=[('lr', lr), ('rf', rf), ('gb', gb)],
        voting='soft'
    )
    
    return {
        "Dummy (Baseline)": dummy,
        "Logistic Regression": lr,
        "Random Forest": rf,
        "Support Vector Machine": svm,
        "Gradient Boosting": gb,
        "Soft Voting Ensemble": ensemble
    }

def run_cross_validation(models: dict, X_train: pd.DataFrame, y_train: np.ndarray, cv_folds: int = 5):
    """
    Perform 5-fold Stratified Cross-Validation on the training partition.
    """
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
    
    cv_records = []
    logger.info(f"Running {cv_folds}-fold stratified cross-validation on training partition...")
    
    for name, model in models.items():
        scores = cross_validate(model, X_train, y_train, cv=cv, scoring=scoring)
        cv_records.append({
            "model": name,
            "cv_accuracy_mean": float(np.mean(scores['test_accuracy'])),
            "cv_accuracy_std": float(np.std(scores['test_accuracy'])),
            "cv_precision_mean": float(np.mean(scores['test_precision'])),
            "cv_precision_std": float(np.std(scores['test_precision'])),
            "cv_recall_mean": float(np.mean(scores['test_recall'])),
            "cv_recall_std": float(np.std(scores['test_recall'])),
            "cv_f1_mean": float(np.mean(scores['test_f1'])),
            "cv_f1_std": float(np.std(scores['test_f1'])),
            "cv_roc_auc_mean": float(np.mean(scores['test_roc_auc'])),
            "cv_roc_auc_std": float(np.std(scores['test_roc_auc']))
        })
    return pd.DataFrame(cv_records)

def run_training_and_testing():
    """
    Main training execution function.
    """
    config = load_config()
    raw_path = config["data"]["raw_csv_path"]
    metrics_dir = config["outputs"]["metrics_dir"]
    os.makedirs(metrics_dir, exist_ok=True)
    
    # 1. Load data
    clean_df = get_clean_classification_data(raw_path)
    
    # 2. Subject-level holdout split
    train_df, test_df = create_leakage_free_splits(
        clean_df,
        test_size=config["split"]["test_size"],
        random_state=config["split"]["random_state"],
        target_col=config["data"]["target_col"]
    )
    
    # Save splits metadata
    train_df[['ID', 'Age', 'M/F', 'CDR', 'target']].to_csv(
        os.path.join(metrics_dir, "train_split_metadata.csv"), index=False
    )
    test_df[['ID', 'Age', 'M/F', 'CDR', 'target']].to_csv(
        os.path.join(metrics_dir, "test_split_metadata.csv"), index=False
    )
    
    # 3. Multimodal combined features
    modality_sets = get_modality_feature_sets()
    combined_cols = modality_sets["multimodal_combined"]
    
    X_train, X_test, y_train, y_test, preprocessor, feature_names = get_processed_feature_matrix(
        train_df, test_df, combined_cols
    )
    
    # Save processed matrices for reproducibility and explanation
    X_train.to_csv(os.path.join(metrics_dir, "X_train_processed.csv"), index=False)
    X_test.to_csv(os.path.join(metrics_dir, "X_test_processed.csv"), index=False)
    np.save(os.path.join(metrics_dir, "y_train.npy"), y_train)
    np.save(os.path.join(metrics_dir, "y_test.npy"), y_test)
    
    models = get_model_instances(random_state=config["split"]["random_state"])
    
    # 4. 5-fold CV on train partition
    cv_df = run_cross_validation(models, X_train, y_train, cv_folds=config["split"]["cv_folds"])
    save_dataframe(cv_df, os.path.join(metrics_dir, "cv_results.csv"))
    save_json(cv_df.to_dict(orient="records"), os.path.join(metrics_dir, "cv_results.json"))
    
    # 5. Fit models on train partition and evaluate on held-out test partition
    test_results = []
    predictions_dict = {"y_true": y_test}
    fitted_models = {}
    
    logger.info("Evaluating models on held-out test partition...")
    for name, model in models.items():
        model.fit(X_train, y_train)
        fitted_models[name] = model
        
        y_pred = model.predict(X_test)
        predictions_dict[f"{name}_pred"] = y_pred
        
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
            predictions_dict[f"{name}_prob"] = y_prob
        else:
            y_prob = None
            
        metrics = compute_all_metrics(y_test, y_pred, y_prob)
        metrics["model"] = name
        test_results.append(metrics)
        
    test_df_results = pd.DataFrame(test_results)
    save_dataframe(test_df_results, os.path.join(metrics_dir, "model_comparison_test.csv"))
    save_json(test_results, os.path.join(metrics_dir, "model_comparison_test.json"))
    
    # Save test predictions DataFrame
    pred_df = pd.DataFrame(predictions_dict, index=test_df['ID'])
    save_dataframe(pred_df, os.path.join(metrics_dir, "test_predictions.csv"))
    
    # Save trained models
    models_dir = os.path.join(metrics_dir, "saved_models")
    os.makedirs(models_dir, exist_ok=True)
    for name, model in fitted_models.items():
        clean_name = name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        joblib.dump(model, os.path.join(models_dir, f"{clean_name}.joblib"))
        
    joblib.dump(preprocessor, os.path.join(models_dir, "preprocessor.joblib"))
    
    # 6. Modality Ablation Study: Clinical-only vs Structural MRI-only vs Combined
    logger.info("Running Modality Comparison (Clinical-only vs Structural MRI-only vs Combined)...")
    modality_records = []
    
    for mod_name, cols in modality_sets.items():
        X_tr_m, X_te_m, y_tr_m, y_te_m, _, _ = get_processed_feature_matrix(train_df, test_df, cols)
        
        # Test Random Forest on each modality
        rf_m = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_split=4, random_state=42)
        rf_m.fit(X_tr_m, y_tr_m)
        y_p_rf = rf_m.predict(X_te_m)
        y_prob_rf = rf_m.predict_proba(X_te_m)[:, 1]
        m_rf = compute_all_metrics(y_te_m, y_p_rf, y_prob_rf)
        m_rf["modality"] = mod_name
        m_rf["classifier"] = "Random Forest"
        m_rf["features"] = ", ".join(cols)
        modality_records.append(m_rf)
        
        # Test Logistic Regression on each modality
        lr_m = LogisticRegression(C=1.0, max_iter=1000, solver="liblinear", random_state=42)
        lr_m.fit(X_tr_m, y_tr_m)
        y_p_lr = lr_m.predict(X_te_m)
        y_prob_lr = lr_m.predict_proba(X_te_m)[:, 1]
        m_lr = compute_all_metrics(y_te_m, y_p_lr, y_prob_lr)
        m_lr["modality"] = mod_name
        m_lr["classifier"] = "Logistic Regression"
        m_lr["features"] = ", ".join(cols)
        modality_records.append(m_lr)
        
    modality_df = pd.DataFrame(modality_records)
    save_dataframe(modality_df, os.path.join(metrics_dir, "modality_comparison.csv"))
    save_json(modality_records, os.path.join(metrics_dir, "modality_comparison.json"))
    
    logger.info("Training and evaluation successfully completed!")
    return test_df_results, cv_df, modality_df

if __name__ == "__main__":
    test_df_results, cv_df, modality_df = run_training_and_testing()
    print("\n" + "="*80)
    print("HELD-OUT TEST SET EVALUATION RESULTS (N=47)")
    print("="*80)
    cols_to_print = ["model", "accuracy", "precision", "recall", "specificity", "f1_score", "roc_auc", "balanced_accuracy"]
    print(test_df_results[cols_to_print].to_string(index=False))
    print("\n" + "="*80)
    print("MODALITY COMPARISON (Clinical vs MRI vs Multimodal Combined)")
    print("="*80)
    print(modality_df[["modality", "classifier", "accuracy", "f1_score", "roc_auc", "recall", "specificity"]].to_string(index=False))
    print("="*80 + "\n")
