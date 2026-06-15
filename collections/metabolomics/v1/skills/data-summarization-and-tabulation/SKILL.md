---
name: data-summarization-and-tabulation
description: Use when after obtaining structural clusters from the MAMSI framework using different parameter configurations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - pandas
  - numpy
  - matplotlib
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
- from matplotlib import pyplot as plt
- A class for performing structural search on multi-modal MS data using
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi
schema_version: 0.2.0
---

# data-summarization-and-tabulation

## Summary

Extract and compute summary statistics from structural clustering outputs (cluster count, size distribution, feature coverage) and tabulate results across parameterized conditions (e.g., adduct mode selection) to enable side-by-side comparison of method effects on LC-MS feature grouping.

## When to use

After obtaining structural clusters from the MAMSI framework using different parameter configurations (e.g., adducts='all' vs adducts='most-common'), use this skill to compute cluster-level descriptive statistics and consolidate them into a single results table for quantitative comparison of how parameter choice affects clustering performance.

## When NOT to use

- Input is a single clustering result with no comparison group — data summarization alone is insufficient without a parameterization or method comparison context.
- Features have not yet been assigned to structural clusters; use MamsiStructSearch.get_structural_clusters() first.
- Cluster outputs are already in the required table format; skip directly to statistical comparison and visualization.

## Inputs

- Structural cluster objects from MamsiStructSearch.get_structural_clusters() calls (one per parameterization)
- Cluster metadata: cluster IDs, member feature counts, feature composition lists

## Outputs

- Summary statistics table (rows=parameter configurations, columns=Adduct Mode, Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage %)
- Size-distribution histograms (one histogram per adduct mode for visual comparison)
- Effect-size difference report (absolute and percentage changes in cluster count and mean cluster size between modes)

## How to apply

For each adduct mode or parameterization, extract cluster metadata (cluster ID, member count, constituent features) and compute summary statistics: total cluster count, mean/median/max cluster sizes, and feature coverage (percentage of input features appearing in ≥1 cluster). Generate size-distribution histograms for visual comparison. Compute effect-size differences (absolute and percentage changes in cluster count and mean cluster size) between modes. Consolidate outputs into a single results table with columns: Adduct Mode, Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage (%), enabling practitioners to quantitatively assess whether parameter choice materially affects the structural clustering output.

## Related tools

- **MAMSI (MamsiStructSearch)** (Generates structural clusters from LC-MS features via isotopologue and adduct signature detection; outputs are the input to this summarization skill) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Tabulate cluster metadata into DataFrames, compute summary statistics (count, mean, median, max, percentages))
- **numpy** (Compute descriptive statistics (mean, median, percentiles) on cluster size arrays)
- **matplotlib** (Generate size-distribution histograms for visual side-by-side comparison of adduct modes)

## Examples

```
struct_all = MamsiStructSearch(rt_win=5, ppm=10); struct_all.load_lcms(selected); struct_all.get_structural_clusters(adducts='all'); struct_mc = MamsiStructSearch(rt_win=5, ppm=10); struct_mc.load_lcms(selected); struct_mc.get_structural_clusters(adducts='most-common'); results = pd.DataFrame({'Adduct Mode': ['all', 'most-common'], 'Total Clusters': [len(struct_all.clusters), len(struct_mc.clusters)], 'Mean Cluster Size': [np.mean([len(c.members) for c in struct_all.clusters]), np.mean([len(c.members) for c in struct_mc.clusters])]}); results.to_csv('cluster_summary.csv', index=False)
```

## Evaluation signals

- Total cluster count is a positive integer; mean/median/max cluster sizes are positive and satisfy: mean ≤ max, median ≤ max
- Feature coverage (%) is between 0 and 100; sum of all feature memberships ≥ number of unique features in coverage denominator
- Effect-size differences (absolute and percentage changes) are correctly computed as: Δ = (value_mode2 − value_mode1) and % change = 100 × (value_mode2 − value_mode1) / value_mode1
- Results table has consistent row and column structure across all parameterizations; no missing or NaN values in summary statistics
- Size-distribution histograms show reasonable distributions (e.g., no negative bin counts or out-of-range cluster sizes)

## Limitations

- Summary statistics assume cluster membership is non-overlapping; if clusters can overlap, feature coverage calculation and mean cluster size may require clarification of counting semantics.
- Effect-size comparisons are valid only when the same input feature set (same p-value threshold, same LC-MS assays) is used across parameterizations; different input feature sets will confound method effects.
- Cluster count and size distribution are sensitive to retention time window width (rt_win parameter) and mass tolerance (ppm parameter); these must be held constant to isolate the effect of adduct mode selection.
- No statistical significance test (e.g., bootstrap CI, permutation test) is performed by default; effect sizes are descriptive only.

## Evidence

- [methods] Extract cluster metadata (cluster ID, size, member count, feature composition) and compute summary statistics (total cluster count, mean/median/max cluster sizes, size distribution histogram).: "Extract cluster metadata (cluster ID, size, member count, feature composition) and compute summary statistics (total cluster count, mean/median/max cluster sizes, size distribution histogram)."
- [methods] Compare outputs side-by-side: tabulate cluster counts, generate size-distribution plots for both modes, and compute effect-size differences (absolute and percentage change in cluster count and mean cluster size).: "Compare outputs side-by-side: tabulate cluster counts, generate size-distribution plots for both modes, and compute effect-size differences (absolute and percentage change in cluster count and mean"
- [methods] Produce a consolidated results table with columns: Adduct Mode, Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage (% features in ≥1 cluster).: "Produce a consolidated results table with columns: Adduct Mode, Total Clusters, Mean Cluster Size, Median Cluster Size, Max Cluster Size, Feature Coverage (% features in ≥1 cluster)."
- [other] tools: Python, pandas, numpy, matplotlib, MAMSI (MamsiStructSearch): "tools: Python, pandas, numpy, matplotlib, MAMSI (MamsiStructSearch)"
