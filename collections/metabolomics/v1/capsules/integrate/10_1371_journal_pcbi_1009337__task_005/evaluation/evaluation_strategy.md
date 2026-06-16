# Evaluation Strategy

## Direct Checks

- file_exists: verify that RAS, RPS, and FFD datasets are deposited in Zenodo (10.5281/zenodo.5824504) or S1 Compressed File Archive and contain reaction-by-sample-by-cellline matrices
- file_format_is: RAS dataset contains normalized Reaction Activity Scores (0–1 range) for each reaction and cell line, derived from transcriptomics via GPR rules
- file_format_is: RPS dataset contains Reaction Propensity Scores computed as product of substrate concentrations raised to stoichiometric coefficients for each reaction and cell line
- file_format_is: FFD dataset contains flux distributions sampled from feasible solution space; verify at least 100,000 steady-state solutions per cell line are present
- row_count_equals: verify classification table has one row per unique (reaction, cell-line-pair) combination; total rows should equal (number of eligible reactions) × 10 pairwise comparisons
- field_present: classification table contains columns: reaction_id, cell_line_pair, RPSvsFFD_concordance_score, RPSvsRAS_concordance_score, regulatory_class, cohen_kappa_value
- value_in_range: Cohen's kappa values in classification table range from -1.0 to +1.0 (robust to parameter choices in concordance computation)
- contains_substring: classification table regulatory_class column contains only values from {transcriptional, metabolic, combined, unclassified, other} matching paper's four-category scheme
- output_matches_reference: classification results for ENGRO2 match or closely align with Fig 4B heatmap (RPSvsRAS and RPSvsFFD scores) and the stated outcomes (44 transcriptional+metabolic, 13 metabolic only) — multiple defensible approaches to exact matching acceptable due to stochasticity in sampling
- script_runs: verify that Cohen's kappa calculation script (from qLSLab/integrate GitHub or Zenodo) executes without error on input RAS, RPS, FFD matrices and produces a kappa coefficient matrix

## Expert Review

- Verify that the concordance classification logic correctly implements the decision rules stated in the paper: positive RPSvsFFD + positive RPSvsRAS → transcriptional+metabolic; positive RPSvsFFD + negative RPSvsRAS → metabolic only; negative RPSvsFFD + positive RPSvsRAS → transcriptional only; negative RPSvsFFD + negative RPSvsRAS → unclassified/other
- Assess whether the threshold of Cohen's kappa > 0.2 for 'fair concordance' is applied consistently across all reactions and whether the FDR-adjusted p-value cutoff (5%) appropriately filters spurious concordance assignments
- Evaluate whether reactions with missing substrate abundance data (omitted from RPS calculation) are correctly marked as ineligible for RPS-based classification and handled transparently in the final table
- Judge whether the handling of reactions lacking GPR associations (RAS = 1.0 by default) in the RPSvsRAS concordance calculation is scientifically justified and clearly documented in the classification table
- Review whether the classification assignments are biologically plausible by spot-checking 5–10 reactions with well-characterized metabolic regulation (e.g., ACONT, RPI, RPE) against literature and the paper's mechanistic descriptions
