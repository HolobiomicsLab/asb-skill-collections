---
name: lipid-species-classification-mapping
description: Use when you have a table of lipid species names or identifiers output from LipidSearch or LIQUID (with associated quantification data) and need to annotate each lipid with its standardized LIPID MAPS classification (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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
- parsing lipid species (using LIPID MAPS classification)
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

# lipid-species-classification-mapping

## Summary

Map parsed lipid species identifiers to standardized LIPID MAPS taxonomic classifications (category and subcategory), enabling consistent annotation and downstream comparative analysis of lipidomics data. This skill bridges raw lipid identifiers from identification tools with a controlled vocabulary for biological interpretation.

## When to use

You have a table of lipid species names or identifiers output from LipidSearch or LIQUID (with associated quantification data) and need to annotate each lipid with its standardized LIPID MAPS classification (e.g., Glycerophospholipids → Phosphatidylcholines) to enable cross-study comparison, category-level filtering, or reporting against a unified lipid taxonomy.

## When NOT to use

- Lipid identifiers are already annotated with LIPID MAPS classifications — mapping would be redundant.
- You require lipid structural detail beyond category/subcategory (e.g., fatty acid composition or regioisomer information) — this skill provides taxonomic classification only, not structural decomposition.
- Your workflow uses a custom or non-standard lipid nomenclature that is not resolvable against LIPID MAPS — alternative ontologies or manual curation would be needed.

## Inputs

- Parsed lipid species table (CSV/TSV) with lipid identifiers and quantification data from LipidSearch or LIQUID output
- LIPID MAPS database or API access

## Outputs

- Annotated lipid species table with LIPID MAPS category and subcategory fields appended to each lipid row
- Mapping report indicating successful and failed classification lookups

## How to apply

Load the parsed lipid species table containing lipid names or identifiers from LipidSearch or LIQUID. For each lipid species, query the LIPID MAPS database or API to retrieve its assigned category (e.g., Glycerophospholipids, Sphingolipids) and subcategory (e.g., Phosphatidylcholines, Ceramides). Append the classification fields as new columns to the original species table, preserving all quantitative data. Validate that all lipid identifiers successfully mapped to LIPID MAPS entries; unmapped lipids should be flagged for manual review or exclusion. Save the annotated table with lipid names, original quantification columns, and classification fields intact.

## Related tools

- **LIPID MAPS** (Database and API for querying lipid species and retrieving standardized taxonomic classifications (category, subcategory) used to annotate parsed lipid identifiers.)
- **LipidSearch** (Upstream lipid identification and quantification tool producing raw lipid species output that serves as input to this mapping skill.)
- **LIQUID** (Alternative upstream lipid identification and quantification tool producing raw lipid species output compatible with this mapping workflow.)
- **ADViSELipidomics** (Shiny application integrating this mapping skill within a full preprocessing and analysis pipeline for lipidomics data.) — https://github.com/ShinyFabio/ADViSELipidomics

## Evaluation signals

- All lipid identifiers in the input table map to exactly one LIPID MAPS entry (no ambiguous or duplicate classifications).
- Classification fields (category, subcategory) are non-empty and match LIPID MAPS controlled vocabulary; no null or invalid values in mapped rows.
- Row count of output table equals input table (1:1 retention of all lipid species, with no rows dropped or duplicated during mapping).
- Quantification columns in the original table are preserved without modification or reordering in the output annotated table.
- A mapping report or log documents the number of successful mappings and any failed lookups, with identifiers of unmapped species for manual review.

## Limitations

- Mapping depends on exact or fuzzy matching of lipid identifiers against LIPID MAPS nomenclature; non-standard or misspelled lipid names may fail to resolve.
- LIPID MAPS database is periodically updated; mappings generated at different points in time may yield different classifications for the same lipid identifier if nomenclature or taxonomy changes.
- This skill provides only high-level category and subcategory classification; it does not decompose lipid structures into individual fatty acid chains or positional isomers.
- Isobaric or isomeric lipid species may receive identical classifications, potentially obscuring important structural differences in downstream analysis.

## Evidence

- [other] Map each lipid species name to its corresponding LIPID MAPS classification using the LIPID MAPS database or API, extracting the category (e.g., Glycerophospholipids, Sphingolipids) and subcategory (e.g., Phosphatidylcholines).: "Map each lipid species name to its corresponding LIPID MAPS classification using the LIPID MAPS database or API, extracting the category (e.g., Glycerophospholipids, Sphingolipids) and subcategory"
- [readme] ADViSELipidomics extracts information by parsing lipid species (using LIPID MAPS classification): "ADViSELipidomics extracts information by parsing lipid species (using LIPID MAPS classification)"
- [other] Load the parsed lipid species table (output from lipid identification tools such as LipidSearch or LIQUID) containing lipid names or identifiers.: "Load the parsed lipid species table (output from lipid identification tools such as LipidSearch or LIQUID) containing lipid names or identifiers."
- [other] Append the classification fields to the parsed species table. Save the annotated table with lipid names, original quantitative data, and classification fields.: "Append the classification fields to the parsed species table. Save the annotated table with lipid names, original quantitative data, and classification fields."
