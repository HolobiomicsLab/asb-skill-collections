---
name: robust-statistical-spread-quantification
description: Use when after drift correction of LC-MS peak intensity data, when you need to identify metabolic features with excessive internal spread (within-group variability in QC samples) or poor biological-to-technical reproducibility (QC-versus-sample spread).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - notame
  - R
  - Biobase
  - correct_drift
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package by Bioconductor'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# robust-statistical-spread-quantification

## Summary

Quantify the internal variability and reproducibility of LC-MS metabolic features using robust statistical metrics (RSD*, D-ratio) that are less sensitive to outliers than classical RSD, enabling reliable identification of low-quality features in non-targeted metabolomics data.

## When to use

After drift correction of LC-MS peak intensity data, when you need to identify metabolic features with excessive internal spread (within-group variability in QC samples) or poor biological-to-technical reproducibility (QC-versus-sample spread). Use robust metrics instead of classical RSD when the feature intensity distribution contains outliers or skewness that would inflate variance estimates.

## When NOT to use

- Input data has not undergone drift correction; apply correct_drift first
- No QC (quality control) samples are present in the dataset; D-ratio and RSD* require QC replicates
- Feature intensities have already been imputed or batch-corrected; apply flag_quality before imputation to avoid bias from imputed values

## Inputs

- drift-corrected MetaboSet object (Biobase ExpressionSet subclass)
- peak intensity matrix (exprs slot) with QC and biological samples
- feature metadata (fData) with sample annotations

## Outputs

- MetaboSet object with Flag column appended to fData
- Boolean Flag vector indicating low-quality features
- RSD, RSD*, and D-ratio values per feature (in fData)
- Quality metric distribution visualizations (histograms, scatter plots)

## How to apply

Apply the flag_quality function from notame with conservative thresholds (RSD 0.1, RSD* 0.1, D-ratio 0.1) on a drift-corrected MetaboSet object to compute three quality metrics per feature: (1) classic RSD—coefficient of variation in QC sample intensities; (2) RSD*—robust variant using median absolute deviation instead of standard deviation; (3) D-ratio—the ratio of QC-sample spread to biological-sample spread. Features exceeding any threshold are flagged in the Flag column of feature metadata (fData). Conservative thresholds (0.1) are stricter than recommended defaults (0.2 for RSD, 0.4 for D-ratio) and should be used when quality control is paramount. Inspect the resulting Flag column and visualize metric distributions (RSD, D-ratio, detection rate histograms) to assess the proportion of flagged features and confirm that flagging aligns with expected feature quality.

## Related tools

- **notame** (provides flag_quality function and MetaboSet container for storing features, intensities, and quality flags together) — https://github.com/hanhineva-lab/notame
- **Biobase** (ExpressionSet class upon which MetaboSet is built; provides exprs and fData slot infrastructure)
- **R** (runtime environment for executing flag_quality and statistical computations)
- **correct_drift** (upstream preprocessing step using cubic spline regression to remove systematic drift before quality flagging) — https://github.com/hanhineva-lab/notame

## Examples

```
# After drift correction; flag_quality computes RSD, RSD*, D-ratio and marks features
metaboset_flagged <- flag_quality(metaboset_driftcorrected, rsd_limit = 0.1, rsd_limit_loq = 0.1, dratio_limit = 0.1)
```

## Evaluation signals

- Flag column is present in fData with logical (TRUE/FALSE) values; at least one feature is flagged if data contains any features with metric violations
- Flagged features have RSD, RSD*, or D-ratio values ≥ the applied thresholds (0.1 in conservative case); unflagged features are strictly below thresholds
- Proportion of flagged features is reasonable relative to data quality context; typically <50% for well-controlled experiments, higher for noisy/complex batches
- RSD and RSD* values are positively correlated (both measure spread); D-ratio distribution is right-skewed (many features with low QC/bio spread ratio)
- Visual inspection of flagged vs. unflagged features in intensity plots or PCA shows flagged features as outliers or with high noise relative to signal

## Limitations

- Conservative thresholds (0.1) may over-flag features in exploratory studies or noisy datasets; recommended defaults (RSD 0.2, D-ratio 0.4) may be more appropriate for less stringent quality control
- RSD* and D-ratio are meaningless if QC sample replicates are absent or too few; minimum of 3–5 QC replicates per feature recommended for robust median-based estimates
- Quality flagging does not account for feature-specific biological relevance; a flagged low-abundance feature with poor reproducibility may still be biologically important
- The notame package API is experimental and breaking changes are possible, as noted in the repository README

## Evidence

- [other] flag_quality function description: "The flag_quality function flags features based on quality metrics using conservative limits of 0.1 for classic RSD, RSD*, and basic D-ratio"
- [other] recommended vs. conservative thresholds: "conservative limits of 0.1 for classic RSD, RSD* (robust version using median absolute deviation), and basic D-ratio (compared to recommended thresholds of 0.2 for RSD and 0.4 for D-ratio)"
- [other] RSD* and D-ratio definitions: "Apply flag_quality function with conservative limit of 0.1 for classic RSD, RSD* (robust version using median absolute deviation), and basic D-ratio to flag features where internal spread or"
- [other] workflow integration context: "Next, we apply drift correction with cubic spline regression. After drift correction, it is time to flag low-quality features"
- [readme] notame design and scope: "Identifying and flagging (or removing) low-quality molecular features using quality metrics defined by Broadhurst et al."
