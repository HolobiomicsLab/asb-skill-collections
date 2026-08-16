---
name: graph-isomorphism-matching
description: Use when when comparing two or more lipid structures and you need to
  determine which atoms and bonds in one structure correspond to those in another,
  prior to computing a distance metric. Specifically, when input lipids have variable
  fatty acyl chain compositions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2941
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - LipidSpace
  - cppgoslin
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-isomorphism-matching

## Summary

Align two molecular structures represented as labeled graphs to identify corresponding atoms and bonds, enabling quantitative comparison of structural similarity. This is a foundational step in computing pairwise structural distances between lipids in lipidomics analysis.

## When to use

When comparing two or more lipid structures and you need to determine which atoms and bonds in one structure correspond to those in another, prior to computing a distance metric. Specifically, when input lipids have variable fatty acyl chain compositions (e.g., PC 18:0_16:1 without specified sn-position) and you want to explore all possible chain pairings to identify the lowest structural distance.

## When NOT to use

- Lipids where structural difference is only abundance-based (use intensity/quantification comparison instead)
- Pre-processed lipid distance matrices already computed (skip to downstream clustering or dimensionality reduction)
- Scenarios where all input lipids have fully-specified stereochemistry and chain positions, making exhaustive chain comparison unnecessary (use default positional mode)

## Inputs

- Two lipid structures represented as labeled molecular graphs (atoms with types, bonds with orders)
- Lipid nomenclature strings (e.g., 'PC 18:0_16:1', 'Cer 18:1;O2/16:0')
- Optional: Boolean flag indicating whether to ignore sn-positions and exhaustively compare all fatty acyl chain combinations

## Outputs

- Atom-to-atom correspondence mapping between the two graphs
- Bond-to-bond correspondence mapping between the two graphs
- List of aligned atom pairs with their types (for difference calculation)
- List of aligned bond pairs with their orders (for difference calculation)

## How to apply

Represent each input lipid structure as a labeled graph encoding atom types and bond connectivity, including functional groups. Apply graph isomorphism or subgraph matching algorithms to align the two graphs and identify atom-to-atom and bond-to-bond correspondences. When sn-positions are not specified, activate exhaustive comparison mode to test all combinations of fatty acyl chain alignments between the two lipids, selecting the pairing that yields the minimum distance. This mode provides more accurate results but with increased computational cost. The alignment output serves as input to the subsequent distance metric computation step.

## Related tools

- **LipidSpace** (Implements graph-based comparison of lipid structures using graph isomorphism/subgraph matching to compute structural distances for lipidome analysis) — https://github.com/lifs-tools/lipidspace
- **cppgoslin** (Parses lipid nomenclature strings and constructs graph representations of lipid structures used by LipidSpace) — https://github.com/lifs-tools/cppgoslin

## Evaluation signals

- Verify that all atoms in the smaller structure are matched to atoms in the larger structure (or subgraph coverage is maximal)
- Check that matched atom pairs have chemically plausible differences (e.g., atom type, valence, functional group assignment); flag impossible pairings (e.g., carbon matched to nitrogen without justification)
- Confirm that bond order differences are consistent with the aligned atom types (e.g., matched double bonds between matched sp2 carbons)
- In exhaustive mode, verify that the selected chain pairing produces the minimum distance among all tested combinations; document which pairing was chosen
- For lipids with specified sn-positions, confirm that chain order is preserved (first FA to first FA, second to second); verify deviations occur only when exhaustive mode is explicitly enabled

## Limitations

- Performance degrades significantly in exhaustive mode (all fatty acyl chain comparison combinations) for lipids with many chains; LipidSpace offers this as an optional mode to balance accuracy vs. speed
- Graph isomorphism/subgraph matching is NP-hard; practical algorithms may not guarantee the global optimum for very large or highly branched lipid structures
- Accuracy depends on correct parsing and graph representation of input lipid nomenclature; ambiguous or non-standard notation may produce incorrect alignments
- The README notes that sn-position comparison mode is available but reduced visibility of lipid spaces may occur with unbound distance metrics where distances range from 0 to infinity

## Evidence

- [other] Align the two graph structures using graph isomorphism or subgraph matching to identify corresponding atoms and bonds.: "Align the two graph structures using graph isomorphism or subgraph matching to identify corresponding atoms and bonds."
- [readme] A graph-based comparison of lipid structures allows to calculate distances between lipids and to determine similarities across lipidomes.: "A graph-based comparison of lipid structures allows to calculate distances between lipids and to determine similarities across lipidomes."
- [readme] When the sn-position is not specified as for instance in PC 18:0_16:1, a mode can be activated to compare all combinations of FA comparisons for both lipids and picking the lowest distance.: "When the sn-position is not specified as for instance in PC 18:0_16:1, a mode can be activated to compare all combinations of FA comparisons for both lipids and picking the lowest distance."
- [readme] The results are more accurate, but the performance is decreased. You can activate this mode in the menu → Analysis → Ignore lipid sn-positions.: "The results are more accurate, but the performance is decreased. You can activate this mode in the menu → Analysis → Ignore lipid sn-positions."
