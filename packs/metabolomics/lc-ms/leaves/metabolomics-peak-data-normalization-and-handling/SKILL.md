---
name: metabolomics-peak-data-normalization-and-handling
description: Use when when you have raw peak intensity matrices from metabolomics LC-MS/MS experiments with zero values (missing peaks or undetected compounds) and need to prepare data for pathway-level analysis using PLAGE, ORA, or GSEA.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - PALS (Pathway Activity Level Scoring)
  - Scipy preprocessing module
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pals_cq
    doi: 10.3390/metabo11020103
    title: pals
  dedup_kept_from: coll_pals_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11020103
  all_source_dois:
  - 10.3390/metabo11020103
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-peak-data-normalization-and-handling

## Summary

Standardize metabolomics peak intensity matrices through log-2 transformation and z-score normalization to enable robust pathway activity scoring. This preprocessing step is essential for metabolomics data because it addresses missing values, scales intensities across samples, and prepares data for decomposition-based pathway analysis methods like PLAGE.

## When to use

When you have raw peak intensity matrices from metabolomics LC-MS/MS experiments with zero values (missing peaks or undetected compounds) and need to prepare data for pathway-level analysis using PLAGE, ORA, or GSEA. Apply this skill before computing pathway activity scores, especially if your data exhibits high noise or missing peak rates (5–20%), which are prevalent in metabolomics and would otherwise bias downstream comparisons.

## When NOT to use

- Data is already quantile-normalized or batch-corrected by external tools (e.g., limma, ComBat); re-normalizing may introduce bias.
- Peak intensities are already log-transformed and z-scored by the mass spectrometry processing pipeline.
- The experimental design has nested or paired factors where group-level imputation is inappropriate; use custom imputation strategies instead.

## Inputs

- Peak intensity CSV matrix (rows = peaks, columns = samples, first column = peak ID)
- Annotation CSV matrix (peak ID, entity_id [KEGG/ChEBI compound ID])
- Experimental design specification (sample-to-group assignments)

## Outputs

- Normalized log-2 z-score intensity matrix (zero mean, unit variance across samples)
- Imputed missing value indicator (optional, for tracking replaced zeros)
- Preprocessed data structure ready for pathway decomposition (PLAGE/ORA/GSEA input)

## How to apply

Load the peak intensity matrix (rows = peaks with column 1 = peak ID, remaining columns = sample intensities) and annotation matrix (peak ID → KEGG/ChEBI compound ID). Apply data imputation: if all samples in a single experimental factor have zero intensity, replace with a user-defined minimum (default 5000); if only some samples in a factor are zero, replace with the mean of non-zero samples in that factor. This preserves group structure while avoiding log(0). Then apply log-2 transformation to the entire imputed matrix and z-score standardize across all samples (zero mean, unit variance) using scipy preprocessing. This normalization stabilizes variance across intensity ranges and makes the data amenable to SVD-based decomposition methods. Validate that the output matrix has no NaN or Inf values and that column means are approximately zero.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Executes normalization as a preprocessing step before PLAGE decomposition or ORA/GSEA ranking) — https://github.com/glasgowcompbio/PALS
- **Scipy preprocessing module** (Provides StandardScaler for z-score normalization and standardization functions)

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control --min_replace 5000
```

## Evaluation signals

- Output matrix has zero column mean (±1e-10 tolerance) and unit column variance for all samples.
- No NaN, Inf, or -Inf values present in the normalized matrix after transformation.
- Imputed zeros are documented; verify that group-wise means of non-imputed values are preserved before and after log transformation.
- Comparison of pathway activity scores (Spearman correlation) between baseline and 5% Gaussian noise-perturbed data shows ≥0.85 correlation for PLAGE (metric of normalization robustness).
- Intensity ranges span multiple orders of magnitude in the log-2 domain (typically 0–20 range for LC-MS intensities) without extreme outliers (>3 σ from mean after z-scoring).

## Limitations

- Zero replacement strategy assumes missing peaks are missing at random (MAR) within experimental factors; non-random missingness may bias results.
- Group-level imputation requires correct experimental design specification; misassigned samples will propagate incorrect mean values.
- Log-2 transformation assumes all intensities are positive; negative or zero imputation values will produce undefined logarithms.
- Z-score normalization assumes roughly symmetric or light-tailed intensity distributions; extreme skewness or multimodal distributions may require alternative transformations (e.g., rank-based).
- The method is sensitive to outlier samples; anomalous samples with extreme intensities will inflate standard deviations and compress other samples.

## Evidence

- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor.: "Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity"
- [readme] The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples."
- [intro] PALS results demonstrate greater robustness to noise and missing peaks compared to ORA and GSEA, which is particularly important for metabolomics peak data where noise and missing peaks are prevalent.: "PALS results demonstrate greater robustness to noise and missing peaks compared to ORA and GSEA, which is particularly important for metabolomics peak data where noise and missing peaks are prevalent."
- [readme] --min_replace: The minimum intensity value for data imputation, e.g. `--min_replace 5000`. Defaults to 5000.: "--min_replace: The minimum intensity value for data imputation, e.g. `--min_replace 5000`. Defaults to 5000."
