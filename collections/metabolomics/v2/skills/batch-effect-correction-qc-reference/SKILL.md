---
name: batch-effect-correction-qc-reference
description: Use when your peak intensity matrix exhibits batch-to-batch variation (retention time drift, signal intensity fluctuation across injection sequences), you have QC samples injected at regular intervals throughout the analysis, and you want to preserve biological signal differences while removing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3673
  tools:
  - R
  - mzrtsim
  - BiocManager
  - SummarizedExperiment
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

# batch-effect-correction-qc-reference

## Summary

QC-based batch correction uses quality control (QC) sample intensities as a stable reference to normalize peak intensity vectors in LC/GC-MS data, attenuating systematic batch effects across runs. The bcpareto() implementation applies Pareto scaling (normalization by QC standard deviation) with optional log transformation to correct for instrument drift and matrix effects.

## When to use

Your peak intensity matrix exhibits batch-to-batch variation (retention time drift, signal intensity fluctuation across injection sequences), you have QC samples injected at regular intervals throughout the analysis, and you want to preserve biological signal differences while removing systematic instrumental artifacts before statistical analysis or normalization.

## When NOT to use

- Input is already a batch-corrected or pre-normalized feature table; re-correction may amplify variance.
- QC samples are absent or too few (n < 3) to reliably estimate mean and standard deviation per feature.
- Peak intensities contain negative values or zeros that are not biological; log transformation will fail or produce invalid results.

## Inputs

- peak intensity matrix (features × samples), numeric
- QC sample indices or boolean mask identifying QC replicates
- optional log transformation flag (boolean)

## Outputs

- corrected peak intensity matrix (same dimensions as input)
- batch-corrected feature table ready for downstream normalization or statistical analysis

## How to apply

Load the peak intensity matrix (features × samples) and identify QC sample indices within the run sequence. Calculate the mean and standard deviation of intensities for each feature across all QC samples. If using log transformation (recommended for data spanning multiple orders of magnitude), apply log2 or log10 to the peak vector first. For each feature, subtract the QC mean and divide by the square root of the QC standard deviation (Pareto scaling formula: (peak_intensity - QC_mean) / sqrt(QC_SD)). This scaling approach emphasizes features with high signal stability (low QC variance) while down-weighting noisy features. Return the corrected peak vector with the same dimensions as input. Evaluate correction success by confirming that QC sample cluster more tightly in downstream multivariate space (e.g., PCA) and that biological replicates show expected grouping patterns.

## Related tools

- **mzrtsim** (R package providing bcpareto() and related QC-based batch correction methods (bccenter, bcscaling, bcrange, bcvast, bclevel) for LC/GC-MS feature tables) — https://github.com/yufree/mzrtsim
- **R** (Runtime and statistical environment for executing batch correction workflows)
- **BiocManager** (Installation manager for Bioconductor-distributed packages like mzrtsim)
- **SummarizedExperiment** (Bioconductor container for storing corrected peak matrices alongside sample metadata and feature annotations)

## Examples

```
# Load peak data and QC indices
library(mzrtsim)
data(peakdata)  # hypothetical feature matrix
qc_idx <- c(1, 11, 21, 31)  # QC sample column indices
# Apply Pareto-scaling QC-based batch correction
corrected <- bcpareto(peakdata, qc_idx, log = TRUE)
```

## Evaluation signals

- QC sample replicates cluster tightly in PCA or t-SNE plots after correction, with within-QC variance reduced compared to before correction.
- Corrected feature table contains no NaN or Inf values; all intensities remain positive (if input was positive) and within expected dynamic range.
- Biological replicates and condition groups maintain or improve separation in multivariate space after QC correction, indicating biological signal is preserved.
- QC mean intensity per feature approaches zero after correction (within numerical precision), confirming successful centering by QC reference.
- Coefficient of variation (CV) among QC replicates for each feature decreases post-correction compared to raw intensities, validating variance reduction.

## Limitations

- Pareto scaling assumes QC standard deviation is a reliable proxy for feature noise; features with high intrinsic biological variance but low QC variance may be over-scaled.
- Log transformation is sensitive to zero or negative intensities; preprocessing must handle or remove non-positive peaks before correction.
- QC-based methods assume QC samples are representative of the overall sample matrix background and ion suppression; if QC composition differs markedly from samples, correction may be suboptimal.
- Method is sensitive to QC sample quality; contaminated or degraded QC replicates will produce biased reference statistics and poor correction.
- No changelog or versioning guidance provided in source repository; reproducibility may depend on pinning specific mzrtsim version.

## Evidence

- [other] bcpareto() is a QC-based batch correction method that accepts a peak vector, QC sample vector, and a log toggle parameter to apply Pareto scaling normalization for correcting batch effects in LC/GC-MS peak intensity data.: "bcpareto() is a QC-based batch correction method that accepts a peak vector, QC sample vector, and a log toggle parameter to apply Pareto scaling normalization for correcting batch effects in"
- [other] Calculate mean and standard deviation of intensities for each feature across QC samples. Apply optional log transformation to the peak vector if the log toggle parameter is enabled. Normalize each feature by subtracting its QC mean and dividing by the square root of its QC standard deviation (Pareto scaling).: "Calculate mean and standard deviation of intensities for each feature across QC samples. Apply optional log transformation to the peak vector if the log toggle parameter is enabled. Normalize each"
- [intro] Available methods: `bccenter`, `bcscaling`, `bcpareto`, `bcrange`, `bcvast`, `bclevel`.: "Available methods: `bccenter`, `bcscaling`, `bcpareto`, `bcrange`, `bcvast`, `bclevel`."
- [intro] `mzrtsim()` generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods.: "`mzrtsim()` generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods."
- [intro] For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`: "For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`"
