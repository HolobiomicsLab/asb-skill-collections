---
name: metabolomics-peak-table-loading
description: Use when you have raw peak tables exported from a tandem mass spectrometry preprocessing tool (e.g. Progenesis, MS-DIAL, or Bruker Metaboscape) and need to integrate them with sample metadata for reproducibility filtering, mispicked-ion removal, or group-based feature exclusion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - R
  - data.table
  - mpactr
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1128/mra.00997-24
  title: mpactr
- doi: 10.1021/acs.analchem.2c04632
  title: ''
evidence_spans:
- This table can be used for a variety of analyses that can be conducted in R
- library(data.table)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr
    doi: 10.1128/mra.00997-24
    title: mpactr
  dedup_kept_from: coll_mpactr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1128/mra.00997-24
  all_source_dois:
  - 10.1128/mra.00997-24
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-peak-table-loading

## Summary

Load preprocessed metabolomics peak tables and associated sample metadata from vendor-specific formats (e.g. Progenesis) into an R data object suitable for downstream filtering and statistical analysis. This is the foundational step that ingests MS1 feature abundance matrices and sample annotations before quality-control filtering.

## When to use

You have raw peak tables exported from a tandem mass spectrometry preprocessing tool (e.g. Progenesis, MS-DIAL, or Bruker Metaboscape) and need to integrate them with sample metadata for reproducibility filtering, mispicked-ion removal, or group-based feature exclusion. Use this skill at the start of a metabolomics analysis pipeline when you must load and structure heterogeneous vendor formats into a unified R object.

## When NOT to use

- Peak table is already loaded in R memory and validated — use this skill only when ingesting from disk.
- Input is in a non-standardized or custom format not supported by import_data() — you will need custom parsing or format conversion first.
- You have already applied filters (e.g. mispicked-ion, group, or CV filters) to the table — this skill is for raw, unfiltered imports only.

## Inputs

- peak_table.csv (vendor-specific format: Progenesis, MS-DIAL MSP, Bruker Metaboscape, or GNPS FBMN export)
- metadata.csv (sample annotations: sample name, group, technical replicate identifier)

## Outputs

- R6 mpactr data object (peak abundance matrix + feature metadata + sample annotations)
- imported_peak_table (data.table or data.frame with features as rows, samples as columns, abundances as values)
- imported_metadata (data.frame with sample names, group assignments, replicate identifiers)

## How to apply

Call import_data() with the file path to the peak table (CSV or vendor-specific format) and specify the format parameter (e.g. format='Progenesis') to parse vendor-specific column schemas and m/z, retention time, and abundance metadata. Simultaneously load the sample metadata file (typically a CSV with sample names, group assignments, and technical replicate identifiers) using the same import_data() call or a separate invocation. The function returns an R6 object (via mpactr) that stores the peak abundance matrix, feature metadata (m/z, RT), and sample annotations in a structured, reference-semantic container. Verify that row counts match the expected number of MS1 features detected and that all samples from your study are represented with correct group labels before proceeding to filtering steps.

## Related tools

- **mpactr** (provides import_data() function to parse vendor-specific metabolomics peak table formats and return R6 object with reference semantics for in-place filtering) — https://github.com/mums2/mpactr
- **data.table** (underlying storage and manipulation of imported peak abundance matrices and feature metadata)
- **R** (runtime environment for import_data() and downstream mpactr filter operations)

## Examples

```
library(mpactr); data <- import_data(example_path('cultures_peak_table.csv'), format='Progenesis'); metadata <- read.csv(example_path('cultures_metadata.csv')); str(data)
```

## Evaluation signals

- Imported peak table row count matches the number of detected MS1 features in the vendor preprocessing report (e.g. 7269 ions for the cultures dataset)
- Column count equals number of samples in the study; all sample names in the table match the metadata file
- Feature metadata columns (m/z, retention time, intensity, isotopic pattern flags) are present and numeric; no missing values in critical fields
- Sample group assignments from metadata are correctly attached to each sample column; verify by spot-checking 3–5 samples across different groups
- R6 object is instantiated and reference-semantic: verify by calling str() or inspecting object class; confirm copy_object parameter is available for downstream filter operations

## Limitations

- import_data() supports only vendor formats explicitly documented in mpactr (Progenesis, MS-DIAL MSP, Bruker Metaboscape, GNPS FBMN); custom vendor formats or non-standard delimiters require custom parsing or preprocessing
- Metadata file must be a single CSV with one row per sample and consistent column naming; complex experimental designs (e.g. nested batches, multi-level replicates) may require manual annotation or preprocessing
- Row or column count mismatches between peak table and metadata are not automatically reconciled; manual curation is required if sample names or feature IDs do not align exactly
- No validation against external databases or in-source fragmentation patterns occurs during import; quality checking is deferred to downstream filters (filter_mispicked_ions, filter_insource_ions, etc.)

## Evidence

- [methods] import_data() function signature and format parameter: "Load cultures peak table and metadata using import_data() with format='Progenesis'"
- [abstract] reference semantics and copy_object parameter behavior: "operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory"
- [methods] mpactr library and data.table usage: "library(mpactr)
... library(data.table)"
- [methods] example data files and their schema: "import_data(example_path("cultures_peak_table.csv")
found on [GitHub](https://github.com/BalunasLab/mpact/tree/main/rawdata/PTY087I2)"
- [readme] support for multiple vendor formats in MPACT desktop tool: "Added support for Bruker Metaboscape peak lists
- Added support for MS-DIAL MSP files"
