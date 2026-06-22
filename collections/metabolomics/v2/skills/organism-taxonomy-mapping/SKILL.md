---
name: organism-taxonomy-mapping
description: Use when you have a cleaned organism table (with validated, deduplicated organism names from sources like NCBI, manual curation, or previous cleaning steps) and need to annotate each organism with Open Tree of Life identifiers, taxonomic lineage, and standardized taxonomic annotations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_0637
  tools:
  - R
  - 5_addingOTL.R
  - 4_cleaningTaxonomy.R
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

# organism-taxonomy-mapping

## Summary

Maps cleaned organism names to standardized taxonomic identifiers using Open Tree of Life (OTL) to enrich organism data with validated phylogenetic and systematic annotations. This skill bridges cleaned taxonomy tables with authoritative external taxonomic references, enabling downstream computational natural products research with resolved organism provenance.

## When to use

Apply this skill when you have a cleaned organism table (with validated, deduplicated organism names from sources like NCBI, manual curation, or previous cleaning steps) and need to annotate each organism with Open Tree of Life identifiers, taxonomic lineage, and standardized taxonomic annotations. Trigger this step after organism name cleaning (e.g., after 4_cleaningTaxonomy.R) and before final curation or cross-database integration, especially when organisms will be used in computational chemistry or structure–organism association workflows.

## When NOT to use

- Input organism table contains raw, uncleaned names with spelling variants, typos, or unvalidated taxonomy — clean and deduplicate names first using 4_cleaningTaxonomy.R or equivalent.
- Organism names are already mapped to a different authoritative taxonomy (e.g., NCBI Taxonomy) and you do not need OTL-specific lineage or phylogenetic context.
- Your downstream workflow does not require standardized taxonomic identifiers and only uses organism names as text labels.

## Inputs

- interim/tables/2_cleaned/organism/cleaned.tsv.gz (cleaned organism table with standardized names)
- Open Tree of Life API or local OTL reference data (external taxonomic authority)

## Outputs

- interim/dictionaries/organism/otl.sqlite (enriched organism dictionary in SQLite format)
- interim/dictionaries/organism/*.tsv.gz (enriched organism dictionary in TSV.GZ format with OTL identifiers and annotations)

## How to apply

Load the cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) containing deduplicated and validated organism names. Execute the 5_addingOTL.R script in R, which queries Open Tree of Life identifiers and taxonomic metadata for each organism name using programmatic API calls or local OTL data. The script maps organism names to OTL unique identifiers (UIDs), retrieves associated taxonomic context (rank, lineage, synonym information), and writes the enriched organism dictionary to interim/dictionaries/organism/ in both SQLite (otl.sqlite) and TSV.GZ formats for downstream use. Validate mapping success by checking coverage (proportion of organisms with matched OTL UIDs) and by spot-checking ambiguous or novel organism names against OTL web interface.

## Related tools

- **5_addingOTL.R** (R script that executes the organism-to-OTL mapping, querying OTL identifiers and taxonomic annotations for each cleaned organism name and writing enriched dictionary outputs) — https://github.com/lotusnprod/lotus-processor
- **4_cleaningTaxonomy.R** (Upstream R script that cleans and validates organism taxonomy before OTL enrichment; output feeds directly into 5_addingOTL.R) — https://github.com/lotusnprod/lotus-processor
- **R** (Language and runtime environment for executing the 5_addingOTL.R script and handling data I/O)

## Examples

```
Rscript 5_addingOTL.R --input interim/tables/2_cleaned/organism/cleaned.tsv.gz --output interim/dictionaries/organism/
```

## Evaluation signals

- Mapping coverage: ≥ 80–90% of organisms in the cleaned table have matched OTL UIDs (expected for well-curated organism lists); document and review organisms with no match.
- Output file integrity: otl.sqlite exists and is readable; .tsv.gz files decompress and contain expected columns (organism name, OTL UID, rank, lineage, synonyms).
- No data loss: row count in output dictionary equals row count in cleaned input table (allowing for duplicates if intentionally retained).
- Spot-check validation: randomly sample 10–20 organism–OTL UID pairs and verify against OTL web interface (https://tree.opentreeoflife.org/) for correct taxonomy and rank.
- Downstream compatibility: enriched dictionary can be successfully joined/integrated with organism references in subsequent workflow steps (e.g., 3_integrating.R) without schema or key mismatches.

## Limitations

- OTL coverage is not universal; organisms that are very recent discoveries, highly specialized nomenclature variants, or taxa not yet incorporated into OTL will fail to map and must be manually reviewed or flagged.
- Ambiguous organism names (e.g., homonyms or names with multiple OTL UIDs) require additional logic or manual disambiguation; the script may default to the first match or require post-hoc curation.
- OTL is a dynamic resource; organism identifiers and taxonomic placements may change between OTL releases, affecting reproducibility if script is re-run against a newer OTL snapshot.
- Performance may degrade for large organism tables (>50,000 entries) if using live API queries; local OTL databases or batch query strategies are recommended for scale.

## Evidence

- [other] The 5_addingOTL.R script processes the cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) to map organism names to Open Tree of Life identifiers: "The 5_addingOTL.R script processes the cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz) to map organism names to Open Tree of Life identifiers"
- [other] Write the enriched organism dictionary to interim/dictionaries/organism/otl.sqlite and associated output files (.tsv.gz format).: "Write the enriched organism dictionary to interim/dictionaries/organism/otl.sqlite and associated output files (.tsv.gz format)."
- [readme] LOTUS is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented: "*LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented"
- [other] Execute 5_addingOTL.R to map cleaned organism names to OTL taxonomic identifiers and annotations.: "Execute 5_addingOTL.R to map cleaned organism names to OTL taxonomic identifiers and annotations."
