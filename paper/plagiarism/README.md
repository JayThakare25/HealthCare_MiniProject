# Plagiarism and AI-Detection Protocol

## 1. Institutional Compliance Guidelines
- **Institution:** Symbiosis Institute of Technology (SIT), Nagpur
- **Course:** Business Intelligence / Machine Learning Mini-Project (CA3)
- **Target Thresholds:**
  - **Similarity Plagiarism Index:** Strictly below **10%** (excluding standard bibliographic references, equations, and author affiliations).
  - **AI-Detection Indicator:** Strictly below **20%** on approved institutional AI-detection engines.

---

## 2. Required Reports
Before final CA3 submission, two institutional verification reports must be obtained:
1. **Turnitin / DrillBit Similarity Plagiarism Report (`similarity_report.pdf`)**
   - Must show total similarity score, match overview, and breakdown of sources.
   - Exclusion criteria applied: Bibliography ON, Small matches (< 1%) OFF/standard, Quotes ON.
2. **AI-Writing Detection Report (`ai_detection_report.pdf`)**
   - Must evaluate the full manuscript text against generative AI stylometric indicators.

---

## 3. Submission Workflow via Institutional Services
1. **File Preparation:** Submit the final compiled manuscript `paper/report.docx` or `paper/report.pdf`. Do NOT submit intermediate drafts.
2. **Access Portal:** Log in to the SIT Nagpur Institutional Turnitin / DrillBit Portal using institutional credentials (`@sitnagpur.siu.edu.in`).
3. **Repository Settings:**
   - Ensure the submission repository is set to **"Standard Repository"** or **"No Repository"** as directed by the course supervisor (to prevent self-plagiarism on future camera-ready submissions).
4. **Report Export:**
   - Once processing completes, download the **"Current View" (Full Digital Receipt & Highlighted Report)** PDF.
   - Save the similarity report as:
     `paper/plagiarism/similarity_report.pdf`
   - Save the AI detection breakdown as:
     `paper/plagiarism/ai_detection_report.pdf`

---

## 4. Integrity and Verification (Checksum Matching)
To verify that the checked document matches the final submitted manuscript, compute and log the SHA-256 checksum:

```powershell
# In PowerShell:
Get-FileHash -Algorithm SHA256 paper/report.docx
Get-FileHash -Algorithm SHA256 paper/report.pdf
```

Record the generated hashes and the Turnitin Submission ID in this folder alongside the downloaded PDF certificates.

---

## 5. Scientific Honesty Statement
No synthetic, mocked, or fabricated plagiarism scores or certificates have been included in this repository. All submissions must be officially processed through the authorized institutional library service.
