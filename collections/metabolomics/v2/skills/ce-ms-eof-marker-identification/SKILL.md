---
name: ce-ms-eof-marker-identification
description: Use when when processing CE-MS test files and you need to identify and extract the migration time of the EOF marker (e.g., Paracetamol) to normalize compound migration times across runs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - R
  - MobilityTransformR
  - msdata
  - MetaboCoreUtils
  - xcms
  - MSnbase
  - Spectra
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- there is no implementation in R that performs effective mobility transformation of CE-MS(/MS) data
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
---

# ce-ms-eof-marker-identification

## Summary

Extraction of capillary electrophoresis–mass spectrometry (CE-MS) end-of-flow (EOF) marker migration times using peak detection on extracted ion electropherograms. This skill enables accurate EOF marker localization—a prerequisite for effective mobility transformation in CE-MS workflows where migration time fluctuations due to electroosmotic flow variations must be corrected.

## When to use

When processing CE-MS test files and you need to identify and extract the migration time of the EOF marker (e.g., Paracetamol) to normalize compound migration times across runs. Apply this skill before effective mobility transformation, especially when migration time reproducibility is compromised by electroosmotic flow drift.

## When NOT to use

- Input is already normalized to effective mobility scale (migration time normalization is already complete)
- CE-UV (capillary electrophoresis with UV detection) data; this skill is specific to CE-MS where effective mobility transformation requires mass-resolved EOF marker detection
- Data lacks a known EOF marker or spiked internal standard at a defined mz value

## Inputs

- OnDiskMSnExp object (CE-MS data loaded from msdata package or similar)
- mz-range parameter (mass-to-charge tolerance window around EOF marker)
- migration time (MT) range parameter (time window for peak search)

## Outputs

- Extracted Ion Electropherogram (EIE) for the specified mz-range
- Peak detection results from findChromPeaks (peak apex, area, intensity)
- Structured table: file identifiers with corresponding EOF marker migration time values
- Exported migration time table (e.g., CSV or similar format)

## How to apply

Load CE-MS data as an OnDiskMSnExp object (e.g., from msdata package in R). Call the getMtime() function with three key inputs: (1) the OnDiskMSnExp object, (2) a narrow mz-range (e.g., mz tolerance around the EOF marker's mass) and (3) a migration time (MT) range filter to constrain the search space. The function generates an Extracted Ion Electropherogram (EIE) for the specified mz-range, then applies findChromPeaks from xcms to automatically pick the peak within the MT-range. Narrow mz and mt ranges are critical to ensure correct peak detection and avoid false positives. Extract and compile the resulting migration time values into a per-file table with file identifiers, then export as a structured output file for downstream effective mobility calculations.

## Related tools

- **MobilityTransformR** (Provides the getMtime() function and overall framework for EOF marker extraction and effective mobility transformation of CE-MS data) — https://github.com/LiesaSalzer/MobilityTransformR
- **xcms** (Supplies findChromPeaks function for automated peak detection on extracted ion electropherograms)
- **MSnbase** (Foundational package for handling mass spectrometry data and OnDiskMSnExp objects)
- **Spectra** (Provides efficient data structures for CE-MS spectra representation)
- **MetaboCoreUtils** (Utility functions for metabolomics data transformation and processing)
- **msdata** (Source package containing CE-MS test data and example files)

## Examples

```
getMtime(msnexp_object, mz = c(150.05, 150.15), mt = c(5, 25))
```

## Evaluation signals

- Extracted migration time values are consistent across replicate files (low inter-file variance for the same EOF marker)
- Peak detection produces a single, unambiguous peak within the specified MT-range for each file (no multiple peaks or missed detections)
- Extracted migration times fall within the expected biological/instrumental range (e.g., all values > 0 and < total run time)
- Peak quality metrics (e.g., signal-to-noise ratio, peak shape) from findChromPeaks indicate robust detection (low baseline, symmetric peak)
- Migration time table structure matches expected schema: one row per file, with file identifier and EOF marker MT value columns

## Limitations

- Narrow mz and mt ranges are required for correct peak detection; overly broad ranges risk false positives from interfering ions or noise
- EOF marker must be present, detectable, and at a known or determinable mz value; absence or suppression of the marker will cause peak detection to fail
- Migration time extraction assumes stable electrospray ionization and mass calibration across files; instrumental drift may compromise accuracy
- The skill does not address cases where the EOF marker co-elutes with other compounds or is present at very low abundance
- Effective mobility transformation (the downstream application) requires accurate EOF marker extraction; errors here propagate to normalized mobility values

## Evidence

- [other] The getMtime() function accepts an OnDiskMSnExp object, mz-range, and MT-range as inputs and determines the migration time of a marker peak by generating an Extracted Ion Electropherogram (EIE) and using findChromPeaks from xcms to pick the peak, with narrow mz and mt ranges required to ensure correct peak detection.: "The getMtime() function accepts an OnDiskMSnExp object, mz-range, and MT-range as inputs and determines the migration time of a marker peak by generating an Extracted Ion Electropherogram (EIE) and"
- [intro] the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility"
- [readme] To install MobilityTransformR, use the stable version available at Bioconductor. Enter:: "To install MobilityTransformR, use the stable version available at Bioconductor. Enter:"
