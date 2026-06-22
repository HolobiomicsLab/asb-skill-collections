---
name: pairwise-mass-comparison-computation
description: Use when after peak m/z values and molecular formulas have been extracted and pre-processed from FT-ICR MS data, and you need to reconstruct biochemical transformation networks ab initio.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboDirect
  - Python (NumPy, pandas)
  - R (vegan package)
  - Cytoscape
  - NumPy
  - pandas
  - FT-ICR MS
  techniques:
  - mass-spectrometry
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

# pairwise-mass-comparison-computation

## Summary

Compute all pairwise mass differences between detected peaks in FT-ICR MS data to identify potential biochemical transformations. This vectorized subtraction yields a difference matrix that serves as input to transformation network reconstruction.

## When to use

After peak m/z values and molecular formulas have been extracted and pre-processed from FT-ICR MS data, and you need to reconstruct biochemical transformation networks ab initio. Apply this skill when you have a list of detected masses for a single sample and want to identify which pairs of masses correspond to known biochemical transformations (e.g., oxidation, methylation, dehydration).

## When NOT to use

- Input consists of already-processed transformation networks or pre-computed edge tables (redundant application).
- Peak list contains unresolved chemical isomers without mass differences as discriminators (FT-ICR MS cannot separate isomers, so mass differences alone may not be informative).
- Mass accuracy of the instrument is worse than ~2 ppm, making 1 ppm error tolerance too stringent to recover true transformations.

## Inputs

- Peak m/z list (CSV format with columns: m/z, molecular_formula, molecular_class)
- Pre-defined biochemical transformation reference key (mass difference → transformation name mapping with error tolerances)
- Single sample from pre-processed FT-ICR MS output

## Outputs

- Edge table (CSV): source peak m/z, target peak m/z, mass difference, transformation name, biotic/abiotic classification
- Pairwise mass difference matrix (n×n, where n = number of peaks)
- Matched transformation list with classification labels

## How to apply

Load the peak m/z list and assigned molecular formulas from the pre-processed CSV output for a single sample. Use vectorized subtraction (NumPy broadcasting) to compute all pairwise mass differences between detected peaks—this produces an n×n difference matrix where n is the number of peaks. Retain only mass differences that fall within ±1 ppm error tolerance when matched against a pre-defined biochemical transformation reference key. Match each retained difference to a transformation name and classification (biotic or abiotic) using the reference database. The rationale is that FT-ICR MS ultra-high mass accuracy (typically sub-ppm) makes mass differences a reliable proxy for specific chemical modifications; the 1 ppm tolerance accounts for measurement uncertainty while rejecting spurious matches.

## Related tools

- **NumPy** (Vectorized subtraction of m/z values to compute all pairwise mass differences efficiently)
- **pandas** (Load, store, and manipulate peak m/z lists and difference matrices as DataFrames)
- **MetaboDirect** (Command-line pipeline that orchestrates pairwise mass comparison as step 3 of transformation network analysis) — https://github.com/Coayala/MetaboDirect
- **FT-ICR MS** (Source instrument providing ultra-high mass accuracy (sub-ppm) that enables reliable mass difference matching)

## Evaluation signals

- Pairwise difference matrix is symmetric and has zeros on the diagonal (mathematical consistency).
- All retained mass differences fall within ±1 ppm of their assigned transformation in the reference key (error tolerance met).
- Edge table has no duplicate edges (same source–target pair listed only once per transformation type).
- Every matched transformation is present in the reference key with a biotic or abiotic label; no unclassified transformations leak through.
- Mass difference values in output edge table are consistent with known biochemical modifications (e.g., +15.99 for oxidation, +14.02 for methylation); spot-check a random sample against reference.

## Limitations

- Cannot distinguish chemical isomers, as FT-ICR MS lacks chromatographic separation; mass differences alone do not disambiguate isomeric pairs.
- Assumes reference transformation key is complete and error tolerances are calibrated for the specific instrument and sample matrix; miscalibrated tolerances will produce false positives or false negatives.
- Vectorized computation becomes memory-intensive for samples with very large peak counts (e.g., >10,000 peaks); consider subsampling or chunking for such cases.
- Does not account for ion suppression or enhancement effects, which can cause weak or missing peaks and thus incompletely sampled transformation networks.

## Evidence

- [methods] Compute all pairwise mass differences between peaks using vectorized subtraction.: "Compute all pairwise mass differences between peaks using vectorized subtraction."
- [methods] Match each mass difference against the pre-defined biochemical transformation key, retaining matches with ≤1 ppm error tolerance.: "Match each mass difference against the pre-defined biochemical transformation key, retaining matches with ≤1 ppm error tolerance."
- [other] MetaboDirect generates molecular transformation networks by identifying mass differences between detected masses in a sample, using the ultra-high mass accuracy of FT-ICR MS to recognize chemically transformed species: "MetaboDirect generates molecular transformation networks by identifying mass differences between detected masses in a sample, using the ultra-high mass accuracy of FT-ICR MS to recognize chemically"
- [other] nodes represent masses and edges represent the mass differences corresponding to specific biochemical transformations: "nodes represent masses and edges represent the mass differences corresponding to specific biochemical transformations"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: numpy, pandas: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: numpy, pandas"
