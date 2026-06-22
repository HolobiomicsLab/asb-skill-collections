---
name: mass-spectrometry-structural-annotation
description: Use when after identifying statistically significant features (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pandas
  - numpy
  - matplotlib
  - MAMSI (MamsiStructSearch)
  - peakPantheR
  - Cytoscape
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

# mass-spectrometry-structural-annotation

## Summary

Link statistically significant LC-MS features into structural clusters by detecting isotopologue signatures, adduct patterns, and cross-assay relationships, parameterized by retention-time windows, mass tolerance, and adduct mode. This enables metabolite-level interpretation of untargeted multi-assay metabolomics datasets.

## When to use

After identifying statistically significant features (e.g., via MB-VIP and permutation testing on multi-assay LC-MS data) and you need to group them by structural properties (m/z, RT, adduct state, isotopologue relationships) to reduce feature-level noise and enable higher-confidence metabolite annotation and cross-assay feature linking.

## When NOT to use

- Input is already a feature table with collapsed metabolite identities or pre-curated metabolite annotations (structural clustering targets raw, significant features, not downstream metabolite tables).
- Retention time is not available or is unreliable; isotopologue and adduct detection require RT windows and accurate m/z.
- Data are from instruments or ionization modes not covered by the common ESI adduct set (e.g., APCI, MALDI, or highly specialized derivatization schemes); the method assumes electrospray ionization conventions.

## Inputs

- Pandas DataFrame of LC-MS feature intensities with column naming convention: AssayName_RTsec_m/z (e.g., HPOS_120.5_500.1234)
- Index/mask of statistically significant features (e.g., from MB-VIP p-value < 0.01)
- Retention-time window size (seconds, typically 5)
- Mass tolerance (ppm, typically 10–15)
- Adduct mode specification ('all' or 'most-common')

## Outputs

- Structural clusters (hierarchical groupings of features by isotopologue, adduct, and cross-assay relationships)
- Cluster metadata table: cluster ID, member count, size, composition, feature coverage (% features in ≥1 cluster)
- Cluster count and size distribution summary statistics (mean, median, max cluster size)
- Side-by-side comparison plots (cluster count and size distributions for different adduct modes)
- Effect-size table (absolute and percentage change in cluster count and mean cluster size between modes)
- Optional: structural network object (NX graph) with nodes = features, edges = structural relationships

## How to apply

Load statistically significant LC-MS features (with column naming convention AssayName_RTsec_m/z) into MamsiStructSearch, then partition features into retention-time windows (typically 5 seconds) and search each window for: (1) isotopologue signatures (mass difference 1.00335 Da between m/z values), (2) common adduct signatures by calculating hypothetical neutral masses at 15 ppm tolerance, (3) overlapping isotopologue and adduct clusters merged into structural clusters, and (4) cross-assay links using [M+H]⁺/[M-H]⁻ as references. The adduct search can be parameterized to use all common adducts or a restricted set of most-common adducts; compare outputs to assess sensitivity. Extract and tabulate cluster metadata (count, size distribution, feature coverage) to quantify the effect of parameter choices.

## Related tools

- **MAMSI (MamsiStructSearch)** (Primary tool for structural clustering: detects isotopologue and adduct signatures, merges overlapping clusters, cross-links assays, and returns cluster metadata and network objects.) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Data loading, manipulation, and tabulation of cluster metadata and summary statistics.)
- **numpy** (Numerical computation of mass differences, tolerance checks, and summary statistics.)
- **matplotlib** (Visualization of cluster size distributions and side-by-side comparison plots.)
- **peakPantheR** (Optional: source of region-of-interest (ROI) files used by MAMSI for automated feature annotation based on RT and m/z.) — https://github.com/phenomecentre/peakPantheR
- **Cytoscape** (Optional: visualization and exploration of structural network graphs exported from MAMSI.) — https://cytoscape.org

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=15)
struct.load_lcms(selected_features)
struct.get_structural_clusters(adducts='all')
clusters = struct.get_structural_clusters(adducts='most-common')
```

## Evaluation signals

- Cluster count and mean cluster size are consistent across independent runs with the same parameters; adduct mode variation produces interpretable effect-size differences (tabulated absolute and percentage changes).
- Feature coverage (% of input features assigned to ≥1 cluster) is non-zero and reported; features with consistent m/z differences (1.00335 Da) or matching neutral masses (within 15 ppm tolerance) appear in the same cluster.
- Cluster size distribution is unimodal or bimodal and matches the expected isotopologue and adduct multiplicity (e.g., clusters of size 2–4 for [M]⁺, [M+H]⁺, [M+Na]⁺ variants).
- Cross-assay links are present and identifiable; [M+H]⁺/[M-H]⁻ feature pairs from different assays appear in the same structural cluster.
- Output table schema includes all required columns (Adduct Mode, Total Clusters, Mean/Median/Max Cluster Size, Feature Coverage); no missing or NaN values in summary statistics.

## Limitations

- The 15 ppm tolerance for adduct mass matching may filter or merge valid adducts in heterogeneous datasets or high-noise regions; tolerance should be validated against instrument performance.
- Isotopologue detection relies on exact mass difference 1.00335 Da; assumes high mass accuracy (≤10 ppm); instruments with lower accuracy or high drift may fail to resolve isotopologues.
- The method is optimized for electrospray ionization (ESI); non-ESI ionization modes (APCI, MALDI, DART, etc.) or complex derivatization schemes are not explicitly supported and may produce spurious or incomplete clusters.
- Retention-time window size (e.g., 5 seconds) is a manual parameter; misspecification can cause features with similar m/z but different chemical structures to cluster together; optimal window size is dataset and chromatography-dependent.
- Cross-assay linking uses [M+H]⁺/[M-H]⁻ as reference; features without these forms (e.g., exclusively Na⁺ or other adducts) may not link across assays.
- Feature annotation is available only for assays profiled by the National Phenome Centre; external datasets will not be automatically annotated.

## Evidence

- [intro] MAMSI links statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters defined by structural properties based on m/z and RT: "the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters"
- [methods] Isotopologue and adduct signature detection with specified tolerance and adduct mode parameterization: "each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 *Da* between mass-to-charge ratios (*m/z*) of the features"
- [methods] Adduct signature search by neutral mass calculation with ESI-based adduct assumptions: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [methods] Merging overlapping isotopologue and adduct clusters into structural clusters: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [methods] Cross-assay linking using [M+H]⁺/[M-H]⁻ reference pairs: "Further, we search cross-assay clusters using [M+H]<sup>+</sup>/[M-H]<sup>-</sup> as link references."
- [other] Input format: features split into RT windows; column naming convention: "Load the selected LC-MS feature intensity data into MamsiStructSearch using load_lcms() with column naming convention (AssayName)_(RTsec)_(m/z)m/z"
- [other] Output: cluster metadata and summary statistics including cluster count, size distribution, and feature coverage: "Extract cluster metadata (cluster ID, size, member count, feature composition) and compute summary statistics (total cluster count, mean/median/max cluster sizes, size distribution histogram)"
- [other] Parameterization by adduct mode and effect-size comparison: "Compare outputs side-by-side: tabulate cluster counts, generate size-distribution plots for both modes, and compute effect-size differences (absolute and percentage change in cluster count and mean"
- [intro] Framework tested on metabolomics data but applicable to other LC-MS data types: "the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data"
- [readme] 15 ppm tolerance for neutral mass matching in adduct detection: "If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 *ppm*) then these features are grouped together"
