---
name: structured-data-matrix-construction
description: Use when you have raw LipidSearch or LIQUID output files (CSV or TSV
  format) containing lipid identifiers and quantification columns (relative intensity
  or area values), and need to construct a clean, analyzable data matrix with consistent
  lipid nomenclature and no missing values in critical fields.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3407
  tools:
  - ADViSELipidomics
  - LipidSearch
  - LIQUID
  - LIPID MAPS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btac706
  title: ADViSELipidomics
evidence_spans:
- ADViSELipidomics can normalize the data matrix, providing absolute values of concentration
  per lipid and sample
- ADViSELipidomics is a novel Shiny app for the preprocessing, analysis, and visualization
  of lipidomics data.
- outputs from LipidSearch and LIQUID for lipid identification and quantification
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_adviselipidomics_cq
    doi: 10.1093/bioinformatics/btac706
    title: ADViSELipidomics
  dedup_kept_from: coll_adviselipidomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac706
  all_source_dois:
  - 10.1093/bioinformatics/btac706
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# structured-data-matrix-construction

## Summary

Transforms raw lipidomics instrument outputs (LipidSearch, LIQUID CSV/TSV files) into a validated, row-normalized data matrix with lipid species as rows and sample measurements as columns, using LIPID MAPS nomenclature to parse and standardize lipid identifiers.

## When to use

You have raw LipidSearch or LIQUID output files (CSV or TSV format) containing lipid identifiers and quantification columns (relative intensity or area values), and need to construct a clean, analyzable data matrix with consistent lipid nomenclature and no missing values in critical fields before performing statistical analysis, normalization, or differential abundance testing.

## When NOT to use

- Input data are already in validated matrix format (rows and columns already correspond to lipid species and samples with no missing critical values).
- Lipid identifiers are already standardized and the file is already structured as a feature table with no parsing required.
- Input is from a different lipidomics platform (e.g., raw MS data, mzML, or non-LipidSearch/LIQUID proprietary formats) that requires different parsing logic.

## Inputs

- LipidSearch output file (CSV or TSV format)
- LIQUID output file (CSV or TSV format)
- Quantification column(s) with relative intensity or area values
- Lipid species identifier column(s) with nomenclature requiring standardization

## Outputs

- Structured lipid species data matrix (rows = lipid species, columns = samples)
- Validated metadata: row count, column count, missing value report
- Standardized lipid identifiers using LIPID MAPS nomenclature
- Quantification matrix ready for normalization or statistical analysis

## How to apply

Load the LipidSearch or LIQUID CSV/TSV file while preserving lipid identifiers and quantification columns. Parse each lipid species name to extract structural information (chain length, saturation, class) by applying LIPID MAPS classification rules to standardize nomenclature. Construct a matrix with lipid species as rows and sample measurements (relative intensity or area) as columns. Validate matrix integrity by confirming no missing values in metabolite identifier and quantification fields, and verify that row and column counts match input file dimensions. If internal lipid standards are present in the experiment, the matrix is ready for downstream normalization to absolute concentration values.

## Related tools

- **ADViSELipidomics** (Shiny application that implements this skill: loads LipidSearch/LIQUID outputs, parses lipid species using LIPID MAPS classification, and constructs structured data matrices for downstream analysis and visualization.) — https://github.com/ShinyFabio/ADViSELipidomics
- **LipidSearch** (Proprietary lipidomics identification and quantification software whose output format (CSV/TSV) is parsed and structured by this skill.)
- **LIQUID** (Open-source lipidomics identification and quantification software whose output format (CSV/TSV) is parsed and structured by this skill.)
- **LIPID MAPS** (Classification system and nomenclature standard used to parse and standardize lipid species identifiers extracted from instrument output.) — https://www.lipidmaps.org/

## Examples

```
library("ADViSELipidomics"); run_ADViSELipidomics()  # Load and parse LipidSearch/LIQUID CSV, construct validated matrix via Shiny UI
```

## Evaluation signals

- Matrix dimensions are consistent: number of rows equals unique lipid species in input file; number of columns equals number of sample measurements.
- No missing values in critical identifier columns (lipid species names) and quantification columns (relative intensity/area values).
- All lipid identifiers have been parsed and standardized according to LIPID MAPS nomenclature (e.g., consistent class notation, chain length and saturation syntax).
- Quantification values are numeric and non-negative, with no unexpected characters or formatting artifacts from raw output.
- Row and column order matches input file after parsing; spot-checks of sample names and lipid IDs against original output confirm data integrity.

## Limitations

- The skill depends on correct and complete LIPID MAPS classification rules; lipid species with non-standard or ambiguous nomenclature may fail to parse or be classified incorrectly.
- Performance and usability depend on screen size and monitor resolution; the ADViSELipidomics interface may display differently on smaller or lower-resolution monitors.
- The skill requires exact formatting of input CSV/TSV files; malformed or corrupted files may fail during file reading or parsing steps.
- Internal lipid standards must be explicitly marked in the input file to enable absolute concentration normalization; their absence limits the matrix to relative quantification.

## Evidence

- [other] File format and parsing method: "Load the LipidSearch or LIQUID output file (CSV or TSV format) using a file reader that preserves lipid identifiers and quantification columns."
- [other] LIPID MAPS standardization: "Parse lipid species names and extract structural information (chain length, saturation, class) using LIPID MAPS nomenclature classification."
- [other] Matrix construction and structure: "Construct a structured data matrix with rows as lipid species and columns as sample measurements, retaining metabolite identifiers and relative intensity or area values."
- [other] Validation and integrity checks: "Validate matrix integrity: confirm no missing values in critical identifier and quantification fields, and verify row and column counts match input file dimensions."
- [readme] Tool implementation and supported formats: "ADViSELipidomics is a novel Shiny app for the preprocessing, analysis, and visualization of lipidomics data. It copes with the outputs from LipidSearch and LIQUID for lipid identification and"
