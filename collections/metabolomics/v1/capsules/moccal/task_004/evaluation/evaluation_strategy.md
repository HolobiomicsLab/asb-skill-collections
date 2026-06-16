# Evaluation Strategy

## Direct Checks

- verify file_exists: the deposited TWIM-MS dataset (accession number or URL) is accessible and downloadable
- verify script_runs: MOCCal workflow executes without error on the external dataset (all three stages: calibration, class assignment, class-specific CCS calculation)
- verify file_exists and file_format_is: structured CCS output file is produced in expected format (CSV, JSON, or HDF5 — solution_space: any documented output format is acceptable)
- verify output_matches_reference: CCS values in output are numeric, within physically plausible range for the biomolecular classes present (expert-validated ranges or literature cross-checks), robust to minor parameter choices
- verify row_count_equals or field_present: output file contains at least one CCS value record per input feature/compound, with required columns (feature ID, class label, CCS value)

## Expert Review

- Confirm that the assigned biomolecular classes are chemically/biologically consistent with the dataset source (e.g., lipids, peptides, metabolites as declared in deposit metadata)
- Review CCS calibration convergence and model diagnostics (residuals, R² or equivalent goodness-of-fit) to assess whether calibration quality is acceptable for the external dataset
- Assess whether class-specific CCS calculations show expected within-class consistency and between-class separation, compared to prior literature or the tool's validation cohort
