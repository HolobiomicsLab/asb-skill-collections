---
name: spectral-feature-clustering-and-comparison
description: Use when after identifying statistically significant LC-MS features (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - pandas
  - numpy
  - matplotlib
  - MAMSI (MamsiStructSearch)
  - MamsiStructSearch
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Feature Clustering and Comparison

## Summary

Group LC-MS features into structural clusters based on isotopologue signatures, adduct patterns, and cross-assay links, then compare clustering outputs across different parameterizations (e.g., all adducts vs. most-common adducts) to quantify the effect of parameter choice on cluster composition and size distribution.

## When to use

After identifying statistically significant LC-MS features (e.g., via MB-VIP permutation testing), you want to understand whether structural clustering is robust to adduct mode selection, or conversely, you need to measure how restricting the adduct search space affects the number and composition of clusters recovered from multi-assay metabolomics data.

## When NOT to use

- Input features are already grouped into predefined metabolite classes or have been manually annotated and validated—clustering becomes redundant.
- Retention time or m/z values are missing, unreliable, or have not been quality-controlled; clustering will produce spurious links.
- The goal is to identify all possible metabolites in an untargeted experiment without filtering for statistical significance; use structural clustering on the full feature set instead of a pre-filtered subset.

## Inputs

- Statistically significant LC-MS feature intensity matrix (rows=samples, columns=features with naming convention AssayName_RTsec_m/z)
- Feature metadata (retention time in seconds, m/z values, assay assignment)

## Outputs

- Structural cluster metadata table (cluster ID, size, member count, feature composition, cluster mode)
- Cluster count and size distribution statistics (total clusters, mean/median/max cluster sizes per mode)
- Feature coverage metric (% features assigned to ≥1 cluster per mode)
- Side-by-side comparison table with columns: Adduct Mode, Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage
- Size-distribution histograms (adducts='all' vs. adducts='most-common')
- Effect-size summary (absolute and percentage change in cluster count and mean cluster size)

## How to apply

Load statistically significant LC-MS features into MamsiStructSearch with column names formatted as (AssayName)_(RTsec)_(m/z)m/z. Call get_structural_clusters() twice: once with adducts='all' and once with adducts='most-common'. Each call searches features within 5-second retention-time windows for isotopologue signatures (mass difference 1.00335 Da), common adduct patterns (ESI-based neutral mass matching at 15 ppm tolerance), and cross-assay links using [M+H]+/[M-H]- references, merging overlapping clusters into structural clusters. Extract cluster metadata (ID, size, member count, feature composition) and compute summary statistics (total cluster count, mean/median/max cluster sizes, size distribution histograms, feature coverage percentage). Generate side-by-side comparison tables and distribution plots, then calculate absolute and percentage changes in cluster count and mean cluster size between modes to quantify the effect.

## Related tools

- **MamsiStructSearch** (Core clustering engine: loads LC-MS features, executes isotopologue/adduct/cross-assay searches, merges overlapping clusters, and extracts cluster metadata and network representations) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Feature matrix manipulation, cluster metadata organization, and comparison table generation)
- **numpy** (Numerical computation of summary statistics (mean, median, max cluster sizes) and percentage changes)
- **matplotlib** (Generation of size-distribution histograms and side-by-side comparison plots)
- **Cytoscape** (Optional network visualization of structural relationships (adduct links, isotopologues, cross-assay links) recovered by clustering) — https://cytoscape.org

## Examples

```
from mamsi.mamsi_struct_search import MamsiStructSearch; struct = MamsiStructSearch(rt_win=5, ppm=15); struct.load_lcms(selected_features); clusters_all = struct.get_structural_clusters(adducts='all'); clusters_common = struct.get_structural_clusters(adducts='most-common')
```

## Evaluation signals

- Total cluster count and mean cluster size are reproducible and differ quantifiably between adducts='all' and adducts='most-common' modes (verify via effect-size calculation).
- Feature coverage (% features in ≥1 cluster) remains consistent across both modes, indicating that parameter choice does not drastically exclude features.
- Cluster size distributions show expected patterns: all-adduct mode may yield more clusters (smaller mean size) due to additional adduct matching, while most-common mode yields fewer larger clusters.
- Isotopologue signature detection (mass difference 1.00335 Da within 5-sec RT windows) is consistent across modes; cross-assay [M+H]+/[M-H]- links appear in both comparisons.
- Structural network visualization (via networkx/pyvis or Cytoscape export) shows connected components that correspond to putative metabolite groups with plausible adduct/isotope relationships.

## Limitations

- Clustering assumes that isotopologue (±1.00335 Da) and adduct mass differences are accurate; errors in feature m/z calibration propagate into spurious or missed clusters.
- The 15 ppm tolerance and 5-second retention-time window are fixed parameters; sensitivity to these thresholds is not explored within this workflow—tuning may be required for non-standard chromatography or high-resolution MS data.
- Cross-assay linking via [M+H]+/[M-H]- references only detects metabolites ionized in opposite modes; metabolites ionized in only one mode remain unlinked across assays.
- Clustering does not assign biological identity or confirm metabolite structure; annotation (via peakPantheR ROI files for NPC assays) is optional and only supported for specific chromatographic methods, limiting transferability to other labs.
- The framework was tested on metabolomics phenotyping data; utility for other LC-MS applications (e.g., proteomics, lipidomics-only) is not fully validated.

## Evidence

- [other] Load the selected LC-MS feature intensity data into MamsiStructSearch using load_lcms() with column naming convention (AssayName)_(RTsec)_(m/z)m/z.: "Load the selected LC-MS feature intensity data into MamsiStructSearch using load_lcms() with column naming convention (AssayName)_(RTsec)_(m/z)m/z."
- [other] Call get_structural_clusters() with adducts='all' parameter to identify isotopologue signatures (mass difference 1.00335 Da), adduct patterns (ESI-based neutral mass matching at 15 ppm tolerance), and cross-assay links ([M+H]+/[M-H]- references); merge overlapping clusters into structural clusters.: "Call get_structural_clusters() with adducts='all' parameter to identify isotopologue signatures (mass difference 1.00335 Da), adduct patterns (ESI-based neutral mass matching at 15 ppm tolerance),"
- [other] Extract cluster metadata (cluster ID, size, member count, feature composition) and compute summary statistics (total cluster count, mean/median/max cluster sizes, size distribution histogram).: "Extract cluster metadata (cluster ID, size, member count, feature composition) and compute summary statistics (total cluster count, mean/median/max cluster sizes, size distribution histogram)."
- [other] Repeat steps 2–3 using adducts='most-common' parameter. Compare outputs side-by-side: tabulate cluster counts, generate size-distribution plots for both modes, and compute effect-size differences (absolute and percentage change in cluster count and mean cluster size).: "Repeat steps 2–3 using adducts='most-common' parameter. Compare outputs side-by-side: tabulate cluster counts, generate size-distribution plots for both modes, and compute effect-size differences"
- [readme] each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da between mass-to-charge ratios (m/z) of the features: "each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da between mass-to-charge ratios (m/z) of the features"
- [readme] This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [readme] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [readme] Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references.: "Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references."
- [readme] the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data.: "the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data."
