---
name: pearson-correlation-statistical-testing
description: Use when when you have two co-registered LA-ICP-MS element images and
  need to determine whether the spatial distribution of one element correlates significantly
  with another.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
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

# Pearson Correlation Statistical Testing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute the Pearson R coefficient between two co-registered LA-ICP-MS element channels and assess its statistical significance by comparing the observed R value to a null distribution generated from random shuffles of one input channel. This quantifies spatial correlation between element distributions and provides a probability estimate (ρ) that the observed correlation arose by chance.

## When to use

When you have two co-registered LA-ICP-MS element images and need to determine whether the spatial distribution of one element correlates significantly with another. Use this skill after image alignment and co-registration, particularly when interpreting whether observed spatial clustering of two elements is statistically meaningful or attributable to random chance.

## When NOT to use

- Input images are not co-registered or have misaligned spatial coordinates; alignment must be verified before correlation analysis.
- One or both channels contain predominantly NaN or missing values in the region of interest, as this will bias the R and ρ estimates.
- You are comparing more than two element channels; use alternative multivariate methods (e.g., principal component analysis) instead.

## Inputs

- Two co-registered LA-ICP-MS element channel images (numeric intensity arrays)
- Image or selected region of interest (optional; defaults to entire image)

## Outputs

- Pearson R coefficient (real number, range −1 to +1)
- Probability value ρ (p-value; real number, range 0 to 1)
- Shuffled R distribution (array of R values from permutation tests)

## How to apply

Load two co-registered element images (channels) into the Colocalisation Dialog via the image or selection context menu in pewpew. Compute the Pearson R coefficient over the entire image region or a user-defined region of interest. To assess statistical significance, calculate the probability (ρ) by comparing the observed R value to a distribution of R values obtained from random shuffles (permutations) of one of the input channels. Display and export the resulting R coefficient and ρ-value. Interpret R values close to +1 as strong positive correlation, close to −1 as strong negative correlation, and values near 0 as weak or no correlation. Use the ρ-value (e.g., ρ < 0.05) to reject the null hypothesis that the correlation is random.

## Related tools

- **pewpew** (GUI application providing the Colocalisation Dialog for computing Pearson R and managing co-registered LA-ICP-MS image pairs) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying pewpew that implements LA-ICP-MS data import, image alignment, and correlation coefficient computation) — https://github.com/djdt/pewlib

## Evaluation signals

- Pearson R coefficient is in the valid range [−1, +1] and matches manual computation on the input arrays.
- Probability value ρ is in the valid range [0, 1] and reflects the fraction of shuffled R values that equal or exceed the observed R in magnitude.
- Shuffled R distribution is approximately symmetric around zero, indicating that the permutation test is unbiased under the null hypothesis of no correlation.
- When applied to synthetic data with known correlation (e.g., identical channels), R approaches 1.0 and ρ approaches 0; when applied to independent random noise, R approaches 0 and ρ approaches 1.0.
- Results exported from the dialog via copy-to-clipboard or context menu match the displayed R and ρ values with full precision.

## Limitations

- Pearson R assumes linear relationships; nonlinear spatial associations between channels may be missed or underestimated.
- The permutation-based ρ-value is computationally expensive for large images and may require significant runtime or memory; the number of shuffles influences precision of the p-value estimate.
- Spatial autocorrelation within each channel can inflate the significance of apparent correlations; the method does not account for non-independence of neighboring pixels.
- The presence of outliers or extreme intensity values in either channel can substantially affect R; no robust correlation variant (e.g., Spearman rank) is described in the workflow.

## Evidence

- [other] Compute Pearson R coefficient over the entire image region and optionally calculate its probability (ρ) by comparing the R value to those of random shuffles of the input.: "Compute Pearson R coefficient over the entire image region and optionally calculate its probability (ρ) by comparing the R value to those of random shuffles of the input."
- [other] The Colocalisation Dialog computes Pearson R, Li ICQ, and Manders coefficients (via Costes thresholding method) to quantify spatial relationships between two element channels in co-registered images.: "The Colocalisation Dialog computes Pearson R, Li ICQ, and Manders coefficients (via Costes thresholding method) to quantify spatial relationships between two element channels in co-registered images."
- [other] Load two co-registered element images (channels) into the Colocalisation Dialog via image or selection context menu.: "Load two co-registered element images (channels) into the Colocalisation Dialog via image or selection context menu."
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib.: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib."
