---
name: metabolite-feature-annotation-aggregation
description: Use when after selecting statistically significant features from multi-assay
  LC-MS metabolomics datasets (e.g., via MB-VIP and permutation testing with p < 0.01).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - MAMSI (MamsiStructSearch)
  - peakPantheR
  - NetworkX / Cytoscape
  - pandas / numpy
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

# metabolite-feature-annotation-aggregation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automated annotation and structural linking of statistically significant untargeted LC-MS features into metabolite clusters defined by mass-to-charge ratio (m/z), retention time (RT), and structural properties (isotopologues, adducts, cross-assay links). This skill aggregates isolated feature detections into coherent metabolite signatures for improved biological interpretation.

## When to use

After selecting statistically significant features from multi-assay LC-MS metabolomics datasets (e.g., via MB-VIP and permutation testing with p < 0.01). Apply this skill when you need to collapse multiple m/z and RT observations into single metabolite identities, and when you have access to retention-time-based metabolite reference annotations (ROI files) or can perform computational structural inference via isotopologue/adduct mass matching within defined mass tolerance (e.g., 15 ppm).

## When NOT to use

- Input is already a curated targeted assay with authenticated metabolite identities; annotation-aggregation is redundant.
- LC-MS data were acquired on low-resolution instruments (unit or 0.1 Da mass accuracy) where mass-tolerance-based adduct matching is unreliable.
- Retention time is not calibrated or normalized across assays, making RT-window partitioning uninformative.

## Inputs

- Selected significant LC-MS features (pandas DataFrame with m/z, retention time, assay prefix columns)
- Multi-assay LC-MS data blocks (HPOS, LPOS, LNEG, RNEG, RPOS, or similar ionization modes)
- Correlation matrix or hierarchical dendrogram from prior MamsiStructSearch run
- ROI files (peakPantheR format, optional) containing reference metabolite annotations with RT and m/z

## Outputs

- Structural cluster assignments (feature ID → cluster ID mapping)
- Cluster membership tables showing feature-level isotopologue, adduct, and cross-assay link types
- Agreement metrics between clustering methods (adjusted Rand index, normalized mutual information)
- Annotated feature list with putative metabolite identities (if ROI-based annotation is applied)
- Network object (NetworkX or Cytoscape-compatible) encoding structural relationships

## How to apply

First, partition significant features into retention-time windows (typically 5-second intervals) to isolate co-eluting species. Within each RT window, search for isotopologue signatures by detecting mass differences of 1.00335 Da between m/z values; group matching pairs. Next, calculate hypothetical neutral masses for each feature assuming common electrospray adducts ([M+H]+, [M-H]−, etc.), and cluster features whose neutral masses match within a defined mass tolerance (typically 15 ppm for high-resolution instruments). Merge overlapping isotopologue and adduct clusters to form structural clusters. Optionally, link cross-assay clusters using [M+H]+/[M-H]− mass-difference signatures as bridge references. If ROI files (peakPantheR format) are available, perform automated annotation by matching observed RT and m/z against reference libraries. Finally, compute a hierarchical dendrogram on feature correlation matrices and flatten using either constant-threshold or silhouette-score optimization to yield consensus cluster assignments. Evaluate agreement between methods (e.g., adjusted Rand index, normalized mutual information) to validate stability.

## Related tools

- **MAMSI (MamsiStructSearch)** (Core framework for structural clustering, isotopologue/adduct detection, and optional ROI-based annotation of LC-MS features) — https://github.com/kopeckylukas/py-mamsi
- **peakPantheR** (Provides ROI (region of interest) files encoding reference retention time and m/z for automated metabolite annotation) — https://github.com/phenomecentre/peakPantheR
- **scikit-learn** (Computes clustering agreement metrics (adjusted Rand index, normalized mutual information) and supports silhouette-score optimization for dendrogram flattening)
- **scipy** (Provides hierarchical clustering, dendrogram construction, and distance metrics for feature correlation analysis)
- **NetworkX / Cytoscape** (Visualizes and exports structural relationship networks as interactive graph objects for manual inspection of adduct/isotopologue/cross-assay links)
- **pandas / numpy** (Data manipulation, tabulation of cluster assignments, and mass/RT difference calculations)

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=15)
struct.load_lcms(selected)
struct.get_structural_clusters(annotate=True)
struct.get_correlation_clusters(flat_method='silhouette', max_clusters=11)
```

## Evaluation signals

- Isotopologue detection: verify that identified mass differences match 1.00335 Da (±instrument accuracy) and that paired features co-elute within the same RT window
- Adduct clustering: confirm that inferred neutral masses for features within a structural cluster agree to within the specified tolerance (15 ppm); check that adduct type assignments are chemically plausible for the ionization mode
- Cluster stability: agreement metrics (e.g., adjusted Rand index > 0.8) between constant-threshold and silhouette-optimized clustering solutions indicate robust assignments
- Cross-assay linking: verify that [M+H]+/[M-H]− links correctly map features across positive and negative ion-mode assays with expected mass differences (~1.008 Da per charge)
- Annotation coverage: if ROI-based annotation is applied, report the proportion of features with matched reference entries and the median RT/m/z error distributions

## Limitations

- Annotation quality depends on mass measurement accuracy and RT calibration consistency; low-resolution instruments (>5 ppm error) may produce spurious adduct matches within 15 ppm tolerance.
- ROI-based annotation is limited to metabolites covered by reference libraries (e.g., NPC assay annotations); novel or unknown metabolites will lack putative identities.
- Isotopologue and adduct detection assume standard ESI polarity conventions; non-standard ionization methods or exotic adducts (e.g., [M+Na]+, [M+Cl]−) may not be detected.
- Hierarchical dendrogram flattening is sensitive to linkage method choice (complete, average, single); silhouette optimization requires specification of max_clusters parameter, which is data-dependent and not automatically determined.
- The framework was tested on metabolomics phenotyping data; applicability to other LC-MS data types (e.g., proteomics, lipidomics-specific instruments) is acknowledged but not formally validated.

## Evidence

- [methods] each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da between mass-to-charge ratios (m/z) of the features: "each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 *Da* between mass-to-charge ratios (*m/z*) of the features"
- [methods] This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [methods] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [methods] Further, we search cross-assay clusters using [M+H]+/[M-H]− as link references.: "Further, we search cross-assay clusters using [M+H]<sup>+</sup>/[M-H]<sup>−</sup> as link references."
- [intro] MAMSI links statistically significant features of untargeted multi-assay LC-MS metabolomics datasets into clusters defined by structural properties based on m/z and RT: "the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters"
- [methods] our structural search tool, that utilises region of interest (ROI) files from peakPantheR, allows for automated annotation of some features based on the RT for a given chromatography and m/z.: "our structural search tool, that utilises region of interest [(ROI) files](https://github.com/phenomecentre/npc-open-lcms) from peakPantheR [[4](#references)], allows for automated annotation of"
- [intro] the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data.: "the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data."
- [methods] Re-flatten the same dendrogram using silhouette-score optimization with max_clusters=11 via the get_correlation_clusters() method with flat_method='silhouette'.: "Re-flatten the same dendrogram using silhouette-score optimization with max_clusters=11 via the get_correlation_clusters() method with flat_method='silhouette'."
- [methods] Compute agreement metrics (adjusted Rand index, normalized mutual information) between the two clustering solutions.: "Compute agreement metrics (adjusted Rand index, normalized mutual information) between the two clustering solutions."
