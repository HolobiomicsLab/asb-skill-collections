---
name: metabolite-abundance-drift-correction
description: Use when you have a raw LCMS nontargeted metabolomics abundance table spanning multiple injections with embedded pooled technical replicate (PREF) or internal standard injections distributed across the run sequence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - bmxp
  - Python
  - bmxp (BMXP platform)
  - Chroma
  - Eclipse
  - Gravity
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf290/8128335
  all_source_dois:
  - 10.1093/bioinformatics/btaf290/8128335
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-abundance-drift-correction

## Summary

Blueshift is a drift correction module that normalizes LCMS metabolomics abundance tables by fitting a polynomial or LOWESS model to pooled technical replicate signals across sample run order, then applying the estimated drift trajectory to correct intensity measurements at each feature's acquisition timepoint. This correction mitigates systematic signal decay or drift that accumulates during long instrument runs.

## When to use

Apply this skill when you have a raw LCMS nontargeted metabolomics abundance table spanning multiple injections with embedded pooled technical replicate (PREF) or internal standard injections distributed across the run sequence. Drift correction is essential for studies with long acquisition windows (hours to days) or where instrument sensitivity decay is suspected to bias feature intensities, particularly when comparing samples acquired early versus late in the instrument run.

## When NOT to use

- Input data lacks pooled technical replicates or internal standards distributed across the run — drift correction cannot establish a reference trajectory without replicate signals spanning acquisition time.
- Abundance table is already normalized or corrected by instrument software or another preprocessing pipeline — applying Blueshift a second time risks over-correction.
- Study design includes only a single short batch or run with minimal run-time variation — drift effects are negligible and correction may introduce noise.

## Inputs

- Feature abundances pivot table (Compound_ID × injection_id) with raw intensity values
- Feature metadata (bmxp.FMDATA) with Compound_ID, RT, MZ, and other feature descriptors
- Injection metadata (bmxp.IMDATA) with injection_id, injection_type, injection_order, and biospecimen labels
- Pooled technical replicate (PREF) identifiers and internal standard compound list

## Outputs

- Drift-corrected feature abundance table (same Compound_ID × injection_id structure)
- Updated feature metadata with 'Batches Skipped' column documenting QC coverage
- Updated injection metadata with QCRole assignments ('QC-drift_correction', 'QC-pooled_ref', 'QC-not_used', 'sample')

## How to apply

Load the raw abundance table (pivot table of Compound_ID × injection_id) and injection metadata identifying pooled technical replicates and their injection_type labels ('prefa' or 'prefb'). Extract abundance signals for all pooled technical replicate injections to establish a reference signal trajectory as a function of injection_order or acquisition time. Fit a polynomial or LOWESS drift correction model to these replicate signals. Apply the fitted model to normalize each feature's intensity by dividing by the estimated drift at that feature's acquisition timepoint, outputting a drift-corrected abundance table with identical dimensions. Flag batches with insufficient PREF coverage (stored in 'Batches Skipped' column) for downstream QC review. Optionally assign QCRole labels ('QC-drift_correction', 'QC-pooled_ref', or 'sample') to injection metadata to document which injections contributed to the correction model.

## Related tools

- **bmxp (BMXP platform)** (Package housing the Blueshift drift correction module; provides shared schema (FMDATA, IMDATA, SMDATA, Feature Abundances) and CLI/Python API for running drift correction as a standalone step) — https://github.com/broadinstitute/bmxp
- **Chroma** (Reads raw .raw and .mzml instrument files upstream of drift correction; outputs feature abundances and metadata that feed into Blueshift) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/chroma/readme.md
- **Eclipse** (Aligns two or more same-method nontargeted LCMS datasets; typically runs before Blueshift to harmonize feature identifiers and retention times across batches) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/eclipse/readme.md
- **Gravity** (Clusters redundant LCMS features based on retention time and correlation; runs after Blueshift to group duplicate features before final formatting) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md

## Evaluation signals

- Output abundance table has identical dimensions (Compound_ID count, injection_id count) to input; no features or injections are dropped.
- Drift-corrected intensities for pooled technical replicate injections show reduced variance (measured by coefficient of variation or SD) across the run compared to raw intensities, indicating successful systematic correction.
- Feature metadata includes a 'Batches Skipped' column documenting which batches lack sufficient PREF coverage; absence or all-zero values indicate complete drift model fit.
- Injection metadata QCRole assignments correctly label all pooled replicate injections as 'QC-pooled_ref' or 'QC-drift_correction' and all samples as 'sample'; injection_type and QCRole are consistent.
- Comparison of mean corrected intensity per batch shows no significant trend or slope across injection_order for pooled replicates, confirming drift removal.

## Limitations

- Drift correction requires a minimum density of pooled technical replicate injections distributed throughout the run; sparse or clustered PREFs may yield an unreliable or overfitted drift model.
- Fitting method choice (polynomial degree, LOWESS bandwidth) is not explicitly parameterized in the article; users must refer to the Blueshift README or source code for tuning guidance.
- Correction assumes drift is systematic and smooth across acquisition time; abrupt instrument failures or recalibrations mid-run are not handled and may require manual batch partitioning.
- Internal standard abundance signals used for drift estimation may themselves be subject to ionization or extraction variability; their use as a correction reference can propagate biases if standards are not validated.
- Batches with zero or very few pooled replicates are flagged in 'Batches Skipped' but not automatically excluded; downstream analyses must manually filter or interpret these batches with caution.

## Evidence

- [other] Blueshift is a standalone module designed to perform drift correction on LCMS datasets via pooled technical replicates and internal standards.: "Blueshift is a standalone module designed to perform drift correction on LCMS datasets via pooled technical replicates and internal standards."
- [other] Extract the abundance signals for pooled technical replicates across all samples to establish a reference signal trajectory. Fit a drift correction model (e.g., polynomial or LOWESS) to the technical replicate signals as a function of sample run order or time.: "Extract the abundance signals for pooled technical replicates across all samples to establish a reference signal trajectory. Fit a drift correction model (e.g., polynomial or LOWESS) to the technical"
- [other] Apply the fitted drift correction model to all features in the abundance table by normalizing each feature's intensity by the estimated drift at its acquisition timepoint.: "Apply the fitted drift correction model to all features in the abundance table by normalizing each feature's intensity by the estimated drift at its acquisition timepoint."
- [readme] Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances.: "Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances."
- [readme] Each tool is meant to be a standalone module that performs a step in our processing pipeline.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline."
- [readme] injection_type - Type of injection ('sample', 'prefa', 'prefb', 'blank', 'other-', 'not_used-'): "injection_type - Type of injection ('sample', 'prefa', 'prefb', 'blank', 'other-', 'not_used-')"
- [readme] Generated by Blueshift: Batches Skipped - Batches that were skipped due to lack of PREFs: "Batches Skipped - Batches that were skipped due to lack of PREFs"
- [readme] QCRole - Role in drift correction ('QC-drift_correction', 'QC-pooled_ref', 'QC-not_used', 'sample'): "QCRole - Role in drift correction ('QC-drift_correction', 'QC-pooled_ref', 'QC-not_used', 'sample')"
