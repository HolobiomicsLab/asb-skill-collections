---
name: adduct-mass-matching-and-clustering
description: Use when after identifying statistically significant LC-MS features (e.g.
  via MB-VIP permutation testing) when you need to consolidate redundant measurements
  of the same metabolite arising from different ionisation adducts (e.g. [M+H]+, [M+Na]+,
  [M−H]−).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - MamsiStructSearch
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- import pandas as pd
- import numpy as np
- scipy
- 'Dependencies: scipy'
- from sklearn.model_selection import train_test_split
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01327
  all_source_dois:
  - 10.1021/acs.analchem.5c01327
  - 10.1371/journal.pcbi.1011814
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Adduct-Mass Matching and Clustering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill groups LC-MS features that share a common neutral mass by calculating hypothetical neutral masses from common electrospray ionisation adducts and matching them within a mass tolerance window. It is essential for linking multiply-charged or adducted ions of the same molecule into structural clusters.

## When to use

Apply this skill after identifying statistically significant LC-MS features (e.g. via MB-VIP permutation testing) when you need to consolidate redundant measurements of the same metabolite arising from different ionisation adducts (e.g. [M+H]+, [M+Na]+, [M−H]−). Use it as part of structural clustering when the input feature table contains m/z and retention time columns and you suspect multiple features represent isotopologues or adducts of the same compound.

## When NOT to use

- Input features are already annotated to specific chemical standards or databases — annotation takes precedence over de novo mass matching.
- LC-MS data were collected in atmospheric pressure chemical ionisation (APCI) or other non-ESI modes where common ESI adduct patterns do not apply.
- Features come from targeted (scheduled) LC-MS methods where ion identities are pre-specified by retention time and m/z windows.

## Inputs

- Feature table with columns: m/z, retention time (RT), assay identifier
- Mass tolerance threshold (ppm)
- List of common electrospray ionisation adducts and their mass shifts

## Outputs

- Adduct cluster assignments (feature→cluster_id mapping)
- Hypothetical neutral mass values for each cluster
- Merged structural clusters (combining adduct and isotopologue groups)

## How to apply

First, define a mass tolerance threshold (typically 15 ppm) appropriate to your instrument's mass accuracy. For each feature's observed m/z value, calculate hypothetical neutral masses by reversing common electrospray ionisation adduct mass shifts (e.g. subtract 1.00728 Da for [M+H]+, subtract 22.98922 Da for [M+Na]+, add 1.00728 Da for [M−H]−). Group features whose calculated neutral masses match within the ppm tolerance into adduct clusters. Merge these adduct clusters with any overlapping isotopologue clusters (identified separately by 1.00335 Da mass-difference searches) to form final structural clusters. This approach assumes accurate m/z calibration and benefits from prior retention time windowing to reduce false-positive mass matches across chemically unrelated compounds.

## Related tools

- **MamsiStructSearch** (Implements adduct mass matching by calculating hypothetical neutral masses from ESI adducts and clustering features with matching neutral masses) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Data manipulation and feature table handling)
- **scipy** (Mass tolerance calculations and clustering operations)
- **scikit-learn** (Optional hierarchical clustering for correlation-based cluster refinement)

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=15)
struct.load_lcms(selected_features)
struct.get_structural_clusters()
```

## Evaluation signals

- All features within an adduct cluster should have calculated neutral masses agreeing within the specified ppm tolerance (e.g. ±15 ppm)
- Features assigned to the same adduct cluster should have retention times within the defined RT window (default 5 seconds) to avoid spurious cross-compound matches
- Each structural cluster should contain at most one feature per assay unless the assay genuinely measures the same metabolite in different ionisation modes
- Merged adduct + isotopologue clusters should show expected mass differences (1.00335 Da for isotopologues; adduct-specific differences for [M+H]+/[M+Na]+/etc.)
- Cross-assay cluster links identified using [M+H]+/[M−H]− as references should have matching neutral masses across positive and negative mode assays

## Limitations

- Requires accurate m/z calibration; systematic mass drift can prevent correct matching, especially at tight ppm tolerances (< 10 ppm).
- Cannot distinguish between structural isomers or isobars with identical m/z and retention time; the method assumes one metabolite per neutral mass per RT window.
- Performance depends on prior retention time windowing and isotopologue/adduct discovery steps; overlapping clusters from different metabolites can cause false merges if RT windows are too broad.
- Limited to common ESI adducts; unusual or instrument-specific adducts (e.g. [M+K]+, [M+NH4]+) may not be included in the default adduct list.
- The framework was tested on metabolomics phenotyping data; applicability to other LC-MS data types (e.g. proteomics, lipidomics with non-standard ionisation) is not guaranteed.

## Evidence

- [readme] This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [readme] If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 ppm) then these features are grouped together.: "If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 ppm) then these features are grouped together."
- [readme] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [methods] Search for adduct signatures by calculating hypothetical neutral masses from common ESI adducts and matching within ppm tolerance; group features with matching neutral masses.: "Search for adduct signatures by calculating hypothetical neutral masses from common ESI adducts and matching within ppm tolerance; group features with matching neutral masses."
- [methods] Define retention time tolerance window (rt_win, default 5 seconds) and mass tolerance (ppm, default 15 ppm) for structural matching.: "Define retention time tolerance window (rt_win, default 5 seconds) and mass tolerance (ppm, default 15 ppm) for structural matching."
- [readme] Further, we search cross-assay clusters using [M+H]<sup>+</sup>/[M-H]<sup>-</sup> as link references.: "Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references."
