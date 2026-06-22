---
name: connected-component-decomposition-in-mass-spectrometry
description: Use when you have a feature list from LC-MS preprocessing (e.g., asari output) and have already identified all pairwise feature matches to isotope and adduct patterns. Apply this skill when you need to separate feature matches into disjoint empirical compounds—i.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - networkx
  - treelib
  - mass2chem
  - Python 3
  - khipu
  - metDataModel
derived_from:
- doi: 10.1021/acs.analchem.2c05810
  title: khipu
evidence_spans:
- The graph operations are supported by the networkx library
- tree visualization aided by the treelib library
- Khipu uses our package mass2chem for search functions
- Khipu is developed as an open source Python 3 package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_khipu_cq
    doi: 10.1021/acs.analchem.2c05810
    title: khipu
  dedup_kept_from: coll_khipu_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c05810
  all_source_dois:
  - 10.1021/acs.analchem.2c05810
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# connected-component-decomposition-in-mass-spectrometry

## Summary

Partition a network of mass spectrometry features (connected via isotope and adduct relationships) into independent connected subnetworks, each representing a single empirical compound. This decomposition enables downstream annotation and neutral mass inference by organizing degenerate ions into tree-structured khipu instances.

## When to use

You have a feature list from LC-MS preprocessing (e.g., asari output) and have already identified all pairwise feature matches to isotope and adduct patterns. Apply this skill when you need to separate feature matches into disjoint empirical compounds—i.e., when a single overall network of matched pairs must be partitioned so that each connected component becomes one independent khipu instance for annotation and neutral mass recovery.

## When NOT to use

- Input is already pre-partitioned into empirical compounds or single-ion features (connected-component decomposition assumes an unparsed network of feature pairs).
- No isotope or adduct relationships are present in the feature list (the network will be trivial—all singletons—and decomposition adds no value).
- Features have not yet been matched to isotope/adduct patterns; this skill assumes pattern matching is complete and yields a full feature–pair graph.

## Inputs

- Feature table (tab-delimited: feature ID, m/z, retention time, intensities)
- Isotope pattern library (m/z shifts and element assignments)
- Adduct pattern library (m/z shifts and adduct compositions)
- Mass precision tolerance (ppm, e.g., 5–10 ppm)

## Outputs

- Partition of features into connected subnetworks (graph structure)
- Set of khipu instances (one per connected component, JSON and tab-delimited formats)
- Per-khipu neutral mass estimates (via linear regression on grid)
- Classification of edges as isotope or adduct type within each khipu

## How to apply

Load the feature list and isotope/adduct pattern library (e.g., m/z shifts for 13C, [M+H]+, [M+Na]+, etc., typically with ppm tolerance ~5–10 ppm). Use mass2chem to search the feature list and identify all feature pairs matching any isotope or adduct pattern. Construct an undirected network in networkx where nodes are features and edges connect all pattern-matched pairs. Apply the connected-components algorithm to partition this network into maximal connected subnetworks. For each subnetwork, inspect nodes for redundancy (e.g., duplicate or near-identical features), remove redundant nodes, classify edges as isotope or adduct type, and optimize an adduct trunk (root + linear path) that maximizes node coverage. Convert each trunk-rooted subnetwork to an optimal tree structure and output as a khipu instance. The rationale is that connected components identify independent metabolite groups, reducing annotation ambiguity and enabling reliable neutral mass regression on a per-compound basis.

## Related tools

- **networkx** (Construct undirected feature network from matched pairs; partition into connected components using connected_components() algorithm) — https://networkx.org/
- **mass2chem** (Search feature list against isotope and adduct pattern library to identify matching feature pairs) — https://github.com/shuzhao-li-lab/mass2chem
- **treelib** (Convert trunk-rooted subnetwork to optimal tree structure and enable tree visualization) — https://github.com/caesar0301/treelib
- **khipu** (End-to-end implementation of feature matching, network construction, connected-component decomposition, and khipu instance output) — https://github.com/shuzhao-li/khipu
- **metDataModel** (Provides data model for empirical compound representation and khipu instance schema) — https://github.com/shuzhao-li-lab/metDataModel

## Examples

```
python3 -m khipu.main -i testdata/ecoli_pos.tsv -o ecoli_decomposed --ppm 5 --mode pos
```

## Evaluation signals

- All features from the input list appear exactly once across all output khipu instances (no duplication or loss).
- Each output khipu instance forms a single connected subnetwork; no two khipus share a feature or edge.
- Redundant nodes (e.g., features with identical or near-identical m/z and rtime within a subnetwork) have been identified and removed prior to tree conversion.
- Each khipu has a well-defined adduct trunk with a single root node and a linear path of adduct edges; isotope edges branch from adduct nodes without creating cycles.
- Neutral mass estimates derived via linear regression on the khipu grid are consistent across ions within each khipu (low residual error; typically inspected visually or via R² metric).

## Limitations

- Some ions may enter the initial network due to noise or unresolved signals. These are removed from the established khipu and sent to form a new khipu, potentially generating spurious single-ion instances.
- Connected-component decomposition assumes clean pattern matching; errors in isotope/adduct pattern definition or mass tolerance settings will propagate and cause features to be grouped or separated incorrectly.
- Performance scales with the size of the feature network; very large networks or dense subnetworks may require optimization in networkx operations.
- Retention time filtering is not applied by default in the decomposition step; users must pre-filter features or supply retention time tolerance (rtol) if retention time should inform connectivity.

## Evidence

- [readme] Connect all pattern-matched feature pairs to an overall network, which is further partitioned into connected subnetworks: "Connect all pattern-matched feature pairs to an overall network, which is further partitioned into connected subnetworks"
- [readme] Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure: "Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure"
- [other] The construction loop begins by searching a feature list against isotope and adduct patterns to identify matching pairs. All matched pairs are then connected into a single overall network. This network is subsequently partitioned into connected subnetworks, with each subnetwork converted into one khipu instance after inspection and removal of redundant nodes.: "The construction loop begins by searching a feature list against isotope and adduct patterns to identify matching pairs. All matched pairs are then connected into a single overall network. This"
- [other] Partition the network into connected subnetworks using networkx connected-components algorithm: "Partition the network into connected subnetworks using networkx connected-components algorithm"
- [readme] Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu: "Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu"
