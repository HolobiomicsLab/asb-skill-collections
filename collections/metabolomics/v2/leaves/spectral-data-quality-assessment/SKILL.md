---
name: spectral-data-quality-assessment
description: Use when importing raw or public mass spectrometry spectral data in formats
  such as MGF, MSP, or mzML that may contain incomplete metadata (e.g., missing instrument
  type, precursor m/z, retention time), low-intensity noise peaks, or spectra with
  invalid or inconsistent metadata fields.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3407
  tools:
  - matchms
  - pytest
  - Python
  - PyTorch
  - read_raw_spectra
  - Python 3.12
  - RDKit (inferred)
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
- doi: 10.1021/acs.analchem.5c02655
  title: ''
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing,
  cleaning, and comparing mass spectrometry data
- make sure the existing tests still work by running ``pytest``
- Python：3.12
- PyTorch：2.6.0 + CUDA 12.4
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  - build: coll_specembedding_cq
    doi: 10.1021/acs.analchem.5c02655
    title: SpecEmbedding
  dedup_kept_from: coll_matchms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  - 10.1021/acs.analchem.5c02655
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-data-quality-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assessment and remediation of mass spectrometry spectral data quality through metadata cleaning, validation, and peak filtering to ensure data accuracy and integrity before downstream analysis or comparison. This skill applies matchms' array of cleaning and filtering tools to standardize spectral datasets and remove spectra or peaks that fail critical quality thresholds.

## When to use

Apply this skill when importing raw or public mass spectrometry spectral data in formats such as MGF, MSP, or mzML that may contain incomplete metadata (e.g., missing instrument type, precursor m/z, retention time), low-intensity noise peaks, or spectra with invalid or inconsistent metadata fields. Use it as an upstream step before spectral similarity comparisons or any downstream analysis that assumes clean, standardized metadata and peak integrity.

## When NOT to use

- Input spectra have already been cleaned and validated by a trusted upstream source or preprocessing pipeline.
- Analysis requires retention of all original peak intensity values or metadata, including low-confidence or borderline entries, for later manual review or sensitivity analysis.
- The spectral dataset is very small (< 10 spectra) and manual inspection is more practical than automated filtering.

## Inputs

- Mass spectrometry spectral data files (MGF, MSP, mzML, or mzXML format)
- Raw or public spectral datasets with potentially incomplete or inconsistent metadata
- Spectrum objects with peak lists and metadata fields

## Outputs

- Cleaned and validated spectrum collection with standardized metadata
- Filtered spectral data file (MGF or JSON format)
- Quality assessment report (implicit: spectra and peaks removed, thresholds applied)

## How to apply

Load spectral data from a file using matchms import functions; then sequentially apply matchms metadata cleaning filters to standardize spectrum metadata fields (instrument type, precursor m/z, retention time, etc.) and matchms validation filters to remove spectra with missing or invalid critical metadata; simultaneously or afterwards, apply matchms peak filtering functions to remove low-intensity peaks and irrelevant peaks below user-defined thresholds. Export the cleaned spectrum collection to an output file (MGF or JSON format). Verify the workflow using pytest or manual inspection to confirm that filter logic and data integrity constraints have been met and that no critical spectra or metadata have been inadvertently lost.

## Related tools

- **matchms** (Provides metadata cleaning filters, validation filters, and peak filtering functions to standardize and filter spectral datasets) — https://github.com/matchms/matchms
- **Python** (Programming language for invoking matchms import, filtering, and export functions)
- **pytest** (Testing framework to verify filter logic and data integrity constraints in the cleaning workflow)

## Examples

```
from matchms import importing; spectra = list(importing.load_from_mgf('raw_spectra.mgf')); from matchms.filtering import normalize_intensities, default_filters; spectra = [default_filters(s) for s in spectra]; spectra = [normalize_intensities(s) for s in spectra]; from matchms import exporting; exporting.save_as_mgf(spectra, 'cleaned_spectra.mgf')
```

## Evaluation signals

- All retained spectra have valid and standardized metadata fields (no missing critical values such as precursor m/z or instrument type).
- Peak lists contain only peaks above the applied intensity threshold; low-intensity noise has been removed.
- The output file (MGF or JSON) is well-formed and can be re-imported without errors.
- pytest validation tests pass, confirming that metadata constraints and peak filtering logic have been correctly applied.
- Comparison of input vs. output spectrum counts and peak counts shows expected reduction due to filtering, with no unexpected loss of data.

## Limitations

- Matchms provides basic peak filtering and metadata cleaning; users must define or select specific threshold values (intensity cutoff, metadata requirements) appropriate for their dataset and analysis goal.
- Overly aggressive filtering (e.g., very high intensity thresholds or strict metadata requirements) may remove valid spectra or peaks and reduce dataset size significantly.
- The skill assumes that spectral file format is one of the supported formats (MGF, MSP, mzML, mzXML); other proprietary or non-standard formats may require custom parsers.

## Evidence

- [other] Matchms provides basic peak filtering tools as part of its data processing workflow to ensure data accuracy and integrity in spectral datasets.: "Matchms provides basic peak filtering tools as part of its data processing workflow to ensure data accuracy and integrity in spectral datasets"
- [other] Apply matchms peak filtering functions to remove low-intensity peaks and irrelevant peaks to ensure data accuracy and integrity.: "Apply matchms peak filtering functions to remove low-intensity peaks and irrelevant peaks to ensure data accuracy and integrity"
- [other] Matchms provides an array of tools for metadata cleaning and validation that work alongside basic peak filtering to ensure data accuracy and integrity of mass spectrometry spectral data.: "Matchms provides an array of tools for metadata cleaning and validation that work alongside basic peak filtering to ensure data accuracy and integrity of mass spectrometry spectral data"
- [other] Apply matchms metadata cleaning filters to standardize and validate spectrum metadata fields (e.g., instrument type, precursor m/z, retention time).: "Apply matchms metadata cleaning filters to standardize and validate spectrum metadata fields (e.g., instrument type, precursor m/z, retention time)"
- [intro] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
