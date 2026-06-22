---
name: molecular-structure-alignment
description: Use when when you have two or more lipid structures represented as labeled molecular graphs and need to compute pairwise structural distances to cluster lipidomes, identify similar lipid species, or rank lipids by structural relatedness.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0364
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-alignment

## Summary

Align graph-based representations of molecular structures (particularly lipids) using graph isomorphism or subgraph matching to identify corresponding atoms, bonds, and functional groups. This enables computation of pairwise structural distance metrics that quantify dissimilarity between molecules and support comparative lipidomics analysis.

## When to use

When you have two or more lipid structures represented as labeled molecular graphs and need to compute pairwise structural distances to cluster lipidomes, identify similar lipid species, or rank lipids by structural relatedness. Particularly useful when comparing lipid species with different fatty acyl chain compositions or when sn-positions are unspecified and all permutations of chain comparisons must be evaluated.

## When NOT to use

- Input lipids lack sufficient structural annotation (atom types, bond orders, or functional groups cannot be reliably encoded as labeled graphs)
- Only abundance comparisons are needed without structural similarity assessment
- Molecular structures are not lipids or cannot be meaningfully represented as connected graphs

## Inputs

- Lipid structure representations (labeled molecular graphs with atom types, bond orders, and functional group annotations)
- Lipid nomenclature strings or structure objects encoding connectivity and chain composition

## Outputs

- Pairwise structural distance scores (normalized scalar values, typically 0–1 range for bounded metrics)
- Graph alignment information (corresponding atom and bond mappings between paired structures)

## How to apply

Parse each input lipid structure as a labeled graph encoding atom connectivity and functional group types. Align the two graph structures using graph isomorphism or subgraph matching to establish correspondence between atoms and bonds across the pair. Compute a structural distance metric from the alignment that accounts for differences in atom types, bond orders, and functional group composition. By default, use a bounded distance metric (range 0–1, where 0 indicates identical structures) unless unbound distance metrics are activated for higher accuracy at the cost of reduced lipidome visibility. When sn-positions are not specified (e.g., 'PC 18:0_16:1'), optionally activate all-combinations comparison mode to evaluate all permutations of fatty acyl chain pairings and select the lowest distance, improving accuracy but reducing computational performance.

## Related tools

- **LipidSpace** (Implements graph-based lipid structure comparison and pairwise distance computation; orchestrates alignment and distance metric calculation for comparative lipidomics analysis) — https://github.com/lifs-tools/lipidspace
- **cppGoslin** (Parses and represents lipid nomenclature as structured molecular objects with atom and functional group information; provides substrate for graph construction)

## Evaluation signals

- Distance scores fall within expected range (0–1 for bounded metrics, or ≥0 for unbound metrics) and are symmetric: distance(A,B) = distance(B,A)
- Identical lipid structures return distance = 0; structurally dissimilar lipids return distance closer to 1 (bounded) or higher values (unbound)
- When sn-positions are specified, first FA of lipid A aligns with first FA of lipid B and second with second; when unspecified and all-combinations mode is active, the lowest pairwise distance among all permutations is returned
- Graph alignments preserve chemical validity: atom types and bond orders are conserved in the correspondence mapping
- Distance-based clustering or dendrograms produce biologically interpretable lipidome groupings (e.g., similar lipid classes or sample types cluster together)

## Limitations

- Graph-based alignment does not account for three-dimensional stereochemistry or conformational dynamics; treats structures as 2D connectivity graphs
- Performance degrades significantly when sn-position mode is deactivated to evaluate all fatty acyl chain permutations, particularly for lipids with >2 chains
- Bounded distance metrics (0–1) limit visibility of very large structural differences in high-dimensional lipid space visualizations; unbound metrics improve accuracy but reduce interpretability
- Alignment accuracy depends on the quality and completeness of structural annotation; missing or incorrect bond orders or atom type assignments propagate to distance calculations
- LipidSpace does not currently support persistent storage or loading of completed analyses, requiring re-computation of alignments and distances for subsequent sessions

## Evidence

- [other] Parse and represent each input lipid structure as a labeled graph encoding atom connectivity and functional groups. Align the two graph structures using graph isomorphism or subgraph matching to identify corresponding atoms and bonds. Compute a structural distance metric based on the graph alignment, accounting for differences in atom types, bond orders, and functional group composition.: "Parse and represent each input lipid structure as a labeled graph encoding atom connectivity and functional groups. Align the two graph structures using graph isomorphism or subgraph matching to"
- [readme] A graph-based comparison of lipid structures allows to calculate distances between lipids and to determine similarities across lipidomes.: "A graph-based comparison of lipid structures allows to calculate distances between lipids and to determine similarities across lipidomes."
- [readme] In default mode, LipidSpace is comparing the first fatty acyl chain (FA) of the first lipid with the first FA of the second lipid, the second FA of the first lipid with the second FA of the second lipid, etc. However, when the sn-position is not specified as for instance in PC 18:0_16:1, a mode can be activated to compare all combinations of FA comparisons for both lipids and picking the lowest distance.: "when the sn-position is not specified as for instance in PC 18:0_16:1, a mode can be activated to compare all combinations of FA comparisons for both lipids and picking the lowest distance."
- [readme] As default, LipidSpace is using a bound distance metric to compare the structure of any two lipids. That means that the distance is a value that ranges between 0 (both lipids are identical) and 1. However, other distance measures suggest an unbound distance ranging from 0 to infinity. This mode provides more accurate results but reduces the visibility of the lipid spaces since the distances may become very big.: "LipidSpace is using a bound distance metric to compare the structure of any two lipids. That means that the distance is a value that ranges between 0 (both lipids are identical) and 1. However, other"
- [other] Return the pairwise distance score as a normalized scalar value (0–1 or similar range) indicating structural dissimilarity.: "Return the pairwise distance score as a normalized scalar value (0–1 or similar range) indicating structural dissimilarity."
