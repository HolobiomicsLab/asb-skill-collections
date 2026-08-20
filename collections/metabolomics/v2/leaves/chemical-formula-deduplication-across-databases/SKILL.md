---
name: chemical-formula-deduplication-across-databases
description: Use when you have retrieved chemical formulae and metadata from two or
  more of HMDB, ChEMBL, or PubChem and need to merge them into a single searchable
  database without formula duplication.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3172
  tools:
  - SMART
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c06210
  title: SMART
evidence_spans:
- we present SMART, an open-source platform designed for precise formula assignment
  in mass spectrometry imaging
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_cq
    doi: 10.1021/acs.analchem.4c06210
    title: SMART
  dedup_kept_from: coll_smart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06210
  all_source_dois:
  - 10.1021/acs.analchem.4c06210
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-formula-deduplication-across-databases

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Deduplicate and resolve cross-references among chemical formulae retrieved from multiple heterogeneous repositories (HMDB, ChEMBL, PubChem) to construct a unified, non-redundant formulae knowledge base. This skill is essential for building comprehensive metabolomic reference databases where the same molecular structure may be catalogued under different identifiers or metadata across sources.

## When to use

You have retrieved chemical formulae and metadata from two or more of HMDB, ChEMBL, or PubChem and need to merge them into a single searchable database without formula duplication. Specifically, apply this skill when you observe that the same molecular structure appears under different accession IDs, names, or structural representations across repositories and you require a unified identifier scheme for subsequent m/z-based lookups or biological edge linking.

## When NOT to use

- Input is already a deduplicated, single-source formulae database (e.g., HMDB alone) — deduplication is unnecessary overhead.
- You require isotope-resolved or adduct-specific formula variants — standard deduplication may conflate isobars or collapse chemically distinct adducts into a single entry.
- The scope is limited to a single repository with no external data integration — apply this skill only when merging data across distinct sources.

## Inputs

- Chemical formulae and metadata from HMDB (molecular identifiers, molecular weights, names)
- Chemical formulae and metadata from ChEMBL (compound records, structural representations)
- Chemical formulae and metadata from PubChem (CID entries, molecular properties)
- Structural identifiers (InChI, SMILES, or canonical keys)

## Outputs

- Deduplicated chemical formula catalogue (unique formula per entry)
- Unified identifier mapping (original repository IDs → deduplicated formula ID)
- Source provenance tags (which repositories contributed each formula)
- Cross-reference resolution metadata (mapping tables between repository IDs)

## How to apply

Parse chemical formulae, molecular weights, and structural metadata from each source repository separately. Implement cross-reference resolution by matching formulae on canonical structural keys (e.g., InChI, SMILES, or exact molecular weight within a tolerance threshold). Deduplicate by selecting a primary record per unique formula and collating source tags (e.g., 'HMDB', 'ChEMBL', 'PubChem') to retain provenance. Assign unified identifiers to each deduplicated formula. Validate edge connectivity by confirming that each formula record links correctly to its source repositories. Store the merged result with explicit mappings between formulae and their originating databases to enable downstream filtering or source-specific queries.

## Related tools

- **SMART** (Integrates deduplicated formulae into the KnownSet database and uses the unified formula catalogue for m/z-based formula assignment and scoring) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
# Pseudocode for deduplication workflow during KnownSet construction
# Parse three repositories, deduplicate on canonical InChI, merge, and export
from SMART.formulae import deduplicate_formulae
hmdb_set = parse_repository('HMDB', 'hmdb.xml')
chembl_set = parse_repository('ChEMBL', 'chembl.sdf')
pubchem_set = parse_repository('PubChem', 'pubchem.csv')
merged = deduplicate_formulae([hmdb_set, chembl_set, pubchem_set], key='inchi', tolerance_ppm=5)
merged.assign_unified_ids()
merged.export_to_database('smart.db')
```

## Evaluation signals

- Total formula count in the merged database (2.8 million reported) is consistent with cumulative counts from source repositories minus confirmed duplicates.
- Each deduplicated formula maps to one or more source repository tags; no formula lacks a source attribution.
- Cross-reference validation: spot-check 100+ known metabolites (e.g., glucose, alanine) across all three repositories and confirm they resolve to a single deduplicated entry.
- Query the merged database by m/z value (e.g., 185.9934) and verify that all returned candidate formulae have unique molecular weights within the PPM tolerance (default 5 ppm) and link to the correct source repositories.
- Inspect mapping tables for bidirectional consistency: if formula X maps to HMDB:H00001 and ChEMBL:CHEMBL456, confirm that querying HMDB and ChEMBL directly retrieves the same X.

## Limitations

- Deduplication relies on exact or near-exact structural matching (InChI, SMILES, or molecular weight); formulae with missing or corrupted structural data may not deduplicate correctly.
- Isobars (same mass, different structure) cannot be resolved by mass alone and may require additional structural metadata or manual curation.
- Repository-specific annotations (e.g., HMDB's biological context, ChEMBL's bioactivity data) are retained per source but may not be reconciled across databases, limiting post-hoc integration of diverse metadata.
- The raw SMART-database exceeds 1 Terabyte; the temporary distributed version includes only HMDB and may not cover all formulae present in the full ChEMBL and PubChem repositories.

## Evidence

- [other] Extract DBEdges by identifying structural and chemical relationships between formulae across the three databases, deduplicating and resolving cross-references.: "Extract DBEdges by identifying structural and chemical relationships between formulae across the three databases, deduplicating and resolving cross-references."
- [readme] SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem: "SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem"
- [other] Merge all formulae, DBEdges, and BioEdges into a unified graph structure, assigning unique identifiers and validating edge connectivity.: "Merge all formulae, DBEdges, and BioEdges into a unified graph structure, assigning unique identifiers and validating edge connectivity."
- [readme] DB: H:HMDB, E:chEMBL, P:PubChem: "results will be shown in the right table (DB: H:HMDB, E:chEMBL, P:PubChem)"
- [readme] Since the raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte: "Since the raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte"
