---
name: time-series-intensity-normalization
description: Use when when LCMS metabolomics abundance tables show systematic intensity drift across the injection sequence (e.g., instrument signal decay or gain over hours), and you have pooled technical replicate injections and/or internal standard compounds distributed throughout the run.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - bmxp
  - Python
  - Blueshift
  - bmxp (Python package)
derived_from:
- doi: 10.1093/bioinformatics/btaf290/8128335
  title: Eclipse
evidence_spans:
- pip install bmxp
- They are written in Python and C
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eclipse_cq
    doi: 10.1093/bioinformatics/btaf290/8128335
    title: Eclipse
  dedup_kept_from: coll_eclipse_cq
schema_version: 0.2.0
---

# time-series-intensity-normalization

## Summary

Correct systematic drift in LCMS metabolomics feature intensities across a run by fitting a drift model to pooled technical replicate signals and applying the correction to all features. This removes time-dependent instrumental variation while preserving biological signal.

## When to use

When LCMS metabolomics abundance tables show systematic intensity drift across the injection sequence (e.g., instrument signal decay or gain over hours), and you have pooled technical replicate injections and/or internal standard compounds distributed throughout the run. Drift correction should be applied before feature clustering, alignment, or statistical analysis to prevent run-order effects from confounding downstream results.

## When NOT to use

- Injection metadata does not identify pooled technical replicates or internal standard compounds; the model cannot be fitted without reference signals.
- The dataset contains only a single injection or batch with no temporal variation; drift correction is unnecessary.
- Feature abundances are already normalized or previously drift-corrected; reapplying may introduce double-correction artifacts.

## Inputs

- Feature abundance table (pivot: Compound_ID × injection_id)
- Feature metadata (bmxp.FMDATA: Compound_ID, RT, MZ, Intensity, Method)
- Injection metadata (bmxp.IMDATA: injection_id, injection_type, injection_order, broad_id)
- Sample metadata (bmxp.SMDATA: broad_id and biospecimen labels)

## Outputs

- Drift-corrected feature abundance table (same dimensions as input)
- Updated injection metadata with QCRole field (QC-drift_correction, QC-pooled_ref, QC-not_used, sample)
- Batches Skipped field in feature metadata (batches lacking sufficient pooled technical replicates)

## How to apply

Load the raw abundance table (Compound_ID × injection_id pivot table) and injection metadata identifying pooled technical replicates and internal standard compounds. Extract the abundance signals for pooled technical replicates across all samples to establish a reference signal trajectory as a function of sample run order or acquisition time. Fit a drift correction model (e.g., polynomial or LOWESS regression) to these replicate signals. Apply the fitted model to all features by normalizing each feature's intensity at each injection by the estimated drift magnitude at that timepoint. Output the drift-corrected abundance table with identical dimensions to the input. Verify that drift-corrected pooled replicates cluster tightly in downstream analyses and that the magnitude of correction is consistent across features.

## Related tools

- **Blueshift** (Standalone BMXP module that performs drift correction on LCMS datasets via pooled technical replicates and internal standards) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/blueshift/readme.md
- **bmxp (Python package)** (Provides shared schema (FMDATA, IMDATA, SMDATA) and DriftCorrection class for applying time-series intensity normalization) — https://github.com/broadinstitute/bmxp

## Examples

```
from bmxp.blueshift import DriftCorrection; dc = DriftCorrection(); corrected_abund = dc.correct(raw_abundance_table, feature_metadata, injection_metadata)
```

## Evaluation signals

- Pooled technical replicate injections show reduced coefficient of variation (CV) in their corrected abundances across the run compared to raw abundances.
- Drift-corrected feature abundances do not correlate with injection_order or acquisition time when tested across the full dataset.
- The QCRole field in injection metadata correctly assigns pooled replicates to 'QC-pooled_ref' or 'QC-drift_correction' roles and samples to 'sample'.
- Batches with insufficient pooled technical replicates are flagged in Batches Skipped field and excluded from correction.
- The corrected abundance table maintains the same dimensions, feature indices, and injection indices as the input; no features or samples are dropped.

## Limitations

- Drift correction requires pooled technical replicates or internal standards to be present and labeled in injection metadata; datasets lacking these reference materials cannot be corrected.
- The fitted drift model assumes monotonic or smooth, slowly-varying drift (polynomial or LOWESS); abrupt instrumental failures or column blockages may violate this assumption.
- Batches without sufficient pooled technical replicates are skipped entirely, leaving those features uncorrected and flagged in metadata.
- The correction is applied uniformly across all features; compound-specific drift signatures (e.g., adduct-dependent or ionization-state-dependent drift) are not modeled.
- Correction depends on the choice of drift model (polynomial degree, LOWESS bandwidth); model misspecification can over- or under-correct and introduce artifacts.

## Evidence

- [other] Blueshift is a standalone module designed to perform drift correction on LCMS datasets via pooled technical replicates and internal standards.: "Blueshift is a standalone module designed to perform drift correction on LCMS datasets via pooled technical replicates and internal standards."
- [other] Extract the abundance signals for pooled technical replicates across all samples to establish a reference signal trajectory.: "Extract the abundance signals for pooled technical replicates across all samples to establish a reference signal trajectory."
- [other] Fit a drift correction model (e.g., polynomial or LOWESS) to the technical replicate signals as a function of sample run order or time.: "Fit a drift correction model (e.g., polynomial or LOWESS) to the technical replicate signals as a function of sample run order or time."
- [other] Apply the fitted drift correction model to all features in the abundance table by normalizing each feature's intensity by the estimated drift at its acquisition timepoint.: "Apply the fitted drift correction model to all features in the abundance table by normalizing each feature's intensity by the estimated drift at its acquisition timepoint."
- [readme] Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances.: "Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances."
- [readme] Batches Skipped - Batches that were skipped due to lack of PREFs: "Batches Skipped - Batches that were skipped due to lack of PREFs"
