---
name: statistical-hypothesis-testing-mean-comparison
description: Use when you have computed raw or standardised correlation scores (or
  other link-ranking metrics) for all possible GCF-MF pairs in a dataset and want
  to verify that validated links (those with known strain co-occurrence or experimental
  confirmation) are significantly enriched at higher score values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3407
  tools:
  - antiSMASH
  - BiG-SCAPE
  - GNPS
  - MIBiG
  - NPLinker
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were
  run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
  and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- we use library MS2 spectra from the public, community-driven GNPS knowledge base
  [33] as a training set for the IOKR model
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  - 10.1371/journal.pcbi.1008920
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# statistical-hypothesis-testing-mean-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compare mean scores between validated and all hypothetical genomic-metabolomic links using t-tests to demonstrate that a standardisation scheme improves the separation and statistical discriminability of true links from background. This skill validates whether a scoring function reliably ranks validated natural product-BGC pairs above random associations.

## When to use

You have computed raw or standardised correlation scores (or other link-ranking metrics) for all possible GCF-MF pairs in a dataset and want to verify that validated links (those with known strain co-occurrence or experimental confirmation) are significantly enriched at higher score values than the population mean. Use this skill when you need to quantify whether a scoring transformation (e.g., standardisation by hypergeometric expectation and variance) improves the statistical power to discriminate true links from background.

## When NOT to use

- You have only a small number of validated links (< 10–20 total), making statistical tests unreliable due to low power and assumption violations.
- Your validated link labels are not reliable (e.g., based on weak homology or unconfirmed predictions rather than experimental co-isolation or high-confidence database curation).
- You are comparing two fundamentally different scoring schemes on entirely different datasets, making it impossible to attribute improvements to the standardisation method itself rather than data properties.

## Inputs

