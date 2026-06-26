---
name: migration-time-extraction
description: Use when you have OnDiskMSnExp CE-MS objects with known marker compounds
  (e.g., Paracetamol EOF marker) and need to extract their migration time positions
  to establish a calibration reference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - R
  - MobilityTransformR
  - msdata
  - MetaboCoreUtils
  - xcms
  - MSnbase
  - Spectra
  techniques:
  - LC-MS
  - CE-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- there is no implementation in R that performs effective mobility transformation
  of CE-MS(/MS) data
- Description and usage of MobilityTransformR
- compute Procaine's effective mobility using mobilityTransform
- The CE-MS test data are from the `r BiocStyle::Biocpkg("msdata")` package
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MetaboCoreUtils")`
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("xcms")`
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

# migration-time-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract migration time (MT) coordinates of marker peaks (e.g., EOF markers) from CE-MS data files by generating Extracted Ion Electropherograms (EIE) and applying xcms peak detection with specified m/z and MT range constraints. This preprocessing step is essential for calibrating and normalizing migration time scales before effective mobility transformation.

## When to use

Apply this skill when you have OnDiskMSnExp CE-MS objects with known marker compounds (e.g., Paracetamol EOF marker) and need to extract their migration time positions to establish a calibration reference. Specifically, use it when you require per-file MT values to correct for electroosmotic flow variations that cause migration time drift across replicate analyses.

## When NOT to use

- Input data are already effective mobility–transformed or already contain pre-computed migration time values; use getMtime only on raw OnDiskMSnExp CE-MS objects.
- No known internal standard or marker peak is available; getMtime requires a reference compound with known m/z to anchor the extraction.
- Migration time ranges are extremely broad or poorly constrained; wide MT-range parameters lead to spurious peak detection.

## Inputs

- OnDiskMSnExp object (CE-MS raw data)
- m/z range (numeric vector or single value with tolerance)
- Migration time range (numeric vector defining lower and upper MT bounds)
- Known marker compound mass and approximate migration time

## Outputs

- Per-file migration time table (file identifier × MT value)
- Structured output file (e.g., CSV or tabular format) with MT values and file metadata

## How to apply

Load CE-MS test files from the msdata package into R as OnDiskMSnExp objects. Call the getMtime() function, supplying the object, a narrow m/z range (mz-range parameter) centered on the marker's known mass, and a plausible migration time window (MT-range parameter). The function generates an Extracted Ion Electropherogram (EIE) by filtering the raw data to the specified m/z tolerance, then invokes xcms::findChromPeaks() to locate the peak within the MT range. Narrow m/z and MT ranges are critical to ensure correct peak detection and avoid false positives. Compile the extracted MT values into a per-file table with file identifiers. Export the result as a structured output file for use in downstream effective mobility calibration workflows.

## Related tools

- **MobilityTransformR** (Package providing getMtime() function for extraction of migration time from CE-MS OnDiskMSnExp objects) — https://github.com/LiesaSalzer/MobilityTransformR
- **xcms** (Provides findChromPeaks() algorithm for peak detection in Extracted Ion Electropherograms)
- **MSnbase** (Supplies OnDiskMSnExp class and spectral data handling for CE-MS files)
- **Spectra** (Provides spectral data representation and filtering infrastructure)
- **msdata** (Supplies CE-MS test data files for validation and example workflows)
- **MetaboCoreUtils** (Supplies core metabolomics data transformation and utility functions)

## Examples

```
getMtime(OnDiskMSnExp_object, mz = c(151.04, 151.08), mt = c(8.0, 12.0))
```

## Evaluation signals

- Extracted MT values fall within the specified MT-range parameter and are reproducible across replicate files.
- Per-file MT table contains no missing values (NA) for successfully processed files, indicating peak detection succeeded.
- MT values cluster around the expected migration time of the marker compound; outliers or bimodal distributions suggest m/z or MT range misconfiguration.
- Comparison of extracted MT values across replicate files shows expected drift consistent with electroosmotic flow variation, not random noise.
- Output file structure matches expected schema (file identifier column, MT value column, metadata columns); schema validation passes without errors.

## Limitations

- getMtime() requires narrow m/z and MT ranges to ensure correct peak detection; overly broad ranges cause false positives or missed detections.
- Migration time extraction depends on the quality and signal intensity of the marker peak; low-abundance or noisy peaks may not be detected reliably.
- The function is specific to CE-MS data; it cannot be applied to LC-MS or other chromatographic techniques.
- Effective mobility transformation for CE-MS data is not straightforward as in CE-UV, and migration time alone does not account for electroosmotic flow variations; extracted MT values must be combined with effective mobility calibration for reproducibility.

## Evidence

- [other] The getMtime() function accepts an OnDiskMSnExp object, mz-range, and MT-range as inputs and determines the migration time of a marker peak by generating an Extracted Ion Electropherogram (EIE) and using findChromPeaks from xcms to pick the peak, with narrow mz and mt ranges required to ensure correct peak detection.: "The getMtime() function accepts an OnDiskMSnExp object, mz-range, and MT-range as inputs and determines the migration time of a marker peak by generating an Extracted Ion Electropherogram (EIE) and"
- [intro] the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility"
- [intro] The CE-MS test data are from the `r BiocStyle::Biocpkg("msdata")` package: "The CE-MS test data are from the `r BiocStyle::Biocpkg("msdata")` package"
- [readme] To install MobilityTransformR, use the stable version available at Bioconductor.: "To install MobilityTransformR, use the stable version available at Bioconductor."
