---
name: qc-sample-integration-normalization
description: Use when normalizing multi-batch metabolomics intensity matrices where QC samples are available alongside biological samples, and when you need to detect whether QC samples are representative of the biological population (i.e., whether they follow the same systematic drift).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
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
---

# QC-Sample Integration for Robust Metabolomics Normalization

## Summary

Integrate both QC and biological samples into a unified normalization model to correct for batch effects and signal drift while detecting representativeness discrepancies. This approach leverages QC sample consistency as an anchor while allowing the normalization surface to fit across the full sample population, improving robustness over QC-only methods.

## When to use

Use this skill when normalizing multi-batch metabolomics intensity matrices where QC samples are available alongside biological samples, and when you need to detect whether QC samples are representative of the biological population (i.e., whether they follow the same systematic drift). Apply it especially when batch effects and signal drift are suspected across sample runs and you want a single unified normalization model rather than batch-specific corrections.

## When NOT to use

- Input lacks QC samples or QC labeling is unavailable — use QC-free or retention-time-only normalization instead.
- QC samples are severely unrepresentative of the biological population (detected via QCcheck flag) — investigate the root cause (instrument malfunction, QC reagent issue) before proceeding.
- Normalization goal is to correct only within-batch variation without accounting for inter-batch drift — batch-specific local regression (e.g., QC-RLSC with QConly=TRUE) may be more appropriate.

## Inputs

- Numerical intensity matrix (rows = metabolite features, columns = samples; typically log-transformed)
- Batch assignment vector (length = number of samples; e.g., c('batch1', 'batch1', ..., 'batch2', ...))
- QC indicator vector (length = number of samples; values in {'QC', 'sample'} or similar binary encoding)

## Outputs

- Corrected intensity matrix (same dimensions as input; normalized across batches)
- QC representativeness assessment (boolean flag or report indicating whether QC samples are representative)
- Diagnostic plots (intensity vs. sample order, pre/post PCA score plots, per-feature trend plots)

## How to apply

Prepare a raw intensity matrix (rows = metabolite features, columns = samples), a batch assignment vector, and a binary QC-indicator vector labeling each sample as 'QC' or 'sample'. Load both QC and biological samples into the normalization function (e.g., Metanorm's metanorm() with type = metanorm.qc argument). Set QCcheck = TRUE to enable automatic detection of QC/biological sample representativeness discrepancies (the function will flag if QCs deviate systematically from biological samples, signaling potential quality issues). Fit a robust generalized additive model (tGAM is the default) across all samples and batches simultaneously; this allows the smoother to learn the common drift pattern from QC consistency while also capturing any systematic differences in biological samples. Extract the corrected intensity matrix from the output object. Examine the pre- vs. post-normalization diagnostic plots (especially individual feature intensity-vs.-order plots) to verify that signal drift has been removed in both QC and biological samples, and confirm that QC samples remain consistent across the run.

## Related tools

- **Metanorm** (R package implementing tGAM, rGAM, rLOESS, QC-RLSC, and QC-RSC normalization methods; provides metanorm() function for unified QC+biological sample normalization with QCcheck and diagnostic plotting) — https://github.com/UGent-LIMET/Metanorm
- **R** (Host environment for Metanorm package; required version >= 4.4.0) — https://cloud.r-project.org/index.html

## Examples

```
library(metanorm); load(system.file('extdata', 'example.RData', package = 'metanorm')); normdat <- metanorm(rawdata[1:5,], model='tGAM', type=metanorm.qc, QCcheck=TRUE, batch=batch, plotdir='~/metanormExample/')
```

## Evaluation signals

- QCcheck = TRUE produces a representativeness assessment confirming QC and biological samples follow the same systematic drift (no flag/warning indicates successful integration)
- Diagnostic plots (pre- vs. post-normalization intensity-vs.-order) show removal of signal drift in both QC and biological sample groups, with QC samples remaining tightly clustered across the run
- PCA score plot before/after normalization shows batch clustering disappears or is substantially reduced while biological sample separation (if present) is preserved
- Normalized intensity ranges and summary statistics (mean, variance per feature) fall within published ranges from the original Metanorm evaluation paper (Vynck et al. 2026)
- Individual feature trends confirm that the fitted normalization surface is smooth and does not introduce artificial discontinuities at the QC/biological sample boundary

## Limitations

- Requires a minimum number of QC replicates per batch to estimate the drift surface reliably; sparse QC sampling may lead to over-fitting or poor generalization to biological samples.
- QCcheck assumes that QC and biological samples experience the same instrumental drift; if QC samples are run under different conditions (temperature, ionization mode, chromatographic flow), representativeness may be spuriously flagged.
- The choice between tGAM (slower, more robust) vs. rGAM/rLOESS (faster but potentially less robust) introduces a speed–robustness trade-off; very large feature matrices (>5000 features) may require rGAM or rLOESS for practical runtime.
- Normalization assumes a smoothly varying drift pattern across sample order; abrupt instrument failures or rapid drift changes may not be adequately captured by the generalized additive model.

## Evidence

- [intro] We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples.: "We further recommend using both QC as well as biological samples for normalization, and to have metanorm check for discrepancies between QC and biological samples"
- [intro] Metanorm implements three (new) robust normalization methods: tGAM, rGAM and rLOESS, alongside formerly proposed ones QC-RLSC, QC-RSC: "implements three (new) robust normalization methods (tGAM, rGAM and rLOESS), alongside formerly proposed ones (QC-RLSC, QC-RSC)"
- [intro] tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster alternatives.: "tGAM is recommended due to its superior robustness, but rGAM and rLOESS are faster"
- [readme] The example demonstrates the recommended approach of using both QC and biological samples with QCcheck enabled.: "The example usage below demonstrates this recommended approach."
- [readme] Normalize by setting type = metanorm.qc vector and QCcheck = TRUE to check representativeness.: "type = metanorm.qc,  # vector with sample types, i.e. "QC" and other sample types QCcheck = TRUE,      # check whether QCs are representative"
