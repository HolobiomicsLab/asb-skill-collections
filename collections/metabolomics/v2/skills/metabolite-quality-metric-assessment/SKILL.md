---
name: metabolite-quality-metric-assessment
description: Use when after drift correction has been applied to a MetaboSet object,
  and before imputation and batch correction.
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

# metabolite-quality-metric-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Flag low-quality molecular features in LC-MS metabolomics data by applying conservative thresholds to relative standard deviation (RSD), robust RSD* (median absolute deviation–based), and D-ratio (QC vs. biological variance ratio) metrics. This quality control step identifies features with excessive internal spread or inconsistent QC reproducibility that should be excluded from downstream statistical analysis.

## When to use

After drift correction has been applied to a MetaboSet object, and before imputation and batch correction. Apply this skill when you need to identify and mark features that fail reproducibility or detection thresholds—specifically when internal feature variability (RSD or RSD*) or the ratio of QC variance to biological variance (D-ratio) exceeds your experimental tolerance.

## When NOT to use

- Input has not undergone drift correction; apply correct_drift first to ensure systematic variation is removed before quality assessment.
- Data is already filtered or you have no QC replicates; D-ratio calculation requires intact QC samples to compute variance ratios.
- You are performing targeted metabolomics with a priori confidence in feature identity; quality flagging is designed for non-targeted discovery where feature annotations are uncertain.

## Inputs

- MetaboSet object (drift-corrected, with exprs intensity matrix and fData feature metadata)
- RSD threshold parameter (numeric; conservative value: 0.1)
- RSD* (robust RSD) threshold parameter (numeric; conservative value: 0.1)
- D-ratio threshold parameter (numeric; conservative value: 0.1)

## Outputs

- MetaboSet object with Flag column added/updated in fData indicating quality violations
- Boolean flag vector (TRUE = low-quality feature)
- Quality metric distributions (RSD, D-ratio, detection rate) for visualization

## How to apply

Use the notame `flag_quality` function on a drift-corrected MetaboSet object, specifying conservative limit thresholds (typically 0.1 for classic RSD, RSD*, and basic D-ratio, compared to the recommended defaults of 0.2 for RSD and 0.4 for D-ratio). The function evaluates each feature's internal spread using median absolute deviation–based RSD* for robustness and compares QC-to-biological variance via D-ratio. Features violating any threshold are marked in the Flag column of the object's feature metadata (fData). Inspect the resulting Flag column to identify newly flagged features, visualize the distribution of quality metrics (RSD, D-ratio, detection rate) across all features to assess the proportion flagged, and document the threshold decisions for reproducibility.

## Related tools

- **notame** (R package providing flag_quality function to apply quality-metric-based flagging on MetaboSet objects; bundles drift correction and quality control workflows for non-targeted LC-MS preprocessing) — https://github.com/hanhineva-lab/notame
- **Biobase** (Bioconductor package providing ExpressionSet class on which MetaboSet is built; enables storage and manipulation of feature metadata (fData) and expression matrices)
- **R** (Statistical computing environment for executing notame functions and quality metric calculations)

## Examples

```
flag_quality(metaboset_object, rsd_limit = 0.1, rsd_alt_limit = 0.1, d_ratio_limit = 0.1)
```

## Evaluation signals

- Flag column is present in fData of output MetaboSet with boolean or integer values (TRUE/1 for flagged, FALSE/0 for pass).
- Number of flagged features is consistent with expected proportion given threshold conservatism (0.1 thresholds are stricter than defaults, so expect higher flagging rates).
- Visualization of quality metric distributions shows bimodal or skewed patterns, with flagged features clustering in high-RSD or high-D-ratio tails.
- Feature count post-flagging is documented; sanity check that not all features are flagged (would indicate thresholds too stringent) and not zero features flagged (would indicate thresholds too lenient).
- Flagged features can be cross-referenced to known contaminants, instrument artifacts, or biological outliers to validate that flagging captured intended low-quality signals.

## Limitations

- RSD* (robust RSD using median absolute deviation) requires sufficient QC replicates; with very few QC samples, robust statistics may be unstable.
- D-ratio threshold selection (0.1 vs. 0.2 vs. 0.4) is application- and study-design-dependent; conservative thresholds may remove true biological signals if biological variance legitimately exceeds QC variance.
- Flagging is binary per feature; does not account for sample-wise or context-dependent quality variation—a feature may be flagged globally even if it is high-quality in a subset of samples.
- The notame package API is experimental and subject to breaking changes; threshold defaults and function signatures may shift between versions.

## Evidence

- [other] flag_quality with conservative thresholds (RSD 0.1, D-ratio 0.1): "Apply flag_quality function with conservative limit of 0.1 for classic RSD, RSD* (robust version using median absolute deviation), and basic D-ratio"
- [other] flag_quality marks features in Flag column: "producing a Flag column on the MetaboSet object to mark low-quality features"
- [other] Recommended thresholds for comparison: "compared to recommended thresholds of 0.2 for RSD and 0.4 for D-ratio"
- [other] D-ratio rationale: "flag features where internal spread or QC-versus-biological spread exceeds thresholds"
- [other] Quality metrics visualization: "Visualize quality metric distributions (RSD, D-ratio, detection rate) across all features to assess the proportion flagged"
- [readme] notame bundles preprocessing methods: "notame is a way to bundle together all the preprocessing methods we use for our non-targeted LC-MS metabolomics data"
- [readme] Identifying and flagging low-quality features: "Identifying and flagging (or removing) low-quality molecular features using quality metrics defined by Broadhurst et al."
