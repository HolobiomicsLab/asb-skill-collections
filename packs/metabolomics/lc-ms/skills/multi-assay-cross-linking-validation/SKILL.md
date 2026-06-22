---
name: multi-assay-cross-linking-validation
description: Use when you have statistically significant features from multiple LC-MS assays with different ionization modes (e.g., positive and negative ESI) and need to collapse redundant feature representations into single structural entities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - MamsiStructSearch
  - networkx
  - peakPantheR
  techniques:
  - LC-MS
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

# Multi-Assay Cross-Linking Validation

## Summary

Validate and link structurally equivalent features across multiple LC-MS assays by searching for canonical adduct pairs ([M+H]+/[M-H]−) that represent the same neutral mass, enabling integration of complementary ionization modes. This skill consolidates multi-assay metabolomics data into unified structural clusters by resolving ionization-mode-specific fragmentation patterns.

## When to use

You have statistically significant features from multiple LC-MS assays with different ionization modes (e.g., positive and negative ESI) and need to collapse redundant feature representations into single structural entities. Apply this skill when you observe features with different m/z values and assay sources but suspect they derive from the same metabolite under different ionization conditions.

## When NOT to use

- Input features are from a single LC-MS assay or ionization mode (cross-linking requires at least two complementary modes).
- Retention time values are missing or unreliable—cross-assay matching depends on RT colocalization within the defined window.
- The metabolite set is dominated by non-canonical adducts or in-source fragments that do not follow standard ESI ionization patterns.

## Inputs

- Feature table with columns: (AssayName)_(RTsec)_(m/z)m/z format
- Pre-computed isotopologue clusters (mass differences 1.00335 Da within RT windows)
- Pre-computed adduct clusters (hypothetical neutral masses matched within ppm tolerance)
- List of statistically significant features (m/z, RT, assay membership)

## Outputs

- Merged structural clusters with cross-assay feature linkages
- Annotated feature table with cluster membership and linkage type (adduct, isotopologue, or cross-assay)
- Network representation of structural relationships including cross-assay edges

## How to apply

After grouping features within retention time windows (default 5 seconds) and identifying isotopologue and adduct clusters separately, search for cross-assay links using [M+H]+/[M-H]− as reference adducts. For each feature in a positive-mode assay (e.g., HPOS), calculate its hypothetical deprotonated form [M−H]− (subtract 1.007825 Da) and search for matching neutral masses in negative-mode assays (e.g., LNEG, HNEG) within the pre-defined mass tolerance (default 15 ppm). When matches are found within the same retention time window, assign both features to the same structural cluster, effectively merging positive/negative ion pair representations. This cross-linking step occurs after isotopologue/adduct clustering but before final cluster merging, and relies on the assumption that canonical ESI adducts are the dominant ionization products for the features of interest.

## Related tools

- **MamsiStructSearch** (Performs retention time windowing, isotopologue/adduct clustering, and cross-assay linking via the .get_structural_clusters() method) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Data loading and feature table manipulation (column parsing, filtering, merging))
- **numpy** (Mass difference calculations and tolerance comparisons)
- **scipy** (Numerical operations for mass tolerance evaluations within ppm thresholds)
- **networkx** (Construction and visualization of structural relationship networks with cross-assay edges)
- **peakPantheR** (Optional: provides ROI files for retention time annotation and quality control) — https://github.com/phenomecentre/peakPantheR

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=15)
struct.load_lcms(selected_features)
struct.get_structural_clusters(annotate=True)
```

## Evaluation signals

- Cross-assay linked feature pairs have matching neutral masses within ±ppm tolerance (default 15 ppm) and overlapping RT values (within ±5 seconds).
- Each structural cluster contains features from at least two different assay/ionization-mode combinations (verified by AssayName prefix in column headers).
- Network visualization shows cross-assay edges (distinct edge type or color) connecting nodes from different assays; edge weights or labels indicate adduct type ([M+H]+/[M-H]−).
- For validation: manually inspect a subset of high-confidence cross-linked pairs by comparing observed m/z differences to theoretical Δm/z = 1.007825 Da and confirming RT overlap.
- Merged cluster redundancy metric: fraction of features appearing in multiple assays should decrease post-merging, indicating successful consolidation.

## Limitations

- Cross-linking assumes canonical ESI adducts; features with unusual adducts (e.g., [M+NH4]+, [M+Na]+) may not be correctly matched if not explicitly included in the adduct list.
- Retention time drift across assays or instrumental runs can cause false negatives; RT tolerance (default 5 seconds) may require optimization per chromatographic protocol.
- The method does not resolve structural isomers—features with identical m/z and RT across assays will be merged even if they represent distinct metabolites.
- Cross-assay linking relies on high-quality feature detection and alignment; missing or misaligned features in either assay will produce incomplete clusters.
- The framework was tested on metabolomics phenotyping data but generalizability to other LC-MS applications (e.g., proteomics, lipidomics-only studies) is not established.

## Evidence

- [methods] Further, we search cross-assay clusters using [M+H]+/[M-H]− as link references.: "Further, we search cross-assay clusters using [M+H]<sup>+</sup>/[M-H]<sup>−</sup> as link references."
- [methods] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [intro] MAMSI links statistically significant features of untargeted multi-assay LC-MS metabolomics datasets into clusters defined by structural properties based on m/z and RT: "the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters"
- [methods] This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [methods] features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures: "all features are split into retention time (*RT*) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures"
