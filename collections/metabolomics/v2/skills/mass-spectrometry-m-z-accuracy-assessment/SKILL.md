---
name: mass-spectrometry-m-z-accuracy-assessment
description: Use when when you have detected peaks in a direct injection FTICR-MS mzML file (or similar high-resolution MS format) and need to assess whether m/z measurements are accurate and consistent across the m/z range.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - xcms
  - Spectra
  techniques:
  - LC-MS
  - GC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans: []
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-m-z-accuracy-assessment

## Summary

Quantify and visualize m/z measurement accuracy before and after calibration in FTICR-MS or other high-resolution direct injection MS data by comparing observed m/z values against expected calibrant masses. This skill reveals systematic m/z bias patterns and validates the effectiveness of calibration corrections across the m/z range.

## When to use

When you have detected peaks in a direct injection FTICR-MS mzML file (or similar high-resolution MS format) and need to assess whether m/z measurements are accurate and consistent across the m/z range. This is especially relevant after applying mass calibration methods like edgeshift, where you want to quantify how much correction was applied and whether peaks within vs. outside the calibrant range received different treatment.

## When NOT to use

- Input is already a feature table with consensus m/z values aggregated across multiple samples; assess calibration on raw spectral data instead.
- You are working with low-resolution MS data (e.g., Orbitrap with <50 ppm intrinsic error) where m/z bias patterns may be negligible or instrument-dependent.
- No calibrant peaks or reference masses are available in the dataset; calibration and accuracy assessment require known mass anchors.

## Inputs

- mzML file(s) from direct injection FTICR-MS (or equivalent high-resolution MS instrument)
- XCMSnExp object after chromatographic peak detection with findChromPeaks()
- List of calibrant masses with expected m/z values

## Outputs

- Calibration difference plot (raw m/z vs. calibration correction in Da or ppm)
- Numeric vector of m/z corrections per detected peak
- Calibrated m/z values for all detected peaks

## How to apply

Load the mzML file into an xcms XCMSnExp object and run findChromPeaks() with appropriate peak detection parameters (e.g., MSWParam). Then apply mass calibration using CalibrantMassParam with method='edgeshift' to correct systematic m/z bias. Generate a calibration difference plot by computing the difference between calibrated m/z and raw m/z values for all detected peaks, plotting this difference against raw m/z. Peaks within the calibrant mass range will show linear interpolation-based corrections while those outside show constant shift factors. Inspect the plot to verify that corrections diminish at edges and that the calibration method successfully reduced m/z measurement error.

## Related tools

- **xcms** (Load mzML files, detect chromatographic peaks with findChromPeaks(), apply mass calibration with CalibrantMassParam, and retrieve calibrated m/z values) — https://github.com/sneumann/xcms
- **Spectra** (Alternative container for spectral data that integrates with xcms version 4 for flexible m/z and intensity access)

## Examples

```
library(xcms); ham <- readMSData('ham_sample.mzML', mode='onDisk'); ham_peaks <- findChromPeaks(ham, param=MSWParam()); calibrated <- calibrateMass(ham_peaks[1], method='edgeshift', calibrants=c(112.0524, 524.2649)); plot(chromPeaks(calibrated)[,'mz'] - chromPeaks(ham_peaks[1])[,'mz'] ~ chromPeaks(ham_peaks[1])[,'mz'])
```

## Evaluation signals

- The calibration difference plot shows a clear functional relationship between raw m/z and correction magnitude; peaks cluster around expected calibration curves (linear in calibrant range, constant outside).
- For peaks within the calibrant mass range, corrections follow linear interpolation; for peaks outside, corrections are constant (no extrapolation beyond calibrant edges).
- The magnitude of m/z corrections is quantified in Da or ppm and varies monotonically or smoothly across the m/z range (no erratic jumps).
- After calibration, the standard deviation (or RMS) of m/z error relative to expected calibrant masses is reduced compared to uncalibrated data.
- Peaks at the edges of the calibrant mass range show smaller corrections than interior peaks, consistent with interpolation vs. constant shift behavior.

## Limitations

- Edgeshift calibration only interpolates within the calibrant m/z range and applies constant shifts outside; m/z accuracy degrades for peaks far from calibrant masses.
- Calibration accuracy depends on the quality and number of calibrant peaks detected; sparse or noisy calibrants introduce errors in both linear fit and constant shift factors.
- Direct injection MS data lacks chromatographic separation, so peak overlap and co-elution can degrade peak detection and inflate m/z uncertainty.
- The method assumes systematic m/z bias that is consistent within a file; highly variable or instrument-state-dependent errors may not be corrected by a single linear or constant model.

## Evidence

- [other] Does the 'edgeshift' calibration method successfully correct m/z values of identified peaks in direct injection MS data, and can the magnitude of these corrections be quantified across the m/z range?: "Does the 'edgeshift' calibration method successfully correct m/z values of identified peaks in direct injection MS data, and can the magnitude of these corrections be quantified"
- [other] The edgeshift calibration method produces measurable m/z corrections that vary as a function of the raw m/z value, with peaks within the calibrant range adjusted via linear interpolation and peaks outside adjusted by constant shift factors, and these differences can be visualized by plotting the difference between calibrated and raw m/z values against raw m/z.: "The edgeshift calibration method produces measurable m/z corrections that vary as a function of the raw m/z value, with peaks within the calibrant range adjusted via linear interpolation and peaks"
- [other] Run findChromPeaks() with MSWParam to detect chromatographic peaks across all files. 3. Isolate the first mzML file and apply mass calibration using CalibrantMassParam with method='edgeshift' to correct m/z bias. 4. Generate a calibration difference plot comparing observed vs. expected m/z before and after calibration for the first file.: "Run findChromPeaks() with MSWParam to detect chromatographic peaks. Isolate the first mzML file and apply mass calibration using CalibrantMassParam with method='edgeshift' to correct m/z bias."
- [readme] The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
