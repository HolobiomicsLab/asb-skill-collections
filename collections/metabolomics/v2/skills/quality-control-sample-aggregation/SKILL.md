---
name: quality-control-sample-aggregation
description: Use when you have a feature intensity matrix (peak vector) and a corresponding
  set of QC sample indices from a multi-batch LC/GC-MS experiment, and you need to
  establish batch-invariant reference statistics before applying QC-based batch correction
  methods such as bcpareto(), bccenter(), or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzrtsim
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c01213
  title: mzrtsim
evidence_spans:
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
  BiocManager::install("mzrtsim")
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# quality-control-sample-aggregation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Aggregate peak intensity vectors across QC (quality control) samples to compute mean and standard deviation statistics per feature, which serve as reference parameters for batch correction in LC/GC-MS metabolomics. This skill enables reproducible normalization by establishing QC-derived baseline intensity distributions.

## When to use

Apply this skill when you have a feature intensity matrix (peak vector) and a corresponding set of QC sample indices from a multi-batch LC/GC-MS experiment, and you need to establish batch-invariant reference statistics before applying QC-based batch correction methods such as bcpareto(), bccenter(), or bcscaling().

## When NOT to use

- Your experiment contains no QC replicates or lacks samples from a unified reference material.
- You have already applied batch correction; re-aggregating QC stats on corrected data will corrupt the reference baseline.
- Your QC samples show extreme outliers or instrument failures; diagnose and remove anomalous QC runs before aggregation to avoid skewed statistics.

## Inputs

- Peak intensity matrix (features × samples)
- QC sample indices (vector of column positions or logical mask identifying QC replicates)

## Outputs

- QC mean intensity vector (one value per feature)
- QC standard deviation vector (one value per feature)

## How to apply

Identify all QC sample indices in your peak intensity matrix. For each feature (row), calculate the mean intensity and standard deviation across only those QC samples. Store these two statistics (mean and SD) per feature; they define the QC baseline distribution. These aggregated statistics are then used as divisors or subtrahends in downstream Pareto scaling, centering, or other normalization workflows. The rationale is that QC samples—replicates of a reference material analyzed throughout the run—capture batch drift and instrumental variation independent of true biological effects; anchoring normalization to QC statistics isolates biological signal from technical noise.

## Related tools

- **mzrtsim** (Provides bcpareto(), bcscaling(), bccenter(), and related QC-based batch correction methods that consume QC aggregation outputs (mean and SD per feature) to normalize peak vectors.) — https://github.com/yufree/mzrtsim
- **R** (Language for computing mean() and sd() across QC sample subsets; used in mzrtsim batch correction pipeline.)

## Examples

```
qc_idx <- c(1, 5, 10, 15); qc_mean <- colMeans(peak_matrix[, qc_idx]); qc_sd <- apply(peak_matrix[, qc_idx], 2, sd)
```

## Evaluation signals

- QC mean and SD vectors have length equal to the number of features (rows) in the peak matrix.
- QC mean values are positive and lie within the observed range of intensities for each feature across all samples.
- QC SD values are non-negative and typically smaller than the corresponding QC means (coefficient of variation < 1 for well-behaved QC replicates).
- When QC statistics are applied to the QC samples themselves via downstream batch correction, the corrected QC intensities should cluster tightly near zero (after centering) or near 1 (after scaling), with low variance relative to biological samples.
- Recomputing QC statistics from the same QC indices yields identical results (reproducibility check).

## Limitations

- QC statistics are sensitive to outlier runs; a single failed QC injection or instrumental malfunction can inflate SD or bias the mean. Outlier detection and removal should precede aggregation.
- If QC replicates are too few (< 3), the SD estimate becomes unstable; at least 3–5 QC replicates per batch are recommended.
- QC aggregation assumes homogeneity across all QC samples; if different QC materials or matrix compositions are used, partition and aggregate separately.
- Features with near-zero or missing intensity in QC samples cannot be reliably normalized; Pareto scaling with QC SD ≈ 0 leads to division by near-zero or requires zero-handling logic.
- QC-based correction assumes batch effects are linear and additive; non-linear or multiplicative batch drift may not be fully corrected by mean/SD statistics alone.

## Evidence

- [other] Calculate mean and standard deviation of intensities for each feature across QC samples.: "Calculate mean and standard deviation of intensities for each feature across QC samples."
- [other] Normalize each feature by subtracting its QC mean and dividing by the square root of its QC standard deviation (Pareto scaling).: "Normalize each feature by subtracting its QC mean and dividing by the square root of its QC standard deviation (Pareto scaling)."
- [other] bcpareto() is a QC-based batch correction method that accepts a peak vector, QC sample vector, and a log toggle parameter to apply Pareto scaling normalization for correcting batch effects in LC/GC-MS peak intensity data.: "bcpareto() is a QC-based batch correction method that accepts a peak vector, QC sample vector, and a log toggle parameter to apply Pareto scaling normalization"
- [intro] Available methods: `bccenter`, `bcscaling`, `bcpareto`, `bcrange`, `bcvast`, `bclevel`.: "Available methods: `bccenter`, `bcscaling`, `bcpareto`, `bcrange`, `bcvast`, `bclevel`."
