---
name: metabolomics-feature-matrix-processing
description: Use when you have a raw metabolomics intensity matrix with missing or zero values across samples in different experimental groups, and you need to input it into pathway activity scoring methods (PLAGE, ORA, GSEA) or metabolite set analysis pipelines that require normalized, zero-mean unit-variance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - PALS Viewer
  - GNPS
  - MS2LDA
  - PALS (Pathway Activity Level Scoring)
  - SciPy preprocessing module
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans:
- To access our interactive Web application PALS Viewer, please visit [https://pals.glasgowcompbio.org/app/]
- Molecular Families from GNPS
- This includes in particular *Molecular Families* from [GNPS](http://gnps.ucsd.edu/)
- Mass2Motifs from MS2LDA
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

# metabolomics-feature-matrix-processing

## Summary

Prepare and preprocess a metabolomics peak intensity matrix for pathway analysis by applying data imputation, log₂ transformation, and standardization to handle missing values and normalize intensity distributions across samples.

## When to use

You have a raw metabolomics intensity matrix with missing or zero values across samples in different experimental groups, and you need to input it into pathway activity scoring methods (PLAGE, ORA, GSEA) or metabolite set analysis pipelines that require normalized, zero-mean unit-variance data.

## When NOT to use

- Input intensity matrix is already log-transformed or standardized from a prior analysis step
- Peak features lack metabolite annotations (they will be excluded and provide no downstream signal)
- The analysis goal does not require sample-group comparisons (i.e., single-condition designs without case/control structure)

## Inputs

- Peak intensity matrix (CSV): rows are peak features with column 1 as peak_id, subsequent columns are sample intensities; optional row 2 contains group assignments
- Metabolite annotation matrix (CSV): two columns (peak_id, entity_id where entity_id is KEGG or ChEBI identifier)

## Outputs

- Preprocessed intensity DataFrame: log₂-transformed, imputed, standardized (zero mean, unit variance) with dimensions matching input
- Experimental design dictionary: structured groups and comparisons extracted from sample metadata

## How to apply

Load the intensity matrix where rows are peak features (with the first column as peak ID) and columns are individual samples, with optional group assignments on the second line. Apply data imputation: replace all-zero intensities within a sample group with a user-defined minimum intensity threshold (default 5000); replace partial-zero values within a group with the mean of non-zero samples in that group. Next, log₂-transform all intensities to stabilize variance across the intensity range. Finally, standardize the matrix using z-score normalization (zero mean, unit variance) across all samples using scipy.preprocessing. This pipeline ensures robust downstream decomposition by reducing the influence of noise and missing peaks, which are prevalent in metabolomics data.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Downstream consumer of preprocessed intensity matrix for pathway ranking via PLAGE, ORA, or GSEA decomposition methods) — https://github.com/glasgowcompbio/PALS
- **SciPy preprocessing module** (Performs standardization (z-score normalization) to achieve zero mean and unit variance across samples)

## Examples

```
```python
import pandas as pd
from scipy import preprocessing

int_df = pd.read_csv('intensity.csv', index_col=0)
group_row = int_df.iloc[0]
int_df = int_df.iloc[1:].astype(float)

# Imputation per group
for group in set(group_row):
    cols = group_row[group_row == group].index
    all_zero = (int_df[cols] == 0).all(axis=1)
    int_df.loc[all_zero, cols] = 5000
    partial_zero = ((int_df[cols] == 0).sum(axis=1) > 0) & ~all_zero
    int_df.loc[partial_zero, cols] = int_df.loc[partial_zero, cols].replace(0, int_df.loc[partial_zero, cols].mean(axis=1, skipna=True))

# Log₂ transform and standardize
int_df = np.log2(int_df + 1)
int_df = pd.DataFrame(preprocessing.StandardScaler().fit_transform(int_df), index=int_df.index, columns=int_df.columns)
```
```

## Evaluation signals

- Verify no missing values remain: all NaN or inf entries should be replaced; check that output matrix has full rank
- Confirm standardization applied correctly: compute mean and standard deviation across all samples in output matrix; mean should be ≈ 0, std ≈ 1 (within floating-point tolerance)
- Validate log₂ transformation: spot-check that intensity values are smaller in magnitude after transformation (e.g., original intensity 2000 becomes ~10.97)
- Check imputation logic: verify that features with all-zero values in a group were replaced with min_replace value; verify partial zeros were replaced with group mean
- Confirm row/column alignment: output matrix dimensions and peak_id order match input; ensure annotation mapping preserves peak IDs

## Limitations

- Imputation using mean or minimum threshold can artificially inflate or deflate activity scores if missingness is informative (e.g., non-random dropout correlated with experimental condition)
- Log₂ transformation assumes all intensity values are positive; zero or negative values will produce NaN or undefined results
- Standardization assumes intensity distributions are approximately normal after log transformation; highly skewed or multimodal distributions may remain poorly scaled
- Loss of information: peaks without metabolite annotations are discarded before pathway analysis, potentially losing signal from unannotated but biologically relevant features

## Evidence

- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor.: "Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity"
- [readme] The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples."
- [intro] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are"
- [readme] As a result of the uncertainty in peak identification, multiple peak IDs may be mapped to multiple compound IDs and vice versa.: "As a result of the uncertainty in peak identification, multiple peak IDs may be mapped to multiple compound IDs and vice versa."
