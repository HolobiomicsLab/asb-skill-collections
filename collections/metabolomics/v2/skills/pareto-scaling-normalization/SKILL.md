---
name: pareto-scaling-normalization
description: Use when you have peak intensity vectors from LC/GC-MS experiments with
  corresponding QC (quality control) sample measurements, and you need to correct
  for batch effects—especially when QC samples show systematic shifts in peak heights
  across analytical batches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
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

# pareto-scaling-normalization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Pareto scaling is a QC-based batch correction method for LC/GC-MS peak intensity data that normalizes each feature by subtracting its QC mean and dividing by the square root of its QC standard deviation, optionally after log transformation. It attenuates batch effects while preserving relative feature intensities.

## When to use

Apply this skill when you have peak intensity vectors from LC/GC-MS experiments with corresponding QC (quality control) sample measurements, and you need to correct for batch effects—especially when QC samples show systematic shifts in peak heights across analytical batches. The method is particularly useful when you want a gentler normalization than simple scaling but stronger variance stabilization than centering alone.

## When NOT to use

- Input is already a feature table with pre-corrected intensities—applying Pareto scaling twice risks over-correction.
- QC samples are absent or too sparse (fewer than 3 QC replicates per feature)—insufficient data for stable mean and SD estimation.
- Data contains negative or zero values and you plan to use log transformation—log of non-positive values is undefined.

## Inputs

- peak intensity matrix (numeric matrix, features × samples)
- QC sample indices (integer vector indicating which column indices are QC samples)
- log toggle parameter (boolean: apply log transformation before normalization)

## Outputs

- batch-corrected peak intensity matrix (same dimensions as input, numeric)
- QC mean vector per feature (numeric vector)
- QC standard deviation vector per feature (numeric vector)

## How to apply

Load a peak intensity matrix (features × samples) and identify QC sample indices within that matrix. Calculate the mean and standard deviation of each feature's intensity across only the QC samples. Optionally apply log transformation to the entire peak vector if the data has high dynamic range or multiplicative noise. For each feature, subtract its QC-derived mean and divide by the square root of its QC-derived standard deviation. This Pareto scaling step—using the square root rather than the full SD—provides a compromise between centering and full variance normalization, reducing the influence of highly variable features while retaining biological signal. Return the corrected peak vector with batch-induced systematic shifts removed.

## Related tools

- **mzrtsim** (Provides the bcpareto() function implementing Pareto-scaling batch correction; also generates simulated LC/GC-MS peak intensity data and QC samples for method benchmarking.) — https://github.com/yufree/mzrtsim
- **R** (Execution environment for bcpareto() and related QC-based normalization methods (bccenter, bcscaling, bcrange, bcvast, bclevel).)

## Examples

```
bcpareto(peak_vector, qc_indices, log = TRUE)
```

## Evaluation signals

- QC sample intensities post-correction should cluster tightly around zero mean with variance ≈ 1.0 (Pareto-scaled variance), indicating successful batch effect removal from reference samples.
- Biological replicates within the same treatment group should show reduced inter-sample coefficient of variation (CV) compared to pre-correction data, confirming batch correction efficacy.
- Feature intensity distributions should remain approximately symmetric (or match input skewness) after correction—gross skewing suggests over-correction or data quality issues.
- Pareto-scaled features should have reduced dynamic range (most values in [-3, +3]) compared to raw intensities, enabling better signal-to-noise ratio for downstream statistical tests.
- Cross-batch comparison (plotting feature intensity vs. batch ID) should show no systematic trend post-correction, confirming removal of batch-level offsets.

## Limitations

- Pareto scaling assumes QC sample composition is representative of all samples in the batch; if QC samples differ systematically from study samples (e.g., different matrix), correction may introduce bias.
- The method requires stable QC sample acquisition across all batches; missing or anomalous QC measurements in a batch will produce unreliable mean/SD estimates and compromise correction quality.
- Square-root scaling is a compromise between no scaling and full variance normalization; for highly skewed or heavy-tailed feature distributions, log transformation alone or robust quantile normalization may be preferable.
- Pareto scaling does not address within-sample (e.g., sample preparation, instrumental sensitivity) drift; it corrects batch-level systematic effects only.

## Evidence

- [other] bcpareto() is a QC-based batch correction method that accepts a peak vector, QC sample vector, and a log toggle parameter to apply Pareto scaling normalization for correcting batch effects in LC/GC-MS peak intensity data.: "bcpareto() is a QC-based batch correction method that accepts a peak vector, QC sample vector, and a log toggle parameter to apply Pareto scaling normalization"
- [other] Normalize each feature by subtracting its QC mean and dividing by the square root of its QC standard deviation (Pareto scaling).: "Normalize each feature by subtracting its QC mean and dividing by the square root of its QC standard deviation (Pareto scaling)."
- [readme] Available methods: `bccenter`, `bcscaling`, `bcpareto`, `bcrange`, `bcvast`, `bclevel`.: "Available methods: `bccenter`, `bcscaling`, `bcpareto`, `bcrange`, `bcvast`, `bclevel`."
- [other] Calculate mean and standard deviation of intensities for each feature across QC samples.: "Calculate mean and standard deviation of intensities for each feature across QC samples."
