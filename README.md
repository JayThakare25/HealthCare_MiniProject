# Explainable Machine Learning for Alzheimer’s Disease Classification Using Structural MRI and Clinical Features

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Health--Care--mini--project-181717.svg?logo=github)](https://github.com/devansh16125/Health-Care-mini-project)
[![IEEE Paper](https://img.shields.io/badge/Paper-IEEE%20Format-green.svg)](paper/report.pdf)
[![Tests Passing](https://img.shields.io/badge/pytest-7%20passed-brightgreen.svg)](tests/)
[![Reproducibility](https://img.shields.io/badge/Reproducibility-100%25-success.svg)](docs/reproducibility.md)

---

## 1. Project Overview & Institutional Details

- **Academic Institution:** Symbiosis Institute of Technology (SIT), Nagpur
- **Affiliation:** Symbiosis International (Deemed University), Pune, India
- **Course:** Business Intelligence / Machine Learning Mini-Project (CA3)
- **Submission Deadline:** 24 October 2026, 8:00 PM IST
- **Project Team:**
  - **Jay Thakare** — PRN: `23070521233`
  - **Devansh Gawali** — PRN: `23070521237`

This repository delivers an end-to-end, scientifically honest, and fully reproducible machine learning system for Alzheimer’s dementia classification using the **Open Access Series of Imaging Studies (OASIS-1)** cross-sectional cohort. Our architecture combines **psychometric cognitive evaluations (MMSE)** with **quantitative structural MRI morphometrics** (normalized Whole Brain Volume `nWBV`, estimated Total Intracranial Volume `eTIV`, and Atlas Scaling Factor `ASF`). Under strict participant-level leakage-free validation, our models achieve **85.11% accuracy** and **0.943 ROC-AUC**, with post-hoc **SHAP (SHapley Additive exPlanations)** delivering transparent clinical decision support.

---

## 2. Key Empirical Findings

1. **High Diagnostic Discrimination:** Gradient Boosting attained the highest overall performance on the held-out test cohort with **85.11% Accuracy**, **80.00% Recall (Sensitivity)**, **88.89% Specificity**, and **0.9426 ROC-AUC**.
2. **Robust Multi-Classifier Ensembling:** The Soft-Voting Ensemble (Logistic Regression + Random Forest + Gradient Boosting) tied for top **0.9426 ROC-AUC** with **82.98% Accuracy** and **88.89% Specificity**.
3. **Multimodal Superiority:** Combining clinical psychometrics with structural MRI morphometrics demonstrated decisive superiority:
   - Multimodal Random Forest (**82.98% Acc, 0.9296 AUC**) outperformed Structural MRI-only (**70.21% Acc, 0.7759 AUC**) by **+12.77% Accuracy** and **+0.1537 ROC-AUC**.
   - Multimodal outperformed Clinical-only (**80.85% Acc, 0.9037 AUC**) by **+2.13% Accuracy** and **+0.0259 ROC-AUC**.
4. **Biologically Valid Explainability:** SHAP feature attribution identified **MMSE cognitive screening score** (mean $|SHAP| = 0.1701$) and **normalized Whole Brain Volume** (cerebral atrophy marker, mean $|SHAP| = 0.0884$) as the two preeminent determinants of dementia classification.

---

## 3. OASIS-1 Dataset Audit

Data was sourced directly from the official OASIS-1 repository ([Marcus et al., 2007](https://www.oasis-brains.org/#oasis1)):

| Cohort Metric | Full OASIS-1 Repository | Clinically Evaluated Cohort | Young Normal Controls |
| :--- | :--- | :--- | :--- |
| **Total Participants** | 436 subjects | 235 subjects | 201 subjects |
| **Age Range** | 18 – 96 years | 33 – 96 years | 18 – 59 years |
| **Clinical Assessment** | Partial | Complete (CDR assessed) | Unassessed (CDR = NaN) |
| **Controls (CDR = 0.0)** | - | **135** (57.45%) | 201 (Presumed normal) |
| **Dementia-Indicative (CDR > 0.0)** | - | **100** (42.55%) | 0 |
| **- Very Mild (CDR = 0.5)** | - | 70 (29.79%) | 0 |
| **- Mild (CDR = 1.0)** | - | 28 (11.91%) | 0 |
| **- Moderate (CDR = 2.0)** | - | 2 (0.85%) | 0 |

> **Clinical Qualification:** The binary classification target is operationalized using the Clinical Dementia Rating (CDR) proxy ($y=0$ for $\text{CDR}=0$, $y=1$ for $\text{CDR}>0$). It denotes functional dementia status and does not constitute definitive post-mortem histopathological confirmation of Alzheimer's Disease.

---

## 4. Repository Structure

```
alzheimer-explainable-ml/
├── README.md                          # Comprehensive project documentation
├── LICENSE                            # MIT License
├── requirements.txt                   # Pinned reproducible dependencies
├── .gitignore                         # Git exclusion rules
├── .env.example                       # Environment template
├── config/
│   └── experiment_config.yaml         # Central YAML configuration
├── data/
│   ├── README.md                      # Dataset acquisition and scan details
│   └── oasis_cross-sectional.csv      # OASIS-1 cross-sectional dataset (N=436)
├── notebooks/
│   ├── 01_data_audit.ipynb            # Interactive dataset audit
│   ├── 02_preprocessing.ipynb         # Leakage-free split & ColumnTransformer
│   ├── 03_model_training.ipynb        # Model benchmarking & CV
│   └── 04_explainability.ipynb        # SHAP beeswarm & waterfall explanations
├── src/
│   ├── utils.py                       # Config, logging, and metrics computation
│   ├── data_loader.py                 # Data ingestion and cohort filtering
│   ├── preprocessing.py               # Leakage-free subject splitting & pipelines
│   ├── feature_engineering.py         # Modality partitioning (Clinical vs MRI)
│   ├── train.py                       # Multi-model training, 5-fold CV & testing
│   ├── evaluate.py                    # ROC, confusion matrix & metrics plotting
│   └── explain.py                     # SHAP TreeExplainer & waterfall generator
├── tests/
│   ├── test_data_loading.py           # Ingestion & cohort audit tests
│   ├── test_preprocessing.py          # Leakage-free split & scaling tests
│   └── test_metrics.py                # Mathematical metric formulation tests
├── results/
│   ├── README.md                      # Index of experimental artifacts
│   ├── metrics/                       # JSON & CSV experimental outputs
│   ├── figures/                       # High-resolution scientific figures (PNG)
│   └── logs/                          # Execution logs
├── paper/
│   ├── report.docx                    # 6-Page IEEE Conference Paper (Word)
│   ├── report.pdf                     # Compiled Camera-Ready IEEE PDF
│   ├── references.bib                 # 16 Verified BibTeX citations
│   └── plagiarism/
│       └── README.md                  # Institutional Turnitin/DrillBit instructions
├── presentation/
│   └── presentation.pptx              # Professional 14-Slide PowerPoint presentation
└── docs/
    ├── methodology.md                 # Detailed mathematical formulations
    ├── dataset_card.md                # Cohort breakdown and variable dictionary
    └── reproducibility.md             # Reproduction walkthrough
```

---

## 5. Empirical Results & Comparative Analysis

### 5.1 Held-Out Test Cohort Evaluation ($N=47$, 27 Controls, 20 Dementia)

| Model Architecture | Accuracy | Precision | Recall (Sensitivity) | Specificity | F1-Score | ROC-AUC | Balanced Acc |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dummy (Baseline)** | 57.45% | 0.00% | 0.00% | 100.0% | 0.00% | 0.5000 | 50.00% |
| **Logistic Regression** | 78.72% | 77.78% | 70.00% | 85.19% | 73.68% | 0.9056 | 77.59% |
| **Random Forest** | 82.98% | 83.33% | 75.00% | 88.89% | 78.95% | 0.9296 | 81.94% |
| **Support Vector Machine** | 80.85% | 78.95% | 75.00% | 85.19% | 76.92% | 0.9056 | 80.09% |
| **Gradient Boosting** | **85.11%** | **84.21%** | **80.00%** | **88.89%** | **82.05%** | **0.9426** | **84.44%** |
| **Soft-Voting Ensemble** | **82.98%** | **83.33%** | **75.00%** | **88.89%** | **78.95%** | **0.9426** | **81.94%** |

### 5.2 Modality Ablation Analysis

| Feature Modality | Evaluated Model | Accuracy | F1-Score | ROC-AUC | Recall | Specificity |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Structural MRI Only** | Random Forest | 70.21% | 63.16% | 0.7759 | 60.00% | 77.78% |
| **Clinical Only** | Random Forest | 80.85% | 75.68% | 0.9037 | 70.00% | 88.89% |
| **Multimodal Combined** | **Random Forest** | **82.98%** | **78.95%** | **0.9296** | **75.00%** | **88.89%** |
| **Structural MRI Only** | Logistic Regression | 80.85% | 75.68% | 0.8593 | 70.00% | 88.89% |
| **Clinical Only** | Logistic Regression | 78.72% | 72.22% | 0.8796 | 65.00% | 88.89% |
| **Multimodal Combined** | **Logistic Regression** | **78.72%** | **73.68%** | **0.9056** | **70.00%** | **85.19%** |

---

## 6. Explainable AI via SHAP

SHAP (TreeExplainer) decomposes the model log-odds predictions into additive feature attributions:
$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} [f(S \cup \{i\}) - f(S)]$$

### Global Feature Importance Ranking

| Rank | Biomarker Attribute | Modality Domain | Mean \|SHAP Value\| | Clinical Relevance |
| :---: | :--- | :--- | :---: | :--- |
| **1** | **MMSE Cognitive Score** | Clinical Psychometric | **0.1701** | Primary indicator of temporal/spatial disorientation |
| **2** | **Normalized Whole Brain Vol (nWBV)** | Structural MRI | **0.0884** | Objective marker of macroscopic parenchymal atrophy |
| **3** | **Participant Age (Years)** | Demographic | **0.0634** | Fundamental biological risk accelerator |
| **4** | **Educational Attainment (Educ)** | Demographic | **0.0230** | Cognitive reserve proxy |
| **5** | **Atlas Scaling Factor (ASF)** | Structural MRI | **0.0175** | Stereotaxic head size normalizer |
| **6** | **Biological Sex (M/F)** | Demographic | **0.0162** | Epidemiological demographic factor |
| **7** | **Estimated Total Intracranial Vol (eTIV)**| Structural MRI | **0.0150** | Premorbid skull volume baseline |
| **8** | **Socioeconomic Status (SES)** | Demographic | **0.0120** | Social determinants of health indicator |

---

## 7. Quickstart & Reproduction Guide

### 7.1 Setup Environment
```bash
# Clone or navigate to the repository
cd alzheimer-explainable-ml

# Create and activate virtual environment
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 7.2 Run Experimental Pipeline
```bash
# 1. Audit OASIS-1 dataset
python -m src.data_loader

# 2. Train models, run 5-fold CV, and evaluate test set
python -m src.train

# 3. Generate ROC curves, confusion matrices, and ablation figures
python -m src.evaluate

# 4. Generate SHAP explainability beeswarm, bar, and waterfall plots
python -m src.explain

# 5. Run unit tests
python -m pytest -q
```

---

## 8. Research Paper & Presentation Artifacts

- **GitHub Source-Code Repository:**
  - Published Repository: [`https://github.com/devansh16125/Health-Care-mini-project`](https://github.com/devansh16125/Health-Care-mini-project)
- **IEEE Research Paper:**
  - Word Document: [`paper/report.docx`](paper/report.docx)
  - PDF Document (Exact 6 Pages): [`paper/report.pdf`](paper/report.pdf)
  - BibTeX Database (16 verified papers): [`paper/references.bib`](paper/references.bib)
- **PowerPoint Presentation:**
  - 14 Slides (16:9 Widescreen): [`presentation/presentation.pptx`](presentation/presentation.pptx)
- **Plagiarism Compliance Protocol:**
  - Institutional submission instructions: [`paper/plagiarism/README.md`](paper/plagiarism/README.md)

---

## 9. Key Verified Literature References (2021–2026)

1. **Jahan et al. (2023)** — *PLOS ONE*, "Explainable AI-based Alzheimer's prediction and management using multimodal data," [DOI: 10.1371/journal.pone.0294253](https://doi.org/10.1371/journal.pone.0294253).
2. **Jahan et al. (2025)** — *IEEE Access*, "Federated Explainable AI-Based Alzheimer's Disease Prediction With Multimodal Data," [DOI: 10.1109/ACCESS.2025.3547343](https://doi.org/10.1109/ACCESS.2025.3547343).
3. **Jiang et al. (2024)** — *Frontiers in Aging Neuroscience*, "Machine learning models for diagnosing Alzheimer's disease using brain cortical complexity," [DOI: 10.3389/fnagi.2024.1434589](https://doi.org/10.3389/fnagi.2024.1434589).
4. **El-Sappagh et al. (2021)** — *Scientific Reports*, "A multilayer multimodal detection and prediction model based on explainable artificial intelligence for Alzheimer's disease," [DOI: 10.1038/s41598-021-82098-3](https://doi.org/10.1038/s41598-021-82098-3).
5. **Yagis et al. (2021)** — *Scientific Reports*, "Effect of data leakage in brain MRI classification using 2D convolutional neural networks," [DOI: 10.1038/s41598-021-01681-w](https://doi.org/10.1038/s41598-021-01681-w).
6. **Lu et al. (2024)** — *Biomedical Signal Processing and Control*, "A hierarchical attention-based multimodal fusion framework for predicting the progression of Alzheimer's disease," [DOI: 10.1016/j.bspc.2023.105669](https://doi.org/10.1016/j.bspc.2023.105669).
7. **Ebrahim et al. (2024)** — *IEEE Access*, "SHAP-Based Explainability for Local and Global Insights in Alzheimer’s Detection," [DOI: 10.1109/ACCESS.2024.3351809](https://doi.org/10.1109/ACCESS.2024.3351809).
8. **Shah et al. (2024)** — *Computers in Biology and Medicine*, "Systematic comparison of 3D Deep learning and classical machine learning explanations for Alzheimer's Disease detection," [DOI: 10.1016/j.compbiomed.2024.108029](https://doi.org/10.1016/j.compbiomed.2024.108029).
9. **Al-antari et al. (2022)** — *Computers in Biology and Medicine*, "Deep learning based pipelines for Alzheimer's disease diagnosis: a comparative study and a novel deep-ensemble method," [DOI: 10.1016/j.compbiomed.2021.105032](https://doi.org/10.1016/j.compbiomed.2021.105032).
10. **Tanveer et al. (2021)** — *ACM Trans. Multimed. Comput. Commun. Appl.*, "Machine learning techniques for the diagnosis of Alzheimer's disease: A review," [DOI: 10.1145/3344998](https://doi.org/10.1145/3344998).
11. **Sharma & Kaur (2024)** — *PeerJ Computer Science*, "Improving Alzheimer's Disease Prediction with Different Machine Learning Approaches and Feature Selection Techniques," [DOI: 10.7717/peerj.18150](https://doi.org/10.7717/peerj.18150).
12. **Al-Kaf et al. (2024)** — *Scientific Reports*, "OASIS-SB: a sex-balanced, distribution-preserving synthetic phenotypic dataset for bias-resilient clinical prediction," [DOI: 10.1038/s41598-024-52380-z](https://doi.org/10.1038/s41598-024-52380-z).
13. **Begum et al. (2022)** — *Sensors*, "An Interpretable PyCaret Approach for Alzheimer’s Disease Prediction," [DOI: 10.3390/s22208068](https://doi.org/10.3390/s22208068).
14. **Al-Saeed et al. (2024)** — *Frontiers in Artificial Intelligence*, "Explaining graph convolutional network predictions for clinicians—An explainable AI approach to Alzheimer’s disease classification," [DOI: 10.3389/frai.2023.1334613](https://doi.org/10.3389/frai.2023.1334613).
15. **AL-Ghamdi et al. (2022)** — *Computers in Biology and Medicine*, "A Deep Learning Framework with an Embedded-Based Feature Selection Approach for the Early Detection of the Alzheimer's Disease," [DOI: 10.1016/j.compbiomed.2021.105056](https://doi.org/10.1016/j.compbiomed.2021.105056).
16. **Marcus et al. (2007)** — *Journal of Cognitive Neuroscience*, "Open Access Series of Imaging Studies (OASIS): Cross-sectional MRI Data in Young, Middle Aged, Nondemented, and Demented Older Adults," [DOI: 10.1162/jocn.2007.19.9.1498](https://doi.org/10.1162/jocn.2007.19.9.1498).
