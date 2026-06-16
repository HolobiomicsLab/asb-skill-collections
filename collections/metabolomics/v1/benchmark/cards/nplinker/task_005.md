# SciTask Card: Analyze the effect of varying combination function parameters on validated-link enrichment beyond reported p values

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:56:40.523217+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_nplinker`
- Domain: `bioinformatics`
- Subtask categories: `data-analysis`, `statistical-analysis`, `benchmark-evaluation`
- DOI: `10.1371/journal.pcbi.1008920`
- GitHub: `NPLinker/nplinker`
- Input from: `task_003`

## Classification

- Task kind: `analysis`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `natural-products`, `microbiome-metabolomics`, `multi-omics-integration`
- Techniques: `correlation-analysis`, `machine-learning`, `database-annotation`, `network-annotation-propagation`

## Research Question
How does the choice of exponent p in the ℓp-norm combination function affect the enrichment of validated links in the top-ranking BGC-metabolite predictions?

## Connected Finding
The ℓ1/2-norm combination function assigned the best rank to validated links in 10 out of 15 cases, including three instances where it substantially outperformed either individual scoring function alone (e.g., retimycin A ranked at 253 vs. much higher individual ranks).

## Task Description
Systematically evaluate how the choice of exponent p and alternative combination function forms (beyond ℓ₁, ℓ₂, ℓ₁/₂ evaluated in Table 4) affect the enrichment ratio of validated links in the top-scoring percentiles across three microbial datasets. Produce a sensitivity analysis report quantifying validated-link enrichment as a function of combination function parameters.

## Inputs
- task_003.expected_outputs[0]: Table reporting proportion of validated links for each dataset at total, top raw correlation (90th percentile), top standardised correlation (90th percentile), top IOKR (90th percentile), and top combined (both ≥90th percentile) link sets
- Standardised strain correlation scores (s'_corr) and standardised IOKR scores (s'_IOKR) for all GCF-MF links in Crüsemann, Gross, and Leão datasets
- Validated link ground truth annotations for Crüsemann (8 validated links), Gross (9 validated links), and Leão (5 validated links) datasets

## Expected Outputs
- Table of validated-link enrichment ratios (proportion of validated links / proportion of all links) indexed by combination function type and exponent p, for 90th and 95th percentiles across all three datasets
- Heatmap visualisation of validated-link enrichment as a function of exponent p (0.5–3.0) and combination function type, with colour intensity proportional to enrichment ratio
- Statistical significance test results (chi-square or Fisher exact p-values) comparing validated-link enrichment for each combination function against the baseline (either score alone) and against the reported ℓ₁/₂ function
- Line plot showing rank improvement (median percentile rank of validated links) as a function of p for the ℓ_p family of norms

## Expected Output File

- `combination_function_sensitivity_report.csv`

## Landmark Outputs

- `enrichment_by_p.csv`
- `enrichment_heatmap.png`
- `rank_percentile_vs_p.png`
- `significance_test_matrix.csv`

## Tools
- antiSMASH
- Python (numpy, scipy.stats, pandas, matplotlib, seaborn)

## Skills
- combination-function-parameterisation
- enrichment-ratio-calculation
- statistical-significance-testing-multicomparison
- scoring-function-sensitivity-analysis
- validated-link-ranking-comparison

## Workflow Description
1. Load pre-computed standardised strain correlation scores (s'_corr) and standardised IOKR scores (s'_IOKR) for all GCF-MF links in the Crüsemann, Gross, and Leão datasets, along with validated link annotations. 2. For each dataset, compute combined scores using the ℓ_p-norm formula s_sum = sgn(s'_corr)|s'_corr|^p + sgn(s'_IOKR)|s'_IOKR|^p across a range of p values (0.5 to 3.0 in 0.1 increments, plus intermediate values 0 < p < 1). 3. For each (p, dataset) combination, rank all GCF-MF links by combined score and compute the proportion of validated links in the 90th and 95th percentile tiers. 4. Test alternative combination functions (e.g. weighted linear combinations with α ∈ [0, 1], Chebyshev distance max(|s'_corr|, |s'_IOKR|), harmonic mean, geometric mean) and compute validated-link enrichment ratios for each. 5. Pool results across the three datasets and perform significance testing (chi-square or Fisher exact test) to identify which combination functions yield statistically significant enrichment (p < 0.05) relative to using either score alone. 6. Visualise enrichment ratio and rank improvement (validated link rank percentile) as heatmaps and line plots indexed by p and function type. 7. Validation: confirm that results reproduce reported enrichment for ℓ₁/₂ (documented in Table 4 and Table D of supplementary text) and that the best-performing alternative function achieves equal or superior enrichment compared to the three functions reported in the paper.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `nplinker.pdf` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| massive | `MSV000078836` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836 | Cs a number of strains for the st From this platform we con MSV000078836 [38], MSV Cru¨semann, Gross and Leã The Cru¨semann data set |
| massive | `MSV000085038` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038 | ets each with numerous validated links: V000085018 [39] and MSV000085038 [40], hereafter referred to as ão, respectively. et consist |

## Missing Information
- No explicit statement of which values of p (exponent) were tested beyond those shown in Table 4, or whether additional combination function forms were evaluated at all.
- No reporting of validated-link enrichment ratios or p-values for the sensitivity analysis across different p values; only the baseline result (p=0.5 in combined function) is reported in Table 2.
- No supplementary figure or table explicitly presenting enrichment metrics as a function of combination function parameters for the three datasets.
- No quantitative guidance on optimal choice of p or combination function form; discussion mentions potential improvements but provides no empirical justification for which variant performs best.

## Domain Knowledge
- The ℓ_p-norm generalises Euclidean (p=2) and Manhattan (p=1) distance metrics; values 0 < p < 1 violate the triangle inequality but remain valid ranking functions (no norm property required for scoring).
- Validated-link enrichment is computed as (proportion of validated links in percentile tier) / (proportion of all links in that tier), pooled across three datasets; significance is assessed via chi-square contingency test after summing counts across datasets.
- The reported ℓ₁/₂ function (Table 4) achieved best rank for 10 out of 15 validated links in the Crüsemann dataset; alternative functions must be evaluated on the same pooled three-dataset cohort to ensure fair comparison.
- Sign-adjusted combination (sgn multiplier on each score term) penalises links with opposite sign contributions; this asymmetry may favour ℓ_p values and function forms that better match the actual correlation structure between the two scores (visible in Fig 6 scatterplots).

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Table of validated-link enrichment ratios (proportion of validated links / proportion of all links) indexed by combination function type and exponent p, for 90th and 95th percentiles across all three datasets, Heatmap visualisation of validated-link enrichment as a function of exponent p (0.5–3.0) and combination function type, with colour intensity proportional to enrichment ratio, Statistical significance test results (chi-square or Fisher exact p-values) comparing validated-link enrichment for each combination function against the baseline (either score alone) and against the reported ℓ₁/₂ function, Line plot showing rank improvement (median percentile rank of validated links) as a function of p for the ℓ_p family of norms.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] How does the choice of exponent p in the ℓp-norm combination function affect the enrichment of validated links in the top-ranking BGC-metabolite predictions?: 'Fig 8 shows the set of points (x, y) such that ℓp(x, y) = 1 for three values of p, demonstrating the parallels of the circle in ℓp to the distribution of scores'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] The ℓ1/2-norm combination function assigned the best rank to validated links in 10 out of 15 cases, including three instances where it substantially outperformed either individual scoring function alone (e.g., retimycin A ranked at 253 vs. much higher individual ranks).: 'In 10 out of the 15 validated links considered, the ℓ'1/2 score assigns the best rank to the validated link, including in three out of the first five cases where the link is unambiguous. For'
- `ev_003` from `agent2_synthesis` (agent2_traced): [results] Standardised strain correlation scores (s'_corr) and standardised IOKR scores (s'_IOKR) for all GCF-MF links in Crüsemann, Gross, and Leão datasets: 'Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links (first row), and for the links scoring above the 90th'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Validated link ground truth annotations for Crüsemann (8 validated links), Gross (9 validated links), and Leão (5 validated links) datasets: 'The Crüsemann data set consists of 120 microbial strains with 8 validated links between a BGC and a MF, the Gross data set consists of 7 strains with 9 validated links between a BGC and a MF, and the'
- `ev_005` from `agent2_synthesis` (agent2_traced): [results] Table of validated-link enrichment ratios (proportion of validated links / proportion of all links) indexed by combination function type and exponent p, for 90th and 95th percentiles across all three datasets: 'Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links (first row), and for the links scoring above the 90th'
- `ev_006` from `agent2_synthesis` (agent2_traced): [results] Heatmap visualisation of validated-link enrichment as a function of exponent p (0.5–3.0) and combination function type, with colour intensity proportional to enrichment ratio: 'Fig 8 shows the set of points (x, y) such that ℓ_p(x, y) = 1, for three different values of p. This shows the form of the iso-lines of scores using the ℓ_p function for different values of p to'
- `ev_007` from `agent2_synthesis` (agent2_traced): [results] Statistical significance test results (chi-square or Fisher exact p-values) comparing validated-link enrichment for each combination function against the baseline (either score alone) and against the reported ℓ₁/₂ function: 'Considering the 90th percentile per data set for both scores, and adding up the numbers of links in each category (validated or unvalidated, and scoring above 90th percentile for either or both'
- `ev_008` from `agent2_synthesis` (agent2_traced): [results] Line plot showing rank improvement (median percentile rank of validated links) as a function of p for the ℓ_p family of norms: 'Table 4. The first two columns show the number of links scoring higher or equal to the validated link ordered by the IOKR and the standardised correlation scores, while the next three columns show'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Python (numpy, scipy.stats, pandas, matplotlib, seaborn): 'NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] No explicit statement of which values of p (exponent) were tested beyond those shown in Table 4, or whether additional combination function forms were evaluated at all.: 'Various values of p, or other functions to combine the scores, may improve the results'
- `ev_011` from `agent2_synthesis` (agent2_traced): [results] No reporting of validated-link enrichment ratios or p-values for the sensitivity analysis across different p values; only the baseline result (p=0.5 in combined function) is reported in Table 2.: 'Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links, and for the links scoring above the 90th percentile'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No supplementary figure or table explicitly presenting enrichment metrics as a function of combination function parameters for the three datasets.: 'By using both scores simultaneously, the prioritisation of hypothetical links can be made more effective'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No quantitative guidance on optimal choice of p or combination function form; discussion mentions potential improvements but provides no empirical justification for which variant performs best.: 'Various values of p, or other functions to combine the scores, may improve the results'

## Evaluation Strategy
### Direct Checks
- verify that S1 Data, S2 Data, S3 Data, and S4 Data files (containing high-scoring links from Crüsemann, Leão, and Gross datasets) are present in the supplementary materials
- verify that the reported combined score formula s'₁/p = sgn(s'_corr)|s'_corr|^(1/p) + sgn(s'_IOKR)|s'_IOKR|^(1/p) is correctly implemented in NPLinker source code (zenodo.org/record/4680579) or referenced supplementary code
- value_in_range: confirm that p values tested in sensitivity analysis span at least the range [0.5, 1.0, 2.0, 4.0] or comparable exponents, with documentation of which values were evaluated
- value_in_range: confirm that validated-link ratio (proportion of validated links among top-scoring links at 90th percentile or equivalent threshold) is reported for each combination function variant, with ratios between 0 and 1
- output_matches_reference: for any combination function form reported, verify that the enrichment p-value and validated-link count matches the corresponding entry in Table 2 or supplementary tables for the baseline case (p=0.5 or equivalent baseline exponent)
- file_exists: verify presence of a supplementary table, figure, or dataset file reporting systematic variation of p and alternative combination functions with corresponding enrichment metrics
- script_runs: verify that a reproducible script or Jupyter notebook exists (in the NPLinker repository or supplementary materials) that accepts the precomputed IOKR and standardised strain correlation score outputs and produces the sensitivity analysis outputs without requiring re-computation of IOKR or strain correlation scores

### Expert Review
- Assess whether the choice of alternative combination function forms (beyond ℓp-norm) is mathematically sound and biologically justified—e.g., weighted linear combinations, geometric means, other norms
- Evaluate whether the reported sensitivity trend (validated-link ratio as a function of p) is consistent across the three datasets (Crüsemann, Leão, Gross) and whether any deviation is explained or flagged
- Judge whether the span of p values and combination functions tested is sufficiently comprehensive to characterize the sensitivity landscape, or whether critical parameter regimes may have been missed
- Review whether the authors discuss or acknowledge limitations in extrapolating sensitivity findings to untested product classes or datasets beyond the three reported microbial strains

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Load pre-computed standardised strain correlation and IOKR scores for all links across the three microbial datasets (Crüsemann, Gross, Leão) and their validated-link annotations.
2. Compute combined scores using the ℓ_p-norm with sign adjustment across a systematic range of p values (0.5 to 3.0 in 0.1 increments, plus fractional values 0 < p < 1) and alternative function forms (weighted linear, Chebyshev, harmonic mean, geometric mean).
3. For each combination function and parameter set, rank all GCF-MF links and calculate validated-link enrichment ratios at the 90th and 95th percentile thresholds.
4. Pool results across the three datasets and perform chi-square contingency tests to determine statistical significance (p < 0.05) of enrichment for each function relative to baseline (individual scores alone) and to the reported ℓ₁/₂ function.
5. Visualise enrichment and rank metrics as heatmaps and line plots indexed by function type and exponent p.
6. Validation: verify that ℓ₁/₂ enrichment ratios match Table 4 and Table D of supplementary text; confirm that the best-performing alternative function achieves equal or superior enrichment compared to the three originally reported functions.
7. References: source article (DOI: 10.1371/journal.pcbi.1008920); MSV000078836 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836); MSV000085038 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038)

## Workflow Ports

**Inputs:**

- `scored_links_crusemannds` — Standardised strain correlation and IOKR scores for all GCF-MF links in Crüsemann dataset
- `scored_links_gross` — Standardised strain correlation and IOKR scores for all GCF-MF links in Gross dataset
- `scored_links_leao` — Standardised strain correlation and IOKR scores for all GCF-MF links in Leão dataset
- `validated_links_all` — Validated GCF-MF link annotations across three datasets

**Outputs:**

- `enrichment_table` — Enrichment ratios indexed by combination function and exponent p
- `enrichment_heatmap` — Heatmap of validated-link enrichment as function of p and function type
- `significance_results` — Statistical test results for all combinations versus baseline and ℓ₁/₂
- `rank_improvement_plot` — Line plot of median validated link rank percentile versus p

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
