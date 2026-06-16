# Evaluation Strategy

## Direct Checks

- verify file exists at Zenodo doi:10.5281/zenodo.18494293 in mzML format
- verify xcms package is installable and contains findChromPeaks, MSWParam, CalibrantMassParam functions
- script_runs: R script that loads mzML from Zenodo, executes findChromPeaks(MSWParam()), then CalibrantMassParam(method='edgeshift') on first file without errors
- file_exists: calibration difference plot output (PDF, PNG, or SVG format)
- expert_review: calibration difference plot visually matches expected mass calibration artifact patterns for FTICR data

## Expert Review

- calibration difference plot interpretation: verify that mass shift magnitudes and distribution are consistent with FTICR instrumental behavior and edgeshift calibration method
- parameter appropriateness: confirm that MSWParam and CalibrantMassParam settings are reasonable for FTICR HAM data characteristics
