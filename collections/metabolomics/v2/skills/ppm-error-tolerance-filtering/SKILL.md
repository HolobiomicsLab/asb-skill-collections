---
name: ppm-error-tolerance-filtering
description: Use when after molecular formula assignment has been performed on FT-ICR
  MS peaks and you need to remove assignments with unacceptable mass error before
  proceeding to chemodiversity analysis, transformation network generation, or multivariate
  statistics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - MetaboDirect
  - CoreMS
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis
  (e.g., chemodiversity analysis, multivariate statistics)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ppm-error-tolerance-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter molecular formula assignments from high-resolution mass spectrometry peaks by requiring mass error to fall within a specified parts-per-million (ppm) threshold. This skill removes unreliable formula assignments before downstream biochemical network analysis or statistical interpretation.

## When to use

Apply this skill after molecular formula assignment has been performed on FT-ICR MS peaks and you need to remove assignments with unacceptable mass error before proceeding to chemodiversity analysis, transformation network generation, or multivariate statistics. Use when the quality of subsequent network or statistical conclusions depends on formula assignment accuracy.

## When NOT to use

- Input peaks have not yet undergone molecular formula assignment (no formulas to filter against).
- Your mass spectrometry instrument has lower mass accuracy (e.g., quadrupole or Orbitrap with >1 ppm typical error); the 0.5 ppm threshold is instrument-specific to FT-ICR MS and may be too stringent for lower-resolution platforms.
- You are working with pre-filtered data that has already been quality-controlled by an upstream pipeline and you have no access to individual peak m/z values or formula assignments.

## Inputs

- peak list with m/z values (CSV or tabular format)
- molecular formula assignments per peak (assigned by prior signal processing step)
- measured peak m/z values with decimal precision

## Outputs

- filtered peak list (CSV) retaining only peaks meeting mass error threshold
- count of peaks retained vs. rejected per error tolerance
- filtered data matrix for downstream analysis

## How to apply

Compare the measured m/z of each detected peak against the theoretical m/z of its assigned molecular formula, then calculate mass error in parts per million. Retain only peaks whose mass error meets or exceeds a user-defined threshold (the MetaboDirect pipeline uses 0.5 ppm error as the filtering cutoff). This filtering step typically occurs after initial peak detection and isotope filtering but before compound class determination and normalization. The rationale is that FT-ICR MS delivers sub-ppm mass accuracy, and stringent error tolerance (≤0.5 ppm) ensures that only high-confidence formula assignments propagate into network inference, where false transformations could be mistakenly inferred from incorrectly assigned peaks.

## Related tools

- **MetaboDirect** (command-line pipeline that implements ppm-error-based filtering of molecular formulas as a built-in data pre-processing step before chemodiversity and transformation network analysis) — https://github.com/Coayala/MetaboDirect
- **CoreMS** (comprehensive software framework for FT-ICR MS signal processing that can produce initial peak and formula assignment data requiring downstream error filtering)

## Evaluation signals

- Verify that all retained peaks have mass error ≤ 0.5 ppm (or your specified threshold) when recalculated from assigned formula and measured m/z.
- Check that the count of rejected peaks is reasonable relative to total peaks (typically 40–50% of peaks are filtered out due to formula assignment failure or high error, not solely by ppm tolerance).
- Confirm that downstream transformation networks contain no spurious transformations arising from misassigned peaks by validating that inferred transformation masses match the reference biochemical transformation key within ±1 ppm.
- Inspect the distribution of mass errors in retained vs. rejected peaks; rejected peaks should cluster at higher error magnitudes.
- Validate that chemodiversity metrics and multivariate statistics (PCA, NMDS) are stable and reproducible when the filtering threshold is applied consistently across all samples.

## Limitations

- The 0.5 ppm threshold is specific to FT-ICR MS and the MetaboDirect pipeline; other high-resolution MS techniques (Orbitrap, time-of-flight) may require different thresholds.
- Filtering alone does not remove false positive formula assignments that happen to fall within the ppm tolerance by chance; orthogonal validation (e.g., database matching, isotope pattern scoring) may be necessary.
- If a peak receives multiple plausible formula assignments, the filtering step as described assumes only one formula per peak; ambiguous assignments must be resolved before filtering.
- MetaboDirect does not provide raw spectra data preprocessing, so input peaks and formulas must come from an external tool (e.g., CoreMS, Formularity); ppm-error filtering cannot be applied earlier in the acquisition pipeline.

## Evidence

- [methods] filtering by error in formula assignment (0.5 ppm): "filtering by error in formula assignment (0.5 ppm)"
- [other] calculated all pairwise mass differences between detected peaks and matched to transformation database with mass error ≤1 ppm tolerance: "Calculate all pairwise mass differences between detected peaks in each sample. 3. Match each mass difference to the reference biochemical transformation key, retaining transformations with mass error"
- [intro] Signal processing and molecular formula assignment produces large data matrices: "Signal processing and molecular formula assignment steps will ultimately produce large data matrices containing the elemental composition and measured abundance of the peaks present in each sample"
- [intro] MetaboDirect pipeline accepts peak abundance and assigned molecular formula data: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique"
- [methods] MetaboDirect does not provide raw spectra data preprocessing: "MetaboDirect does not provide raw spectra data preprocessing"
