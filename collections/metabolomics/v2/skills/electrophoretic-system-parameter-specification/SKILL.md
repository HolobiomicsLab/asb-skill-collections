---
name: electrophoretic-system-parameter-specification
description: Use when you are preparing to perform effective mobility transformation of CE-MS data and must establish the electrophoretic system's calibration context.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - MobilityTransformR
  - R
  - MetaboCoreUtils
  - Spectra
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- Description and usage of MobilityTransformR
- compute Procaine's effective mobility using mobilityTransform
- there is no implementation in R that performs effective mobility transformation of CE-MS(/MS) data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilitytransformr_cq
    doi: 10.1093/bioinformatics/btac441
    title: MobilityTransformR
  dedup_kept_from: coll_mobilitytransformr_cq
schema_version: 0.2.0
---

# electrophoretic-system-parameter-specification

## Summary

Specification and provision of electrical and physical parameters that define a capillary electrophoresis–mass spectrometry (CE-MS) system for effective mobility transformation. These parameters (applied voltage, capillary length, electrical field ramp time) are required inputs to the mobilityTransform function and must be accurately documented to enable reproducible mobility calibration across analytical runs.

## When to use

You are preparing to perform effective mobility transformation of CE-MS data and must establish the electrophoretic system's calibration context. This skill applies when you have migration time measurements from a CE-MS run and need to convert them to effective mobility values using a reference compound (EOF marker). The skill is triggered when system parameters—particularly applied voltage (U), capillary length (L), and electrical field ramp time (tR)—are available from the instrument method or experimental protocol but have not yet been formally encoded for the mobilityTransform function.

## When NOT to use

- System parameters are unknown or unavailable from the instrument method or experimental documentation—the skill cannot proceed without concrete U, L, and tR values.
- CE-UV (capillary electrophoresis–ultraviolet) data is being analyzed instead of CE-MS; effective mobility transformation for CE-UV does not require the same parameter specification workflow.
- Migration times have already been converted to effective mobility values in a prior analytical step; re-specification would be redundant.

## Inputs

- CE-MS instrument method file or experimental protocol documentation containing electrical and capillary specifications
- Named parameters or configuration object with keys: U (applied voltage in kV), L (capillary length in mm), tR (electrical field ramp time in minutes)

## Outputs

- Structured parameter specification (vector, list, or data frame) compatible with MobilityTransformR::mobilityTransform function
- Validated set of U, L, and tR values ready for use in single-marker effective mobility calibration

## How to apply

Document three core electrophoretic system parameters: (1) applied voltage (U), typically specified in kilovolts (e.g., +30 kV), (2) capillary length (L), measured in millimeters (e.g., 800 mm), and (3) electrical field ramp time (tR), the time during which voltage is ramped to the set value, typically expressed as a fraction of a minute (e.g., 3/60 min = 0.05 min). These parameters are extracted from the CE-MS instrument method file or experimental setup documentation. Organize these values in a named vector or parameter list compatible with the MobilityTransformR package's mobilityTransform function. These specified parameters are then passed alongside migration time measurements and a reference compound (EOF marker with known mobility, typically mobility = 0 for Paracetamol) to compute effective mobility using the single-marker transformation equation. The rationale is that effective mobility is calculated from migration time using the equation µ_eff = (L × U) / (tR × migration_time), normalized by the reference compound's known mobility.

## Related tools

- **MobilityTransformR** (R package that implements the mobilityTransform function accepting the specified electrophoretic system parameters (U, L, tR) to perform single-marker effective mobility transformation on CE-MS data) — https://github.com/LiesaSalzer/MobilityTransformR
- **MetaboCoreUtils** (Bioconductor package providing utility functions for metabolomics data transformation, leveraged by MobilityTransformR)
- **Spectra** (Bioconductor package for MS spectrum representation and manipulation, used within MobilityTransformR workflow)

## Examples

```
mobilityTransform(mtime=3.5, marker_mtime=NA, marker_mobility=0, tR=3/60, U=30, L=800)
```

## Evaluation signals

- All three parameters (U, L, tR) are present, numeric, and within physically plausible ranges for CE-MS (e.g., U > 0 kV, L > 0 mm, tR > 0 min).
- Parameters match the recorded instrument method file or experimental documentation without transcription error or unit mismatch.
- When mobilityTransform is invoked with the specified parameters and a migration time measurement from the same CE-MS run, the resulting effective mobility value is reproducible and stable across repeated reference compound calibrations.
- The single-marker transformation output (effective mobility) is independent of fluctuations in migration time, whereas migration time itself shows variation across runs due to electroosmotic flow drift.
- Parameters are version-controlled or timestamped in the analytical workflow, enabling audit trail linking parameter specification to mobility calibration results.

## Limitations

- Parameters must be accurately transcribed from the instrument method; typographical errors in U, L, or tR will propagate directly into incorrect effective mobility values.
- Effective mobility transformation for CE-MS is more complex than for CE-UV and requires careful parameter specification; incorrect or incomplete specification can prevent proper normalization.
- If the electrophoretic system (capillary, instrument, or voltage settings) changes between runs, parameters must be re-specified; using stale parameters with new data will produce incorrect mobility values.
- The skill assumes that applied voltage (U) and capillary length (L) remain constant within a single analytical run; if voltage ramping or capillary configuration changes mid-run, a single tR value may not adequately represent the system.

## Evidence

- [other] applied voltage (U), capillary length (L), and electrical field ramp time (tR) are critical inputs to mobilityTransform: "Invoke MobilityTransformR's mobilityTransform function with the calibration parameters: tR (reference time) = 3/60 minutes, U (applied voltage) = +30 kV, and L (capillary length) = 800 cm."
- [intro] effective mobility remains stable whereas migration times fluctuate: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] effective mobility transformation for CE-MS requires parameter specification unlike CE-UV: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility"
- [other] parameters are provided to mobilityTransform alongside migration time and reference marker data: "The mobilityTransform function computes Procaine's effective mobility using equation 1 (single marker method) with the Paracetamol EOF marker as reference, requiring inputs of migration time, marker"
