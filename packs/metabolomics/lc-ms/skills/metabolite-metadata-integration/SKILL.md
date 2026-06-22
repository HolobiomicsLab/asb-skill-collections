---
name: metabolite-metadata-integration
description: Use when when you have separate quantification data (abundance matrix), sample metadata (phenotypes, treatment groups, experimental conditions), and spectral data (MS/MS fragmentation patterns or other spectral features) that must be combined for mass spectrometry-based metabolite analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - msFeaST
  - pandas
  - jupyter-notebook
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-metadata-integration

## Summary

Integration of quantification tables, metadata tables, and spectral data into a unified internal data structure required by the msFeaST pipeline. This skill prepares mass spectrometry data for downstream feature annotation and statistical analysis by aligning metabolite abundances with sample metadata and spectral information.

## When to use

When you have separate quantification data (abundance matrix), sample metadata (phenotypes, treatment groups, experimental conditions), and spectral data (MS/MS fragmentation patterns or other spectral features) that must be combined for mass spectrometry-based metabolite analysis. Use this skill as a prerequisite step before running msFeaST statistical and visualization workflows on your own datasets.

## When NOT to use

- Input data are already preprocessed and aligned into a single msFeaST-compatible Python object or JSON intermediate file
- Spectral data are not available or are not linked to quantification features by shared identifiers
- Metadata table does not share sample ID indices with the quantification table

## Inputs

- Quantification table (TSV, CSV, or pandas-compatible format with samples × features matrix)
- Metadata table (TSV, CSV, or pandas-compatible format with sample IDs and experimental covariates)
- Spectral data (vendor format or processed spectral features indexed by feature ID)

## Outputs

- Python data structures (dictionaries or DataFrames) compatible with msFeaST pipeline
- Validated, normalized quantification and metadata aligned by sample and feature identifiers
- Feature-to-spectrum mappings for downstream annotation

## How to apply

Load the three input data types (quantification table, metadata table, and spectral data files) using pandas and custom I/O functions provided in the msFeaST preprocessing notebook. Parse and validate the input data structures to ensure compatibility with msFeaST's internal requirements—typically a quantification matrix with features as columns and samples as rows, a metadata table indexed by sample ID, and spectral features indexed by feature identifier. Transform and normalize the quantification and metadata tables into the internal data format expected by msFeaST, ensuring sample IDs and feature identifiers align across all three sources. Process spectral data to align with feature identifiers and quantification mappings. Generate intermediate Python data structures (dictionaries, DataFrames, or objects) that serve as inputs to the msFeaST pipeline by running the preprocessing_mushroom_type_comparison.ipynb notebook with your data filepaths substituted for the example paths.

## Related tools

- **msFeaST** (Defines the internal data structure requirements and provides preprocessing notebook template for integration workflow) — https://github.com/kevinmildau/msFeaST
- **pandas** (Load, parse, and manipulate quantification and metadata tables in memory)
- **jupyter-notebook** (Interactive environment for running preprocessing_mushroom_type_comparison.ipynb to execute integration steps)

## Examples

```
jupyter-notebook && open preprocessing_mushroom_type_comparison.ipynb # then modify filepath variables at top of notebook to point to your quantification.csv, metadata.csv, and spectral_data files, then run all cells
```

## Evaluation signals

- All samples present in quantification table are also present in metadata table and indexed by the same sample ID
- All features in quantification table are mapped to spectral data entries via shared feature identifiers
- Quantification matrix has no NaN or infinite values in critical regions after normalization
- Output data structures conform to msFeaST's expected internal format (e.g., validated schema when passed to pipeline initialization)
- No rows or columns are dropped unintentionally during alignment; row/column counts should be documented before and after integration

## Limitations

- msFeaST preprocessing and pipeline workflow has been tested on macOS and Linux only; Windows support is currently being worked on
- Integration depends on consistent naming and indexing conventions across input files; mismatched or duplicated sample/feature IDs will cause failures
- Custom I/O functions in the preprocessing notebook may not handle all vendor spectral data formats; users may need to adapt file parsing logic
- No automatic deduplication or conflict resolution for conflicting metadata values across input sources

## Evidence

- [other] The preprocessing_mushroom_type_comparison.ipynb notebook demonstrates processing of three input data types—quantification table, metadata table, and spectral data—that are required for msFeaST: "processing of three input data types—quantification table, metadata table, and spectral data—that are required for msFeaST"
- [other] Load the quantification table, metadata table, and spectral data files from the omsw_pleurotus example dataset using pandas and custom I/O functions in the msFeaST preprocessing notebook. Parse and validate the input data structures to ensure compatibility with msFeaST requirements.: "Load the quantification table, metadata table, and spectral data files from the omsw_pleurotus example dataset using pandas and custom I/O functions in the msFeaST preprocessing notebook. Parse and"
- [other] Transform and normalize the quantification and metadata tables into the internal data format expected by msFeaST. Process spectral data to align with feature identifiers and quantification mappings. Generate intermediate Python data structures (dictionaries, DataFrames, or objects) that serve as inputs to the msFeaST pipeline.: "Transform and normalize the quantification and metadata tables into the internal data format expected by msFeaST. Process spectral data to align with feature identifiers and quantification mappings."
- [readme] These notebooks contain a complete example of quantification table, metadata table, and spectral data processing required for msFeaST, as well as a complete use-case example. To make use of your own data, change the data filepath arguments to your own data file location and run the pipeline.: "These notebooks contain a complete example of quantification table, metadata table, and spectral data processing required for msFeaST, as well as a complete use-case example. To make use of your own"
- [readme] The current msFeaST pre-processing and pipeline workflow has been tested on macos and should work identically on linux operating systems. Windows support is currently being worked on.: "The current msFeaST pre-processing and pipeline workflow has been tested on macos and should work identically on linux operating systems. Windows support is currently being worked on."
