---
name: taxonomic-metadata-integration
description: Use when after organism name cleaning and standardization (via 1_cleaningOriginal.R and 4_cleaningTaxonomy.R) has produced a cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz), apply this skill to map those cleaned names to Open Tree of Life (OTL) identifiers.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0637
  tools:
  - R
  - 5_addingOTL.R
  - Open Tree of Life (OTL)
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

# taxonomic-metadata-integration

## Summary

Integration of cleaned organism names with standardized taxonomic identifiers (Open Tree of Life) to produce an enriched organism dictionary. This skill bridges curated organism records with external taxonomic authority data, enabling downstream computational natural products research to leverage standardized, resolvable organism references.

## When to use

After organism name cleaning and standardization (via 1_cleaningOriginal.R and 4_cleaningTaxonomy.R) has produced a cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz), apply this skill to map those cleaned names to Open Tree of Life (OTL) identifiers. Trigger when organism records lack stable external taxonomic URIs and computational downstream workflows (e.g., phylogenetic enrichment, organism filtering, multi-database harmonization) require resolvable, standardized organism references.

## When NOT to use

- Input organism records have already been mapped to OTL or other stable taxonomic identifiers (e.g., NCBI taxid, GBIF taxonKey); re-running risks duplicating identifiers or introducing conflicts.
- Organism names are not yet cleaned or standardized; apply 1_cleaningOriginal.R and 4_cleaningTaxonomy.R first.
- Downstream workflow does not require standardized organism URIs or taxonomic harmonization across multiple databases (e.g., purely chemical structure analysis without organism context).

## Inputs

- interim/tables/2_cleaned/organism/cleaned.tsv.gz (cleaned organism table with standardized names post-taxonomy verification)

## Outputs

- interim/dictionaries/organism/otl.sqlite (OTL-enriched organism dictionary in SQLite format)
- interim/dictionaries/organism/*.tsv.gz (OTL-enriched organism dictionary in tab-separated compressed format)

## How to apply

Load the cleaned organism table from interim/tables/2_cleaned/organism/cleaned.tsv.gz and execute the 5_addingOTL.R script, which queries the Open Tree of Life API or local taxonomy database to map each cleaned organism name to corresponding OTL identifiers and taxonomic annotations. The script applies name matching (likely fuzzy or exact) against OTL's curated taxonomy, captures matching confidence or alternative candidates, and writes the enriched organism dictionary to interim/dictionaries/organism/otl.sqlite and associated .tsv.gz output files. Success is determined by coverage (fraction of input organisms receiving valid OTL identifiers), uniqueness of mappings (no unintended collapsing of distinct taxa), and retention of organism metadata (common names, synonyms) for traceability.

## Related tools

- **5_addingOTL.R** (R script that executes organism name to OTL identifier mapping, queries OTL taxonomy, and writes enriched organism dictionary to SQLite and .tsv.gz outputs) — https://github.com/lotusnprod/lotus-processor
- **R** (Language and runtime for executing 5_addingOTL.R script) — https://www.r-project.org
- **Open Tree of Life (OTL)** (External taxonomic authority providing stable organism identifiers and standardized taxonomy; queried by 5_addingOTL.R) — https://tree.opentreeoflife.org

## Examples

```
Rscript 5_addingOTL.R --input interim/tables/2_cleaned/organism/cleaned.tsv.gz --output interim/dictionaries/organism/
```

## Evaluation signals

- Percentage of input organisms (from cleaned.tsv.gz) receiving valid, non-null OTL identifiers; expect >80% coverage for well-curated inputs.
- Absence of duplicated OTL identifiers mapping to the same organism record (1:1 or n:1 expected, not m:n collisions).
- Output otl.sqlite schema integrity: presence of organism ID, OTL identifier, confidence/match quality, and timestamp columns.
- Comparison of organism count before and after enrichment: total organisms should remain constant (no spurious filtering) unless explicitly documented pruning occurs.
- Spot checks of OTL identifiers for taxonomic plausibility (e.g., genus/species assignments should not be botanically or zoologically impossible).

## Limitations

- OTL coverage is incomplete for all organisms, especially microbial, rare, or recently described taxa; unmapped organisms will have null OTL identifiers and may require manual curation or alternative taxonomic sources.
- Name matching (fuzzy or exact) may produce false positives if organism names are ambiguous or colloquial; confidence scores or manual review steps are recommended for mission-critical applications.
- OTL itself may contain errors or outdated synonymy; the script inherits any upstream taxonomic inaccuracies from the OTL source.
- The 5_addingOTL.R script's implementation details (matching algorithm, API query parameters, timeout behavior) are not fully specified in the provided documentation; script source inspection is required for reproducibility or troubleshooting.

## Evidence

- [other] The 5_addingOTL.R script processes the cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) to map organism names to Open Tree of Life identifiers: "The 5_addingOTL.R script processes the cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) to map organism names to Open Tree of Life identifiers"
- [other] Write the enriched organism dictionary to interim/dictionaries/organism/otl.sqlite and associated output files (.tsv.gz format).: "Write the enriched organism dictionary to interim/dictionaries/organism/otl.sqlite and associated output files (.tsv.gz format)."
- [readme] Within the frame of current computational approaches in Natural Products research and related fields, these documented structure-organism pairs should allow a more complete understanding of organisms and their chemistry.: "Within the frame of current computational approaches in Natural Products research and related fields, these documented structure-organism pairs should allow a more complete understanding of organisms"
- [methods] 100([interim/tables/0_original/organism/*.tsv]) --> 101[[1_cleaningOriginal.R]] --> 102([interim/tables/2_cleaned/organism/original/*.json]): "2_editing organism – cleaning and taxonomy verification  [section=methods; evidence='100([interim/tables/0_original/organism/*.tsv]) --> 101[[1_cleaningOriginal.R]] -->"
- [other] Execute 5_addingOTL.R to map cleaned organism names to OTL taxonomic identifiers and annotations.: "Execute 5_addingOTL.R to map cleaned organism names to OTL taxonomic identifiers and annotations."
