---
name: fragment-ion-spectral-matching
description: Use when after pointwise correlation analysis and exact mass difference refinement have identified candidate ion-species pairs that may share a common analyte origin.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DBDIpy
  - Python
  - matchms
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bioinformatics/btad088/7036334
  title: DBDIpy
evidence_spans:
- DBDIpy is an open-source Python library for the curation and interpretation of dielectric barrier discharge ionisation mass spectrometric datasets
- DBDIpy is an open-source Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dbdipy_cq
    doi: 10.1093/bioinformatics/btad088/7036334
    title: DBDIpy
  dedup_kept_from: coll_dbdipy_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btad088/7036334
  all_source_dois:
  - 10.1093/bioinformatics/btad088/7036334
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragment-ion-spectral-matching

## Summary

Calculate MS2 spectral similarity scores between fragment ion profiles of candidate ion-species pairs to confirm they originate from the same analyte compound. This is the final confirmation step in DBDIpy's three-stage identification pipeline for direct-injection plasma ionization mass spectrometry.

## When to use

Apply this skill after pointwise correlation analysis and exact mass difference refinement have identified candidate ion-species pairs that may share a common analyte origin. Use it when you have preprocessed MS2 fragment spectra (normalized intensity, noise-removed) for each candidate pair and need to computationally verify their putative relationship by comparing fragmentation patterns.

## When NOT to use

- MS2 data are not available or are of poor quality (sparse fragmentation, low signal-to-noise ratio)
- Input is a single ion species without a paired candidate — spectral similarity comparison requires at least two spectra
- Candidate pairs have not yet undergone pointwise correlation and mass difference refinement (required upstream steps)

## Inputs

- MS2 spectral data (fragment m/z–intensity pairs for each ion species)
- candidate ion-species pair list from mass difference refinement step
- preprocessed fragment spectra (intensity-normalized, noise-reduced)

## Outputs

- annotated candidate pair table with spectral similarity scores
- confirmation status for each pair (above/below threshold)
- output table mapping candidate pairs to spectral similarity scores and confirmation status

## How to apply

For each candidate ion-species pair output from the mass difference refinement step, extract and preprocess the corresponding MS2 fragment spectra by normalizing intensities and removing noise. Calculate the spectral similarity score using cosine similarity or a related spectral matching algorithm that compares the fragment ion profiles between pair members. Annotate each candidate pair with its computed similarity score and apply an acceptance threshold (typically ≥0.9 for Pearson correlation in the DBDIpy workflow) to flag pairs that exceed the threshold as confirmed shared-analyte relationships. Generate a final output table mapping each candidate pair to its spectral similarity score and confirmation status.

## Related tools

- **DBDIpy** (implements the three-step identification procedure including MS2 spectral similarity scoring as the final confirmation step) — https://github.com/leopold-weidner/DBDIpy
- **matchms** (provides spectral matching algorithms and is integrated into DBDIpy's workflow for spectral preprocessing and similarity calculation) — https://github.com/matchms/matchms
- **Python** (execution environment for DBDIpy library and cosine similarity / spectral matching implementations)

## Examples

```
search_res = dbdi.identify_adducts(df=specs_imputed, masses=feature_mz, custom_adducts=adduct_rule, method='pearson', threshold=0.9, mass_error=2)
```

## Evaluation signals

- All candidate pairs receive a numerical spectral similarity score in the valid range [0, 1] or similar bounded metric
- Pairs exceeding the acceptance threshold (e.g., ≥0.9) are consistently flagged as confirmed; pairs below threshold are marked as unconfirmed
- Output table contains no null or missing similarity scores for pairs that have valid MS2 data
- Confirmed pairs show strong visual overlap when their fragment spectra are plotted or aligned (qualitative sanity check)
- Similarity scores for true biological adducts/fragments are significantly higher than scores for random peak pairs from the same dataset

## Limitations

- MS2 spectral similarity scoring requires high-quality, complete MS2 data; sparse or noisy fragmentation patterns reduce confidence in similarity scores
- Threshold selection (e.g., 0.9 for Pearson correlation) is user-dependent and may require empirical tuning based on instrument type, ionization method, and dataset characteristics
- Spectral similarity alone cannot distinguish between true analyte fragments and coincidental spectral overlap; it must be applied after correlation and mass accuracy filtering for reliable confirmation
- Performance depends on preprocessing steps (normalization, noise removal); suboptimal upstream preprocessing degrades downstream similarity calculations

## Evidence

- [other] DBDIpy implements a three-step identification procedure in which MS2 spectral similarity scoring is the final step, following pointwise correlation analysis of temporal intensity profiles and exact mass difference refinement, to confirm shared analyte origin of candidate ion pairs.: "MS2 spectral similarity scoring is the final step, following pointwise correlation analysis of temporal intensity profiles and exact mass difference refinement, to confirm shared analyte origin"
- [other] For each candidate pair, extract and preprocess the corresponding MS2 fragment spectra (normalize intensity, remove noise). Calculate MS2 spectral similarity score using cosine similarity or related spectral matching algorithm between fragment profiles.: "extract and preprocess the corresponding MS2 fragment spectra (normalize intensity, remove noise). Calculate MS2 spectral similarity score using cosine similarity or related spectral matching"
- [readme] The identification is performed in a three-step procedure (from V > 2.* on, in preparation): calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment. (exact) mass differences are used to refine the nature of potential candidates. calculation of MS2 spectral similarity score by ...: "The identification is performed in a three-step procedure: calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment. (exact) mass"
- [other] Annotate each pair with its similarity score and flag pairs exceeding the acceptance threshold as confirmed shared-analyte relationships. Generate output table mapping candidate pairs to their spectral similarity scores and confirmation status.: "flag pairs exceeding the acceptance threshold as confirmed shared-analyte relationships. Generate output table mapping candidate pairs to their spectral similarity scores and confirmation status"
- [readme] major implementation for V2: modification of the former two-step search algorithm towards refinement by MS2 spectral similarity scoring.: "major implementation for V2: modification of the former two-step search algorithm towards refinement by MS2 spectral similarity scoring"
