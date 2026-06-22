---
name: spectral-format-parsing-and-validation
description: Use when you have raw or unprocessed MS/MS spectral data in standard metabolomics formats (MGF, mzML, mzXML, msp, or JSON) and need to import them into a Python-based workflow for MS2 fingerprint generation, peak counting, or spectral similarity scoring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - scikit-bio
  - memo-ms
  - Python 3.8+
  techniques:
  - tandem-MS
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra
- conda create --name memo python=3.8
- pip install numpy
- conda install -c conda-forge scikit-bio
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fbinf.2022.842964
  all_source_dois:
  - 10.3389/fbinf.2022.842964
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-format-parsing-and-validation

## Summary

Parse mass spectrometry spectral data from common file formats (mzML, mzXML, MGF, msp, JSON) and validate metadata, peak lists, and precursor ion information to ensure data integrity before downstream processing. This is essential for MS/MS-based sample comparison workflows where spectral quality directly affects fingerprint generation and sample alignment.

## When to use

You have raw or unprocessed MS/MS spectral data in standard metabolomics formats (MGF, mzML, mzXML, msp, or JSON) and need to import them into a Python-based workflow for MS2 fingerprint generation, peak counting, or spectral similarity scoring. Use this skill as the entry point before memo_from_aligned, spec2vec embedding, or matchms-based comparisons.

## When NOT to use

- Input spectral data is already pre-parsed into Python objects (e.g., Spectrum objects already in memory) — skip directly to filtering or fingerprinting.
- You are working with aligned feature tables and MS/MS spectra are already integrated into the feature matrix — use memo_from_aligned instead.
- Spectral data is in a proprietary vendor format not supported by matchms (e.g., Bruker .d, Waters .raw) — first convert to mzML or mzXML using vendor tools or MSConvert.

## Inputs

- MGF spectral file (Mascot Generic Format)
- mzML spectral file (mzML XML format)
- mzXML spectral file (mzXML XML format)
- msp spectral library file (NIST MSP format)
- JSON spectral file (JSON metabolomics-USI format)

## Outputs

- Parsed Spectrum objects (matchms.Spectrum instances)
- Validated spectral metadata (precursor m/z, charge, ionization mode, scan number)
- Cleaned peak lists (m/z-intensity pairs, neutral losses if applicable)
- QC report (count of spectra loaded, spectra failing validation, metadata completeness)

## How to apply

Use matchms to load spectral data from MGF, mzML, mzXML, msp, or JSON files. Apply built-in metadata cleaning and validation routines to remove or flag spectra with missing precursor m/z, incorrect ionization mode, or invalid peak lists. Filter out spectra that fail validation thresholds (e.g., minimum number of peaks, m/z range consistency). Validate that all spectra contain required fields (precursor m/z, retention time if applicable, scan metadata) before passing to downstream MS2 fingerprinting or similarity scoring steps. The validation ensures that subsequent MS2 peak and neutral loss counting for MEMO generates accurate fingerprints.

## Related tools

- **matchms** (Imports, parses, validates, and cleans MS/MS spectral metadata and peak lists from multiple file formats (mzML, mzXML, MGF, msp, JSON); enforces data quality before downstream processing.) — https://github.com/matchms/matchms
- **memo-ms** (Consumes validated Spectrum objects and their associated aligned feature tables to generate MS2 fingerprints via peak and neutral loss counting.) — https://github.com/mandelbrot-project/memo
- **spec2vec** (Uses parsed and validated spectra to compute spectral embeddings and similarity scores based on spectral relationships learned from MS/MS fragmentation patterns.) — https://github.com/iomega/spec2vec
- **Python 3.8+** (Runtime environment for matchms, spec2vec, and memo-ms libraries.)
- **numpy** (Underlying array operations for peak list manipulation and spectral matrix construction.)

## Examples

```
from matchms.importing import load_from_mgf; from matchms.data_source import load_spectrum; spectra = list(load_from_mgf('spectra.mgf')); print(f'Loaded {len(spectra)} spectra'); valid = [s for s in spectra if s.precursor_mz is not None and len(s.peaks) > 0]; print(f'Valid spectra: {len(valid)}')
```

## Evaluation signals

- All spectral files are successfully loaded without I/O errors; log shows count of spectra parsed from each file format.
- Metadata completeness: ≥95% of spectra contain precursor m/z, scan identifiers, and ionization mode (if applicable); QC report flags spectra with missing fields.
- Peak list validation: all m/z values are in expected range (50–2000 m/z typical for metabolomics); intensity values are non-negative; no duplicate m/z entries within a spectrum.
- Spectral deduplication: no exact duplicate spectra (identical precursor m/z, retention time, peak list) remain after parsing; duplicates logged and removed if requested.
- Schema compliance: parsed Spectrum objects conform to matchms.Spectrum class; downstream functions (memo_from_aligned, spec2vec similarity) accept parsed objects without casting errors.

## Limitations

- Vendor-specific proprietary formats (Bruker .d, Waters .raw, Thermo .raw) are not directly supported by matchms; require prior conversion to mzML/mzXML using third-party tools (e.g., MSConvert).
- Metadata cleaning is heuristic-based and may remove or corrupt non-standard metadata fields; critical custom annotations should be preserved in separate auxiliary files.
- Performance scales with file size; parsing very large mzML files (>1 GB) may consume significant memory; consider chunked or streaming approaches for batch processing.
- Neutral loss annotations (required for MEMO fingerprinting) may be absent or inconsistently formatted in some spectral libraries; must be computed or inferred separately if not present in input files.

## Evidence

- [readme] Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS).: "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS)."
- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [readme] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity."
- [other] Load aligned feature tables and corresponding MS2 spectra data files in formats expected by memo-ms (e.g., CSV feature tables and MGF/mzML spectral files).: "Load aligned feature tables and corresponding MS2 spectra data files in formats expected by memo-ms (e.g., CSV feature tables and MGF/mzML spectral files)."
- [other] MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
