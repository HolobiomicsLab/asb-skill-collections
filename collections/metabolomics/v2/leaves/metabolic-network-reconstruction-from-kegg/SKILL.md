---
name: metabolic-network-reconstruction-from-kegg
description: Use when you have selected two organisms (by KEGG code, e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3407
  tools:
  - MetNet
  - KEGG
  - Java
  license_tier: open
derived_from:
- doi: 10.1371/journal.pone.0246962
  title: MetNet
evidence_spans:
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic
  network of two organisms selected in KEGG
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic
  network
- their metabolic data are retrieved from KEGG and the corresponding networks of metabolic
  functions are built
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

# metabolic-network-reconstruction-from-kegg

## Summary

Automatically reconstruct and compare metabolic networks for two organisms by querying KEGG pathway and reaction data, then building two-level network representations (structural topology and functional mapping). Use this when you need to identify metabolic pathway similarities or differences between species for drug discovery or comparative genomics.

## When to use

You have selected two organisms (by KEGG code, e.g. 'hsa' for Homo sapiens, 'ptr' for Pan troglodytes) and need to systematically retrieve their metabolic pathway data from KEGG, reconstruct both the network topology and functional organization, and generate quantitative/visual comparisons of their metabolic capabilities.

## When NOT to use

- You only have one organism and no comparative goal — metabolic network reconstruction can be simpler without the comparison framework.
- Your organisms are not in the KEGG database or you lack KEGG access.
- You require real-time metabolic flux data or experimental metabolomics measurements — this skill reconstructs static network topology, not dynamic flux.

## Inputs

- KEGG organism code (e.g., 'hsa', 'ptr')
- organismList.txt (configuration file listing available organisms)
- pathwayList.txt (configuration file listing pathways to compare)

## Outputs

- Structural-level network representation (metabolic network topology for each organism)
- Functional-level network representation (metabolic functions mapped to pathways)
- Similarity index matrices (structural and functional levels)
- Comparative visualization of network differences and similarities

## How to apply

Load the two organism identifiers (KEGG codes) from configuration or command line. Query KEGG to retrieve metabolic pathway and reaction data for each organism using MetNet's KEGG API integration. Execute MetNet's reconstruction algorithm to build the structural-level network representation (nodes = metabolic entities, edges = reactions) for each organism. Then execute MetNet's functional-level mapper to overlay metabolic function annotations onto each pathway. Apply similarity indexes at both levels (structural topology similarity and functional pathway similarity). Export network representations and comparison matrices for visual and quantitative analysis. The comparison method (set-based or multiset-based) should be selected based on whether reaction multiplicity matters for your research question.

## Related tools

- **MetNet** (Java tool that automatically reconstructs metabolic network topology and functional-level representations, executes network comparison, and generates similarity indexes at structural and functional levels) — https://github.com/simeoni-biolab/MetNet
- **KEGG** (Database source for metabolic pathway, reaction, and organism data retrieval)

## Examples

```
java -jar MetNet.jar hsa ptr set
```

## Evaluation signals

- Both organisms' metabolic networks successfully load with non-zero node and edge counts; network topology is acyclic or contains only known regulatory cycles.
- Functional-level mapping produces metabolic function annotations for ≥80% of pathways retrieved; no pathway lacks a functional classification.
- Similarity indexes are bounded in [0, 1] and differ between the two organisms (not identical networks); set-based and multiset-based comparisons yield consistent rank ordering of pathway similarities.
- Exported network files (GraphML, JSON, or visual image) are valid and renderable; visual comparison clearly highlights structural and functional differences.
- If comparing known organisms (e.g., human vs. primate), similarity indexes should be higher than unrelated species; metabolic pathway coverage should match published KEGG annotation counts.

## Limitations

- Reconstruction depends entirely on KEGG data completeness; organisms with sparse KEGG annotation will produce incomplete networks.
- The two-level representation (structural + functional) assumes independence between topology and function; does not account for allosteric regulation, enzyme isoforms, or post-translational modifications.
- Comparison via similarity indexes at both levels is qualitative; no statistical significance testing or confidence intervals are provided for index differences.
- Command-line execution requires manual specification of KEGG organism codes and comparison method; mistyped codes or missing configuration files (organismList.txt, pathwayList.txt) cause silent failures or incorrect organism selection.

## Evidence

- [intro] MetNet automatically reconstructs metabolic networks by retrieving metabolic data from KEGG for two organisms selected by the user, then builds the corresponding networks of metabolic functions.: "MetNet automatically reconstructs the metabolic network of two organisms selected in KEGG and to compare their two networks both quantitatively and visually"
- [intro] The skill applies a two-level representation of metabolic networks with a structural level (topology) and functional level (pathway mapping).: "a two-level representation of metabolic networks: a structural level representing the metabolic network topology and a functional level representing the metabolic functions of each pathway"
- [intro] Metabolic comparison is supported by similarity indexes at both the structural and functional levels.: "The approach is supported by similarity indexes for the comparisons at both levels"
- [readme] MetNet is a Java tool requiring library dependencies (gs-algo, gs-core, gs-ui, guava, poi, sax2r2) and configuration files.: "MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG"
- [readme] Command-line invocation requires three parameters: organism codes and comparison method.: "To run MetNet as a command line tool, the following three parameters must be specified when starting the execution: 1. KEGG code of the first organism to compare 2. KEGG code of the second organism"
