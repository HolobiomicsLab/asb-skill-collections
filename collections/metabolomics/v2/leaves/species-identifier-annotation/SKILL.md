---
name: species-identifier-annotation
description: Use when you have a parsed lipid species table output from LipidSearch
  or LIQUID containing lipid names or identifiers and their quantitative measurements,
  but lack standardized taxonomic annotation (e.g., Glycerophospholipids, Phosphatidylcholines).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3172
  tools:
  - ADViSELipidomics
  - LIPID MAPS
  - LipidSearch
  - LIQUID
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

# Reconstruct LIPID MAPS classification annotation of parsed lipid species

## Summary

Map parsed lipid species identifiers to standardized LIPID MAPS taxonomic classifications (category and subcategory) and append those annotations to the quantitative species table. This enriches raw lipid identifications with systematic, reusable taxonomic context.

## When to use

You have a parsed lipid species table output from LipidSearch or LIQUID containing lipid names or identifiers and their quantitative measurements, but lack standardized taxonomic annotation (e.g., Glycerophospholipids, Phosphatidylcholines). Use this skill before performing differential abundance analysis or lipid class–level summarization to enable systematic filtering and comparison.

## When NOT to use

- Input lipid identifiers are already mapped to LIPID MAPS classifications — skip this skill and proceed directly to downstream analysis.
- Lipid species names are ambiguous or non-standard and cannot be reliably resolved by LIPID MAPS — consider curating names manually or using alternative classification schemes first.
- You require custom, non-LIPID-MAPS taxonomic annotation — this skill is specific to LIPID MAPS and will not produce alternative classification systems.

## Inputs

- Parsed lipid species table (LipidSearch or LIQUID output format)
- Lipid species names or identifiers column
- Quantitative data (e.g., peak areas, concentrations per sample)

## Outputs

- Annotated lipid species table with LIPID MAPS category field
- Annotated lipid species table with LIPID MAPS subcategory field
- Mapping success/failure report (matched vs. unmatched identifiers)

## How to apply

Load the parsed lipid species table (rows = lipid species, columns = lipid names/identifiers plus quantitative data from LipidSearch or LIQUID). For each lipid species name, query the LIPID MAPS database or API to retrieve its category (e.g., Glycerophospholipids, Sphingolipids) and subcategory (e.g., Phosphatidylcholines, Ceramides). Append two or more classification columns to the original table. Verify that all lipid names successfully map to LIPID MAPS entries; unmatched names should be flagged for manual review or alternative identifier lookup. Save the annotated table with lipid identities, original quantitative data, and classification fields intact for downstream analysis.

## Related tools

- **ADViSELipidomics** (Shiny application that executes LIPID MAPS parsing and annotation workflow on imported LipidSearch or LIQUID species tables) — https://github.com/ShinyFabio/ADViSELipidomics
- **LIPID MAPS** (Reference database and API queried to resolve lipid species names to standardized category and subcategory classifications)
- **LipidSearch** (Upstream lipid identification and quantification tool producing parsed species table input)
- **LIQUID** (Upstream lipid identification and quantification tool producing parsed species table input)

## Examples

```
library('ADViSELipidomics'); run_ADViSELipidomics() # Upload LipidSearch .csv; navigate to 'Lipid Annotation' tab; map species to LIPID MAPS; download annotated table.
```

## Evaluation signals

- All lipid species names in the input table have been assigned a LIPID MAPS category and subcategory; no unmapped rows remain (or unmapped rows are explicitly flagged).
- Classification columns contain valid LIPID MAPS terms matching the official taxonomy (e.g., 'Glycerophospholipids', 'Phosphatidylcholines') — spot-check a random sample against LIPID MAPS website.
- Row count and quantitative data columns are identical before and after annotation; no samples or quantitative values were lost or altered.
- Annotated table can be loaded and partitioned by category and subcategory in downstream analyses (e.g., summed by lipid class in ADViSELipidomics); no schema errors or missing values prevent grouping.
- If a manual validation set exists, percentage of correctly mapped lipid species matches expected accuracy (e.g., > 95% for standard nomenclature).

## Limitations

- Lipid species names that deviate from LIPID MAPS standard nomenclature or use non-standard abbreviations may fail to map; mapping success depends on input name quality and currency of the LIPID MAPS reference.
- LIPID MAPS API or database access may be unavailable or rate-limited during bulk queries, necessitating fallback to cached or offline LIPID MAPS snapshots.
- Newly discovered or non-canonical lipid species not yet in LIPID MAPS cannot be classified; such cases require manual curation or supplementary metadata.
- The annotation workflow does not assign additional metadata (e.g., charge, adduct, ionization mode) beyond LIPID MAPS category/subcategory; further enrichment requires additional tools.

## Evidence

- [intro] Mapping each lipid species name to LIPID MAPS classification: "Map each lipid species name to its corresponding LIPID MAPS classification using the LIPID MAPS database or API, extracting the category (e.g., Glycerophospholipids, Sphingolipids) and subcategory"
- [readme] ADViSELipidomics executes this workflow on LipidSearch or LIQUID output: "It copes with the outputs from LipidSearch and LIQUID for lipid identification and quantification, and with data available from the Metabolomics Workbench. ADViSELipidomics extracts information by"
- [intro] Annotation appended to quantitative table: "Append the classification fields to the parsed species table. Save the annotated table with lipid names, original quantitative data, and classification fields."
- [intro] Input source format: "Load the parsed lipid species table (output from lipid identification tools such as LipidSearch or LIQUID) containing lipid names or identifiers."
