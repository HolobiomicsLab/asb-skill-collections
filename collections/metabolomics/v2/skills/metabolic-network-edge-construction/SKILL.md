---
name: metabolic-network-edge-construction
description: Use when when building a comprehensive chemical knowledge base for mass spectrometry formula assignment, particularly when you need to link chemical formulae across heterogeneous repositories (HMDB, ChEMBL, PubChem) and connect them through known metabolic transformations to improve annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_2258
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

# metabolic-network-edge-construction

## Summary

Construction of interconnected chemical formula networks by integrating structural relationships (DBEdges) from multi-source chemical repositories and biological reaction pairs (BioEdges) from KEGG, enabling m/z-based lookups for spatially-resolved metabolomics annotation.

## When to use

When building a comprehensive chemical knowledge base for mass spectrometry formula assignment, particularly when you need to link chemical formulae across heterogeneous repositories (HMDB, ChEMBL, PubChem) and connect them through known metabolic transformations to improve annotation confidence in spatially-resolved or imaging mass spectrometry experiments.

## When NOT to use

- Input data is already a pre-computed formula network or feature table with assigned annotations — use this skill only to construct the network from raw repository sources.
- You require real-time or streaming formula updates — this approach builds a static snapshot indexed at construction time.
- Coverage of non-metabolic chemical space is critical and KEGG-only biological edges are insufficient — consider supplementing with additional reaction databases or organism-specific pathways.

## Inputs

- Chemical formulae and metadata from HMDB, ChEMBL, PubChem repositories
- KEGG biological reactant pair mappings
- Cross-reference identifiers linking compounds across repositories

## Outputs

- KnownSet database file (serialized, indexed for m/z lookup)
- Graph of 2.8 million formulae nodes
- DBEdge list (structural/chemical relationships)
- BioEdge list (metabolic reaction links)

## How to apply

Retrieve and parse chemical formulae and metadata from HMDB, ChEMBL, and PubChem repositories, then extract DBEdges by identifying structural and chemical relationships between formulae while deduplicating cross-references. In parallel, retrieve KEGG biological reactant pairs and construct BioEdges that link formulae involved in metabolic reactions. Merge all formulae, DBEdges, and BioEdges into a unified graph structure with unique identifiers, validate edge connectivity to ensure no orphaned nodes, and index the complete database for efficient m/z-based lookups using a multiple linear regression model. Export the final structure as a serialized database file (e.g., .db format) for downstream formula scoring, which weights candidates by linked formulae density, edge type (DBEdge vs. BioEdge), and parts-per-million (PPM) deviation from observed m/z.

## Related tools

- **SMART** (Formula assignment platform that consumes the KnownSet database to extract formula networks, score candidates using DBEdges/BioEdges and PPM thresholds, and predict formulae with precision on spatially-resolved metabolomics data) — https://github.com/bioinfo-ibms-pumc/SMART

## Evaluation signals

- Database completeness: verify 2.8 million formulae are present and indexed; check for no null or duplicate identifiers.
- Edge integrity: confirm all DBEdges and BioEdges reference valid formula nodes; no orphaned edge endpoints.
- Cross-repository deduplication: spot-check that compounds with identical molecular weight and formula across HMDB, ChEMBL, and PubChem are merged, not duplicated.
- m/z lookup performance: benchmark query latency for common m/z ranges (e.g., 100–1000 m/z) to confirm indexing is functional.
- Downstream annotation accuracy: run SMART formula prediction on reference datasets with known ground truth; confirm precision matches or exceeds published benchmarks.

## Limitations

- Raw SMART-database size exceeds 1 Terabyte; users must request access from maintainers or use the temporary HMDB-only version from Figshare.
- DBEdge extraction relies on structural and chemical relationship inference across repositories; cross-reference inconsistencies or missing metadata in source repositories may create gaps or false edges.
- BioEdges are limited to KEGG reactant pairs, which may not capture all tissue-specific or non-canonical metabolic transformations.
- PPM-based m/z matching (default 5 ppm) may cause false positives at low m/z or miss formulae if instrument mass calibration is poor.

## Evidence

- [other] The KnownSet database comprises 2.8 million formulae interconnected by DBEdges sourced from HMDB, ChEMBL, and PubChem, and by BioEdges from KEGG biological reactant pairs.: "The KnownSet database comprises 2.8 million formulae interconnected by DBEdges sourced from HMDB, ChEMBL, and PubChem, and by BioEdges from KEGG biological reactant pairs."
- [other] Extract DBEdges by identifying structural and chemical relationships between formulae across the three databases, deduplicating and resolving cross-references.: "Extract DBEdges by identifying structural and chemical relationships between formulae across the three databases, deduplicating and resolving cross-references."
- [other] Retrieve KEGG biological reactant pairs and construct BioEdges that link formulae involved in metabolic reactions.: "Retrieve KEGG biological reactant pairs and construct BioEdges that link formulae involved in metabolic reactions."
- [other] Merge all formulae, DBEdges, and BioEdges into a unified graph structure, assigning unique identifiers and validating edge connectivity.: "Merge all formulae, DBEdges, and BioEdges into a unified graph structure, assigning unique identifiers and validating edge connectivity."
- [readme] scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs ppms values: "scores potential candidates based on various criteria, including linked formulae, DBEdges/BioEdges, and PPMs values"
- [readme] Since the raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte, users who want to use the raw SMART-database can contact us: "Since the raw SMART-database consists of huge number of formulae with their evidences, with database size exceeds 1 Terabyte, users who want to use the raw SMART-database can contact us"
