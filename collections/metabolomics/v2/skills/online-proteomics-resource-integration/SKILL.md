---
name: online-proteomics-resource-integration
description: Use when your analysis requires MS/MS spectra from public proteomics
  datasets but you want to avoid manual download and format conversion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - Python
  - spectrum_utils
  - NumPy
  - Numba
  - PSI-MOD Protein Modifications Ontology
  techniques:
  - LC-MS
  license_tier: restricted
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

# online-proteomics-resource-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load tandem mass spectrometry spectra from distributed online proteomics and metabolomics repositories (PRIDE, MassIVE) using Universal Spectrum Identifier (USI) strings, resolving them to raw spectral data and instantiating searchable spectrum objects. This skill bridges the gap between web-accessible MS/MS data archives and local processing pipelines.

## When to use

Your analysis requires MS/MS spectra from public proteomics datasets but you want to avoid manual download and format conversion. You have a USI string (format: mzspec:REPOSITORY:DATASET:scan:SCANNUMBER) identifying a specific spectrum in PRIDE, MassIVE, or equivalent online resource, and you need programmatic access to its m/z array, intensity array, precursor m/z, charge state, and retention time without writing custom HTTP/API logic.

## When NOT to use

- Spectrum data is already local (mzML, mgf, or other file format on disk) — use direct file loading instead
- You require offline processing without network access to public repositories
- The spectrum's repository or USI string is not publicly registered in PRIDE, MassIVE, or other supported online resources

## Inputs

- Universal Spectrum Identifier (USI) string (e.g., 'mzspec:MSV000082283:f07074:scan:5475')
- Network access to online proteomics repository (PRIDE, MassIVE, or PSI-MOD compliant endpoint)

## Outputs

- MsmsSpectrum object with populated attributes: title, precursor_mz, charge, mz array, intensity array, retention_time
- Accessible spectrum data ready for filtering and annotation operations

## How to apply

Use spectrum_utils's USI resolver to parse the USI string and extract the repository identifier, dataset/file accession, and scan number. Query the online proteomics resource (via the USI endpoint) to retrieve the raw spectrum data—m/z and intensity arrays, precursor m/z, charge state, and retention time. Pass these resolved values to the MsmsSpectrum constructor (title, precursor_mz, charge, mz array, intensity array, retention_time) to instantiate a spectrum object that is then accessible for downstream filtering (precursor/noise removal, intensity scaling) and annotation (ProForma 2.0 fragment matching). The spectrum object's spectral attributes are immediately available for subsequent processing chains, avoiding re-parsing.

## Related tools

- **spectrum_utils** (Parses USI strings, resolves spectrum data from online endpoints, instantiates MsmsSpectrum objects with resolved spectral attributes) — https://github.com/bittremieux/spectrum_utils
- **NumPy** (Optimizes spectrum array operations (m/z and intensity arrays) for computational efficiency during spectrum loading and processing) — https://www.numpy.org/
- **Numba** (Just-in-time compilation of spectrum processing operations to accelerate USI resolution and spectrum object construction) — http://numba.pydata.org/
- **PSI-MOD Protein Modifications Ontology** (Provides controlled vocabulary for protein modifications referenced in ProForma 2.0 peptide annotations during spectrum annotation) — https://github.com/HUPO-PSI/psi-mod-CV

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum
from spectrum_utils.utils import load_spectrum
usi = "mzspec:MSV000082283:f07074:scan:5475"
spectrum = load_spectrum(usi)
print(spectrum.precursor_mz, spectrum.charge, len(spectrum.mz))
```

## Evaluation signals

- MsmsSpectrum object is successfully instantiated with non-null title, precursor_mz, charge, mz array, and intensity array attributes
- m/z array and intensity array have matching lengths and no NaN or negative intensity values
- Precursor m/z is within expected mass range (typically 200–2000 m/z for peptide MS/MS)
- Charge state is a positive integer (typically +1 to +4 for peptides)
- Spectrum object methods (e.g., set_mz_range, remove_precursor_peak, filter_intensity) execute without AttributeError, confirming schema compliance

## Limitations

- USI resolution requires stable network connectivity and availability of the target online repository; transient network failures or repository downtime will cause resolution to fail
- Only spectra registered in supported PSI-compliant repositories (PRIDE, MassIVE, and others with active USI endpoints) are accessible; private or legacy formats require alternative loading strategies
- USI string format must be syntactically correct and the referenced dataset/scan must exist; typos or deleted scans will raise resolution errors
- No changelog is available to track breaking changes in USI endpoint behavior or spectrum_utils API versions

## Evidence

- [intro] Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism.: "Spectrum loading from online proteomics and metabolomics data resources using the Universal Spectrum Identifier (USI) mechanism."
- [other] Parse the USI string to extract repository accession, file/dataset identifier, and scan number using spectrum_utils' USI resolver.: "Parse the USI string to extract repository accession, file/dataset identifier, and scan number using spectrum_utils' USI resolver."
- [other] Retrieve the raw spectrum data (m/z array, intensity array, precursor m/z, charge state, retention time) from the online proteomics resource (PRIDE, MassIVE, or equivalent) via the USI endpoint.: "Retrieve the raw spectrum data (m/z array, intensity array, precursor m/z, charge state, retention time) from the online proteomics resource (PRIDE, MassIVE, or equivalent) via the USI endpoint."
- [other] Instantiate an MsmsSpectrum object by passing the resolved spectrum data (title, precursor m/z, charge, m/z array, intensity array, retention time) to the MsmsSpectrum constructor.: "Instantiate an MsmsSpectrum object by passing the resolved spectrum data (title, precursor m/z, charge, m/z array, intensity array, retention time) to the MsmsSpectrum constructor."
- [other] Return the populated MsmsSpectrum object with all spectral attributes accessible for subsequent processing chains.: "Return the populated MsmsSpectrum object with all spectral attributes accessible for subsequent processing chains."
- [other] Load a spectrum from an online data resource by its Universal Spectrum Identifier (USI): "Load a spectrum from an online data resource by its Universal Spectrum Identifier (USI)"
