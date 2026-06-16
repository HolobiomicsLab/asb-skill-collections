# SciTask Card: Reproduce the complementarity analysis combining standardised strain correlation and IOKR scores on microbial datasets

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:56:40.523217+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_nplinker`
- Domain: `bioinformatics`
- Subtask categories: `data-analysis`, `statistical-analysis`, `benchmark-evaluation`
- DOI: `10.1371/journal.pcbi.1008920`
- GitHub: `NPLinker/nplinker`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `natural-products`, `microbiome-metabolomics`, `multi-omics-integration`
- Techniques: `correlation-analysis`, `machine-learning`, `database-annotation`, `network-annotation-propagation`

## Research Question
When combining standardised strain correlation and IOKR scores, does the joint top percentile enrichment of validated links exceed that of either individual scoring function alone?

## Connected Finding
Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links (p=2.633×10−4 from IOKR and p=0.0208 from standardised correlation) compared to either individual score alone.

## Task Description
Reproduce the complementarity analysis of standardised strain correlation and IOKR scoring functions on three microbial datasets (Crüsemann, Gross, Leão), demonstrating that links scoring in the joint top percentiles show higher enrichment of validated links than either score alone.

## Inputs
- Crüsemann dataset: GCF-MF links with strain membership and validated link annotations from MSV000078836
- Gross dataset: GCF-MF links with strain membership and validated link annotations from MSV000085018
- Leão dataset: BGC-spectrum links with strain membership and validated link annotations from MSV000085038
- antiSMASH v5.0.0 output for BGC detection in strain assemblies
- BiG-SCAPE v1.0.0 output for GCF clustering
- GNPS MS2 spectra with strain association for metabolomic data

## Expected Outputs
- Table reporting proportion of validated links for each dataset at total, top raw correlation (90th percentile), top standardised correlation (90th percentile), top IOKR (90th percentile), and top combined (both ≥90th percentile) link sets
- P-values and effect size comparison demonstrating significant enrichment of validated links in joint top percentile versus individual score top percentiles across pooled datasets
- Distribution plots (histograms or scatter plots) showing the relative position of validated links within score distributions for all three datasets
- List of top-scoring links for each dataset ranked by combined score with their individual standardised correlation and IOKR scores

## Expected Output File

- `complementarity_analysis_results.csv`

## Landmark Outputs

- `standardised_correlation_scores.csv`
- `iokr_scores.csv`
- `validated_links_per_dataset.csv`
- `percentile_enrichment_table.csv`
- `statistical_comparison_pvalues.txt`
- `score_distribution_plots.png`

## Tools
- antiSMASH
- BiG-SCAPE
- NPLinker
- GNPS
- MIBiG

## Skills
- bgc-mf-link-scoring-standardisation
- strain-correlation-hypergeometric-adjustment
- iokr-fingerprint-space-ranking
- validated-link-enrichment-analysis
- percentile-threshold-based-filtering
- multi-score-complementarity-evaluation
- pooled-statistical-significance-testing

## Workflow Description
1. Load GCF-MF links and their associated strain membership from the Crüsemann, Gross, and Leão datasets processed through antiSMASH v5.0.0 and BiG-SCAPE v1.0.0. 2. Compute raw and standardised strain correlation scores (σ_corr and σ*_corr) for each GCF-MF pair using hypergeometric null distribution with expected value and variance adjustment. 3. Compute IOKR scores (σ_IOKR) for BGC-spectrum links by ranking candidate structures using molecular fingerprint space projection, then assign the maximum IOKR score for each GCF-MF pair. 4. Standardise IOKR scores (σ*_IOKR) using expected value and variance over all potential links. 5. Identify validated links for each dataset from the Paired Omics Data Platform based on curated BGC-spectrum correspondence with antiSMASH BLAST matching (cumulative score ≥10000). 6. Filter links at the 90th percentile threshold for each scoring function independently and for the joint (both functions) criterion. 7. Calculate the proportion of validated links within each percentile group (total links, top raw correlation, top standardised correlation, top IOKR, top combined) for all three datasets. 8. Pool validated link counts across datasets and compute Fisher exact test p-values comparing enrichment of the joint top percentile group versus either single-function top percentile group.

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
- No explicit statement of exact values for the ratio of validated links in the 90th percentile for combined score vs. strain correlation alone, or combined vs. IOKR alone, for each of the three datasets
- No detailed breakdown of how the ℓp-norm exponent was selected or tuned, or whether sensitivity analysis across multiple p values was performed beyond visual inspection mentioned in results
- No explicit count or percentage of BGCs in each dataset that had sufficient MIBiG homology to receive IOKR scores, limiting clarity on the effective sample size
- No statement of whether the combined scoring function was optimised on the same datasets used for performance evaluation, or whether cross-validation or held-out test sets were used

## Domain Knowledge
- Strain correlation scoring relies on the overlap of strains between a GCF and MF, but raw scores are highly dependent on set sizes (GCF size, MF size, population size N); standardisation via hypergeometric expected value and variance correction makes scores comparable across different-sized GCFs and MFs.
- IOKR projects MS2 spectra into molecular fingerprint space and ranks candidate BGCs by similarity; unlike product-type-specific methods, it requires only BGCs with predicted molecular structures (those with MIBiG homology).
- Validated links in paired omics datasets are curated manually by researchers based on literature and BGC-spectrum correspondence; antiSMASH BLAST matching with cumulative score ≥10000 filters for high-confidence structural predictions.
- Complementarity is demonstrated by showing that links scoring in the joint top percentile of both functions are significantly enriched for validated links compared to either function's top percentile alone, as measured by Fisher exact test p-values.
- The 90th percentile threshold is an arbitrary but standard choice for identifying 'high-scoring' links; the magnitude of enrichment p-value (e.g. 2.633 × 10−4 for IOKR-based comparison) indicates the strength of complementarity between the two scoring approaches.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] When combining standardised strain correlation and IOKR scores, does the joint top percentile enrichment of validated links exceed that of either individual scoring function alone?: 'demonstrate their complementarity, and hence the potential in combining the scores. The distribution of the scores for the Crüsemann data set, and the relative score of the validated links, can be'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links (p=2.633×10−4 from IOKR and p=0.0208 from standardised correlation) compared to either individual score alone.: 'the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores (p-value of 2.633 × 10−4 and 0.0208'
- `ev_003` from `agent2_synthesis` (agent2_traced): [results] Crüsemann dataset: GCF-MF links with strain membership and validated link annotations from MSV000078836: 'The Crüsemann data set consists of 120 microbial strains with 8 validated links between a BGC and a MF'
- `ev_004` from `agent2_synthesis` (agent2_traced): [results] Gross dataset: GCF-MF links with strain membership and validated link annotations from MSV000085018: 'the Gross data set consists of 7 strains with 9 validated links between a BGC and a MF'
- `ev_005` from `agent2_synthesis` (agent2_traced): [results] Leão dataset: BGC-spectrum links with strain membership and validated link annotations from MSV000085038: 'the Leão data set contains 4 strains with 5 validated links between a BGC and a specific MS2 spectrum'
- `ev_006` from `agent2_synthesis` (agent2_traced): [results] antiSMASH v5.0.0 output for BGC detection in strain assemblies: 'after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection'
- `ev_007` from `agent2_synthesis` (agent2_traced): [results] BiG-SCAPE v1.0.0 output for GCF clustering: 'BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs'
- `ev_008` from `agent2_synthesis` (agent2_traced): [results] GNPS MS2 spectra with strain association for metabolomic data: 'after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs'
- `ev_009` from `agent2_synthesis` (agent2_traced): [results] Table reporting proportion of validated links for each dataset at total, top raw correlation (90th percentile), top standardised correlation (90th percentile), top IOKR (90th percentile), and top combined (both ≥90th percentile) link sets: 'Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links (first row), and for the links scoring above the 90th'
- `ev_010` from `agent2_synthesis` (agent2_traced): [results] P-values and effect size comparison demonstrating significant enrichment of validated links in joint top percentile versus individual score top percentiles across pooled datasets: 'pooling the links across the three datasets to get a clearer sense of the statistical significance. Considering the 90th percentile per data set for both scores, and adding up the numbers of links in'
- `ev_011` from `agent2_synthesis` (agent2_traced): [results] Distribution plots (histograms or scatter plots) showing the relative position of validated links within score distributions for all three datasets: 'The distribution of the scores for the Crüsemann data set, and the relative score of the validated links, can be seen in the histograms of Fig 6'
- `ev_012` from `agent2_synthesis` (agent2_traced): [results] List of top-scoring links for each dataset ranked by combined score with their individual standardised correlation and IOKR scores: 'the top-scoring links for each data set can be found in S2–S4 Data'
- `ev_013` from `agent2_synthesis` (agent2_traced): [results] antiSMASH: 'genomes were run through antiSMASH v5.0.0 for BGC detection'
- `ev_014` from `agent2_synthesis` (agent2_traced): [results] BiG-SCAPE: 'BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs'
- `ev_015` from `agent2_synthesis` (agent2_traced): [abstract] NPLinker: 'NPLinker, a software framework to link genomic and metabolomic data'
- `ev_016` from `agent2_synthesis` (agent2_traced): [results] GNPS: 'MS2 spectra in specific GNPS data sets'
- `ev_017` from `agent2_synthesis` (agent2_traced): [results] MIBiG: 'established homology to a particular MIBiG BGC'
- `ev_018` from `agent2_synthesis` (agent2_traced): [discussion] No explicit statement of exact values for the ratio of validated links in the 90th percentile for combined score vs. strain correlation alone, or combined vs. IOKR alone, for each of the three datasets: 'By using both scores simultaneously, the prioritisation of hypothetical links can be made more effective.'
- `ev_019` from `agent2_synthesis` (agent2_traced): [discussion] No detailed breakdown of how the ℓp-norm exponent was selected or tuned, or whether sensitivity analysis across multiple p values was performed beyond visual inspection mentioned in results: 'various values of p, or other functions to combine the scores, may improve performance'
- `ev_020` from `agent2_synthesis` (agent2_traced): [discussion] No explicit count or percentage of BGCs in each dataset that had sufficient MIBiG homology to receive IOKR scores, limiting clarity on the effective sample size: 'restricts its use to those BGCs which show considerable homology with MIBiG entries'
- `ev_021` from `agent2_synthesis` (agent2_traced): [results] No statement of whether the combined scoring function was optimised on the same datasets used for performance evaluation, or whether cross-validation or held-out test sets were used: 'we proceed to combine them into a single scoring function for genomic and metabolomic links'

## Evaluation Strategy
### Direct Checks
- file_exists: S1 Data (Linked MIBiG and GNPS databases with SMILES strings and BGC-spectrum links)
- file_exists: S2 Data (High-scoring links from Crüsemann dataset)
- file_exists: S3 Data (High-scoring links from Leão dataset)
- file_exists: S4 Data (High-scoring links from Gross dataset)
- script_runs: NPLinker strain correlation scoring module on input GCF-MF pairs from three datasets, producing standardised scores
- script_runs: NPLinker IOKR scoring module on input spectra and BGC candidates, producing IOKR scores for the three datasets
- script_runs: NPLinker combined scoring function (ℓp-norm with sign adjustment) integrating both standardised scores
- output_matches_reference: ratio of validated links in top 10% by combined score vs. top 10% by strain correlation alone, across all three datasets (reference: Table 4 values)
- output_matches_reference: ratio of validated links in top 10% by combined score vs. top 10% by IOKR alone, across all three datasets (reference: Table 4 values)
- value_in_range: proportion of validated links in 90th percentile for standardised strain correlation score in Crüsemann dataset, robust to choice of percentile threshold
- value_in_range: proportion of validated links in 90th percentile for IOKR score in Crüsemann dataset, robust to choice of percentile threshold
- value_in_range: proportion of validated links in 90th percentile for combined score in Crüsemann dataset, robust to choice of percentile threshold
- row_count_equals: number of GCF-MF pairs evaluated in each of Crüsemann, Gross, and Leão datasets matches supplementary data counts
- contains_substring: Table 4 in published article reports enrichment ratios and p-values for joint top-percentile performance across three datasets

### Expert Review
- Verify that the reported improvement in validated link ratio (Table 4) represents a meaningful biological or chemical validation criterion (e.g., spectral matching, known biosynthetic relationship)
- Assess whether the choice of ℓp-norm exponent (p=0.5 in combined function) is justified and whether alternative exponents were tested and reported
- Evaluate whether the three datasets (Crüsemann, Gross, Leão) represent adequate diversity in microbial ecology, strain characteristics, and compound classes to support generalisability claims
- Review the statistical significance and effect sizes reported in Table 4 to determine whether improvements are both statistically and practically significant

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load GCF-MF link data with strain membership and validated annotations from three curated microbial datasets.
2. Compute standardised strain correlation score for each GCF-MF pair by calculating raw correlation score and adjusting for expected value and variance under hypergeometric null hypothesis.
3. Compute IOKR scores for BGC-spectrum links via molecular fingerprint space projection, then propagate maximum IOKR score to GCF-MF level.
4. Standardise IOKR scores using expected value and variance computed over all potential links in the dataset.
5. Identify the 90th percentile threshold independently for standardised correlation and IOKR scores, then categorise links as: above neither, above only standardised correlation, above only IOKR, or above both (joint).
6. Calculate the proportion of validated links within each category (total, top raw correlation, top standardised correlation, top IOKR, top combined) for each of the three datasets.
7. Pool validated and unvalidated link counts across the three datasets and apply Fisher exact test to compare enrichment of the joint top-percentile group versus individual top-percentile groups.
8. Validation: Demonstrate that the p-value for enrichment of validated links in the joint top percentile (both scores ≥90th percentile) is significantly lower than the p-values for either score alone (p < 0.05 after Bonferroni correction if multiple tests), confirming complementarity of the two scoring functions.
9. References: source article (DOI: 10.1371/journal.pcbi.1008920); MSV000078836 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836); MSV000085038 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038)

## Workflow Ports

**Inputs:**

- `crusemann_links` — Crüsemann GCF-MF links with strain membership and validated annotations ← `task_001/standardised_scores_all_datasets`
- `gross_links` — Gross GCF-MF links with strain membership and validated annotations
- `leao_links` — Leão BGC-spectrum links with strain membership and validated annotations
- `antismash_output` — antiSMASH v5.0.0 BGC predictions for all strains
- `bigscape_output` — BiG-SCAPE v1.0.0 GCF clustering results
- `gnps_spectra` — GNPS MS2 spectra with strain associations

**Outputs:**

- `enrichment_table` — Proportion of validated links by percentile and scoring method for all three datasets
- `statistical_tests` — P-values and comparisons demonstrating complementarity of scoring functions
- `score_distributions` — Histograms or scatter plots of standardised correlation and IOKR scores with validated link positions
- `ranked_links` — Top-scoring links for each dataset ranked by combined score with component scores

**Used:** `urn:asb:port:task_001/standardised_scores_all_datasets`

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
