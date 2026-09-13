---
name: compound-identifier-standardization
description: Use when ingesting compound metadata from multiple sources (PubChem,
  DrugBank, LOTUS, Dictionary of Natural Products, DrugCentral) that lack uniform
  column naming, have incomplete structure information, or contain only compound names
  without structural data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0209
  tools:
  - PubChem
  - jobs.py
  - prepare_wikidata_lotus_prefect.py
  - drugbank_extraction.py
  techniques:
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-025-02813-0
  title: MSnLib
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msnlib_cq
    doi: 10.1038/s41592-025-02813-0
    title: MSnLib
  dedup_kept_from: coll_msnlib_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02813-0
  all_source_dois:
  - 10.1038/s41592-025-02813-0
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-identifier-standardization

## Summary

Standardize and enrich compound metadata by enforcing a uniform column structure and automatically retrieving missing structural identifiers (SMILES, InChI, molecular formula, PubChem CID) via PubChem Name search. This ensures consistent, queryable metadata across heterogeneous natural product and drug databases.

## When to use

Apply this skill when ingesting compound metadata from multiple sources (PubChem, DrugBank, LOTUS, Dictionary of Natural Products, DrugCentral) that lack uniform column naming, have incomplete structure information, or contain only compound names without structural data.

## When NOT to use

- Input metadata already contains complete structural identifiers for all compounds; skip enrichment.
- Compound names are ambiguous or non-standard (e.g., proprietary or trade names with no PubChem entry); Name search will fail or return incorrect structures.
- Analysis requires only compound classification or activity prediction without need for standardized structure data.

## Inputs

- Metadata table (CSV/Excel/TSV) with compound names and optional structure identifiers
- Compound names (as query strings for PubChem Name search)
- Metadata template with standardized column definitions

## Outputs

- Standardized metadata table with uniform column names
- Enriched metadata with structure fields (SMILES, InChI, molecular formula, PubChem CID)
- Mapping of compound names to PubChem CIDs

## How to apply

First, map all incoming metadata to a standardized template with uniform column names and minimum required fields (compound name, identifier, source). For each row where structure information (SMILES, InChI, molecular formula, or PubChem CID) is absent, submit the compound name as a query to the PubChem API or web interface using Name search. Extract returned structure fields and merge them back into the metadata table, preserving all original columns while appending the new structure fields. Finally, validate that all rows now contain at least one structural identifier and save the enriched metadata table.

## Related tools

- **PubChem** (Queried via Name search API to retrieve structure data (SMILES, InChI, molecular formula, CID) for compounds with missing structural identifiers)
- **jobs.py** (Configuration file for specifying which external databases (DrugBank, LOTUS, DrugCentral, Dictionary of Natural Products) to enable/disable for metadata enrichment) — https://github.com/corinnabrungs/msn_tree_library
- **prepare_wikidata_lotus_prefect.py** (Script to update LOTUS natural product database data before standardization pipeline) — https://github.com/corinnabrungs/msn_tree_library
- **drugbank_extraction.py** (Script to extract and standardize structure and metadata fields from DrugBank source files) — https://github.com/corinnabrungs/msn_tree_library

## Examples

```
python metadata_cleanup_prefect.py --input compounds.csv --template https://docs.google.com/spreadsheets/d/1v6_IlGS3VgycGc-mSSdNeocY-CFXpONVZbuh3XNLX2E --output enriched_compounds.csv
```

## Evaluation signals

- All rows in the output table have the same column names and order as the standardized template
- Rows with previously missing structure data now contain at least one non-empty structural identifier (SMILES, InChI, or molecular formula)
- PubChem CID is retrieved and populated for all successfully matched compounds
- Row count and original compound names are preserved; no rows are dropped or renamed
- Spot-check: manually query PubChem for 5–10 compounds in the output and verify returned structure fields match the enriched table

## Limitations

- PubChem Name search may fail or return incorrect structures for ambiguous, proprietary, or non-standard compound names; manual curation may be required.
- Compounds not present in PubChem will not be enriched; these rows should be flagged for manual review or alternative data source lookup.
- Name search is sensitive to spelling and formatting; synonyms and trade names may not resolve reliably.
- API rate limits or network failures during bulk queries may interrupt the enrichment process; implement retry logic and checkpointing.
- Some compounds (e.g., mixtures, stereoisomers with ambiguous configuration) may have multiple PubChem entries; the first or highest-CID result may not be the intended compound.

## Evidence

- [intro] Metadata cleanup and standardization using template: "Please use the [template] for your metadata for having same column names and minimum needed information for the query"
- [intro] PubChem Name search retrieval of structure information: "If no structure information is provided, it is queried from PubChem by Name search"
- [other] Structure field extraction and enrichment workflow: "Extract structure data (SMILES, InChI, molecular formula, and PubChem CID) from the returned results. Merge retrieved structure information back into the metadata table, preserving original columns"
- [readme] Multi-database integration with selective loading: "For querying other databases, some need a local file and/or special access otherwise set it to False in the jobs.py"
