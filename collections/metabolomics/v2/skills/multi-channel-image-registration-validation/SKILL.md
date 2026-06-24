---
name: multi-channel-image-registration-validation
description: Use when after importing and manually aligning two element channels in
  LA-ICP-MS images, use this skill to confirm registration quality before computing
  spatial relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3382
  - http://edamontology.org/topic_0091
  tools:
  - pewpew
  - pewlib
  - Python
  license_tier: restricted
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

# Multi-channel Image Registration Validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validates spatial alignment of two co-registered element channels in LA-ICP-MS images by computing quantitative colocalization coefficients (Pearson R, Li ICQ, and Manders) to confirm registration fidelity before downstream spatial analysis.

## When to use

After importing and manually aligning two element channels in LA-ICP-MS images, use this skill to confirm registration quality before computing spatial relationships. Apply when you need to test whether observed colocalization is genuine (not due to misalignment) or when preparing images for quantitative colocalization analysis.

## When NOT to use

- Input channels are not co-registered or not in the same coordinate frame—manually align via overlay pixel size first
- Only one element channel is available; this skill requires exactly two channels
- Raw unprocessed LA-ICP-MS data has not been imported and calibrated; preprocessing must precede registration validation

## Inputs

- Two co-registered LA-ICP-MS element channel images (loaded as separate layers or selections)
- Image region of interest (optional; defaults to entire image)

## Outputs

- Pearson R coefficient with probability (ρ) value
- Li ICQ coefficient
- Manders M1 and M2 coefficients (Costes-thresholded)
- Exported coefficient table (context menu or clipboard)

## How to apply

Load two co-registered element images into the Colocalisation Dialog via the image or selection context menu. Compute Li ICQ coefficient over the entire image region to assess overall pixel-wise correlation. Calculate Pearson R coefficient and its probability (ρ) by comparing the R value to those of random shuffles of the input—high ρ indicates genuine colocalization rather than chance. Apply Costes thresholding method to compute Manders coefficients on the full image or selected region to quantify the proportion of each channel that overlaps. Display and export all three coefficients; strong alignment is indicated by Pearson R > 0.5 and Manders values showing substantial overlap. Use this coefficient profile as a registration quality gate: poor coefficients suggest realignment is needed before proceeding.

## Related tools

- **pewpew** (GUI host for loading co-registered images and launching Colocalisation Dialog) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying image import, channel selection, and coefficient computation) — https://github.com/djdt/pewlib

## Evaluation signals

- Pearson R coefficient is between −1 and +1, with positive values > 0.5 indicating acceptable alignment
- Probability (ρ) of Pearson R under random shuffle is < 0.05, confirming colocalization is not due to chance
- Manders M1 and M2 coefficients are both between 0 and 1 and show symmetric or near-symmetric overlap (M1 ≈ M2 for genuine colocalization)
- Li ICQ coefficient is positive and ideally > 0 (negative Li ICQ suggests channels are anticorrelated or misaligned)
- All three coefficient types are successfully exported and match expected ranges for known positive-control co-registered pairs

## Limitations

- Coefficients are sensitive to pixel intensity distribution and thresholding method; Costes thresholding assumes signal above local background
- Pearson R does not detect non-linear spatial relationships; use in combination with visual inspection of overlay
- Random shuffle probability (ρ) requires sufficient sample size; images with very few bright pixels may produce unreliable ρ estimates
- Manders coefficients can be high even for partially misaligned images if only a subset of pixels overlap; validate with region-specific analysis

## Evidence

- [other] Load two co-registered element images (channels) into the Colocalisation Dialog via image or selection context menu.: "Load two co-registered element images (channels) into the Colocalisation Dialog via image or selection context menu."
- [other] Compute Li ICQ coefficient over the entire image region. Compute Pearson R coefficient over the entire image region and optionally calculate its probability (ρ) by comparing the R value to those of random shuffles of the input.: "Compute Li ICQ coefficient over the entire image region. Compute Pearson R coefficient over the entire image region and optionally calculate its probability (ρ) by comparing the R value to those of"
- [other] Compute Manders coefficients using the Costes thresholding method on the image or selected region.: "Compute Manders coefficients using the Costes thresholding method on the image or selected region."
- [other] The Colocalisation Dialog computes Pearson R, Li ICQ, and Manders coefficients (via Costes thresholding method) to quantify spatial relationships between two element channels in co-registered images.: "The Colocalisation Dialog computes Pearson R, Li ICQ, and Manders coefficients (via Costes thresholding method) to quantify spatial relationships between two element channels in co-registered images."
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib"
