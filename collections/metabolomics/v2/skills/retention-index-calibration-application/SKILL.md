---
name: retention-index-calibration-application
description: Use when when processing GC-MS data where retention time alone is insufficient
  for compound identification due to instrument drift or method variation, and you
  need to match detected peaks against a spectral library (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - CoreMS
  - GC_RI_Calibration
  - LowResMassSpectralMatch
  - PNNLMetV20191015.MSL
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development
  and data analysis of small molecules analysis.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-index-calibration-application

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Retention index (RI) calibration transforms GC-MS retention times into standardized indices using FAMES (fatty acid methyl ester) standards, enabling reliable compound identification across instruments and methods by normalizing peak elution order to a reference scale. This calibration is prerequisite for spectral library matching in low-resolution GC-MS workflows.

## When to use

When processing GC-MS data where retention time alone is insufficient for compound identification due to instrument drift or method variation, and you need to match detected peaks against a spectral library (e.g., GCMS spectral library) that uses retention index as a filtering or ranking criterion. Specifically, apply this skill before executing spectral matching algorithms when working with ANDI NetCDF GC-MS datasets containing multiple chromatographic peaks.

## When NOT to use

- Input data is already retention-index-annotated or sourced from a pre-calibrated library (e.g., NIST library peaks already have RI values assigned).
- Working with high-resolution GC-MS where m/z accuracy alone (< 5 ppm) is sufficient for unambiguous compound identification; RI calibration adds minimal discriminatory value.
- FAMES or other RI standard peaks are absent or not reliably detected in the chromatogram (calibration would be unreliable).

## Inputs

- ANDI NetCDF GC-MS dataset (.cdf file with chromatographic peaks and m/z spectra)
- Detected peak list (retention times, m/z values, peak intensities)
- FAMES standard retention times (reference calibration compounds and their known RI values)

## Outputs

- Retention-index-calibrated peak list (original peaks annotated with computed RI values)
- Calibration function/model (e.g., polynomial coefficients mapping retention time to RI)
- Calibration residuals and diagnostic metrics (RI prediction error per FAMES standard)

## How to apply

Load the ANDI NetCDF GC-MS dataset using CoreMS input module to access the chromatographic data structure. Apply GC_RI_Calibration to the peak list using FAMES standard retention times as reference markers; this computes a calibration function (typically linear or polynomial) that maps observed retention times to standardized retention indices on the alkane scale. The calibration corrects for instrument-specific retention time shifts and column aging effects. Pass the retention-index-calibrated peak list to downstream spectral matching algorithms (e.g., LowResMassSpectralMatch) which filter and rank library candidates using both m/z spectral similarity and RI alignment confidence. Verify calibration quality by inspecting the residuals between predicted and observed RI values for FAMES standards; typical acceptable error is < 2–5 RI units for GC-MS.

## Related tools

- **CoreMS** (Framework providing ANDI NetCDF input module, GC_RI_Calibration algorithm, and peak data structures for retention index computation) — https://github.com/EMSL-Computing/CoreMS
- **GC_RI_Calibration** (CoreMS module that computes retention indices for detected peaks using FAMES standard retention times as reference) — https://github.com/EMSL-Computing/CoreMS
- **LowResMassSpectralMatch** (CoreMS spectral matching algorithm that ranks library candidates using both m/z similarity and RI alignment confidence from calibrated peaks) — https://github.com/EMSL-Computing/CoreMS
- **PNNLMetV20191015.MSL** (GCMS spectral library bundled with CoreMS; serves as reference database for spectral matching after RI calibration) — https://github.com/EMSL-Computing/CoreMS

## Examples

```
from corems.gc_ms.input import ANDI_NetCDF; from corems.gc_ms.calibration import GC_RI_Calibration; ms = ANDI_NetCDF('sample.cdf').get_mass_spectrum(); GC_RI_Calibration(ms, fames_standards).run(); matched = LowResMassSpectralMatch(ms.peaks, spectral_library='PNNLMetV20191015.MSL').execute()
```

## Evaluation signals

- FAMES standard peaks map to their known RI values with residuals < 5 RI units (or within instrument vendor specification)
- All detected peaks are assigned a valid RI value (no null or NaN values in calibrated output); RI values increase monotonically with retention time
- Downstream spectral matching ranks correct library compounds higher when RI filter is enabled vs. disabled, indicating RI calibration improves specificity
- Calibration function (e.g., polynomial fit) has R² > 0.99 when predicting RI from retention time across the full chromatographic range
- RI-calibrated peaks from replicate injections differ by < 2 RI units, demonstrating reproducibility

## Limitations

- RI calibration assumes FAMES standards (or equivalent alkane references) are present and co-elute with analytes; if standards are degraded, absent, or poorly resolved, calibration fails or produces unreliable RI values.
- RI is column-dependent and temperature/pressure-sensitive; calibration is valid only for the specific GC method and column used; transferring RI values across different column phases or stationary chemicals is not straightforward.
- Low-resolution MS (unit m/z) spectral library matching after RI calibration remains susceptible to false positives if multiple compounds share similar fragmentation patterns; RI filtering alone does not guarantee compound identity.
- The linear or polynomial model underlying RI calibration assumes smooth, monotonic retention time progression; highly non-linear or segmented chromatograms may require piecewise calibration models not covered in the standard workflow.

## Evidence

- [other] research_question: "How does the LowResMassSpectralMatch algorithm use retention index calibration data to improve compound identification in low-resolution GC-MS data?"
- [other] workflow_step_1: "Load ANDI NetCDF GC-MS dataset using CoreMS input module for GC-MS format support."
- [other] workflow_step_2: "Apply GC_RI_Calibration to compute retention indices for each detected peak."
- [other] workflow_step_3_and_4: "Initialize LowResMassSpectralMatch spectral matching algorithm with PNNLMetV20191015.MSL spectral library as reference database. Execute spectral matching using retention-index-calibrated peaks to"
- [other] fames_standard_role: "LowResMassSpectralMatch performs spectral matching against a bundled GCMS spectral library after retention index calibration using FAMES standards"
- [readme] gcms_feature_from_readme: "Retention Index Calibration. Automatic local (SQLite) or external (MongoDB or PostgreSQL) database check, generation, and search. Automatic molecular match algorithm with all spectral similarity"
- [readme] data_input_format: "ANDI NetCDF for GC-MS (.cdf)"
