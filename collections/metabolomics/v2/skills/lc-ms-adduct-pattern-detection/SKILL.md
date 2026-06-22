---
name: lc-ms-adduct-pattern-detection
description: Use when when you have statistically significant features from multi-assay LC-MS metabolomics data (with m/z and retention time annotations) and need to group features that may represent the same compound ionized as different adducts (e.g., [M+H]⁺ vs. [M+Na]⁺).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pandas
  - numpy
  - matplotlib
  - MAMSI (MamsiStructSearch)
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
- from matplotlib import pyplot as plt
- A class for performing structural search on multi-modal MS data using
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

# LC-MS adduct pattern detection

## Summary

Identifies common adduct signatures in untargeted LC-MS features by calculating hypothetical neutral masses from known electrospray ionization adducts and matching them within a mass tolerance window. This clustering step links features that likely derive from the same molecular species ionized under different conditions.

## When to use

When you have statistically significant features from multi-assay LC-MS metabolomics data (with m/z and retention time annotations) and need to group features that may represent the same compound ionized as different adducts (e.g., [M+H]⁺ vs. [M+Na]⁺). Use this skill after isotopologue detection and before merging overlapping clusters into structural groups, especially when analyzing data from multiple ionization assays (positive and negative mode).

## When NOT to use

- Input features lack accurate m/z or retention time annotations (adduct matching requires precise mass values).
- Data originate from targeted LC-MS or MRM assays where compound identity is already known (adduct detection is designed for untargeted discovery).
- Features have not yet been filtered for statistical significance or quality control (applying adduct detection to noise or artifacts will inflate cluster counts).

## Inputs

- Statistically significant LC-MS features (pandas DataFrame with columns: AssayName, RTsec, m/z)
- Mass tolerance threshold in ppm (integer, typically 10–15)
- Retention time window size in seconds (typically 5)
- Adduct list or mode ('all' common adducts vs. 'most-common' subset)

## Outputs

- Adduct clusters (grouped features with matching neutral masses within tolerance)
- Cluster metadata (cluster ID, member feature count, neutral mass, assay composition)
- Cluster summary statistics (total cluster count, mean/median/max cluster sizes)
- Feature coverage metric (percentage of input features assigned to ≥1 cluster)

## How to apply

Within each 5-second retention time window, calculate the hypothetical neutral mass for each feature by reversing common electrospray ionization adduct transformations (e.g., subtracting 1.00783 Da for [M+H]⁺, adding 18.01056 Da for [M-H]⁻). Group features whose hypothetical neutral masses match within a pre-defined mass tolerance (typically 10–15 ppm). The rationale is that features with identical neutral masses but different m/z values represent the same metabolite in different ionization states. Merge these adduct clusters with previously detected isotopologue clusters to form structural clusters. Document the matching tolerance and which adducts were searched (either all common adducts or a restricted 'most-common' set) as this directly affects cluster count and composition.

## Related tools

- **MAMSI (MamsiStructSearch)** (Python class that implements adduct signature search, isotopologue detection, and structural cluster merging via the get_structural_clusters() method with adducts parameter) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Data manipulation and filtering of LC-MS feature tables before and after adduct clustering)
- **numpy** (Mass tolerance calculations and neutral mass arithmetic)
- **matplotlib** (Visualization of cluster size distributions and comparison plots between adduct modes)
- **peakPantheR** (Optional: provides region-of-interest (ROI) files for automated annotation of detected adduct clusters by retention time and m/z) — https://github.com/phenomecentre/peakPantheR

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=15)
struct.load_lcms(selected_features)
struct.get_structural_clusters(adducts='most-common')
```

## Evaluation signals

- Adduct cluster counts are stable and reproducible within the same tolerance and assay pair (no stochastic variation between runs).
- Features within each adduct cluster have neutral masses that agree to within the declared ppm tolerance (verify by back-calculating neutral mass for each feature and checking standard deviation).
- Feature coverage (percentage of input features in ≥1 cluster) increases monotonically or plateaus as adduct tolerance is relaxed; a sudden jump may indicate tolerance is too permissive.
- When comparing 'all' vs. 'most-common' adduct modes, the more restrictive mode produces fewer but more confident clusters; the difference in total cluster count and mean cluster size should be documented and biologically plausible.
- Cluster composition respects assay boundaries: cross-assay adduct links (e.g., [M+H]⁺ in positive mode matched to [M-H]⁻ in negative mode) are validated separately and reported with distinct link type labels.

## Limitations

- Adduct detection relies on accurate m/z values; systematic mass calibration errors (>2 ppm) will cause true adduct pairs to be missed or false matches to occur.
- The method assumes features in the same 5-second retention time window are co-eluting; features that co-elute may have different neutral masses and represent distinct compounds, leading to false grouping if the RT window is too wide.
- Isobaric compounds (same neutral mass, different structure) cannot be distinguished by m/z alone; additional evidence (MS/MS fragmentation, external databases) is needed to resolve them.
- The number of clusters and mean cluster size are sensitive to the choice of mass tolerance and adduct list; no automatic threshold selection is provided, and users must justify their chosen tolerance based on instrument calibration and metabolite database literature.
- Framework was tested on metabolomics phenotyping data; performance on other LC-MS data types (proteomics, natural products) is unvalidated.

## Evidence

- [readme] This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [readme] If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 *ppm*) then these features are grouped together.: "If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 *ppm*) then these features are grouped together."
- [readme] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [other] adduct patterns (ESI-based neutral mass matching at 15 ppm tolerance): "adduct patterns (ESI-based neutral mass matching at 15 ppm tolerance)"
- [other] MAMSI enables clustering of LC-MS features by structural properties through adduct signature detection, which can be parameterized to search either all common adducts or a restricted set of most-common adducts.: "MAMSI enables clustering of LC-MS features by structural properties through adduct signature detection, which can be parameterized to search either all common adducts or a restricted set of"
- [readme] each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 *Da* between mass-to-charge ratios (*m/z*) of the features: "each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 *Da* between mass-to-charge ratios (*m/z*) of the features"
