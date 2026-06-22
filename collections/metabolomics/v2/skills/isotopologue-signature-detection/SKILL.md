---
name: isotopologue-signature-detection
description: Use when you have preprocessed, statistically significant LC-MS features (from multiple assays or a single assay) and need to group features that represent the same metabolite in different isotopic labeling states.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - MamsiStructSearch
  - MAMSI (MamsiStructSearch)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotopologue-signature-detection

## Summary

Identifies isotopologue signatures within retention-time windows of LC-MS features by detecting characteristic mass differences (1.00335 Da, corresponding to ¹³C–¹²C) between feature m/z values. This is a foundational step in structural clustering that groups features likely derived from the same compound across different isotopic states.

## When to use

Apply this skill when you have preprocessed, statistically significant LC-MS features (from multiple assays or a single assay) and need to group features that represent the same metabolite in different isotopic labeling states. Trigger: you have an annotated feature table with m/z and retention time columns, and you want to reduce structural redundancy before downstream metabolite annotation or pathway analysis.

## When NOT to use

- Input features are already taxonomically labeled or have curated metabolite annotations; isotopologue detection is most useful before manual or database-driven annotation to avoid redundant labeling.
- Feature RT precision is poor (±> 1 sec per feature) or RT calibration is uncorrected, leading to systematic drift that will fragment true isotopologue pairs across RT windows.
- Analysis focuses on targeted/quantitative assays with known isotope labels already encoded in sample preparation; the method is designed for untargeted discovery where isotopologue status is unknown a priori.

## Inputs

- Preprocessed LC-MS feature intensity table (rows = samples, columns = features with naming format AssayName_RTsec_m/zValue)
- Feature metadata: m/z (mass-to-charge ratio), RT (retention time in seconds), assay identifier
- Retention time tolerance window parameter (rt_win, default 5 seconds)
- Mass tolerance for structural matching (ppm, default 15 ppm, though primarily used for adduct matching)

## Outputs

- Isotopologue cluster assignments (feature → cluster ID mapping)
- Cluster composition table (cluster ID, member features, cluster size)
- Annotated feature table with isotopologue cluster membership column
- Merged structural clusters (combination of isotopologue + adduct clusters)

## How to apply

Load the selected LC-MS features into MamsiStructSearch and invoke the isotopologue search as part of the structural clustering workflow. The method partitions features into retention time windows (default 5 seconds); within each window, it exhaustively compares all pairwise m/z differences and flags pairs where the difference equals 1.00335 Da (the monoisotopic mass shift for one ¹³C substitution). Features meeting this criterion are grouped into isotopologue clusters. The choice of RT window width (rt_win parameter) balances sensitivity—smaller windows (e.g., 2–3 sec) reduce false positives from co-eluting unrelated compounds, while larger windows (e.g., 10 sec) capture features with slight RT drift due to column effects. After isotopologue clusters are identified, they are merged with adduct clusters (found via neutral mass matching) to form final structural clusters. The output is an annotated feature table with isotopologue cluster membership.

## Related tools

- **MamsiStructSearch** (Core class for loading LC-MS features and executing isotopologue signature search within retention time windows as a sub-step of structural clustering) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Feature table manipulation and metadata extraction (m/z, RT columns))
- **numpy** (Vectorized pairwise m/z difference computation and filtering)
- **scipy** (Clustering algorithms (hierarchical linkage) for merging isotopologue clusters)

## Examples

```
from mamsi.mamsi_struct_search import MamsiStructSearch
struct = MamsiStructSearch(rt_win=5, ppm=15)
struct.load_lcms(selected_features)
struct.get_structural_clusters()
```

## Evaluation signals

- All isotopologue cluster members have m/z differences equal to 1.00335 ± tolerance (typically ≤0.01 Da at high resolution); no spurious mass pairs appear.
- Cluster members co-elute within the specified RT window (e.g., max RT spread ≤ 5 seconds); no clusters span multiple widely-separated RT regions.
- Cluster size distribution is reasonable (most clusters 2–4 members for typical natural abundance ¹³C patterns; larger clusters indicate potential adduct or correlation artifacts).
- Feature coverage in isotopologue clusters is low to moderate (typically 5–20% of significant features); excessive clustering suggests rt_win or mass tolerance is too permissive.
- Downstream merged structural clusters (isotopologue + adduct) show distinct patterns in correlation analyses or network visualizations; isotopologue membership improves feature grouping interpretability.

## Limitations

- Detection sensitivity depends on feature m/z resolution and accuracy; low-resolution or uncalibrated mass spectra will miss true isotopologues or produce false positives. The method assumes ≤ ±15 ppm mass accuracy for reliable matching.
- RT window choice is critical but not data-adaptive; systematic RT drift or poor chromatographic resolution can scatter true isotopologue pairs across windows. Users must verify rt_win empirically (e.g., by visualizing feature distributions).
- Handles only single ¹³C substitutions (mass diff = 1.00335 Da); multi-labeled isotopologues (²H, ¹⁵N, ¹⁸O, or multiple ¹³C) are not detected and would be treated as separate features or merged with unrelated adducts.
- Cannot distinguish true isotopologues from accidental mass matches (e.g., [M+H]⁺ of one compound matching [M]⁺ of another). Requires downstream validation via adduct-based clustering or correlation analysis.
- The framework was tested on metabolomics phenotyping data; applicability to other LC-MS data types (proteomics, lipidomics with different ionization modes) is not fully characterized.

## Evidence

- [methods] each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da between mass-to-charge ratios (m/z) of the features: "each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 *Da* between mass-to-charge ratios (*m/z*) of the features"
- [readme] features are split into retention time (RT) windows of 5 seconds intervals: "all features are split into retention time (*RT*) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures"
- [methods] Overlapping adduct and isotopologue clusters are merged to form structural clusters: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [methods] Load preprocessing data using load_lcms() with column naming convention: "Load the selected LC-MS feature intensity data into MamsiStructSearch using load_lcms() with column naming convention (AssayName)_(RTsec)_(m/z)m/z"
- [intro] MAMSI links statistically significant features into clusters defined by structural properties based on m/z and RT: "the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters"
- [intro] the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data: "the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data"
