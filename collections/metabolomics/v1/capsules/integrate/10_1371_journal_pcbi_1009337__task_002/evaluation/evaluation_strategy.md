# Evaluation Strategy

## Direct Checks

- verify file 10.5281/zenodo.5824504 is accessible and contains RAS and RPS datasets
- verify RAS dataset file exists and contains reaction scores for all five cell lines (MCF102A, SKBR3, MCF7, MDAMB231, MDAMB361)
- verify RPS dataset file exists and contains reaction propensity scores for all five cell lines
- verify metabolomics coverage metadata file identifies exactly 81 reactions with full substrate abundance quantification
- verify that input datasets contain directional change annotations (up/down/no-change) for pairwise comparisons across five cell lines
- script_runs: Cohen's kappa computation script completes without error on RAS and RPS input matrices
- output_matches_reference: Cohen's kappa concordance values for RASvsRPS comparisons match reported values in Fig 4A (robust to rounding to 2 decimal places)
- output_matches_reference: number of reactions with RPSvsRAS concordance score ≥0.2 equals 44 as reported in text
- output_matches_reference: number of reactions with RPSvsFFD concordance score ≥0.2 equals 13 as reported in text
- verify that reactions without GPR associations are correctly excluded from RASvsRPS concordance analysis
- verify that reactions missing any substrate metabolomics measurement are excluded from the 81-reaction subset

## Expert Review

- Cohen's kappa concordance calculation follows standard definition: (observed agreement − expected agreement by chance) / (1 − expected agreement by chance)
- interpretation of Cohen's kappa thresholds (poor <0.2, fair 0.21–0.40, moderate 0.41–0.60, good 0.61–0.80, very good 0.81–1.0) aligns with cited references [51]
- directionality of sign changes (up=+1, down=−1, no-change=0) is correctly determined from Mann-Whitney U test (p<0.05) and log₂ fold-change threshold (≥20% or ≤−20%) as specified in Material and methods
- statistical tests (Mann-Whitney U for FFD, t-test for RPS) are applied correctly to compare distributions across pairwise cell-line comparisons
- any discrepancies between reproduced and reported kappa values are investigated for potential causes: sampling variability in FFD (10 batches of 100k solutions), RPS sensitivity to kinetic assumptions, or threshold parameter choices
