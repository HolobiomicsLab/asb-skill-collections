---
name: robustness-metric-computation-metabolomics
description: Use when when you have applied multiple normalization methods (e.g.,
  tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC) to metabolomics datasets and need to rank them
  by robustness and execution speed to determine which method is most suitable for
  your experimental design and computational constraints.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Metanorm
  license_tier: restricted
  provenance_tier: literature
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

# robustness-metric-computation-metabolomics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute and compare robustness metrics (bias, variance, recovery of ground truth) and computational speed across multiple normalization methods applied to metabolomics data. This skill enables quantitative evaluation of normalization method performance for reproducibility assessment and method recommendation.

## When to use

When you have applied multiple normalization methods (e.g., tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC) to metabolomics datasets and need to rank them by robustness and execution speed to determine which method is most suitable for your experimental design and computational constraints.

## When NOT to use

- Input data lacks batch structure or QC sample replicates — robustness metrics require within-batch and cross-batch variation to be meaningful.
- No ground truth reference is available and the biological sample set is too small to estimate true signal reliably — bias and recovery metrics will be unreliable.
- Only one normalization method has been applied — comparative ranking requires at least two methods to be evaluated side-by-side.

## Inputs

- Unnormalized metabolomics intensity matrix (rows = compounds, columns = samples)
- Batch assignment vector (one value per sample)
- Sample type vector indicating QC vs. biological samples
- Ground truth or spike-in reference values (optional but recommended for bias/recovery calculation)

## Outputs

- Robustness metrics table (columns = methods; rows = bias, variance, recovery %; units specified)
- Execution time vector (one value per method, in seconds or milliseconds)
- Comparative ranking plots (e.g., box plots of bias/variance by method, scatter of speed vs. robustness)
- Ranked method list (sorted by robustness score or by user-specified priority order)

## How to apply

Run each normalization method on a standardized metabolomics dataset with known ground truth or spike-in controls, recording both the normalized intensity matrix and execution time. Calculate bias as deviation from ground truth (e.g., mean relative error), variance as stability across replicates or batches, and recovery rate as the percentage of true signal retained. Normalize metrics to a common scale (e.g., 0–100 or standardized units) and generate a comparative ranking table and visualization (e.g., box plots or radar charts) matching the published paper's comparative evaluation structure. Verify that reproduced metric ranges and rankings align with the paper's reported findings within acceptable tolerance (typically ±10% relative difference for bias and variance, ±5% for execution time).

## Related tools

- **Metanorm** (R package implementing five normalization methods (tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC) on which robustness metrics are computed) — https://github.com/UGent-LIMET/Metanorm
- **R** (Statistical environment for running Metanorm, computing robustness metrics (bias, variance, recovery), and generating comparative visualizations)

## Examples

```
normdat_tGAM <- metanorm(rawdata[1:5,], model="tGAM", type=metanorm.qc, QCcheck=TRUE, batch=batch); normdat_QC <- metanorm(rawdata[1:5,], model="QC-RLSC", type=metanorm.qc, QConly=TRUE, batch=batch); # Then compute bias, variance, and execution times, and compare rankings.
```

## Evaluation signals

- Reproduced metric values (bias, variance, recovery %) for each method fall within ±10% relative difference of the published paper's reported ranges.
- Ranking order of methods by robustness matches the paper's findings (e.g., tGAM ranked highest for robustness, rGAM and rLOESS ranked higher for speed).
- Execution time measurements are internally consistent across repeated runs and scale reasonably with dataset size (compound count and sample count).
- Comparative visualization (plots and tables) shows clear separation between methods on at least one robustness or speed dimension, demonstrating discriminative power.
- QC vs. biological sample discrepancy checks (if applicable) flag or report any samples with unexpected normalization behavior, confirming method reliability assessment.

## Limitations

- Robustness metrics depend critically on the representativeness and abundance of QC samples; sparse or biased QC sampling may yield unreliable comparisons.
- Ground truth recovery cannot be computed without spike-in controls or independent reference measurements; bias and recovery estimates will be approximate if based on replicate variance alone.
- Execution speed is platform- and dataset-dependent; reported timings may not generalize to smaller or larger metabolomics cohorts or different computational hardware.
- The paper recommends using both QC and biological samples for normalization, but only QC-only methods (e.g., QC-RLSC with QConly=TRUE) may show different robustness profiles; ensure parameter consistency across comparisons.

## Evidence

- [other] Comparative evaluation workflow: "Compute robustness metrics (e.g., bias, variance, recovery of ground truth) and execution time for each method."
- [readme] Five methods evaluated: "The R package implements three (new) robust normalization methods (tGAM, rGAM and rLOESS), alongside formerly proposed ones (QC-RLSC, QC-RSC)."
- [readme] Recommended method ranking by robustness: "tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster."
- [other] Ranking verification criterion: "Verify that reproduced rankings and metric ranges align with published findings within acceptable tolerance."
- [readme] QC and biological sample recommendation: "We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples."
