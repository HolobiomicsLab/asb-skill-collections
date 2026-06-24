---
name: tandem-ms-feature-table-import-and-parsing
description: Use when when you have raw feature tables exported from a tandem LC-MS/MS
  preprocessing tool (e.g., Progenesis QI, MS-DIAL, Bruker Metaboscape) and need to
  combine them with sample metadata (group assignments, replicate structure) before
  applying feature filtering or quality control workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R
  - data.table
  - mpactr
  - MPACT (Python/Anaconda)
  techniques:
  - LC-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-ms-feature-table-import-and-parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse and load tandem mass spectrometry feature tables (m/z, retention time, abundance) from vendor-specific formats (Progenesis, MS-DIAL, Bruker Metaboscape) into a standardized in-memory object for downstream filtering and analysis. This is the necessary first step before any quality control or statistical analysis can be applied to metabolomics features.

## When to use

When you have raw feature tables exported from a tandem LC-MS/MS preprocessing tool (e.g., Progenesis QI, MS-DIAL, Bruker Metaboscape) and need to combine them with sample metadata (group assignments, replicate structure) before applying feature filtering or quality control workflows. Specifically when you need to enforce consistent feature representation (m/z, retention time, peak area/intensity) across multiple samples and groups.

## When NOT to use

- Input is already an mpactr object or pre-parsed R data structure — skip directly to filtering.
- Data is in non-tabular format (binary mzML, mzXML, or raw instrument files) — use vendor-specific converters (e.g., MSConvert) to export feature tables first.
- Feature table lacks required columns (m/z, retention time, sample abundances) or metadata lacks group/replicate annotations — data must be validated before parsing.

## Inputs

- Feature table CSV (Progenesis QI format: columns = m/z, retention time, per-sample intensity/area)
- Feature table CSV (MS-DIAL MSP or GNPS peak table format)
- Feature table CSV (Bruker Metaboscape format)
- Sample metadata CSV (columns = sample name, group label, replicate ID)

## Outputs

- mpactr R6 object (in-memory feature matrix + metadata, reference semantics)
- Structured data.table or matrix representation (m/z × samples, indexed by feature)
- Parsed group assignments and replicate structure for downstream filtering

## How to apply

Use mpactr::import_data() with the format parameter set to match your preprocessing software output (e.g., format='Progenesis'). Provide the path to the feature table CSV (containing m/z, retention time, and per-sample abundance columns) and a metadata CSV that maps sample names to experimental group labels (e.g., 'Solvent_Blank', 'Media_Blank', 'culture_sample'). The function returns an R6 mpactr object with reference semantics that stores the feature matrix and metadata in-place, avoiding expensive data copies. This object is then passed to downstream filter functions in sequence. Parsing must preserve the original feature identifiers and abundance values for audit traceability.

## Related tools

- **mpactr** (Primary parsing and object creation; provides import_data() function with format detection for Progenesis, MS-DIAL, Bruker, and GNPS inputs) — https://github.com/mums2/mpactr
- **R** (Execution environment and data manipulation (via data.table library))
- **data.table** (Underlying tabular data structure for efficient in-memory storage of feature × sample matrix)
- **MPACT (Python/Anaconda)** (Alternative GUI-based import tool for Progenesis, MS-DIAL, Bruker, and GNPS formats; outputs data suitable for downstream filtering) — https://github.com/BalunasLab/mpact

## Examples

```
mpactr::import_data(system.file('extdata', 'cultures_peak_table.csv', package='mpactr'), metadata_file=system.file('extdata', 'cultures_metadata.csv', package='mpactr'), format='Progenesis')
```

## Evaluation signals

- Returned mpactr object contains all samples as columns and all features as rows, with no missing or NaN values in abundance data.
- Group assignments from metadata are correctly mapped to each sample (verify via object@metadata or inspection of group factor levels).
- m/z and retention time columns are numeric and fall within expected ranges (e.g., m/z > 50 Da; retention time > 0 min).
- Feature counts match the original table (no rows dropped during parsing unless explicitly requested).
- Re-export the parsed data.table and compare column names and first 10 rows to the input CSV to confirm lossless parsing.

## Limitations

- Format parameter must exactly match the preprocessing software (Progenesis, MS-DIAL, Bruker, GNPS); incorrect format choice will fail or produce mis-parsed data.
- Metadata CSV must have consistent sample name spelling and a group column; mismatches between feature table and metadata will cause mapping failures.
- Large feature tables (>50k features × >100 samples) may incur memory overhead despite R6 reference semantics; consider subsetting by m/z or feature quality before import if memory is constrained.
- No built-in validation of chemical feasibility (e.g., retention time order, m/z monotonicity) — user is responsible for assessing input quality.

## Evidence

- [methods] Import cultures_peak_table.csv and cultures_metadata.csv using mpactr::import_data() with format='Progenesis'.: "Import cultures_peak_table.csv and cultures_metadata.csv using mpactr::import_data() with format='Progenesis'"
- [readme] Progenesis, MS-DIAL, and Bruker formats are supported.: "Added support for Bruker Metaboscape peak lists"
- [readme] MS-DIAL MSP and GNPS formats can be imported.: "Added GNPS peak table filtering functionality (experimental, only tested with FBMN export in MS-DIAL)"
- [methods] mpactr operates with reference semantics for in-place data updates.: "operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory,"
- [methods] Data is organized into feature matrix with m/z, retention time, and per-sample abundances.: "The qc_summary() function returns a data.table with compound IDs and filtering status for each ion"
