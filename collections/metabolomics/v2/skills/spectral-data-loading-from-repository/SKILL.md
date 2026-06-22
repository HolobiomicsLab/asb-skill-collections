---
name: spectral-data-loading-from-repository
description: Use when when you need to retrieve a specific MS/MS spectrum from a public proteomics repository (PRIDE, MassIVE, PeptideAtlas) by its USI string for annotation, visualization, or comparative analysis, rather than working with locally stored mzML/mzXML files or already-loaded spectrum objects.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  - NumPy
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-data-loading-from-repository

## Summary

Load tandem mass spectrometry (MS/MS) spectra from online proteomics and metabolomics repositories using Universal Spectrum Identifier (USI) strings, resolving repository accessions, file identifiers, and scan numbers to retrieve raw spectral data (m/z, intensity, precursor m/z, charge state, retention time) and instantiate MsmsSpectrum objects for downstream processing.

## When to use

When you need to retrieve a specific MS/MS spectrum from a public proteomics repository (PRIDE, MassIVE, PeptideAtlas) by its USI string for annotation, visualization, or comparative analysis, rather than working with locally stored mzML/mzXML files or already-loaded spectrum objects.

## When NOT to use

- Input spectra are already loaded locally as mzML/mzXML files or pre-instantiated MsmsSpectrum objects — use local file I/O instead.
- USI string is malformed or specifies a dataset that no longer exists or has restricted access.
- Batch loading of hundreds or thousands of spectra from a repository — consider downloading the raw dataset files directly for efficiency.

## Inputs

- USI string (e.g., 'mzspec:MSV000082283:f07074:scan:5475')
- Online proteomics repository (PRIDE, MassIVE, PeptideAtlas)

## Outputs

- MsmsSpectrum object with populated attributes (title, precursor m/z, charge, m/z array, intensity array, retention time)

## How to apply

Parse the USI string (e.g., 'mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555') using spectrum_utils' USI resolver to extract the repository accession, dataset/file identifier, and scan number. Query the online proteomics resource endpoint via the USI mechanism to retrieve the raw spectrum data including m/z array, intensity array, precursor m/z, charge state, and retention time. Pass the resolved spectral attributes to the MsmsSpectrum constructor to instantiate a fully populated spectrum object. Verify that all required fields (title, precursor m/z, charge, m/z and intensity arrays) are accessible and non-empty before proceeding to processing steps such as mass range filtering, noise removal, or annotation.

## Related tools

- **spectrum_utils** (Provides USI resolution, spectral data retrieval from online repositories, and MsmsSpectrum instantiation.) — https://github.com/bittremieux/spectrum_utils
- **Python** (Core language for implementing the spectrum loading workflow.)
- **NumPy** (Efficient array operations for storing and manipulating m/z and intensity arrays.) — https://www.numpy.org/

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum; from spectrum_utils.utils import get_spectrum; usi = 'mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555'; spectrum = get_spectrum(usi)
```

## Evaluation signals

- MsmsSpectrum object is successfully instantiated with non-null title, precursor_mz, charge, mz, and intensity attributes.
- m/z and intensity arrays have equal length and contain numeric values; m/z values are strictly increasing.
- Precursor m/z value matches the expected range for the specified ion type (e.g., singly to multiply charged ions).
- Retention time (if present in the repository) is a non-negative numeric value in seconds or minutes.
- Spectrum object can be serialized and passed to downstream processing functions (e.g., filter_intensity, annotate_proforma) without type errors.

## Limitations

- USI resolution depends on network connectivity and repository endpoint availability; requests may fail or timeout if the repository is offline or throttles API traffic.
- Not all scan numbers or dataset accessions are guaranteed to exist or be publicly accessible; access may be restricted or data may have been withdrawn.
- Spectrum metadata (e.g., retention time, charge state) may be incomplete or absent in some repositories, resulting in partial MsmsSpectrum objects.
- Large or complex spectra may consume significant memory; batch loading without filtering can exhaust available RAM.

## Evidence

- [other] Parse the USI string to extract repository accession, file/dataset identifier, and scan number using spectrum_utils' USI resolver.: "Parse the USI string to extract repository accession, file/dataset identifier, and scan number using spectrum_utils' USI resolver."
- [other] Retrieve the raw spectrum data (m/z array, intensity array, precursor m/z, charge state, retention time) from the online proteomics resource via the USI endpoint.: "Retrieve the raw spectrum data (m/z array, intensity array, precursor m/z, charge state, retention time) from the online proteomics resource (PRIDE, MassIVE, or equivalent) via the USI endpoint."
- [other] Instantiate an MsmsSpectrum object by passing the resolved spectrum data to the MsmsSpectrum constructor.: "Instantiate an MsmsSpectrum object by passing the resolved spectrum data (title, precursor m/z, charge, m/z array, intensity array, retention time) to the MsmsSpectrum constructor."
- [intro] Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism.: "Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism."
- [other] Load a spectrum from an online data resource by its Universal Spectrum Identifier (USI): "Load a spectrum from an online data resource by its Universal Spectrum Identifier (USI)"
