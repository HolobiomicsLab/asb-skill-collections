---
name: otl-identifier-assignment
description: Use when after organism name cleaning and taxonomy verification (4_cleaningTaxonomy.R) have been completed and you have a cleaned organism table with standardized names.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3050
  tools:
  - R
  - 5_addingOTL.R
  - 4_cleaningTaxonomy.R
  - Open Tree of Life
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- standardizing.R, 1_integrating.R, 1_cleaningOriginal.R, 4_cleaningTaxonomy.R, 5_addingOTL.R
- 1_integrating.R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.7554/eLife.70780
  all_source_dois:
  - 10.7554/eLife.70780
  - 10.1007/s00044-016-1764-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# otl-identifier-assignment

## Summary

Maps cleaned organism names to Open Tree of Life (OTL) taxonomic identifiers and annotations. This enrichment step adds standardized phylogenetic context to organism records, enabling downstream comparative and validation workflows in natural products research.

## When to use

Apply this skill after organism name cleaning and taxonomy verification (4_cleaningTaxonomy.R) have been completed and you have a cleaned organism table with standardized names. Use it when you need to add OTL identifiers and associated taxonomic annotations to support phylogenetic analysis, cross-database organism validation, or downstream curation steps that require standardized taxonomic identifiers.

## When NOT to use

- Organism names have not yet been cleaned or standardized — run 4_cleaningTaxonomy.R first to resolve synonyms and correct nomenclatural errors.
- You require only raw organism name matching without taxonomic validation — simpler string-matching or exact-lookup approaches are more efficient.
- Your downstream workflow does not require phylogenetic context or cross-database organism reconciliation — OTL enrichment adds overhead without benefit.

## Inputs

- interim/tables/2_cleaned/organism/cleaned.tsv.gz (cleaned organism table with standardized names)
- Open Tree of Life API or reference taxonomic database

## Outputs

- interim/dictionaries/organism/otl.sqlite (OTL-enriched organism dictionary in SQLite format)
- interim/dictionaries/organism/*.tsv.gz (OTL-enriched organism dictionary in compressed tabular format with identifiers and annotations)

## How to apply

Load the cleaned organism table from interim/tables/2_cleaned/organism/cleaned.tsv.gz. Execute the 5_addingOTL.R script, which maps each cleaned organism name to Open Tree of Life taxonomic identifiers using OTL API calls or local taxonomic reference data. The script processes organism records iteratively, resolving ambiguous names through fuzzy matching or user-guided curation where needed. Output the enriched organism dictionary to interim/dictionaries/organism/otl.sqlite in SQLite format along with accompanying .tsv.gz files containing mapped OTL identifiers, taxonomic rank annotations, and confidence scores for each organism entry.

## Related tools

- **5_addingOTL.R** (R script that executes OTL identifier mapping and enrichment on the cleaned organism table) — https://github.com/lotusnprod/lotus-processor
- **4_cleaningTaxonomy.R** (Upstream R script that cleans and verifies organism taxonomy before OTL mapping) — https://github.com/lotusnprod/lotus-processor
- **Open Tree of Life** (External taxonomic reference API and database used to resolve organism names to standardized identifiers) — https://tree.opentreeoflife.org/

## Examples

```
Rscript 5_addingOTL.R --input interim/tables/2_cleaned/organism/cleaned.tsv.gz --output interim/dictionaries/organism/
```

## Evaluation signals

- All organism entries in the input cleaned.tsv.gz have corresponding OTL identifier assignments in the output .sqlite or .tsv.gz files with no null or missing values for valid organism names.
- OTL identifiers are valid, resolvable identifiers matching the Open Tree of Life taxonomy (e.g., ott_id format).
- Mapping confidence or match quality scores (if present) are reasonable and clustered appropriately (e.g., high-confidence exact matches vs. fuzzy matches with lower scores).
- The output .sqlite database schema matches expected organism dictionary structure with columns for organism name, OTL identifier, taxonomic rank, and annotation metadata.
- Spot-check: a sample of 10–20 organism names from the input can be manually verified against the OTL web interface to confirm identifier correctness and annotation consistency.

## Limitations

- OTL coverage is incomplete for some organisms, particularly rare or newly described species; unmapped organisms may require manual curation or fallback to alternative taxonomic sources.
- Fuzzy matching and name resolution can introduce false positives when organism names are ambiguous or homonymous across kingdoms (e.g., genus names shared between plants and fungi).
- The 5_addingOTL.R script depends on stable OTL API availability and taxonomy version; changes to the OTL API or taxonomy release may require script updates or version pinning.
- Performance scales with organism table size; large datasets (>10,000 unique organisms) may require batching or caching strategies to avoid timeouts during OTL API queries.

## Evidence

- [methods] Organism taxonomy enrichment via OTL integration: "The 5_addingOTL.R script processes the cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) to map organism names to Open Tree of Life identifiers"
- [methods] OTL output format and location: "producing an OTL-enriched organism dictionary output in interim/dictionaries/organism/"
- [methods] Workflow integration after taxonomy cleaning: "Execute 5_addingOTL.R to map cleaned organism names to OTL taxonomic identifiers and annotations"
- [methods] Output file formats: "Write the enriched organism dictionary to interim/dictionaries/organism/otl.sqlite and associated output files (.tsv.gz format)"
- [readme] LOTUS organism scope: "LOTUS is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented"
