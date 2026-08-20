---
name: mass-spectrometry-data-parsing
description: Use when you have received raw or vendor-converted centroid mzML files
  from LC-MS, GC-MS, or DI-MS platforms and need to extract MS1 spectra before building
  mass tracks, performing peak detection, or constructing composite feature maps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3931
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - pymzml
  - Python
  - ThermoRawFileParser
  - ProteoWizard (msconvert)
  - asari
  - GNPS LCMS Visualization Dashboard
  - pyteomics
  - mzmine
  - IDSL.IPA
  - R
  - RnetCDF
  - Spectra
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - MEMO
  - memo-ms
  techniques:
  - LC-MS
  - GC-MS
  - direct-infusion-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
- doi: 10.1038/s41592-021-01339-5
  title: ''
- doi: 10.1021/acs.jproteome.2c00120
  title: ''
- doi: 10.1186/s13321-023-00695-y
  title: ''
- doi: 10.3389/fbinf.2022.842964
  title: ''
evidence_spans:
- The default method uses `pymzml` to parse mzML files.
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory
  for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight
  R package'
- light-weight R package
- performs spectral database dereplication using R Package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari_cq
    doi: 10.1038/s41467-023-39889-1
    title: asari
  - build: coll_gnps_dashboard_cq
    doi: 10.1038/s41592-021-01339-5
    title: GNPS Dashboard
  - build: coll_idsl_ipa_cq
    doi: 10.1021/acs.jproteome.2c00120
    title: IDSL.IPA
  - build: coll_maw_cq
    doi: 10.1186/s13321-023-00695-y
    title: MAW
  - build: coll_memo
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_asari_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  - 10.1038/s41592-021-01339-5
  - 10.1021/acs.jproteome.2c00120
  - 10.1186/s13321-023-00695-y
  - 10.3389/fbinf.2022.842964
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse centroid mzML files from LC-MS instruments to extract MS1 spectra as (m/z, scan_number, intensity) tuples, indexing them for efficient retrieval and downstream mass track construction. This is the foundational step that converts vendor instrument data into a structured, queryable representation suitable for high-resolution metabolomics feature extraction.

## When to use

You have received raw or vendor-converted centroid mzML files from LC-MS, GC-MS, or DI-MS platforms and need to extract MS1 spectra before building mass tracks, performing peak detection, or constructing composite feature maps. Use this skill at the start of any asari workflow or when you need to inspect and validate the structure and quality of raw mass spectrometry data before alignment or annotation.

## When NOT to use

- Input data are in profile (non-centroid) format — asari requires centroid mzML; convert using ProteoWizard or ThermoRawFileParser first.
- Data have already been processed into mass tracks or feature tables — this skill is for raw spectrum extraction only.
- You need to extract or process MS/MS spectra — asari's default LC-MS workflow ignores MS/MS data; use alternative workflows if tandem data are required.

## Inputs

- centroid mzML file (from LC-MS, GC-MS, or DI-MS platform)
- vendor .RAW file (if converted to mzML via ThermoRawFileParser or ProteoWizard)

## Outputs

- list of (m/z, scan_number, intensity) tuples extracted from MS1 spectra
- mzTree dictionary keyed by int(mz × 1000) for efficient mass-indexed lookup

## How to apply

Use pymzml to parse the mzML file and retrieve all MS1 spectra as a list of (m/z, scan_number, intensity) tuples. Index the resulting data points into an mzTree dictionary keyed by int(mz × 1000) to enable efficient O(1) lookup during subsequent binning and mass track construction. Validate that the parsed tuples retain high mass resolution (typically sub-ppm for Orbitrap or similar instruments) and that scan numbers are sequential and complete. Check that intensity values are positive and that the m/z range matches the instrument's configured mass window. This indexing scheme exploits high mass resolution to prioritize mass separation during the initial processing phase, laying the groundwork for accurate alignment and downstream feature detection.

## Related tools

- **pymzml** (Parse mzML files and retrieve MS1 spectra as (m/z, scan_number, intensity) tuples)
- **ThermoRawFileParser** (Convert Thermo .RAW files to indexed mzML format before parsing) — https://github.com/compomics/ThermoRawFileParser
- **ProteoWizard (msconvert)** (Convert most vendor mass spectrometry formats to mzML or mzXML) — https://proteowizard.sourceforge.io/tools.shtml
- **asari** (Orchestrates mzML parsing and downstream mass track construction via chromatograms.extract_massTracks_) — https://github.com/shuzhao-li/asari

## Examples

```
from pymzml import run; spectra = [(s['m/z array'], s['ID'], s['intensity array']) for s in run('sample.mzML') if s['ms level'] == 1]
```

## Evaluation signals

- Parsed tuple list contains non-zero counts of (m/z, scan_number, intensity) entries with m/z values spanning the instrument's configured mass window (typically 50–1200 m/z for metabolomics).
- mzTree dictionary contains entries for all unique int(mz × 1000) keys; no collisions or data loss during indexing.
- Scan numbers are sequential (or contain expected gaps for non-MS1 scans); no duplicate or out-of-order entries.
- Intensity values are all positive integers or floats; no negative or NaN entries after parsing.
- High mass resolution is preserved: m/z values show sub-ppm precision (e.g., 5–10 decimal places for Orbitrap data), not truncated to lower precision.

## Limitations

- Performance scales with file size; very large mzML files (>10 GB) may require streaming or chunked parsing to stay within memory budget.
- Profile-mode (non-centroid) data must be converted to centroid format before parsing; centroiding is not performed by pymzml itself.
- Parsing speed and accuracy depend on mzML file quality and vendor-specific schema compliance; some vendor formats may have non-standard or incomplete metadata.
- MS/MS spectra are ignored in this parsing step; if tandem data are required, alternative workflows or explicit MS2 extraction logic must be applied.

## Evidence

- [other] Parse the mzML file using pymzml to retrieve all MS1 spectra as a list of (m/z, scan_number, intensity) tuples.: "Parse the mzML file using pymzml to retrieve all MS1 spectra as a list of (m/z, scan_number, intensity) tuples."
- [other] The default method uses `pymzml` to parse mzML files.: "The default method uses `pymzml` to parse mzML files."
- [other] Index data points into an mzTree dictionary keyed by int(mz × 1000) for efficient retrieval.: "Index data points into an mzTree dictionary keyed by int(mz × 1000) for efficient retrieval."
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
- [other] We use ThermoRawFileParser to convert Thermo .RAW files to .mzML. Msconvert in ProteoWizard can handle the conversion of most vendor data formats.: "We use ThermoRawFileParser to convert Thermo .RAW files to .mzML. Msconvert in ProteoWizard can handle the conversion of most vendor data formats."
- [other] Input data are centroid mzML files from LC, GC or DI-MS metabolomics.: "Input data are centroid mzML files from LC, GC or DI-MS metabolomics."
- [other] MS/MS spectra are ignored in default LC-MS workflow but handled by alternative workflows.: "MS/MS spectra are ignored in default LC-MS workflow but handled by alternative workflows."
