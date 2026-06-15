---
name: metabolomics-data-structure-handling
description: Use when when beginning an LC-MS/MS metabolomics analysis pipeline and you have preprocessed xcms result objects (XcmsExperiment or legacy xcmsSet) that need to be loaded into memory, validated for integrity, and prepared for feature grouping (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - xcms
  - MsExperiment
  - Spectra
  - MSnbase
derived_from:
- doi: 10.1021/acs.analchem.5c04338
  title: xcms
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
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

# metabolomics-data-structure-handling

## Summary

Load, validate, and manipulate LC-MS metabolomics data using modern Bioconductor container objects (XcmsExperiment, MsExperiment, Spectra) to enable seamless integration with downstream feature grouping, annotation, and spectral matching workflows. This skill bridges raw mass spectrometry data and structured analysis-ready objects.

## When to use

When beginning an LC-MS/MS metabolomics analysis pipeline and you have preprocessed xcms result objects (XcmsExperiment or legacy xcmsSet) that need to be loaded into memory, validated for integrity, and prepared for feature grouping (e.g., SimilarRtimeParam-based grouping) or spectral analysis. Use this skill at the start of compounding workflows or when integrating chromatographic peaks with MS2 spectra for annotation.

## When NOT to use

- Input data has not yet undergone chromatographic peak detection (findChromPeaks); load and preprocess raw data first using xcms peak detection.
- You are working with already-grouped feature tables or consensus spectra; this skill is for initial object assembly, not refined outputs.
- Data is in legacy non-Bioconductor formats (e.g., proprietary vendor software output); convert to mzML or xcms objects first.

## Inputs

- xcmsSet or XcmsExperiment object (preprocessed chromatographic peaks and feature table)
- Raw mzML/mzXML/NetCDF LC-MS data files (optional, if re-loading)
- Chromatographic peak parameters (retention time, m/z, intensity matrix across samples)
- MS2 spectrum metadata and intensities (if performing spectral grouping)

## Outputs

- Loaded and validated XcmsExperiment or MsExperiment object
- Extracted Spectra object (for MS2 data associated with chromatographic peaks)
- Feature table (m/z, retention time, abundance matrix) accessible via featureValues()
- Metadata slots (sample phenotypes, acquisition parameters) accessible via pData() or metadata()

## How to apply

Load the preprocessed faahKO xcms result object or equivalent XcmsExperiment/xcmsSet using xcms package functions. Verify the object contains valid chromatographic peaks, retention times, m/z values, and sample metadata by inspecting the structure using standard Bioconductor accessors (chromPeaks(), featureValues(), etc.). If working with MS2 data, extract associated spectra using chromPeakSpectra() to create a Spectra object. For multi-modal analyses, combine Spectra and xcms results into an MsExperiment object. This structured representation ensures compatibility with MsFeatures grouping functions (SimilarRtimeParam, AbundanceSimilarityParam, EicSimilarityParam) and downstream spectral matching via compareSpectra() or GNPS library search.

## Related tools

- **xcms** (Provides XcmsExperiment/xcmsSet container and accessor methods (chromPeaks, featureValues, chromPeakSpectra) for loading and validating preprocessed LC-MS data) — https://github.com/sneumann/xcms
- **MsExperiment** (Container class for integrating Spectra, xcms results, and sample metadata into a unified multi-modal metabolomics object)
- **Spectra** (In-memory or file-backed representation of MS spectra (MS1 and MS2) extracted from chromatographic peaks or raw data)
- **MsFeatures** (Consumes XcmsExperiment/MsExperiment objects and applies grouping parameters (SimilarRtimeParam, AbundanceSimilarityParam, EicSimilarityParam) to group related features)
- **MSnbase** (Provides base classes and validation framework underlying xcms and Spectra objects)

## Examples

```
library(xcms); data(faahKO); data <- faahKO; xset <- groupChromPeaks(xset, param=PeakDensityParam(sampleGroups=rep(1:2, each=4))); feats <- featureValues(xset); spectra <- chromPeakSpectra(xset)
```

## Evaluation signals

- Loaded XcmsExperiment/MsExperiment object passes validation (no missing or inconsistent chromPeaks, featureValues dimensions match sample count, retention times are numeric and sorted)
- chromPeaks() accessor returns a matrix with rows = detected peaks, columns including mz, mzmin, mzmax, rt, rtmin, rtmax, into, intb, maxo, sample
- featureValues() returns a numeric matrix with rows = features (unique m/z–rt combinations), columns = samples, no NaN in positions corresponding to detected peaks
- Extracted Spectra object (from chromPeakSpectra) contains MS level, m/z values, intensities, and links to parent chromatographic peak indices
- Sample metadata (pData() or metadata()) is non-empty and matches the number of input data files

## Limitations

- Data objects loaded must already be preprocessed (peaks detected, aligned); this skill does not perform peak detection or correspondence — use xcms::findChromPeaks() and groupChromPeaks() first.
- Legacy xcmsSet objects lack some accessors and metadata slots present in newer XcmsExperiment; consider upgrading to XcmsExperiment for compatibility with MsFeatures and other RforMassSpectrometry packages.
- For samples with missing chromatographic peak detections, gap-filling must be applied separately (xcms::fillChromPeaks()) to recover signal from the m/z–retention time range; this skill assumes filled or raw peak tables are provided.
- Very large datasets (>1000 samples or >10,000 features) may require file-backed storage (on-disk Spectra) rather than in-memory objects to manage RAM efficiently.

## Evidence

- [readme] Version 4 adds native support for the Spectra package to xcms and allows to perform the pre-processing on MsExperiment objects: "Version 4 adds native support for the Spectra package to `xcms` and allows to perform the pre-processing on `MsExperiment` objects (from the MsExperiment"
- [readme] The new supported data containers (Spectra, MsExperiment and XcmsExperiment) allow more flexible analyses and seamless future extensions: "The new supported data containers (`Spectra`, `MsExperiment` and `XcmsExperiment`) allow more flexible analyses and seamless future extensions to additional types of data"
- [other] Load the preprocessed faahKO xcms result object (XcmsExperiment or xcmsSet) and apply the groupFeatures() function with SimilarRtimeParam: "Load the preprocessed faahKO xcms result object (XcmsExperiment or xcmsSet). 2. Apply the groupFeatures() function with SimilarRtimeParam(window=20)"
- [intro] Spectra for identified chromatographic peaks can be extracted with the chromPeakSpectra() method: "Spectra for identified chromatographic peaks can be extracted with the `chromPeakSpectra()` method."
- [intro] for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated: "for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated."
- [readme] These changes will also allow easier integration of xcms with other R packages such as MsFeatures or MetaboAnnotation: "These changes will also allow easier integration of `xcms` with other R packages such as MsFeatures or MetaboAnnotation"
