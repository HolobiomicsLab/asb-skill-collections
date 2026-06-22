---
name: ppm-tolerance-filtering-in-mass-spectrometry
description: Use when when you have assigned molecular formulas to m/z peaks or computed mass differences between peaks in FT-ICR MS data, and you need to distinguish true chemical matches from noise or random coincidences.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MetaboDirect
  - Python (NumPy, pandas)
  - R (vegan package)
  - Cytoscape
  - FT-ICR MS
  - KEGG database
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- Molecular transformation networks for each sample (mass difference network-based approach) are generated in this step
- The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1)
- The MetaboDirect pipeline was developed in Python 3.8 and requires the Python dependencies NumPy, pandas
- developed in Python 3.8 [38] and R 4.0.2 [39]
- Networks are then constructed using Cytoscape and colored based on their molecular class
- Networks are then constructed using Cytoscape [79] and colored based on their molecular class.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ppm-tolerance-filtering-in-mass-spectrometry

## Summary

Apply mass accuracy thresholds (parts per million tolerance) to validate molecular formula assignments and biochemical transformation matches in FT-ICR MS data. This skill filters spurious identifications and retains only high-confidence chemical entities and transformations based on ultra-high mass accuracy.

## When to use

When you have assigned molecular formulas to m/z peaks or computed mass differences between peaks in FT-ICR MS data, and you need to distinguish true chemical matches from noise or random coincidences. Use this skill after formula assignment but before network construction or statistical analysis, especially when matching mass differences against biochemical transformation databases where false positives could propagate downstream.

## When NOT to use

- Input is already pre-filtered or consensus-called (e.g., from commercial software with built-in tolerance); re-filtering may introduce unnecessary data loss or inconsistency.
- Mass spectrometry data is from lower-resolution instruments (e.g., quadrupole MS, TOF-MS with >5 ppm typical error); ppm tolerance filtering designed for FT-ICR MS accuracy may be too stringent or not appropriate for the instrument's capabilities.
- Formula assignments or transformation databases have not been vetted for the specific sample type or organism; applying ppm filtering without validating reference data may propagate systematic errors.

## Inputs

- Peak m/z list with assigned molecular formulas (CSV format)
- Pairwise mass differences between peaks (numeric array or table)
- Reference biochemical transformation key with theoretical mass differences
- User-specified ppm tolerance threshold (float, typically 0.5–1.0)

## Outputs

- Filtered edge table (CSV) listing source peak m/z, target peak m/z, mass difference, transformation name, and classification (biotic/abiotic)
- Filtered node table (CSV) with validated peaks and molecular class assignments
- Network statistics (degree distribution, component count) based on ppm-filtered edges

## How to apply

Define a ppm error tolerance threshold (MetaboDirect uses ≤1 ppm for biochemical transformation matching and ≤0.5 ppm for formula assignment error filtering). For each candidate match (e.g., mass difference vs. transformation mass, or observed m/z vs. theoretical formula mass), compute the absolute ppm error as |observed − theoretical| / theoretical × 10^6. Retain only matches meeting the tolerance threshold. This exploits FT-ICR MS's ultra-high mass accuracy to recognize chemically meaningful transformations while eliminating stochastic coincidences. Apply the same tolerance consistently across all samples in a comparison to ensure reproducibility and comparability of downstream network topology and statistical results.

## Related tools

- **MetaboDirect** (Command-line pipeline that implements ppm-tolerance filtering for formula assignment (0.5 ppm) and biochemical transformation matching (≤1 ppm error tolerance) during network construction.) — https://github.com/Coayala/MetaboDirect
- **FT-ICR MS** (Analytical instrument that provides the ultra-high mass accuracy (enabling sub-ppm error) on which ppm-tolerance thresholds are calibrated and applied.)
- **Cytoscape** (Network visualization and analysis platform that imports the ppm-filtered edge and node tables to render and explore validated biochemical transformation networks.)
- **Python (NumPy, pandas)** (Libraries used to vectorize pairwise mass difference calculations and filter matches against transformation keys using ppm tolerance comparisons.)
- **KEGG database** (Reference database of known biochemical transformations and their exact mass differences, against which observed mass differences are matched with ppm tolerance.)

## Examples

```
metabodirect --input sample_peaks.csv --ppm-tolerance 1.0 --transformation-db KEGG --output-edges filtered_transformations.csv --output-nodes filtered_peaks.csv
```

## Evaluation signals

- Retained transformations show mean ppm error ≤ threshold and no retained matches exceed the tolerance threshold.
- Edge count and network density metrics are reproducible when the same ppm threshold is applied to replicate samples.
- Filtered transformation networks contain only biologically plausible edges (e.g., known oxidations, dehydrations, methylations) with no anomalous mass differences.
- Comparison of networks before and after ppm filtering shows removal of isolated or low-degree nodes corresponding to spurious matches.
- Cross-validation: independently verified transformations (e.g., measured standards, literature) are retained; known false positives are excluded.

## Limitations

- Ultra-high mass accuracy is specific to FT-ICR MS; results are not transferable to lower-resolution instruments without recalibration of thresholds.
- ppm tolerance filtering cannot resolve chemical isomers or distinguish isobaric compounds; false negatives may occur when multiple valid formulas fall within the same ppm window.
- Matching against incomplete or organism-specific transformation databases may introduce systematic bias—transformations not in the database are never matched, regardless of ppm accuracy.
- Ion suppression or enhancement can distort measured m/z values and inflate ppm errors for co-eluting peaks; pre-filtering of low-intensity or artifact peaks is prerequisite.
- Threshold selection (e.g., 0.5 vs. 1.0 ppm) is heuristic and instrument-dependent; no universal threshold is specified for all sample types or metabolite classes.

## Evidence

- [other] Match each mass difference against the pre-defined biochemical transformation key, retaining matches with ≤1 ppm error tolerance.: "Match each mass difference against the pre-defined biochemical transformation key, retaining matches with ≤1 ppm error tolerance."
- [methods] Filter by error in formula assignment (0.5 ppm): "Filter by error in formula assignment (0.5 ppm)"
- [intro] FT-ICR MS has evolved during the past two decades into a powerful tool to study the molecular composition of small-molecule organic complex mixtures: "FT-ICR MS has evolved during the past two decades into a powerful tool to study the molecular composition of small-molecule organic complex mixtures"
- [intro] high-resolution mass spectrometry (HR-MS) in the last 20 years have allowed for high-precision formula: "advances in analytical mass spectrometry techniques and in particular the introduction of high-resolution mass spectrometry (HR-MS) in the last 20 years have allowed for high-precision formula"
- [other] the ultra-high mass accuracy of FT-ICR MS to recognize chemically transformed species: "using the ultra-high mass accuracy of FT-ICR MS to recognize chemically transformed species"
