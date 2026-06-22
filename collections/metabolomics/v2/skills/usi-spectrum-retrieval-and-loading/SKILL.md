---
name: usi-spectrum-retrieval-and-loading
description: Use when you have a USI accession (e.g., 'mzspec:MSV000082283:f07074:scan:5475' or 'mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555') pointing to a publicly deposited tandem mass spectrometry scan in a GNPS or ProteomeXchange repository, and you need to retrieve and instantiate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spectrum_utils
  - Python
  - matplotlib
  - GNPS public library
  - ProteomeXchange (PXD datasets)
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
- import matplotlib.pyplot as plt
- fig, ax = plt.subplots(figsize=(12, 6))
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils
schema_version: 0.2.0
---

# USI-based spectrum retrieval and loading

## Summary

Load mass spectrometry spectra from public proteomics and metabolomics repositories using Universal Spectrum Identifiers (USI), enabling direct programmatic access to published data without manual download. This skill bridges online data discovery and local analysis by parsing USI accessions and instantiating spectrum objects ready for downstream processing and visualization.

## When to use

You have a USI accession (e.g., 'mzspec:MSV000082283:f07074:scan:5475' or 'mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555') pointing to a publicly deposited tandem mass spectrometry scan in a GNPS or ProteomeXchange repository, and you need to retrieve and instantiate that spectrum programmatically for annotation, processing, or visualization without downloading raw files locally.

## When NOT to use

- Input is a local raw file (mzML, mzXML, mgf); use file-based loading methods instead (e.g., spectrum_utils.io.mgf_file() or pymzML).
- Network connectivity is unavailable or unreliable; pre-download spectra locally or use offline formats.
- The data is from a private or restricted-access repository not indexed by GNPS or ProteomeXchange; USI mechanism requires public metadata registration.

## Inputs

- USI accession string (e.g., 'mzspec:MSV000082283:f07074:scan:5475')
- Network connectivity to public mass spectrometry data repositories (GNPS, MassIVE, ProteomeXchange)

## Outputs

- MsmsSpectrum object with populated m/z array, intensity array, precursor m/z, precursor charge, and scan metadata

## How to apply

Call the MsmsSpectrum.from_usi() method with the USI string as the sole argument; this queries the remote repository index (GNPS, MassIVE, or ProteomeXchange) via HTTP, retrieves the scan metadata and peak list, and returns a spectrum object with m/z and intensity arrays. The USI parsing is handled transparently by spectrum_utils, which maps the repository prefix (MSV, PXD) and scan identifier to the corresponding data service endpoint. Verify successful retrieval by inspecting the returned spectrum's precursor m/z, charge state, and peak count; empty or malformed spectra indicate network failure or invalid USI format. This approach is preferred when you need reproducibility (USI is a persistent identifier) and want to avoid storing large raw mzML or mzXML files locally.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum.from_usi() method for USI-based retrieval and instantiation; handles USI parsing, repository endpoint mapping, and spectrum object construction) — https://github.com/bittremieuxlab/spectrum_utils
- **GNPS public library** (Public repository indexed by USI that hosts mass spectrometry spectra and library matches)
- **ProteomeXchange (PXD datasets)** (Repository system (MassIVE, PRIDE, jPOST) that provides persistent access to submitted proteomics datasets via USI identifiers)

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum; spectrum = MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475')
```

## Evaluation signals

- Returned MsmsSpectrum object is not None and contains non-empty m/z and intensity arrays
- Precursor m/z, charge state, and scan identifier match the expected values from the USI accession metadata
- Peak count and intensity distribution are consistent with the original repository record (spot-check against online viewer if available)
- Subsequent processing steps (e.g., annotation, filtering) execute without errors on the retrieved spectrum
- HTTP request to the repository endpoint succeeds (200 status) and completes within a reasonable timeout (e.g., <10 seconds per spectrum)

## Limitations

- Requires network connectivity; cannot be used offline or in restricted-network environments.
- Dependent on remote repository availability and uptime; spectra may become temporarily or permanently unavailable if the repository is down or the dataset is retracted.
- USI resolution relies on correct repository indexing; newly uploaded datasets may have a lag before USI resolution succeeds.
- Large-scale batch retrieval of many spectra via USI may be rate-limited by the remote service; consider caching or batching requests.
- No changelog found in the spectrum_utils repository, limiting ability to track breaking changes in USI parsing or API mappings.

## Evidence

- [intro] Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism.: "Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism."
- [other] Example USI accession for a public spectrum: "usi = "mzspec:MSV000082283:f07074:scan:5475""
- [other] Method signature and usage: "Retrieve the spectrum from an online proteomics data resource using MsmsSpectrum.from_usi() with the provided USI accession."
- [other] Supported datasets from multiple repositories: "usi = "mzspec:PXD000561:Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555""
