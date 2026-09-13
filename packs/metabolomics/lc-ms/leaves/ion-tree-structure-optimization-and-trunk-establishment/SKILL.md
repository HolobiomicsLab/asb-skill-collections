---
name: ion-tree-structure-optimization-and-trunk-establishment
description: Use when after you have partitioned a feature network into connected
  subnetworks (each containing ion features linked by isotope or adduct mass differences).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0157
  tools:
  - networkx
  - treelib
  - mass2chem
  - Python 3
  - khipu
  - metDataModel
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-tree-structure-optimization-and-trunk-establishment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill optimizes a connected subnetwork of matched isotope and adduct ion features into a tree structure by identifying an adduct trunk (root and linear path) that maximizes node coverage, then assigns isotopic branches to that trunk. It converts a flat feature relationship graph into a hierarchical empirical compound representation suitable for neutral mass inference and ion annotation.

## When to use

Apply this skill after you have partitioned a feature network into connected subnetworks (each containing ion features linked by isotope or adduct mass differences). Use it when you need to convert a potentially cyclic or redundant subnetwork into a canonical tree structure for neutral mass calculation, ion species assignment, and compound annotation in untargeted LC-MS metabolomics or stable isotope tracing experiments.

## When NOT to use

- If the subnetwork contains fewer than 2 feature nodes—a single ion cannot be optimized into a meaningful tree structure.
- If all edges in the subnetwork are of only one type (all isotope or all adduct) and no branching topology is possible, consider whether the subnetwork represents a trivial or malformed network.
- If the subnetwork contains cyclic relationships that cannot be resolved by edge classification (e.g., three ions mutually matching isotope and adduct patterns simultaneously)—this suggests overlapping or ambiguous patterns that should be re-evaluated at the pattern-matching stage.

## Inputs

- connected subnetwork (networkx Graph object with feature nodes and isotope/adduct edges)
- list of feature nodes with m/z values
- isotope pattern list (e.g., 1.003355 Da for 13C/12C shift)
- adduct pattern list (e.g., +1.007276 for M+H[+], +18.033826 for M+NH4[+])
- theoretical khipu grid (matrix of neutral mass M0 and isotopologue m/z shifts by adduct type)

## Outputs

- tree-structured khipu instance (treelib Tree object) with root, trunk (adduct path), and branches (isotope groups)
- optimized neutral mass estimate (via linear regression against khipu grid)
- edge classification per ion pair (isotope or adduct type)
- JSON and tab-delimited representation of the khipu (empirical compound) with node metadata and tree hierarchy

## How to apply

First, separate isotope edges from adduct edges within the subnetwork. Group connected isotope edges by shared nodes—each group belongs to one adduct type and forms one 'branch'. Then establish an adduct trunk by identifying a root node and a linear path through adduct edges that optimizes coverage (maximizes the number of nodes explained by the fewest adduct steps). Assign each isotopic branch to nodes along this adduct trunk, re-aligning isotopic spacing to match the theoretical khipu grid (e.g., M0, 13C/12C, 13C/12C*2, etc.). Finally, convert the rooted structure to a tree using treelib and remove any redundant or misassigned nodes. This creates a unique, optimal tree representation per subnetwork.

## Related tools

- **networkx** (partition the overall network into connected subnetworks and support graph operations for edge/node traversal during trunk optimization)
- **treelib** (convert the optimized trunk-rooted subnetwork into a canonical tree data structure and enable tree visualization)
- **mass2chem** (provide isotope and adduct pattern matching functions used upstream to label edges before tree optimization) — https://github.com/shuzhao-li-lab/mass2chem
- **khipu** (orchestrate the full pipeline including subnetwork partitioning, trunk establishment, and tree construction into empirical compound (khipu instance) output) — https://github.com/shuzhao-li-lab/khipu
- **metDataModel** (define the data model for the output empirical compound object and its JSON/TSV serialization formats) — https://github.com/shuzhao-li-lab/metDataModel

## Examples

```
python3 -m khipu.main -i feature_table.tsv --ppm 5 --rtol 10 -o output_khipus
```

## Evaluation signals

- The output tree is acyclic and fully connected, with exactly one root node (the adduct trunk root) and all other nodes reachable via a unique path.
- Isotope edges form contiguous branches off the adduct trunk; no isotope edge crosses multiple adduct nodes.
- The trunk path is linear (each adduct node has at most one adduct parent and one adduct child) and covers the maximum number of feature nodes relative to alternative roots.
- Neutral mass estimated via linear regression of observed m/z values against the khipu grid matches expected biochemical mass ranges (e.g., typical metabolite MW 50–1500 Da for small-molecule LC-MS).
- All redundant nodes (e.g., duplicate m/z values or nodes fully explained by isotope shifts from a parent) have been removed; node count is minimal while preserving all distinct ion species in the subnetwork.

## Limitations

- Some ions may enter the initial network by mass measurement error or unresolved signals and are incorrectly assigned to the tree; these are removed post-hoc and sent to form a separate khipu, reducing the completeness of the original subnetwork.
- The choice of adduct trunk root and path is greedy and depends on the order of isotope and adduct pattern matching; if multiple equally optimal trunks exist, the algorithm may select one arbitrarily, leading to different tree topologies for the same subnetwork.
- The khipu grid assumes regular isotopic spacing (e.g., uniform 1.003355 Da per 13C); rare isotopes or unusual derivatization shifts may not align well to the grid, reducing accuracy of neutral mass inference.
- Performance and optimality degrade if the subnetwork is large (>50 nodes) or highly connected; the trunk-finding algorithm may not explore all possible roots exhaustively in such cases.
- The method assumes no overlapping or competing adduct types (e.g., M+H[+] and M+NH4[+] are mutually exclusive for a given neutral mass in the same khipu); ambiguity can lead to incorrect trunk assignment.

## Evidence

- [readme] Separate isotope edges and adduct edges within each subnetwork; group connected isotope edges by shared nodes—each group belongs to one adduct type and forms one 'branch'.: "Separate isotope edges and adduct edges. The isotope edges form their own groups by shared nodes, each group belong to one adduct type. Each group of connected isotope edges is treated as one"
- [intro] Establish an adduct trunk by optimizing node coverage and selecting a root and linear path through adduct edges.: "Establish an adduct trunk by optimizing node coverage and selecting a root and linear path through adduct edges."
- [intro] For each subnetwork, inspect nodes and remove redundant features; convert the trunk-rooted subnetwork to an optimal tree structure.: "For each subnetwork, inspect nodes and remove redundant features. ... Convert the trunk-rooted subnetwork to an optimal tree structure and output as a khipu instance using treelib."
- [readme] Re-align isotopes in all branches to establish optimal match to the khipu grid; based on available ions and the theoretical khipu grid, neutral mass can be obtained via linear regression.: "Re-align isotopes in all branches to establish optimal match to the khipu grid. Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression."
- [readme] Some ions may come into the initial network by mistakes or unresolved signals and are removed from the established khipu, and sent off to form a new khipu.: "Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu."
