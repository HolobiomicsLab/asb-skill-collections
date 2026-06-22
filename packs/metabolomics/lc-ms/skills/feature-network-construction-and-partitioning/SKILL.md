---
name: feature-network-construction-and-partitioning
description: Use when you have a preprocessed LC-MS feature table (m/z, retention time, intensity columns) and need to identify which features belong together as isotopes or adducts of the same neutral compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0599
  tools:
  - networkx
  - treelib
  - mass2chem
  - Python 3
  - metDataModel
  techniques:
  - LC-MS
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

# feature-network-construction-and-partitioning

## Summary

Construct a graph of mass spectrometry features by matching isotope and adduct patterns, then partition it into connected subnetworks to group related ions into empirical compounds. This skill transforms a flat feature list into a structured annotation intermediate suitable for neutral mass inference and metabolite identification.

## When to use

You have a preprocessed LC-MS feature table (m/z, retention time, intensity columns) and need to identify which features belong together as isotopes or adducts of the same neutral compound. This skill is essential when you must annotate degenerate ions, infer neutral mass, or analyze isotope tracing experiments where multiple ion species arise from a single metabolite.

## When NOT to use

- Input is already annotated to known metabolites or spectral libraries; this skill performs *de novo* grouping and is redundant after compound identification.
- Feature table lacks precise m/z or retention time information; pattern matching depends on mass accuracy (typically ≤ 5 ppm) and optional retention time tolerance.
- Data are from targeted or scheduled LC-MS methods measuring only a few known compounds; network partitioning excels with untargeted data containing hundreds of features from unknown metabolites.

## Inputs

- feature table (tab-delimited text: columns ≥ feature_ID, m/z, retention_time, intensity_start...intensity_end)
- isotope pattern library (mass shifts and charge differences)
- adduct pattern library (mass shifts and charge differences)
- mass tolerance parameter in ppm (part per million)

## Outputs

- connected subnetwork partitions (one per empirical compound)
- khipu instances in JSON format (tree-structured ion relationships)
- khipu instances in tab-delimited TSV format
- node classification (isotope vs. adduct edges)
- adduct trunk structure (root, linear path, node coverage count)

## How to apply

Load a feature table (tab-delimited, with m/z and retention time columns) and an isotope/adduct pattern library (defining expected mass and charge differences). Use mass2chem to search all feature pairs against the pattern library, matching pairs within a specified ppm tolerance (default used in khipu; adjustable via --ppm parameter). Connect all matched pairs using networkx to form a single graph. Apply networkx's connected_components algorithm to partition this graph into disjoint connected subnetworks. Each subnetwork represents one empirical compound (khipu instance). For each subnetwork, inspect nodes for redundancy, classify edges as isotope or adduct type, and optionally establish an adduct trunk by optimizing node coverage to create an optimal tree structure. Retain only nodes that pass quality inspection; isolated or erroneous nodes are removed and may form new khipu instances.

## Related tools

- **networkx** (Construct the feature graph by connecting matched pairs; partition graph into connected components) — https://networkx.org
- **mass2chem** (Search feature pairs against isotope and adduct patterns to identify matches within mass tolerance) — https://github.com/shuzhao-li-lab/mass2chem
- **treelib** (Convert optimized subnetwork to tree structure for hierarchical visualization and output) — https://pypi.org/project/treelib
- **metDataModel** (Define data model for empirical compound (khipu instance) representation and serialization) — https://github.com/shuzhao-li-lab/metDataModel

## Examples

```
khipu -i testdata/ecoli_pos.tsv -o ecoli_annotation --ppm 5 --rtol 0.2
```

## Evaluation signals

- All matched feature pairs are connected in the graph; verify by comparing cardinality of edges against total pattern matches reported by mass2chem.
- Connected components are disjoint; verify by checking that no feature appears in more than one subnetwork partition.
- Each subnetwork is acyclic after tree optimization; verify absence of cycles using networkx acyclic detection.
- Redundant nodes (e.g., multiple features with identical m/z and isotopic offset) are removed; verify node count decreases after inspection step.
- Neutral mass inference is stable; verify by checking that linear regression on khipu grid produces consistent neutral mass estimates and that residuals are within expected measurement noise (typically < 5 ppm error).

## Limitations

- Pattern-matching ambiguity can cause false groupings when overlapping isotope or adduct mass shifts occur; some ions may enter the network by mistake and are later removed to form separate khipu instances.
- Adduct trunk optimization is greedy and may not find the globally optimal tree; results depend on the order of edge processing and choice of root node.
- Retention time tolerance (rtol parameter) is arbitrary and tool-dependent; user must calibrate it for their preprocessing pipeline to avoid grouping co-eluting but distinct metabolites.
- The method assumes all ions in the initial network are genuine signals; noise, unresolved signals, or contamination that happen to match isotope/adduct patterns will be included initially and must be filtered downstream.
- Pattern library must be provided or curated by the user; default patterns may not capture all adducts or isotopes relevant to a specific analytical method or biochemical experiment.

## Evidence

- [other] Search feature list using mass2chem to identify all feature pairs matching any isotope or adduct pattern.: "Start with an initial list of isotope patterns and adduct patterns (see khipu grid below). Search feature list to get all pairs that match any of the pattern"
- [other] Construct an overall network by connecting all pattern-matched feature pairs using networkx.: "Connect all pattern-matched feature pairs to an overall network, which is further partitioned into connected subnetworks"
- [other] Partition the network into connected subnetworks using networkx connected-components algorithm.: "The graph operations are supported by the networkx library"
- [other] For each subnetwork, inspect nodes and remove redundant features, then convert to tree structure.: "Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure"
- [readme] Khipu applies to regular LC-MS data and enables analysis of isotope tracing and chemical labeling data.: "This applies to regular LC-MS data, but also enables easy analysis of isotope tracing and chemical labeling data"
- [readme] Some ions may enter the network by mistakes or unresolved signals and are removed from the established khipu.: "Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu"
