---
name: redundant-node-removal-and-edge-classification
description: Use when after network partitioning, when you have identified connected subnetworks of features matched by isotope or adduct patterns and need to sanitize and categorize the relationships before tree construction. Use it when redundant features (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - networkx
  - treelib
  - mass2chem
  - Python 3
  - khipu
  techniques:
  - mass-spectrometry
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

# Redundant Node Removal and Edge Classification

## Summary

After partitioning a feature network into connected subnetworks, inspect each subnetwork to remove redundant (duplicate or erroneous) nodes and classify edges as either isotope or adduct type. This prepares the subnetwork for conversion into an optimal tree structure (khipu instance) suitable for neutral mass inference and ion annotation.

## When to use

Apply this skill after network partitioning, when you have identified connected subnetworks of features matched by isotope or adduct patterns and need to sanitize and categorize the relationships before tree construction. Use it when redundant features (e.g., duplicate ions detected at the same m/z or unresolved signals) have entered the network during pattern matching and must be removed to avoid degeneracy in downstream tree optimization.

## When NOT to use

- Input is a single isolated feature (not a connected subnetwork); this skill requires at least 2 nodes with edges.
- Edge types have already been reliably classified by prior steps or external tools; applying this skill redundantly may introduce inconsistency.
- The feature table lacks sufficient metadata (e.g., m/z precision, isotope/adduct pattern annotations) to distinguish genuine redundancy from biological multiplicity.

## Inputs

- connected subnetwork (networkx Graph or list of nodes and edges from a single connected component)
- feature list with m/z, retention time, and isotope/adduct pattern match labels
- isotope and adduct pattern library used for the original matching

## Outputs

- sanitized subnetwork (networkx Graph with redundant nodes removed)
- edge classification table (mapping edge ID to isotope or adduct type)
- metadata record of removed nodes (for traceability and QC)

## How to apply

For each connected subnetwork: (1) Inspect all nodes to identify and flag redundant features—nodes arising from mistakes or unresolved signals that duplicate other nodes in the subnetwork. (2) Remove flagged redundant nodes and their incident edges. (3) Classify the remaining edges into two types based on the original pattern match: isotope edges (connecting nodes differing by isotope mass shifts, e.g., 13C/12C = 2.010631 Da) and adduct edges (connecting nodes with adduct mass differences, e.g., M+H vs. M+Na). (4) Document the edge type as metadata on each edge in the graph. This classification is essential for the subsequent trunk-building step, which separately optimizes the adduct backbone and isotope branches to establish the empirical compound tree.

## Related tools

- **networkx** (Graph data structure and node/edge inspection and manipulation for redundancy detection and edge type assignment) — https://networkx.org/
- **mass2chem** (Provides isotope and adduct pattern library for edge classification and redundancy validation) — https://github.com/shuzhao-li-lab/mass2chem
- **khipu** (Orchestrates the full pipeline including this redundancy-removal and classification step within Weavor and Khipu classes) — https://github.com/shuzhao-li/khipu

## Examples

```
# Python snippet within khipu workflow after network partitioning
import networkx as nx
from khipu import Weavor, Khipu

# Assuming 'subnetwork' is a connected component from partitioning
weavor = Weavor(subnetwork, feature_data, isotope_patterns, adduct_patterns)
weavor.remove_redundant_nodes()  # Remove duplicates and erroneous signals
weavor.classify_edges()  # Label edges as isotope or adduct type
khipu_instance = weavor.build_tree()  # Convert sanitized subnetwork to tree
```

## Evaluation signals

- All removed nodes are recoverable from logs and do not reappear in the final khipu tree output.
- Every remaining edge in the subnetwork is labeled with either 'isotope' or 'adduct' type; no unlabeled edges remain.
- The number of nodes in the sanitized subnetwork is less than or equal to the original; redundancy removal does not increase node count.
- Isotope-classified edges exhibit m/z differences matching known isotope patterns (e.g., ±2.010631 Da for 13C/12C); adduct edges match known adduct mass shifts from the pattern library.
- The sanitized subnetwork produces a valid tree structure in the next step (trunk establishment and tree conversion) without errors due to cycles or isolated components.

## Limitations

- Redundancy detection relies on heuristics (e.g., identical m/z within mass tolerance, shared intensity profiles, or retention time clustering) and may miss subtle duplicates from instrument noise or co-eluting features with identical m/z.
- Edge classification depends on the completeness and accuracy of the isotope and adduct pattern library; missing or incorrect patterns will cause misclassification.
- Ambiguous edges (e.g., a mass shift matching both an isotope and an adduct pattern) require tie-breaking heuristics; the article does not specify detailed resolution rules, leaving interpretation to implementation.
- Features removed as redundant are sent to form new khipu instances; if the redundancy detection is overly aggressive, true biological variants may be lost to separate trees.

## Evidence

- [readme] Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure: "Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure"
- [other] For each subnetwork, inspect nodes and remove redundant features. Classify edges within each subnetwork as isotope or adduct type.: "For each subnetwork, inspect nodes and remove redundant features. Classify edges within each subnetwork as isotope or adduct type."
- [readme] Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu: "Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu"
- [readme] Separate isotope edges and adduct edges: "Separate isotope edges and adduct edges"
- [readme] The graph operations are supported by the networkx library: "The graph operations are supported by the networkx library"
