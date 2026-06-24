---
name: metadata-structure-field-enrichment
description: Use when a metadata table contains compound names and identifiers but
  lacks structural data (SMILES, InChI, or molecular formula). The compounds are publicly
  available in PubChem and can be reliably identified by their chemical names. Use
  this skill before performing structure-dependent analyses (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  tools:
  - PubChem
  - prepare_wikidata_lotus_prefect.py
  - jobs.py
  techniques:
  - mass-spectrometry
  license_tier: open
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

# metadata-structure-field-enrichment

## Summary

Automatically retrieve and attach structural chemical data (SMILES, InChI, molecular formula, PubChem CID) to metadata entries lacking structure information by querying PubChem via Name search. This enriches compound metadata tables with standardized structural fields required for downstream cheminformatic analysis.

## When to use

A metadata table contains compound names and identifiers but lacks structural data (SMILES, InChI, or molecular formula). The compounds are publicly available in PubChem and can be reliably identified by their chemical names. Use this skill before performing structure-dependent analyses (e.g., molecular similarity calculations, mass spectrometry interpretation, or chemical database merging).

## When NOT to use

- Structure information is already present and validated in the metadata table; enrichment is redundant.
- Compound names are ambiguous, non-standard, or not indexed in PubChem (e.g., proprietary or synthesized compounds without public records).
- The analysis requires chemical structures not available via public Name search (e.g., stereoisomeric or salt-form disambiguation that PubChem Name search cannot resolve automatically).

## Inputs

- Metadata table with compound names (CSV, TSV, or Google Sheet conforming to the msn_tree_library template)
- Compound name column (required for PubChem Name search query)
- Optional: existing partial structure fields (used to identify gaps)

## Outputs

- Enriched metadata table with structure fields populated (SMILES, InChI, molecular formula, PubChem CID)
- Merged metadata table preserving original columns and adding new structure columns
- Query log or manifest mapping compound names to retrieved PubChem CIDs and structure identifiers

## How to apply

Load the metadata table and identify entries with missing structure fields using the provided Google Sheets template as the reference schema. For each compound with absent structure information, submit the compound name to the PubChem API or web interface using Name search; extract returned structure fields (SMILES, InChI, molecular formula, PubChem CID). Merge the retrieved structure data back into the original metadata table by joining on compound name or identifier, preserving all original columns while appending new structure-bearing fields. Validate that structure fields are now populated and consistent with PubChem's canonical representations before saving the enriched metadata.

## Related tools

- **PubChem** (Remote database queried via Name search to retrieve structure data (SMILES, InChI, molecular formula, CID) for compounds identified by name.)
- **prepare_wikidata_lotus_prefect.py** (Prefect workflow script for updating LOTUS natural product database data prior to or alongside metadata enrichment.) — https://github.com/corinnabrungs/msn_tree_library
- **jobs.py** (Configuration file defining which databases (including PubChem) are queried and whether local files or remote APIs are used.) — https://github.com/corinnabrungs/msn_tree_library

## Evaluation signals

- All entries in the metadata table that originally lacked structure information now have non-empty SMILES, InChI, and molecular formula fields.
- PubChem CID values are valid positive integers and consistent with canonical PubChem records for the queried compound names.
- SMILES and InChI strings parse without error in a cheminformatic library (e.g., RDKit) and represent chemically valid structures.
- No rows are dropped or duplicated; the enriched table has the same number of rows as the input, with original columns preserved.
- Structure fields conform to the template schema defined in the msn_tree_library documentation (same column names and data types).

## Limitations

- PubChem Name search may return ambiguous results for compounds with multiple trivial names, trade names, or isomers; manual curation may be required.
- Compounds not indexed in PubChem (proprietary, recently synthesized, or non-English named) will fail to retrieve structure data.
- PubChem's canonical SMILES and InChI may differ from domain-specific or legacy representations, requiring downstream validation or remapping.
- No changelog is provided in the repository, so updates to PubChem or API behavior may not be tracked or documented for reproducibility.

## Evidence

- [readme] If no structure information is provided, it is queried from PubChem by Name search: "If no structure information is provided, it is queried from PubChem by Name search"
- [other] Extract structure data (SMILES, InChI, molecular formula, and PubChem CID) from the returned results.: "Extract structure data (SMILES, InChI, molecular formula, and PubChem CID) from the returned results"
- [other] Merge retrieved structure information back into the metadata table, preserving original columns and appending new structure fields.: "Merge retrieved structure information back into the metadata table, preserving original columns and appending new structure fields"
- [readme] use the [template] for your metadata for having same column names and minimum needed information for the query: "use the [template] for your metadata for having same column names and minimum needed information for the query"
