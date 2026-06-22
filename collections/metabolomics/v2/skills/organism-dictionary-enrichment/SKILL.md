---
name: organism-dictionary-enrichment
description: Use when after organism names have been cleaned and standardized (e.g., via 1_cleaningOriginal.R and 4_cleaningTaxonomy.R) but before final integration of organism, structure, and reference data. Use it when you have a cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3050
  tools:
  - R
  - 5_addingOTL.R
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# organism-dictionary-enrichment

## Summary

Enriches cleaned organism names with standardized taxonomic identifiers from the Open Tree of Life (OTL) by mapping organism records to OTL taxonomic annotations and identifiers. This step bridges curated organism nomenclature with a comprehensive, externally-maintained reference taxonomy.

## When to use

Apply this skill after organism names have been cleaned and standardized (e.g., via 1_cleaningOriginal.R and 4_cleaningTaxonomy.R) but before final integration of organism, structure, and reference data. Use it when you have a cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) and need to attach stable, externally-validated taxonomic identifiers to enable downstream taxonomic queries, validation, and cross-database linking.

## When NOT to use

- Input organism table has not yet been cleaned or validated (run 4_cleaningTaxonomy.R first).
- Your workflow does not require external taxonomic reference alignment (e.g., organism names are sufficient as-is).
- OTL API or reference data is unavailable and mapping cannot proceed.

## Inputs

- interim/tables/2_cleaned/organism/cleaned.tsv.gz (cleaned organism table with standardized names)
- Open Tree of Life reference taxonomy (via API or local database)
- Organism name mapping rules and synonym lists (if available in external/translation/)

## Outputs

- interim/dictionaries/organism/otl.sqlite (SQLite dictionary with OTL-enriched organism records)
- interim/dictionaries/organism/*.tsv.gz (compressed TSV exports of OTL-enriched organism dictionary)

## How to apply

Load the cleaned organism table from interim/tables/2_cleaned/organism/cleaned.tsv.gz into an R environment. Execute the 5_addingOTL.R script, which maps each cleaned organism name to corresponding Open Tree of Life identifiers and taxonomic annotations using OTL's REST API or local reference data. The script validates organism names against OTL's taxonomy, resolves synonyms where possible, and attaches OTL IDs and hierarchical annotations. Write the enriched organism dictionary to interim/dictionaries/organism/otl.sqlite (SQLite format) and export summary outputs in compressed TSV format (.tsv.gz). Verify success by checking that the output dictionary contains non-null OTL IDs for the majority of organisms and that no rows are lost in the mapping process.

## Related tools

- **5_addingOTL.R** (Core R script that executes organism-to-OTL mapping, validates names, and writes enriched dictionary outputs) — https://github.com/lotusnprod/lotus-processor
- **R** (Execution environment for 5_addingOTL.R and related organism enrichment workflows)
- **Open Tree of Life** (External taxonomic reference database providing standardized organism identifiers and hierarchical annotations)

## Examples

```
Rscript 5_addingOTL.R --input interim/tables/2_cleaned/organism/cleaned.tsv.gz --output interim/dictionaries/organism/
```

## Evaluation signals

- Output SQLite database (otl.sqlite) is created and non-empty, with organism records containing OTL IDs.
- Row count of output dictionary matches or is close to input organism table (no significant data loss).
- OTL ID fields are non-null for ≥90% of organism records; null OTL IDs appear only for genuinely unmatched or ambiguous taxa.
- Spot-check: sample organisms in output have correct taxonomic rank, parent taxon, and OTL identifier alignment.
- TSV.gz output files are valid, compressible, and match the schema of the SQLite dictionary.

## Limitations

- Organism names that are ambiguous, misspelled, or not present in OTL will not be enriched; mapping success depends on name quality from prior cleaning steps.
- OTL API rate limits or downtime may cause the enrichment step to fail or time out; fallback or retry logic may be required.
- Synonymy and taxonomic rank interpretation can vary between OTL and the input source; manual curation may be needed for edge cases.
- The enrichment step does not validate biological plausibility or uniqueness across structure–organism pairs; it only adds taxonomic metadata.

## Evidence

- [other] The 5_addingOTL.R script processes the cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) to map organism names to Open Tree of Life identifiers: "The 5_addingOTL.R script processes the cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) to map organism names to Open Tree of Life identifiers, producing an OTL-enriched"
- [other] Load the cleaned organism table from interim/tables/2_cleaned/organism/cleaned.tsv.gz. Execute 5_addingOTL.R to map cleaned organism names to OTL taxonomic identifiers and annotations. Write the enriched organism dictionary to interim/dictionaries/organism/otl.sqlite and associated output files (.tsv.gz format).: "Load the cleaned organism table from interim/tables/2_cleaned/organism/cleaned.tsv.gz. Execute 5_addingOTL.R to map cleaned organism names to OTL taxonomic identifiers and annotations. Write the"
- [readme] within the frame of current computational approaches in Natural Products research and related fields, these documented structure-organism pairs should allow a more complete understanding of organisms and their chemistry: "Within the frame of current computational approaches in Natural Products research and related fields, these documented structure-organism pairs should allow a more complete understanding of organisms"
- [readme] All data sources used for this study are listed under docs/dataset.csv: "All data sources used for this study are listed under docs/dataset.csv"
