---
name: genomic-metabolomic-link-ranking
description: Use when you have paired genomic (BGCs clustered into GCFs via BiG-SCAPE) and metabolomic data (MS2 spectra grouped into MFs), with strain/sample co-occurrence patterns and predicted BGC–spectrum IOKR scores, and you need to prioritise which GCF–MF pairs are most likely to represent true natural.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3520
  tools:
  - NPLinker
  - BiG-SCAPE
  - IOKR
  - antiSMASH
  - GNPS
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them
- Finally, we present NPLinker, a software framework to link genomic and metabolomic data
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE clusters the BGCs separately by product type
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
---

# genomic-metabolomic-link-ranking

## Summary

Rank Gene Cluster Family (GCF) to Molecular Family (MF) links by combining standardised strain correlation and IOKR spectral-genomic scoring functions. This skill identifies true metabolite–biosynthetic gene cluster associations by leveraging complementary scoring signals that distinguish validated links from background.

## When to use

You have paired genomic (BGCs clustered into GCFs via BiG-SCAPE) and metabolomic data (MS2 spectra grouped into MFs), with strain/sample co-occurrence patterns and predicted BGC–spectrum IOKR scores, and you need to prioritise which GCF–MF pairs are most likely to represent true natural product links. Use this skill when a single scoring method leaves many potential links indistinguishable or when you want to exploit complementary signals (strain correlation vs. spectral similarity) to improve ranking accuracy.

## When NOT to use

- You lack paired genomic and metabolomic data or have not yet clustered BGCs into GCFs or spectra into MFs — this skill assumes both inputs are pre-processed and linked at the family level.
- Your IOKR scores are unavailable or unreliable because most BGCs in your dataset lack homology to reference BGCs in MIBiG — IOKR requires molecular fingerprints derived from homologous compounds, severely limiting its use to well-characterised product types.
- You require interpretability of which specific BGC–spectrum pairs drive high GCF–MF scores; this skill aggregates via max and thus obscures individual link contributions.

## Inputs

- BGC-to-GCF mapping (output from BiG-SCAPE clustering)
- Spectrum-to-MF mapping (MF grouping from metabolomic clustering)
- Predicted BGC–spectrum IOKR score table (σ_IOKR values for individual pairs)
- Strain/sample co-occurrence matrix (presence/absence vectors for GCFs and MFs)

## Outputs

- Ranked GCF–MF link table with columns: GCF_ID, MF_ID, raw_correlation_score, raw_IOKR_score, standardised_correlation_score, standardised_IOKR_score, combined_score (s_sum), rank
- High-confidence link subset (90th percentile filtering on both standardised scores)

## How to apply

First, compute or obtain raw strain correlation scores (e.g., Pearson correlation of strain presence/absence vectors for each GCF and MF pair) and raw IOKR scores (maximum σ_IOKR over all BGC–spectrum pairs within the GCF–MF). Standardise both scores independently using (s − E[s]) / SD[s] to place them on comparable scales and remedy the strain correlation score's inability to distinguish links with identical patterns. Combine the standardised scores using the ℓ₁ norm with sign preservation: s_sum = sgn(s_corr)|s_corr| + sgn(s_IOKR)|s_IOKR|. Rank all GCF–MF pairs by s_sum in descending order. Optionally, filter to links scoring above the 90th percentile on both individual scores to obtain a high-confidence subset enriched for validated links. Evaluate performance against known valid links using top-n accuracy (proportion of true links in top n ranks) and AUC.

## Related tools

- **BiG-SCAPE** (Clusters BGCs into Gene Cluster Families (GCFs) prior to scoring) — https://github.com/medema/BiG-SCAPE
- **IOKR** (Scores individual BGC–spectrum pairs by comparing molecular fingerprints derived from homologous BGCs to mass spectral features; output aggregated to GCF–MF level via max operator)
- **NPLinker** (Integration framework that implements the combined scoring function and link ranking workflow) — https://github.com/NPLinker/nplinker
- **antiSMASH** (Detects BGCs from microbial genomes upstream of BiG-SCAPE clustering) — https://github.com/antismash/antismash
- **GNPS** (Public MS2 spectral database; used as training data for IOKR model) — https://gnps.ucsd.edu/

## Examples

