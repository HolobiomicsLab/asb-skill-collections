---
name: file-format-standardization
description: Use when when you have raw outputs from LipidSearch or LIQUID identification
  software (CSV or TSV format with vendor-specific column naming and lipid identifiers)
  and need to construct a structured data matrix suitable for batch normalization,
  statistical testing, or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0091
  tools:
  - ADViSELipidomics
  - LipidSearch
  - LIQUID
  - LIPID MAPS
  - metabolomicsWorkbenchR
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

# file-format-standardization

## Summary

Convert vendor-specific lipidomics output formats (LipidSearch, LIQUID) into a standardized tabular data matrix with consistent lipid nomenclature, sample identifiers, and quantification columns. This enables downstream statistical and exploratory analysis within a unified computational framework.

## When to use

When you have raw outputs from LipidSearch or LIQUID identification software (CSV or TSV format with vendor-specific column naming and lipid identifiers) and need to construct a structured data matrix suitable for batch normalization, statistical testing, or visualization. Specifically when you must map heterogeneous lipid species names to a common classification standard (LIPID MAPS) before pooling data from multiple instruments or experiments.

## When NOT to use

- Input is already a pre-processed feature table with normalized or log-transformed values where lipid identifiers are already standardized.
- Lipid identifiers do not follow recognizable nomenclature patterns that LIPID MAPS classification can parse (e.g., arbitrary hash IDs without structural annotation).
- Input data is from non-targeted metabolomics workflows using different classification schemes incompatible with LIPID MAPS.

## Inputs

- LipidSearch output file (CSV or TSV format)
- LIQUID output file (CSV or TSV format)
- Metabolomics Workbench lipidomic experiment (via do_query() function)
- Sample metadata table with identifiers

## Outputs

- Standardized lipid species data matrix (rows = lipids, columns = samples)
- Lipid identifier column with LIPID MAPS-parsed nomenclature
- Quantification matrix (relative intensity or area values)
- Validated matrix with integrity checks passed

## How to apply

Load the LipidSearch or LIQUID output file as CSV or TSV, preserving lipid identifiers and quantification columns. Parse lipid species names using LIPID MAPS nomenclature classification to extract structural information (chain length, saturation, class). Construct a structured matrix with lipid species as rows and sample measurements (relative intensity or area values) as columns. Retain metabolite identifiers and quantification columns throughout. Validate matrix integrity by confirming no missing values in critical identifier and quantification fields, verifying row and column counts match input file dimensions, and checking that all lipid names conform to LIPID MAPS terminology.

## Related tools

- **ADViSELipidomics** (Shiny application that orchestrates file loading, parsing, and matrix construction for LipidSearch and LIQUID outputs) — https://github.com/ShinyFabio/ADViSELipidomics
- **LipidSearch** (Generates vendor-specific lipidomics identification and quantification output consumed by this standardization workflow)
- **LIQUID** (Generates vendor-specific lipidomics identification and quantification output consumed by this standardization workflow)
- **LIPID MAPS** (Provides nomenclature classification standard used to parse and map heterogeneous lipid species names)
- **metabolomicsWorkbenchR** (Enables real-time download of lipidomic experiments from Metabolomics Workbench repository using do_query() function)

## Examples

```
library("ADViSELipidomics")
run_ADViSELipidomics()
```

## Evaluation signals

- No missing values in critical identifier and quantification fields after parsing.
- Row count and column count of output matrix match input file dimensions.
- All lipid species names conform to LIPID MAPS nomenclature (e.g., format like 'TG(18:0_18:1_18:2)' or 'PC(O-16:0/18:1)').
- Sample columns correctly preserve quantification values (relative intensity or area) with no unintended data transformation or loss of significant figures.
- Metabolite identifiers are unique and consistently formatted across the standardized matrix.

## Limitations

- Parsing accuracy depends on lipid nomenclature consistency in the vendor output; malformed or non-standard lipid names may not map correctly to LIPID MAPS classification.
- The tool assumes internal lipid standards are optional; quantification remains relative intensity if no internal standards are provided; absolute concentration normalization requires explicit standard specification.
- Resolution and display of the Shiny interface may vary depending on screen size and monitor resolution, requiring manual zoom adjustment (Ctrl +/- or Command +/-).
- Docker deployment requires appropriate system resources and Internet connection for initial image pull; local installation may require OS-specific system dependencies (Rtools on Windows, cairo on macOS, build tools on Ubuntu).

## Evidence

- [intro] Parsing and matrix construction methodology: "ADViSELipidomics copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification, and with data available from the Metabolomics Workbench. ADViSELipidomics extracts"
- [other] Standardized matrix structure and validation: "Construct a structured data matrix with rows as lipid species and columns as sample measurements, retaining metabolite identifiers and relative intensity or area values. 4. Validate matrix integrity:"
- [other] File format support and parsing workflow: "Load the LipidSearch or LIQUID output file (CSV or TSV format) using a file reader that preserves lipid identifiers and quantification columns. 2. Parse lipid species names and extract structural"
- [readme] Installation and usage invocation: "Once the installation is completed, run: library("ADViSELipidomics") run_ADViSELipidomics()"
