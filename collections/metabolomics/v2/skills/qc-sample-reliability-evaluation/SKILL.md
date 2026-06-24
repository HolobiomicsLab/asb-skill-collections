---
name: qc-sample-reliability-evaluation
description: Use when after drift correction has been applied to your LC-MS peak table
  and you need to identify low-quality metabolic features that exhibit high internal
  spread (RSD, RSD*) or excessive QC-versus-biological variation (D-ratio) before
  imputation and batch correction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - notame
  - R
  - Biobase
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package
  by Bioconductor'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_notame_cq
    doi: 10.3390/metabo10040135
    title: notame
  dedup_kept_from: coll_notame_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo10040135
  all_source_dois:
  - 10.3390/metabo10040135
  - 10.1093/bioinformatics/btr597
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# QC Sample Reliability Evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assess the reliability and quality of quality control (QC) samples in LC-MS metabolomics data by applying conservative thresholds to relative standard deviation (RSD), robust RSD*, and D-ratio metrics, then flag features that fail to meet reproducibility standards before downstream analysis.

## When to use

After drift correction has been applied to your LC-MS peak table and you need to identify low-quality metabolic features that exhibit high internal spread (RSD, RSD*) or excessive QC-versus-biological variation (D-ratio) before imputation and batch correction. Use this when QC samples are still present in the MetaboSet and you want to quantify feature reliability prior to their removal.

## When NOT to use

- QC samples have already been removed from the dataset—flag_quality requires QC replicates to compute RSD and D-ratio metrics.
- Drift correction has not yet been performed—drift-induced systematic shifts will artificially inflate RSD and invalidate quality assessment.
- Your LC-MS data has no replicate QC injections—the function requires multiple QC runs to calculate reproducibility statistics.

## Inputs

- MetaboSet object (Biobase ExpressionSet subclass) with drift-corrected intensity matrix in exprs slot
- fData feature annotation table with quality metric columns (RSD, RSD*, D-ratio)
- pData sample metadata distinguishing QC and biological samples

## Outputs

- MetaboSet object with Flag column added to fData, marking low-quality features with TRUE/FALSE or a flag code
- Quality metric summary table showing proportion of features flagged by each metric
- Visualization (histogram/density plot) of RSD, D-ratio, and detection rate distributions across all features

## How to apply

Load the drift-corrected MetaboSet object and apply the flag_quality function with conservative thresholds (RSD limit 0.1, RSD* limit 0.1, D-ratio limit 0.1) that are stricter than recommended defaults (RSD 0.2, D-ratio 0.4). The function evaluates RSD as the coefficient of variation of feature intensity across all QC injections, RSD* as the robust variant using median absolute deviation, and D-ratio as the ratio of between-group spread (QC vs. biological samples) to within-group spread. Features exceeding any of these thresholds are marked in the Flag column of the fData slot. Inspect the resulting Flag column to identify newly flagged features and cross-reference them against the distribution of quality metrics (RSD, D-ratio, detection rate) to assess what proportion of the feature set falls below your quality thresholds.

## Related tools

- **notame** (R package providing the flag_quality function and MetaboSet data structure for non-targeted LC-MS metabolomics preprocessing and quality control) — https://github.com/hanhineva-lab/notame
- **Biobase** (Bioconductor package providing the ExpressionSet class upon which MetaboSet is built, enabling consistent fData/pData/exprs slot access)
- **R** (Statistical computing language in which notame and the flag_quality function are implemented)

## Examples

```
mset_flagged <- flag_quality(mset_drift_corrected, rsd_limit = 0.1, rsd_star_limit = 0.1, d_ratio_limit = 0.1); fData(mset_flagged)$Flag
```

## Evaluation signals

- Flag column is present in fData with boolean or flag-code values for all features; no missing values in the Flag column.
- Flagged feature count and proportion match expectations based on the conservative thresholds (RSD 0.1, RSD* 0.1, D-ratio 0.1)—typically a higher proportion than recommended thresholds would flag.
- Quality metric distributions (RSD, D-ratio, detection rate histograms) show clear separation between flagged and unflagged populations, with flagged features concentrated at the high end of the metric range.
- Spot-check: manually verify 5–10 flagged features by examining their RSD, RSD*, and D-ratio values to confirm they exceed at least one threshold.
- Unflagged features should have RSD < 0.1 AND RSD* < 0.1 AND D-ratio < 0.1 (all three conditions must be satisfied to pass).

## Limitations

- Conservative thresholds (0.1 for all metrics) may be overly stringent for exploratory metabolomics; 30–50% of features may be flagged depending on data quality, potentially excluding true biology.
- D-ratio calculation assumes adequate separation between QC (technical replicates) and biological samples; poor experimental design or confounding variables will invalidate the metric.
- RSD and RSD* are sensitive to low-abundance features and features with missing values; imputation strategy applied post-flagging can alter the reliability assessment retroactively.
- The function does not account for feature-specific biological variability; a feature with high D-ratio may reflect genuine biological heterogeneity rather than poor QC performance.
- Recommended thresholds (RSD 0.2, D-ratio 0.4) are dataset- and platform-dependent; the choice of 0.1 should be justified by piloting or reference materials.

## Evidence

- [other] The flag_quality function flags features based on quality metrics using conservative limits of 0.1 for classic RSD, RSD*, and basic D-ratio (compared to recommended thresholds of 0.2 for RSD and 0.4 for D-ratio), producing a Flag column on the MetaboSet object to mark low-quality features.: "The flag_quality function flags features based on quality metrics using conservative limits of 0.1 for classic RSD, RSD*, and basic D-ratio (compared to recommended thresholds of 0.2 for RSD and 0.4"
- [other] Apply flag_quality function with conservative limit of 0.1 for classic RSD, RSD* (robust version using median absolute deviation), and basic D-ratio to flag features where internal spread or QC-versus-biological spread exceeds thresholds.: "Apply flag_quality function with conservative limit of 0.1 for classic RSD, RSD* (robust version using median absolute deviation), and basic D-ratio to flag features where internal spread or"
- [readme] Identifying and flagging (or removing) low-quality molecular features using quality metrics defined by Broadhurst et al.: "Identifying and flagging (or removing) low-quality molecular features using quality metrics"
- [readme] Drift correction: correcting for systematic drift in the intensity of molecular features using cubic spline correction: "After peak picking with the dedicated software, we use R for data preprocessing, quality control, statistical analysis and visualization"
- [other] flag_quality is used to flag features based on the other quality metrics: "flag_quality is used to flag features based on the other quality metrics"
