---
name: mass-spectrometry-quantification-extraction
description: Use when you have raw LipidSearch or LIQUID output files (CSV or TSV format) containing lipid identifiers and per-sample quantification measurements, and you need to convert them into a machine-readable data matrix for downstream statistical analysis, normalization, or differential abundance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - ADViSELipidomics
  - LipidSearch
  - LIQUID
  - LIPID MAPS
derived_from:
- doi: 10.1093/bioinformatics/btac706
  title: ADViSELipidomics
evidence_spans:
- ADViSELipidomics can normalize the data matrix, providing absolute values of concentration per lipid and sample
- ADViSELipidomics is a novel Shiny app for the preprocessing, analysis, and visualization of lipidomics data.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-quantification-extraction

## Summary

Extract and structure lipid quantification measurements (relative intensity or area values) from mass spectrometry–based lipid identification outputs (LipidSearch, LIQUID) into a validated data matrix with lipid species as rows and sample measurements as columns.

## When to use

You have raw LipidSearch or LIQUID output files (CSV or TSV format) containing lipid identifiers and per-sample quantification measurements, and you need to convert them into a machine-readable data matrix for downstream statistical analysis, normalization, or differential abundance testing.

## When NOT to use

- Input is already a preprocessed, validated feature table or abundance matrix — skip directly to normalization or statistical analysis.
- Lipid identifiers do not conform to LIPID MAPS nomenclature and cannot be reliably parsed into structural components.
- Quantification data is already absolute concentration values (not relative intensity/area); normalization via internal standards would be inappropriate.

## Inputs

- LipidSearch output file (CSV or TSV format with lipid identifiers and quantification columns)
- LIQUID output file (CSV or TSV format with lipid identifiers and quantification columns)
- Sample metadata (optional, for sample-level annotation)

## Outputs

- Lipid species quantification data matrix (rows = lipid species, columns = samples)
- Parsed lipid identifiers with LIPID MAPS structural annotations (chain length, saturation, class)
- Validation report confirming matrix integrity and dimensional consistency

## How to apply

Load the LipidSearch or LIQUID output file using a file reader that preserves lipid identifiers and quantification columns. Parse lipid species names to extract structural information (chain length, saturation, class) using LIPID MAPS nomenclature classification, which ADViSELipidomics applies to standardize lipid naming conventions. Construct a structured data matrix with rows indexed by lipid species identifiers and columns representing individual samples, populating cells with relative intensity or area values. Validate matrix integrity by confirming no missing values in critical identifier and quantification fields, and verifying that row and column counts match the dimensions of the input file. This structured output enables subsequent normalization (if internal standards are present), batch effect correction, and statistical testing for differentially abundant lipids.

## Related tools

- **ADViSELipidomics** (Shiny application that loads LipidSearch/LIQUID outputs, parses lipid species using LIPID MAPS, and constructs quantification matrices) — https://github.com/ShinyFabio/ADViSELipidomics
- **LipidSearch** (Mass spectrometry lipid identification and quantification software; produces output files consumed by this skill)
- **LIQUID** (Mass spectrometry lipid identification and quantification software; produces output files consumed by this skill)
- **LIPID MAPS** (Lipid nomenclature classification system used to parse and standardize lipid species identifiers)

## Examples

```
library("ADViSELipidomics"); run_ADViSELipidomics()
```

## Evaluation signals

- Data matrix has no missing values in identifier and quantification columns; confirmed via validation report.
- Row count equals the number of unique lipid species in the input file; column count matches the number of samples.
- Parsed lipid identifiers successfully resolve to valid LIPID MAPS structural annotations (class, chain length, saturation); spot-check a random sample of 5–10 lipids.
- Quantification values are numeric, positive, and span the expected range for relative intensity or area measurements (no negative or zero-only columns).
- Downstream analyses (normalization, differential abundance testing) execute without errors and produce expected statistical distributions.

## Limitations

- Lipid identifiers that do not follow LIPID MAPS nomenclature cannot be reliably parsed; manually curated identifiers or vendor-specific formats may fail.
- Missing or corrupted quantification values in the input file will propagate into the matrix; preprocessing to handle sparse or incomplete data is not addressed by this skill.
- The skill assumes quantification columns represent relative measurements (intensity or area); absolute concentration values require normalization via internal standards, which is a separate workflow step.
- Performance and interface layout may vary depending on screen size and monitor resolution, requiring manual zoom adjustment (Ctrl +/– or Command +/–).

## Evidence

- [intro] Loading and parsing quantification data: "Load the LipidSearch or LIQUID output file (CSV or TSV format) using a file reader that preserves lipid identifiers and quantification columns."
- [intro] LIPID MAPS-based lipid nomenclature parsing: "Parse lipid species names and extract structural information (chain length, saturation, class) using LIPID MAPS nomenclature classification."
- [intro] Data matrix construction with rows and columns: "Construct a structured data matrix with rows as lipid species and columns as sample measurements, retaining metabolite identifiers and relative intensity or area values."
- [intro] Matrix validation and integrity checks: "Validate matrix integrity: confirm no missing values in critical identifier and quantification fields, and verify row and column counts match input file dimensions."
- [readme] Tool capability for handling multiple output formats: "It copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification, and with data available from the Metabolomics Workbench."
