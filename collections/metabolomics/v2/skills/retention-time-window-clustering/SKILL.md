---
name: retention-time-window-clustering
description: Use when after filtering LC-MS features by statistical significance (e.g., p-value < 0.01) and you need to link individual m/z features into structural clusters representing the same metabolite in different ionization states or isotopic forms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - MamsiStructSearch
  - peakPantheR
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets.
- import pandas as pd
- import numpy as np
- 'Dependencies: scipy'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi_cq
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi_cq
schema_version: 0.2.0
---

# Retention-Time Window Clustering

## Summary

Split LC-MS features into fixed retention time windows and search within each window for isotopologue and adduct signatures to group structurally related features. This clustering step bridges individual m/z features to higher-order structural clusters by exploiting co-elution patterns.

## When to use

After filtering LC-MS features by statistical significance (e.g., p-value < 0.01) and you need to link individual m/z features into structural clusters representing the same metabolite in different ionization states or isotopic forms. Use when you have untargeted multi-assay LC-MS metabolomics data and want to reduce noise and annotation ambiguity by grouping features that co-elute and share chemical identity.

## When NOT to use

- Input features are already annotated and validated against a targeted metabolite library; use targeted extraction instead.
- RT values are missing or unreliable (e.g., from flow-injection or direct-infusion MS without chromatography).
- You are working with targeted assays where metabolite identity is already known; RT windowing is unnecessary overhead.

## Inputs

- Filtered LC-MS feature table (rows=samples, columns=significant features with m/z and RT metadata)
- Retention time values (seconds) for each feature
- Mass-to-charge (m/z) values for each feature
- Assay label or ionization mode identifier for each feature

## Outputs

- Structural clusters table with feature-to-cluster assignments
- Annotated cluster metadata including isotopologue links, adduct assignments, and cross-assay cluster identifiers
- Cluster-level neutral mass estimates with supporting evidence counts

## How to apply

Split all statistically significant LC-MS features into retention time (RT) windows of fixed width (typically 5 seconds). Within each RT window, search for isotopologue signatures by detecting mass differences of 1.00335 Da between m/z values; group features with matching mass differences. Next, calculate hypothetical neutral masses for common ESI adducts and group features with matching neutral masses within the specified ppm tolerance (e.g., 10 ppm). Finally, merge overlapping isotopologue and adduct clusters to form structural clusters, then search across assays for cross-linking patterns using [M+H]+/[M-H]- as reference signatures to identify the same metabolite measured in different ionization modes.

## Related tools

- **MamsiStructSearch** (Core component that implements retention-time windowing, isotopologue detection, adduct matching, and structural cluster merging for LC-MS features) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Data handling and feature table manipulation (loading, filtering, and grouping features by RT window and cluster))
- **scipy** (Mass difference calculations and tolerance-based matching within isotopologue and adduct detection)
- **peakPantheR** (Optional: provides ROI (region of interest) files for automated retention-time-based feature annotation within structural clusters) — https://github.com/phenomecentre/peakPantheR

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected)
struct.get_structural_clusters(annotate=True)
```

## Evaluation signals

- Structural clusters contain features with m/z differences matching expected isotopologue (1.00335 Da ± ppm tolerance) or common ESI adduct patterns ([M+H]+, [M-Na]+, [M-H]-, etc.).
- No feature appears in more than one structural cluster (clusters are mutually exclusive).
- Cross-assay links exist only between features from different ionization modes (e.g., HPOS and LPOS) with matching neutral masses; within-assay clusters do not falsely link different analytes.
- Cluster RT coherence: all features within a cluster fall within the specified RT window width (e.g., 5 seconds); clusters straddling window boundaries are not merged.
- Neutral mass estimates derived from adduct-matched clusters are chemically plausible (align with known metabolite masses or curated databases when available).

## Limitations

- RT window width (5 seconds) is a fixed parameter; peaks with high RT drift or co-eluting isomers may be incorrectly merged or split depending on assay chromatographic resolution.
- Isotopologue detection assumes natural abundance isotope ratios; enriched isotope experiments will produce false negatives.
- Adduct matching is limited to common ESI adducts defined in the tool; unusual or in-source-generated adducts will be missed.
- Cross-assay linking relies on neutral mass matching; features from assays with different m/z calibration or RT shifts may fail to link despite representing the same metabolite.
- The framework was tested on metabolomics phenotyping data; applicability to other LC-MS data types (e.g., proteomics, environmental samples) is untested.

## Evidence

- [methods] all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da: "all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da"
- [methods] This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [methods] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [methods] Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references.: "Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references."
- [readme] Firstly, all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da between mass-to-charge ratios (m/z) of the features: "Firstly, all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da"
- [readme] If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 ppm) then these features are grouped together.: "If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 ppm) then these features are grouped together."
