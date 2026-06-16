# SciTask Card: Reproduce the size-bias demonstration and standardised strain correlation score computation on microbial datasets

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:56:40.523217+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_nplinker`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `statistical-analysis`, `visualization`
- DOI: `10.1371/journal.pcbi.1008920`
- GitHub: `NPLinker/nplinker`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `natural-products`, `microbiome-metabolomics`, `multi-omics-integration`
- Techniques: `correlation-analysis`, `machine-learning`, `database-annotation`, `network-annotation-propagation`

## Research Question
Does standardising the raw strain correlation score by its hypergeometric expectation and variance improve comparability of scores across GCF-MF links of different sizes?

## Connected Finding
The standardised correlation score achieves a mean of -0.0060 for all links and 3.6717 for validated links (p=6.8302 × 10−64), compared to the raw score's means of 83.5144 and 14.6667 respectively, demonstrating that standardisation successfully enables comparison across links with different GCF and MF sizes.

## Task Description
Implement the standardised strain correlation score (σ*_corr) by computing hypergeometric expectation and variance of raw scores, then apply it to Crüsemann, Gross, and Leão datasets to reproduce reported score distributions and validated-link positions shown in S1 Fig.

## Inputs
- Crüsemann dataset: genomic data (antiSMASH-predicted BGCs and BiG-SCAPE GCFs) and metabolomic data (MS2 spectra grouped into MFs) with 120 strains and 8 validated links
- Gross dataset: genomic and metabolomic data with 7 strains and 9 validated links between a BGC and a MF
- Leão dataset: genomic and metabolomic data with 4 strains and 5 validated links between a BGC and a specific MS2 spectrum
- Raw strain correlation scores computed for all GCF-MF pairs in each dataset using the scoring function: start at zero; add 10 if strain produces metabolite and has BGC in GCF; subtract 10 if strain produces metabolite but no BGC in GCF; add 1 if strain has BGC but no metabolite; leave unchanged otherwise

## Expected Outputs
- Standardised strain correlation scores (s*_corr) for all GCF-MF pairs in the three datasets, including mean score for all links and validated links with p-value
- Distribution histograms and scatter plots (Figure 5 / S1 Fig) showing raw versus standardised strain correlation scores for validated links relative to all links in the three datasets
- Statistical test results (t-test p-values) comparing mean scores for validated links versus all links under both raw and standardised scoring, demonstrating that standardisation enables reliable comparison
- Table of proportions of validated links among top-scoring links (90th percentile and above) for raw, standardised, and combined scores across all three datasets

## Expected Output File

- `standardised_strain_correlation_scores.csv`

## Landmark Outputs

- `raw_correlation_scores.csv`
- `hypergeometric_expectation_variance.csv`
- `standardised_correlation_scores.csv`
- `score_distributions.png`
- `validated_vs_all_links_statistics.csv`
- `90th_percentile_enrichment_table.csv`

## Tools
- antiSMASH
- BiG-SCAPE
- GNPS
- MIBiG

## Skills
- strain-correlation-score-standardisation
- hypergeometric-distribution-calculation
- gcf-mf-link-scoring
- score-distribution-visualization
- statistical-hypothesis-testing-mean-comparison
- enrichment-analysis-validated-links

## Workflow Description
1. Load raw strain correlation scores for all GCF-MF pairs in each dataset (Crüsemann, Gross, Leão), extracting GCF sizes (#G), MF sizes (#m), overlap sizes (#(G∩M)), and population size (#N). 2. For each GCF-MF pair, compute expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] using hypergeometric distribution over all possible overlap sizes k, where p(o=k) follows hypergeometric with parameters N, m, g, and overlap. 3. Calculate standardised correlation score s*_corr = (σ_corr(M,G) - E[σ_corr(M,G)]) / √Var[σ_corr(M,G)] for all links. 4. Generate distributions (histograms and boxplots) comparing raw versus standardised scores for validated links versus all links across the three datasets. 5. Compute mean scores and p-values (t-test) for validated links versus all links under both scoring schemes to verify standardisation improves separation. 6. Reproduce S1 Fig showing raw and standardised strain correlation score distributions with validated links highlighted.

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
- Exact mathematical formula for the hypergeometric expectation and variance used to standardise the raw strain correlation score σ_corr into σ*_corr
- Detailed algorithm or pseudocode for computing standardised strain correlation score across all potential GCF-spectrum pairs in each dataset
- Specification of how many strains were shared between GCFs and MFs in the Crüsemann, Gross, and Leão datasets, and how this affects the hypergeometric calculation
- Threshold or cutoff criteria for including or excluding strain correlation pairs in the standardisation computation (e.g., minimum strain overlap, maximum background correlation)

## Domain Knowledge
- Strain correlation score raw form: 10 points for co-presence of metabolite in strain and BGC in GCF, −10 for metabolite without BGC, +1 for neither metabolite nor BGC, 0 if BGC without metabolite; this weighting heavily biases raw scores toward large GCFs and MFs with many strains.
- Hypergeometric distribution null model: assuming independence of GCF and MF strain sets, the probability of observing an overlap of k strains between GCF G (size g) and MF M (size m) in population N follows Hypergeometric(N, m, g); expected value and variance of this distribution are used to standardise raw scores.
- Standardisation formula: s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr] yields mean 0 and variance 1, enabling direct comparison of scores across links of different GCF and MF sizes and allowing pooling of links from multiple datasets for significance testing.
- A validated link is one explicitly cited in the literature or Paired Omics Data Platform as confirmed through heterologous expression, spectroscopic validation, or comparative genomics; in the test datasets used, validated links are typically 5–15 per dataset, representing a tiny fraction of all possible GCF-MF combinations.
- 90th percentile ranking: comparison of proportions of validated links above 90th percentile versus all links reveals enrichment; significance is assessed by pooling validated and unvalidated links across all three datasets and computing binomial p-values to account for small sample size per dataset.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Does standardising the raw strain correlation score by its hypergeometric expectation and variance improve comparability of scores across GCF-MF links of different sizes?: 'This effect of GCF and MF sizes on the strain correlation score can be mitigated by standardising the score. For a given GCF and MF, let G and M be the sets of strains contributing to the GCF and the'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] The standardised correlation score achieves a mean of -0.0060 for all links and 3.6717 for validated links (p=6.8302 × 10−64), compared to the raw score's means of 83.5144 and 14.6667 respectively, demonstrating that standardisation successfully enables comparison across links with different GCF and MF sizes.: 'Raw correlation 83.5144 (all), 14.6667 (validated); Standardised correlation -0.0060 (all), 3.6717 (validated), p-value 6.8302 × 10−64'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Crüsemann dataset: genomic data (antiSMASH-predicted BGCs and BiG-SCAPE GCFs) and metabolomic data (MS2 spectra grouped into MFs) with 120 strains and 8 validated links: 'The Crüsemann data set consists of 120 microbial strains with 8 validated links between a BGC and a MF'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Gross dataset: genomic and metabolomic data with 7 strains and 9 validated links between a BGC and a MF: 'the Gross data set consists of 7 strains with 9 validated links between a BGC and a MF'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Leão dataset: genomic and metabolomic data with 4 strains and 5 validated links between a BGC and a specific MS2 spectrum: 'the Leão data set contains 4 strains with 5 validated links between a BGC and a specific MS2 spectrum'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Raw strain correlation scores computed for all GCF-MF pairs in each dataset using the scoring function: start at zero; add 10 if strain produces metabolite and has BGC in GCF; subtract 10 if strain produces metabolite but no BGC in GCF; add 1 if strain has BGC but no metabolite; leave unchanged otherwise: 'starting from zero, for each strain in the population, add 10 to the score if the strain produces the metabolite and has a BGC in the GCF, subtract 10 from the score if the strain produces the'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Standardised strain correlation scores (s*_corr) for all GCF-MF pairs in the three datasets, including mean score for all links and validated links with p-value: 'Standardising the score gives a mean score of -0.006 for all links, and 3.6717 for validated links (Table 1)'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] Distribution histograms and scatter plots (Figure 5 / S1 Fig) showing raw versus standardised strain correlation scores for validated links relative to all links in the three datasets: 'Distribution of the raw and standardised strain correlation scores, as well as the distribution of the scores for validated links (in black) relative to the distribution of scores for all links'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Statistical test results (t-test p-values) comparing mean scores for validated links versus all links under both raw and standardised scoring, demonstrating that standardisation enables reliable comparison: 'the null hypothesis for testing the validity of the scoring function is that both distributions of scores (for validated links and all links) have the same mean'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] Table of proportions of validated links among top-scoring links (90th percentile and above) for raw, standardised, and combined scores across all three datasets: 'Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links (first row), and for the links scoring above the 90th'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] antiSMASH: 'after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] BiG-SCAPE: 'and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] GNPS: 'the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] MIBiG: 'To assign one or more molecular structures to BGCs, according to how many high-scoring matches are found in MIBiG'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] Exact mathematical formula for the hypergeometric expectation and variance used to standardise the raw strain correlation score σ_corr into σ*_corr: 'The standardised strain correlation score makes it more effective at prioritising validated links relative to all links, and introduced IOKR as a complementary feature-based scoring function.'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] Detailed algorithm or pseudocode for computing standardised strain correlation score across all potential GCF-spectrum pairs in each dataset: 'The standardised strain correlation score still suffers from the drawback inherent in correlation-based scoring, of not being able to distinguish between potential links showing the same pattern of'
- `ev_017` from `agent2_synthesis` (agent2_traced): [discussion] Specification of how many strains were shared between GCFs and MFs in the Crüsemann, Gross, and Leão datasets, and how this affects the hypergeometric calculation: 'An obvious example is prioritising multiple singleton GCFs and MFs for the same strain. As a complementary scoring function to the strain correlation score, IOKR does not have this limitation.'
- `ev_018` from `agent2_synthesis` (agent2_traced): [discussion] Threshold or cutoff criteria for including or excluding strain correlation pairs in the standardisation computation (e.g., minimum strain overlap, maximum background correlation): 'The standardised strain correlation score makes it more effective at prioritising validated links relative to all links'

## Evaluation Strategy
### Direct Checks
- file_exists: verify S1 Fig exists in supplementary materials or deposited package
- file_format_is: S1 Fig output format is PDF or PNG
- script_runs: NPLinker implementation of standardised strain correlation score (σ*_corr) executes without errors on Crüsemann, Gross, and Leão datasets from Paired Omics Data Platform
- output_matches_reference: histogram distributions for raw and standardised strain correlation scores in reproduced S1 Fig match published S1 Fig (visually robust to minor plotting parameter choices)
- value_in_range: computed standardised strain correlation score for all links in Crüsemann dataset is approximately −0.0060 (parameter-sensitive; exact match not required, allow ±5% tolerance)
- value_in_range: computed standardised strain correlation score for validated links in Crüsemann dataset is approximately 3.6717 (parameter-sensitive; exact match not required, allow ±5% tolerance)
- contains_substring: reproduced figure caption or metadata explicitly identifies validated link positions marked within score distribution histogram
- format_is: computed σ*_corr scores are numeric, real-valued, with no missing values across all three datasets

### Expert Review
- Verify that hypergeometric expectation and variance calculations used to standardise raw strain correlation score are statistically sound and correctly map the raw score distribution to zero-mean standardised form
- Confirm that the standardised score formula correctly implements the reported mathematical definition of σ*_corr (trace back to Methods section for exact formula; not present in discussion excerpt)
- Validate that validated link positions in reproduced histograms align with expected enrichment signal reported in text (e.g., p-value of 2.483 × 10−11 at 90th percentile)
- Review whether handling of ties, missing data, or edge cases in strain correlation (e.g., links with single shared strain) is consistent with article description

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load GCF-MF pairs for each dataset (Crüsemann, Gross, Leão) and extract GCF size, MF size, overlap size, and population size parameters.
2. Compute hypergeometric expected value E[σ_corr] and variance Var[σ_corr] for each pair by summing over all possible overlap sizes weighted by hypergeometric probabilities.
3. Calculate standardised score s*_corr = (raw_score − E[σ_corr]) / √Var[σ_corr] for all GCF-MF pairs.
4. Generate distribution histograms and summary statistics (mean, p-value) for validated versus all links under both raw and standardised scoring.
5. Determine enrichment of validated links at 90th percentile for each dataset and pool across datasets to compute significance.
6. Validation: standardised score demonstrates significantly higher p-value for separation of validated from non-validated links (p < 2.5 × 10⁻¹¹) and higher proportion of validated links in top 90th percentile, consistent with reported Table 1 and Table 2 values.
7. References: source article (DOI: 10.1371/journal.pcbi.1008920); MSV000078836 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000078836); MSV000085038 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000085038)

## Workflow Ports

**Inputs:**

- `crusemann_genomics` — Crüsemann genomic data (BGCs and GCFs)
- `crusemann_metabolomics` — Crüsemann metabolomic data (MS2 spectra and MFs)
- `gross_genomics` — Gross genomic data (BGCs and GCFs)
- `gross_metabolomics` — Gross metabolomic data (MS2 spectra and MFs)
- `leao_genomics` — Leão genomic data (BGCs and GCFs)
- `leao_metabolomics` — Leão metabolomic data (MS2 spectra and MFs)
- `validated_links_crusemann` — Crüsemann validated BGC-MF links
- `validated_links_gross` — Gross validated BGC-MF links
- `validated_links_leao` — Leão validated BGC-spectrum links

**Outputs:**

- `standardised_scores_all_datasets` — Standardised strain correlation scores for all GCF-MF pairs
- `score_distributions_figure` — Distribution histograms of raw vs standardised scores (S1 Fig)
- `statistical_test_results` — Mean scores and p-values for validated vs all links
- `enrichment_table_90th_percentile` — Table of proportions of validated links at 90th percentile

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
