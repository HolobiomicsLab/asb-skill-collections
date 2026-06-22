---
name: statistical-enrichment-analysis
description: Use when you have ranked GCF-MF (Gene Cluster Family–Molecular Family) links using two or more independent scoring functions and a set of experimentally validated links.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3473
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0091
  tools:
  - NPLinker
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
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

# statistical-enrichment-analysis

## Summary

Quantify whether a subset of genomic-metabolomic links scoring above defined percentile thresholds on complementary scoring functions (strain correlation, IOKR) shows significantly higher validation rates than links exceeding only individual scores. This determines whether multiple scoring approaches are genuinely complementary for prioritizing true links.

## When to use

You have ranked GCF-MF (Gene Cluster Family–Molecular Family) links using two or more independent scoring functions and a set of experimentally validated links. Apply this skill when you want to test whether links that simultaneously exceed high percentile thresholds on both scores are enriched for validation—i.e., whether combining scores recovers a higher proportion of true links than either score alone would suggest.

## When NOT to use

- You have only one scoring function available—enrichment analysis requires at least two independent scores to test complementarity.
- Your validated link set is very small (n < 20–30)—statistical power to detect enrichment may be insufficient, and Fisher's exact test assumes adequate contingency table cell counts.
- Links have already been filtered to a single high-confidence subset—you need the full distribution of scores to define meaningful percentile thresholds.

## Inputs

- GCF-MF link scores from at least two independent scoring methods (e.g., standardised strain correlation scores, IOKR scores)
- Set of experimentally validated GCF-MF pairs for each dataset
- Preprocessed link score matrix for all potential links across multiple datasets

## Outputs

- Contingency table showing link counts and validated link proportions for each score-threshold category
- Fisher's exact test p-values comparing dual-threshold category to single-threshold categories
- Summary statistics (proportion of validated links, 95% confidence intervals) for each category pooled across datasets

## How to apply

First, compute the 90th percentile threshold independently for each scoring function (e.g., standardised strain correlation and IOKR) within each dataset. Partition all links into four categories: (1) above 90th percentile for score A only, (2) above 90th percentile for score B only, (3) above 90th percentile for both, and (4) below 90th percentile for both. For each category, calculate the proportion of validated links (count of validated links in category / total links in category). Pool data across datasets and apply Fisher's exact test to compare the validation proportion in the dual-threshold category against each single-threshold category. Tabulate results showing proportions, counts, and p-values. Significance (p < 0.05) in the dual-threshold comparison indicates complementarity—the two scores are capturing different aspects of link quality.

## Related tools

- **NPLinker** (Framework for integrating and ranking genomic (antiSMASH/BiG-SCAPE) and metabolomic (GNPS) data; provides infrastructure for computing and combining link scores (strain correlation, IOKR)) — https://github.com/sdrogers/nplinker
- **antiSMASH** (Detects biosynthetic gene clusters (BGCs) from microbial genomes; output BGCs are clustered into GCFs that serve as input for link scoring)
- **BiG-SCAPE** (Clusters BGCs into Gene Cluster Families (GCFs) based on homology; GCFs are used as one side of the GCF-MF link pairs being scored and enriched)
- **GNPS** (Public metabolomics knowledge base; provides MS2 spectra and molecular families (MFs) that form the metabolomic side of GCF-MF pairs; also used to train IOKR scoring model)
- **MIBiG** (Reference database of characterized BGCs; used by IOKR to assign molecular structures to BGCs via homology, enabling molecular fingerprint computation for scoring)

## Evaluation signals

- Fisher's exact test p-value for the dual-threshold category is significantly lower (p < 0.05) than for single-threshold categories, indicating complementarity of the two scoring functions.
- Proportion of validated links in the dual-threshold category is substantially higher than in single-threshold or below-threshold categories (inspect effect size and confidence intervals).
- Contingency table cells contain adequate counts (typically ≥5–10 observations per cell) to satisfy Fisher's exact test assumptions; results remain consistent when pooling across multiple independent datasets.
- Validation enrichment pattern is consistent across all three datasets (Crüsemann, Gross, Leão) before and after pooling, indicating robustness and absence of dataset-specific artifacts.

## Limitations

- Correlation-based scoring (strain correlation) cannot distinguish between links with identical strain presence/absence patterns, even after standardisation, potentially masking true links or inflating false positives in low-diversity strain sets.
- IOKR scoring depends on MIBiG homology to assign molecular structures to BGCs; links for novel BGCs with low homology to characterized reference clusters cannot be scored, restricting method applicability.
- IOKR performance is highly sensitive to kernel function and parameter selection; choice is not fully characterized across different compound classes, leading to unpredictable scoring behaviour for underrepresented natural product types.
- Statistical power is limited if validated link sets are small (n < 20–30); contingency table sparsity can inflate p-values or lead to unstable estimates.

## Evidence

- [results] Links scoring above the 90th percentile on both standardised strain correlation and IOKR scores are significantly enriched for validated links (p-value 2.633 × 10−4 from IOKR and 0.0208 from standardised strain correlation), demonstrating complementarity of the two scoring approaches.: "the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores (p-value of 2.633 × 10−4 and 0.0208"
- [results] Partition links into four categories by score threshold; compute proportion of validated links per category; pool across datasets and apply Fisher exact test.: "Partition links into four categories: above 90th percentile for standardised correlation only, above 90th percentile for IOKR only, above 90th percentile for both scores, and below 90th percentile"
- [abstract] Using multiple link-scoring functions together makes it easier to prioritise true links relative to others.: "we demonstrate that using multiple link-scoring functions together makes it easier to prioritise true links relative to others"
- [results] Standardise scores independently before combining; strain correlation is standardised by subtracting dataset mean and dividing by standard deviation to make it comparable across links within a dataset.: "Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links"
- [discussion] Strain correlation still suffers from inability to distinguish between potential links with identical patterns of strain presence/absence.: "standardising the strain correlation score still suffers from the drawback inherent in correlation-based scoring, of not being able to distinguish between potential links showing the same pattern of"
- [discussion] IOKR relies on MIBiG homology to assign molecular structures, restricting use to BGCs with considerable homology.: "A drawback of the current IOKR scoring method is its reliance on MIBiG homology to assign molecular structures to BGCs, which is needed to compute the molecular fingerprint. This restricts its use to"
