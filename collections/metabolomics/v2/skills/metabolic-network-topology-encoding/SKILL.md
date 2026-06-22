---
name: metabolic-network-topology-encoding
description: Use when when you have reconstructed metabolic networks for one or more organisms and need to represent them in a way that preserves both the graph topology (connectivity structure) and the metabolic function annotations (pathway membership and enzymatic roles) for subsequent cross-organism.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_0821
  tools:
  - MetNet
  - Java
  - KEGG
derived_from:
- doi: 10.1371/journal.pone.0246962
  title: MetNet
evidence_spans:
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network
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
---

# metabolic-network-topology-encoding

## Summary

Construct a two-level representation of a reconstructed metabolic network that encodes both structural topology (nodes as metabolites, edges as enzymatic reactions) and functional pathway information, enabling quantitative comparison of metabolic networks between organisms.

## When to use

When you have reconstructed metabolic networks for one or more organisms and need to represent them in a way that preserves both the graph topology (connectivity structure) and the metabolic function annotations (pathway membership and enzymatic roles) for subsequent cross-organism comparison or functional analysis.

## When NOT to use

- Input is already a pre-computed metabolic network object; use this skill only when starting from raw KEGG data that requires parsing and graph construction.
- The analysis goal is only pathway enumeration without network topology; structural encoding is unnecessary if you only need pathway lists.
- Organisms lack sufficient KEGG annotation or coverage; the method requires complete or near-complete pathway and reaction data from KEGG.

## Inputs

- KEGG organism codes (e.g., 'hsa' for Homo sapiens)
- KEGG reaction and metabolite data
- Pathway annotations from KEGG

## Outputs

- Structural-level network representation (nodes, edges, connectivity metrics)
- Functional-level network representation (pathway annotations, metabolic function assignments)
- Two-level metabolic network object(s) in structured format suitable for comparison

## How to apply

First, retrieve metabolic data from KEGG using MetNet for the selected organism(s). Parse KEGG reactions and metabolites into a graph representation where nodes represent metabolites and edges represent enzymatic reactions, encoding the structural network topology. Simultaneously, assign each reaction and pathway to its corresponding metabolic function and map these function annotations to the structural nodes and edges. Export both the structural level (topology with connectivity metrics) and the functional level (pathway annotations and metabolic functions) to structured formats (e.g., Java objects or serialized graph representations) that support subsequent similarity index computation and visualization. The two-level encoding enables independent or comparative analysis at the structural topology level and at the functional pathway level.

## Related tools

- **MetNet** (Java tool that automatically reconstructs metabolic networks from KEGG data and encodes both structural topology and functional pathway information) — https://github.com/simeoni-biolab/MetNet
- **KEGG** (Source database providing reaction, metabolite, and pathway annotations for metabolic network reconstruction)

## Examples

```
java -jar MetNet.jar hsa ptr set
```

## Evaluation signals

- Structural level contains all metabolites as nodes and all enzymatic reactions as edges retrieved from KEGG, with no missing or orphaned nodes.
- Functional level has every pathway and metabolic function correctly mapped to corresponding nodes and edges in the structural representation.
- Both levels are consistently synchronized — each structural edge has a corresponding functional annotation, and vice versa.
- Exported representation can be successfully loaded and parsed for downstream similarity index computation without format errors.
- Network connectivity metrics (degree, betweenness, etc.) and pathway annotations are reproducible and match independently queried KEGG data.

## Limitations

- Reconstruction fidelity depends on KEGG annotation completeness; organisms with sparse KEGG coverage will produce incomplete two-level representations.
- The method encodes only reactions and pathways present in KEGG; non-canonical or organism-specific metabolic routes not in KEGG are excluded.
- No handling of conditional or context-dependent metabolism (e.g., tissue-specific or growth-condition-dependent pathways) within the two-level encoding itself.
- Scalability to very large metabolic networks (thousands of metabolites and reactions) may be limited by Java memory and graph traversal performance.

## Evidence

- [intro] structural level that represents metabolic network topology and a functional level that represents the metabolic functions of each pathway: "a two-level representation of metabolic networks: a structural level representing the metabolic network topology and a functional level representing the metabolic functions of each pathway"
- [other] nodes as metabolites and edges as enzymatic reactions: "represent nodes as metabolites and edges as enzymatic reactions, encoding network topology"
- [other] assign each pathway to its corresponding metabolic function and map functions to the structural nodes and edges: "assign each pathway to its corresponding metabolic function and map functions to the structural nodes and edges"
- [readme] MetNet is a Java tool that automatically reconstructs the metabolic network of two organisms selected in KEGG: "MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG"
- [readme] metabolic data are retrieved from KEGG and the corresponding networks of metabolic functions are built: "their metabolic data are retrieved from KEGG and the corresponding networks of metabolic functions are built"
