---
name: xcms-data-import-preprocessing
description: Use when you have raw LC-MS or GC-MS data files from a mass spectrometer (in mzML, NetCDF, or mzXML format) and need to detect chromatographic peaks, correct m/z bias via mass calibration (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - xcms
  - MSnbase
  - Spectra
  - MsExperiment
  - BiocParallel
derived_from:
- doi: 10.1021/acs.analchem.5c04338
  title: xcms
evidence_spans:
- The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.
- The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/acs.analchem.5c04338
    title: xcms
  dedup_kept_from: coll_xcms
schema_version: 0.2.0
---

# xcms-data-import-preprocessing

## Summary

Load LC-MS/MS raw data files (mzML, NetCDF, or mzXML) into xcms XCMSnExp objects and apply initial preprocessing including chromatographic peak detection, mass calibration, and retention time filtering. This skill forms the foundation of untargeted metabolomics workflows by converting instrument output into a standardized R object amenable to downstream feature detection and grouping.

## When to use

You have raw LC-MS or GC-MS data files from a mass spectrometer (in mzML, NetCDF, or mzXML format) and need to detect chromatographic peaks, correct m/z bias via mass calibration (e.g., edgeshift method), and subset data to regions of interest before feature grouping or statistical analysis.

## When NOT to use

- Input data are already in feature table format (e.g., aligned peak matrix with m/z and retention time columns); use xcms only when you have raw instrument files requiring peak detection.
- Peak detection has already been performed and you only need to perform feature grouping; skip directly to feature correspondence methods.
- Your workflow requires isolation-window-specific (e.g., SWATH) peak detection in MS/MS data; use findChromPeaksIsolationWindow() instead of the standard findChromPeaks().

## Inputs

- mzML file(s) from FTICR-MS or TOF-MS instrument
- NetCDF or mzXML format raw MS data (alternative formats)
- Calibration reference compound list with expected m/z and retention time (for edgeshift calibration)
- Peak detection parameter object (MSWParam, CentWaveParam, or equivalent)

## Outputs

- XCMSnExp object with detected chromatographic peaks and metadata
- Calibrated m/z values stored within the XCMSnExp object
- Calibration difference plot (raw m/z vs. calibrated m/z difference)
- Filtered XCMSnExp subset (if retention time or m/z filtering applied)

## How to apply

Begin by importing raw MS data files into an XCMSnExp object using the xcms package. Run findChromPeaks() with an appropriate peak detection parameter object (e.g., MSWParam for direct infusion or CentWaveParam for chromatographic separation) to detect peaks across all samples. Apply mass calibration using CalibrantMassParam with method='edgeshift' to correct m/z value bias as a function of raw m/z position; this produces measurable corrections that vary linearly within the calibrant range and by constant shift outside it. Optionally filter the data to specific retention time ranges using filterRt() or m/z ranges using filterMz() to isolate analytes of interest. Visualize calibration corrections by plotting the difference between calibrated and raw m/z values against raw m/z to assess correction magnitude and consistency across the m/z range.

## Related tools

- **xcms** (Core R package for LC-MS data import, chromatographic peak detection, mass calibration (edgeshift method), and retention time filtering; handles mzML/NetCDF file I/O and produces XCMSnExp result objects) — https://github.com/sneumann/xcms
- **MSnbase** (Provides underlying MS data structures and spectra handling used by xcms)
- **Spectra** (New data container supported by xcms version 4+ for flexible spectrum representation and preprocessing)
- **MsExperiment** (Container for multi-sample MS experiments; xcms version 4+ performs preprocessing on MsExperiment objects)
- **BiocParallel** (Enables parallel processing of chromatographic peak detection across multiple files)

## Examples

```
library(xcms); xdata <- readMSData(files=c('sample1.mzML','sample2.mzML'), mode='onDisk'); xdata <- findChromPeaks(xdata, param=MSWParam()); xdata <- calibratemasses(xdata, param=CalibrantMassParam(method='edgeshift')); xdata_filt <- filterRt(xdata, rt=c(100, 900))
```

## Evaluation signals

- XCMSnExp object is successfully created with chromPeaks() returning a matrix of detected peak m/z, retention time, and intensity values
- Mass calibration difference plot shows smooth, monotonic variation in m/z correction across the m/z range, with peaks within calibrant range adjusted via linear interpolation and peaks outside adjusted by constant shift
- Calibrated m/z values lie within expected tolerance (e.g., < 5 ppm error) of reference calibrant compounds; visual inspection confirms correction magnitude decreases towards calibrant m/z region
- filterRt() and filterMz() operations successfully subset the XCMSnExp to the specified ranges with corresponding reduction in detected peak count
- No loss of data integrity: row/column dimensions of peak matrix match sample count; no missing or NaN values in core peak attributes (mz, rt, intensity)

## Limitations

- Peak detection parameter selection (e.g., MSWParam vs. CentWaveParam) is method-dependent and requires prior knowledge of data acquisition mode; inappropriate parameter choice will miss true peaks or generate false positives.
- The edgeshift calibration method assumes availability of internal calibrants; if calibrants are absent or their identities are unknown, calibration will fail or produce unreliable corrections.
- For some samples, chromatographic peaks may not be detected even when signal is present in raw data (e.g., due to low signal-to-noise ratio or peak shape outside the detection model); gap-filling is required post-feature-grouping to recover missing abundances.
- xcms version 3 and earlier use XCMSnExp and older classes; version 4 introduces Spectra and MsExperiment containers with improved performance but requires code migration for legacy workflows.

## Evidence

- [intro] Load and preprocess LC-MS data using xcms: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
- [other] Run findChromPeaks() with MSWParam on direct injection FTICR-MS data: "Run findChromPeaks() with MSWParam to detect chromatographic peaks across all files."
- [other] Apply edgeshift mass calibration method: "apply mass calibration using CalibrantMassParam with method='edgeshift' to correct m/z bias"
- [other] Edgeshift produces variable corrections based on m/z position: "The edgeshift calibration method produces measurable m/z corrections that vary as a function of the raw m/z value, with peaks within the calibrant range adjusted via linear interpolation and peaks"
- [intro] Filter by retention time and m/z range: "We thus filter the DDA data to this retention time range. dda_data <- filterRt(dda_data, rt = c(230, 610))"
- [intro] Gap-filling for missing peaks: "for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated."
- [readme] Version 4 support for Spectra and MsExperiment: "Version 4 adds native support for the Spectra package to `xcms` and allows to perform the pre-processing on `MsExperiment` objects"
