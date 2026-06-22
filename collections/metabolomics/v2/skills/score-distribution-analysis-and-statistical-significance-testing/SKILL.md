---
name: score-distribution-analysis-and-statistical-significance-testing
description: Use when after computing a scoring function over all possible genomic-metabolomic candidate pairs (e.g., all 2966 MIBiG-GNPS BGC-spectrum pairs), when you have a subset of known validated links and need to assess whether the scoring function ranks them significantly higher than expected by chance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0602
  tools:
  - GNPS
  - MIBiG
  - Chemistry Development Kit (CDK)
  - antiSMASH
  - NPLinker
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- we use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model
- To assign one or more molecular structures to BGCs, according to how many high-scoring matches are found in MIBiG
- Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit
- Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit [29]
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# score-distribution-analysis-and-statistical-significance-testing

## Summary

Analyze the distribution of link-scoring function outputs (e.g., IOKR, strain correlation) across all candidate pairs and compare validated links against the null distribution using statistical hypothesis tests to quantify enrichment. This skill determines whether a scoring function reliably separates true BGC-spectrum pairs from spurious matches.

## When to use

After computing a scoring function over all possible genomic-metabolomic candidate pairs (e.g., all 2966 MIBiG-GNPS BGC-spectrum pairs), when you have a subset of known validated links and need to assess whether the scoring function ranks them significantly higher than expected by chance. Apply this skill to decide whether a single scoring function is sufficiently discriminative, or whether multiple scores must be combined.

## When NOT to use

- No validated link ground truth is available; statistical tests require a known positive set to contrast against the null distribution.
- Scoring function output is categorical or ordinal rather than continuous numeric; choose rank-based or contingency-table tests instead.
- Sample size is very small (validated subset <5–10 pairs); statistical power will be insufficient and visual inspection alone may be more honest.

## Inputs

- Scoring function output (numeric scores) for all candidate pairs (e.g., 2966 BGC-spectrum pairs)
- Curated list of validated/true links (subset of the candidate pairs with known correct matches)
- Optionally, multiple scoring functions to be compared or combined

## Outputs

- Mean score and standard deviation for all pairs and validated subset
- P-value and test statistic quantifying enrichment of validated links
- Distribution histogram(s) with validated link positions overlaid
- Percentile-based enrichment table (e.g., proportion of validated links above the 90th percentile)
- Ranking metrics such as top-n accuracy and area-under-curve (AUC) relative to random baseline

## How to apply

Calculate the mean and standard deviation of the scoring function for all candidate pairs and separately for the known validated subset. Perform a two-sample statistical test (e.g., t-test or Mann-Whitney U, depending on normality) to compute a p-value quantifying whether validated links are enriched at higher scores. Construct histograms of the full score distribution and overlay the positions of validated links to visually confirm separation from the null distribution. Compute percentile ranks (e.g., what fraction of all pairs score above the 90th percentile?) and compare the proportion of validated links in the high-scoring tail. Report mean scores, p-values, and effect sizes (e.g., mean difference and 95% confidence intervals) alongside the visual distributions to support claims of enrichment.

## Related tools

- **NPLinker** (Framework providing candidate link enumeration and scoring functions (strain correlation, IOKR) whose distributions are analyzed) — https://github.com/sdrogers/nplinker
- **MIBiG** (Source of validated BGC-metabolite links used as ground truth for enrichment testing)
- **GNPS** (Source of mass spectrometry data paired with MIBiG entries to construct the evaluation dataset)

## Examples

```
import numpy as np; from scipy import stats; iokr_all = [0.0105] * 2966; iokr_val = [0.0364] * 50; t_stat, p_val = stats.ttest_ind(iokr_val, iokr_all); print(f'Mean (all): {np.mean(iokr_all):.4f}, Mean (validated): {np.mean(iokr_val):.4f}, p={p_val:.2e}')
```

## Evaluation signals

- Validated links show mean score significantly higher than all-pairs mean (p < 0.05), with effect size large enough to be actionable (e.g., mean difference ≥ 0.02 IOKR units or ≥ 3.5 standardized correlation units).
- Visual histogram confirms bimodal or right-skewed distribution with validated links concentrated in the upper tail, not randomly scattered across the distribution.
- Top-n accuracy (e.g., fraction of validated links in top 5, 10, 20 ranks) is substantially higher than random baseline (e.g., top-5 >0.17 vs. baseline 0.0014), and AUC > 0.65 vs. random AUC ≈ 0.52.
- Percentile enrichment analysis (e.g., proportion of validated links above 90th percentile) matches reported p-values; if 90th percentile p ≈ 2×10⁻¹¹, the enrichment should be visually obvious.
- Combined or standardized scoring function shows further improvement in both mean separation and AUC relative to individual scoring functions, confirming complementarity.

## Limitations

- P-values are sensitive to sample size; with large numbers of candidate pairs (e.g., 2966), even small effect sizes become statistically significant but may lack practical utility for ranking.
- Validated link set may be incomplete or biased toward certain product types or metabolite classes; the observed enrichment reflects only the ground truth available, not the true biological signal.
- Distribution analysis assumes independence of scores within the candidate set; if scores are correlated (e.g., due to shared spectral features), standard statistical tests may overestimate significance.
- High dependence on the choice of kernel function and molecular fingerprints used in scoring; optimizing these choices may substantially alter both the mean scores and the distribution shape.
- Reliance on MIBiG homology to assign candidate structures restricts applicability; BGCs with weak or no homology to MIBiG entries are excluded, potentially biasing the evaluation.

## Evidence

- [results] Finding: IOKR mean score comparison: "IOKR achieves a mean score of 0.0105 for all 2966 BGC-spectrum links and 0.0364 for validated links (p=1.7968 × 10−9)"
- [results] Standardised correlation mean score comparison: "Standardised correlation: -0.0060 (all), 3.6717 (validated), p-value 6.8302 × 10−64"
- [results] Top-n accuracy and AUC for IOKR: "Table 3 shows the top-n performance of IOKR: top-1: 0.1208, top-5: 0.1708, top-10: 0.1870, top-20: 0.2121, top-200: 0.2946; AUC: 0.6534"
- [results] Percentile enrichment analysis for validated links: "both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links"
- [results] Distribution evaluation method: "we selected to evaluate the standardised strain correlation score. To do this, we examine the distribution of scores for validated links in relation to the scores for all hypothetical links"
- [other] Visualization and statistical reporting: "Generate distribution histograms of IOKR scores for all 2966 pairs and overlay positions of validated links, reporting mean scores, p-values, and visual confirmation against reported S2 Fig and Table"
