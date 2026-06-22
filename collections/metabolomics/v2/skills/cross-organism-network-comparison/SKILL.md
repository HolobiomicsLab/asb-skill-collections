---
name: cross-organism-network-comparison
description: Use when you have selected two organisms whose metabolic networks are available in KEGG and you need to quantitatively assess their structural and functional similarity to identify shared or divergent metabolic capabilities for comparative systems biology, drug target discovery, or evolutionary.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0621
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

# cross-organism-network-comparison

## Summary

Quantitatively compare metabolic networks of two organisms at both structural (topology) and functional (pathway annotation) levels using similarity indexes. This skill enables detection of metabolic pathway interactions and differences that inform drug engineering and medical science applications.

## When to use

Apply this skill when you have selected two organisms whose metabolic networks are available in KEGG and you need to quantitatively assess their structural and functional similarity to identify shared or divergent metabolic capabilities for comparative systems biology, drug target discovery, or evolutionary analysis.

## When NOT to use

- Organisms' metabolic data are not available in KEGG or cannot be automatically reconstructed
- Analysis goal is to study a single organism's metabolic network rather than comparative analysis between two organisms
- Input data are pre-computed similarity matrices or feature tables rather than raw metabolic network topology and annotations

## Inputs

- KEGG organism codes (two organisms)
- Metabolic network topology data from KEGG (nodes, edges, connectivity)
- Metabolic pathway annotations from KEGG (functional assignments)

## Outputs

- Structural-level similarity indexes (quantitative comparison of network topology)
- Functional-level similarity indexes (quantitative comparison of pathway functions)
- Aggregated comparison results file (structured output with both similarity score sets)
- Visual network comparison (from MetNet interface)

## How to apply

Load both organisms' metabolic network data from KEGG into MetNet. Extract structural features (nodes, edges, connectivity metrics) representing network topology and functional features (pathway annotations, metabolic function assignments) for each organism. Compute structural-level similarity indexes by comparing topology characteristics between the two networks. Compute functional-level similarity indexes by comparing pathway annotations and metabolic functions. Aggregate both sets of similarity scores and select a comparison method ('set' or 'multiset') depending on whether pathway multiplicity should be considered. Report results as a structured output file containing similarity scores at both levels, composing a comprehensive view of similarities and differences.

## Related tools

- **MetNet** (Java tool that automatically reconstructs metabolic networks for two organisms from KEGG and computes structural and functional similarity indexes for quantitative and visual comparison) — https://github.com/simeoni-biolab/MetNet
- **KEGG** (Source database from which metabolic data and pathway annotations for both organisms are retrieved to build corresponding networks of metabolic functions)

## Examples

```
java -jar MetNet.jar hsa ptr set
```

## Evaluation signals

- Both structural and functional similarity indexes are computed and reported (not missing either level)
- Similarity scores fall within a valid range (e.g., 0–1 or percentage) and are interpretable relative to the comparison method ('set' vs 'multiset')
- Output file contains aggregated results from both organisms with consistent formatting and completeness
- Visual network comparison (if generated) displays topological and functional differences between the two metabolic networks
- Comparison method parameter ('set' or 'multiset') correctly influences whether pathway multiplicity is considered in functional-level indexes

## Limitations

- Only organisms available in KEGG can be compared; metabolic data for non-sequenced or non-annotated organisms cannot be retrieved
- Comparison quality depends on the completeness and accuracy of KEGG metabolic annotations for each organism
- The two-level representation simplifies metabolic complexity; regulatory interactions, post-translational modifications, and organism-specific metabolic variants not in KEGG pathways are not captured
- Choice between 'set' and 'multiset' comparison methods requires prior knowledge of whether pathway multiplicity is biologically meaningful for the research question

## Evidence

- [readme] Metabolic pathway comparison and interaction between different species can detect important information for drug engineering and medical science: "Metabolic pathway comparison and interaction between different species can detect important information for drug engineering and medical science"
- [readme] MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG and to compare their two networks both quantitatively and visually: "MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG and to compare their two networks both quantitatively and visually"
- [readme] A two-level representation of metabolic networks is proposed: a structural level representing the metabolic network topology and a functional level representing the metabolic functions of each pathway: "a two-level representation of metabolic networks: a structural level representing the metabolic network topology and a functional level representing the metabolic functions of each pathway"
- [readme] The approach is supported by similarity indexes for the comparisons at both levels: "The approach is supported by similarity indexes for the comparisons at both levels"
- [other] Extract structural features (nodes, edges, connectivity metrics) from each organism's network topology. Extract functional features (pathway annotations, metabolic functions) from each organism's functional representation. Compute structural-level similarity indexes by comparing network topology characteristics between the two organisms. Compute functional-level similarity indexes by comparing metabolic function assignments and pathway annotations: "Extract structural features (nodes, edges, connectivity metrics) from each organism's network topology. 3. Extract functional features (pathway annotations, metabolic functions) from each organism's"
