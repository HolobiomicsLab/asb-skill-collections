# Evaluation Strategy

## Direct Checks

- verify that github:HinesLab__MOCCal repository is accessible and contains source code for class-specific CCS calculation
- verify that the MOCCal Python package can be imported and contains a callable function or method for class-specific CCS computation
- verify that an example or test CCS calculation output file exists in the repository (any of the following: CSV, TSV, HDF5, Parquet, or structured data format)
- verify that the CCS output table contains at least one numeric column with expected CCS value units (Ų or Å²) and at least one column with biomolecular class labels
- verify that CCS values in the output table are within physically plausible ranges (typical CCS values 50–500 Ų for small molecules and ions)

## Expert Review

- confirm that the class-specific CCS calculation formula and methodology are scientifically justified for each biomolecular class (protein, lipid, carbohydrate, metabolite, or other categories used)
- confirm that the class-specific CCS assignments produce values consistent with reported literature CCS measurements for reference standards in each class
- assess whether the class-specific calculation properly accounts for instrument-specific calibration curves and arrival-time-to-drift-time conversion (relevant to TWIM-MS physics)
