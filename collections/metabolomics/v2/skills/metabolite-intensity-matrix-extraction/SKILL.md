---
name: metabolite-intensity-matrix-extraction
description: Use when when you have raw mass spectrometry peak intensity data (rows = peaks with IDs, columns = individual samples) and you need to align it with metabolite annotations (peak ID → KEGG or ChEBI compound ID mappings) before performing pathway-level analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - PALS
  - scipy.preprocessing
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-intensity-matrix-extraction

## Summary

Extract and preprocess a sample-by-metabolite intensity matrix from mass spectrometry peak data, performing data imputation, log-2 transformation, and standardization to prepare input for pathway activity level scoring. This is the foundational data preparation step that enables downstream decomposition methods like PLAGE to compute pathway activity scores.

## When to use

When you have raw mass spectrometry peak intensity data (rows = peaks with IDs, columns = individual samples) and you need to align it with metabolite annotations (peak ID → KEGG or ChEBI compound ID mappings) before performing pathway-level analysis. Essential when noise, missing values, or zero intensities are prevalent in metabolomics datasets and you plan to compute robust pathway activity scores.

## When NOT to use

- Input is already a normalized gene expression matrix (e.g., RNA-seq counts or microarray intensities); use metabolomics-specific preprocessing instead.
- Annotations are missing for >50% of peaks; imputation and standardization will amplify noise and reduce pathway signal.
- Data contains technical replicates or batch effects that have not been corrected; apply batch correction before matrix extraction.

## Inputs

- Peak intensity matrix CSV (rows = peak features with IDs, columns = sample identifiers; optional second row = group/factor labels)
- Annotation matrix (peak ID, metabolite entity ID pairs in KEGG or ChEBI format)
- Experimental design specification (groups and comparisons)

## Outputs

- Preprocessed intensity dataframe (samples × metabolites, log-2 transformed, standardized to zero mean and unit variance)
- Metadata mapping (peak ID → metabolite ID, sample → group/factor)

## How to apply

Load the peak intensity CSV file (samples as columns, peak features as rows) and the corresponding annotation file (peak ID → metabolite entity ID pairs). For each experimental factor (group of samples), apply data imputation: replace all-zero intensities in a factor with the user-specified minimum value (default 5000), and replace partial-zero intensities with the mean of non-zero values in that factor. Log-2 transform the entire imputed matrix, then standardize it to zero mean and unit variance across samples using scipy.preprocessing. Retain only peaks that have at least one metabolite annotation; discard unannotated peaks. The resulting preprocessed matrix (samples × annotated metabolites) is now ready for pathway decomposition.

## Related tools

- **PALS** (Orchestrates metabolite intensity matrix extraction, imputation, and standardization as part of the full pathway analysis pipeline) — https://github.com/glasgowcompbio/PALS
- **scipy.preprocessing** (Provides standardization (zero mean, unit variance) after log-2 transformation)

## Examples

```
from pals.feature_extraction import DataSource
import pandas as pd
int_df = pd.read_csv('intensity.csv', index_col=0)
annot_df = pd.read_csv('annotation.csv', index_col=0)
experimental_design = {'comparisons': [{'case': 'treatment', 'control': 'control'}]}
ds = DataSource(int_df, annot_df, experimental_design, database_name='COMPOUND', min_replace=5000)
```

## Evaluation signals

- Verify no unannotated peaks remain in the output matrix (all retained peaks have ≥1 metabolite annotation).
- Check that log-2 transformed and standardized intensity values have mean ≈ 0 and standard deviation ≈ 1 across all samples.
- Confirm imputation occurred correctly: all-zero factors should be replaced with min_replace value; partial-zero values within a factor should equal the factor mean of non-zero entries.
- Validate matrix dimensions: samples (columns) and annotated metabolites (rows) match the input file counts after filtering out unannotated peaks.
- Ensure no NaN or infinite values remain after log-2 transformation (all imputed intensities > 0).

## Limitations

- Imputation assumes that missing or zero intensities are biochemically meaningful (below detection limit), not biological absence; strong assumptions may not hold for all metabolomics workflows.
- Standardization to unit variance can inflate noise for low-intensity metabolites and compress variation in high-intensity metabolites.
- Multiple peak-to-metabolite mappings (one peak → multiple compounds, or vice versa) require manual curation; the matrix construction does not resolve ambiguity automatically.
- Log-2 transformation undefined for zero or negative intensities; complete imputation of all zeros is required beforehand.

## Evidence

- [other] Load the metabolite intensity matrix (samples × metabolites) and pathway definitions (pathway identifiers mapped to metabolite sets).: "Load the metabolite intensity matrix (samples × metabolites) and pathway definitions (pathway identifiers mapped to metabolite sets)."
- [readme] The first is a matrix is of individual peak intensities (rows are peak features with column one containing the peak id, further columns representing individual samples).: "The first is a matrix is of individual peak intensities (rows are peak features with column one containing the peak id, further columns representing individual samples)."
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor.: "Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity"
- [readme] The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples."
- [readme] In addition, users also provide a list of compound annotations assigned to peak features (peaks that do not have annotations will not be used for pathway analysis).: "In addition, users also provide a list of compound annotations assigned to peak features (peaks that do not have annotations will not be used for pathway analysis)."
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
