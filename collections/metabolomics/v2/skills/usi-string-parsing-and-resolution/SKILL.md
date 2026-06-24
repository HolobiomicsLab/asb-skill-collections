---
name: usi-string-parsing-and-resolution
description: Use when you have a USI string referencing a spectrum in an online public
  repository (PRIDE, MassIVE, etc.) and need to load its raw spectral data without
  downloading the entire dataset file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils_cq
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# usi-string-parsing-and-resolution

## Summary

Parse and resolve Universal Spectrum Identifier (USI) strings to retrieve raw MS/MS spectrum data (m/z array, intensity array, precursor m/z, charge state, retention time) from online proteomics and metabolomics repositories (PRIDE, MassIVE). This skill bridges USI string syntax to live spectrum objects suitable for downstream processing and annotation.

## When to use

You have a USI string referencing a spectrum in an online public repository (PRIDE, MassIVE, etc.) and need to load its raw spectral data without downloading the entire dataset file. Common scenarios: comparing spectra across repositories, rapid spectrum retrieval for annotation workflows, or integrating live data into interactive analysis notebooks.

## When NOT to use

- USI string points to a private or access-restricted repository without valid authentication credentials.
- Spectrum data is already available locally in mzML or other standard file format; use local file parsing instead.
- Network connectivity is unavailable or the online repository endpoint is down.

## Inputs

- USI string (e.g., 'mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555')
- Internet connectivity to online proteomics repository

## Outputs

- MsmsSpectrum object with populated attributes: title, precursor_mz, charge, mz array, intensity array, retention_time

## How to apply

Parse the USI string to extract the repository accession (e.g., 'mzspec:PXD000561'), dataset/file identifier, and scan number using spectrum_utils' built-in USI resolver. Query the online proteomics resource's USI endpoint to retrieve the resolved spectrum data, including m/z array, intensity array, precursor m/z, charge state, and retention time. Instantiate an MsmsSpectrum object by passing these resolved attributes to the MsmsSpectrum constructor. Verify that all spectral attributes (title, precursor m/z, charge, arrays, retention time) are populated and accessible before proceeding to downstream processing chains such as noise removal, intensity scaling, or fragment annotation.

## Related tools

- **spectrum_utils** (Provides USI resolver, MsmsSpectrum class, and endpoint integration for parsing USI strings and loading spectra from online repositories.) — https://github.com/bittremieux/spectrum_utils
- **Python** (Programming language for executing USI parsing and spectrum object instantiation.)

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum; from spectrum_utils.resolvers import resolve_usi; usi = "mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555"; spectrum = resolve_usi(usi)
```

## Evaluation signals

- MsmsSpectrum object is successfully instantiated with non-null title, precursor_mz, charge, mz array, and intensity array.
- m/z and intensity arrays have matching length and contain only numeric values within physically plausible ranges (m/z > 0, intensity ≥ 0).
- Precursor m/z, charge state, and retention time are consistent with the USI repository metadata.
- Subsequent spectrum processing operations (e.g., set_mz_range, remove_precursor_peak, filter_intensity) execute without AttributeError or data validation failures.
- USI string parsing completes without network timeout or HTTP 404 errors from the repository endpoint.

## Limitations

- USI resolution depends on continuous availability and correct implementation of the online repository's USI endpoint; transient network or API changes may cause failures.
- Only supports repositories that implement the PSI-DEV USI standard; proprietary or non-standard repository formats are not supported.
- Large-scale batch USI resolution may be rate-limited by repository servers; no built-in batching or caching is mentioned in the article.
- Spectrum data retrieved via USI is read-only; local modifications to the MsmsSpectrum object do not persist back to the repository.

## Evidence

- [intro] spectrum_utils implements spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism.: "Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism."
- [other] Parse the USI string and extract repository/file/scan identifiers, then retrieve spectrum data via the USI endpoint, then construct an MsmsSpectrum object.: "Parse the USI string to extract repository accession, file/dataset identifier, and scan number using spectrum_utils' USI resolver. 2. Retrieve the raw spectrum data (m/z array, intensity array,"
- [other] Concrete USI examples from the article's workflow and datasets.: "usi = "mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555""
- [intro] spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.: "spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization."
- [other] Return the populated MsmsSpectrum object with all spectral attributes accessible for subsequent processing chains.: "Return the populated MsmsSpectrum object with all spectral attributes accessible for subsequent processing chains."
