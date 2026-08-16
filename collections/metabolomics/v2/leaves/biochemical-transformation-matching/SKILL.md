---
name: biochemical-transformation-matching
description: Use when after you have detected and assigned molecular formulas to peaks
  in a single FT-ICR MS sample, and you want to infer which biochemical or abiotic
  reactions are occurring by examining pairwise mass differences.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3407
  tools:
  - MetaboDirect
  - Python (NumPy, pandas)
  - R (vegan package)
  - Cytoscape
  - KEGG database
  techniques:
  - direct-infusion-MS
  license_tier: open
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- Molecular transformation networks for each sample (mass difference network-based
  approach) are generated in this step
- The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1)
- The MetaboDirect pipeline was developed in Python 3.8 and requires the Python dependencies
  NumPy, pandas
- developed in Python 3.8 [38] and R 4.0.2 [39]
- Networks are then constructed using Cytoscape and colored based on their molecular
  class
- Networks are then constructed using Cytoscape [79] and colored based on their molecular
  class.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biochemical-transformation-matching

## Summary

Match observed mass differences between FT-ICR MS peaks against a reference library of biochemical transformations to construct transformation networks ab initio. This skill enables automated identification of metabolic and abiotic chemical conversions encoded in mass-difference patterns, with classification by transformation type and biotic/abiotic origin.

## When to use

Apply this skill after you have detected and assigned molecular formulas to peaks in a single FT-ICR MS sample, and you want to infer which biochemical or abiotic reactions are occurring by examining pairwise mass differences. Use it when your research goal is to reconstruct metabolic pathways, identify hub metabolites, or characterize the transformation landscape without chromatographic separation.

## When NOT to use

- Input peak list has not yet been assigned molecular formulas or has not undergone quality filtering (e.g. isotope removal, ppm-error thresholding) — pre-processing must occur first.
- You have only a single peak or fewer than three peaks in the sample — pairwise matching requires sufficient peak diversity to generate meaningful transformations.
- Your biochemical transformation reference key is not curated for the organism, environment, or reaction scope of your study — mismatched reference libraries will yield false positive or irrelevant transformations.

## Inputs

- Peak m/z list (CSV) with detected masses from a single FT-ICR MS sample
- Molecular formulas assigned to each peak (pre-processed output)
- Biochemical transformation reference key (mass difference ↔ transformation name/type)
- Sample molecular class assignments per peak

## Outputs

- Edge table (CSV): source m/z, target m/z, mass difference, transformation name, biotic/abiotic classification
- Node table (CSV): peak m/z values and molecular class assignments
- Network statistics (degree distribution, connected component count)
- Cytoscape-formatted edge and node files (.sif or .csv)

## How to apply

Compute all pairwise mass differences between detected m/z values in your sample using vectorized subtraction. For each mass difference, query a pre-defined biochemical transformation reference key (keyed by exact mass difference values) and retain matches where the observed mass difference falls within ±1 ppm error tolerance of a known transformation mass. Classify each retained transformation as biotic or abiotic according to the reference key metadata. Generate edge and node tables: edges list source peak m/z, target peak m/z, observed mass difference, transformation name, and classification; nodes list all peaks and their molecular class assignments. Export for network visualization in Cytoscape and compute network statistics (degree distribution, component count) to identify highly connected hub metabolites and dominant transformation types.

## Related tools

- **MetaboDirect** (Command-line pipeline implementing transformation matching, network generation, and Cytoscape export; orchestrates mass difference vectorization, ±1 ppm matching, and biotic/abiotic classification) — https://github.com/Coayala/MetaboDirect
- **Python (NumPy, pandas)** (Vectorized mass difference computation; all-pairs subtraction and DataFrame manipulation for match filtering)
- **Cytoscape** (Network visualization and exploration of edges/nodes; computation of degree distribution and connected components)
- **KEGG database** (Reference source for biochemical transformations (mass differences) and reaction annotations)

## Examples

```
metabodirect --input sample_peaks.csv --transformation-key biochemical_transformations.db --ppm-tolerance 1 --output-prefix sample_network
```

## Evaluation signals

- Edge table contains no duplicate (source, target, transformation) tuples; each edge represents a unique transformation instance.
- All retained mass differences fall within ±1 ppm of their reference transformation value; verify by computing (observed_diff − reference_diff) / reference_diff × 1e6 ≤ ±1.
- Every edge references a transformation name and classification (biotic or abiotic) present in the reference key; no unmatched or orphaned edges.
- Node table includes all peaks from the input m/z list with no missing molecular class assignments.
- Network statistics (e.g., degree distribution) are non-trivial: hub metabolites (high-degree nodes) can be identified; component count ≥ 1 and ≤ number of unique peaks.

## Limitations

- Cannot distinguish chemical isomers: FT-ICR MS alone cannot differentiate isomers with identical m/z; mass difference matching treats all matches as equivalent.
- Ion suppression and signal enhancement can cause missing or artificially weak peaks, leading to incomplete transformation networks and underestimation of true reaction connectivity.
- Reference transformation key completeness and accuracy directly determine output quality; incomplete or misannotated keys introduce false negatives (missed transformations) and false positives (spurious matches).
- The ±1 ppm tolerance is instrument-specific to FT-ICR MS ultra-high mass accuracy; application to lower-resolution instruments may require relaxed tolerance and yield ambiguous matches.
- Single-sample analysis per execution; no cross-sample integration of transformations unless multiple samples are run separately and results are merged post-hoc.

## Evidence

- [other] MetaboDirect generates molecular transformation networks by identifying mass differences between detected masses in a sample, using the ultra-high mass accuracy of FT-ICR MS to recognize chemically transformed species; nodes represent masses and edges represent the mass differences corresponding to specific biochemical transformations.: "MetaboDirect generates molecular transformation networks by identifying mass differences between detected masses in a sample, using the ultra-high mass accuracy of FT-ICR MS to recognize chemically"
- [other] Compute all pairwise mass differences between peaks using vectorized subtraction. Match each mass difference against the pre-defined biochemical transformation key, retaining matches with ≤1 ppm error tolerance.: "Compute all pairwise mass differences between peaks using vectorized subtraction. 3. Match each mass difference against the pre-defined biochemical transformation key, retaining matches with ≤1 ppm"
- [other] Classify retained transformations as biotic or abiotic according to the reference key. Generate edge table (CSV) listing source peak m/z, target peak m/z, mass difference, transformation name, and classification.: "Classify retained transformations as biotic or abiotic according to the reference key. 5. Generate edge table (CSV) listing source peak m/z, target peak m/z, mass difference, transformation name, and"
- [abstract] MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences: "MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences"
- [intro] Even though DI-MS has ample coverage and can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin), some drawbacks are its inability to separate chemical isomers, lack of fine resolving power: "Even though DI-MS has ample coverage and can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin), some drawbacks are its inability to separate chemical isomers"
