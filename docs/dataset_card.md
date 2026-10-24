# OASIS-1 Dataset Card & Audit

## 1. Dataset Summary
- **Dataset Name:** Open Access Series of Imaging Studies (OASIS-1) Cross-Sectional MRI Dataset
- **Official Portal:** https://www.oasis-brains.org/#oasis1
- **Foundational Paper:** Marcus, D. S., et al. (2007). "Open Access Series of Imaging Studies (OASIS): Cross-sectional MRI Data in Young, Middle Aged, Nondemented, and Demented Older Adults." *Journal of Cognitive Neuroscience*, 19(9), 1498–1507.
- **Acquisition Protocol:** 1.5-T Siemens Vision scanner, T1-weighted MPRAGE sequences (TR=9.7 ms, TE=4.0 ms, flip angle=10°, voxel resolution=1.0 x 1.0 x 1.25 mm).

---

## 2. Cohort Stratification & Audit
| Attribute | Full Repository | Clinically Evaluated Cohort | Young Controls Cohort |
| :--- | :--- | :--- | :--- |
| **Total Subjects** | 436 | 235 | 201 |
| **Age Range (years)** | 18 – 96 | 33 – 96 | 18 – 59 |
| **Clinical Assessment** | Partial | Complete (CDR assessed) | Unassessed (CDR = NaN) |
| **Controls (CDR = 0.0)** | - | 135 (57.45%) | 201 (presumed normal) |
| **Dementia (CDR > 0.0)** | - | 100 (42.55%) | 0 |
| **- Very Mild (CDR 0.5)** | - | 70 (29.79%) | 0 |
| **- Mild (CDR 1.0)** | - | 28 (11.91%) | 0 |
| **- Moderate (CDR 2.0)** | - | 2 (0.85%) | 0 |

---

## 3. Variable Dictionary
### Clinical and Demographic Attributes
- `ID`: Unique participant accession identifier (e.g., `OAS1_0001_MR1`). Excluded from predictor matrix.
- `M/F`: Biological gender (Categorical: Male / Female). One-hot encoded.
- `Hand`: Handedness (All Right-handed). Excluded due to zero variance.
- `Age`: Chronological age in years (Range: 33 to 96 in evaluated cohort).
- `Educ`: Educational attainment score (1: < High School to 5: Advanced College Degree).
- `SES`: Socioeconomic status score (1: Highest status to 5: Lowest status). 19 missing values imputed via training median.
- `MMSE`: Mini-Mental State Examination score (Range: 15 to 30). Validated cognitive screening inventory.

### Structural Neuroimaging Morphometric Attributes
- `eTIV`: Estimated Total Intracranial Volume ($mm^3$). Computed from the determinant of the transformation matrix aligning the skull to the Talairach atlas space.
- `nWBV`: Normalized Whole Brain Volume. Proportion of intracranial voxels classified as brain tissue (gray matter + white matter) relative to total intracranial volume. Primary marker of diffuse cerebral atrophy.
- `ASF`: Atlas Scaling Factor. One-parameter scaling factor representing brain size differences required for standard space alignment.

---

## 4. Ethical & Clinical Usage Disclaimer
The classification target ($\text{CDR} > 0$) serves as a functional dementia indicator and does not replace differential neuropathological assessment. Data usage complies with OASIS Open Access Data Use Terms.
