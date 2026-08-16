---
name: metabolite-feature-distribution-comparison
description: Use when when metabolomics data contains both QC control samples and
  biological samples that will be normalized together using methods like tGAM, rGAM,
  rLOESS, QC-RLSC, or QC-RSC. Apply this skill to verify that QC and biological sample
  distributions remain consistent;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2945
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Metanorm
  license_tier: restricted
derived_from:
- doi: 10.1101/2025.09.30.679445v1
  title: Metanorm
- doi: 10.1021/acs.analchem.5c06841
  title: ''
evidence_spans:
- The R package implements three (new) robust normalization methods
- Metanorm supports robust metabolomics data normalization across scales and experimental
  designs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metanorm_cq
    doi: 10.1101/2025.09.30.679445v1
    title: Metanorm
  dedup_kept_from: coll_metanorm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.09.30.679445v1
  all_source_dois:
  - 10.1101/2025.09.30.679445v1
  - 10.1021/acs.analchem.5c06841
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-distribution-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compare distributional statistics (mean, variance, robust quantiles) of metabolic features between QC and biological sample subsets to identify discrepancies that may indicate normalization issues or sample batch effects. This skill is applied after sample partitioning and serves as a diagnostic checkpoint to ensure QC samples remain representative of biological samples during joint normalization.

## When to use

When metabolomics data contains both QC control samples and biological samples that will be normalized together using methods like tGAM, rGAM, rLOESS, QC-RLSC, or QC-RSC. Apply this skill to verify that QC and biological sample distributions remain consistent; discrepancies signal that QC samples may not be representative or that batch/instrumental drift has affected one group differently.

## When NOT to use

- Input data contains only QC samples or only biological samples (no comparison group exists).
- Normalization has not yet been applied—this skill is a post-normalization diagnostic, not a pre-processing filter.
- Sample type metadata is missing or unreliable; QC vs. biological classification must be accurate and complete.

## Inputs

- Normalized metabolomics data matrix (rows = metabolic features, columns = samples)
- Sample metadata vector indicating QC vs. biological sample classification for each column
- Batch assignment vector (one batch label per sample, optional but recommended)

## Outputs

- Discrepancy report table (CSV or data frame) with columns: feature ID, discrepancy metric value, statistical test result, affected sample count, batch(es)
- Summary statistics per feature per sample type (mean, variance, robust quantiles)
- List of flagged features exceeding discrepancy threshold

## How to apply

Partition normalized metabolomics data into two subsets: QC samples (identified via sample type vector) and biological samples (all non-QC samples). For each metabolic feature, compute distributional statistics independently within each subset—use mean and variance as primary summaries, with robust quantiles (e.g., median, IQR) as complements to reduce influence of outliers. Calculate discrepancy metrics between QC and biological distributions per feature; acceptable metrics include fold-change (QC mean / biological mean), effect size (Cohen's d or similar), or distance measures (e.g., Wasserstein distance, Kolmogorov-Smirnov statistic). Apply a statistical threshold (e.g., fold-change > 1.5, effect size > 0.8, or p-value < 0.05 from a two-sample test) to flag features with significant QC–biological discrepancies. Generate and review a tabular discrepancy report listing flagged features, their discrepancy metric values, affected samples, and batch assignments; features with large discrepancies warrant investigation of instrumental drift, batch effects, or QC sample contamination before proceeding with downstream analysis.

## Related tools

- **Metanorm** (R package implementing normalization methods (tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC) with built-in QC–biological sample discrepancy checking via QCcheck parameter) — https://github.com/UGent-LIMET/Metanorm
- **R** (Statistical computing environment for subset partitioning, distributional statistics computation, discrepancy metric calculation, and visualization)

## Examples

```
normdat <- metanorm(rawdata[1:5,], model = "tGAM", type = metanorm.qc, QCcheck = TRUE, batch = batch, plotdir = "~/Documents/metanormExample/")
```

## Evaluation signals

- Discrepancy report contains no missing values; all features have discrepancy metrics and sample counts populated.
- Flagged features are reproducible across independent runs of the same data and threshold; rank order of discrepancy values is stable.
- QC and biological sample subset sizes match expected counts (sum of QC rows + sum of biological rows = total sample count).
- Fold-change, effect size, or p-value distributions are internally consistent (e.g., features with large fold-changes also show large effect sizes).
- Visual inspection of intensity-vs-order plots for flagged features reveals visible drift, batch jumps, or distributional shifts between QC and biological samples that justify flagging.

## Limitations

- Discrepancy detection assumes QC samples and biological samples are drawn from comparable populations; if QC samples are intentionally spiked, enriched, or chemically distinct, systematic differences are expected and do not indicate a problem.
- Thresholds for fold-change, effect size, or p-value are heuristic and should be calibrated per metabolomics platform and study design; no universal cutoff is recommended by the source article.
- Small sample sizes (e.g., <3 QC or <3 biological samples) yield unreliable variance estimates and statistical tests; robust quantiles are preferable in such cases.
- The skill detects distributional discrepancies but does not identify root causes (instrumental drift, contamination, batch effects, or biological heterogeneity); manual inspection of pre- vs. post-normalization diagnostic plots is required to interpret findings.

## Evidence

- [other] Partition dataset into QC and biological subset; compute statistics per feature per subset; calculate discrepancy metrics; apply threshold; generate report: "Partition the dataset into QC sample subset and biological sample subset. 3. Compute distributional statistics (mean, variance, or robust quantiles) for each metabolic feature within each subset. 4."
- [intro] Joint normalization with QC check is recommended; discrepancies between QC and biological samples indicate normalization issues: "We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples"
- [readme] QCcheck parameter in Metanorm enables discrepancy detection during normalization workflow: "QCcheck = TRUE,      # check whether QCs are representative"
- [readme] Diagnostic plots are essential for interpreting discrepancies and assessing normalization performance: "Individual compound pre- vs. post-normalization intensity vs. order plots can be retrieved from the *plotdir* directory. These allow finegrained assessment of normalization performance. It is highly"
