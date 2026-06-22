---
name: robust-regression-gam-fitting
description: Use when metabolomics intensity data exhibits systematic signal drift across sample runs (especially within batches), QC samples are available to anchor normalization, and you require robustness against outlier compounds or aberrant sample intensities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# robust-regression-gam-fitting

## Summary

Fit robust generalized additive models (GAMs) to metabolomics intensity data across quality control (QC) and biological samples to normalize signal drift and batch effects while resisting outliers. tGAM is recommended for superior robustness in metabolomics normalization despite slower computation than faster alternatives like rGAM and rLOESS.

## When to use

Apply this skill when metabolomics intensity data exhibits systematic signal drift across sample runs (especially within batches), QC samples are available to anchor normalization, and you require robustness against outlier compounds or aberrant sample intensities. Use tGAM specifically when robustness is prioritized over computational speed; use rGAM or rLOESS if computational performance is critical and moderate robustness is acceptable.

## When NOT to use

- Input data are already batch-corrected or normalized using another method; applying robust GAM fitting may over-correct and introduce spurious patterns.
- No QC samples are available; robust GAM fitting relies on QC sample stability to anchor the normalization curve.
- Sample size is very small (< 10 samples per batch); GAM fitting may be unreliable with insufficient data to estimate smooth drift trends.

## Inputs

- Unnormalized metabolomics intensity matrix (numerical; rows = compounds, columns = samples)
- Batch assignment vector (one element per sample)
- Sample-type vector indicating QC vs. biological samples

## Outputs

- Normalized metabolomics intensity matrix (same dimensions as input)
- Diagnostic plots (intensity vs. run order, pre/post-normalization comparisons by compound)

## How to apply

Load raw metabolomics intensity data (rows = compounds/metabolites, columns = samples) and prepare metadata vectors indicating batch assignment and sample type (QC vs. biological). Install and load the Metanorm R package. Call the metanorm() function with the intensity matrix, specify model='tGAM', pass the sample-type vector to the 'type' argument, set QCcheck=TRUE to validate QC representativeness, and provide the batch vector. The function fits a robust GAM across both QC and biological samples within each batch, downweighting outlying observations to estimate smooth signal-drift curves. Extract normalized intensities from the returned object and inspect diagnostic plots (pre- vs. post-normalization intensity vs. order plots for individual compounds) to verify that drift has been removed without introducing artifact.

## Related tools

- **Metanorm** (R package implementing tGAM, rGAM, rLOESS, QC-RLSC, and QC-RSC normalization methods with robust GAM as core engine) — https://github.com/UGent-LIMET/Metanorm
- **R** (Execution environment (version >= 4.4.0 required); host for Metanorm and underlying GAM fitting libraries)

## Examples

```
library(metanorm); load(system.file('extdata', 'example.RData', package = 'metanorm')); normdat <- metanorm(rawdata[1:5,], model='tGAM', type=metanorm.qc, QCcheck=TRUE, batch=batch, plotdir='~/metanormResults/')
```

## Evaluation signals

- Diagnostic plots show substantially reduced signal drift across run order in biological samples post-normalization, without over-correction (i.e., QC intensity variance should remain low and stable).
- QC samples pre- and post-normalization maintain low within-batch coefficient of variation (CV); QCcheck=TRUE output confirms QCs are representative of the dataset.
- Principal component analysis (PCA) score plots labeled by batch show batch effects are diminished post-normalization; biological variance structure (if present) is preserved.
- Individual compound intensity-vs.-order plots show smooth, fitted drift curves that follow QC sample trajectories without fitting to sporadic biological sample outliers.
- Normalized data pass downstream statistical tests or biomarker discovery steps without inflated false-discovery rates, indicating no artificial patterns were introduced.

## Limitations

- tGAM computation is slower than rGAM and rLOESS alternatives; high-dimensional datasets (thousands of metabolites) may require extended runtime.
- Robust GAM fitting assumes drift is smooth and continuous within each batch; abrupt instrumental failures or rapid calibration shifts may not be fully captured.
- Requires both QC and biological samples; if QC samples are non-representative of the biological sample matrix (e.g., different ionization efficiency), normalization curves may not generalize optimally.
- Results are sensitive to batch assignment; incorrect or artificial batch boundaries may lead to spurious within-batch drift patterns.

## Evidence

- [readme] Metanorm implements three (new) robust normalization methods (tGAM, rGAM and rLOESS), alongside formerly proposed ones (QC-RLSC, QC-RSC). tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster.: "Metanorm implements three (new) robust normalization methods (tGAM, rGAM and rLOESS), alongside formerly proposed ones (QC-RLSC, QC-RSC). tGAM is recommended due to its superior robustness, but rGAM"
- [readme] We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples: "We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples"
- [other] Apply the tGAM normalization method using Metanorm's tGAM function, which fits a robust generalized additive model across QC and biological samples.: "Apply the tGAM normalization method using Metanorm's tGAM function, which fits a robust generalized additive model across QC and biological samples."
- [readme] Individual compound pre- vs. post-normalization intensity vs. order plots can be retrieved from the plotdir directory. These allow finegrained assessment of normalization performance. It is highly recommended to look at a decent number of these plots to judge normalization performance.: "Individual compound pre- vs. post-normalization intensity vs. order plots can be retrieved from the plotdir directory. These allow finegrained assessment of normalization performance."
- [other] tGAM is distinguished by superior robustness despite potentially slower computation than rGAM and rLOESS.: "tGAM distinguished by superior robustness despite potentially slower computation than rGAM and rLOESS."
