---
name: cross-database-entity-reconciliation
description: Use when you have chemical entity records scattered across two or more public repositories (e.g., HMDB, ChEMBL, PubChem, KEGG) and need a single authoritative, deduplicated knowledge base indexed by a queryable identifier (e.g., m/z value or chemical formula).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - SMART
derived_from:
- doi: 10.1021/acs.analchem.4c06210
  title: SMART
evidence_spans:
- we present SMART, an open-source platform designed for precise formula assignment in mass spectrometry imaging
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-database-entity-reconciliation

## Summary

Integrate and deduplicate chemical entities (formulae, structures) sourced from multiple independent repositories (HMDB, ChEMBL, PubChem) by resolving cross-references and assigning unique identifiers, then enrich the unified entity set with biological relationship edges (BioEdges) from KEGG metabolic reaction pairs. This skill enables construction of a comprehensive, interconnected reference database suitable for high-precision mass spectrometry annotation.

## When to use

Apply this skill when you have chemical entity records scattered across two or more public repositories (e.g., HMDB, ChEMBL, PubChem, KEGG) and need a single authoritative, deduplicated knowledge base indexed by a queryable identifier (e.g., m/z value or chemical formula). Use it specifically when downstream analysis (e.g., formula assignment in mass spectrometry imaging) requires both structural relationships (DBEdges) and metabolic/biological relationships (BioEdges) to rank and score candidate matches.

## When NOT to use

- You already have a single, internally consistent chemical entity database with all required edges pre-computed; reconciliation would add overhead without new information.
- Your analysis is restricted to a single repository (e.g., only HMDB) and you do not require cross-source deduplication or biological relationship enrichment.
- Your input data is feature-by-sample peak intensity tables (metabolomics output) rather than raw chemical entity records; use formula assignment or annotation workflows instead.

## Inputs

- Parsed chemical formulae and metadata tables from HMDB
- Parsed chemical formulae and metadata tables from ChEMBL
- Parsed chemical formulae and metadata tables from PubChem
- KEGG biological reactant pair records (linking formulae in metabolic reactions)
- Cross-reference mappings between repositories (e.g., InChIKey, PubChem CID to HMDB ID)

## Outputs

- Unified KnownSet database comprising 2.8 million unique chemical formulae
- DBEdges: set of structural/chemical relationship edges linking formulae across HMDB, ChEMBL, and PubChem
- BioEdges: set of metabolic relationship edges linking formulae from KEGG reactant pairs
- Indexed, serialized database file (e.g., smart.db) with formula→m/z, formula→DBEdges, formula→BioEdges lookups
- Unique identifier mapping (formula ID → provenance source(s))

## How to apply

First, retrieve and parse chemical formulae and metadata in bulk from each source repository (HMDB, ChEMBL, PubChem). Second, extract DBEdges by identifying structural and chemical relationships between formulae across the three databases, then deduplicate records and resolve cross-references using canonical identifiers or chemical structure matching. Third, independently retrieve KEGG biological reactant pairs and construct BioEdges that link formulae participating in the same metabolic reactions. Fourth, merge all unique formulae, DBEdges, and BioEdges into a unified directed graph structure, assigning a single unique identifier per formula and validating that all edge endpoints reference valid nodes. Finally, index the complete merged database by m/z (or other query key) and serialize to a database file (e.g., SQLite or pickle format) for efficient runtime lookups. At each deduplication step, retain provenance—recording which source repository contributed each entity—to support later scoring and filtering by database origin.

## Related tools

- **SMART** (Orchestrates KnownSet database construction and uses the reconciled, indexed database for formula assignment in spatially-resolved mass spectrometry imaging via multiple linear regression scoring.) — https://github.com/bioinfo-ibms-pumc/SMART

## Evaluation signals

- All 2.8 million formulae are present in the final merged database and each formula has a unique, canonical identifier with no duplicates.
- Every DBEdge references valid formula IDs on both endpoints; edge directionality and metadata (source repository) are preserved.
- Every BioEdge correctly links at least two formulae that appear together as reactants or products in a KEGG reaction; no edges reference non-existent formulae.
- Database index lookups by m/z (within ±PPM tolerance, default 5 ppm) return the expected formula candidates in reasonable runtime; no timeouts or missing results for reference m/z values.
- Provenance records show that duplicate formulae across repositories are merged (not replicated) with all source origins recorded; spot-check confirms cross-repository edges are present.

## Limitations

- The raw SMART-database file size exceeds 1 Terabyte; most users receive a compressed or subset version (e.g., HMDB-only temporary database from Figshare). Full reconciliation requires significant storage and computational resources.
- Deduplication quality depends on the availability and accuracy of cross-repository mappings (e.g., InChIKey, CID mappings); discrepancies or missing mappings may result in false duplicates or false negatives.
- KEGG BioEdges are limited to reactions explicitly curated in KEGG; novel or tissue-specific metabolic pathways not yet in KEGG will not appear as BioEdges.
- The skill assumes formulae can be reliably parsed and matched across repositories; repositories with inconsistent or incomplete chemical metadata may introduce errors during reconciliation.

## Evidence

- [other] Extract DBEdges by identifying structural and chemical relationships between formulae across the three databases, deduplicating and resolving cross-references.: "Extract DBEdges by identifying structural and chemical relationships between formulae across the three databases, deduplicating and resolving cross-references."
- [other] Retrieve KEGG biological reactant pairs and construct BioEdges that link formulae involved in metabolic reactions.: "Retrieve KEGG biological reactant pairs and construct BioEdges that link formulae involved in metabolic reactions."
- [other] Merge all formulae, DBEdges, and BioEdges into a unified graph structure, assigning unique identifiers and validating edge connectivity.: "Merge all formulae, DBEdges, and BioEdges into a unified graph structure, assigning unique identifiers and validating edge connectivity."
- [readme] SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG biological reactant pairs.: "SMART constructs a KnownSet database that comprise 2.8 million formulae interconnected by DBEdges sourced from repositories such as HMDB, ChEMBL, PubChem, and BioEdges from KEGG biological reactant"
- [readme] the raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte: "the raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte"
