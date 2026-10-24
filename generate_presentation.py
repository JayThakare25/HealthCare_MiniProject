"""
Script to generate the professional 14-slide PowerPoint presentation for CA3 Mini-Project.
Title: Explainable Machine Learning for Alzheimer’s Disease Classification Using Structural MRI and Clinical Features
Authors: Jay Thakare (23070521233) and Devansh Gawali (23070521237)
Institution: Symbiosis Institute of Technology, Nagpur
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # Set 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Color palette
    NAVY = RGBColor(27, 54, 93)       # #1B365D Primary Dark
    TEAL = RGBColor(0, 128, 128)      # #008080 Primary Accent
    LIGHT_BG = RGBColor(245, 247, 250)# #F5F7FA Background
    WHITE = RGBColor(255, 255, 255)
    DARK_TEXT = RGBColor(30, 41, 59)  # #1E293B
    MUTED_TEXT = RGBColor(100, 116, 139) # #64748B
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)
    GOLD = RGBColor(212, 175, 55)
    CORAL = RGBColor(224, 90, 71)

    figures_dir = r"C:\Users\devan\.gemini\antigravity-ide\scratch\alzheimer-explainable-ml\results\figures"

    def add_header(slide, title_text, category_text="BUSINESS INTELLIGENCE & MACHINE LEARNING MINI-PROJECT (CA3)"):
        # Header banner shape
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = NAVY
        header_shape.line.fill.background()
        
        # Teal accent bar
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        accent.fill.solid()
        accent.fill.fore_color.rgb = TEAL
        accent.line.fill.background()
        
        # Header text
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.95))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = GOLD
        p_cat.font.name = "Arial"
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE
        p_title.font.name = "Arial"

    def add_card(slide, left, top, width, height, title=None, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        
        if title:
            tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
            tf = tx.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = NAVY
            p.font.name = "Arial"
        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()
    
    # Accent ribbon
    ribbon = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.35), Inches(7.5))
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = TEAL
    ribbon.line.fill.background()
    
    # Title Box
    t_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.0), Inches(11.0), Inches(2.2))
    t_frame = t_box.text_frame
    t_frame.word_wrap = True
    
    p0 = t_frame.paragraphs[0]
    p0.text = "BUSINESS INTELLIGENCE & MACHINE LEARNING MINI-PROJECT (CA3)"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = GOLD
    p0.font.name = "Arial"
    
    p1 = t_frame.add_paragraph()
    p1.text = "Explainable Machine Learning for Alzheimer’s Disease Classification Using Structural MRI and Clinical Features"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.font.name = "Arial"
    
    # Subtitle / Details Card
    card_t = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.6), Inches(10.8), Inches(3.0))
    card_t.fill.solid()
    card_t.fill.fore_color.rgb = RGBColor(38, 70, 115)
    card_t.line.color.rgb = TEAL
    card_t.line.width = Pt(1.5)
    
    c_box = slide1.shapes.add_textbox(Inches(1.5), Inches(3.8), Inches(10.2), Inches(2.6))
    c_frame = c_box.text_frame
    c_frame.word_wrap = True
    
    cp1 = c_frame.paragraphs[0]
    cp1.text = "Project Team Members:"
    cp1.font.size = Pt(13)
    cp1.font.bold = True
    cp1.font.color.rgb = GOLD
    
    cp2 = c_frame.add_paragraph()
    cp2.text = "• Jay Thakare — PRN: 23070521233\n• Devansh Gawali — PRN: 23070521237"
    cp2.font.size = Pt(14)
    cp2.font.bold = True
    cp2.font.color.rgb = WHITE
    
    cp3 = c_frame.add_paragraph()
    cp3.text = "\nAcademic Institution:"
    cp3.font.size = Pt(12)
    cp3.font.bold = True
    cp3.font.color.rgb = GOLD
    
    cp4 = c_frame.add_paragraph()
    cp4.text = "Department of Computer Science & Engineering\nSymbiosis Institute of Technology (SIT), Nagpur\nSymbiosis International (Deemed University), Pune, India"
    cp4.font.size = Pt(12)
    cp4.font.color.rgb = WHITE
    
    slide1.notes_slide.notes_text_frame.text = (
        "Good morning/afternoon. Today, Devansh Gawali and I, Jay Thakare, present our CA3 mini-project on "
        "Explainable Machine Learning for Alzheimer's Disease Classification Using Structural MRI and Clinical Features. "
        "Our goal is to build an accurate, transparent, and leakage-free diagnostic system that clinicians can understand and trust."
    )

    # ==========================================
    # SLIDE 2: BACKGROUND & MOTIVATION
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Background & Clinical Motivation", "1. CLINICAL CONTEXT")
    
    # 3 Column Cards
    col_w = Inches(3.7)
    gap = Inches(0.3)
    top_pos = Inches(1.5)
    card_h = Inches(5.3)
    
    # Card 1
    add_card(slide2, Inches(0.8), top_pos, col_w, card_h, "Global Healthcare Challenge")
    tb = slide2.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.7), col_w - Inches(0.4), card_h - Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Alzheimer's Disease (AD) accounts for 60%–80% of all global dementia cases.\n\n• Over 55 million individuals are currently affected, projected to reach 152 million by 2050.\n\n• Annual healthcare economic costs exceed $1.3 trillion globally.\n\n• Irreversible cerebral damage precedes overt functional symptoms by 5–15 years."
    for p in tf.paragraphs: p.font.size = Pt(11); p.font.color.rgb = DARK_TEXT
    
    # Card 2
    add_card(slide2, Inches(0.8) + col_w + gap, top_pos, col_w, card_h, "The Diagnostic Dilemma")
    tb = slide2.shapes.add_textbox(Inches(1.0) + col_w + gap, top_pos + Inches(0.7), col_w - Inches(0.4), card_h - Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Structural MRI (sMRI) captures macroscopic cerebral atrophy, ventricular enlargement, and hippocampal shrinkage.\n\n• Cognitive exams (MMSE) evaluate immediate recall and orientation.\n\n• Manual radiological review is labor-intensive, scarce in primary care, and suffers from inter-rater subjectivity in mild stages.\n\n• Need for automated, reliable clinical screening support."
    for p in tf.paragraphs: p.font.size = Pt(11); p.font.color.rgb = DARK_TEXT

    # Card 3
    add_card(slide2, Inches(0.8) + (col_w + gap)*2, top_pos, col_w, card_h, "The Explainability Imperative")
    tb = slide2.shapes.add_textbox(Inches(1.0) + (col_w + gap)*2, top_pos + Inches(0.7), col_w - Inches(0.4), card_h - Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = "• Deep neural networks operate as uninterpretable 'black boxes', blocking clinical translation.\n\n• Medical AI requires actionable, biological justification for individual patient diagnoses.\n\n• Regulatory bodies (FDA, EU AI Act) mandate high transparency in automated medical decision systems.\n\n• Explainable AI (XAI) bridges the gap between predictive accuracy and clinical trust."
    for p in tf.paragraphs: p.font.size = Pt(11); p.font.color.rgb = DARK_TEXT

    slide2.notes_slide.notes_text_frame.text = (
        "Alzheimer's is a massive global crisis. Macroscopic brain changes happen years before obvious memory failure. "
        "While MRI and MMSE tests exist, manual evaluation has bottlenecks. Automated AI has high potential, "
        "but black-box models cannot be safely adopted in clinical neurology without explainability."
    )

    # ==========================================
    # SLIDE 3: PROBLEM STATEMENT & OBJECTIVES
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Problem Statement & Research Objectives", "2. RESEARCH FOCUS")
    
    # Left Card: Problem Statement
    add_card(slide3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), "Core Research Problem")
    tb = slide3.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = (
        "Existing machine learning literature for Alzheimer's diagnosis exhibits three persistent vulnerabilities:\n\n"
        "1. Black-Box Opacity: Lack of patient-specific feature attribution prevents clinicians from verifying if decisions stem from genuine pathology or spurious noise.\n\n"
        "2. Widespread Data Leakage: Participant overlap across cross-validation splits and global pre-scaling artificially inflate reported scores by up to 25%.\n\n"
        "3. Computational Overhead: 3D deep learning models require heavy GPU clusters and lengthy registration pipelines impractical in resource-constrained clinics."
    )
    for p in tf.paragraphs: p.font.size = Pt(11.5); p.font.color.rgb = DARK_TEXT

    # Right Card: Objectives
    add_card(slide3, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), "Key Project Objectives")
    tb = slide3.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = (
        "• Strict Leakage-Free Validation: Implement strict participant-level 80/20 holdout splitting and training-only preprocessor fitting.\n\n"
        "• Multimodal Integration: Combine cognitive psychometrics (MMSE) with structural MRI volumetric morphometrics (nWBV, eTIV, ASF).\n\n"
        "• Lightweight Ensemble Architecture: Benchmark 6 classifiers including a Soft-Voting Ensemble on standard commodity hardware.\n\n"
        "• Post-Hoc Interpretability via SHAP: Unpack global biomarker importance and provide local waterfall patient explanations for clinical decision support."
    )
    for p in tf.paragraphs: p.font.size = Pt(11.5); p.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 4: LITERATURE REVIEW & RESEARCH GAP
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Literature Review & Research Gap (2021–2026)", "3. STATE OF THE ART")
    
    # Table of verified literature
    table_shape = slide4.shapes.add_table(rows=6, cols=5, left=Inches(0.8), top=Inches(1.5), width=Inches(11.7), height=Inches(4.2))
    table = table_shape.table
    
    headers = ["Author & Year", "Dataset & Modality", "Models Evaluated", "Key Findings & Metrics", "Limitations Addressed"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.text_frame.paragraphs[0].runs[0].font.bold = True
        cell.text_frame.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell.text_frame.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        
    lit_data = [
        ["Jahan et al. (2023) [PLOS ONE]", "OASIS-3 Multimodal", "Random Forest + SHAP", "Multimodal fusion outperforms unimodal baselines", "Addressed: Cross-modality feature trade-offs"],
        ["Jahan et al. (2025) [IEEE Access]", "OASIS-3 Multimodal", "Federated Ensemble + SHAP", "Decentralized interpretability preserves privacy", "Addressed: Transparent clinical verification"],
        ["Yagis et al. (2021) [Sci. Reports]", "Brain MRI (ADNI/OASIS)", "2D CNNs & Classical ML", "Scan/slice leakage inflates metrics by up to 25%", "Addressed: Participant-level holdout partition"],
        ["Shah et al. (2024) [Comp. Biol. Med.]", "ADNI Structural MRI", "3D ResNet vs Tree ML + SHAP", "Tree-based SHAP exhibits higher consistency", "Addressed: Transparent biomarker rankings"],
        ["Jiang et al. (2024) [Front. Aging Neur.]", "Structural MRI Morphometry", "SVM, RF, XGBoost + SHAP", "Cortical complexity strongly correlates with CDR", "Addressed: Biological validation of XAI"]
    ]
    for r_idx, row in enumerate(lit_data, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.text_frame.paragraphs[0].runs[0].font.size = Pt(8.5)
            cell.text_frame.paragraphs[0].runs[0].font.color.rgb = DARK_TEXT
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)

    # Bottom summary card
    add_card(slide4, Inches(0.8), Inches(5.9), Inches(11.7), Inches(1.1), None, CARD_BG, TEAL)
    tb = slide4.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.3), Inches(0.95))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "RESEARCH GAP IDENTIFIED: Despite high reported metrics in literature, few studies enforce strict participant-level leakage isolation on accessible OASIS cohorts while providing both global and local patient-level SHAP interpretability on lightweight, reproducible models."
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEAL

    # ==========================================
    # SLIDE 5: OASIS-1 DATASET & DATA AUDIT
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "OASIS-1 Dataset & Rigorous Data Audit", "4. DATA PROVENANCE")
    
    # Left Card: Audit Statistics
    add_card(slide5, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.4), "OASIS-1 Cohort Audit (Actual Statistics)")
    tb = slide5.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = (
        "• Total Records in OASIS-1: 436 unique subjects.\n\n"
        "• Cohort Stratification:\n"
        "  - 201 Young Normal Controls (Ages 18–59, CDR = NaN).\n"
        "  - 235 Clinically Evaluated Older Adults (Ages 33–96).\n\n"
        "• Evaluated Cohort Diagnostic Breakdown (N = 235):\n"
        "  - Controls (CDR = 0.0): 135 subjects (57.45%)\n"
        "  - Dementia (CDR > 0.0): 100 subjects (42.55%)\n"
        "    * Very Mild Dementia (CDR = 0.5): 70 subjects (29.79%)\n"
        "    * Mild Dementia (CDR = 1.0): 28 subjects (11.91%)\n"
        "    * Moderate Dementia (CDR = 2.0): 2 subjects (0.85%)\n\n"
        "• Missing Data: 19 missing values in SES (Hollingshead Index), imputed via training median. Zero missing values in MRI features."
    )
    for p in tf.paragraphs: p.font.size = Pt(10.5); p.font.color.rgb = DARK_TEXT

    # Right: Embedded Chart
    img_dist = os.path.join(figures_dir, "dataset_distribution.png")
    if os.path.exists(img_dist):
        slide5.shapes.add_picture(img_dist, Inches(6.6), Inches(1.8), width=Inches(5.9))

    # ==========================================
    # SLIDE 6: PROPOSED METHODOLOGY FLOWCHART
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Proposed Methodology Architecture", "5. EXPERIMENTAL PIPELINE")
    
    img_flow = os.path.join(figures_dir, "methodology_flowchart.png")
    if os.path.exists(img_flow):
        slide6.shapes.add_picture(img_flow, Inches(0.8), Inches(1.5), width=Inches(11.7))

    slide6.notes_slide.notes_text_frame.text = (
        "Here is our end-to-end pipeline: We take raw OASIS-1 data, filter to the 235 evaluated subjects, "
        "perform a participant-level 80/20 train/test split to guarantee zero leakage, fit imputation and scaling on train only, "
        "train 6 classifiers, aggregate top models into a soft-voting ensemble, and compute SHAP explanations."
    )

    # ==========================================
    # SLIDE 7: PREPROCESSING & FEATURE ENGINEERING
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "MRI Preprocessing & Feature Engineering", "6. DATA PREPARATION")
    
    # 2 Column Cards
    add_card(slide7, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Leakage-Free Preprocessing Protocol")
    tb = slide7.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = (
        "• Participant-Level Partitioning:\n"
        "  - 80% Training Cohort: N = 188 (108 Controls, 80 Dementia)\n"
        "  - 20% Held-Out Test Cohort: N = 47 (27 Controls, 20 Dementia)\n"
        "  - S_train ∩ S_test = ∅ (Strict zero subject overlap).\n\n"
        "• scikit-learn ColumnTransformer Pipeline:\n"
        "  - Imputation: Median for numerical SES, Mode for categorical M/F.\n"
        "  - Scaling: StandardScaler z-score fitted ONLY on training set.\n"
        "  - Categorical: OneHotEncoder(drop='first') fitted on training set.\n\n"
        "• Non-Predictive Column Exclusion:\n"
        "  - 'ID', 'Hand' (all Right-handed), 'Delay' (all NaN) removed."
    )
    for p in tf.paragraphs: p.font.size = Pt(11); p.font.color.rgb = DARK_TEXT

    add_card(slide7, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Extracted Multimodal Feature Space")
    tb = slide7.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = (
        "1. Clinical & Demographic Features (5 Variables):\n"
        "  • MMSE (0–30): Primary cognitive screening test score.\n"
        "  • Age (33–96): Primary demographic risk factor.\n"
        "  • M/F: Biological gender (Male / Female).\n"
        "  • Educ (1–5): Educational attainment level.\n"
        "  • SES (1–5): Hollingshead Socioeconomic Status.\n\n"
        "2. Structural MRI Morphometrics (3 Variables):\n"
        "  • nWBV (0.64–0.85): Normalized Whole Brain Volume (brain tissue ratio; primary indicator of cerebral atrophy).\n"
        "  • eTIV (1123–1992 mm³): Estimated Total Intracranial Volume.\n"
        "  • ASF (0.88–1.56): Atlas Scaling Factor to Talairach standard."
    )
    for p in tf.paragraphs: p.font.size = Pt(11); p.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 8: CLASSIFIERS & ENSEMBLE ARCHITECTURE
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Classification Models & Ensemble Architecture", "7. MODEL DESIGN")
    
    # Left Card: Model descriptions
    add_card(slide8, Inches(0.8), Inches(1.5), Inches(5.2), Inches(5.4), "Evaluated Classification Models")
    tb = slide8.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(4.8), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.text = (
        "• Dummy Classifier (Baseline):\n"
        "  Majority class prediction; defines empirical performance floor.\n\n"
        "• Logistic Regression (LR):\n"
        "  Linear probabilistic classifier with L2 regularization penalty.\n\n"
        "• Random Forest (RF):\n"
        "  100 bagged decorrelated decision trees (depth=5, split=4).\n\n"
        "• Support Vector Machine (SVM):\n"
        "  RBF kernel with Platt-scaled calibrated posterior probabilities.\n\n"
        "• Gradient Boosting (GB):\n"
        "  100 sequential residual regression trees (lr=0.1, depth=3).\n\n"
        "• Soft-Voting Ensemble:\n"
        "  Weighted consensus: P = (1·P_LR + 2·P_RF + 2·P_GB) / 5."
    )
    for p in tf.paragraphs: p.font.size = Pt(10.5); p.font.color.rgb = DARK_TEXT

    # Right: Embedded Architecture Diagram
    img_arch = os.path.join(figures_dir, "model_architecture_diagram.png")
    if os.path.exists(img_arch):
        slide8.shapes.add_picture(img_arch, Inches(6.3), Inches(1.8), width=Inches(6.2))

    # ==========================================
    # SLIDE 9: EXPLAINABLE AI USING SHAP
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Explainable AI Using SHAP Framework", "8. INTERPRETABILITY")
    
    col_w = Inches(3.7)
    add_card(slide9, Inches(0.8), Inches(1.5), col_w, Inches(5.4), "Game-Theoretic Foundation")
    tb = slide9.shapes.add_textbox(Inches(1.0), Inches(2.2), col_w - Inches(0.4), Inches(4.4))
    tf = tb.text_frame; tf.word_wrap = True
    tf.text = (
        "• SHapley Additive exPlanations (SHAP) is grounded in cooperative game theory.\n\n"
        "• Fairly allocates model prediction credit across all features via marginal contributions:\n\n"
        "  φ_i = Σ [|S|!(|F|-|S|-1)! / |F|!] · [f(S ∪ {i}) - f(S)]\n\n"
        "• Satisfies key axioms: Efficiency, Symmetry, Dummy player, and Additivity."
    )
    for p in tf.paragraphs: p.font.size = Pt(10.5); p.font.color.rgb = DARK_TEXT

    add_card(slide9, Inches(0.8) + col_w + gap, Inches(1.5), col_w, Inches(5.4), "Global Interpretability")
    tb = slide9.shapes.add_textbox(Inches(1.0) + col_w + gap, Inches(2.2), col_w - Inches(0.4), Inches(4.4))
    tf = tb.text_frame; tf.word_wrap = True
    tf.text = (
        "• Ranks overall biomarker influence using mean absolute SHAP values across test cohort.\n\n"
        "• Summary Beeswarm Plot reveals feature impact distributions and directional relationships.\n\n"
        "• Confirms whether model relies on biologically valid neurodegeneration or imaging artifacts."
    )
    for p in tf.paragraphs: p.font.size = Pt(10.5); p.font.color.rgb = DARK_TEXT

    add_card(slide9, Inches(0.8) + (col_w + gap)*2, Inches(1.5), col_w, Inches(5.4), "Local Patient Attribution")
    tb = slide9.shapes.add_textbox(Inches(1.0) + (col_w + gap)*2, Inches(2.2), col_w - Inches(0.4), Inches(4.4))
    tf = tb.text_frame; tf.word_wrap = True
    tf.text = (
        "• Waterfall Explanations decompose an individual patient's diagnostic risk score.\n\n"
        "• Base Value (expected population log-odds) shifts toward positive or negative prediction.\n\n"
        "• Provides clinical decision support by explicitly justifying why patient is classified as high-risk."
    )
    for p in tf.paragraphs: p.font.size = Pt(10.5); p.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 10: EXPERIMENTAL SETUP & HYPERPARAMETERS
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Experimental Setup & Hyperparameters", "9. RIGOROUS SETUP")
    
    # Left Card: Environment
    add_card(slide10, Inches(0.8), Inches(1.5), Inches(4.8), Inches(5.4), "Hardware & Software Stack")
    tb = slide10.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(4.4), Inches(4.5))
    tf = tb.text_frame; tf.word_wrap = True
    tf.text = (
        "• Operating System: Windows 10/11 (AMD64 platform)\n"
        "• Python Runtime: Python 3.11.0\n"
        "• Core Libraries: scikit-learn 1.7.0, NumPy 2.x, pandas 2.x, SHAP 0.46.0, Matplotlib 3.10.0\n"
        "• Hardware: Intel Core i5 CPU, 16 GB RAM (No GPU required)\n"
        "• Execution Time: < 15 seconds for full training, CV, testing, and SHAP generation\n"
        "• Reproducibility: Seed = 42 enforced across all splits and algorithms\n"
        "• Unit Testing: 7/7 pytest unit tests verified."
    )
    for p in tf.paragraphs: p.font.size = Pt(10.5); p.font.color.rgb = DARK_TEXT

    # Right: Hyperparameters Table
    table_shape = slide10.shapes.add_table(rows=7, cols=3, left=Inches(5.9), top=Inches(1.5), width=Inches(6.6), height=Inches(5.4))
    table = table_shape.table
    
    h_params = ["Classifier", "Exact Hyperparameters", "Optimization Objective"]
    for i, h in enumerate(h_params):
        cell = table.cell(0, i)
        cell.text = h
        cell.text_frame.paragraphs[0].runs[0].font.bold = True
        cell.text_frame.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell.text_frame.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        
    hp_data = [
        ["Dummy Baseline", "strategy='most_frequent'", "Class prior floor"],
        ["Logistic Regression", "C=1.0, solver='liblinear', max_iter=1000", "L2 Cross-Entropy"],
        ["Random Forest", "n_estimators=100, max_depth=5, min_samples_split=4", "Gini Impurity"],
        ["Support Vector Machine", "C=1.0, kernel='rbf', probability=True", "Hinge Loss"],
        ["Gradient Boosting", "n_estimators=100, lr=0.1, max_depth=3", "Binomial Deviance"],
        ["Soft Voting Ensemble", "voting='soft', weights=[1, 2, 2]", "Weighted Log-Loss"]
    ]
    for r_idx, row in enumerate(hp_data, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.text_frame.paragraphs[0].runs[0].font.size = Pt(8.5)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)

    # ==========================================
    # SLIDE 11: COMPARATIVE MODEL RESULTS
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "Comparative Model Results (Held-Out Test Set, N=47)", "10. EMPIRICAL FINDINGS")
    
    # Results Table
    table_shape = slide11.shapes.add_table(rows=7, cols=8, left=Inches(0.8), top=Inches(1.5), width=Inches(11.7), height=Inches(3.8))
    table = table_shape.table
    
    headers = ["Model", "Accuracy", "Precision", "Recall (Sens)", "Specificity", "F1-Score", "ROC-AUC", "Bal. Acc"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.text_frame.paragraphs[0].runs[0].font.bold = True
        cell.text_frame.paragraphs[0].runs[0].font.size = Pt(9.5)
        cell.text_frame.paragraphs[0].runs[0].font.color.rgb = WHITE
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        
    res_data = [
        ["Dummy (Baseline)", "57.45%", "0.00%", "0.00%", "100.0%", "0.00%", "0.5000", "50.00%"],
        ["Logistic Regression", "78.72%", "77.78%", "70.00%", "85.19%", "73.68%", "0.9056", "77.59%"],
        ["Random Forest", "82.98%", "83.33%", "75.00%", "88.89%", "78.95%", "0.9296", "81.94%"],
        ["Support Vector Machine", "80.85%", "78.95%", "75.00%", "85.19%", "76.92%", "0.9056", "80.09%"],
        ["Gradient Boosting", "85.11%", "84.21%", "80.00%", "88.89%", "82.05%", "0.9426", "84.44%"],
        ["Soft Voting Ensemble", "82.98%", "83.33%", "75.00%", "88.89%", "78.95%", "0.9426", "81.94%"]
    ]
    for r_idx, row in enumerate(res_data, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.text_frame.paragraphs[0].runs[0].font.size = Pt(9)
            if "Gradient" in row[0] or "Voting" in row[0]:
                cell.text_frame.paragraphs[0].runs[0].font.bold = True
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)

    # Key Takeaways Box
    add_card(slide11, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.5), None, CARD_BG, TEAL)
    tb = slide11.shapes.add_textbox(Inches(1.0), Inches(5.55), Inches(11.3), Inches(1.35))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EMPIRICAL FINDINGS HIGHLIGHTS:"
    p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = TEAL
    
    p2 = tf.add_paragraph()
    p2.text = (
        "1. Gradient Boosting achieved top overall diagnostic accuracy (85.11%) and sensitivity/recall (80.00%), detecting 16 of 20 dementia cases.\n"
        "2. Soft-Voting Ensemble tied Gradient Boosting for top ROC-AUC (0.9426) with robust 88.89% specificity (identifying 24 of 27 healthy controls).\n"
        "3. All machine learning models achieved ROC-AUC > 0.90, confirming strong discriminative separation under strict zero-leakage conditions."
    )
    p2.font.size = Pt(10); p2.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 12: METRIC VISUALIZATIONS & ABLATION
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "Evaluation Visualizations & Modality Ablation", "11. DETAILED METRICS")
    
    # 2 Figures Side by Side
    img_roc = os.path.join(figures_dir, "roc_curves.png")
    img_mod = os.path.join(figures_dir, "modality_comparison_bar.png")
    
    if os.path.exists(img_roc):
        slide12.shapes.add_picture(img_roc, Inches(0.8), Inches(1.5), width=Inches(5.6))
    if os.path.exists(img_mod):
        slide12.shapes.add_picture(img_mod, Inches(6.8), Inches(1.5), width=Inches(5.7))

    # Notes
    slide12.notes_slide.notes_text_frame.text = (
        "On the left, the ROC curves show that Gradient Boosting and Ensemble reach an outstanding 0.943 AUC. "
        "On the right, our ablation study proves that multimodal fusion delivers a huge +12.77% gain over MRI alone "
        "and +2.13% over clinical tests alone, proving both modalities are essential."
    )

    # ==========================================
    # SLIDE 13: SHAP EXPLAINABILITY & DISCUSSION
    # ==========================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "Explainability Insights & Patient Case Studies", "12. CLINICAL EXPLAINABILITY")
    
    img_swarm = os.path.join(figures_dir, "shap_summary_beeswarm.png")
    img_wf = os.path.join(figures_dir, "shap_waterfall_demented.png")
    
    if os.path.exists(img_swarm):
        slide13.shapes.add_picture(img_swarm, Inches(0.8), Inches(1.5), width=Inches(6.0))
    if os.path.exists(img_wf):
        slide13.shapes.add_picture(img_wf, Inches(7.1), Inches(1.5), width=Inches(5.4))

    slide13.notes_slide.notes_text_frame.text = (
        "Here are our SHAP findings: Globally, MMSE cognitive decline and normalized whole brain volume loss (nWBV) "
        "are the top two drivers of dementia classification. On the right, our local patient waterfall shows how "
        "a specific patient with low MMSE and severe brain atrophy was classified as dementia with 96% confidence."
    )

    # ==========================================
    # SLIDE 14: CONCLUSION, FUTURE WORK & REFS
    # ==========================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_header(slide14, "Conclusion, Future Work & Selected References", "13. SUMMARY")
    
    col_w = Inches(3.7)
    add_card(slide14, Inches(0.8), Inches(1.5), col_w, Inches(5.4), "Summary of Contributions")
    tb = slide14.shapes.add_textbox(Inches(1.0), Inches(2.2), col_w - Inches(0.4), Inches(4.4))
    tf = tb.text_frame; tf.word_wrap = True
    tf.text = (
        "• Validated Lightweight Framework: Built a transparent multimodal ML system executing in seconds without GPU requirements.\n\n"
        "• Zero-Leakage Protocol: Enforced strict participant-level splitting and training-only transformer fitting.\n\n"
        "• High Diagnostic Power: Gradient Boosting achieved 85.11% accuracy, 80.0% recall, and 0.943 ROC-AUC.\n\n"
        "• Clinical Transparency: SHAP confirmed biological validity (MMSE + brain parenchymal volume loss nWBV)."
    )
    for p in tf.paragraphs: p.font.size = Pt(10.5); p.font.color.rgb = DARK_TEXT

    add_card(slide14, Inches(0.8) + col_w + gap, Inches(1.5), col_w, Inches(5.4), "Future Research Directions")
    tb = slide14.shapes.add_textbox(Inches(1.0) + col_w + gap, Inches(2.2), col_w - Inches(0.4), Inches(4.4))
    tf = tb.text_frame; tf.word_wrap = True
    tf.text = (
        "• Regional Volumetric Segmentation: Integrate FreeSurfer subcortical volumetry (hippocampus and lateral ventricles).\n\n"
        "• Longitudinal Staging: Track Mild Cognitive Impairment (MCI) progression over multi-year timepoints using OASIS-2/3.\n\n"
        "• Multicenter Validation: Cross-evaluate on ADNI and AIBL cohorts.\n\n"
        "• Federated Learning: Implement privacy-preserving decentralized learning across hospitals [Jahan et al., 2025]."
    )
    for p in tf.paragraphs: p.font.size = Pt(10.5); p.font.color.rgb = DARK_TEXT

    add_card(slide14, Inches(0.8) + (col_w + gap)*2, Inches(1.5), col_w, Inches(5.4), "Selected References")
    tb = slide14.shapes.add_textbox(Inches(1.0) + (col_w + gap)*2, Inches(2.2), col_w - Inches(0.4), Inches(4.4))
    tf = tb.text_frame; tf.word_wrap = True
    tf.text = (
        "1. Marcus et al., J. Cogn. Neurosci., 2007 (OASIS-1 Benchmark).\n\n"
        "2. Jahan et al., PLOS ONE, 2023 (Multimodal XAI Alzheimer's).\n\n"
        "3. Jahan et al., IEEE Access, 2025 (Federated XAI).\n\n"
        "4. Yagis et al., Sci. Reports, 2021 (Data Leakage in Brain MRI).\n\n"
        "5. Shah et al., Comp. Biol. Med., 2024 (XAI Explanations for AD).\n\n"
        "6. Jiang et al., Front. Aging Neur., 2024 (Brain Complexity XAI)."
    )
    for p in tf.paragraphs: p.font.size = Pt(9.5); p.font.color.rgb = DARK_TEXT

    slide14.notes_slide.notes_text_frame.text = (
        "In conclusion, our work proves that transparent, explainable machine learning combining cognitive screening "
        "and structural MRI delivers high-accuracy dementia classification without expensive deep learning or data leakage. "
        "Thank you! We welcome any questions."
    )

    out_dir = r"C:\Users\devan\.gemini\antigravity-ide\scratch\alzheimer-explainable-ml\presentation"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "presentation.pptx")
    prs.save(out_path)
    print(f"Professional 14-slide PowerPoint presentation generated at: {out_path}")
    return out_path

if __name__ == "__main__":
    create_deck()
