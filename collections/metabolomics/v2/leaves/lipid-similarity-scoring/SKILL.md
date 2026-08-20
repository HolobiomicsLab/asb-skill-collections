---
name: lipid-similarity-scoring
description: Use when you have two or more lipid structures (represented as molecular
  graphs or parsed lipid names) and need to quantify their structural dissimilarity
  for dendrogram construction, lipidome clustering, or identification of structurally
  similar lipids.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1812
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - LipidSpace
  - cppGoslin
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

# lipid-similarity-scoring

## Summary

Compute pairwise structural distance scores between lipid molecules using graph-based comparison of their atomic connectivity and functional group composition. This skill enables quantitative assessment of lipid structural similarity for lipidomic profiling, clustering, and comparative analysis.

## When to use

Apply this skill when you have two or more lipid structures (represented as molecular graphs or parsed lipid names) and need to quantify their structural dissimilarity for dendrogram construction, lipidome clustering, or identification of structurally similar lipids. Trigger conditions include: analyzing multiple lipid species across samples, performing hierarchical clustering of lipidomes, or selecting structurally representative lipids from a lipidomic dataset.

## When NOT to use

- Input is already a pre-computed distance matrix or dissimilarity table — skip this skill and proceed directly to clustering.
- Lipid structures lack functional group or stereochemical annotation — graph representation cannot faithfully capture structure; consider enriching data first.
- Analysis goal is quantitative abundance comparison rather than structural similarity — use abundance-based metrics (e.g., intensity ratios) instead.

## Inputs

- Lipid molecular graphs (atom connectivity and functional group labels)
- Parsed lipid structure names or SMILES representations
- Pairs of lipid structures from a lipidomic dataset

## Outputs

- Pairwise lipid distance scores (bounded 0–1 or unbounded 0–∞)
- Normalized structural dissimilarity scalar per lipid pair
- Distance matrix for hierarchical clustering and dendrogram construction

## How to apply

Parse each input lipid structure into a labeled molecular graph encoding atom types, bond orders, and functional group positions. Align the two graph structures using graph isomorphism or subgraph matching to establish atom-to-atom correspondence. Compute a distance metric from the alignment that accounts for differences in atomic composition and bond topology. By default, LipidSpace returns a bounded distance (0–1 range, where 0 indicates identical structures and 1 indicates maximum dissimilarity); optionally use an unbounded metric (0 to infinity) for higher accuracy when lipid spaces need not be visualized. When sn-positions are unspecified (e.g., 'PC 18:0_16:1'), activate combinatorial fatty acyl chain comparison to test all chain pairings and select the lowest distance. Apply the chosen linkage strategy (single, average, or complete) to aggregate pairwise distances into a dendrogram.

## Related tools

- **LipidSpace** (Primary tool implementing graph-based lipid structure comparison and distance scoring; handles data import (CSV, XLSX, mzTab-M), graph alignment, distance computation, and dendrogram visualization.) — https://github.com/lifs-tools/lipidspace
- **cppGoslin** (Dependency for lipid structure parsing and graph representation; enables standardized conversion of lipid names to molecular graphs.) — https://github.com/lifs-tools/cppgoslin

## Evaluation signals

- Verify distance scores fall within expected range (0–1 for bounded metric, 0–∞ for unbounded) with no NaN or Inf values.
- Confirm distance matrix is symmetric (d[i,j] == d[j,i]) and has zero diagonal (d[i,i] == 0).
- Check that identical lipid structures yield distance = 0 and structurally distinct lipids yield distance > 0.
- Validate dendrogram topology: structurally similar lipids cluster together; branching order reflects increasing distance thresholds.
- When sn-positions are ignored, confirm that alternative fatty acyl chain pairings were tested and lowest distance was selected.

## Limitations

- Graph isomorphism matching is computationally expensive for large lipidomes; combinatorial fatty acyl chain comparison further reduces performance when sn-positions are unspecified. NVIDIA CUDA acceleration is available in LipidSpaceRest for Hausdorff distance calculation on L4 GPUs.
- Bounded distance metric (0–1) limits visibility when lipid structural differences are very large; unbounded metric improves accuracy but sacrifices visual interpretability.
- Stereochemical information (e.g., sn-positions, E/Z configuration) is not fully leveraged unless explicitly specified in input lipid names; ambiguous or incomplete annotations may yield unreliable scores.
- Graph-based comparison does not account for 3D spatial conformation or pharmacological/biological activity; structurally similar lipids may have different physiological roles.
- Performance is not benchmarked against other lipid similarity metrics (e.g., Tanimoto fingerprints, Hausdorff distance variants); no published validation against experimental lipid function data.

## Evidence

- [readme] A graph-based comparison of lipid structures allows to calculate distances between lipids and to determine similarities across lipidomes: "A graph-based comparison of lipid structures allows to calculate distances between lipids and to determine similarities across lipidomes"
- [other] Parse and represent each input lipid structure as a labeled graph encoding atom connectivity and functional groups: "Parse and represent each input lipid structure as a labeled graph encoding atom connectivity and functional groups"
- [other] Align the two graph structures using graph isomorphism or subgraph matching to identify corresponding atoms and bonds: "Align the two graph structures using graph isomorphism or subgraph matching to identify corresponding atoms and bonds"
- [other] Compute a structural distance metric based on the graph alignment, accounting for differences in atom types, bond orders, and functional group composition: "Compute a structural distance metric based on the graph alignment, accounting for differences in atom types, bond orders, and functional group composition"
- [other] Return the pairwise distance score as a normalized scalar value (0–1 or similar range) indicating structural dissimilarity: "Return the pairwise distance score as a normalized scalar value (0–1 or similar range) indicating structural dissimilarity"
- [readme] As default, LipidSpace is using a bound distance metric to compare the structure of any two lipids. That means that the distance is a value that ranges between 0 (both lipids are identical) and 1.: "As default, LipidSpace is using a bound distance metric to compare the structure of any two lipids. That means that the distance is a value that ranges between 0 (both lipids are identical) and 1."
- [readme] In default mode, LipidSpace is comparing the first fatty acyl chain (FA) of the first lipid with the first FA of the second lipid, the second FA of the first lipid with the second FA of the second lipid, etc. However, when the sn-position is not specified as for instance in PC 18:0_16:1, a mode can be activated to compare all combinations of FA comparisons for both lipids and picking the lowest distance.: "In default mode, LipidSpace is comparing the first fatty acyl chain (FA) of the first lipid with the first FA of the second lipid, the second FA of the first lipid with the second FA of the second"
- [readme] Other distance measures suggest an unbound distance ranging from 0 to infinity. This mode provides more accurate results but reduces the visibility of the lipid spaces since the distances may become very big.: "Other distance measures suggest an unbound distance ranging from 0 to infinity. This mode provides more accurate results but reduces the visibility of the lipid spaces since the distances may become"
- [readme] The user can switch between single linkage, unweighted average, and complete linkage clustering in the menu → Analysis → Clustering strategy.: "The user can switch between single linkage, unweighted average, and complete linkage clustering in the menu → Analysis → Clustering strategy."
- [readme] Optionally, you can build LipidSpaceRest with NVIDIA CUDA Support to accelerate the Hausdorff distance calculation: "Optionally, you can build LipidSpaceRest with NVIDIA CUDA Support to accelerate the Hausdorff distance calculation"
