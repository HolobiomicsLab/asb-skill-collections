---
name: graph-representation-construction
description: Use when you have KEGG metabolic data for one or more organisms and need
  to simultaneously analyze network topology and functional pathway organization—for
  example, when comparing metabolic capabilities between species for drug target discovery
  or when you need to expose both structural rewiring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3083
  edam_topics:
  - http://edamontology.org/topic_0601
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3324
  tools:
  - MetNet
  - Java
  - KEGG
  - Java (GraphStream, Guava, Apache POI libraries)
  license_tier: open
derived_from:
- doi: 10.1371/journal.pone.0246962
  title: MetNet
evidence_spans:
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic
  network of two organisms selected in KEGG
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic
  network
- MetNet is a Java tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metnet_cq
    doi: 10.1371/journal.pone.0246962
    title: MetNet
  dedup_kept_from: coll_metnet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pone.0246962
  all_source_dois:
  - 10.1371/journal.pone.0246962
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Construct two-level graph representation of metabolic networks

## Summary

Build a dual-layer graph encoding both structural topology (metabolites as nodes, enzymatic reactions as edges) and functional pathway information from reconstructed metabolic networks. This enables quantitative and visual comparison of metabolic systems across organisms using similarity indexes at each representational level.

## When to use

You have KEGG metabolic data for one or more organisms and need to simultaneously analyze network topology and functional pathway organization—for example, when comparing metabolic capabilities between species for drug target discovery or when you need to expose both structural rewiring and functional shifts in pathway reorganization.

## When NOT to use

- Input metabolic data is already in a flattened feature table or pathway abundance matrix—this skill requires reaction-level KEGG records, not pre-aggregated summaries.
- You only need pathway presence/absence or gene expression scores, not topology-aware network comparison—simpler set operations suffice.
- Organisms lack sufficient KEGG annotation coverage; the method depends on complete and accurate KEGG pathway assignment.

## Inputs

- KEGG organism codes (e.g., 'hsa' for Homo sapiens)
- KEGG reaction and metabolite records (retrieved via KEGG API)
- Pathway-to-function mapping configuration (pathwayList.txt format)

## Outputs

- Structural-level graph (metabolite nodes, reaction edges)
- Functional-level graph (function nodes/edges mapped to structural equivalents)
- Similarity indexes comparing two organisms at structural level
- Similarity indexes comparing two organisms at functional level
- Composite comparison results (structural + functional similarities/differences)

## How to apply

First, parse KEGG reaction and metabolite data into a directed graph where metabolites are nodes and enzymatic reactions are edges, establishing the structural level that encodes network topology. Second, independently construct a functional level by mapping each metabolic pathway from KEGG to its designated metabolic function and associating those functions with the corresponding structural nodes and edges. Third, compute similarity indexes (using 'set' or 'multiset' comparison methods depending on whether reaction multiplicities matter) at both the structural level and functional level separately. This two-level separation allows you to detect topological differences independent of functional annotation, and functional divergence independent of structural rewiring, providing a comprehensive view of inter-organism metabolic relationships.

## Related tools

- **MetNet** (Primary tool that automates reconstruction of dual-level metabolic network representation, executes graph construction from KEGG data, and computes structural/functional similarity indexes) — https://github.com/simeoni-biolab/MetNet
- **KEGG** (Source database providing organism-specific reactions, metabolites, and pathway annotations that seed the graph construction)
- **Java (GraphStream, Guava, Apache POI libraries)** (Runtime environment and supporting libraries used by MetNet for graph algorithms, I/O, and visualization rendering)

## Examples

```
java -jar MetNet.jar hsa ptr set
```

## Evaluation signals

- Structural graph exhibits expected network properties: metabolites map to KEGG compound IDs, reactions map to KEGG reaction IDs with correct stoichiometry and directionality.
- Functional graph correctly assigns each structural pathway to one metabolic function; functions are consistent across both organisms being compared.
- Similarity indexes at structural level differ from those at functional level when topology and function diverge (validating dual-layer independence).
- Comparison results include both quantitative similarity scores (for each level) and visual network overlays showing consensus and divergent subnetworks.
- Two organisms compared via 'set' method (ignoring reaction multiplicity) produce different similarity index magnitudes than 'multiset' method (accounting for multiplicity).

## Limitations

- KEGG annotation completeness varies by organism; sparse or incomplete pathway annotations will produce incomplete or misleading functional-level graphs.
- The method does not model reaction directionality constraints or cofactor roles beyond simple graph topology; metabolic flux and thermodynamic feasibility are not encoded.
- Similarity indexes depend on the choice of 'set' vs. 'multiset' comparison; no principled guidance is provided for selecting between them for a given biological question.
- Configuration files (organismList.txt, pathwayList.txt) must be manually maintained and synchronized with KEGG updates; stale configurations produce outdated comparisons.

## Evidence

- [intro] Two-level graph structure and input retrieval: "a two-level representation of metabolic networks: a structural level representing the metabolic network topology and a functional level representing the metabolic functions of each pathway"
- [other] Nodes and edges definition: "Build the structural level: represent nodes as metabolites and edges as enzymatic reactions, encoding network topology."
- [other] Functional mapping procedure: "Build the functional level: assign each pathway to its corresponding metabolic function and map functions to the structural nodes and edges."
- [intro] KEGG data retrieval and workflow start: "their metabolic data are retrieved from KEGG and the corresponding networks of metabolic functions are built"
- [intro] Similarity-based comparison at both levels: "The approach is supported by similarity indexes for the comparisons at both levels"
- [readme] Executable tool invocation with method selection: "java -jar MetNet.jar hsa ptr set will start the execution for the organisms "hsa" (Homo Sapiens) and "prt" (Pan troglodytes) with the comparison method "set"."