```
# Pseudocode from NPLinker workflow:
# 1. Load IOKR scores and GCF/MF mappings
# 2. For each GCF–MF pair, compute max IOKR
# 3. Compute strain correlation (Pearson) for each pair
# 4. Standardise both scores independently
# 5. Combine: s_sum = sgn(s_corr)|s_corr| + sgn(s_IOKR)|s_IOKR|
# 6. Rank by s_sum descending
# Example (conceptual):
from nplinker import NPLinkerProject
project = NPLinkerProject(config_file='config.yaml')
ranked_links = project.rank_links(method='combined', standardise=True, percentile_filter=90)
ranked_links.to_csv('ranked_gcf_mf_links.csv')
```

## Evaluation signals

- Standardised scores (both correlation and IOKR) should have approximately zero mean and unit variance across the full link set; standardisation is correctly applied if E[s_std] ≈ 0 and SD[s_std] ≈ 1.
- Validated links (known true associations) should have significantly higher combined scores (s_sum) than the full link set; test using a two-tailed t-test or Mann–Whitney U test (expect p < 0.05 and median s_sum for validated links > median for all links).
- Top-n accuracy should exceed random baseline (e.g. if 200 total links and 1 true link per spectrum, random top-1 accuracy ≈ 0; expect top-1 accuracy > 0.10 and AUC > 0.65).
- Links in the 90th percentile of both standardised scores should show significant enrichment of validated links compared to links exceeding either individual score alone (Fisher's exact test or chi-squared, p < 0.05).
- GCF–MF pairs should have exactly one max IOKR score value; verify no duplicate entries and that the number of output rows equals the number of GCF–MF pairs for which at least one (BGC, spectrum) pair exists in the input IOKR table.

## Limitations

- IOKR scoring relies on homology to MIBiG reference BGCs to assign molecular structures and fingerprints; this restricts its use to BGCs with considerable sequence homology and excludes novel or divergent biosynthetic pathways.
- Standardised strain correlation score, despite normalisation, still cannot distinguish between GCF–MF pairs exhibiting identical patterns of strain presence or absence, fundamentally limiting its discriminatory power for co-occurring but unrelated molecules.
- IOKR performance is highly dependent on kernel function and parameters (which determine substructure features in molecular fingerprints); the article notes these choices are not fully characterised, and performance may vary unpredictably across product types due to insufficient test set sizes for subtype-level validation.
- The max aggregation operator (σ_IOKR(G,M) = max σ_IOKR(m, g)) is sensitive to outlier high-scoring BGC–spectrum pairs and may inflate GCF–MF scores even when only a single spurious or weakly supported match exists.
- Combined scoring requires both strain data and IOKR scores; missing data for either modality prevents ranking, and sparse co-occurrence patterns can lead to uninformative or unstable correlation estimates.

## Evidence

- [results] Standardising the strain correlation score by subtracting mean and dividing by standard deviation: "Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links"
- [other] Computing maximum IOKR score over all BGC–spectrum pairs within a GCF–MF: "σ_IOKR(M, G) = max{σ_IOKR(m, g) : m ∈ M, g ∈ G}, where σ_IOKR scores individual BGC-spectrum links"
- [results] Combining standardised IOKR and correlation scores using ℓ₁ norm with sign function: "Our combined scoring function is therefore s_sum = sgn(s_corr)|s_corr| + sgn(s_IOKR)|s_IOKR|"
- [abstract] Complementary power of strain correlation and IOKR for ranking links: "we introduce a method for combining their scores into a single scoring function for genomic and metabolomic links, which shows improved performance over either of the individual approaches"
- [results] Filtering to high-percentile links improves validated link enrichment: "the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores (p-value of 2.633 × 10−4 and 0.0208"
- [discussion] IOKR relies on MIBiG homology, restricting scope: "A drawback of the current IOKR scoring method is its reliance on MIBiG homology to assign molecular structures to BGCs, which is needed to compute the molecular fingerprint. This restricts its use to"
- [discussion] Strain correlation inability to distinguish identical patterns: "standardising the strain correlation score still suffers from the drawback inherent in correlation-based scoring, of not being able to distinguish between potential links showing the same pattern of"
- [readme] NPLinker framework integration and repository: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
