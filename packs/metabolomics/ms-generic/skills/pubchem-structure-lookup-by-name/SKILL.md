---
name: pubchem-structure-lookup-by-name
description: Use when your metadata table contains compound names but lacks structure information (SMILES, InChI, molecular formula, or PubChem CID).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0159
  tools:
  - PubChem
  - jobs.py
  - metadata_cleanup_prefect.py
  - prepare_wikidata_lotus_prefect.py
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1038/s41592-025-02813-0
  title: MSnLib
evidence_spans:
- it is queried from PubChem by Name search
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

# pubchem-structure-lookup-by-name

## Summary

Automatically retrieve chemical structure data (SMILES, InChI, molecular formula, CID) from PubChem for metadata entries lacking structural information by performing name-based searches. This skill bridges gaps in incomplete chemical metadata tables during preprocessing for mass spectrometry or natural product workflows.

## When to use

Your metadata table contains compound names but lacks structure information (SMILES, InChI, molecular formula, or PubChem CID). This is particularly relevant when preparing entries for querying natural product or drug databases that require standardized structural identifiers, or when enriching heterogeneous datasets compiled from multiple sources (e.g., combining LOTUS, DrugBank, and user-supplied compounds).

## When NOT to use

- Compound names are ambiguous, non-standard, or proprietary (e.g., internal lab codes without chemical nomenclature); PubChem Name search may return incorrect or no results.
- Structure information is already provided in the metadata table; this skill is redundant and will waste API quota.
- High-throughput structure resolution is needed for >100,000 compounds; consider batch APIs or local chemical libraries to avoid rate limiting.

## Inputs

- Metadata table (CSV, TSV, or spreadsheet) with compound names and optional partial structure information
- List of compound names lacking structure data

## Outputs

- Enriched metadata table with appended structure columns (SMILES, InChI, molecular formula, PubChem CID)
- Mapping of original compound names to PubChem identifiers

## How to apply

Load the metadata table and identify rows where structure fields are empty or absent. For each compound with missing structure, submit the compound name as a query to the PubChem API (or web interface) using the Name search endpoint. Extract the returned structure data fields—SMILES string, InChI notation, molecular formula, and PubChem CID—from the top result (or manually review if multiple matches exist). Merge the retrieved fields back into the original metadata table by appending new columns while preserving all existing columns and row order. Validate that newly populated structure fields conform to expected formats (e.g., SMILES syntax, InChI prefix) before saving the enriched table.

## Related tools

- **PubChem** (Primary query service for compound name-to-structure resolution; returns SMILES, InChI, molecular formula, and CID via Name search API)
- **jobs.py** (Prefect job definition and control file; set local database flags (e.g., PubChem query parameters) and enable/disable external queries) — https://github.com/corinnabrungs/msn_tree_library
- **metadata_cleanup_prefect.py** (Orchestrates metadata enrichment workflow as a Prefect 2 flow; manages task sequencing including structure lookup) — https://github.com/corinnabrungs/msn_tree_library
- **prepare_wikidata_lotus_prefect.py** (Optionally updates LOTUS natural product database before or alongside structure lookups to ensure matched compounds are checked against curated reference data) — https://github.com/corinnabrungs/msn_tree_library

## Evaluation signals

- All originally empty structure fields are now populated with non-empty SMILES, InChI, and CID values; no row should have structure data unless a successful PubChem lookup occurred.
- SMILES strings pass chemical validity checks (e.g., balanced brackets, valid atomic symbols); InChI strings begin with 'InChI=' prefix.
- PubChem CID values are numeric and consistent with PubChem's public record identifiers (resolvable via pubchem.ncbi.nlm.nih.gov/compound/{CID}).
- Molecular formula matches the structure (SMILES/InChI can be converted to formula and compared).
- Enriched table row count and original columns are preserved; no rows were lost or duplicated during merge.

## Limitations

- PubChem Name search may return multiple hits for ambiguous compound names; automated selection of the top result risks retrieving the wrong isomer or salt form. Manual review or disambiguation rules are recommended for high-confidence workflows.
- Compounds not indexed in PubChem (e.g., newly synthesized or proprietary molecules, rare natural products) will fail to retrieve structure; these entries remain unfilled and require manual curation or alternative databases.
- Rate limiting on PubChem's public API may throttle large-batch queries; consider batch API access or local structure libraries for high-throughput enrichment.
- Compound name variations (e.g., trade names, systematic IUPAC names, abbreviations, partial names) may yield different PubChem records; standardization of input names improves recall.

## Evidence

- [readme] If no structure information is provided, it is queried from PubChem by Name search: "If no structure information is provided, it is queried from PubChem by Name search"
- [other] Extract structure data (SMILES, InChI, molecular formula, and PubChem CID) from the returned results.: "Extract structure data (SMILES, InChI, molecular formula, and PubChem CID) from the returned results"
- [other] Merge retrieved structure information back into the metadata table, preserving original columns and appending new structure fields.: "Merge retrieved structure information back into the metadata table, preserving original columns and appending new structure fields"
- [other] For each compound with missing structure, submit a PubChem Name search query via the PubChem API or web interface.: "For each compound with missing structure, submit a PubChem Name search query via the PubChem API or web interface"
- [readme] Please use the [template] for your metadata for having same column names and minimum needed information for the query: "Please use the [template] for your metadata for having same column names and minimum needed information for the query"
