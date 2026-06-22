---
name: lipid-nomenclature-parsing
description: Use when you have received raw lipid identification output from LipidSearch or LIQUID in CSV or TSV format containing lipid species names or identifiers, and you need to extract their structural components and map them to standardized LIPID MAPS categories before building a quantitative data matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ADViSELipidomics
  - LipidSearch
  - LIQUID
  - LIPID MAPS
  - pandas
  - Python
  - Python regex (re module)
  - Skyline
  - Thermo QExactive HF
  - Agilent QTOF
derived_from:
- doi: 10.1093/bioinformatics/btac706
  title: ADViSELipidomics
- doi: 10.1021/acs.analchem.4c05039
  title: ''
- doi: 10.1038/s41467-020-15960-z
  title: ''
evidence_spans:
- ADViSELipidomics can normalize the data matrix, providing absolute values of concentration per lipid and sample
- ADViSELipidomics is a novel Shiny app for the preprocessing, analysis, and visualization of lipidomics data.
- outputs from LipidSearch and LIQUID for lipid identification and quantification
- parsing lipid species (using LIPID MAPS classification)
- _No usage/docs found._
- streamline various tasks such as data parsing, matching, statistical analysis, and visualization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_adviselipidomics_cq
    doi: 10.1093/bioinformatics/btac706
    title: ADViSELipidomics
  - build: coll_claw_mrm_cq
    doi: 10.1021/acs.analchem.4c05039
    title: CLAW-MRM
  - build: coll_lipidcreator_cq
    doi: 10.1038/s41467-020-15960-z
    title: LipidCreator
  dedup_kept_from: coll_adviselipidomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac706
  all_source_dois:
  - 10.1093/bioinformatics/btac706
  - 10.1021/acs.analchem.4c05039
  - 10.1038/s41467-020-15960-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-nomenclature-parsing

## Summary

Parse lipid species identifiers from LipidSearch or LIQUID outputs and extract structural information (chain length, saturation, lipid class) using LIPID MAPS nomenclature classification. This skill converts free-text or semi-structured lipid names into standardized, machine-readable components for downstream annotation and quantitative analysis.

## When to use

You have received raw lipid identification output from LipidSearch or LIQUID in CSV or TSV format containing lipid species names or identifiers, and you need to extract their structural components and map them to standardized LIPID MAPS categories before building a quantitative data matrix or performing differential abundance analysis.

## When NOT to use

- Input lipid data is already a normalized feature table with pre-computed absolute concentration values—use normalization skills instead
- You are working with non-lipidomics mass spectrometry data (e.g., proteomics, metabolomics of small molecules) where LIPID MAPS nomenclature does not apply
- Lipid identifiers are already mapped to LIPID MAPS classifications and no structural parsing is needed

## Inputs

- LipidSearch output file (CSV or TSV format with lipid species names and quantification columns)
- LIQUID output file (CSV or TSV format with lipid species names and quantification columns)
- Metabolomics Workbench lipidomics experiment data

## Outputs

- Structured lipid species table with rows as lipid species and columns as sample measurements
- Annotated species table with lipid names, quantitative data, and LIPID MAPS classification fields
- Validated data matrix with confirmed structural metadata and no missing values in identifier/quantification fields

## How to apply

Load the LipidSearch or LIQUID output file (CSV or TSV format) preserving lipid identifiers and quantification columns. Parse each lipid species name to extract structural information—chain length, degree of saturation, and lipid class—using LIPID MAPS nomenclature rules. Map each parsed lipid identifier to its corresponding LIPID MAPS classification (e.g., category: Glycerophospholipids, subcategory: Phosphatidylcholines) using the LIPID MAPS database or API. Construct a structured data matrix with rows as lipid species and columns as sample measurements, appending both original identifiers and LIPID MAPS classification fields. Validate matrix integrity by confirming no missing values in critical identifier and classification fields, and verify row and column counts match input file dimensions.

## Related tools

- **LipidSearch** (Primary source of lipid identification and quantification output; produces the raw lipid species names and intensity/area values to be parsed)
- **LIQUID** (Alternative source of lipid identification and quantification output; produces raw lipid species names and intensity/area values to be parsed)
- **LIPID MAPS** (Classification database and nomenclature standard used to map parsed lipid species to standardized categories and subcategories) — https://www.lipidmaps.org/
- **ADViSELipidomics** (Shiny application that implements the parsing workflow and LIPID MAPS annotation as part of its preprocessing pipeline) — https://github.com/ShinyFabio/ADViSELipidomics

## Examples

```
library("ADViSELipidomics"); run_ADViSELipidomics()
```

## Evaluation signals

- All lipid species identifiers in the output matrix are present and correctly parsed from the input file; no identifiers are dropped or truncated
- Structural metadata (chain length, saturation, lipid class) are extracted and consistent with LIPID MAPS nomenclature rules; spot-check 5–10 entries against LIPID MAPS database
- LIPID MAPS category and subcategory fields are populated for all rows; no missing values in classification columns
- Row count of output matrix equals the number of unique lipid species in the input; column count equals the number of samples plus metadata columns
- Quantification columns (area or relative intensity values) are preserved and match the input file; no values are modified during parsing

## Limitations

- Parsing accuracy depends on consistent, standardized lipid nomenclature in the input file; non-standard or malformed lipid names may fail to parse or map incorrectly to LIPID MAPS
- LIPID MAPS database coverage is incomplete for very recently discovered or non-canonical lipid species; novel lipids may not have a corresponding classification entry
- The workflow does not validate the biological plausibility of lipid abundances or detect instrumental artifacts; preprocessing assumes input quantification values are reliable
- Cross-tool compatibility: LipidSearch and LIQUID use slightly different nomenclature conventions; mapping rules may need adjustment for each tool

## Evidence

- [other] Parse lipid species names and extract structural information (chain length, saturation, class) using LIPID MAPS nomenclature classification.: "Parse lipid species names and extract structural information (chain length, saturation, class) using LIPID MAPS nomenclature classification"
- [other] Load the parsed lipid species table (output from lipid identification tools such as LipidSearch or LIQUID) containing lipid names or identifiers.: "Load the parsed lipid species table (output from lipid identification tools such as LipidSearch or LIQUID) containing lipid names or identifiers"
- [other] Map each lipid species name to its corresponding LIPID MAPS classification using the LIPID MAPS database or API, extracting the category (e.g., Glycerophospholipids, Sphingolipids) and subcategory (e.g., Phosphatidylcholines).: "Map each lipid species name to its corresponding LIPID MAPS classification using the LIPID MAPS database or API, extracting the category (e.g., Glycerophospholipids, Sphingolipids) and subcategory"
- [readme] ADViSELipidomics copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification: "ADViSELipidomics copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification"
- [readme] ADViSELipidomics extracts information by parsing lipid species (using LIPID MAPS classification): "ADViSELipidomics extracts information by parsing lipid species (using LIPID MAPS classification)"
