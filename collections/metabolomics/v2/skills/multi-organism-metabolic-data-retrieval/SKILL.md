---
name: multi-organism-metabolic-data-retrieval
description: Use when when you have identifiers for two organisms available in KEGG and need to compare their metabolic networks quantitatively and visually at both structural (node–edge topology) and functional (pathway role) levels for applications in drug engineering, medical science, or systems biology.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0821
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_0625
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

# multi-organism-metabolic-data-retrieval

## Summary

Automatically retrieve metabolic pathway and reaction data from KEGG for two selected organisms, then reconstruct both structural (topology) and functional (pathway-level) metabolic network representations using MetNet. This skill enables systematic comparative analysis of metabolic capabilities across species.

## When to use

When you have identifiers for two organisms available in KEGG and need to compare their metabolic networks quantitatively and visually at both structural (node–edge topology) and functional (pathway role) levels for applications in drug engineering, medical science, or systems biology.

## When NOT to use

- When organism data is not available in KEGG or organism KEGG codes are unknown.
- When only a single organism's metabolic network is needed (use single-organism metabolic reconstruction instead).
- When the goal is pathway enrichment or statistical association testing rather than pairwise network topology comparison.

## Inputs

- KEGG organism codes (string pair, e.g., 'hsa', 'ptr')
- organismList.txt (configuration file listing available KEGG organisms)
- pathwayList.txt (configuration file listing pathways to consider)
- KEGG database (remote or local, via KEGG API)

## Outputs

- Metabolic network topology (structural level) for each organism
- Metabolic functional network representation for each organism
- Similarity index comparisons at structural level
- Similarity index comparisons at functional level
- Visual and quantitative comparison results

## How to apply

Load organism KEGG identifiers (e.g., 'hsa' for Homo sapiens, 'ptr' for Pan troglodytes) from the organismList.txt configuration file. Query the KEGG database to retrieve metabolic pathway and reaction data for each of the two organisms. Execute MetNet (a Java tool) with the retrieved KEGG data to automatically reconstruct the metabolic network topology at the structural level. Then execute MetNet to generate the functional-level representation that maps metabolic functions to each pathway. Finally, apply similarity indexes at both structural and functional levels to compare the two networks. The comparison method can be specified as either 'set' (unique pathways) or 'multiset' (considering pathway multiplicity).

## Related tools

- **MetNet** (Automatically reconstructs metabolic networks from KEGG data and performs structural/functional comparison via similarity indexes) — https://github.com/simeoni-biolab/MetNet
- **KEGG** (Source database providing metabolic pathway, reaction, and organism data via API queries)
- **Java** (Execution environment for MetNet tool compilation and runtime)

## Examples

```
java -jar MetNet.jar hsa ptr set
```

## Evaluation signals

- Both organism networks are successfully reconstructed with matching node counts and edge topology consistent with KEGG pathway definitions.
- Structural and functional network files export without errors and can be parsed into graph objects (e.g., via GraphStream or NetworkX).
- Similarity index values are computed and fall within the expected range (typically 0–1 or percentage); comparison results show non-identical networks for different organisms.
- Visual comparison output clearly shows differences and similarities in pathway topology and metabolic function distribution between the two organisms.
- Command-line execution with two valid KEGG organism codes and a specified comparison method ('set' or 'multiset') completes without exceptions and generates output files.

## Limitations

- Requires network connectivity or a local KEGG database mirror to retrieve organism metabolic data; offline use is not supported unless KEGG data is pre-cached.
- Limited to comparison of exactly two organisms; simultaneous multi-organism comparisons require sequential pairwise executions.
- Organism and pathway scope are constrained by the contents of organismList.txt and pathwayList.txt configuration files; manually updating these files is necessary for organisms or pathways not pre-listed.
- Network comparison is based on pathway and reaction topology; does not account for gene expression, regulation, or enzyme kinetics.

## Evidence

- [other] MetNet automatically reconstructs metabolic networks by retrieving metabolic data from KEGG for two organisms selected by the user, then builds the corresponding networks of metabolic functions.: "MetNet automatically reconstructs the metabolic network of two organisms selected in KEGG and to compare their two networks both quantitatively and visually"
- [other] The workflow loads organism identifiers from a configuration file, queries KEGG for pathway/reaction data, then reconstructs structural and functional network representations.: "Load organism identifiers from organismList.txt. 2. Query KEGG database to retrieve metabolic pathway and reaction data for each of the two organisms."
- [readme] MetNet proposes a two-level representation: structural level representing metabolic network topology and functional level representing metabolic functions of each pathway.: "a two-level representation of metabolic networks: a structural level representing the metabolic network topology and a functional level representing the metabolic functions of each pathway"
- [readme] Similarity indexes support comparisons at both structural and functional levels.: "The approach is supported by similarity indexes for the comparisons at both levels"
- [readme] MetNet is a Java tool that can be executed from the command line with three parameters: organism codes and comparison method.: "To run MetNet as a command line tool, the following three parameters must be specified: 1. KEGG code of the first organism to compare 2. KEGG code of the second organism to compare 3. comparison"
