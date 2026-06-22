---
name: python-data-structure-engineering
description: Use when you have raw mass spectrometry quantification tables (feature abundance matrices), sample metadata tables, and spectral data files (e.g., from the omsw_pleurotus dataset) that must be ingested into the msFeaST pipeline;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3750
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - msFeaST
  - pandas
  - jupyter-notebook
  techniques:
  - mass-spectrometry
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

# Python Data Structure Engineering

## Summary

Transform raw quantification tables, metadata, and spectral data files into intermediate Python objects (dictionaries, DataFrames) that conform to msFeaST pipeline input specifications. This skill bridges file I/O and pipeline ingestion by parsing, validating, and normalizing heterogeneous scientific data formats into a unified internal representation.

## When to use

You have raw mass spectrometry quantification tables (feature abundance matrices), sample metadata tables, and spectral data files (e.g., from the omsw_pleurotus dataset) that must be ingested into the msFeaST pipeline; the raw files are in different formats or schemas and require alignment on feature identifiers and sample mappings before downstream analysis.

## When NOT to use

- Input data are already in msFeaST's internal format (e.g., from a prior preprocessing step) — skip directly to pipeline execution.
- Spectral data are in non-standard formats with no documented parser in msFeaST; manual converter development may be required first.
- Sample/feature identifiers cannot be reliably aligned across the three input tables — resolve identifier mismatches before engineering data structures.

## Inputs

- quantification table (CSV/TSV or pandas DataFrame with features as rows, samples as columns, abundance values as cells)
- metadata table (CSV/TSV or pandas DataFrame with sample identifiers and experimental annotations)
- spectral data files (format supported by msFeaST I/O, e.g., JSON or custom format with feature-to-spectrum mappings)

## Outputs

- validated quantification DataFrame aligned to feature identifiers
- validated metadata DataFrame aligned to sample identifiers
- intermediate Python dictionary or object mapping features to spectral data
- Python data structures ready for msFeaST pipeline ingestion

## How to apply

Load quantification, metadata, and spectral data files using pandas and custom I/O functions provided in the preprocessing_mushroom_type_comparison.ipynb notebook. Parse each input to validate structure and ensure column/row identifiers align across tables (quantification feature IDs must match spectral feature mappings; metadata sample IDs must match quantification sample columns). Transform and normalize tables into the internal data format expected by msFeaST—this typically involves reshaping DataFrames, converting data types, and mapping identifiers. Generate intermediate Python objects (dictionaries mapping features to spectra, or nested DataFrames) that serve as direct inputs to the msFeaST pipeline. Verify schema compliance by inspecting object keys, data types, and shape before passing to the pipeline.

## Related tools

- **pandas** (Load, parse, validate, and transform quantification and metadata tables into aligned DataFrames with consistent indexing)
- **jupyter-notebook** (Execute preprocessing_mushroom_type_comparison.ipynb to interactively load, inspect, and engineer data structures with user control over filepath arguments) — https://github.com/kevinmildau/msFeaST
- **msFeaST** (Define and consume the validated intermediate Python data structures produced by this engineering step) — https://github.com/kevinmildau/msFeaST

## Examples

```
# In preprocessing_mushroom_type_comparison.ipynb:
import pandas as pd
quant_df = pd.read_csv('path/to/quantification.csv', index_col=0)
meta_df = pd.read_csv('path/to/metadata.csv', index_col=0)
# Validate alignment and generate msFeaST-compatible data structure
```

## Evaluation signals

- All three input tables (quantification, metadata, spectral) load without I/O errors and have consistent encoding and delimiter handling.
- Feature identifiers in the quantification table match those in the spectral data object; sample identifiers in quantification match those in metadata.
- DataFrame shapes and data types are correct: quantification is numeric (float/int), metadata is mixed but consistent, no unexpected NaN or missing values in critical columns.
- Generated intermediate Python objects pass schema validation checks before being passed to the msFeaST pipeline (e.g., nested dictionary keys exist, expected fields are populated).
- The preprocessed data structures can be serialized (e.g., to JSON via the pipeline) and round-trip without loss of precision or identifier fidelity.

## Limitations

- msFeaST preprocessing has been tested on macOS and Linux; Windows support is currently being worked on, so cross-platform reproducibility of this skill may vary.
- The skill requires manual modification of filepath arguments in the Jupyter notebook; no automated file discovery or batch ingestion is documented, limiting scalability to multiple datasets.
- Data validation is implicit and depends on notebook cell execution order; rerunning cells out of order or with modified inputs may produce silently incorrect intermediate structures.
- No changelog is available for the preprocessing notebook, making it difficult to track what input schema changes or fixes may have been applied.

## Evidence

- [other] Load the quantification table, metadata table, and spectral data files from the omsw_pleurotus example dataset using pandas and custom I/O functions in the msFeaST preprocessing notebook.: "Load the quantification table, metadata table, and spectral data files from the omsw_pleurotus example dataset using pandas and custom I/O functions in the msFeaST preprocessing notebook."
- [other] Parse and validate the input data structures to ensure compatibility with msFeaST requirements.: "Parse and validate the input data structures to ensure compatibility with msFeaST requirements."
- [other] Transform and normalize the quantification and metadata tables into the internal data format expected by msFeaST.: "Transform and normalize the quantification and metadata tables into the internal data format expected by msFeaST."
- [other] Generate intermediate Python data structures (dictionaries, DataFrames, or objects) that serve as inputs to the msFeaST pipeline.: "Generate intermediate Python data structures (dictionaries, DataFrames, or objects) that serve as inputs to the msFeaST pipeline."
- [readme] These notebooks contain a complete example of quantification table, metadata table, and spectral data processing required for msFeaST, as well as a complete use-case example. To make use of your own data, change the data filepath arguments to your own data file location and run the pipeline.: "These notebooks contain a complete example of quantification table, metadata table, and spectral data processing required for msFeaST, as well as a complete use-case example. To make use of your own"
