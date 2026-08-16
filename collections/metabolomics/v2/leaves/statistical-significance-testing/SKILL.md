---
name: statistical-significance-testing
description: Use when when you have computed rank-based accuracy metrics (top-1, top-5,
  top-10 hit rates) for two or more competing methods on the same test dataset (e.g.,
  Orbitrap spectra), and need to determine whether performance differences are genuine
  rather than noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Anaconda
  - Git
  - Python scipy.stats
  - PyTorch
  - Git / GitHub
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.4c02426
  title: MSBERT
evidence_spans:
- '[Anaconda](https://www.anaconda.com) for Python 3.12'
- Install [Git](https://git-scm.com/downloads)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msbert_cq
    doi: 10.1021/acs.analchem.4c02426
    title: MSBERT
  dedup_kept_from: coll_msbert_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c02426
  all_source_dois:
  - 10.1021/acs.analchem.4c02426
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# statistical-significance-testing

## Summary

Quantitative comparison of library matching performance across multiple embedding methods (MSBERT, Spec2Vec, cosine similarity) using rank-based accuracy metrics and inferential statistics to confirm superior performance. This skill validates whether observed differences in top-k hit rates are statistically significant or attributable to random variation.

## When to use

When you have computed rank-based accuracy metrics (top-1, top-5, top-10 hit rates) for two or more competing methods on the same test dataset (e.g., Orbitrap spectra), and need to determine whether performance differences are genuine rather than noise. Apply this skill before reporting final comparative benchmarks in publications or deployment decisions.

## When NOT to use

- Test sets for different methods are not aligned (e.g., different subsets of spectra evaluated by each method) — use unpaired tests instead.
- Sample size is very small (n < 10 per-method) without prior justification — power analysis is needed first.
- Accuracy metrics have already been reported as point estimates without raw per-spectrum rankings — you cannot compute paired differences post-hoc.

## Inputs

- top-1, top-5, top-10 hit rate accuracies for method 1 (MSBERT) on test dataset
- top-1, top-5, top-10 hit rate accuracies for method 2 (Spec2Vec) on same test dataset
- top-1, top-5, top-10 hit rate accuracies for method 3 (cosine similarity baseline) on same test dataset
- test spectra count and reference library size metadata

## Outputs

- p-values for each pairwise method comparison at each top-k tier
- summary table with accuracy scores, p-values, and significance notation (e.g., *p<0.05, **p<0.01)
- conclusion statement confirming or rejecting superior performance of MSBERT over baselines

## How to apply

After computing top-1, top-5, and top-10 hit rate accuracies for MSBERT, Spec2Vec, and cosine-similarity baselines on the same test spectra and reference library, apply paired statistical tests (paired t-test or chi-squared test, depending on sample size and data distribution) to each accuracy tier. Use the paired test because the same test spectra are ranked by all three methods. Report both the accuracy scores and p-values in a summary table; conventionally, p < 0.05 indicates statistical significance. Document the test choice (parametric vs. non-parametric) and assumptions (e.g., sample size, normality if applicable).

## Related tools

- **Python scipy.stats** (Compute paired t-test and chi-squared test p-values; provides parametric and non-parametric significance testing.)
- **PyTorch** (Load pre-trained MSBERT model and compute embeddings for test spectra; necessary to generate accuracy metrics that feed into significance testing.) — https://pytorch.org/
- **Git / GitHub** (Version control and reproducibility; clone MSBERT repository and Spec2Vec baseline implementations to ensure all methods use the same test dataset.) — https://github.com/zhanghailiangcsu/MSBERT

## Examples

```
from scipy.stats import wilcoxon; import pandas as pd; msbert_acc = [0.7871, 0.8950, 0.9080]; spec2vec_acc = [0.7200, 0.8600, 0.8900]; stat, pval = wilcoxon(msbert_acc, spec2vec_acc); print(f'Paired Wilcoxon p-value: {pval:.4f}')
```

## Evaluation signals

- P-values are in the valid range [0, 1] and are computed for every top-k tier (top-1, top-5, top-10).
- For each pairwise comparison, p-value < 0.05 is reported alongside the corresponding accuracy difference (MSBERT score − baseline score), confirming direction of effect.
- Sample sizes and test type (paired t-test vs. chi-squared) are explicitly documented; paired test is used because same spectra are ranked by all methods.
- Summary table includes all six pairwise comparisons (MSBERT vs. Spec2Vec, MSBERT vs. cosine similarity, Spec2Vec vs. cosine similarity) at each top-k level, totaling ≥ 9 p-values.
- Results table is reproducible: given the same test spectra embeddings and ranked match lists, recomputing the test yields identical p-values within machine precision.

## Limitations

- Significance testing assumes independence between top-1, top-5, and top-10 metrics; multiple comparisons at different k values may inflate Type I error (false positives) without correction (e.g., Bonferroni).
- Paired t-test assumes normality of accuracy differences; with small sample sizes or non-normal distributions, non-parametric alternatives (e.g., Wilcoxon signed-rank test) are more robust.
- Statistical significance does not imply practical significance; a p < 0.05 improvement of 0.001 in top-1 accuracy may be statistically significant but operationally negligible.
- Test dataset characteristics (e.g., Orbitrap instrument, specific compound classes in GNPS) constrain generalizability; results may not hold for other mass spectrometry instruments or libraries.

## Evidence

- [other] Perform statistical significance testing (e.g., paired t-test or chi-squared) to confirm MSBERT outperforms both baselines.: "Perform statistical significance testing (e.g., paired t-test or chi-squared) to confirm MSBERT outperforms both baselines."
- [other] Calculate rank-based accuracy metrics (top-1, top-5, top-10 hit rates) for all three methods.: "Calculate rank-based accuracy metrics (top-1, top-5, top-10 hit rates) for all three methods."
- [other] Report accuracy scores and p-values in a summary table.: "Report accuracy scores and p-values in a summary table."
- [intro] MSBERT achieved top-1, top-5, and top-10 library matching scores of 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset, outperforming Spec2Vec and cosine similarity baselines.: "MSBERT achieved top-1, top-5, and top-10 library matching scores of 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset, outperforming Spec2Vec and cosine similarity baselines."
- [readme] The results are significantly better than Spec2Vec and cosine similarity.: "The results are significantly better than Spec2Vec and cosine similarity."
