# Dataset Documentation

This directory contains data files for the OASIS-1 Cross-Sectional MRI study.

## 1. Primary Dataset File
- **File:** `oasis_cross-sectional.csv`
- **Source:** Open Access Series of Imaging Studies (OASIS-1)
- **Official URL:** https://www.oasis-brains.org/#oasis1
- **Citation:** Marcus et al., Journal of Cognitive Neuroscience, 2007.

## 2. Dataset Structure
- **Total Records:** 436 subjects
- **Clinically Evaluated Cohort:** 235 subjects (Age 33–96, CDR assessed)
  - Control Group (CDR = 0.0): 135 subjects
  - Dementia Group (CDR > 0.0): 100 subjects (70 very mild, 28 mild, 2 moderate)
- **Young Normal Controls:** 201 subjects (Age 18–59, unassessed CDR)

## 3. Imaging Scans Location
Raw 3D T1-weighted structural MRI scans (MPRAGE format with FSL brain tissue segmentations) are stored in the local disk directory:
`Downloads/oasis_cross-sectional_disc1/disc1/`
comprising 39 raw participant scan directories (`OAS1_0001_MR1` through `OAS1_0039_MR1`). Volumetric measurements extracted by the OASIS imaging pipeline are captured in `oasis_cross-sectional.csv`.
