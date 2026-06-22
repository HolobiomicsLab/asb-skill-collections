---
name: technical-replicate-signal-modeling
description: Use when your LCMS metabolomics dataset exhibits run-order-dependent intensity drift (signal decay or gain over the course of a sample batch), you have pooled technical replicates (identical biospecimen injected multiple times across the run sequence) and/or known internal standard compounds, and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - bmxp
  - Python
  - Blueshift
  - bmxp (package)
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

# technical-replicate-signal-modeling

## Summary

Extract and model signal trajectories from pooled technical replicates across LCMS run sequences to establish a reference drift profile, then apply the fitted model to normalize feature intensities across all samples. This is the core method used by Blueshift to correct for systematic intensity drift in metabolomics datasets.

## When to use

Your LCMS metabolomics dataset exhibits run-order-dependent intensity drift (signal decay or gain over the course of a sample batch), you have pooled technical replicates (identical biospecimen injected multiple times across the run sequence) and/or known internal standard compounds, and you need to normalize feature abundances before downstream statistical analysis or cross-dataset alignment.

## When NOT to use

- Input dataset has no pooled technical replicates or internal standards (cannot establish a reference signal trajectory)
- Drift is non-monotonic or highly nonlinear within a batch and cannot be well-captured by polynomial or LOWESS regression
- Samples are already normalized by an upstream instrument method (e.g., internal standard correction applied at acquisition time)

## Inputs

- Feature abundance table (Compound_ID × injection_id pivot table with raw intensity values)
- Feature metadata (bmxp.FMDATA: Compound_ID, RT, MZ, and optional __extraction_method)
- Injection metadata (bmxp.IMDATA: injection_id, injection_type, injection_order, batches)
- Sample metadata (bmxp.SMDATA: broad_id, program_id)

## Outputs

- Drift-corrected feature abundance table (same dimensions as input, normalized intensities)
- Updated injection metadata (bmxp.IMDATA with new QCRole column: 'QC-drift_correction', 'QC-pooled_ref', 'QC-not_used', or 'sample')
- Updated feature metadata (bmxp.FMDATA with new 'Batches Skipped' column tracking batches lacking sufficient pooled reference injections)

## How to apply

Load the raw abundance table (features × injections) and associated metadata identifying which injections are pooled technical replicates and which compounds are internal standards. Extract the abundance signals for these reference materials across all samples to establish a reference signal trajectory as a function of injection order or acquisition time. Fit a smooth drift correction model (e.g., polynomial regression or LOWESS) to the pooled replicate signals. Apply the fitted model to normalize every feature's intensity by dividing each observation by the estimated drift magnitude at its acquisition timepoint. Output the drift-corrected abundance table with identical dimensions to the input, and flag in the injection metadata which batches were successfully corrected (or skipped due to insufficient reference material).

## Related tools

- **Blueshift** (Standalone BMXP module that implements technical-replicate-signal-modeling for drift correction via pooled technical replicates and internal standards) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/blueshift/readme.md
- **bmxp (package)** (Python package providing unified schema (FMDATA, IMDATA, SMDATA) and cloud-compatible infrastructure for running Blueshift and other metabolomics modules) — https://github.com/broadinstitute/bmxp

## Examples

```
from bmxp.blueshift import DriftCorrection; dc = DriftCorrection(abundance_df, feature_metadata, injection_metadata); corrected_abundance, updated_injection_meta, updated_feature_meta = dc.fit_and_correct()
```

## Evaluation signals

- Drift-corrected abundances show reduced correlation with injection order / acquisition time when compared to raw abundances (within pooled technical replicates and across sample batches)
- Pooled technical replicates have lower coefficient of variation (CV) in corrected vs. raw abundances
- Output abundance table has identical shape and Compound_ID × injection_id index as input; no features or injections are dropped
- Injection metadata QCRole column correctly classifies reference injections ('QC-pooled_ref', 'QC-drift_correction') separate from samples
- Feature metadata 'Batches Skipped' column is populated only for features in batches with insufficient pooled reference injections (≥1 entry per batch)

## Limitations

- Requires at least 2–3 pooled technical replicates per batch to fit a stable drift model; batches with fewer replicates are skipped
- Assumes drift is smooth and can be captured by polynomial or LOWESS fitting; abrupt instrument failures or sudden calibration shifts may not be well-corrected
- Pooled replicates must be representative of the overall sample cohort; if replicates are run only at the start/end of a batch, mid-batch drift may be underestimated
- Internal standards must be present and quantifiable in all (or nearly all) injections; missing or saturated standard peaks reduce model quality

## Evidence

- [other] Blueshift is a standalone module designed to perform drift correction on LCMS datasets via pooled technical replicates and internal standards.: "Blueshift is a standalone module designed to perform drift correction on LCMS datasets via pooled technical replicates and internal standards."
- [other] Extract the abundance signals for pooled technical replicates across all samples to establish a reference signal trajectory.: "Extract the abundance signals for pooled technical replicates across all samples to establish a reference signal trajectory."
- [other] Fit a drift correction model (e.g., polynomial or LOWESS) to the technical replicate signals as a function of sample run order or time.: "Fit a drift correction model (e.g., polynomial or LOWESS) to the technical replicate signals as a function of sample run order or time."
- [other] Apply the fitted drift correction model to all features in the abundance table by normalizing each feature's intensity by the estimated drift at its acquisition timepoint.: "Apply the fitted drift correction model to all features in the abundance table by normalizing each feature's intensity by the estimated drift at its acquisition timepoint."
- [readme] Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances.: "Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances."
- [readme] Each tool is meant to be a standalone module that performs a step in our processing pipeline.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline."
