# Evaluation Strategy

## Direct Checks

- file_exists: ENGRO2 model in SBML or XLSX format from the S2 File or S3 File deposit or Zenodo 10.5281/zenodo.5824504
- file_exists: intracellular metabolomics dataset (LC-MS data) from MetaboLights MTBLS3597 in a tabular or spectral format
- file_format_is: metabolomics input data contains at least columns for metabolite identifiers, compartment location, and concentration measurements across at least two distinct samples or cell lines
- script_runs: execute RPS computation script from qLSLab/integrate GitHub repository or Zenodo deposit with ENGRO2 model and metabolomics data as inputs, no errors on stderr
- output_matches_reference: RPS dataset produced by the stage matches the numerical values and reaction identifiers reported in Figure 5B (ACONT cytosolic flux distribution) and Figure 5C (RPI flux distribution) or in supplementary S4 File concordance table, robust to rounding to 2–3 significant figures
- row_count_equals: RPS dataset contains one row per metabolic reaction in ENGRO2 (494 total reactions) and one column per sample or cell line tested (5 cell lines: MCF102A, SKBR3, MCF7, MDAMB231, MDAMB361); allow for omission of reactions with missing substrate metabolites per evidence_span rule
- field_present: RPS dataset includes a column or metadata field documenting for each reaction which substrate metabolites were available for RPS computation and which were omitted
- value_in_range: all RPS values are positive real numbers (product of metabolite concentrations raised to stoichiometric coefficient powers); verify no negative or NaN values except where reactions were intentionally omitted
- contains_substring: RPS computation output or method section in generated report contains the mass action law formula (or equivalent: product of [X_q]^s_r,q across all substrates q) and identifies the stoichiometric coefficients (s_r,q) sourced from ENGRO2 GPR rules or stoichiometric matrix

## Expert Review

- Verify that the mass action law formulation applied matches the stated assumption in equation (10): RPS_r^c = ∏([X_q])^s_r,q for all substrates, and that kinetic constant k_r is assumed constant across cell lines as stated in the text
- Confirm that reactions with one or more missing substrate metabolites (not detected in LC-MS) are correctly identified and omitted from the RPS dataset, as per the stated rule: 'If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset'
- Assess whether metabolite abundance values used in RPS computation are properly normalized or z-scored within cell lines, or left in raw concentration units; verify consistency with the treatment of RAS values (which are normalized by max RAS across cell lines in equation 3)
- Evaluate whether the RPS stage correctly handles reversible reactions (forward vs. backward flux direction) given that the pipeline converts to irreversible models; confirm that only forward-reaction substrates are used in RPS for reversible reactions split into two irreversible forms
- Review whether compartmentalization is correctly preserved: confirm that RPS distinguishes reactions in different compartments (e.g., cytosolic vs. mitochondrial aconitase, as highlighted in Discussion for ACONT) by using compartment-specific metabolite concentrations