- Raw strain correlation scores for all GCF-MF pairs (numeric vector or table)
- GCF size (#G), MF size (#m), overlap size (#(G∩M)), and population size (#N) metadata for each link
- Boolean or categorical label indicating which GCF-MF links are validated (e.g., via MIBiG homology or Paired Omics Data Platform curation)
- Standardised or alternative-scored versions of the same links (computed by centering and scaling by hypergeometric expectation and variance)

## Outputs

- Mean score for validated links
- Mean score for all links
- t-test statistic and p-value comparing validated vs. all links under each scoring scheme
- Comparison table showing raw vs. standardised score distributions (e.g., histograms, boxplots)
- Enrichment p-value and proportion of validated links above the 90th percentile threshold
- Summary statistics demonstrating improvement in discriminative power (e.g., larger separation in means or smaller p-value)

## How to apply

Partition all GCF-MF links into two groups: validated links (those with confirmed co-occurrence or structural homology to a reference database like MIBiG) and all hypothetical links. Compute the mean score for each group under both the raw and standardised (or alternative) scoring scheme. Perform an independent-samples t-test to compare the mean scores between groups, computing the p-value and recording the t-statistic. The standardised or improved scheme is successful if it achieves a substantially smaller p-value (e.g., moving from p ≈ 0.0001 to p ≈ 10⁻⁶⁴) and a larger effect size (difference in means), demonstrating that standardisation enables better separation of true links. Additionally, compute the proportion of validated links in the top-scoring decile (e.g., above the 90th percentile) and test for enrichment using a chi-square or Fisher exact test to verify that validated links cluster in the tail of the score distribution.

## Related tools

- **NPLinker** (Framework within which strain correlation and IOKR scoring functions are computed and compared via t-tests; provides the computational pipeline for linking GCFs and metabolomic features) — https://github.com/sdrogers/nplinker
- **antiSMASH** (Detects and annotates biosynthetic gene clusters (BGCs) in microbial genomes; output is clustered into GCFs, which are then scored against metabolomic features)
- **BiG-SCAPE** (Clusters antiSMASH-detected BGCs into gene cluster families (GCFs) for grouping similar biosynthetic loci; these GCFs are the genomic entities scored against metabolomic features)
- **GNPS** (Public metabolomics database providing MS2 spectra and molecular structures; used as the source of metabolomic features (MFs) that are paired with GCFs and scored)
- **MIBiG** (Reference database of validated BGC-metabolite pairs with high-confidence structural annotations; used to define the gold-standard validated links against which scoring functions are evaluated)

## Examples

```
from scipy import stats; validated_scores = [3.67, 3.45, 3.89]; all_scores = [-0.01, 0.02, -0.05]; t_stat, p_val = stats.ttest_ind(validated_scores, all_scores); print(f'Mean validated: {np.mean(validated_scores):.4f}, Mean all: {np.mean(all_scores):.4f}, p-value: {p_val:.2e}')
```

## Evaluation signals

- The standardised score achieves a p-value substantially smaller than the raw score (e.g., p < 10⁻⁶⁰ vs. p ≈ 10⁻⁴), indicating improved discriminative power.
- The mean score for validated links is notably higher than for all links under the improved scheme (e.g., mean = 3.67 vs. mean = −0.006 for standardised score), with minimal overlap in distributions visualized as boxplots or histograms.
- The proportion of validated links enriched above the 90th percentile is statistically significant (p < 0.05) and substantially higher than the baseline proportion in the full set.
- The standardised score distribution for all links is centred near zero with unit variance (by design), confirming correct implementation of standardisation by hypergeometric expectation and variance.
- The separation of validated and all-links distributions is reproducible across independent datasets (e.g., Crüsemann, Gross, Leão), indicating that the improvement is robust and not dataset-specific artifact.

## Limitations

- The test assumes that validated links (those with MIBiG homology) represent true positives, but some may be false positives if homology assignments are weak or if functional validity has not been experimentally confirmed.
- Statistical significance (small p-value) does not imply high absolute predictive accuracy; the IOKR and standardised strain correlation scores achieve top-1 accuracy of only ~12%, indicating that other factors (molecular fingerprint choice, kernel function, incomplete homology coverage) limit practical utility.
- The hypergeometric standardisation relies on the assumption that the population is finite and well-defined; if strain annotations are incomplete or metabolomic features are not comprehensively sampled, the expected value and variance estimates may be biased.
- Reliance on MIBiG homology restricts the applicability of validated link definitions to BGCs showing considerable homology with reference entries; novel or divergent BGCs will not be captured in the validation set, potentially underestimating the true performance.
- T-tests assume normality and homogeneity of variance; with large datasets and non-normal score distributions, the test may yield unreliable p-values even when effect sizes are meaningful; permutation tests or rank-based alternatives may be more appropriate.

## Evidence

- [results] Raw score: 83.5144 (all links) vs. 14.6667 (validated); standardised score: −0.0060 (all) vs. 3.6717 (validated); p-value improves from 6.8302 × 10⁻⁴ to 6.8302 × 10⁻⁶⁴: "standardised correlation score achieves a mean of -0.0060 for all links and 3.6717 for validated links (p=6.8302 × 10−64), compared to the raw score's means of 83.5144 and 14.6667 respectively"
- [results] Method of standardisation: centring by hypergeometric expectation and dividing by variance: "For each GCF-MF pair, compute expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] using hypergeometric distribution... s*_corr = (σ_corr(M,G) - E[σ_corr(M,G)]) / √Var[σ_corr(M,G)]"
- [results] Evaluation approach: compute distributions and statistical tests for validated vs. all links: "Generate distributions (histograms and boxplots) comparing raw versus standardised scores for validated links versus all links across the three datasets. Compute mean scores and p-values (t-test) for"
- [results] Enrichment test using percentile cutoff: "Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links, and for the links scoring above the 90th percentile"
- [results] Validation set definition based on reference database homology: "Out of 3316 BGCs in the data set, 2242 could be assigned structure based on similarity to MIBiG entries, and used as candidate set for the 6246 MS2 spectra in the data set"
- [abstract] Rationale for standardisation: enables comparison across links of different sizes: "Does standardising the raw strain correlation score by its hypergeometric expectation and variance improve comparability of scores across GCF-MF links of different sizes?"
