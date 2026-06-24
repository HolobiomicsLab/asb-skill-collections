---
name: metabolomics-normalization-artifact-reproduction
description: Use when you have raw metabolomics intensity data (rows = compounds,
  columns = samples) with batch annotations and QC/biological sample labels, and you
  need to select among five normalization methods.
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

# metabolomics-normalization-artifact-reproduction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Reproduce the comparative evaluation of five normalization methods (tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC) from the Metanorm R package to verify reported robustness and computational speed rankings on metabolomics data. This skill validates whether a published normalization approach generalizes to your own metabolomics dataset by replicating the paper's comparative metrics and visual diagnostics.

## When to use

You have raw metabolomics intensity data (rows = compounds, columns = samples) with batch annotations and QC/biological sample labels, and you need to select among five normalization methods. Reproduction is warranted when the paper's robustness or speed claims are central to your method choice, or when you suspect batch effects or QC drift in your own data and want to verify that the published comparative rankings hold for your experimental design.

## When NOT to use

- Your data is already normalized or batch-corrected by another tool; reproduction would be redundant and risks compounding artifacts.
- You lack QC samples or reliable batch labels; the comparative evaluation depends on QC representativeness and batch structure.
- Your metabolomics platform or sample type (e.g., single-batch, no drift) differs fundamentally from the paper's (multi-batch LC–MS); rankings may not transfer and reproduction would not validate your use case.

## Inputs

- rawdata: numerical matrix (rows = compounds/metabolites, columns = samples); log-transformed intensity or abundance values
- batch: character vector assigning each sample column to a batch identifier
- metanorm.qc: character vector labeling each sample as 'QC' or 'sample' (other type)
- ground_truth_intensities (optional): reference or spike-in compound values to compute recovery metrics

## Outputs

- normdat_tGAM, normdat_rGAM, normdat_rLOESS, normdat_QCRLSC, normdat_QCRSC: five normalized data matrices (same shape as input)
- robustness_metrics_table: data frame with columns [method, mean_bias, variance, recovery_pct, exec_time_sec]
- diagnostic_plots: pre/post-normalization PC score plots (by batch) and per-compound intensity-vs.-order plots
- QCcheck_report: discrepancy flags between QC and biological sample distributions (if QCcheck=TRUE)

## How to apply

Install Metanorm (R ≥ 4.4.0) and load your unnormalized data matrix alongside batch and QC-type vectors. Run each of the five normalization methods (tGAM as default, then rGAM, rLOESS, QC-RLSC with QConly=TRUE, and QC-RSC) using the metanorm() function with QCcheck=TRUE to detect QC/biological sample discrepancies. Record execution time for each method. Extract or compute robustness metrics (bias, variance, recovery of ground truth) on a subset of compounds with known or spiked ground-truth intensities if available. Generate PC score plots before and after normalization (colored by batch) and inspect individual compound intensity-vs.-order diagnostic plots for each method to assess signal drift removal. Compare your reproduced rankings and metric ranges (e.g., mean absolute bias, residual variance) to the published table; acceptable tolerance is typically ±10–15% or visual consistency in batch effect attenuation.

## Related tools

- **Metanorm** (R package implementing the five normalization methods (tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC) and QC-check diagnostics; also provides plotPCA() for visual batch assessment and per-compound diagnostic plot generation.) — https://github.com/UGent-LIMET/Metanorm
- **R** (Runtime environment for installing Metanorm and executing normalization workflows, PCA plots, and metric calculations.)

## Examples

```
library(metanorm); load(system.file('extdata', 'example.RData', package = 'metanorm')); normdat <- metanorm(rawdata[1:5,], model='tGAM', type=metanorm.qc, QCcheck=TRUE, batch=batch, plotdir='~/metanormExample/'); plotPCA(rawdata[1:5,], type=batch); plotPCA(normdat, type=batch)
```

## Evaluation signals

- Reproduced robustness rankings (e.g., tGAM > rGAM ≥ rLOESS > QC-RLSC, QC-RSC in bias/variance) match published table within ±10–15% or visual consistency in ranking order.
- Computational execution time ranking (e.g., rGAM and rLOESS faster than tGAM) is consistent with published findings; absolute runtimes scale reasonably with dataset size.
- PC score plots before and after normalization show visible attenuation of batch clustering (tighter within-batch cohesion post-normalization).
- QCcheck=TRUE reports no systematic discrepancies between QC and biological sample distributions (or flags known outliers reproducibly).
- Individual compound intensity-vs.-order diagnostic plots reveal removal of drift trends and reduced residual signal variation post-normalization for majority of compounds tested.

## Limitations

- Reproduction is sensitive to input data preprocessing (log-transformation, scaling); if your data use different transforms than the paper's example dataset, metric ranges and visual appearance may shift.
- QC representativeness is assumed; if QC samples do not reflect the biological sample ionization/instrument state, QCcheck and QC-only methods may mislead.
- Ground-truth robustness metrics (bias, recovery) require spiked or reference compounds; if unavailable, visual inspection of diagnostic plots becomes the primary reproducibility signal.
- tGAM robustness gain over faster methods may diminish on single-batch datasets or datasets with minimal drift; the paper's multi-batch LC–MS setting is the primary validation context.

## Evidence

- [intro] tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster alternatives.: "tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster"
- [intro] The R package implements three new robust normalization methods (tGAM, rGAM, rLOESS) alongside formerly proposed methods (QC-RLSC, QC-RSC).: "implements three (new) robust normalization methods (tGAM, rGAM and rLOESS), alongside formerly proposed ones (QC-RLSC, QC-RSC)"
- [intro] Both QC and biological samples should be used for normalization, with metanorm checking for discrepancies between them.: "We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples"
- [readme] An example dataset contains a numerical matrix of unnormalized data (rows = compounds, columns = samples), batch vector, and QC-type vector.: "rawdata, a numerical matrix containing the unnormalized data (rows = compounds, columns = samples); batch, a vector containing for each sample run the batch to which it belongs; metanorm.qc, a vector"
- [readme] Individual compound pre- vs. post-normalization intensity vs. order plots are retrieved for finegrained assessment of normalization performance.: "Individual compound pre- vs. post-normalization intensity vs. order plots can be retrieved from the plotdir directory. These allow finegrained assessment of normalization performance."
- [readme] The metanorm function accepts a QCcheck parameter to detect discrepancies between QC and biological samples.: "QCcheck = TRUE,      # check whether QCs are representative"
