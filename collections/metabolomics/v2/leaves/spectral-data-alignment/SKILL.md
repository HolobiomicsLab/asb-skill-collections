---
name: spectral-data-alignment
description: Use when you have quantification tables (with feature IDs and abundance
  values), metadata tables (with sample annotations), and separate spectral data files
  (e.g., MS/MS spectra or fragmentation patterns), and you need to integrate them
  into a unified input for msFeaST.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - msFeaST
  - jupyter-notebook
  - pandas
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btae584
  title: msFeaST
evidence_spans:
- github.com__kevinmildau__msFeaST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msfeast_cq
    doi: 10.1093/bioinformatics/btae584
    title: msFeaST
  dedup_kept_from: coll_msfeast_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae584
  all_source_dois:
  - 10.1093/bioinformatics/btae584
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-data-alignment

## Summary

Align mass spectrometry spectral data with feature identifiers and quantification mappings to ensure consistent indexing across the msFeaST pipeline. This step transforms raw spectral records into an intermediate data structure compatible with downstream feature extraction and statistical analysis.

## When to use

You have quantification tables (with feature IDs and abundance values), metadata tables (with sample annotations), and separate spectral data files (e.g., MS/MS spectra or fragmentation patterns), and you need to integrate them into a unified input for msFeaST. Use this skill when spectral data references do not naturally align with quantification row/column indices and require explicit mapping or indexing validation.

## When NOT to use

- Spectral data is already indexed identically to the quantification table and requires no transformation or mapping.
- You are only working with quantification and metadata tables (no separate spectral data files).
- Spectral data is in a format that msFeaST natively ingests without intermediate Python structures.

## Inputs

- quantification table (pandas DataFrame or CSV with feature IDs and abundance values)
- metadata table (pandas DataFrame or CSV with sample identifiers and annotations)
- spectral data file (JSON, text, or binary format containing MS/MS fragmentation records or spectral properties)

## Outputs

- aligned spectral data structure (Python dictionary or DataFrame with feature-to-spectrum mappings)
- intermediate data structures (dictionaries, DataFrames, or objects ready for msFeaST input)
- validation report (implicit or explicit confirmation of index consistency across quantification, metadata, and spectral data)

## How to apply

Load quantification, metadata, and spectral data files using pandas and custom I/O functions provided in the preprocessing_mushroom_type_comparison.ipynb notebook. Parse the spectral data to extract feature identifiers (e.g., scan numbers, m/z values, or custom spectrum IDs) and cross-reference them against the quantification table's row or column identifiers. Validate that all spectral records correspond to features present in the quantification table, and vice versa. Transform spectral data into Python dictionaries or DataFrames that preserve the feature-to-spectrum mapping. Finally, generate intermediate data structures (e.g., nested dictionaries keyed by feature ID, or DataFrames with aligned indices) that serve as inputs to the msFeaST pipeline alongside the quantification and metadata tables.

## Related tools

- **msFeaST** (Python module that consumes aligned spectral data as part of its preprocessing and feature extraction pipeline) — https://github.com/kevinmildau/msFeaST
- **jupyter-notebook** (Interactive environment for executing preprocessing workflows and spectral data alignment logic via preprocessing_mushroom_type_comparison.ipynb)
- **pandas** (Data loading and manipulation of quantification, metadata, and aligned spectral tables)

## Examples

```
# In preprocessing_mushroom_type_comparison.ipynb:
# Load and align spectral data with quantification indices
quantification_df = pd.read_csv('quantification.csv', index_col='feature_id')
spectral_data = json.load(open('spectral_data.json'))
aligned_spectra = {fid: spectral_data[fid] for fid in quantification_df.index if fid in spectral_data}
```

## Evaluation signals

- All spectral data feature identifiers are present in the quantification table (no orphaned spectra).
- All quantified features have a corresponding spectral record (no missing spectra for quantified features).
- Indices or keys in the aligned spectral structure exactly match quantification row/column identifiers.
- The intermediate Python data structure (dictionary or DataFrame) can be serialized and deserialized without loss of feature-to-spectrum mappings.
- The msFeaST pipeline accepts the aligned spectral structure without index mismatch errors during feature extraction.

## Limitations

- Windows support for msFeaST preprocessing is currently being worked on; spectral data alignment has been tested on macOS and Linux only.
- Spectral data format must be compatible with custom I/O functions provided in the notebook; non-standard or proprietary formats may require custom parsing logic.
- If spectral data and quantification tables use different feature identifier schemes (e.g., m/z values vs. scan indices), manual mapping rules or lookup tables must be defined before alignment.
- R path caching issues can occur if rscript calls are run before conda environment activation, potentially affecting downstream R-based statistical steps in msFeaST.

## Evidence

- [other] Process spectral data to align with feature identifiers and quantification mappings.: "Process spectral data to align with feature identifiers and quantification mappings."
- [other] Load the quantification table, metadata table, and spectral data files from the omsw_pleurotus example dataset using pandas and custom I/O functions in the msFeaST preprocessing notebook.: "Load the quantification table, metadata table, and spectral data files from the omsw_pleurotus example dataset using pandas and custom I/O functions in the msFeaST preprocessing notebook."
- [other] Generate intermediate Python data structures (dictionaries, DataFrames, or objects) that serve as inputs to the msFeaST pipeline.: "Generate intermediate Python data structures (dictionaries, DataFrames, or objects) that serve as inputs to the msFeaST pipeline."
- [readme] The current msFeaST pre-processing and pipeline workflow has been tested on macos and should work identically on linux operating systems. Windows support is currently being worked on.: "The current msFeaST pre-processing and pipeline workflow has been tested on macos and should work identically on linux operating systems. Windows support is currently being worked on."
- [readme] These notebooks contain a complete example of quantification table, metadata table, and spectral data processing required for msFeaST: "These notebooks contain a complete example of quantification table, metadata table, and spectral data processing required for msFeaST"
