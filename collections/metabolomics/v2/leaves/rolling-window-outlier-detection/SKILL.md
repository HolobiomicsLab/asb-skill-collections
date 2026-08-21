---
name: rolling-window-outlier-detection
description: Use when raw LA-ICP-MS image data contains isolated spike artifacts—pixels
  with anomalously high or low intensities relative to their spatial neighborhood—that
  distort downstream quantification or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0769
  tools:
  - pewpew
  - pewlib
  - Python
  - pew²
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

# rolling-window-outlier-detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Detects and removes spike outliers from LA-ICP-MS image data by comparing each pixel against local rolling-window statistics (median or mean). The skill identifies pixels deviating beyond a configurable threshold and replaces them with the local statistic, preserving spatial structure while suppressing instrumental noise.

## When to use

Apply this skill when raw LA-ICP-MS image data contains isolated spike artifacts—pixels with anomalously high or low intensities relative to their spatial neighborhood—that distort downstream quantification or visualization. Typical triggers: visual inspection reveals bright/dark spots uncorrelated with sample chemistry, or statistical summaries show implausible outliers at individual pixel positions in line-by-line, spot-wise, or ablation-time-aligned data.

## When NOT to use

- Input is already a pre-filtered or processed dataset; re-filtering may introduce artificial bias.
- Spikes are not isolated pixels but represent genuine sample heterogeneity or legitimate geochemical features; median/mean replacement will erase true compositional variation.
- Data are from spot-wise or time-resolved ablation where the local neighborhood is not spatially coherent; rolling-window assumptions break down.

## Inputs

- LA-ICP-MS image data (raw, with spike artifacts)
- Window size parameter (integer: 3, 5, or 7 pixels)
- Threshold parameter (M for Rolling Median, σ for Rolling Mean)
- Filter type selection (Rolling Median or Rolling Mean)

## Outputs

- Filtered LA-ICP-MS image with spike outliers replaced
- Layer or exported image file with spike removal applied

## How to apply

Load the raw LA-ICP-MS image into pew² and select either Rolling Median (threshold M = distance in medians from local median) or Rolling Mean (threshold σ = distance in standard deviations from local mean). Set the window size (typical: 3, 5, or 7 pixels) and threshold parameter according to your noise level and desired spike sensitivity. Apply the filter, which compares each pixel's absolute deviation against the local statistic (computed excluding the tested pixel itself). Replace outlier pixels with the corresponding local median or mean. Output the filtered image as a new layer or export. The choice between median and mean depends on spike distribution: median is more robust to extreme outliers; mean is more sensitive to broader deviations.

## Related tools

- **pew²** (GUI platform for importing, filtering, and exporting LA-ICP-MS image data; implements both Rolling Median and Rolling Mean filters with configurable window size and threshold) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying pew² that performs the rolling-window statistical computation and pixel replacement logic) — https://github.com/djdt/pewlib

## Evaluation signals

- Spike pixels (outliers beyond threshold) are visually absent or greatly reduced in the filtered image compared to the raw input.
- Histogram or intensity distribution of the filtered image shows elimination of extreme outlier pixels while preserving the bulk intensity distribution.
- Local spatial continuity is improved: neighboring pixels are now more similar in intensity, without artificial blurring of true compositional boundaries.
- Re-application of the same filter with the same parameters produces idempotent output (no further spikes removed), indicating convergence.
- Quantitative metrics (e.g., mean, median, standard deviation of pixel intensities in homogeneous regions) are stable and more plausible after filtering.

## Limitations

- Rolling-window filters assume spike outliers are isolated to single or very few pixels; dense clusters of anomalous pixels may not be fully corrected.
- Window size (3, 5, 7) is a discrete choice; suboptimal selection can either miss subtle spikes or over-smooth legitimate fine structure.
- Threshold parameter (M or σ) must be manually tuned; no automatic threshold selection is documented in the workflow.
- Median replacement is robust but may create discontinuities at spike boundaries; mean replacement is smoother but may propagate spike influence into surrounding pixels.
- The filter excludes the tested pixel from the local statistic, which is conservative but may underestimate the local value in strongly trended regions.

## Evidence

- [methods] Rolling Median filtering mechanism: "Rolling Median filtering compares each pixel against a local median value and uses a threshold M (distance in medians from the local median) to identify and replace outlier pixels."
- [methods] Window size and threshold parameters: "Set the window size (typical values: 3, 5, or 7 pixels) and the threshold parameter according to the chosen filter."
- [methods] Rolling Mean as alternative filter: "Rolling Mean (threshold σ = Distance in stddevs from the local mean)"
- [methods] Pixel exclusion from local statistic: "Replace outlier pixels with the corresponding local median (Rolling Median) or local mean (Rolling Mean), excluding the tested pixel from the local statistic."
- [readme] pew² as filtering platform: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib."
