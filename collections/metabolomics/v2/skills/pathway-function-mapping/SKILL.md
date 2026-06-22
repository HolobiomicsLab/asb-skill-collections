---
name: pathway-function-mapping
description: Use when when you have reconstructed metabolic networks for two or more organisms from KEGG and need to compare them both topologically and functionally.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3083
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0601
  - http://edamontology.org/topic_3407
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

# pathway-function-mapping

## Summary

Map metabolic pathways retrieved from KEGG to their corresponding biological functions and integrate them into a dual-level network representation (structural topology + functional annotation). This skill enables quantitative and visual comparison of metabolic networks across organisms by encoding both reaction connectivity and pathway-level functional semantics.

## When to use

When you have reconstructed metabolic networks for two or more organisms from KEGG and need to compare them both topologically and functionally. Apply this skill if your analysis goal is to detect metabolic differences for drug engineering or medical science applications, and you require a structured representation that preserves both network structure (metabolite–reaction graphs) and semantic pathway function information.

## When NOT to use

- Input organisms are not available in KEGG or lack sufficient metabolic annotation coverage.
- Goal is solely to visualize a single organism's metabolic network without cross-organism functional comparison.
- Metabolic data has already been manually curated into a custom format incompatible with KEGG structure (reactions, metabolites, pathway functions must be parseable from KEGG).

## Inputs

- KEGG organism codes (e.g., 'hsa' for Homo sapiens, 'ptr' for Pan troglodytes)
- KEGG reaction database (enzymatic reactions with metabolite participants)
- KEGG pathway annotations (pathway IDs mapped to biological functions)
- Configuration files: organismList.txt, pathwayList.txt

## Outputs

- Dual-level metabolic network representation (structural graph + functional pathway map)
- Similarity index scores at structural level (network topology comparison)
- Similarity index scores at functional level (pathway function comparison)
- Comparative visualization of network differences/similarities between organisms

## How to apply

After retrieving metabolic data (reactions and metabolites) from KEGG for each organism, build a structural-level graph representation where nodes are metabolites and edges are enzymatic reactions. Simultaneously, retrieve pathway annotations from KEGG and assign each pathway to its corresponding metabolic function (e.g., glycolysis, citric acid cycle). Map these functional labels back to the structural nodes and edges to create a functional-level representation. Export both levels to structured formats (e.g., graph files with dual node/edge annotations) that support comparison. Use similarity indexes at both levels to quantify structural topology overlap and functional pathway alignment, enabling comprehensive organism-to-organism comparison.

## Related tools

- **MetNet** (Java application that automatically reconstructs metabolic networks from KEGG data and implements dual-level representation with pathway-to-function mapping and comparison via similarity indexes) — https://github.com/simeoni-biolab/MetNet
- **KEGG** (Source database providing organism-specific metabolic reactions, metabolites, and pathway functional annotations)

## Examples

```
java -jar MetNet.jar hsa ptr set
```

## Evaluation signals

- Structural level correctly encodes all KEGG reactions as edges and metabolites as nodes for both organisms; graph connectivity statistics (degree distribution, connected components) are reproducible.
- Functional level successfully maps each pathway from the organism's KEGG annotation to at least one metabolic function; no pathway remains unmapped.
- Similarity indexes at both levels return numeric scores in valid range (typically 0–1); structural and functional scores can be independently verified by manual spot-checking a subset of pathways.
- Comparative output identifies expected biological differences (e.g., pathways present in one organism but absent in another) consistent with known organism physiology.
- Exported network files conform to declared format schema and are parseable by visualization and comparison tools.

## Limitations

- Accuracy depends on KEGG annotation completeness; organisms with incomplete or outdated pathway coverage in KEGG will yield incomplete dual-level representations.
- Similarity indexes measure topological and functional overlap but do not account for enzyme kinetics, regulation, or metabolite concentration dynamics.
- The method requires manual configuration of pathwayList.txt; omitted pathways will not be included in functional-level representation and may bias organism comparison.
- MetNet operates on KEGG's static data at query time; metabolic networks may become stale if KEGG is updated without re-running the reconstruction.

## Evidence

- [intro] Metabolic pathway comparison and interaction between different species can detect important information for drug engineering and medical science: "Metabolic pathway comparison and interaction between different species can detect important information for drug engineering and medical science"
- [intro] Two-level representation with structural and functional levels: "a two-level representation of metabolic networks: a structural level representing the metabolic network topology and a functional level representing the metabolic functions of each pathway"
- [intro] Similarity indexes support both levels: "The approach is supported by similarity indexes for the comparisons at both levels"
- [readme] MetNet retrieves metabolic data from KEGG and builds networks: "their metabolic data are retrieved from KEGG and the corresponding networks of metabolic functions are built"
- [readme] Configuration file requirements for pathway selection: "pathwayList.txt : configuration file containing the list of patways to be considered for the comparison"
