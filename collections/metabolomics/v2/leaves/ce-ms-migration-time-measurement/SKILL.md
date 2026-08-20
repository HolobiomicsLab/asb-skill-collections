---
name: ce-ms-migration-time-measurement
description: Use when when processing raw CE-MS data and need to establish a baseline
  migration time scale before transforming to effective mobility.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - MobilityTransformR
  - R
  - xcms
  - MSnbase
  - Spectra
  - msdata
  techniques:
  - CE-MS
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- Description and usage of MobilityTransformR
- compute Procaine's effective mobility using mobilityTransform
- there is no implementation in R that performs effective mobility transformation
  of CE-MS(/MS) data
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac441
  all_source_dois:
  - 10.1093/bioinformatics/btac441
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CE-MS migration time measurement

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and record migration times (retention times) of analytes from capillary electrophoresis–mass spectrometry (CE-MS) datasets, serving as the primary input for subsequent effective mobility transformation. Migration times vary with electroosmotic flow fluctuations and must be precisely measured to enable calibration against EOF markers.

## When to use

When processing raw CE-MS data and need to establish a baseline migration time scale before transforming to effective mobility. Specifically required when the goal is to normalize peak positions across runs with variable electroosmotic flow, or when preparing analyte data for single- or multi-marker mobility calibration using reference compounds with known effective mobilities.

## When NOT to use

- Input is already transformed to effective mobility scale — migration time measurement is a prerequisite, not a post-processing step.
- Capillary electrophoresis–UV (CE-UV) data without MS detection — CE-UV uses different detection and quantitation workflows that do not require subsequent mobility transformation.
- When EOF marker or reference compound migration times are unavailable — the calibration step depends on both analyte and marker migration times, so measurement of markers must be complete first.

## Inputs

- Raw CE-MS electropherogram or extracted ion chromatogram (mzML, NetCDF, or vendor-specific format)
- Analyte peak detection list (m/z, retention time window, signal intensity)
- Experimental metadata: applied voltage (U in kV), capillary length (L in mm or cm), electrical field ramp time (tR in minutes)

## Outputs

- Analyte migration time (tM or rtime) in minutes, per compound
- Data frame with columns: compound name/ID, migration time, m/z, peak intensity, experimental run ID

## How to apply

Load the CE-MS dataset (typically from msdata package or vendor-supplied files) and identify the analyte peak of interest within the extracted ion chromatogram or electropherogram. Record the migration time (tM or rtime) as the time at which the analyte signal reaches its maximum intensity. Measure this value in minutes, converting from raw instrument output if needed (e.g., from seconds to fractional minutes for consistency with calibration parameters tR in 3/60 min format). Ensure the measurement includes the full instrumental runtime context (applied voltage U, capillary length L, temperature conditions). This migration time then serves as the mandatory input to mobilityTransform() for calculation of effective mobility via the single-marker or multi-marker equations. Validate that migration times are stable and reproducible across technical replicates before proceeding to mobility transformation; high variance suggests instrumental drift or EOF instability requiring separate troubleshooting.

## Related tools

- **xcms** (Peak detection and feature extraction from CE-MS raw data; identifies analyte migration times in electropherograms)
- **MSnbase** (Spectral data representation and manipulation; stores and accesses migration time metadata within MS objects)
- **Spectra** (Unified interface for spectrum and chromatogram handling; retrieves migration times from CE-MS objects)
- **msdata** (Provides CE-MS test datasets for validation and prototyping of migration time extraction workflows)
- **MobilityTransformR** (Consumes extracted migration times and applies them as input to mobilityTransform() function for effective mobility calculation) — https://github.com/LiesaSalzer/MobilityTransformR

## Examples

```
# Load CE-MS data and extract Procaine migration time; prepare for mobilityTransform
df_procaine <- data.frame(compound='Procaine', rtime=tM_procaine_mins, marker_rtime=3/60, marker_mobility=0, U=30, L=800, tR=3/60)
mobility_result <- mobilityTransform(df_procaine$rtime, marker_rtime=df_procaine$marker_rtime, marker_mobility=0, tR=3/60, U=30, L=800)
```

## Evaluation signals

- Migration times are recorded in consistent units (minutes) and fall within the expected instrumental runtime window (typically 0–30 min for capillary electrophoresis).
- EOF marker migration time (e.g., Paracetamol in the reference task) is measured and present in the dataset; analyte migration times are greater than EOF marker time for positively charged species under positive voltage.
- Migration time values are reproducible across technical replicates with coefficient of variation < 5–10%, indicating stable EOF and instrumental conditions.
- Both analyte and reference marker migration times can be successfully passed to mobilityTransform() function without schema errors or missing-value flags.
- Extracted migration times align with expected peak positions in the mass trace visualization and match vendor software or literature values for known reference compounds.

## Limitations

- Migration times fluctuate due to electroosmotic flow variations across runs; effective mobility transformation is specifically designed to compensate for this drift, meaning migration time alone is not a stable metric for cross-run peak alignment.
- Measurement accuracy depends on peak detection algorithm quality; co-eluting peaks or low signal-to-noise ratios can produce unreliable migration times.
- No R implementation existed for CE-MS mobility transformation until MobilityTransformR; legacy CE-UV tools or non-R software (e.g., ROMANCE) may not be compatible with standard R data frame formats.
- Migration time measurement from raw instrument files requires format-specific parsers (mzML, NetCDF); proprietary vendor formats may require additional preprocessing or conversion steps.

## Evidence

- [intro] Migration time serves as primary input to mobilityTransform function: "Invoke MobilityTransformR's mobilityTransform function with the calibration parameters: tR (reference time) = 3/60 minutes, U (applied voltage) = +30 kV, and L (capillary length) = 800 cm."
- [intro] Migration times show fluctuations due to EOF variation, necessitating transformation: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] CE-MS mobility transformation differs from CE-UV and requires dedicated implementation: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility"
- [intro] MobilityTransformR consolidates positive and negative mobilities in single output: "However, the outputs are two separate files, each for positive and negative mobilities... the output will be a single file containing both, the positive and negative effective mobilities"
- [readme] Installation and access to CE-MS test data for validation: "if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager"); BiocManager::install("MobilityTransformR")"
