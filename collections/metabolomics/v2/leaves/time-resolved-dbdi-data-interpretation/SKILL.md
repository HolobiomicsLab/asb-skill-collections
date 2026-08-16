---
name: time-resolved-dbdi-data-interpretation
description: Use when you have time-resolved DBDI-MS data (intensity matrix with m/z
  features as rows and scan timepoints as columns) from direct injection analysis
  where chromatographic separation is unavailable and you need to identify which features
  represent fragments or adducts of the same parent compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DBDIpy
  - Python
  - matchms
  - scipy.stats.pearsonr
  - pandas
  techniques:
  - LC-MS
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

# time-resolved-dbdi-data-interpretation

## Summary

Identify in-source fragments and adducts in direct-injection dielectric barrier discharge ionisation (DBDI) mass spectrometry by combining pointwise correlation of temporal intensity profiles with exact mass difference refinement. This skill enables putative annotation of multiple ion species arising from single analytes in time-resolved plasma ionization datasets where chromatographic separation is absent.

## When to use

Apply this skill when you have time-resolved DBDI-MS data (intensity matrix with m/z features as rows and scan timepoints as columns) from direct injection analysis where chromatographic separation is unavailable and you need to identify which features represent fragments or adducts of the same parent compound rather than independent analytes.

## When NOT to use

- Input data already contain chromatographic separation—use conventional metabolomics workflows instead; correlation-based co-elution is redundant when retention time already disambiguates features.
- Feature table is not time-resolved (e.g., single static MS spectra or already aggregated across time)—pointwise correlation requires temporal dynamics.
- Individual features have < 3 time points—correlation estimation becomes unreliable with very short XIC traces.

## Inputs

- Raw mass spectrometry data files (.mgf, .mzML, .mzXML formats)
- Aligned feature intensity matrix (pandas DataFrame): rows = m/z features, columns = time points/scans, first column = mean m/z
- Time-resolved DBDI dataset with or without missing values
- Optional: custom adduct definitions (delta m/z values and motives)

## Outputs

- Dictionary of DataFrames, one per adduct type, containing: base_mz, base_index, match_mz, match_index, mzdiff (observed mass difference), and corr (Pearson correlation coefficient)
- Filtered feature pair list with correlation scores exceeding threshold
- Imputed feature intensity matrix (no missing values)

## How to apply

Load and align raw MS data (in .mgf, .mzML, or .mzXML format) into a 2D feature table using the align_spectra() function with a ppm_window matching your instrument resolution. Impute missing values across all extracted ion chromatograms (XIC) using linear interpolation followed by baseline generation to ensure uniform length traces. Compute Pearson correlation coefficients between all feature pairs' temporal intensity profiles, filtering pairs exceeding a correlation threshold (typically r > 0.9) as candidates for co-elution. Refine candidates by checking whether observed m/z differences match known adduct mass shifts (e.g., Δm/z ≈ 15.99 for [M+O+H]⁺, 31.99 for [M+2O+H]⁺, or 18.01 for [M+H₂O+H]⁺). Return matched feature pairs with correlation scores and mass differences as structured output for further validation.

## Related tools

- **DBDIpy** (Primary library for alignment, imputation, pointwise correlation, mass difference refinement, and adduct/fragment identification in DBDI datasets) — https://github.com/leopold-weidner/DBDIpy
- **matchms** (Spectral I/O and preprocessing backend for loading and filtering raw mass spectra before feature alignment) — https://github.com/matchms/matchms
- **scipy.stats.pearsonr** (Computation of Pearson correlation coefficients between feature temporal profiles)
- **pandas** (Data structure (DataFrame) for storing and manipulating aligned feature intensity matrices)

## Examples

```
import DBDIpy as dbdi
import pandas as pd
from matchms.importing import load_from_mgf
spectrums = list(load_from_mgf('example_dataset.mgf'))
specs_aligned = dbdi.align_spectra(spec=spectrums, ppm_window=2)
specs_imputed = dbdi.impute_intensities(df=specs_aligned.drop('mean', axis=1), method='linear')
search_res = dbdi.identify_adducts(df=specs_imputed, masses=specs_aligned['mean'], method='pearson', threshold=0.9, mass_error=2)
```

## Evaluation signals

- Imputed feature table contains no NaN values and all XIC traces are uniform length (checked via df.isnull().values.any() → False)
- Correlation matrix is symmetric (r[i,j] = r[j,i]) and diagonal values = 1.0
- All feature pairs returned as matches have correlation ≥ specified threshold (default r ≥ 0.9); no false negatives within margin
- Observed m/z differences (mzdiff column) fall within ±mass_error ppm of expected adduct Δm/z values (e.g., 15.99 ± 0.02 for [M+O+H]⁺ with 2 ppm tolerance)
- Returned base_mz and match_mz values appear in original input feature list with correct indices

## Limitations

- Pointwise correlation assumes no chromatographic separation; performance degrades if co-eluting features with unrelated temporal profiles are abundant.
- Imputation method (linear interpolation + baseline generation) may introduce artifacts in regions with large intensity gaps; edge-case sensitivity not thoroughly characterized.
- Threshold selection (correlation cutoff r, mass_error in ppm) is user-dependent; no adaptive threshold recommendation provided in DBDIpy.
- MS1-only workflow cannot distinguish isomeric adducts or fragments with identical m/z and temporal profiles; MS2 spectral similarity refinement is planned for Version 2.* but workflow incomplete in README.
- Dataset demonstrated on 500 randomly selected features; scalability and runtime on full-scale (10k+ feature) datasets not reported.

## Evidence

- [readme] Mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts generated during the ionization process: "Mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts"
- [readme] DBDIpy's core functionality relies on putative identification of in-source fragments and adducts via a three-step procedure: pointwise correlation, mass difference refinement, and MS2 spectral similarity scoring: "DBDIpy's core functionality relys on putative identification of in-source fragments (eg. [M-H2O+H]+) and in-source generated adducts (eg. [M+nO+H]+)"
- [readme] Imputation ensures all extracted ion chromatograms (XIC) are of uniform length, a prerequisite for pointwise correlation calculation: "impute_intensities() will assure that after imputation we will have a set of uniform length extracted ion chromatograms (XIC) in our DataFrame. This is an important prerequisite for pointwise"
- [readme] Pointwise correlation identifies feature groups with matching temporal intensity profiles; mass differences refine the nature of candidates: "calculation of pointwise intensity correlation identifies feature groups with matching temporal intensity profiles through the experiment. Second, (exact) mass differences are used to refine the"
- [readme] The identify_adducts() function returns a dictionary with one DataFrame per adduct type, containing base m/z, match m/z, m/z difference, and correlation score: "The function will return a dictionary holding one DataFrame for each adduct type that was defined. A typical output looks like the following: 'O':   base_mz    base_index  match_mz  match_index"
- [readme] Alignment is performed via align_spectra() with user-defined ppm_window parameter matched to mass spectrometer resolution: "Remember to set the ``ppm_window`` parameter according to the resolution of you mass spectrometric system."
