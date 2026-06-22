---
name: peak-intensity-removal-and-thresholding
description: Use when when you have imported raw mass spectrometry spectral data (in formats like mzML, mzXML, msp, MGF, or JSON) and need to clean peak lists before metadata validation, similarity scoring, or library comparison.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pytest
  - matchms
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_2_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-intensity-removal-and-thresholding

## Summary

Remove low-intensity and noise peaks from mass spectrometry data during pre-processing to ensure data accuracy and integrity before downstream analysis. This is a foundational step in the matchms spectral cleaning pipeline that eliminates uninformative peaks while preserving signal peaks.

## When to use

When you have imported raw mass spectrometry spectral data (in formats like mzML, mzXML, msp, MGF, or JSON) and need to clean peak lists before metadata validation, similarity scoring, or library comparison. Apply this skill when raw spectra contain numerous low-abundance peaks or noise that could introduce artifacts into spectral comparisons or consume computational resources unnecessarily.

## When NOT to use

- Input spectra have already undergone vendor-supplied peak picking and denoising—reapplying thresholding may remove reproducible weak signals or fragment ions of diagnostic value.
- The analysis goal requires retention of all detected peaks, including noise, for noise characterization or detection limit studies.
- Peak intensity values are not available or are in an unsupported format that prevents threshold-based filtering.

## Inputs

- Raw mass spectrometry spectral data in supported formats (mzML, mzXML, msp, MGF, JSON)
- Peak intensity values for each m/z feature
- Intensity threshold or noise level parameters

## Outputs

- Filtered peak lists with low-intensity and noise peaks removed
- Intensity-normalized peak data
- Pre-processed spectral data ready for metadata cleaning and validation

## How to apply

Load raw mass spectrometry spectral data using matchms import functions. Apply basic peak filtering operations to remove peaks below intensity thresholds or identified as noise, then normalize remaining peak intensities to a consistent scale. The filtering logic should distinguish between low-intensity noise (which can be removed) and genuine weak signals (which may be biologically relevant depending on the analytical context). Validate that filtered peak lists pass the existing pytest test suite to confirm the filtering logic is correct and that no critical peaks were inadvertently removed. Export the pre-processed spectral data with cleaned peak lists in the original or compatible format for downstream processing.

## Related tools

- **matchms** (Provides basic peak filtering operations, import/export functionality for spectral data formats, and pre-processing toolkit for peak removal and intensity normalization) — https://github.com/matchms/matchms
- **pytest** (Validates filtered peak lists against existing test suite to confirm filtering logic is correct)
- **Python** (Programming language for implementing and executing the peak filtering workflow)

## Examples

```
from matchms.importing_utils import load_from_msp; from matchms.filtering import normalize_intensities, remove_peaks_below_threshold; spectra = load_from_msp('raw_spectra.msp'); cleaned = [normalize_intensities(remove_peaks_below_threshold(s, intensity_threshold=10)) for s in spectra]
```

## Evaluation signals

- Filtered peak lists contain no peaks below the specified intensity threshold.
- Peak intensity values are normalized to a consistent scale (e.g., 0–1 or relative to base peak) across all spectra.
- All filtered spectra pass the existing pytest test suite without new failures.
- Comparison of peak count before and after filtering shows expected reduction in noise peaks while retaining significant peaks.
- Downstream similarity scores computed on filtered spectra are stable and reproducible across multiple runs of the same filtering operation.

## Limitations

- Threshold selection is data- and instrument-dependent; a fixed threshold may over-filter or under-filter spectra from different ionization methods or mass analyzers.
- Peak filtering cannot distinguish between genuine low-abundance diagnostic peaks and noise without additional contextual information (e.g., isotope patterns, known fragment annotations).
- Removal of low-intensity peaks is irreversible; if filtering is too aggressive, weak signals relevant for specialized applications (e.g., isotope tracing, trace metabolite detection) will be lost.
- Matchms basic peak filtering does not address other sources of spectral artifacts such as calibration errors, isotope overlap, or adduct contamination.

## Evidence

- [other] Apply basic peak filtering operations including peak removal (e.g., low-intensity or noise peaks) and peak intensity normalization to ensure data accuracy and integrity.: "Apply basic peak filtering operations including peak removal (e.g., low-intensity or noise peaks) and peak intensity normalization to ensure data accuracy and integrity"
- [readme] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
- [other] Load raw mass spectrometry spectral data in supported formats (mzML, mzXML, msp, MGF, JSON) using matchms import functionality.: "Load raw mass spectrometry spectral data in supported formats (mzML, mzXML, msp, MGF, JSON) using matchms import functionality"
- [other] Validate filtered peak lists pass existing pytest test suite to confirm filtering logic is correct.: "Validate filtered peak lists pass existing pytest test suite to confirm filtering logic is correct"
- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
