---
name: peak-intensity-threshold-optimization
description: Use when you have loaded raw mass spectrometry spectral data (in MGF, MSP, mzML, or mzXML format) and need to decide which intensity threshold(s) to use for filtering out noise and low-abundance peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - Python
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms
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

# peak-intensity-threshold-optimization

## Summary

This skill optimizes the intensity thresholds used during peak filtering in mass spectrometry data preprocessing to remove low-intensity and irrelevant peaks while preserving spectral information quality. It is essential for ensuring data accuracy and integrity in spectral datasets before downstream similarity comparisons or library curation.

## When to use

Apply this skill when you have loaded raw mass spectrometry spectral data (in MGF, MSP, mzML, or mzXML format) and need to decide which intensity threshold(s) to use for filtering out noise and low-abundance peaks. This is typically the first step after data import and before metadata cleaning or similarity scoring, especially when spectral quality or reproducibility across datasets is a concern.

## When NOT to use

- Input spectra are already pre-processed or from a curated, high-quality library where intensity filtering has been validated.
- The analysis requires preservation of all peaks including noise for specific diagnostic or method validation purposes.
- Peak intensity values are missing, corrupted, or not comparable across spectra (e.g., non-normalized or instrument-specific scales).

## Inputs

- Raw mass spectrometry spectral data (MGF, MSP, mzML, or mzXML format)
- Spectrum collection or list of Spectrum objects
- Peak intensity values (numeric array or dictionary per spectrum)

## Outputs

- Filtered spectrum collection with low-intensity peaks removed
- Spectral data in compatible format (MGF, MSP, mzML, mzXML, or JSON)
- Metadata on threshold applied and peaks removed (count, intensity ranges)

## How to apply

Load spectral data from a common mass spectrometry file format using matchms import functions. Examine the intensity distribution of peaks across the spectral dataset to identify candidates for low-intensity peak removal. Apply matchms peak filtering functions iteratively with different intensity thresholds to remove peaks below the chosen cutoff(s), evaluating the trade-off between noise reduction and information loss. Monitor effects on spectral diversity, peak count per spectrum, and downstream analysis outcomes (e.g., cosine similarity score distributions or library matching performance). Select the threshold that balances data fidelity with signal quality, typically retaining only peaks that contribute meaningfully to spectral characterization while reducing computational burden and improving reproducibility.

## Related tools

- **matchms** (Provides peak filtering functions and spectrum data import/export for applying intensity thresholds to remove low-intensity peaks and ensure data accuracy) — https://github.com/matchms/matchms
- **Python** (Programming language for scripting and automating peak filtering workflows with matchms)

## Examples

```
from matchms import importing; spectra = list(importing.load_from_mgf('raw_spectra.mgf')); from matchms.filtering import remove_peaks_below_threshold; filtered = [remove_peaks_below_threshold(s, intensity_threshold=10) for s in spectra]
```

## Evaluation signals

- Peak count per spectrum decreases after filtering; verify that at least 5–10 peaks remain per spectrum on average to retain spectral information.
- Low-intensity peaks (below the chosen threshold) are completely absent from filtered spectra; spot-check a sample of spectra to confirm threshold enforcement.
- Cosine similarity scores or spectral matching performance (e.g., library hit rates) remain stable or improve after filtering, indicating noise reduction without loss of diagnostic peaks.
- Intensity distribution of remaining peaks shows a clear cutoff at the applied threshold with no stragglers below it.
- Filtered spectra can be successfully exported to the same or compatible file format (MGF, MSP, JSON) without loss or corruption.

## Limitations

- Peak intensity thresholds are often instrument-specific and dataset-dependent; a threshold optimized for one MS/MS dataset may not generalize to another platform or sample type.
- Aggressive filtering (high thresholds) may remove low-abundance but diagnostically important peaks (e.g., rare fragment ions or adducts), reducing spectral specificity.
- matchms provides only basic peak filtering; more sophisticated noise estimation or probabilistic thresholding methods are not built-in and require custom implementations or external tools.
- The skill does not account for relative peak intensity normalization; unnormalized spectra may require per-spectrum normalization before threshold-based filtering is meaningful.

## Evidence

- [other] Apply matchms peak filtering functions to remove low-intensity peaks and irrelevant peaks to ensure data accuracy and integrity.: "Apply matchms peak filtering functions to remove low-intensity peaks and irrelevant peaks to ensure data accuracy and integrity"
- [readme] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
- [other] Load spectral data from a file (MGF, MSP, or mzML format) using matchms import functions.: "Load spectral data from a file (MGF, MSP, or mzML format) using matchms import functions"
- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [readme] It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
