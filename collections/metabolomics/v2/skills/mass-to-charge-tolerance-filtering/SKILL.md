---
name: mass-to-charge-tolerance-filtering
description: Use when extracting migration times of specific analyte or reference markers (e.g., Paracetamol EOF marker) from CE-MS files using peak-picking workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
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
  - build: coll_metabcombiner_cq
    doi: 10.1021/acs.analchem.0c03693
    title: metabCombiner
  - build: coll_mobilitytransformr_cq
    doi: 10.1093/bioinformatics/btac441
    title: MobilityTransformR
  dedup_kept_from: coll_mobilitytransformr_cq
schema_version: 0.2.0
---

# mass-to-charge-tolerance-filtering

## Summary

Filter ion peaks in CE-MS data by specifying narrow m/z tolerance windows to ensure correct peak detection during extracted ion electropherogram (EIE) generation. This skill is essential when extracting migration times of known markers (e.g., EOF markers) where precise m/z ranges prevent false peak assignments.

## When to use

Apply this skill when extracting migration times of specific analyte or reference markers (e.g., Paracetamol EOF marker) from CE-MS files using peak-picking workflows. Use it when the getMtime() function or similar extracted ion electropherogram methods require m/z-range filtering to isolate a single peak of interest from a crowded mass spectrum.

## When NOT to use

- When you do not have a prior knowledge of the target marker's theoretical m/z value or approximate migration time window.
- When the goal is untargeted feature detection across the full m/z and MT range (use full-spectrum peak picking instead).
- When the m/z tolerance is already defined by a pre-computed feature matrix or reference library (use library matching instead).

## Inputs

- OnDiskMSnExp object (CE-MS raw data, loaded from msdata package or equivalent)
- Theoretical m/z value of target marker (e.g., Paracetamol)
- Approximate migration time range for the marker (in minutes or seconds)

## Outputs

- Extracted Ion Electropherogram (EIE) filtered by m/z tolerance
- Peak table with detected marker peak(s), migration time(s), and intensity(ies)
- Per-file migration time table with file identifiers and MT values

## How to apply

Define a narrow m/z tolerance range (e.g., ±0.5 Da or tighter, depending on instrument resolution) centered on the target marker's theoretical m/z value. Pass this m/z-range as a parameter to the peak-detection function (e.g., getMtime with mz-range argument, or xcms::findChromPeaks on an EIE). Combine the m/z filter with a migration time (MT) range filter to further constrain the search space and ensure the peak-picking algorithm identifies only the intended marker. The rationale is that narrow m/z and MT ranges together prevent spurious peak detection and ensure reproducible extraction of marker migration times across multiple CE-MS files.

## Related tools

- **MobilityTransformR** (Implements getMtime() function to extract migration times with m/z and MT-range filtering; provides the primary workflow for this skill) — https://github.com/LiesaSalzer/MobilityTransformR
- **xcms** (Provides findChromPeaks() function for peak detection on extracted ion electropherograms filtered by m/z tolerance)
- **MetaboCoreUtils** (Contributes utility functions for effective mobility transformation and m/z-based filtering)
- **MSnbase** (Provides OnDiskMSnExp object class and spectral data handling for m/z filtering operations)
- **Spectra** (Enables efficient m/z-based filtering and extraction of ion traces)
- **msdata** (Provides CE-MS test data files for development and validation of m/z filtering workflows)

## Examples

```
getMtime(object = mse, mz = c(194.08, 194.10), MT = c(8, 12))
```

## Evaluation signals

- EIE plot shows a single, well-isolated peak at the expected migration time (no spurious peaks or baseline noise).
- Peak detection success rate is 100% across all input CE-MS files (all files yield a valid MT value, with no failed peak picks).
- Extracted MT values are reproducible and fall within the expected range for the marker in the given electrophoretic system.
- The m/z range filter excludes interfering ions: verify by comparing EIE with and without m/z filtering, or by inspecting the raw spectrum at the detected MT.
- Output per-file MT table has no missing values and all MT entries are numeric and within the specified MT-range bounds.

## Limitations

- Narrow m/z tolerances may fail to detect the marker if the theoretical m/z is inaccurate or if the instrument's mass calibration is poor.
- Migration time shifts caused by electroosmotic flow (EOF) variations between runs may cause the marker peak to fall outside the predefined MT-range filter, leading to missed detections.
- Effective mobility transformation for CE-MS is not as straightforward as CE-UV; m/z-based filtering alone does not address MT drift, which may require concurrent use of internal standards or EOF markers.
- Performance depends critically on having accurate prior knowledge of both the target marker's m/z and its typical MT window; for novel or unstable markers, an exploratory untargeted analysis may be necessary first.

## Evidence

- [other] The getMtime() function accepts an OnDiskMSnExp object, mz-range, and MT-range as inputs and determines the migration time of a marker peak by generating an Extracted Ion Electropherogram (EIE) and using findChromPeaks from xcms to pick the peak, with narrow mz and mt ranges required to ensure correct peak detection.: "The getMtime() function accepts an OnDiskMSnExp object, mz-range, and MT-range as inputs and determines the migration time of a marker peak by generating an Extracted Ion Electropherogram (EIE) and"
- [intro] the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility"
- [intro] The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("xcms")`: "The transformation is performed using functionality from the packages xcms"
- [readme] To install MobilityTransformR, use the stable version available at Bioconductor. Enter: if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager"); BiocManager::install("MobilityTransformR"): "To install MobilityTransformR, use the stable version available at Bioconductor"
