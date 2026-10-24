# Methodology and Mathematical Formulation

## 1. Problem Formulation
Alzheimer’s disease (AD) is characterized by insidious neurodegeneration and structural brain atrophy. In this investigation, we formulate dementia classification as a supervised binary learning task:
$$\hat{y} = f(\mathbf{x}) \in \{0, 1\}$$
where $\mathbf{x} = [x_1, x_2, \dots, x_d]^T$ represents an 8-dimensional multimodal feature vector combining demographic attributes, psychometric test scores, and structural MRI volumetric morphometrics.

### Diagnostic Target Definition
The ground truth target is operationalized using the Clinical Dementia Rating (CDR):
- Class 0 ($y = 0$): Cognitively Normal Control ($\text{CDR} = 0.0$)
- Class 1 ($y = 1$): Dementia-Indicative ($\text{CDR} \in \{0.5, 1.0, 2.0\}$)

*Clinical qualification:* This target serves as a dementia-status proxy reflecting functional and cognitive impairment; definitive post-mortem histopathology is required for etiologic confirmation of Alzheimer's Disease.

---

## 2. Participant-Level Leakage Prevention
To prevent overly optimistic performance estimation and data leakage (as highlighted in neuroimaging studies such as Yagis et al., 2021):
1. **Partitioning Scheme:** Stratified 80/20 train/test holdout splitting is performed strictly at the participant level ($N=235$ unique individuals: $N_{\text{train}}=188$, $N_{\text{test}}=47$).
2. **Zero Overlap:** $\mathcal{S}_{\text{train}} \cap \mathcal{S}_{\text{test}} = \emptyset$.
3. **Independent Preprocessing:** Imputation statistics (median for numerical $SES$, mode for categorical variables) and scaling parameters ($\mu, \sigma$) are computed exclusively on $\mathcal{S}_{\text{train}}$ and transformed downstream to $\mathcal{S}_{\text{test}}$.

---

## 3. Mathematical Model Formulations

### 3.1 Logistic Regression
The conditional posterior probability of dementia is modeled as:
$$P(y = 1 \mid \mathbf{x}) = \sigma(\mathbf{w}^T \mathbf{x} + b) = \frac{1}{1 + \exp(-(\mathbf{w}^T \mathbf{x} + b))}$$
Trained via $L_2$-regularized cross-entropy minimization:
$$\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|_2^2 + C \sum_{i=1}^{N_{\text{train}}} \log(1 + \exp(-y_i (\mathbf{w}^T \mathbf{x}_i + b)))$$

### 3.2 Random Forest (Bagging Ensemble)
Ensemble of $B = 100$ decorrelated decision trees constructed via bootstrap sampling and random feature sub-selection:
$$\hat{P}_{\text{RF}}(y = 1 \mid \mathbf{x}) = \frac{1}{B} \sum_{b=1}^B T_b(\mathbf{x})$$

### 3.3 Gradient Boosting (Sequential Residual Learning)
Constructs additive regression trees sequentially fitting negative binomial log-likelihood gradients:
$$F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \eta \cdot h_m(\mathbf{x})$$
with learning rate $\eta = 0.1$ and maximum tree depth $D = 3$.

### 3.4 Soft-Voting Ensemble
Aggregates predicted class probability distributions using weighted consensus:
$$\hat{P}_{\text{Ensemble}}(y = 1 \mid \mathbf{x}) = \frac{\sum_{m=1}^M w_m \hat{P}_m(y = 1 \mid \mathbf{x})}{\sum_{m=1}^M w_m}$$
with weights $w_{\text{LR}} = 1, w_{\text{RF}} = 2, w_{\text{GB}} = 2$.
Decision rule:
$$\hat{y} = \mathbb{I}\left(\hat{P}_{\text{Ensemble}}(y = 1 \mid \mathbf{x}) \ge 0.5\right)$$

---

## 4. Evaluation Metrics
Predictions are evaluated against ground truth labels through confusion matrix entries ($TP, TN, FP, FN$):
- **Accuracy:** $\frac{TP + TN}{TP + TN + FP + FN}$
- **Precision:** $\frac{TP}{TP + FP}$
- **Recall (Sensitivity):** $\frac{TP}{TP + FN}$
- **Specificity:** $\frac{TN}{TN + FP}$
- **Balanced Accuracy:** $\frac{1}{2} \left(\text{Sensitivity} + \text{Specificity}\right)$
- **F1-Score:** $\frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$
- **Area Under the ROC Curve (ROC-AUC):** Trapezoidal numerical integration of True Positive Rate vs False Positive Rate across all classification thresholds $\tau \in [0, 1]$.

---

## 5. Explainable AI via SHAP (SHapley Additive exPlanations)
Based on cooperative game theory, the prediction $f(\mathbf{x})$ is locally decomposed into additive feature contributions:
$$f(\mathbf{x}) = \phi_0 + \sum_{i=1}^d \phi_i(\mathbf{x})$$
where the Shapley attribution value $\phi_i$ for feature $i$ is uniquely determined by:
$$\phi_i(f, \mathbf{x}) = \sum_{\mathcal{S} \subseteq \mathcal{F} \setminus \{i\}} \frac{|\mathcal{S}|! (|\mathcal{F}| - |\mathcal{S}| - 1)!}{|\mathcal{F}|!} \left[ f_{\mathcal{S} \cup \{i\}}(\mathbf{x}_{\mathcal{S} \cup \{i\}}) - f_{\mathcal{S}}(\mathbf{x}_{\mathcal{S}}) \right]$$
Here $\mathcal{F}$ is the set of all 8 features and $\mathcal{S}$ represents feature coalitions. Global feature importance is quantified through the mean absolute SHAP value:
$$I_i = \frac{1}{N_{\text{test}}} \sum_{j=1}^{N_{\text{test}}} |\phi_i^{(j)}|$$
