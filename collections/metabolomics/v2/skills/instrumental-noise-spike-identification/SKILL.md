---
name: instrumental-noise-spike-identification
description: Use when you have raw LA-ICP-MS image data (line-by-line, spot-wise,
  or ablation-time-aligned) that exhibits isolated high-intensity or low-intensity
  pixels inconsistent with neighboring pixels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - pewpew
  - pewlib
  - Python
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.1c02138
  title: Pew2
- doi: 10.1529/biophysj.103.038422
  title: ''
evidence_spans:
- The built in `Filtering Tool` removes spikes by comparing pixel values to a locally
  defined threshold
- '|pewpew| is an open-source LA-ICP-MS data import and processing application'
- based on the python library pewlib_
- python library [pewlib]
- python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pew2_cq
    doi: 10.1021/acs.analchem.1c02138
    title: Pew2
  dedup_kept_from: coll_pew2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02138
  all_source_dois:
  - 10.1021/acs.analchem.1c02138
  - 10.1529/biophysj.103.038422
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Instrumental Noise Spike Identification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and flag outlier pixels in LA-ICP-MS image data that deviate anomalously from their local neighborhood, using rolling statistical comparisons (median or mean) to distinguish instrumental noise spikes from true signal. This skill is essential for preprocessing ablation image data before quantitative analysis.

## When to use

Apply this skill when you have raw LA-ICP-MS image data (line-by-line, spot-wise, or ablation-time-aligned) that exhibits isolated high-intensity or low-intensity pixels inconsistent with neighboring pixels. Spike artifacts are common in LA-ICP-MS and must be identified before filtering or exporting for downstream quantification. Use it as a prerequisite to spike removal or when you need to flag suspicious pixels for manual review or masking.

## When NOT to use

- If the data has already been spike-filtered or if you are working with pre-processed or binned aggregates where spike structure is no longer resolvable at pixel level.
- If your goal is absolute spike removal rather than identification; use the companion spike-removal skill instead, which replaces flagged pixels with local median or mean.
- If the noise is systematic (e.g., whole-line drop-outs, detector dead zones) rather than random isolated pixels; spike identification targets only localized anomalies.

## Inputs

- raw LA-ICP-MS image data (line-by-line, spot-wise, or ablation-time-aligned)
- window size parameter (integer: 3, 5, 7, or other odd values)
- threshold parameter M (rolling median mode) or σ (rolling mean mode)

## Outputs

- spike-flagged image or pixel coordinate list identifying outliers
- boolean or numeric mask indicating spike locations
- optional: visualization overlay showing flagged pixels on original image

## How to apply

Load raw LA-ICP-MS image data into the Filtering Tool (pewpew). Choose between Rolling Median (comparing each pixel against a local median, flagging pixels at distance M or more in medians from the local median) or Rolling Mean (comparing against local mean, flagging pixels at distance σ or more in standard deviations from the local mean). Set window size (typically 3, 5, or 7 pixels) and threshold parameter M or σ based on your spike sensitivity tolerance. Apply the filter to test each pixel against its local rolling-window statistic, excluding the tested pixel itself from the statistic. Output identifies which pixels exceed the threshold; these are the spike candidates. The choice between median and mean depends on noise distribution: median is more robust to extreme outliers, while mean is simpler but can be influenced by the spikes themselves.

## Related tools

- **pewpew** (GUI application for importing, visualizing, and applying spike-identification filters to LA-ICP-MS image data) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying pewpew; provides the rolling median/mean filter algorithms and data I/O for LA-ICP-MS formats) — https://github.com/djdt/pewlib

## Evaluation signals

- Flagged pixels should form isolated clusters or single pixels, not contiguous regions (indicating true noise rather than valid signal variation).
- Spike flags should be spatially uncorrelated with known sample boundaries or regions of interest; systematic geographic patterns suggest incorrect threshold choice.
- Visual overlay of flagged pixels on the raw image should show clear visual anomalies (extreme high/low intensity relative to neighbors) at every flagged location.
- Comparing results from Rolling Median vs. Rolling Mean on the same data should yield similar spike locations (confirming robustness); large divergence suggests threshold or window size is marginal.
- Sensitivity test: gradually increasing M (or σ) should increase the count of flagged pixels monotonically, with rapid jump indicating the true threshold where instrumental noise becomes dominant.

## Limitations

- Window size (typically 3–7 pixels) must be chosen a priori; too small and true signal variations are flagged as spikes; too large and real instrumental spikes are missed.
- Threshold parameters M and σ are user-set and data-dependent; no universal defaults are documented; choice requires either prior calibration or manual tuning on representative images.
- Rolling Median is robust but computationally slower than Rolling Mean; large images or many filters may require optimization.
- Method assumes spikes are truly localized (isolated pixels or very small clusters); extended spike features (e.g., line artifacts) will not be fully resolved by this pixel-level approach.
- Does not distinguish between instrumental spikes and true high-concentration micro-inclusions; domain knowledge or complementary element analysis required for interpretation.

## Evidence

- [other] Rolling Median filtering compares each pixel against a local median value and uses a threshold M (distance in medians from the local median) to identify and replace outlier pixels.: "Rolling Median filtering compares each pixel against a local median value and uses a threshold M (distance in medians from the local median) to identify and replace outlier pixels."
- [other] Set the window size (typical values: 3, 5, or 7 pixels) and the threshold parameter according to the chosen filter. Apply the filter to identify pixels where the absolute deviation exceeds the threshold.: "Set the window size (typical values: 3, 5, or 7 pixels) and the threshold parameter according to the chosen filter. Apply the filter to identify pixels where the absolute deviation exceeds the"
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library"
- [methods] Rolling Mean | σ | Distance in stddevs from the local mean; Rolling Median | M | Distance in medians from the local median: "Rolling Mean | σ | Distance in stddevs from the local mean; Rolling Median | M | Distance in medians from the local median"
- [readme] Pewlib is a library for importing, processing and exporting LA-ICP-MS data.: "Pewlib is a library for importing, processing and exporting LA-ICP-MS data."
