---
name: mass-spectrometry-feature-intensity-normalization
description: Use when after aligning raw mass spectra into a 2D feature intensity matrix (features × time points) but before computing pointwise correlation to identify feature pairs with matching temporal profiles.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DBDIpy
  - Python
  - pandas
  - scikit-learn
  - scipy.stats
  techniques:
  - mass-spectrometry
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-feature-intensity-normalization

## Summary

Standardize extracted ion chromatogram (XIC) intensity profiles across mass spectrometric features to remove absolute intensity differences before correlation analysis. This preprocessing step ensures that temporal dynamics rather than signal magnitude drive the identification of co-eluting adducts and in-source fragments in time-resolved DBDI-MS datasets.

## When to use

Apply this skill after aligning raw mass spectra into a 2D feature intensity matrix (features × time points) but before computing pointwise correlation to identify feature pairs with matching temporal profiles. Use it whenever features have widely varying absolute intensities but may share the same temporal dynamics—a common scenario in direct injection mass spectrometry where ionization efficiency and detector response vary across m/z values.

## When NOT to use

- Input is already a correlation or distance matrix (not raw intensities).
- Absolute intensity magnitude is a discriminative feature (e.g., abundance-based filtering or quantification is required after correlation).
- Features have zero or near-zero variance across time points (normalization will fail or produce NaN values).

## Inputs

- pandas.DataFrame: aligned and imputed feature intensity matrix (rows=features, columns=time points/scans)
- Optionally: m/z values for features (used for labeling output)

## Outputs

- pandas.DataFrame: normalized feature intensity matrix with same shape as input, standardized intensity values
- Normalization metadata: mean and standard deviation (or min/max) per feature, stored for optional denormalization

## How to apply

Load the aligned intensity matrix as a pandas DataFrame with features as rows and time points (scans) as columns. For each feature row, apply a standardization method (e.g., z-score normalization or min-max scaling) to remove absolute intensity differences while preserving temporal shape. The choice of normalization method affects downstream correlation sensitivity: z-score normalization centers each XIC and scales by its standard deviation, making temporal correlation robust to baseline shifts and amplitude variations. After normalization, verify that all XIC profiles have comparable dynamic ranges (typically 0–1 or mean=0, std=1 depending on method) before passing the normalized matrix to pointwise correlation calculation using Pearson correlation coefficients or equivalent metrics.

## Related tools

- **DBDIpy** (Provides impute_intensities() and identify_adducts() functions that accept normalized feature matrices and perform downstream correlation-based adduct detection.) — https://github.com/leopold-weidner/DBDIpy
- **pandas** (DataFrame manipulation and row-wise normalization operations.)
- **scikit-learn** (StandardScaler or MinMaxScaler for vectorized normalization of feature intensities.)
- **scipy.stats** (Manual z-score computation or alternative statistical normalization methods.)

## Examples

```
specs_aligned = specs_aligned.drop('mean', axis=1); specs_imputed = dbdi.impute_intensities(df=specs_aligned, method='linear'); specs_normalized = (specs_imputed - specs_imputed.mean(axis=1).values.reshape(-1, 1)) / specs_imputed.std(axis=1).values.reshape(-1, 1)
```

## Evaluation signals

- After normalization, each feature's intensity profile has zero mean and unit variance (z-score) or is bounded to [0, 1] (min-max), with no NaN or Inf values.
- Pointwise Pearson correlation coefficients between features with similar temporal dynamics remain high (e.g., r > 0.9) after normalization, demonstrating that temporal shape is preserved while absolute magnitude is removed.
- Downstream correlation-based adduct detection (using identify_adducts()) reports candidate pairs with mass differences matching known adduct rules (e.g., Δm/z ≈ 16 for [M+O+H]⁺) at expected correlation thresholds (default 0.9).
- Comparison of correlation matrices computed before and after normalization shows stronger clustering of true co-eluting features and reduced false positives caused by intensity magnitude differences alone.

## Limitations

- Normalization cannot recover temporal information from features with zero variance (constant intensity); such features should be filtered before normalization.
- Choice of normalization method (z-score vs. min-max vs. others) affects sensitivity to outlier time points; z-score is more robust to extreme values, while min-max preserves relative magnitude within each feature.
- Normalization assumes features are independent; highly correlated features with vastly different absolute intensities may still appear dissimilar after normalization if their temporal profiles differ even slightly.
- README does not explicitly specify which normalization method is used by default in DBDIpy; user must verify or apply custom normalization before calling identify_adducts().

## Evidence

- [other] Normalize or standardize intensity profiles for each feature to account for absolute intensity differences.: "Normalize or standardize intensity profiles for each feature to account for absolute intensity differences."
- [readme] Missing values within the detected signal region are interpolated in between. Second, a noisy baseline is generated for all XIC to be of uniform length.: "Missing values within the detected signal region are interpolated in between. Second, a noisy baseline is generated for all XIC to be of uniform length"
- [readme] calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment.: "calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment."
- [readme] By aplication of ``align_spectra()``, we transformed the list of spectra objects to a two-dimensional ``pandas.DataFrame``. Now you have a column for each mass spectrometric scan and features are aligned to rows.: "By aplication of ``align_spectra()``, we transformed the list of spectra objects to a two-dimensional ``pandas.DataFrame``. Now you have a column for each mass spectrometric scan and features are"
