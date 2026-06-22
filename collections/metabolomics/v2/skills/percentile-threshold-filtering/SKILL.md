---
name: percentile-threshold-filtering
description: Use when you have computed multiple independent scoring functions (e.g., standardised strain correlation and IOKR) for a large set of potential genomic–metabolomic links and wish to identify subsets enriched for validated links.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0202
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3697
  tools:
  - NPLinker
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# percentile-threshold-filtering

## Summary

Filter genomic–metabolomic links by computing independent percentile thresholds (e.g., 90th) on scoring functions and partitioning links into single- or multi-score categories. This enables enrichment analysis of validated links and prioritization of high-confidence predictions by combining complementary scoring approaches.

## When to use

You have computed multiple independent scoring functions (e.g., standardised strain correlation and IOKR) for a large set of potential genomic–metabolomic links and wish to identify subsets enriched for validated links. Use this skill when you need to (1) compare the discriminatory power of individual scores, (2) test whether combining scores above independent percentile thresholds yields statistically significant enrichment, or (3) prioritize candidate links by dual-score membership.

## When NOT to use

- Scores are not standardised or lack comparable distributions across links (use standardisation/z-score normalisation first).
- You have only one scoring function (use univariate percentile filtering instead; dual-score comparison requires ≥2 independent scores).
- No validated links are available to benchmark enrichment (enrichment comparison requires ground truth labels).
- Sample sizes are very small (Fisher exact test may lack power; consider reporting effect sizes and descriptive statistics only).

## Inputs

- GCF–MF link scores (standardised strain correlation scores and IOKR scores)
- Gold-standard validated link labels (binary: validated or not)
- Multiple paired-omics datasets (e.g., MSV000078836, MSV000085018, MSV000085038)

## Outputs

- Partitioned link sets by percentile category (single-score-A-only, single-score-B-only, dual-score, below-both)
- Enrichment table with proportions of validated links per category and per dataset
- Fisher exact test p-values comparing dual-score to single-score categories
- Pooled enrichment results across all datasets

## How to apply

First, compute the percentile thresholds (e.g., 90th) independently for each scoring function and each dataset (e.g., Crüsemann, Gross, Leão). Partition all links into disjoint categories: above threshold for score A only, above threshold for score B only, above threshold for both, and below threshold for both. For each category, calculate the proportion of validated links (number of validated links in category ÷ total links in category). Pool data across datasets and apply Fisher exact test to compare the proportion of validated links in dual-threshold category versus single-threshold categories. Report proportions, p-values, and effect sizes. The rationale: standardised scores have comparable distributions across links within and across GCFs/MFs, allowing percentile thresholds to be applied uniformly; dual-threshold enrichment demonstrates complementarity and reduces false-positive rates.

## Related tools

- **NPLinker** (Framework for linking genomic and metabolomic data; integrates scoring functions and supports filter-based link prioritisation) — https://github.com/sdrogers/nplinker
- **antiSMASH** (Detects biosynthetic gene clusters (BGCs) from genomic sequences; output BGCs are clustered and scored for metabolomic links)
- **BiG-SCAPE** (Clusters BGCs into Gene Cluster Families (GCFs); GCF–MF links are then scored and filtered)
- **GNPS** (Provides community MS2 spectra library for IOKR model training and metabolomic data source)
- **MIBiG** (Reference database of characterised BGCs used for IOKR model training and validation link annotation)

## Evaluation signals

- Percentile thresholds are computed independently per scoring function and per dataset (verify threshold values differ appropriately by function and dataset).
- Link partition categories are exhaustive and mutually exclusive (total links = single-A + single-B + dual + below-both).
- Dual-score category shows statistically significant enrichment (p < 0.05 in Fisher exact test) compared to at least one single-score category, demonstrating complementarity.
- Proportions of validated links in dual-score category exceed those in single-score categories (visual consistency across all three datasets).
- Effect sizes and 95% confidence intervals on proportions do not overlap between dual-score and below-both categories.

## Limitations

- Percentile thresholds are sensitive to distributional properties of scores; poorly standardised or skewed scores may yield uninformative thresholds.
- Enrichment analysis requires sufficiently large numbers of validated links per category; small sample sizes reduce statistical power and reliability of p-value estimates.
- The method assumes independence of scoring functions; if two scoring functions are correlated, dual-threshold filtering may not provide independent evidence.
- Percentile threshold choice (e.g., 90th vs. 75th) is somewhat arbitrary; sensitivity analysis across multiple percentiles is recommended but not always feasible.
- IOKR relies on MIBiG homology to assign molecular structures to BGCs, restricting its use to BGCs showing considerable homology to known BGCs.

## Evidence

- [supplementary] Calculate the 90th percentile threshold for standardised strain correlation scores and IOKR scores independently for each dataset.: "Calculate the 90th percentile threshold for standardised strain correlation scores and IOKR scores independently for each dataset."
- [supplementary] Partition links into four categories: above 90th percentile for standardised correlation only, above 90th percentile for IOKR only, above 90th percentile for both scores, and below 90th percentile for both.: "Partition links into four categories: above 90th percentile for standardised correlation only, above 90th percentile for IOKR only, above 90th percentile for both scores, and below 90th percentile"
- [supplementary] For each category, compute the proportion of validated links (number of validated links in category / total links in category).: "For each category, compute the proportion of validated links (number of validated links in category / total links in category)."
- [supplementary] Pool data across all three datasets and compute Fisher exact test p-values comparing the proportion of validated links in the dual-score (both scores ≥90th percentile) category to each single-score category.: "Pool data across all three datasets and compute Fisher exact test p-values comparing the proportion of validated links in the dual-score (both scores ≥90th percentile) category to each single-score"
- [results] Links scoring above the 90th percentile on both standardised strain correlation and IOKR scores are significantly enriched for validated links (p-value 2.633 × 10−4 from IOKR and 0.0208 from standardised strain correlation): "Links scoring above the 90th percentile on both standardised strain correlation and IOKR scores are significantly enriched for validated links (p-value 2.633 × 10−4 from IOKR and 0.0208 from"
- [results] Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links: "Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links"
- [results] To make the IOKR score comparable to the standardised correlation score, we can standardise it in a similar manner: "To make the IOKR score comparable to the standardised correlation score, we can standardise it in a similar manner"
