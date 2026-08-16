---
name: in-source-fragment-adduct-candidate-flagging
description: Use when you have aligned, imputed time-resolved mass spectrometric data
  from direct-injection plasma ionization (e.g., DBDI, DESI) without chromatographic
  separation, and you suspect multiple m/z features belong to the same neutral analyte
  as in-source fragments or oxygen-bound adducts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
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
  - MS-imaging
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btad088/7036334
  title: DBDIpy
evidence_spans:
- DBDIpy is an open-source Python library for the curation and interpretation of dielectric
  barrier discharge ionisation mass spectrometric datasets
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

# in-source-fragment-adduct-candidate-flagging

## Summary

Identifies co-eluting ion pairs arising from in-source fragmentation or adduct formation in time-resolved plasma ionization mass spectrometry by computing pointwise correlation of extracted ion chromatograms (XIC) and filtering on correlation threshold and exact mass difference. This is the first step in DBDIpy's three-step putative identification workflow for direct-injection MS datasets.

## When to use

Apply this skill when you have aligned, imputed time-resolved mass spectrometric data from direct-injection plasma ionization (e.g., DBDI, DESI) without chromatographic separation, and you suspect multiple m/z features belong to the same neutral analyte as in-source fragments or oxygen-bound adducts. The input must be a 2D feature table with rows as aligned m/z features and columns as sequential time points or scans.

## When NOT to use

- Input is chromatographically separated (LC–MS or GC–MS) data: this skill targets direct-injection time-resolved datasets where temporal co-elution is meaningful; chromatographic separation breaks the temporal matching assumption.
- Feature table contains missing values (NaN): imputation must precede this skill; Pearson correlation cannot handle gaps.
- Single scan or static mass spectrum (no time dimension): pointwise correlation requires ≥2 time points per feature; bulk MS1 spectra without temporal resolution are not suitable.

## Inputs

- Imputed time-resolved intensity matrix (pandas DataFrame or numpy array; features as rows, time points/scans as columns, no NaN values)
- Feature m/z values (1D array or pandas Series, one per feature)
- User-defined adduct/fragment rules (pandas DataFrame with columns: deltamz, motive; e.g., [M+O+H], [M+2O+H], [M−H₂O+H])

## Outputs

- Correlation matrix (symmetric 2D array of Pearson r values, features × features)
- Flagged candidate pairs table (DataFrame with columns: base_mz, base_index, match_mz, match_index, mzdiff, corr, adduct_type)
- Per-adduct result dictionaries (one DataFrame per adduct species, indexed by row)
- Structured output file(s) with candidate assignments and correlation scores

## How to apply

Load the imputed intensity matrix (features × time points) and associated m/z values. Normalize or standardize the intensity profile for each feature to remove absolute intensity bias. Compute Pearson correlation coefficients between all pairwise feature temporal profiles using scipy.stats.pearsonr or numpy.corrcoef, generating a full symmetric correlation matrix. Filter the matrix to retain only feature pairs exceeding a user-defined correlation threshold (default r > 0.90–0.95) as candidates with matching temporal dynamics. For each flagged pair, calculate the exact m/z difference and cross-reference against known adduct mass shifts (e.g., [M+O+H]+ = +15.99491 Da, [M+2O+H]+ = +31.98983 Da, [M−H₂O+H]+ = +18.01057 Da) to assign putative adduct or fragment identity. Export results as a structured table mapping base m/z, matched m/z, correlation score, m/z difference, and assigned adduct type.

## Related tools

- **DBDIpy** (Primary Python library providing align_spectra(), impute_intensities(), identify_adducts() functions and correlation-based adduct detection pipeline) — https://github.com/leopold-weidner/DBDIpy
- **scipy.stats.pearsonr** (Pairwise Pearson correlation coefficient calculation between XIC temporal profiles)
- **numpy.corrcoef** (Vectorized full correlation matrix computation across all feature pairs)
- **pandas** (DataFrame manipulation and structured output export of flagged pairs and results)
- **matchms** (Upstream spectral I/O and preprocessing (load_from_mgf, spectrum alignment, preprocessing pipelines)) — https://github.com/matchms/matchms

## Examples

```
search_res = dbdi.identify_adducts(df=specs_imputed, masses=feature_mz, custom_adducts=adduct_rule, method='pearson', threshold=0.9, mass_error=2)
```

## Evaluation signals

- Correlation matrix is symmetric and square (n_features × n_features) with diagonal = 1.0
- All retained candidate pairs have |r| ≥ specified threshold (e.g., r > 0.90); pairs below threshold are absent from output
- Exact m/z differences between base and match features match expected adduct mass shifts within stated mass error tolerance (typically ±2 ppm for high-resolution MS)
- Flagged pairs are bidirectional: if (feature_i, feature_j) is flagged with r=0.95, then (feature_j, feature_i) also appears with same r value and reversed m/z assignment
- Output DataFrame has no missing values in correlation, m/z, or adduct assignment columns; spot-check 5–10 pairs manually against reference adduct tables or literature

## Limitations

- Correlation-based matching requires temporal intensity profiles to be present and interpretable; features with low signal-to-noise or sparse temporal sampling may produce spurious correlations.
- Pointwise correlation does not distinguish between true adducts/fragments and unrelated features with coincidentally matching temporal patterns; mass difference filtering is essential but not always sufficient (confirmed by downstream MS/MS similarity scoring in DBDIpy v2+).
- Threshold selection (e.g., r > 0.90) is user-dependent and dataset-sensitive; no automated threshold recommendation is provided. Threshold choice directly affects sensitivity/specificity trade-off.
- Does not account for multiple adducts of the same neutral species (e.g., [M+O+H]+ and [M+2O+H]+ arising from one analyte); these appear as separate pairs and must be post-processed to group into a single molecular family.
- Assumes linear imputation or baseline-filling preserves temporal dynamics reasonably; heavy imputation in sparse regions may inflate false correlations.

## Evidence

- [intro] calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment: "calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment"
- [readme] The identification is performed in a three-step procedure: - calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment. - (exact) mass differences are used to refine the nature of potential candidates.: "The identification is performed in a three-step procedure (from V > 2.* on, in preparation): 
- calculation of pointwise correlation identifies features with matching temporal intensity profiles"
- [other] Compute Pearson correlation coefficients between all pairs of feature temporal profiles using scipy.stats.pearsonr or numpy.corrcoef to generate a full correlation matrix. Filter the correlation matrix to identify feature pairs exceeding a correlation threshold (e.g., r > 0.95) as candidates with matching temporal dynamics.: "Compute Pearson correlation coefficients between all pairs of feature temporal profiles using scipy.stats.pearsonr or numpy.corrcoef to generate a full correlation matrix. Filter the correlation"
- [readme] impute_intensities() will assure that after imputation we will have a set of uniform length extracted ion chromatograms (XIC) in our DataFrame. This is an important prerequisite for pointwise correlation calculation: "impute_intensities() will assure that after imputation we will have a set of uniform length extracted ion chromatograms (XIC) in our DataFrame. This is an important prerequisite for pointwise"
- [readme] By default, identify_adducts() searches for [M−H₂O+H]+, [M+1O+H]+ and [M+2O+H]+. For demonstrational purposes we also want to search for [M+3O+H]+ in this example. Note that identify_adducts() has a variety of other parameters which allow high user customization.: "By default, ``identify_adducts()`` searches for [M-H<sub>2</sub>O+H]<sup>+</sup>, [M+1O+H]<sup>+</sup> and [M+2O+H]<sup>+</sup>. For demonstrational purposes we also want to search for"
- [readme] Mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts generated during the ionization process.: "Mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts"
