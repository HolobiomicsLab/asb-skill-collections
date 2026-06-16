# Evaluation Strategy

## Direct Checks

- verify file exists: github:FelinaHildebrand/MobiLipid repository is accessible and contains DTCCSN2 library artifact
- verify file_format_is: DTCCSN2 library is in a format compatible with R (e.g., .csv, .rds, or documented data structure)
- verify script_runs: R Markdown workflow in MobiLipid codebase executes without error when provided with lipid detection counts and CCS measurements as inputs
- verify output_matches_reference: computational workflow produces a quantitative metric (bias estimate, root mean square error, or correlation coefficient) that demonstrates relationship between lipid count per class and CCS bias quality
- verify field_present: output includes explicit statement or table row showing minimum lipid count per class threshold below which bias estimation remains effective

## Expert Review

- Assess whether the reported finding (low number of lipids per class suffices for effective CCS bias estimation) is scientifically defensible given the computational results and DTCCSN2 reference data
- Evaluate the statistical rigor of the relationship analysis (e.g., linearity, saturation behavior, confidence bounds) between lipid count per class and bias estimation quality
- Review whether the CCS bias estimation method is appropriate for ion mobility-mass spectrometry lipidomics and whether internal standardization with U13C labeled lipids is correctly implemented in the computational workflow
