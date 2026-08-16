---
name: validated-link-proportional-comparison
description: Use when when you have scored GCF-MF (gene cluster family–molecular family) links using two or more complementary scoring approaches (e.g., standardised strain correlation and IOKR), and you need to determine whether combining scores improves discrimination of true links from false positives.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3397
  - http://edamontology.org/topic_0219
  - http://edamontology.org/topic_2269
  tools:
  - NPLinker
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them
- Finally, we present NPLinker, a software framework to link genomic and metabolomic data
- After downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE clusters the BGCs separately by product type
- antiSMASH to score the correspondence between the MIBiG entries and the detected BGCs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker_cq
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

# Validated-Link Proportional Comparison

## Summary

A statistical method to compare the enrichment of validated genomic-metabolomic links across partitioned scoring categories, using proportional analysis and Fisher exact tests to assess whether links meeting combined scoring thresholds are significantly more reliable than links meeting individual thresholds alone.

## When to use

When you have scored GCF-MF (gene cluster family–molecular family) links using two or more complementary scoring approaches (e.g., standardised strain correlation and IOKR), and you need to determine whether combining scores improves discrimination of true links from false positives. Specifically, use this skill when you have ground-truth validated links and want to test whether links exceeding multiple score thresholds simultaneously show significantly higher validation rates than links exceeding either threshold alone.

## When NOT to use

- You have only one scoring function available; the method requires at least two independent scoring approaches to assess complementarity.
- You lack ground-truth validated links; Fisher exact tests require a binary classification (validated/not validated) for each link.
- Your link scores are not independently derived; if the two scoring functions are highly correlated or derived from the same underlying data, the assumption of complementarity is violated.

## Inputs

- GCF-MF link scores (two independent scoring functions, e.g., standardised strain correlation and IOKR scores)
- List of validated links (ground-truth positive pairs)
- Link partition thresholds (percentile values, typically 90th percentile)

## Outputs

- Proportion of validated links per category (single score A, single score B, both scores, neither)
- Fisher exact test p-values comparing dual-threshold to each single-threshold category
- Pooled summary table with per-dataset and cross-dataset results

## How to apply

Partition all GCF-MF links into four mutually exclusive categories based on independent percentile thresholds (e.g., 90th percentile) for each scoring function: (1) above threshold for score A only, (2) above threshold for score B only, (3) above both thresholds, (4) below both thresholds. For each category, calculate the proportion of validated links (validated count ÷ total links in category). Pool data across independent datasets (e.g., Crüsemann, Gross, Leão) and compute two-tailed Fisher exact test p-values comparing the dual-threshold category proportion to each single-threshold category proportion. Tabulate results showing proportions and p-values for each dataset individually and for the pooled analysis. The rationale is that complementarity between scoring functions is demonstrated when the dual-threshold category exhibits significantly enriched validation rates compared to single-threshold sets, indicating that the two approaches capture different aspects of link quality.

## Related tools

- **NPLinker** (Framework integrating genomics and metabolomics data; orchestrates link scoring and provides GCF-MF link inputs for proportional comparison) — https://github.com/sdrogers/nplinker
- **antiSMASH** (Detects biosynthetic gene clusters (BGCs) from microbial genomes; outputs are clustered into GCFs used to define genomic entities in link scoring)
- **BiG-SCAPE** (Clusters BGCs into gene cluster families (GCFs); GCF membership is required input for link scoring and partitioning)
- **MIBiG** (Reference database of characterized BGCs; used by IOKR scoring and provides ground-truth validated BGC–metabolite pairs for analysis)
- **GNPS** (Public metabolomics spectral database; provides MS2 spectra as training data for IOKR and spectra used in link scoring)

## Evaluation signals

- Verify that the four partition categories are mutually exclusive and collectively exhaustive (all links assigned to exactly one category).
- Confirm that the dual-threshold category proportion of validated links is statistically significantly higher than both single-threshold category proportions (p < 0.05), demonstrating complementarity.
- Check that within-dataset p-values and pooled p-values show consistent direction of effect (dual-threshold consistently enriched) across all datasets.
- Validate that proportions are calculated correctly: (count of validated links in category) ÷ (total links in category), not a ratio of validated to unvalidated.
- Ensure Fisher exact test assumptions are met: categories have sufficient sample sizes (typically n ≥ 5 per cell in contingency table) or report exact p-values for sparse counts.

## Limitations

- The method depends critically on the quality and completeness of ground-truth validated links; sparse or biased validation sets can distort enrichment estimates.
- Independence of the two scoring functions is assumed; if scores are correlated or share underlying features, complementarity may be overstated and p-values inflated.
- Percentile thresholds are arbitrary (e.g., 90th percentile); results are sensitive to threshold choice, and no principled method for selecting optimal thresholds is provided in the article.
- Standardised strain correlation scores still suffer from inability to distinguish links with identical patterns of strain presence/absence, limiting discrimination even after standardisation.
- IOKR scoring requires BGC–MIBiG homology to assign molecular structures, restricting its applicability to BGCs with high sequence similarity to reference clusters.

## Evidence

- [other] Partition links into four categories: above 90th percentile for standardised correlation only, above 90th percentile for IOKR only, above 90th percentile for both scores, and below 90th percentile for both.: "Partition links into four categories: above 90th percentile for standardised correlation only, above 90th percentile for IOKR only, above 90th percentile for both scores, and below 90th percentile"
- [other] For each category, compute the proportion of validated links (number of validated links in category / total links in category).: "For each category, compute the proportion of validated links (number of validated links in category / total links in category)."
- [other] Pool data across all three datasets and compute Fisher exact test p-values comparing the proportion of validated links in the dual-score (both scores ≥90th percentile) category to each single-score category.: "Pool data across all three datasets and compute Fisher exact test p-values comparing the proportion of validated links in the dual-score (both scores ≥90th percentile) category to each single-score"
- [results] Links scoring above the 90th percentile on both standardised strain correlation and IOKR scores are significantly enriched for validated links (p-value 2.633 × 10−4 from IOKR and 0.0208 from standardised strain correlation), demonstrating complementarity of the two scoring approaches.: "Links scoring above the 90th percentile on both standardised strain correlation and IOKR scores are significantly enriched for validated links (p-value 2.633 × 10−4 from IOKR and 0.0208 from"
- [abstract] using multiple link-scoring functions together makes it easier to prioritise true links relative to others: "using multiple link-scoring functions together makes it easier to prioritise true links relative to others"
- [other] Tabulate results showing proportions and p-values for all three datasets and pooled analysis, matching the structure and values reported in Table 2 and Table D in S1 Text.: "Tabulate results showing proportions and p-values for all three datasets and pooled analysis, matching the structure and values reported in Table 2 and Table D in S1 Text."
