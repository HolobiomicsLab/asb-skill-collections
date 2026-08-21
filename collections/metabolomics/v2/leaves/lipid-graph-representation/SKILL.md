---
name: lipid-graph-representation
description: Use when when you have multiple lipid structures (from lipidomics data
  in CSV, XLSX, or mzTab-M format) and need to compute pairwise structural distances,
  identify lipids responsible for shaping a lipidome, or perform hierarchical clustering
  of lipidomes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2422
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - LipidSpace
  - cppGoslin
  license_tier: open
  provenance_tier: literature
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

# lipid-graph-representation

## Summary

Represent lipid structures as labeled graphs encoding atom connectivity and functional groups, enabling graph-based structural comparison and distance computation across lipidomes. This representation underlies LipidSpace's ability to calculate pairwise lipid distances and identify lipidome similarities.

## When to use

When you have multiple lipid structures (from lipidomics data in CSV, XLSX, or mzTab-M format) and need to compute pairwise structural distances, identify lipids responsible for shaping a lipidome, or perform hierarchical clustering of lipidomes. Use this skill as the foundation before distance metric computation or dendrogram construction.

## When NOT to use

- Input data lacks structural information (only lipid names without atom/bond details provided by cppGoslin parsing)
- Lipid identifiers are non-standard or cannot be parsed by the underlying cppGoslin library
- Analysis requires only quantitative intensity comparisons without structural distance (use direct abundance clustering instead)

## Inputs

- Lipid structure identifiers (LIPID MAPS nomenclature, e.g., 'PC 18:0_16:1')
- Parsed lipidomes from CSV, XLSX, or mzTab-M import files
- Atom connectivity and functional group composition data

## Outputs

- Labeled graph representation of each lipid structure (nodes: atoms with types; edges: bonds with orders)
- Graph subcomponents (e.g., headgroup, fatty acyl chains)
- Ready-for-alignment graph pairs for distance computation

## How to apply

Parse each input lipid structure (e.g., 'PC 18:0_16:1', 'Cer 18:1;O2/16:0') into a labeled graph where nodes represent atoms with their types and bonds encode connectivity and bond orders. For multi-chain lipids, represent each fatty acyl chain and headgroup as subgraph components. Optionally normalize sn-position handling: by default, match the first fatty acyl chain of lipid A to the first chain of lipid B (positionally ordered); activate 'Ignore lipid sn-positions' mode to compare all pairwise chain combinations and select the lowest distance, trading accuracy for performance. The resulting graph representation serves as input to graph alignment (isomorphism or subgraph matching) and subsequent distance metric computation (normalized 0–1 by default, or unbounded 0–∞ if enabled).

## Related tools

- **LipidSpace** (GUI and REST framework for importing lipidomes, constructing graph representations, and computing structural distances; delegates graph parsing to cppGoslin) — https://github.com/lifs-tools/lipidspace
- **cppGoslin** (Core library for parsing LIPID MAPS nomenclature into structural components (atoms, bonds, functional groups) that form the basis of graph representation) — https://github.com/lifs-tools/cppgoslin

## Evaluation signals

- Graph parsing succeeds without errors for all lipids in the input lipidome (check cppGoslin library version and nomenclature compliance)
- Atom counts, bond types, and functional group identifiers match expected lipid class compositions (e.g., PC headgroup contains phosphocholine, fatty acyl chains have correct carbon/unsaturation counts)
- Graph isomorphism or subgraph matching produces symmetric distance matrices (distance from lipid A to B equals distance from B to A) when sn-position mode is consistent
- Pairwise distances fall in the expected range (0–1 for normalized, 0–∞ for unbounded) and show intuitive clustering (identical lipids have distance 0, structurally similar lipids have smaller distances than dissimilar pairs)
- Dendrogram and downstream analyses (PCA, feature analysis) show reasonable biological grouping and stable results across repeated runs with the same parameters

## Limitations

- Performance degrades when 'Ignore lipid sn-positions' mode is activated; combinatorial chain comparison grows quadratically with number of chains per lipid
- Nomenclature parsing depends on cppGoslin library version; non-standard or legacy LIPID MAPS names may fail to parse; ensure cppGoslin is up-to-date (mentioned in README as common build error source)
- Bounded distance metric (0–1) may obscure large structural differences; use unbounded mode for more accurate but less interpretable results
- Graph representation does not encode 3D stereochemistry or exact spatial conformations; comparisons are topological only

## Evidence

- [other] Parse and represent each input lipid structure as a labeled graph encoding atom connectivity and functional groups.: "Parse and represent each input lipid structure as a labeled graph encoding atom connectivity and functional groups."
- [readme] A graph-based comparison of lipid structures allows to calculate distances between lipids and to determine similarities across lipidomes.: "A graph-based comparison of lipid structures allows to calculate distances between lipids and to determine similarities across lipidomes."
- [readme] In default mode, LipidSpace is comparing the first fatty acyl chain (FA) of the first lipid with the first FA of the second lipid, the second FA of the first lipid with the second FA of the second lipid, etc.: "In default mode, LipidSpace is comparing the first fatty acyl chain (FA) of the first lipid with the first FA of the second lipid, the second FA of the first lipid with the second FA of the second"
- [readme] when the sn-position is not specified as for instance in PC 18:0_16:1, a mode can be activated to compare all combinations of FA comparisons for both lipids and picking the lowest distance.: "when the sn-position is not specified as for instance in PC 18:0_16:1, a mode can be activated to compare all combinations of FA comparisons for both lipids and picking the lowest distance."
- [readme] As default, LipidSpace is using a bound distance metric to compare the structure of any two lipids. That means that the distance is a value that ranges between 0 (both lipids are identical) and 1.: "As default, LipidSpace is using a bound distance metric to compare the structure of any two lipids. That means that the distance is a value that ranges between 0 (both lipids are identical) and 1."
