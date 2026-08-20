---
name: r-package-workflow-implementation
description: Use when you have raw unnormalized metabolomics intensity data organized
  by batch and sample type (QC vs. biological), and you need to remove systematic
  variation (drift, batch effects) while preserving biological signal.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Metanorm
  - pak
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

# R Package Workflow Implementation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Implement a complete R package-based metabolomics data normalization workflow by loading raw intensity data, applying robust normalization methods (tGAM, rGAM, rLOESS, QC-RLSC, or QC-RSC), and validating batch effect removal through diagnostic plots and PCA. This skill demonstrates how to structure and execute a reproducible R package workflow for preprocessing large-scale metabolomics datasets.

## When to use

You have raw unnormalized metabolomics intensity data organized by batch and sample type (QC vs. biological), and you need to remove systematic variation (drift, batch effects) while preserving biological signal. Use this when your data matrix has compounds as rows, samples as columns, and you have accompanying vectors indicating batch assignment and QC sample status.

## When NOT to use

- Data are already normalized or batch-corrected by another method; applying sequential normalization may over-process and distort biological signal.
- You have no QC samples or sample type information; Metanorm requires explicit QC labeling to function and to validate robustness.
- Your data matrix has samples as rows and compounds as columns; Metanorm expects the transpose (compounds × samples).

## Inputs

- Raw metabolomics intensity matrix (numerical; rows=compounds, columns=samples)
- Batch assignment vector (character or factor; length=ncol(rawdata))
- Sample type vector (character; values include 'QC' and non-QC sample types)
- Optional: output directory path for diagnostic plots

## Outputs

- Normalized intensity matrix (same dimensions as input; rows=compounds, columns=samples)
- Diagnostic plots (individual compound pre-vs.-post intensity-vs.-order, PCA score plots)
- QC check report (if QCcheck=TRUE)

## How to apply

Install the Metanorm R package from GitHub (github.com/UGent-LIMET/Metanorm), load raw intensity data as a numerical matrix alongside batch and sample-type vectors. Choose a normalization model: tGAM is recommended for superior robustness despite slower computation; rGAM and rLOESS are faster alternatives. Always set QCcheck=TRUE to verify QC representativeness, and use both QC and biological samples for normalization by leaving QConly=FALSE (default). Call metanorm() with the raw data matrix, model choice, sample type vector, batch vector, and a plot directory for diagnostic output. Extract normalized intensities from the output and validate by generating PCA score plots before and after normalization, colored by batch—successful normalization should show batch clustering collapse. Examine individual compound intensity-vs.-order plots from the plotdir to confirm signal drift correction.

## Related tools

- **Metanorm** (R package implementing five robust normalization methods (tGAM, rGAM, rLOESS, QC-RLSC, QC-RSC) for metabolomics data across batches and scales) — https://github.com/UGent-LIMET/Metanorm
- **R** (Runtime environment for installing and executing Metanorm package (version ≥ 4.4.0 required)) — https://cloud.r-project.org/index.html
- **pak** (R package manager for installing Metanorm directly from GitHub repository)

## Examples

```
library(metanorm); load(system.file('extdata', 'example.RData', package = 'metanorm')); normdat <- metanorm(rawdata[1:5,], model='tGAM', type=metanorm.qc, QCcheck=TRUE, batch=batch, plotdir='~/metanormExample/'); plotPCA(normdat[1:5,], type=batch)
```

## Evaluation signals

- PCA score plot of normalized data shows no batch clustering when colored by batch assignment; batch effects visually disappear.
- Individual compound intensity-vs.-order plots in plotdir show flattened trend lines post-normalization (no systematic drift), whereas pre-normalization plots show clear upward or downward drift.
- QC check report (QCcheck=TRUE) confirms QC samples are representative and within expected tolerance; no discrepancies flagged between QC and biological sample distributions.
- Normalized intensity matrix dimensions match input (same rows and columns); no missing or NaN values introduced except where raw data had missing values.
- Comparison of normalization models (e.g., tGAM vs. QC-RLSC) on subset of compounds shows tGAM preserves biological signal better in diagnostic plots while achieving equal or better batch effect removal.

## Limitations

- tGAM is computationally slower than rGAM and rLOESS; for very large datasets (thousands of compounds), consider faster alternatives or subset testing first.
- Metanorm requires explicit QC sample labeling; if QCs are mislabeled or absent, normalization will fail or produce misleading results.
- Package has been extensively tested but use cases differ; unforeseen circumstances may cause unexpected behavior—GitHub issues or direct contact with authors ([redacted-email]) is recommended for troubleshooting.
- Robustness of normalization depends on adequate QC sample distribution across the run sequence; sparse or clustered QC samples may lead to poor model fitting.

## Evidence

- [readme] The R package implements three (new) robust normalization methods (tGAM, rGAM and rLOESS), alongside formerly proposed ones (QC-RLSC, QC-RSC).: "The R package implements three (new) robust normalization methods (tGAM, rGAM and rLOESS), alongside formerly proposed ones (QC-RLSC, QC-RSC)."
- [readme] tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster.: "tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster."
- [readme] We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples.: "We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples."
- [readme] The example dataset contains three objects: rawdata, a numerical matrix containing the unnormalized data (rows = compounds, columns = samples); batch, a vector containing for each sample run the batch to which it belongs; metanorm.qc, a vector containing for each sample run whether it is a QC or another type of sample.: "The example dataset contains three objects: rawdata, a numerical matrix containing the unnormalized data (rows = compounds, columns = samples); batch, a vector containing for each sample run the"
- [readme] It is highly recommended to look at a decent number of these plots to judge normalization performance.: "It is highly recommended to look at a decent number of these plots to judge normalization performance."
- [readme] Make sure R (version >= 4.4.0) is installed on your computer.: "Make sure R (version >= 4.4.0) is installed on your computer."
