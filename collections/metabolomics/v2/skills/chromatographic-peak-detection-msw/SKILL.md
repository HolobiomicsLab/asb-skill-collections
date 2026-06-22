---
name: chromatographic-peak-detection-msw
description: Use when you have raw mzML files from an FTICR-MS or other direct-injection MS instrument and need to identify discrete chromatographic peaks across the m/z and retention-time dimensions. Use this skill when you must isolate individual ion signals before applying calibration corrections (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MsFeatures
  - Spectra
  - MsBackendMgf
  - MetaboCoreUtils
  - xcms
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
- doi: 10.5281/zenodo.18494293
  title: ''
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
- library(Spectra)
- library(MsBackendMgf)
- '%\VignetteDepends{xcms,MsDataHub,BiocStyle,pander,Spectra,MsBackendMgf,MetaboCoreUtils}'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac051437y
  all_source_dois:
  - 10.1021/ac051437y
  - 10.5281/zenodo.18494293
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-peak-detection-msw

## Summary

Detect chromatographic peaks in direct-injection or LC-MS data using the MSWParam algorithm, which identifies signal clusters by integrating mass and intensity information. This skill is essential for isolating individual ion signals prior to mass calibration, feature grouping, or spectral annotation in untargeted metabolomics workflows.

## When to use

You have raw mzML files from an FTICR-MS or other direct-injection MS instrument and need to identify discrete chromatographic peaks across the m/z and retention-time dimensions. Use this skill when you must isolate individual ion signals before applying calibration corrections (e.g., edgeshift) or extracting MS/MS spectra for compound identification. The MSWParam algorithm is appropriate when signal-to-noise is high and you expect well-defined peak boundaries.

## When NOT to use

- Input is already a preprocessed feature table or consensus peak list — re-detection would be redundant.
- Signal-to-noise is very low (< 5:1) or peaks are poorly resolved; use CentWaveParam or other wavelet-based algorithms instead.
- You require peak picking on isolated MS/MS spectra with different dynamic-range characteristics; use findChromPeaksIsolationWindow() for MS2-specific detection.

## Inputs

- XCMSnExp object (initialized from raw mzML files)
- MSWParam parameter object

## Outputs

- XCMSnExp object with populated chromPeaks matrix (columns: mz, mzmin, mzmax, rt, rtmin, rtmax, into, intb, maxo, sn)
- Chromatographic peak table (accessible via chromPeaks() method)

## How to apply

Load raw mzML data into an xcms XCMSnExp object using the appropriate data import method. Create an MSWParam instance and call findChromPeaks() on the XCMSnExp object with this parameter object. The MSWParam algorithm scans the m/z–intensity–retention-time space and identifies peaks based on connected-component clustering. The resulting object contains a chromPeaks matrix with columns for m/z (median), retention time, peak area, and intensity. Verify detection success by checking that peaks are identified across your target m/z range and that peak counts are reasonable relative to file complexity. Visualize detected peaks in m/z–retention-time space to confirm spatial clustering corresponds to expected compound locations.

## Related tools

- **xcms** (Provides XCMSnExp class, findChromPeaks() method, and MSWParam algorithm for peak detection in mass spectrometry data) — https://github.com/sneumann/xcms

## Examples

```
library(xcms); xdata <- readMzmlFiles('path/to/mzml/'); xdata <- findChromPeaks(xdata, MSWParam()); peaks <- chromPeaks(xdata)
```

## Evaluation signals

- chromPeaks matrix is populated with m/z, retention time, area, and intensity values; no empty or NaN rows
- Median m/z and retention time for each peak fall within expected ranges for the instrument and sample
- Peak count and distribution across m/z space is consistent with known compound complexity; sparse regions contain fewer peaks
- Visualized peaks in m/z–retention-time space form expected spatial clusters without isolated outliers
- Peaks detected at calibrant m/z values (if known) can be extracted and used for downstream calibration (e.g., edgeshift)

## Limitations

- MSWParam performance degrades when signal is heavily overlapped in m/z or retention time; closely-spaced isotopologs may merge into single peaks.
- Direct-injection data (no chromatographic separation) may produce artificially broad or multiple peaks from the same ion if acquisition time is long.
- The algorithm requires tuning of internal thresholds (not exposed in the basic API); default parameters may not generalize across different MS platforms or acquisition modes.
- No built-in gap-filling for samples where peaks fail to detect; downstream processing must handle missing peaks explicitly.

## Evidence

- [other] Run findChromPeaks() with MSWParam to detect chromatographic peaks across all files: "Run findChromPeaks() with MSWParam to detect chromatographic peaks across all files."
- [other] Load FTICR HAM mzML files from Zenodo deposit into an xcms XCMSnExp object: "Load FTICR HAM mzML files from Zenodo deposit doi:10.5281/zenodo.18494293 into an xcms XCMSnExp object."
- [readme] The xcms R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
- [other] perform a chromatographic peak detection in MS level 2 data separately for each individual isolation window using findChromPeaksIsolationWindow(): "perform a chromatographic peak detection in MS level 2 data separately for each individual isolation window. We use the `findChromPeaksIsolationWindow()` function"
