---
name: chromatographic-peak-detection-wavelet
description: Use when you have loaded raw LC-MS or direct-injection FTICR-MS data (in mzML or netCDF format) into an XCMSnExp object and need to identify individual chromatographic peaks before feature grouping.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MsDataHub
  - MassSpecWavelet
  - xcms
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- library(MsDataHub)
- '`r Biocpkg("xcms")` uses functionality from the *MassSpecWavelet* package to identify such peaks'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms_cq
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms_cq
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

# chromatographic-peak-detection-wavelet

## Summary

Detect chromatographic peaks in mass spectrometry data using wavelet-based peak finding (MSWParam) with configurable scales, noise parameters, and signal-to-noise thresholds. This skill applies the MassSpecWavelet algorithm via xcms to identify peaks across direct-injection or LC-MS spectra, producing a chromPeaks matrix suitable for downstream feature alignment and quantification.

## When to use

Apply this skill when you have loaded raw LC-MS or direct-injection FTICR-MS data (in mzML or netCDF format) into an XCMSnExp object and need to identify individual chromatographic peaks before feature grouping. Use wavelet-based detection when peaks have variable widths or when you require fine control over scale-dependent noise filtering (e.g., HAM004/HAM005 direct-injection spectra with known SNR characteristics).

## When NOT to use

- Input is already a feature table or has been pre-processed with centWave or other peak detection — avoid re-running wavelet detection to prevent double-filtering artifacts.
- Data exhibits very narrow peaks (<1 m/z unit width) or extremely broad peaks (>100 scans) — wavelet scales c(1, 4, 9) may not span the full peak width range; consider centWave or adjust scales.
- Spectra have extremely low SNR globally (mean SNR < 3) — MSWParam with snthresh=10 will likely produce few or no peaks; preprocess or relax the threshold only after manual inspection of raw data.

## Inputs

- XCMSnExp object (created via readMSData() from mzML or netCDF files)
- Raw LC-MS or direct-injection FTICR-MS spectra in mzML format

## Outputs

- chromPeaks matrix with detected peaks (columns: mz, mzmin, mzmax, rt, rtmin, rtmax, into, intb, maxo, sample, and SNR)
- Peak detection metadata (scales used, noise parameters applied, SNR method)

## How to apply

Load raw MS data files into an XCMSnExp object using readMSData() in on-disk mode. Configure MSWParam with wavelet scales (typically c(1, 4, 9) for multi-scale analysis), set nearbyPeak=TRUE to merge nearby detections, define a noise window size (e.g., 500 for direct injection), select SNR.method='data.mean' to estimate noise from the full spectrum mean, and set a signal-to-noise threshold (snthresh=10 or higher depending on data quality and desired specificity). Execute findChromPeaks() on the XCMSnExp with the configured MSWParam to apply the MassSpecWavelet algorithm across all samples. Validate the resulting chromPeaks matrix: check that detected peaks span the expected m/z and retention time ranges, verify that peak count and intensity distributions match experimental expectations, and confirm SNR values exceed the specified threshold.

## Related tools

- **xcms** (Provides XCMSnExp data container, readMSData() for file loading, MSWParam configuration class, and findChromPeaks() dispatcher for wavelet-based peak detection) — https://github.com/sneumann/xcms
- **MassSpecWavelet** (Implements the underlying wavelet-based peak detection algorithm used by xcms MSWParam)
- **MsDataHub** (Provides remote access to example MS data files (HAM004, HAM005) in mzML format for demonstration)

## Examples

```
findChromPeaks(xmse, param = MSWParam(scales = c(1, 4, 9), nearbyPeak = TRUE, winSize.noise = 500, SNR.method = 'data.mean', snthresh = 10))
```

## Evaluation signals

- chromPeaks matrix contains one or more rows with mz, rt, into, intb, maxo, and SNR columns populated; no NaN or Inf values in numeric columns.
- Peak SNR values (chromPeaks[, 'SNR']) are all ≥ snthresh (e.g., ≥ 10 for snthresh=10); peaks below threshold should not appear in the matrix.
- Detected peak m/z values span the expected mass range for the experiment; retention times (rt column) fall within the acquisition window.
- Peak count per sample is consistent with visual inspection of the total ion chromatogram and expected compound complexity for the sample type.
- Intensity distributions (into and maxo columns) show expected sample-to-sample or replicate-to-replicate correlation when peaks represent the same compounds.

## Limitations

- Wavelet scales c(1, 4, 9) are hardcoded in many workflows; peaks with very narrow or broad peak widths may not be optimally detected — manual scale tuning is often required.
- SNR threshold (snthresh=10) assumes data.mean method for noise estimation; this can overestimate noise in spectra with sparse signals, leading to false negatives.
- Direct-injection data (HAM004/HAM005) lacks chromatographic separation, so all peaks appear at the same retention time; the algorithm still detects them but downstream feature grouping must account for rt-free coelution.
- No built-in filtering for isotope peaks or adducts; the chromPeaks matrix includes all wavelet-detected features, and isotope removal or adduct annotation must be performed in subsequent steps.
- The nearbyPeak=TRUE parameter may merge separate peaks with similar m/z if they occur within the algorithm's merging window; inspect individual peak boundaries in raw data when in doubt.

## Evidence

- [other] MSWParam peak detection uses wavelet scales of 1, 4, and 9 with nearbyPeak=TRUE, a noise window size of 500, data mean signal-to-noise ratio method, and signal-to-noise threshold of 10: "MSWParam peak detection uses wavelet scales of 1, 4, and 9 with nearbyPeak=TRUE, a noise window size of 500, data mean signal-to-noise ratio method, and signal-to-noise threshold of 10 to identify"
- [other] Load the HAM004 and HAM005 mzML files from MsDataHub using readMSData() in xcms with on-disk mode to create an XCMSnExp object. Configure MSWParam with scales c(1,4,9), nearbyPeak=TRUE, winSize.noise=500, SNR.method='data.mean', and snthresh=10. Execute findChromPeaks() on the XCMSnExp object: "Load the HAM004 and HAM005 mzML files from MsDataHub using readMSData() in xcms with on-disk mode to create an XCMSnExp object. 2. Configure MSWParam with scales c(1,4,9), nearbyPeak=TRUE,"
- [intro] xcms uses functionality from the MassSpecWavelet package to identify such peaks: "xcms uses functionality from the *MassSpecWavelet* package to identify such peaks"
- [readme] The xcms R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
