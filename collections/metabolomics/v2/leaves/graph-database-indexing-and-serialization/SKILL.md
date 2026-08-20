---
name: graph-database-indexing-and-serialization
description: Use when you have retrieved and deduplicated chemical formulae and metadata
  from multiple heterogeneous sources (HMDB, ChEMBL, PubChem) and extracted both structural
  relationships (DBEdges) and biological reactant pairs (BioEdges from KEGG), and
  now need to merge them into a single queryable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - SMART
  techniques:
  - MS-imaging
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

# graph-database-indexing-and-serialization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct and index a unified graph database of chemical formulae and their interconnections (DBEdges and BioEdges) for efficient mass-to-charge (m/z) based lookup and export as a serialized database file. This skill bridges multiple chemical repositories and biological reaction networks into a queryable knowledge structure.

## When to use

You have retrieved and deduplicated chemical formulae and metadata from multiple heterogeneous sources (HMDB, ChEMBL, PubChem) and extracted both structural relationships (DBEdges) and biological reactant pairs (BioEdges from KEGG), and now need to merge them into a single queryable structure that supports rapid m/z-based formula lookup in mass spectrometry workflows.

## When NOT to use

- Input formulae have not been deduplicated or cross-referenced across repositories — index will contain redundant/conflicting entries.
- DBEdges and BioEdges have not been validated for correctness — index will propagate annotation errors downstream.
- You only need to query a small set of known formulae — full graph construction and serialization is unnecessary overhead; use a lightweight lookup table instead.

## Inputs

- Deduplicated chemical formulae with metadata (structure, SMILES, molecular weight)
- DBEdges: structural and chemical relationships between formulae (source: HMDB, ChEMBL, PubChem cross-references)
- BioEdges: metabolic reactant pairs linking formulae (source: KEGG biological reaction database)
- Predicted m/z values from multiple linear regression model

## Outputs

- Unified serialized KnownSet database file (smart.db) comprising 2.8 million formulae indexed by m/z
- Graph structure with nodes (formulae) annotated with source provenance (HMDB, ChEMBL, PubChem, KEGG)
- Secondary m/z index enabling rapid formula network extraction within PPM tolerance threshold

## How to apply

Merge all deduplicated formulae, DBEdges, and BioEdges into a unified directed graph structure, assigning unique identifiers to each node (formula) and validating edge connectivity across all three source databases and KEGG reactant pairs. Build a secondary index on the m/z mass-to-charge ratio using the multiple linear regression model's predicted m/z values to enable fast lookups within a specified PPM (parts per million) tolerance window. Serialize the indexed graph (typically >1 TB for the full KnownSet) using a database format that preserves node attributes (formula, m/z, source provenance) and edge metadata (DBEdge type, BioEdge reaction context). Validate indexing by spot-checking that querying an m/z value (e.g., 185.9934) within the default 5 ppm threshold returns only formulae whose m/z values fall within that band, and that edge traversals correctly trace linked formulae across databases.

## Related tools

- **SMART** (Integrates KnownSet database construction and uses indexed m/z lookups for formula assignment in spatially-resolved mass spectrometry imaging) — https://github.com/bioinfo-ibms-pumc/SMART

## Examples

```
python SMART.py -i 185.9934 -d smart.db -l lr_4f.pkl -p 0 -m 5
```

## Evaluation signals

- Verify all 2.8 million formulae are present in the serialized database and no deduplication artifacts remain (e.g., duplicate m/z entries with conflicting source tags).
- Query a reference set of known m/z values (e.g., 185.9934) and confirm returned formulae have m/z within the specified PPM tolerance (default 5 ppm) and have valid edge connections to at least one DBEdge or BioEdge neighbor.
- Perform graph connectivity checks: verify that all formulae reachable by BioEdges are also represented in the chemical repositories (HMDB, ChEMBL, PubChem) to catch orphaned KEGG-only nodes.
- Measure index query latency: typical m/z-based lookups should complete in milliseconds; significant slowdown (>1 second) indicates poor index structure or insufficient partitioning.
- Validate edge metadata: spot-check DBEdges for source consistency (edges between two HMDB formulae should be marked as DBEdge type 'HMDB-HMDB') and BioEdges for reaction context presence.

## Limitations

- The full raw SMART-database exceeds 1 terabyte in size and is not publicly distributed; users must contact maintainers or use the temporary HMDB-only version for download.
- m/z indexing relies on predicted values from the multiple linear regression model, which may introduce systematic bias for formulae with unusual ionization behavior or post-translational modifications.
- Cross-repository deduplication is heuristic-based and may miss true duplicates or false-positive merges if chemical repositories use inconsistent nomenclature or structural representations (e.g., tautomers, salt forms).

## Evidence

- [readme] SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG biological reactant pairs: "SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG"
- [other] Merge all formulae, DBEdges, and BioEdges into a unified graph structure, assigning unique identifiers and validating edge connectivity: "Merge all formulae, DBEdges, and BioEdges into a unified graph structure, assigning unique identifiers and validating edge connectivity"
- [other] Index the complete KnownSet database for efficient m/z-based lookups and export as a serialized database file: "Index the complete KnownSet database for efficient m/z-based lookups and export as a serialized database file"
- [readme] scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values: "scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs"
- [readme] Since the raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte, users who want to use the raw SMART-database can contact us: "raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte"
