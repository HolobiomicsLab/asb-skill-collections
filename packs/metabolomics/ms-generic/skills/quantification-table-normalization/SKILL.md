---
name: quantification-table-normalization
description: Use when you have raw quantification data (abundance or intensity values across samples and features) from mass spectrometry or similar high-dimensional assays and need to prepare it for msFeaST's feature selection workflow, which requires standardized internal data structures compatible with.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - msFeaST
  - jupyter-notebook
  - pandas
  - globaltest (R package)
  - Shiny
  - QuantyFey
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btae584
  title: msFeaST
- doi: 10.1016/j.aca.2025.344571
  title: ''
evidence_spans:
- github.com__kevinmildau__msFeaST
- '**QuantyFey** is a Shiny application for the **visualization, analysis, and quantification** of **mass spectrometry (MS) data**'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msfeast_cq
    doi: 10.1093/bioinformatics/btae584
    title: msFeaST
  - build: coll_quantyfey_cq
    doi: 10.1016/j.aca.2025.344571
    title: quantyfey
  dedup_kept_from: coll_msfeast_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae584
  all_source_dois:
  - 10.1093/bioinformatics/btae584
  - 10.1016/j.aca.2025.344571
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# quantification-table-normalization

## Summary

Transform and normalize quantification tables (metabolite or feature abundance matrices) into the internal data format expected by msFeaST for downstream feature selection and statistical analysis. This preprocessing step ensures compatibility with the pipeline's statistical tests and interactive visualization.

## When to use

You have raw quantification data (abundance or intensity values across samples and features) from mass spectrometry or similar high-dimensional assays and need to prepare it for msFeaST's feature selection workflow, which requires standardized internal data structures compatible with R-based statistical tests (e.g., globaltest).

## When NOT to use

- Quantification data is already in msFeaST's internal format or has been validated and formatted by a prior preprocessing run.
- You only need to inspect pre-computed results without re-processing raw abundance data—use the dashboard directly with existing dashboard_data.json.
- Your quantification matrix lacks metadata or spectral data mappings, making alignment impossible.

## Inputs

- quantification table (CSV, TSV, or pandas DataFrame with samples × features abundance matrix)
- metadata table (for sample ID validation and alignment)
- data filepath arguments (user-specified locations of quantification files)

## Outputs

- normalized quantification data structure (Python dictionary or DataFrame in msFeaST internal format)
- validated sample-feature mappings ready for pipeline input
- intermediate data object compatible with R globaltest and statistical functions

## How to apply

Load the quantification table (typically a pandas DataFrame or CSV with samples as rows and features/metabolites as columns) using the msFeaST preprocessing notebook (preprocessing_mushroom_type_comparison.ipynb). Parse and validate the input data structure to ensure it meets msFeaST requirements—notably sample identifiers that map to metadata rows and feature identifiers that correspond to spectral data. Transform the quantification table into the internal Python data structure (dictionary or DataFrame) expected by msFeaST, which aligns with downstream R statistical dependencies including the globaltest package. The normalization step may include handling missing values, scaling, or log-transformation depending on the assay type; refer to the notebook's magenta-italicized user input sections for dataset-specific parameters. Validate alignment between quantification sample IDs and metadata table rows before proceeding to the pipeline.

## Related tools

- **msFeaST** (provides the preprocessing notebook, internal data format specification, and statistical pipeline that consumes the normalized quantification table) — https://github.com/kevinmildau/msFeaST
- **jupyter-notebook** (execution environment for the preprocessing_mushroom_type_comparison.ipynb notebook that loads, parses, and normalizes the quantification table)
- **pandas** (used implicitly within msFeaST preprocessing to load and manipulate quantification DataFrames)
- **globaltest (R package)** (downstream R dependency that receives the normalized quantification data for feature selection and statistical testing)

## Examples

```
jupyter-notebook preprocessing_mushroom_type_comparison.ipynb  # then modify data filepath arguments to your quantification, metadata, and spectral data files and execute cells
```

## Evaluation signals

- Quantification table sample IDs match all rows in the metadata table with no missing or orphaned mappings.
- Feature identifiers in the quantification table align with feature IDs in the spectral data without duplicates or conflicts.
- The normalized data structure can be serialized and passed to the msFeaST pipeline without schema or type errors.
- R globaltest and associated statistical functions (dplyr, tibble) execute without error on the normalized quantification object.
- The pipeline produces a valid JSON output file that loads successfully in the msFeaST interactive dashboard.

## Limitations

- msFeaST preprocessing and pipeline workflow have been tested on macOS and Linux; Windows support is currently being worked on.
- R package installation via conda is not reliable for the required packages; remotes and BiocManager must be used to control R package versions, which may require several minutes for compilation.
- The skill assumes that sample identifiers and feature identifiers are stable and unambiguous across the quantification, metadata, and spectral data files; user must verify alignment before pipeline execution.
- No changelog is available to track changes in data format specifications between msFeaST versions, potentially causing compatibility issues if updating the tool.

## Evidence

- [other] Transform and normalize the quantification and metadata tables into the internal data format expected by msFeaST.: "Transform and normalize the quantification and metadata tables into the internal data format expected by msFeaST"
- [other] Parse and validate the input data structures to ensure compatibility with msFeaST requirements.: "Parse and validate the input data structures to ensure compatibility with msFeaST requirements"
- [readme] Navigate to the notebook folder and open the preprocessing_mushroom_type_comparison.ipynb and msfeast_pipeline_mushroom_type_comparison.ipynb notebooks on your local machine. These notebooks contain a complete example of quantification table, metadata table, and spectral data processing required for msFeaST, as well as a complete use-case example.: "These notebooks contain a complete example of quantification table, metadata table, and spectral data processing required for msFeaST"
- [readme] Text in magenta italics font highlights required user input for the pipeline.: "Text in magenta italics font highlights required user input for the pipeline"
- [readme] The current msFeaST pre-processing and pipeline workflow has been tested on macos and should work identically on linux operating systems. Windows support is currently being worked on.: "The current msFeaST pre-processing and pipeline workflow has been tested on macos and should work identically on linux operating systems. Windows support is currently being worked on"
