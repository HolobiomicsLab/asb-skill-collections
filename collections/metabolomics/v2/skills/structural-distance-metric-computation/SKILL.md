---
name: structural-distance-metric-computation
description: 'Use when you have two or more lipid structures (in standardized lipid nomenclature or chemical format) and need to: (1) quantify structural dissimilarity for hierarchical clustering of lipidomes; (2) identify lipids responsible for shaping lipidome composition via distance-based feature selection;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0360
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - LipidSpace
  - cppGoslin
derived_from:
- doi: 10.1021/acs.analchem.3c02449
  title: LipidSpace
evidence_spans:
- LipidSpace is a stand-alone tool to analyze and compare lipidomes
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidspace_cq
    doi: 10.1021/acs.analchem.3c02449
    title: LipidSpace
  dedup_kept_from: coll_lipidspace_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c02449
  all_source_dois:
  - 10.1021/acs.analchem.3c02449
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# structural-distance-metric-computation

## Summary

Compute normalized pairwise structural distance metrics between lipid molecules by representing each as a labeled graph encoding atom connectivity and functional groups, then aligning graphs to identify structural dissimilarities. This skill enables quantitative comparison of lipid structural space and clustering of lipidomes by chemical similarity.

## When to use

Apply this skill when you have two or more lipid structures (in standardized lipid nomenclature or chemical format) and need to: (1) quantify structural dissimilarity for hierarchical clustering of lipidomes; (2) identify lipids responsible for shaping lipidome composition via distance-based feature selection; or (3) rank lipid pairs by structural relatedness for quality control. Particularly useful when sn-positions are unspecified (e.g., 'PC 18:0_16:1') and fatty acyl chain order may vary between molecules.

## When NOT to use

- Input lipids are already represented as precomputed feature vectors or intensity tables (use a distance metric on those directly instead).
- Sn-positions are fully specified and order matters semantically for your biological question (standard ordered comparison is already default).
- You require sub-structural (subgraph) matches rather than complete pairwise distances (consider separate subgraph isomorphism tools).

## Inputs

- lipid structure (standardized nomenclature or parsed chemical structure)
- pair of lipid molecules to compare
- optional: fatty acyl chain comparison mode (ordered vs. all-combinations)

## Outputs

- pairwise distance score (scalar, range 0–1 for bounded metric or 0–∞ for unbound)
- distance matrix (for multiple lipid pairs)
- graph alignment correspondence (atom/bond mappings)

## How to apply

First, parse each input lipid structure into a labeled graph representation encoding atom types, bond orders, and functional group composition. Align the two graph structures using graph isomorphism or subgraph matching to identify corresponding atoms and bonds between the pair. Compute a structural distance metric based on differences in atom types, bond orders, and functional group composition detected during alignment. Normalize the result to a bounded scalar in the range [0–1], where 0 indicates identical structures and 1 indicates maximal dissimilarity. For improved accuracy when sn-positions are unknown, optionally compute all combinations of fatty acyl chain comparisons and return the minimum distance, though this reduces performance. Optionally activate unbound distance metrics (range 0 to ∞) for more accurate results when visibility of large distances is acceptable.

## Related tools

- **LipidSpace** (implements graph-based lipid structure comparison and distance computation; provides GUI and REST API for calculating bounded (0–1) and unbound (0–∞) distance metrics, with support for fatty acyl chain mode selection and clustering linkage strategies) — https://github.com/lifs-tools/lipidspace
- **cppGoslin** (dependency of LipidSpace; parses and represents lipid structures as graphs encoding atom connectivity and functional groups) — https://github.com/lifs-tools/cppgoslin

## Examples

```
curl -X POST -H 'Content-Type: application/json' --data-binary '@examples/Rest/Plasma-Singapore-Short.json' localhost:8888/lipidspace/v1/pca
```

## Evaluation signals

- Identical lipids (same structure, same sn-positions) return distance = 0.
- Completely different lipid classes or carbon chain lengths return distance approaching 1 (bounded) or large values (unbound).
- Distance matrix is symmetric (d[i,j] = d[j,i]) and satisfies triangle inequality when using metric variants.
- Hierarchical clustering dendrogram produced from distance matrix shows expected lipidome groupings (lipids with similar structural features cluster together).
- When fatty acyl chain all-combinations mode is enabled, unspecified sn-position lipids (e.g., 'PC 18:0_16:1' vs. 'PC 16:1_18:0') show lower distances than in ordered mode.

## Limitations

- Performance degrades significantly when all-combinations fatty acyl chain mode is enabled (exponential in number of chains).
- Unbound distance metrics reduce lipid space visibility due to potentially very large distance values.
- Graph alignment relies on isomorphism/subgraph matching; ambiguous or complex functional group representations may affect reproducibility.
- Bounded [0–1] metric is default; switching to unbound metric requires explicit menu selection and may not be suitable for all downstream analyses (e.g., visualization, clustering with fixed distance thresholds).
- Analysis cannot be saved or loaded; re-running identical analyses requires re-importing data and reconfiguring parameters.

## Evidence

- [other] Parse and represent each input lipid structure as a labeled graph encoding atom connectivity and functional groups. Align the two graph structures using graph isomorphism or subgraph matching to identify corresponding atoms and bonds. Compute a structural distance metric based on the graph alignment, accounting for differences in atom types, bond orders, and functional group composition. Return the pairwise distance score as a normalized scalar value (0–1 or similar range) indicating structural dissimilarity.: "Parse and represent each input lipid structure as a labeled graph encoding atom connectivity and functional groups. Align the two graph structures using graph isomorphism or subgraph matching to"
- [intro] A graph-based comparison of lipid structures allows to calculate distances between lipids and to determine similarities across lipidomes.: "A graph-based comparison of lipid structures allows to calculate distances between lipids and to determine similarities across lipidomes"
- [readme] In default mode, LipidSpace is comparing the first fatty acyl chain (FA) of the first lipid with the first FA of the second lipid, the second FA of the first lipid with the second FA of the second lipid, etc. However, when the sn-position is not specified as for instance in PC 18:0_16:1, a mode can be activated to compare all combinations of FA comparisons for both lipids and picking the lowest distance.: "when the sn-position is not specified as for instance in PC 18:0_16:1, a mode can be activated to compare all combinations of FA comparisons for both lipids and picking the lowest distance"
- [readme] As default, LipidSpace is using a bound distance metric to compare the structure of any two lipids. That means that the distance is a value that ranges between 0 (both lipids are identical) and 1. However, other distance measures suggest an unbound distance ranging from 0 to infinity.: "a bound distance metric to compare the structure of any two lipids. That means that the distance is a value that ranges between 0 (both lipids are identical) and 1. However, other distance measures"
- [intro] It allows for a rapid (re)analysis of experiments, identifies lipids responsible for shaping the respective lipidome, and provides methods for quality control.: "identifies lipids responsible for shaping the respective lipidome, and provides methods for quality control"
