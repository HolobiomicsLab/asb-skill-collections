---
name: peak-intensity-vector-transformation
description: Use when you have a peak intensity matrix from LC/GC-MS analysis with known QC sample indices and suspect batch-related systematic variation in feature intensities. Use it as a preprocessing step before downstream analysis (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzrtsim
  techniques:
  - GC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01213
  title: mzrtsim
evidence_spans:
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager") BiocManager::install("mzrtsim")
- github.com__yufree__mzrtsim
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrtsim_cq
    doi: 10.1021/acs.analchem.5c01213
    title: mzrtsim
  dedup_kept_from: coll_mzrtsim_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01213
  all_source_dois:
  - 10.1021/acs.analchem.5c01213
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-intensity-vector-transformation

## Summary

QC-based batch correction of LC/GC-MS peak intensity vectors using Pareto scaling normalization with optional log transformation. This skill attenuates batch effects by standardizing feature intensities relative to QC sample statistics.

## When to use

Apply this skill when you have a peak intensity matrix from LC/GC-MS analysis with known QC sample indices and suspect batch-related systematic variation in feature intensities. Use it as a preprocessing step before downstream analysis (e.g., statistical testing, biomarker discovery) to reduce technical noise while preserving biological signal.

## When NOT to use

- Input is a feature table already processed through different batch correction (e.g., ComBat, SVA) — combining methods may remove genuine signal.
- Fewer than 3 QC replicates available — QC statistics become unreliable.
- QC samples are not representative of biological samples or instrumental conditions — batch correction may amplify systematic differences rather than correct them.

## Inputs

- peak intensity matrix (features × samples, typically numeric data frame or matrix)
- QC sample indices or boolean vector identifying QC replicates
- log transformation toggle parameter (boolean)

## Outputs

- batch-corrected peak intensity matrix (same dimensions as input)
- optionally: QC mean and standard deviation values per feature for documentation

## How to apply

Load the peak intensity matrix (features × samples) and identify QC sample column indices. For each feature, calculate the mean and standard deviation across QC samples. Optionally apply log transformation to the entire peak vector if intensity values span multiple orders of magnitude or if heteroscedasticity is suspected. Normalize each feature by subtracting its QC mean and dividing by the square root of its QC standard deviation (Pareto scaling). This normalization leverages QC replicate variance to scale features according to their technical stability rather than absolute intensity, reducing the influence of high-abundance features that may not be more informative. Return the corrected peak vector with attenuated batch effects.

## Related tools

- **mzrtsim** (R package providing bcpareto() and other QC-based batch correction methods (bccenter, bcscaling, bcrange, bcvast, bclevel) for LC/GC-MS peak intensity normalization) — https://github.com/yufree/mzrtsim
- **R** (Statistical computing environment for implementing the bcpareto() method and matrix operations)

## Examples

```
bcpareto(peak_vector = feature_matrix, qc_vector = qc_indices, log = TRUE)
```

## Evaluation signals

- QC sample intensities cluster tightly after correction across the run; within-QC variance should decrease relative to between-biological-group variance.
- Pareto-scaled values approximate a standard normal distribution (mean ≈ 0, SD ≈ 1) for each feature when computed across all samples.
- Feature ranking (by effect size or fold-change in downstream analysis) changes minimally for robust signals but high-abundance technical artifacts are deprioritized.
- Corrected intensities remain non-negative if log transformation was not applied; log-transformed values span expected range without artificial truncation.
- Batch-related patterns visible in PCA or t-SNE plots before correction should be reduced after correction while biological grouping is preserved.

## Limitations

- Assumes QC samples are true technical replicates with no intentional biological variation — failure to meet this assumption leads to overcorrection.
- Pareto scaling may insufficiently correct extreme heteroscedasticity; range or VAST scaling may be preferable for highly skewed features.
- Log transformation can amplify noise in low-intensity features (near detection limit); consider filtering low-abundance features beforehand.
- Method is sensitive to outlier QC measurements; one erratic QC replicate inflates the standard deviation and weakens correction for that feature.
- Not designed to correct drift or nonlinear batch effects spanning the full run — ideally combine with run-order normalization or interpolation-based methods for longer LC/GC-MS experiments.

## Evidence

- [full_text] bcpareto() accepts a peak vector, QC sample vector, and log toggle parameter to apply Pareto scaling normalization: "bcpareto() is a QC-based batch correction method that accepts a peak vector, QC sample vector, and a log toggle parameter to apply Pareto scaling normalization"
- [full_text] Normalization by subtracting QC mean and dividing by square root of QC standard deviation: "Normalize each feature by subtracting its QC mean and dividing by the square root of its QC standard deviation (Pareto scaling)"
- [full_text] Calculate mean and standard deviation across QC samples for each feature: "Calculate mean and standard deviation of intensities for each feature across QC samples"
- [readme] Available QC-based batch correction methods in mzrtsim: "Available methods: `bccenter`, `bcscaling`, `bcpareto`, `bcrange`, `bcvast`, `bclevel`."
- [readme] Method corrects batch effects in LC/GC-MS peak intensity data: "Batch correction using QC-based methods including centering, scaling, Pareto scaling, range, VAST, and level normalization"
