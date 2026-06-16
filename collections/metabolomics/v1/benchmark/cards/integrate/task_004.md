# SciTask Card: Reconstruct the Reaction Propensity Score (RPS) computation module using mass action law formulation

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:26:15.469347+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_integrate`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `data-analysis`, `modeling`
- DOI: `10.1371/journal.pcbi.1009337`
- GitHub: `qLSLab/integrate`

## Classification

- Task kind: `component_reconstruction`
- Article type: `research-article`
- Primary domain: `multi-omics`
- Subdomains: `multi-omics-integration`, `computational-metabolomics`, `fluxomics`
- Techniques: `flux-analysis`, `multi-omics-integration`, `pathway-analysis`, `differential-abundance-analysis`
- Keywords: `constraint-based metabolic modeling` · `metabolic flux prediction` · `transcriptomics integration` · `metabolomics integration` · `multi-level metabolic regulation` · `gene expression` · `substrate availability` · `enzyme kinetics` · `Michaelis-Menten law` · `systems metabolism`

## Research Question
How does the mass action law formulation translate intracellular metabolomics data into Reaction Propensity Scores (RPS) that quantify the expected relative metabolic flux changes across cell lines based purely on substrate availability differences?

## Connected Finding
For each reaction r and cell line c, the Reaction Propensity Score (RPS) is computed as the product of substrate concentrations each raised to their stoichiometric coefficients: RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q), where [X_q] is substrate concentration and s_r,q is the stoichiometric coefficient. If any substrate is unmeasured, the reaction is omitted from the RPS dataset.

## Task Description
Compute Reaction Propensity Scores (RPS) for all metabolic reactions in the ENGRO2 model using intracellular metabolomics data and the mass action law, producing a quantitative dataset that predicts how differences in substrate availability translate into differences in metabolic fluxes.

## Inputs
- Intracellular metabolomics abundance data (metabolite concentrations in molar or relative units) for five breast cell lines (MCF102A, MCF7, MDAMB231, MDAMB361, SKBR3), including at least 2 biological replicates per cell line
- ENGRO2 constraint-based stoichiometric metabolic network model with Gene-Protein-Reaction (GPR) associations and complete reaction-metabolite stoichiometry

## Expected Outputs
- Reaction Propensity Scores (RPS) dataset: a matrix (or table) with metabolic reactions as rows, cell lines as columns, and normalized RPS values (0–1 range) as entries, computed from mass action law applied to substrate concentrations

## Expected Output File

- `rps_scores.csv`

## Landmark Outputs

- `metabolite_reaction_mapping.csv`
- `rps_raw_scores.csv`
- `rps_normalized.csv`

## Tools
- constraint-based stoichiometric metabolic models

## Skills
- metabolite-concentration-stoichiometric-mapping
- mass-action-kinetics-formulation
- reaction-propensity-score-computation
- metabolomics-data-integration-with-metabolic-networks
- metabolite-abundance-normalization-across-conditions

## Workflow Description
1. Load intracellular metabolomics abundance data (metabolite concentrations in each cell line) and the ENGRO2 stoichiometric metabolic network model with reaction-metabolite associations. 2. For each metabolic reaction and each cell line, identify all substrate metabolites from the model's stoichiometry and retrieve their measured intracellular concentrations; omit reactions missing one or more substrate abundance measurements. 3. For each eligible reaction in each cell line, compute the Reaction Propensity Score (RPS) as the product of substrate concentrations each raised to their stoichiometric coefficient power, following the mass action law formulation: RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q), where [X_q] is substrate q concentration and s_r,q is its stoichiometric coefficient. 4. Aggregate RPS values across biological replicates within each cell line (using median or mean as appropriate) to produce a cell-line-level RPS score for each reaction. 5. Normalize RPS scores within each reaction across all cell lines by dividing by the maximum RPS value observed for that reaction. 6. Output the normalized RPS dataset as a table with reactions as rows, cell lines as columns, and normalized RPS values as entries.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `integrate.pdf` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| metabolights | `MTBLS3597` | https://www.ebi.ac.uk/metabolights/MTBLS3597 | etails on data processing the at www.ebi.ac.uk/metabolights/MTBLS3597. Normalized data (on utational analyses are reported in S1 |
| bioproject | `PRJNA767228` | https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228 | sing the h abundance was measured i Raw reads are available PRJNA767228. ENGRO2 model recon Starting from ENGRO1 [44 core model of |

## Missing Information
- No explicit specification of whether metabolite abundance values are normalized, log-transformed, or left in raw concentration units before RPS computation; unclear if concentrations are treated as absolute (mM) or relative
- No explicit listing of how many reactions in ENGRO2 (out of 494 total) are expected to retain RPS values after applying the missing-substrate-omission rule; no count of excluded reactions provided
- No explicit detail on whether stoichiometric coefficients (s_r,q) are sourced from the ENGRO2 stoichiometric matrix directly or computed from GPR rule parsing; unclear if the formula applies stoichiometric integer coefficients or fractional ATP/cofactor stoichiometries
- No explicit documentation of how the stage handles metabolites with below-detection-limit (BDL) or missing values in the LC-MS dataset; unclear whether BDL values are set to zero, a floor, or excluded entirely
- No explicit statement on whether the RPS stage applies the same cell-relative model constraints (Type 1, Type 2, Type 3 nutrient/extracellular/transcriptomics constraints) as described for FFD generation, or operates independently on raw metabolomics data

## Domain Knowledge
- The mass action law states that the rate of a chemical reaction is proportional to the product of the concentrations of the reacting substances, each raised to the power of its stoichiometric coefficient: v_r = k_r × ∏[X_q]^(s_r,q), where k_r is assumed constant across steady states being compared.
- Reactions whose substrates include metabolites not measured in the intracellular metabolomics dataset must be omitted from RPS computation because the propensity score cannot be calculated without complete substrate abundance information.
- RPS scores represent relative enzymatic substrate availability and predict flux variation assuming kinetic constants remain invariant between cell lines and that allosteric and product-inhibition effects are negligible—a strong simplification suitable only for identifying reactions likely regulated by substrate concentration rather than enzyme abundance.
- The ENGRO2 model comprises 494 reactions and 410 intracellular metabolites distributed across two compartments (cytosol and mitochondrial matrix), requiring metabolomics data to be mapped to the correct subcellular location for accurate stoichiometric calculation.
- Normalization of RPS by the maximum value per reaction is necessary for qualitative concordance analysis with Reaction Activity Scores (RAS) derived from transcriptomics, allowing sign-based agreement assessment without enforcing proportional relationship between the two metrics.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] How does the mass action law formulation translate intracellular metabolomics data into Reaction Propensity Scores (RPS) that quantify the expected relative metabolic flux changes across cell lines based purely on substrate availability differences?: 'INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict how differences in substrate availability translate into differences in metabolic fluxes (metabolic'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] For each reaction r and cell line c, the Reaction Propensity Score (RPS) is computed as the product of substrate concentrations each raised to their stoichiometric coefficients: RPS_r^c = ∏(q=1 to N) [X_q]^(s_r,q), where [X_q] is substrate concentration and s_r,q is the stoichiometric coefficient. If any substrate is unmeasured, the reaction is omitted from the RPS dataset.: 'the RPS score is computed as the product of the concentrations of the reacting substances, with each concentration raised to a power equal to its stoichiometric coefficient. According to the mass'
- `ev_003` from `agent2_synthesis` (agent2_traced): [results] Intracellular metabolomics abundance data (metabolite concentrations in molar or relative units) for five breast cell lines (MCF102A, MCF7, MDAMB231, MDAMB361, SKBR3), including at least 2 biological replicates per cell line: 'We quantified the abundance of intracellular metabolites and prepared libraries for RNA-sequencing at 48h'
- `ev_004` from `agent2_synthesis` (agent2_traced): [results] ENGRO2 constraint-based stoichiometric metabolic network model with Gene-Protein-Reaction (GPR) associations and complete reaction-metabolite stoichiometry: 'The ENGRO2 core model consists of 494 reactions, 410 metabolites and 494 genes'
- `ev_005` from `agent2_synthesis` (agent2_traced): [results] Reaction Propensity Scores (RPS) dataset: a matrix (or table) with metabolic reactions as rows, cell lines as columns, and normalized RPS values (0–1 range) as entries, computed from mass action law applied to substrate concentrations: 'This dataset includes an RPS score, based on the availability of reaction substrates, for (ideally) each input model reaction and for each sample'
- `ev_006` from `agent2_synthesis` (agent2_traced): [abstract] constraint-based stoichiometric metabolic models: 'using constraint-based stoichiometric metabolic models as a scaffold'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] No explicit specification of whether metabolite abundance values are normalized, log-transformed, or left in raw concentration units before RPS computation; unclear if concentrations are treated as absolute (mM) or relative: 'RPS_r^c = ∏([X_q])^s_r,q does not specify the units or normalization of [X_q] metabolite concentration values or whether they are absolute or relative abundances'
- `ev_008` from `agent2_synthesis` (agent2_traced): [results] No explicit listing of how many reactions in ENGRO2 (out of 494 total) are expected to retain RPS values after applying the missing-substrate-omission rule; no count of excluded reactions provided: 'If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset; 81 reactions analyzed for concordance but unclear if 81 is the post-omission'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] No explicit detail on whether stoichiometric coefficients (s_r,q) are sourced from the ENGRO2 stoichiometric matrix directly or computed from GPR rule parsing; unclear if the formula applies stoichiometric integer coefficients or fractional ATP/cofactor stoichiometries: 'the mass action law is assumed: v_r = k_r ∏[X_q]^s_r,q; s_r is the stoichiometric coefficient of substrate X_q in reaction r i.e., how many molecules of the substrate partake to the reaction; no'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] No explicit documentation of how the stage handles metabolites with below-detection-limit (BDL) or missing values in the LC-MS dataset; unclear whether BDL values are set to zero, a floor, or excluded entirely: 'Metabolite extraction and LC-MS profiling method describes instrument parameters and data processing with MassHunter ProFinder but does not address missing or below-detection-limit metabolite'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] No explicit statement on whether the RPS stage applies the same cell-relative model constraints (Type 1, Type 2, Type 3 nutrient/extracellular/transcriptomics constraints) as described for FFD generation, or operates independently on raw metabolomics data: 'INTEGRATE uses intracellular metabolomics datasets and the mass action law formulation to predict differences in metabolic fluxes (metabolic regulation only), neglecting enzymatic activity;'

## Evaluation Strategy
### Direct Checks
- file_exists: ENGRO2 model in SBML or XLSX format from the S2 File or S3 File deposit or Zenodo 10.5281/zenodo.5824504
- file_exists: intracellular metabolomics dataset (LC-MS data) from MetaboLights MTBLS3597 in a tabular or spectral format
- file_format_is: metabolomics input data contains at least columns for metabolite identifiers, compartment location, and concentration measurements across at least two distinct samples or cell lines
- script_runs: execute RPS computation script from qLSLab/integrate GitHub repository or Zenodo deposit with ENGRO2 model and metabolomics data as inputs, no errors on stderr
- output_matches_reference: RPS dataset produced by the stage matches the numerical values and reaction identifiers reported in Figure 5B (ACONT cytosolic flux distribution) and Figure 5C (RPI flux distribution) or in supplementary S4 File concordance table, robust to rounding to 2–3 significant figures
- row_count_equals: RPS dataset contains one row per metabolic reaction in ENGRO2 (494 total reactions) and one column per sample or cell line tested (5 cell lines: MCF102A, SKBR3, MCF7, MDAMB231, MDAMB361); allow for omission of reactions with missing substrate metabolites per evidence_span rule
- field_present: RPS dataset includes a column or metadata field documenting for each reaction which substrate metabolites were available for RPS computation and which were omitted
- value_in_range: all RPS values are positive real numbers (product of metabolite concentrations raised to stoichiometric coefficient powers); verify no negative or NaN values except where reactions were intentionally omitted
- contains_substring: RPS computation output or method section in generated report contains the mass action law formula (or equivalent: product of [X_q]^s_r,q across all substrates q) and identifies the stoichiometric coefficients (s_r,q) sourced from ENGRO2 GPR rules or stoichiometric matrix

### Expert Review
- Verify that the mass action law formulation applied matches the stated assumption in equation (10): RPS_r^c = ∏([X_q])^s_r,q for all substrates, and that kinetic constant k_r is assumed constant across cell lines as stated in the text
- Confirm that reactions with one or more missing substrate metabolites (not detected in LC-MS) are correctly identified and omitted from the RPS dataset, as per the stated rule: 'If one single reaction substrate is missing from the metabolomics measurements, the reaction is omitted from the dataset'
- Assess whether metabolite abundance values used in RPS computation are properly normalized or z-scored within cell lines, or left in raw concentration units; verify consistency with the treatment of RAS values (which are normalized by max RAS across cell lines in equation 3)
- Evaluate whether the RPS stage correctly handles reversible reactions (forward vs. backward flux direction) given that the pipeline converts to irreversible models; confirm that only forward-reaction substrates are used in RPS for reversible reactions split into two irreversible forms
- Review whether compartmentalization is correctly preserved: confirm that RPS distinguishes reactions in different compartments (e.g., cytosolic vs. mitochondrial aconitase, as highlighted in Discussion for ACONT) by using compartment-specific metabolite concentrations

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load intracellular metabolomics data and ENGRO2 stoichiometric model with reaction-metabolite associations.
2. For each reaction and cell line, retrieve all substrate metabolite concentrations from the model stoichiometry.
3. Omit reactions with any missing substrate abundance measurements from the metabolomics dataset.
4. Compute Reaction Propensity Score for each eligible reaction in each cell line using mass action law: RPS = product of [substrate_i]^(stoichiometric_coeff_i).
5. Aggregate RPS across biological replicates within each cell line using median or mean.
6. Normalize RPS within each reaction across cell lines by dividing by the maximum RPS value for that reaction.
7. Validation: verify that RPS dataset contains no reactions with missing substrate abundances, that all values are non-negative, and that normalization produces scores in the range [0, 1] for each reaction.
8. References: source article (DOI: 10.1371/journal.pcbi.1009337); MTBLS3597 (https://www.ebi.ac.uk/metabolights/MTBLS3597); PRJNA767228 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA767228)

## Workflow Ports

**Inputs:**

- `metabolomics_data` — Intracellular metabolomics abundance data
- `engro2_model` — ENGRO2 stoichiometric metabolic model

**Outputs:**

- `rps_dataset` — Normalized Reaction Propensity Scores (RPS) for all eligible reactions across cell lines

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
