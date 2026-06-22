---
name: normalization-method-comparative-evaluation
description: Use when you have raw metabolomics intensity data affected by batch effects and signal drift, and need to select among multiple normalization approaches based on published comparative metrics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3391
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

# Comparative Evaluation of Metabolomics Normalization Methods

## Summary

This skill reproduces and validates published rankings of five normalization methods (tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC) across robustness and computational speed dimensions using the Metanorm R package on metabolomics datasets. It enables practitioners to verify which method best suits their experimental design and performance requirements.

## When to use

Apply this skill when you have raw metabolomics intensity data affected by batch effects and signal drift, and need to select among multiple normalization approaches based on published comparative metrics. Specifically useful when your experiment includes both QC (quality control) and biological samples run across multiple batches, and you want empirical evidence that a chosen method's robustness and speed rankings match those reported in peer-reviewed literature.

## When NOT to use

- When your metabolomics dataset does not include both QC and biological samples across multiple batches — the recommended Metanorm workflow depends on this structure.
- When you lack access to the published paper's reported metric values or parameters — reproduction requires grounding against the original evaluation.
- When your raw data is already normalized or preprocessed by an upstream pipeline — this skill is designed for raw (unnormalized) intensity matrices.

## Inputs

- rawdata: numerical matrix with compounds (rows) and samples (columns)
- batch: character vector assigning each sample to a batch identifier
- metanorm.qc (or equivalent type vector): character vector labeling each sample as 'QC' or other sample type (e.g., 'sample')
- published evaluation table: reported robustness and speed rankings from Analytical Chemistry article or bioRxiv preprint

## Outputs

- comparative ranking table: method × metric matrix (e.g., tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC ranked by robustness and execution time)
- robustness metric values: bias, variance, ground-truth recovery per method
- execution time (seconds or milliseconds) per method
- PCA score plots: pre- and post-normalization, colored by batch
- per-compound diagnostic plots: intensity vs. sample order before and after normalization
- QC discrepancy report: flagged samples where QC and biological samples show divergent normalization behavior

## How to apply

First, retrieve the published comparative evaluation from the Analytical Chemistry article and bioRxiv preprint, extracting reported metric values and rankings for robustness (e.g., bias, variance, recovery of ground truth) and execution time across the five methods. Install the Metanorm R package (version-compatible with R ≥ 4.4.0) and load the example metabolomics dataset(s) used in the paper's validation. Apply each of the five normalization methods with parameters specified in the article, using both QC and biological samples for normalization and enabling QCcheck=TRUE to verify QC representativeness. Compute robustness metrics and wall-clock execution time for each method. Generate a comparative ranking table and diagnostic plots (pre/post PCA score plots and per-compound intensity-vs.-order plots) and verify that reproduced rankings and metric ranges align with published findings within acceptable tolerance (typically ≤10% deviation for metric values unless otherwise specified in the article).

## Related tools

- **Metanorm** (R package implementing tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC normalization methods and comparative evaluation framework) — https://github.com/UGent-LIMET/Metanorm
- **R** (Runtime environment for executing Metanorm package functions, PCA visualization, and metric computation)

## Examples

```
library(metanorm); load(system.file("extdata", "example.RData", package = "metanorm")); normdat <- metanorm(rawdata[1:5,], model="tGAM", type=metanorm.qc, QCcheck=TRUE, batch=batch, plotdir="~/metanormExample/"); plotPCA(rawdata[1:5,], type=batch); plotPCA(normdat[1:5,], type=batch)
```

## Evaluation signals

- Reproduced robustness rankings (tGAM > rGAM, rLOESS > QC-RLSC, QC-RSC) match published order within tolerance.
- Reproduced execution times for each method fall within ±10% of published values or within the same speed tier (fast/moderate/slow).
- PCA score plots show visual reduction in batch clustering post-normalization, consistent with published pre/post visualizations.
- Per-compound intensity-vs.-order plots demonstrate removal of systematic signal drift for compounds that showed drift in raw data.
- QCcheck output flags or confirms QC representativeness; QC and biological samples show concordant normalization trajectories in diagnostic plots.

## Limitations

- Reproduction accuracy depends on exact parameter specification from the published article; deviations in model hyperparameters or data preprocessing can alter results.
- The example dataset provided by Metanorm may not reflect all experimental designs covered in the comparative study; results may vary on datasets with different QC/sample ratios, batch sizes, or compound characteristics.
- Execution time comparisons are platform- and load-dependent; reported timings are indicative and may differ across computational environments.
- Visual inspection of diagnostic plots (pre/post intensity plots) is subjective; the paper recommends manual examination of 'a decent number' of plots to judge normalization performance.

## Evidence

- [intro] five normalization methods (tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC): "implements three (new) robust normalization methods (tGAM, rGAM and rLOESS), alongside formerly proposed ones (QC-RLSC, QC-RSC)"
- [intro] tGAM superior robustness; rGAM and rLOESS faster: "tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster"
- [intro] use both QC and biological samples for normalization: "We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples"
- [readme] inputs: rawdata matrix, batch vector, metanorm.qc type vector: "rawdata, a numerical matrix containing the unnormalized data (rows = compounds, columns = samples); batch, a vector containing for each sample run the batch to which it belongs; metanorm.qc, a vector"
- [readme] metanorm function call with model, type, QCcheck, batch, plotdir parameters: "normdat <- metanorm(rawdata[1:5,], model = "tGAM", type = metanorm.qc, QCcheck = TRUE, batch = batch, plotdir = "~/Documents/metanormExample/")"
- [readme] diagnostic plots generated for per-compound assessment: "Individual compound pre- vs. post-normalization intensity vs. order plots can be retrieved from the plotdir directory. These allow finegrained assessment of normalization performance."
