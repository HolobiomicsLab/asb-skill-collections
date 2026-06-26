---
name: log-transformation-preprocessing
description: Use when apply log transformation when peak intensity distributions are
  right-skewed with heteroscedastic variance (intensity-dependent noise), particularly
  in QC-based batch correction workflows where variance stabilization improves the
  effectiveness of subsequent Pareto scaling normalization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzrtsim
  - bcpareto
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
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
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
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

# log-transformation-preprocessing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply optional logarithmic transformation to peak intensity vectors in LC/GC-MS metabolomics data to stabilize variance and improve normality before batch correction. This preprocessing step is toggled conditionally based on data characteristics and is typically paired with Pareto scaling for robust QC-based batch effect attenuation.

## When to use

Apply log transformation when peak intensity distributions are right-skewed with heteroscedastic variance (intensity-dependent noise), particularly in QC-based batch correction workflows where variance stabilization improves the effectiveness of subsequent Pareto scaling normalization. Use the log toggle parameter to enable transformation only when justified by data distribution analysis.

## When NOT to use

- Input contains zero or negative intensities without pseudocount addition (log undefined for x ≤ 0).
- Data is already on log scale or has been previously log-transformed (double transformation introduces bias).
- Intensity distribution is approximately normal or left-skewed; log transformation is unnecessary and may degrade statistical power.

## Inputs

- peak intensity matrix (features × samples, numeric)
- log_toggle parameter (Boolean: TRUE to apply log transformation, FALSE to skip)
- optional: QC sample indices for batch effect assessment

## Outputs

- log-transformed peak intensity matrix (same dimensions as input, if log_toggle=TRUE)
- original peak intensity matrix (if log_toggle=FALSE)

## How to apply

Load a peak intensity matrix (feature × sample) and determine whether log transformation is appropriate by inspecting the intensity distribution for right-skew and variance heterogeneity. If justified, apply the transformation with a log toggle parameter enabled in the bcpareto() function. The transformation is applied to the entire peak vector before Pareto scaling normalization, which divides each feature by the square root of its QC standard deviation. The log step precedes QC mean subtraction and Pareto division, ensuring that the subsequent normalization operates on log-scale intensities. Evaluate the result by checking that normalized intensities are approximately normally distributed and that batch effects (systematic intensity shifts across QC replicates) are attenuated without introducing artificial structure.

## Related tools

- **bcpareto** (QC-based batch correction method that accepts the log-transformed peak vector and applies Pareto scaling normalization) — https://github.com/yufree/mzrtsim
- **mzrtsim** (R package providing bcpareto() function and simulated LC/GC-MS feature tables for testing log-transformation and batch correction workflows) — https://github.com/yufree/mzrtsim
- **R** (Programming language environment for implementing log transformation and batch correction functions)

## Examples

```
# In R, load mzrtsim and apply log-transformed batch correction:
library(mzrtsim)
data(peakdata)
result <- bcpareto(peak = peakdata$intensity_matrix, qc_idx = peakdata$qc_samples, log = TRUE)
```

## Evaluation signals

- Log-transformed intensities are approximately normally distributed (Q-Q plot or Shapiro-Wilk p > 0.05 when applicable).
- Variance is homogeneous across the intensity range (Levene's test or visual inspection of residual plot after Pareto scaling).
- QC sample replicates cluster tightly in PCA or UMAP after log transformation and Pareto normalization, indicating batch effects have been attenuated.
- Batch-corrected feature intensities show no systematic relationship between intensity magnitude and residual batch effect (independence of variance and mean).
- Comparison of feature recovery or fold-change estimates with/without log transformation shows improved consistency with known biological differences when transformation is applied.

## Limitations

- Log transformation requires strictly positive intensities; zero values must be replaced with a pseudocount (e.g., half the detection limit) or the feature excluded.
- Log transformation is irreversible without reversing the exponential; downstream interpretation of feature abundances must account for this if back-transformation is desired.
- Over-transformation can occur if data are already moderately normal; unnecessary log transformation may suppress true subtle biological differences in low-abundance features.
- The choice to apply log transformation is user-specified via toggle parameter; no automated decision rule is provided, requiring domain expertise or exploratory data analysis.

## Evidence

- [other] Apply optional log transformation to the peak vector if the log toggle parameter is enabled.: "Apply optional log transformation to the peak vector if the log toggle parameter is enabled."
- [other] Normalize each feature by subtracting its QC mean and dividing by the square root of its QC standard deviation (Pareto scaling).: "Normalize each feature by subtracting its QC mean and dividing by the square root of its QC standard deviation (Pareto scaling)."
- [other] bcpareto() is a QC-based batch correction method that accepts a peak vector, QC sample vector, and a log toggle parameter to apply Pareto scaling normalization.: "bcpareto() is a QC-based batch correction method that accepts a peak vector, QC sample vector, and a log toggle parameter"
- [intro] Available methods: `bccenter`, `bcscaling`, `bcpareto`, `bcrange`, `bcvast`, `bclevel`.: "Available methods: `bccenter`, `bcscaling`, `bcpareto`, `bcrange`, `bcvast`, `bclevel`."
- [intro] `mzrtsim()` generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods.: "`mzrtsim()` generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods."
