# Evaluation Strategy

## Direct Checks

- verify file exists in FelinaHildebrand/MobiLipid repository: R Markdown file for CCS bias calculation
- verify file exists in FelinaHildebrand/MobiLipid repository: DTCCSN2 library artifact (format: .csv, .RData, or equivalent structured data)
- verify R Markdown script runs without errors on a representative IM-MS lipidomics dataset input
- verify bias assessment report output file is generated with expected format (HTML, PDF, or .txt)
- verify bias assessment report contains at least one quantitative bias metric (e.g., mean error, standard deviation, or percent deviation)
- verify report includes per-lipid-class bias estimates consistent with DTCCSN2 library reference values

## Expert Review

- assess whether the CCS bias calculation methodology (as implemented in the R Markdown) is scientifically sound for IM-MS lipidomics
- assess whether the bias assessment report correctly isolates the assessment step without applying corrections
- assess whether the representative input dataset is appropriate in composition and scale for demonstrating CCS bias calculation
- assess whether reported bias values are within expected ranges for typical IM-MS instruments and lipid classes
