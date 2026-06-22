---
name: mass-spectrometry-data-format-parsing
description: Use when you have raw MS/MS spectra in one of the supported exchange formats (.mgf, .mzML, or .msp) and need to ingest them into an MS2LDA pipeline for unsupervised motif discovery. This skill is required before any preprocessing, filtering, or ionization-mode-specific handling can occur.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - MS2LDA
  - Python
  - Conda
  - MS2LDA.Preprocessing.load_and_clean
  - OpenMS
  - pyarrow
  - R
  - Rust mzPeak library and CLI converter
  - Python pyarrow implementation
  - R arrow implementation
  - Apache Arrow / PyArrow
  - mzPeak specification
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
- doi: 10.1021/acs.jproteome.5c00435
  title: ''
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- Invoke the main script `ms2lda_runfull.py` with your arguments
- configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- Configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- These steps assume you have [Conda](http://conda.io/) installed.
- There is a separate Python implementation in `python/`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_comparems2_2_0_cq
    doi: 10.1021/acs.jproteome.2c00457
    title: compareMS2 2.0
  - build: coll_ms2lda_cq
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  - build: coll_mzpeak
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  dedup_kept_from: coll_ms2lda_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  - 10.1021/acs.jproteome.5c00435
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-format-parsing

## Summary

Load and parse tandem mass spectrometry (MS/MS) spectral data from standard interchange formats (.mgf, .mzML, .msp) into memory for downstream preprocessing and modeling. This is the essential first step that converts heterogeneous file formats into a unified in-memory representation suitable for spectral filtering, fragmentation analysis, and bag-of-fragments conversion.

## When to use

You have raw MS/MS spectra in one of the supported exchange formats (.mgf, .mzML, or .msp) and need to ingest them into an MS2LDA pipeline for unsupervised motif discovery. This skill is required before any preprocessing, filtering, or ionization-mode-specific handling can occur.

## When NOT to use

- Input is already in memory as Python objects or a parsed spectral object from another tool — skip directly to filtering.
- You have already extracted and aggregated fragment intensities into a bag-of-words or feature matrix — parsing is unnecessary.
- Input file format is not one of the three supported formats (.mgf, .mzML, .msp); conversion to a supported format is required first.

## Inputs

- Mass spectrometry spectral file (.mgf format)
- Mass spectrometry spectral file (.mzML format)
- Mass spectrometry spectral file (.msp format)

## Outputs

- Parsed spectrum collection (in-memory objects with precursor mass, fragments, intensities, ionization mode)
- Spectrum metadata (MS level, ionization mode, acquisition parameters)

## How to apply

Use the MS2LDA.Preprocessing.load_and_clean module to read spectral data from disk. The loader automatically detects or accepts the input format (.mgf, .mzML, or .msp) and deserializes spectra into structured objects that preserve precursor mass, fragment m/z values, intensities, and ionization mode metadata. The module performs basic validation during parsing (e.g., checking for required fields, handling missing intensity values). The parsed spectrum collection is then passed directly to subsequent filtering and neutral loss extraction steps. Correct parsing is verified by confirming that spectrum count matches the input file's declared spectrum count, that all required fields (precursor mass, fragment m/z, intensity) are populated, and that no malformed records cause loader errors.

## Related tools

- **MS2LDA.Preprocessing.load_and_clean** (Primary module for loading and parsing MS/MS spectral data from supported file formats into structured in-memory objects.) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Broader toolkit that orchestrates preprocessing, modeling, and annotation; this skill is the data ingestion entry point.) — https://github.com/vdhooftcompmet/MS2LDA

## Examples

```
from MS2LDA.Preprocessing import load_and_clean; spectra = load_and_clean.load_spectra('samples.mgf', ionization_mode='positive')
```

## Evaluation signals

- Spectrum count in parsed collection matches declared count in input file (no records dropped due to parse errors).
- All spectra have populated precursor mass, fragment m/z arrays, and intensity arrays (no null/missing required fields).
- Ionization mode metadata (positive/negative) is correctly assigned to each spectrum based on file headers or user input.
- No parsing exceptions or malformed record warnings during load; loader completes without errors.
- Downstream filtering steps (noise removal, ionization-mode-specific handling) execute without type errors or schema violations.

## Limitations

- Only three file formats (.mgf, .mzML, .msp) are supported; other MS data formats (e.g., raw proprietary formats, NetCDF) require conversion before ingestion.
- Parser assumes standard compliance with .mgf, .mzML, and .msp specifications; nonstandard or corrupted files may fail silently or produce incomplete records.
- No automatic ionization-mode detection in .mgf format; user must specify or file must include ionization mode in headers.
- Large files (>1 GB) may cause high memory consumption during parsing; chunked or streaming load is not explicitly documented.

## Evidence

- [other] Load MS/MS spectra from supported input file formats (.mgf, .mzML, or .msp) using the MS2LDA.Preprocessing.load_and_clean module.: "Load MS/MS spectra from supported input file formats (.mgf, .mzML, or .msp) using the MS2LDA.Preprocessing.load_and_clean module."
- [readme] MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling and providing automated annotation of discovered motifs.: "MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling and providing automated annotation of discovered motifs."
- [methods] Preprocessing → filter & clean your spectra (positive/negative ion mode): "Preprocessing → filter & clean your spectra (positive/negative ion mode)"
