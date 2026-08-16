---
name: msms-spectrum-object-instantiation
description: Use when when you have successfully resolved a USI string to extract
  raw spectrum data from an online proteomics/metabolomics repository (PRIDE, MassIVE,
  etc.) and need to construct a spectrum object that exposes spectrum data as Python
  attributes and methods for downstream processing (filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spectrum_utils
  - Python
  techniques:
  - mass-spectrometry
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

# msms-spectrum-object-instantiation

## Summary

Instantiate an MsmsSpectrum object by populating it with resolved spectrum data (m/z array, intensity array, precursor m/z, charge state, retention time, and metadata) retrieved from online proteomics repositories via Universal Spectrum Identifier (USI) resolution. This creates a structured, in-memory spectrum object that is ready for subsequent processing and annotation workflows.

## When to use

When you have successfully resolved a USI string to extract raw spectrum data from an online proteomics/metabolomics repository (PRIDE, MassIVE, etc.) and need to construct a spectrum object that exposes spectrum data as Python attributes and methods for downstream processing (filtering, annotation, visualization).

## When NOT to use

- Input spectrum data is already encapsulated in an existing MsmsSpectrum object — use that object directly.
- Spectrum data is in raw binary format (mzML, mzXML, raw vendor files) without prior USI resolution — use spectrum_utils' mzML/file-based loaders instead.
- Spectrum retrieval from the online repository failed or USI resolution returned incomplete/malformed data — validate repository connectivity and USI format before instantiation.

## Inputs

- Universal Spectrum Identifier (USI) string (e.g., 'mzspec:MSV000082283:f07074:scan:5475')
- resolved spectrum data tuple or dict: m/z array, intensity array, precursor_mz, precursor_charge, retention_time, scan_number, and optional metadata (title, file identifier)

## Outputs

- MsmsSpectrum object with populated precursor_mz, precursor_charge, mz, intensity, retention_time, and title attributes

## How to apply

After parsing the USI string and retrieving the raw spectrum data (m/z array, intensity array, precursor m/z, charge state, retention time, scan number) from the online repository endpoint, instantiate an MsmsSpectrum object by passing these resolved values to the MsmsSpectrum constructor, typically including title, precursor m/z, charge state, m/z array, intensity array, and retention time. The resulting object encapsulates all spectral attributes as accessible properties, enabling subsequent method calls such as set_mz_range(), remove_precursor_peak(), filter_intensity(), scale_intensity(), and annotate_proforma(). Verify successful instantiation by checking that the object's precursor_mz, precursor_charge, mz, and intensity properties match the expected values from the repository.

## Related tools

- **spectrum_utils** (Provides the MsmsSpectrum class constructor and USI resolution mechanism for retrieving and instantiating spectrum objects from online repositories) — https://github.com/bittremieux/spectrum_utils
- **Python** (Host language for MsmsSpectrum object instantiation and spectrum_utils library)

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum; import numpy as np; spectrum = MsmsSpectrum(title="scan_5475", precursor_mz=500.5, precursor_charge=2, mz=np.array([100.1, 150.2, 200.3]), intensity=np.array([10, 50, 100]), retention_time=300.5)
```

## Evaluation signals

- The returned object is an instance of MsmsSpectrum with non-None precursor_mz and precursor_charge attributes matching the USI-resolved values.
- The mz and intensity arrays have matching lengths and are non-empty NumPy arrays.
- The object's title or identifier field correctly reflects the USI scan number and source repository.
- Subsequent method calls (e.g., spectrum.filter_intensity(), spectrum.annotate_proforma()) execute without AttributeError, confirming the object structure is valid.
- The retention_time attribute (if present in the repository) is populated as a numeric value in seconds or matches the expected precision from the data source.

## Limitations

- USI resolution depends on external repository availability and network connectivity; transient or persistent repository outages will cause instantiation to fail.
- Spectrum data completeness varies by repository; some repositories may not provide retention time, charge state, or other optional metadata fields, resulting in partial object instantiation.
- The MsmsSpectrum constructor expects specific array types (NumPy arrays for mz and intensity); mismatched or improperly formatted input arrays may cause instantiation to fail or produce unexpected behavior.
- Large-scale batch instantiation of spectrum objects from multiple USI strings may exhaust memory if spectrum arrays are particularly large or if the batch size is not managed carefully.

## Evidence

- [other] Parse the USI string to extract repository accession, file/dataset identifier, and scan number using spectrum_utils' USI resolver.: "Parse the USI string to extract repository accession, file/dataset identifier, and scan number using spectrum_utils' USI resolver."
- [other] Retrieve the raw spectrum data (m/z array, intensity array, precursor m/z, charge state, retention time) from the online proteomics resource.: "Retrieve the raw spectrum data (m/z array, intensity array, precursor m/z, charge state, retention time) from the online proteomics resource"
- [other] Instantiate an MsmsSpectrum object by passing the resolved spectrum data to the MsmsSpectrum constructor.: "Instantiate an MsmsSpectrum object by passing the resolved spectrum data (title, precursor m/z, charge, m/z array, intensity array, retention time) to the MsmsSpectrum constructor."
- [other] Return the populated MsmsSpectrum object with all spectral attributes accessible for subsequent processing chains.: "Return the populated MsmsSpectrum object with all spectral attributes accessible for subsequent processing chains."
- [intro] Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism.: "Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism."
