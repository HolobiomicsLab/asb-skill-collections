---
name: kegg-data-retrieval-and-parsing
description: Use when when you have selected one or more organisms to analyze and need to extract their complete metabolic reaction and metabolite data from KEGG in order to build a network representation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3283
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3407
  tools:
  - MetNet
  - KEGG
  - Java
derived_from:
- doi: 10.1371/journal.pone.0246962
  title: MetNet
evidence_spans:
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network
- their metabolic data are retrieved from KEGG and the corresponding networks of metabolic functions are built
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# KEGG Data Retrieval and Parsing

## Summary

Retrieve metabolic data for one or more organisms from the KEGG database and parse KEGG reactions and metabolites into a machine-readable graph representation. This skill forms the foundation for reconstructing metabolic networks and enabling downstream comparative analysis.

## When to use

When you have selected one or more organisms to analyze and need to extract their complete metabolic reaction and metabolite data from KEGG in order to build a network representation. Use this skill as the first step before any metabolic network reconstruction, comparison, or functional annotation.

## When NOT to use

- If metabolic data has already been downloaded and parsed into a graph or adjacency matrix representation—this skill is redundant.
- If you only need to query individual reactions or metabolites without reconstructing a whole-network view—use direct KEGG API queries instead.
- If your organism is not available in KEGG or lacks sufficient reaction/metabolite annotation for meaningful network reconstruction.

## Inputs

- KEGG organism code(s) (string, e.g., 'hsa', 'ptr')
- KEGG pathway list (configuration file listing which pathways to retrieve)
- KEGG organism list (configuration file listing available organisms)

## Outputs

- Parsed metabolic network graph (nodes = metabolites, edges = enzymatic reactions)
- Structured reaction data (reaction ID, enzyme code, substrate/product pairs)
- Structured metabolite data (metabolite ID, chemical properties, pathway membership)

## How to apply

Using MetNet or equivalent tooling: (1) Specify the target organism(s) by their KEGG organism code (e.g., 'hsa' for Homo sapiens, 'ptr' for Pan troglodytes). (2) Query KEGG to retrieve all reactions and metabolites associated with each organism. (3) Parse the returned KEGG data—which includes reaction identifiers, enzyme codes, substrate/product metabolites, and pathway associations—into a structured graph representation where nodes represent metabolites and directed edges represent enzymatic reactions. (4) Validate that all reactions and metabolites have been successfully parsed and that the graph is topologically coherent (e.g., no isolated nodes, bidirectional edges where applicable). Store the parsed graph in a format suitable for downstream structural and functional analysis.

## Related tools

- **MetNet** (Java application that orchestrates KEGG data retrieval, parsing, and graph reconstruction for metabolic networks) — github.com/simeoni-biolab/MetNet
- **KEGG** (Source database from which metabolic data (reactions, metabolites, pathways, organism assignments) are retrieved)

## Examples

```
java -jar MetNet.jar hsa ptr set
```

## Evaluation signals

- All metabolites and reactions for the selected organism(s) are present in the parsed graph with no missing edges or nodes.
- Graph topology is valid: no duplicate reactions, no orphaned metabolites, bidirectionality is correctly encoded where applicable.
- Reaction and metabolite identifiers conform to KEGG nomenclature (e.g., 'R' prefix for reactions, 'C' prefix for compounds).
- Enzyme commission (EC) codes and pathway membership are correctly assigned to each reaction.
- The graph size (number of nodes and edges) is consistent with documented genome/metabolome complexity for the organism (e.g., human metabolic networks typically contain thousands of reactions and metabolites).

## Limitations

- KEGG data completeness varies by organism; less-studied species may have incomplete pathway and reaction annotations.
- MetNet relies on configuration files (organismList.txt, pathwayList.txt) that must be manually maintained and may lag behind KEGG updates.
- The parsing process assumes KEGG data is well-formed; malformed or deprecated KEGG entries may cause parsing errors or produce incomplete graphs.
- Spontaneous or non-enzymatic reactions may not be represented in KEGG, leading to incomplete network topology.

## Evidence

- [readme] MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG: "MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG"
- [readme] their metabolic data are retrieved from KEGG and the corresponding networks of metabolic functions are built: "their metabolic data are retrieved from KEGG and the corresponding networks of metabolic functions are built"
- [other] Reconstruct the metabolic network by parsing KEGG reactions and metabolites into a graph representation: "Reconstruct the metabolic network by parsing KEGG reactions and metabolites into a graph representation"
- [other] Retrieve metabolic data for the selected organism from KEGG using MetNet: "Retrieve metabolic data for the selected organism from KEGG using MetNet"
