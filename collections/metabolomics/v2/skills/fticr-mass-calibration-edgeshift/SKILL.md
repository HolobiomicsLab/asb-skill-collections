---
name: fticr-mass-calibration-edgeshift
description: Use when you have FTICR-MS direct injection (mzML) data with identified
  chromatographic peaks and need to correct systematic m/z bias.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - xcms
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
- doi: 10.5281/zenodo.18494293
  title: ''
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
  - 10.5281/zenodo.18494293
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# FTICR Mass Calibration with Edgeshift

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply edgeshift calibration to correct m/z measurement bias in FTICR-MS direct injection data, where peaks within the calibrant range are adjusted via linear interpolation and peaks outside are corrected by constant shift factors. This skill quantifies and visualizes the magnitude of m/z corrections across the measured mass range.

## When to use

Use this skill when you have FTICR-MS direct injection (mzML) data with identified chromatographic peaks and need to correct systematic m/z bias. The edgeshift method is appropriate when you have calibrant peaks at known m/z values distributed across your mass range and want to measure how m/z measurement error varies as a function of raw m/z, particularly to distinguish between linear drift and edge effects.

## When NOT to use

- Input data is already calibrated or comes from instruments with built-in mass correction (e.g., internal lock mass calibration already applied).
- No reliable calibrant peaks are available or calibrants do not span the m/z range of interest.
- The m/z bias is not systematic with respect to m/z value (e.g., random noise rather than drift or edge effect).

## Inputs

- mzML files from FTICR-MS direct injection acquisition
- XCMSnExp object with detected chromatographic peaks (output of findChromPeaks with MSWParam)
- Known calibrant m/z values with their expected masses

## Outputs

- Mass-calibrated XCMSnExp object with corrected m/z values
- Calibration difference plot (raw m/z vs. calibration correction magnitude)
- Quantified m/z correction values as a function of raw m/z

## How to apply

Load mzML files into an xcms XCMSnExp object and perform chromatographic peak detection using findChromPeaks() with MSWParam. For the target mzML file, apply mass calibration via CalibrantMassParam with method='edgeshift', specifying reference calibrant m/z values. The edgeshift algorithm will interpolate corrections for peaks within the calibrant range using linear regression, and apply constant shift factors for peaks outside this range. Generate a calibration difference plot by calculating the difference between calibrated and raw m/z values and plotting against raw m/z to visualize where and how corrections vary across the mass spectrum.

## Related tools

- **xcms** (Peak detection (findChromPeaks with MSWParam), mass calibration (CalibrantMassParam with edgeshift method), and result container for calibrated m/z values) — https://github.com/sneumann/xcms

## Examples

```
library(xcms); ham_data <- readMzmlFiles('path/to/mzML/'); xcms_obj <- findChromPeaks(ham_data, MSWParam()); cal_obj <- calibrateMass(xcms_obj[1], CalibrantMassParam(calibrants = data.frame(mz = c(112.0, 256.1, 512.2), expected_mz = c(112.0, 256.1, 512.2)), method = 'edgeshift')); plot(chromPeaks(xcms_obj[1])[, 'mz'], calibrateMass(xcms_obj[1], CalibrantMassParam(method='edgeshift'))[, 'mz'] - chromPeaks(xcms_obj[1])[, 'mz'])
```

## Evaluation signals

- Calibration difference plot shows a systematic trend (non-random pattern) of m/z corrections as a function of raw m/z, confirming edgeshift method detected measurable bias.
- Peaks within the calibrant range exhibit corrections following a linear interpolation pattern; peaks outside exhibit constant shift offsets distinct from interpolated region.
- Magnitude of m/z corrections varies visibly across the m/z range (not uniform), validating that the edgeshift method captured drift or edge effects rather than global constant shift.
- Calibrated m/z values for calibrant peaks match their expected reference masses within specified tolerance (typically <5 ppm for FTICR).
- Comparison of raw vs. calibrated m/z difference plots shows the post-calibration scatter or bias is reduced relative to pre-calibration, indicating successful correction.

## Limitations

- Edgeshift calibration assumes a linear relationship between raw m/z and correction within the calibrant range; non-linear or multi-modal mass bias may not be fully captured.
- Peaks outside the calibrant m/z range are corrected by constant shift factors, which may not be accurate if the true bias function extends non-linearly beyond the calibrant bounds.
- Performance depends on the number, distribution, and accuracy of calibrant peaks; sparse or unevenly distributed calibrants may yield less reliable interpolation.
- The method is designed for direct injection (static, non-chromatographic) FTICR-MS; applicability to LC-FTICR workflows where m/z bias might vary with chromatographic conditions is not established in the source material.

## Evidence

- [other] Does the 'edgeshift' calibration method successfully correct m/z values of identified peaks in direct injection MS data, and can the magnitude of these corrections be quantified across the m/z range?: "Does the 'edgeshift' calibration method successfully correct m/z values of identified peaks in direct injection MS data, and can the magnitude of these corrections be quantified across the m/z range?"
- [other] The edgeshift calibration method produces measurable m/z corrections that vary as a function of the raw m/z value, with peaks within the calibrant range adjusted via linear interpolation and peaks outside adjusted by constant shift factors, and these differences can be visualized by plotting the difference between calibrated and raw m/z values against raw m/z.: "The edgeshift calibration method produces measurable m/z corrections that vary as a function of the raw m/z value, with peaks within the calibrant range adjusted via linear interpolation and peaks"
- [other] Load FTICR HAM mzML files from Zenodo deposit doi:10.5281/zenodo.18494293 into an xcms XCMSnExp object. 2. Run findChromPeaks() with MSWParam to detect chromatographic peaks across all files. 3. Isolate the first mzML file and apply mass calibration using CalibrantMassParam with method='edgeshift' to correct m/z bias.: "Load FTICR HAM mzML files from Zenodo deposit doi:10.5281/zenodo.18494293 into an xcms XCMSnExp object. 2. Run findChromPeaks() with MSWParam to detect chromatographic peaks across all files. 3."
- [readme] The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
