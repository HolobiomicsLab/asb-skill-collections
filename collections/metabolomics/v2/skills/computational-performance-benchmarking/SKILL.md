---
name: computational-performance-benchmarking
description: Use when you have multiple candidate normalization methods for metabolomics data and need to choose one based on both statistical robustness and computational cost.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Metanorm
derived_from:
- doi: 10.1101/2025.09.30.679445v1
  title: Metanorm
- doi: 10.1021/acs.analchem.5c06841
  title: ''
evidence_spans:
- The R package implements three (new) robust normalization methods
- Metanorm supports robust metabolomics data normalization across scales and experimental designs
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

# computational-performance-benchmarking

## Summary

Systematically measure and rank competing normalization algorithms (tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC) on robustness metrics (bias, variance, ground-truth recovery) and execution time to guide method selection for metabolomics batch correction. This skill enables reproducible performance trade-off analysis across computational speed and statistical accuracy dimensions.

## When to use

You have multiple candidate normalization methods for metabolomics data and need to choose one based on both statistical robustness and computational cost. Trigger this skill when you have published comparative results to reproduce, or when you must evaluate methods on your own dataset and lack empirical performance rankings. Use it especially when data scale, batch structure, or QC sample availability varies—factors that influence both robustness and speed differently across methods.

## When NOT to use

- You have only one candidate method available and no need to choose between alternatives.
- Your dataset is already normalized or you only need to apply a single recommended method (e.g., tGAM only) without comparative evaluation.
- You lack access to the published paper's metric definitions, parameter settings, or ground truth, making reproduction impossible.

## Inputs

- rawdata: numerical matrix (rows = compounds, columns = samples)
- batch: vector indicating batch membership for each sample
- metanorm.qc: vector labeling each sample as 'QC' or non-QC type
- ground_truth (optional): reference intensities or known fold-changes for robustness metric calculation
- method parameters: tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC configurations from published paper

## Outputs

- robustness_metrics: table of bias, variance, ground-truth recovery for each method
- execution_times: vector or table of wall-clock runtime for each method
- ranking_table: comparative ranking of methods on robustness and speed dimensions
- diagnostic_plots: pre/post-normalization intensity-vs-order plots per compound, PCA score plots by batch, side-by-side comparisons
- reproducibility_report: alignment summary comparing reproduced vs. published metric ranges and rankings

## How to apply

First, retrieve the published comparative evaluation from the Analytical Chemistry article (DOI: 10.1021/acs.analchem.5c06841) or bioRxiv preprint to extract reported robustness and speed rankings for the five methods. Then, obtain the Metanorm R package and load the example metabolomics dataset (rawdata matrix, batch vector, QC/sample type indicator). Run each of the five normalization methods with paper-specified parameters on the same input data, computing robustness metrics (bias, variance, recovery of ground truth relative to unnormalized or synthetic ground truth) and wall-clock execution time for each compound or batch. Generate a comparative ranking table and visualization plots matching the published results' metric ranges. Finally, verify alignment of your reproduced rankings and metric values with published findings within acceptable tolerance (e.g., within 5–10% for speed, within method-dependent precision for robustness metrics). This workflow ensures your method selection is grounded in empirical evidence rather than theoretical claims.

## Related tools

- **Metanorm** (R package implementing tGAM, rGAM, rLOESS, QC-RLSC, and QC-RSC normalization methods; provides metanorm() function for batch-aware normalization and plotPCA() for diagnostic visualization) — https://github.com/UGent-LIMET/Metanorm
- **R** (Statistical environment required (version ≥ 4.4.0) for running Metanorm package, computing metrics, and generating plots) — https://cloud.r-project.org/index.html

## Examples

```
normdat_tgam <- metanorm(rawdata[1:5,], model='tGAM', type=metanorm.qc, QCcheck=TRUE, batch=batch, plotdir='~/metanormBench/'); normdat_qc <- metanorm(rawdata[1:5,], model='QC-RLSC', type=metanorm.qc, QConly=TRUE, batch=batch, plotdir='~/metanormBench2/'); # Compare execution times and visual diagnostics across methods
```

## Evaluation signals

- Reproduced robustness rankings (tGAM ranked highest, rGAM and rLOESS in middle tier, QC-RLSC/QC-RSC lower) align with published findings.
- Execution times for each method fall within ±10% of published values or overlap published time ranges when data scale matches.
- Bias, variance, and ground-truth recovery metrics for tGAM exceed or equal those of faster alternatives by statistically significant margins.
- PCA score plots show comparable batch effect reduction before/after normalization compared to published figures.
- Pre/post-normalization intensity-vs-order diagnostic plots for individual compounds show signal drift correction consistent with paper's visual examples.

## Limitations

- Reproducibility depends on exact parameter specification from the paper; deviations in normalization hyperparameters or QC sample definition will yield different rankings.
- Robustness metrics are sensitive to ground-truth definition; if synthetic or known ground truth is unavailable, only relative ranking is achievable.
- Execution times vary with hardware, R version, and system load; direct numeric comparison across platforms is unreliable—relative ordering is more stable.
- The example dataset in Metanorm may not reflect the statistical properties of your own data (batch sizes, QC density, signal range); method rankings may differ on significantly different data structures.
- QC sample representativeness and composition affect method performance; methods like QC-RLSC and QC-RSC require sufficient QC replicates to be effective—sparse or biased QCs can inflate their robustness metrics.

## Evidence

- [readme] tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster alternatives.: "tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster"
- [readme] The R package implements five normalization methods with explicit comparative evaluation of robustness and speed.: "implements three (new) robust normalization methods (tGAM, rGAM and rLOESS), alongside formerly proposed ones (QC-RLSC, QC-RSC)"
- [readme] Comparative evaluation published in peer-reviewed article with reported metric values and rankings.: "A detailed description and a comparative evaluation of Metanorm's capabilities are available here: Vynck, M., Vangeenderhuysen, P., De Paepe, E., Nawrot, T., Plekhova, V., Vanhaecke, L. (2026)."
- [readme] Diagnostic plots enable visual assessment of normalization performance across methods.: "Individual compound pre- vs. post-normalization intensity vs. order plots can be retrieved from the plotdir directory. These allow finegrained assessment of normalization performance."
- [other] Workflow step for extracting reported metric values and rankings from published paper.: "Extract the reported metric values and rankings for tGAM, rGAM, rLOESS, QC-RLSC, and QC-RSC across robustness and computational speed dimensions."
