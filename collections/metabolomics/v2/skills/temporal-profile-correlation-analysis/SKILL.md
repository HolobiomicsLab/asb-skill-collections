---
name: temporal-profile-correlation-analysis
description: Use when you have time-resolved direct injection mass spectrometry data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DBDIpy
  - Python
  - scipy.stats.pearsonr
  - numpy.corrcoef
  - pandas
  - matchms
  techniques:
  - LC-MS
  - GC-MS
  - tandem-MS
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

# temporal-profile-correlation-analysis

## Summary

Identifies co-eluting feature pairs in time-resolved mass spectrometric datasets by computing Pearson correlation coefficients across all feature temporal intensity profiles. This workflow detects in-source fragments and adducts that share matching dynamics through the experiment, a core step in DBDIpy's adduct and fragment identification pipeline for direct injection plasma ionization techniques.

## When to use

Apply this skill when you have time-resolved direct injection mass spectrometry data (e.g., DBDI-MS or breath analysis) where chromatographic separation is absent or minimal, and you need to discover which m/z features co-vary temporally — indicating they may arise from a single parent analyte or be related in-source transformation products. Use it as the first filtering step before refining candidates by exact mass differences.

## When NOT to use

- Input data contains missing values (NaN) or unequal XIC lengths — imputation must be completed first
- Feature table is already pre-filtered to single compound classes or has undergone prior adduct removal — you would lose the discovery aspect
- Mass spectrometric data includes chromatographic separation (LC-MS or GC-MS) — temporal co-variance may reflect co-elution rather than in-source relationships

## Inputs

- Aligned feature intensity matrix (pandas DataFrame or 2D numpy array): features × time points, with intensity values and optional m/z column
- Time-resolved direct injection mass spectrometry dataset (e.g., .mgf, .mzML, .mzXML after preprocessing and alignment)
- Imputed intensity table with no missing values (NaN)

## Outputs

- Full Pearson correlation coefficient matrix (features × features)
- Filtered list of co-correlated feature pairs with correlation scores and indices
- Structured output file (CSV/DataFrame) of candidate pairs for downstream mass-difference refinement

## How to apply

Load your aligned and imputed feature intensity matrix (features as rows, time points as columns) into a standardized numerical table. Normalize or standardize each feature's temporal profile to account for absolute intensity differences. Compute Pearson correlation coefficients between all pairs of feature profiles using scipy.stats.pearsonr or numpy.corrcoef to generate a full correlation matrix. Filter the resulting matrix to flag feature pairs exceeding a user-defined correlation threshold (default r > 0.9–0.95 as reported in DBDIpy documentation). The threshold choice depends on your sensitivity–specificity tradeoff: higher thresholds reduce false positives but may miss genuine weak correlations. Export the filtered correlation matrix and paired feature list with correlation scores for downstream mass-difference refinement.

## Related tools

- **DBDIpy** (Python library integrating pointwise correlation calculation, imputation, and adduct/fragment identification workflow; provides identify_adducts() and impute_intensities() functions) — https://github.com/leopold-weidner/DBDIpy
- **scipy.stats.pearsonr** (Computes Pearson correlation coefficient and p-value for pairs of feature temporal profiles)
- **numpy.corrcoef** (Generates full correlation matrix for all feature pairs in a single call)
- **pandas** (Handles aligned feature intensity matrices and structured output export)
- **matchms** (Imports and preprocesses raw MS spectra (.mgf, .mzML, .mzXML) prior to alignment and correlation analysis; integrated into DBDIpy workflow) — https://github.com/matchms/matchms

## Examples

```
search_res = dbdi.identify_adducts(df = specs_imputed, masses = feature_mz, method = "pearson", threshold = 0.9, mass_error = 2)
```

## Evaluation signals

- Correlation matrix is symmetric and square (features × features); diagonal values all equal 1.0
- All correlation coefficients fall within [−1, 1]; no NaN or inf values in output
- Number of flagged pairs below the threshold is reasonable relative to total possible pairs (e.g., < 10–20% for r > 0.9 on typical datasets)
- Filtered candidate pairs include known or plausible adduct relationships (e.g., M+O vs M, mass difference ≈ 15.99 Da) when compared against subsequent mass-difference refinement results
- XIC profiles of highly correlated pairs (r > 0.95) are visually synchronous when plotted; peak maxima and decay rates align across time points

## Limitations

- Pearson correlation assumes linear relationships; non-linear temporal co-variation (e.g., biphasic dynamics) may yield low scores despite chemical relatedness
- Threshold choice (e.g., r > 0.9 vs r > 0.95) is user-dependent and affects sensitivity; no single optimal value is universally applicable across different ionization conditions or sample types
- Correlation alone cannot distinguish in-source fragments from genuine co-eluting contaminants or unrelated overlapping species; mass-difference and MS/MS spectral similarity refinement steps are essential
- Missing data handling via interpolation or baseline imputation may artificially inflate correlations between sparse features; imputation method choice (linear, forward-fill, etc.) impacts downstream results
- High correlation can arise from shared instrumental artifacts or noise patterns; visual inspection and chemical plausibility checks are recommended before assigning adduct relationships

## Evidence

- [readme] calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment: "calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment"
- [other] Compute Pearson correlation coefficients between all pairs of feature temporal profiles using scipy.stats.pearsonr or numpy.corrcoef to generate a full correlation matrix: "Compute Pearson correlation coefficients between all pairs of feature temporal profiles using scipy.stats.pearsonr or numpy.corrcoef to generate a full correlation matrix"
- [other] Filter the correlation matrix to identify feature pairs exceeding a correlation threshold (e.g., r > 0.95) as candidates with matching temporal dynamics: "Filter the correlation matrix to identify feature pairs exceeding a correlation threshold (e.g., r > 0.95) as candidates with matching temporal dynamics"
- [readme] impute_intensities() will assure that after imputation we will have a set of uniform length extracted ion chromatograms (XIC) in our DataFrame. This is an important prerequisite for pointwise correlation calculation: "impute_intensities() will assure that after imputation we will have a set of uniform length extracted ion chromatograms (XIC) in our DataFrame. This is an important prerequisite for pointwise"
- [readme] calculation of pointwise intensity correlation identifies feature groups with matching temporal intensity profiles through the experiment: "calculation of pointwise intensity correlation identifies feature groups with matching temporal intensity profiles through the experiment"
- [readme] identify_adducts() searches for [M-H₂O+H]⁺, [M+1O+H]⁺ and [M+2O+H]⁺. For demonstrational purposes we also want to search for [M+3O+H]⁺: "identify_adducts() searches for [M-H₂O+H]⁺, [M+1O+H]⁺ and [M+2O+H]⁺. For demonstrational purposes we also want to search for [M+3O+H]⁺"
