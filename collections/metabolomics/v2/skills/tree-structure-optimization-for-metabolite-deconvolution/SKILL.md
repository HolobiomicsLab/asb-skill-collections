---
name: tree-structure-optimization-for-metabolite-deconvolution
description: Use when you have a connected subnetwork of LC-MS features that matched
  isotope or adduct patterns, and you need to establish a canonical tree representation
  with a single neutral mass assignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - networkx
  - treelib
  - mass2chem
  - metDataModel
  - Python 3
  - khipu
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.2c05810
  title: khipu
evidence_spans:
- The graph operations are supported by the networkx library
- tree visualization aided by the treelib library
- Khipu uses our package mass2chem for search functions
- The data model of “empirical compound” is described in the metDataModel package.
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

# tree-structure-optimization-for-metabolite-deconvolution

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Converts feature-pair networks into optimized tree structures representing empirical compounds by separating isotope and adduct edges, establishing an adduct trunk with a root path, and inferring neutral mass via linear regression against a theoretical khipu grid. This skill removes redundant nodes and resolves ambiguous ion relationships in LC-MS feature tables.

## When to use

Apply this skill when you have a connected subnetwork of LC-MS features that matched isotope or adduct patterns, and you need to establish a canonical tree representation with a single neutral mass assignment. Specifically: after pattern matching has identified m/z relationships within a feature group, before exporting pre-annotated empirical compounds for downstream metabolite identification.

## When NOT to use

- Input is already a curated list of known metabolites with verified neutral masses—tree optimization is for degenerate ion annotation, not metabolite identification.
- Subnetwork contains fewer than 2 connected features—a single feature or isolated pairs do not warrant tree structure optimization.
- Feature table lacks m/z precision better than ±100 ppm or retention time consistency—linear regression neutral mass inference requires mass accuracy ≤ 5–10 ppm and coherent chromatographic clustering.

## Inputs

- connected subnetwork of features (nodes with m/z, retention time, intensity; edges indicating isotope or adduct mass differences)
- feature table (TSV or similar format with columns: feature_id, m/z, rtime, intensity values)
- theoretical khipu grid (matrix of neutral mass + adduct m/z deltas and isotope offsets)

## Outputs

- optimized khipu tree instance (empirical compound object with root node, adduct trunk, isotopic branches, and neutral mass assignment)
- JSON annotation file (per-feature adduct/isotope assignment and neutral mass)
- tab-delimited empirical compounds table (empirical_compound_id, neutral_mass, representative_m/z, adduct_type, assigned_features)

## How to apply

Starting from a connected subnetwork of pattern-matched features, (1) inspect the subnetwork and remove redundant nodes (features that do not improve node explanation). (2) Separate isotope edges from adduct edges to identify isotopic branches (groups of connected isotope edges sharing an adduct type) and potential adduct variants. (3) Build a trunk of adducts by enumerating candidate root nodes and paths that maximize the number of features explained, using linear regression to infer neutral mass from available ions and the theoretical khipu grid (e.g., m/z differences for [M+H]+, [M+NH4]+, [M+Na]+, [M+K]+, [M+ACN+H]+ and their 13C isotopologs). (4) Assign each isotopic branch to the optimal adduct trunk node and re-align isotopic offsets to khipu grid positions. (5) Suppress or fork features that remain unexplained after optimal assignment—these become new khipu instances. The optimization criterion is maximizing the count of nodes consistent with theoretical adduct and isotope masses, weighted by feature intensity or SNR when available.

## Related tools

- **networkx** (graph operations for subnetwork construction and partitioning from pattern-matched feature pairs)
- **treelib** (tree structure representation and plain-text visualization of optimized khipu instances)
- **mass2chem** (search functions and theoretical mass calculations for adduct and isotope grid) — https://github.com/shuzhao-li-lab/mass2chem
- **metDataModel** (data model definition for empirical compound objects and output serialization) — https://github.com/shuzhao-li-lab/metDataModel
- **khipu** (main Python package implementing Weavor and Khipu classes for tree optimization algorithm) — https://github.com/shuzhao-li/khipu

## Examples

```
khipu -i ecoli_pos.tsv -o ecoli_preannotation
```

## Evaluation signals

- All nodes in the optimized tree are within ±5–10 ppm of theoretical m/z values predicted from the neutral mass, selected adduct, and isotope offset.
- Linear regression fit for neutral mass inference (R² > 0.95 or residual std. dev. < 2 ppm) indicates strong coherence of ion assignments.
- Redundant nodes have been removed: no feature remains in the tree that would be redundantly explained by another feature with the same neutral mass and adduct type.
- Isotope and adduct edges are correctly segregated: isotope edges form closed cycles within adduct branches; adduct edges connect the trunk.
- Output JSON and TSV files are valid, contain matching neutral mass and empirical_compound_id for all assigned features, and match the source feature table row count with zero missing assignments.

## Limitations

- Linear regression neutral mass inference assumes all observed ions belong to the same neutral compound—co-eluting isobars or unresolved isomers can produce biased neutral mass estimates.
- Tree optimization uses greedy node explanation maximization, which may fail if the feature network is highly ambiguous (e.g., many plausible adduct assignments at similar m/z differences); user may need to supply custom isotope/adduct patterns or constraints.
- Some ions may enter the initial network by mistakes or unresolved signals and are removed from the established khipu—these are forked into separate khipu instances, potentially fragmenting true empirical compounds across multiple trees if retention time clustering is poor.
- Algorithm performance degrades with low mass precision (>10 ppm tolerance required) or when feature SNR is not available; yeast demo dataset was pre-filtered by SNR > 100 to serve as cleaner reference.

## Evidence

- [readme] Each subnetwork becomes a khipu instance; subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure: "Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure"
- [readme] Separate isotope edges and adduct edges; establish a trunk of adducts with root and path by optimizing node explanation: "Separate isotope edges and adduct edges. The isotope edges form their own groups by shared nodes, each group belong to one adduct type. Establish a "trunk" of adducts with a root and a path for"
- [readme] Neutral mass inferred via linear regression based on available ions and theoretical khipu grid: "Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression."
- [readme] Ions from mistakes or unresolved signals are removed from established khipu and sent off to form new khipu: "Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu"
- [intro] Running khipu command-line tool produces JSON file and tab-delimited empirical compounds file: "Running the khipu command-line tool produces two output files: a JSON file and a tab-delimited file containing annotated empirical compounds."
