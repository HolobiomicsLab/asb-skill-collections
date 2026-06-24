---
name: metabolomics-data-matrix-handling
description: Use when when you have raw metabolomics peak intensities or concentrations
  and accompanying sample metadata (batch, run order, sample type, factors of interest)
  and need to organize them into the featuredata, sampledata, and metabolitedata dataframes
  that NormalizeMets functions expect.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - R
  - NormalizeMets
  - RStudio
  - Microsoft Excel
  license_tier: open
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive
  Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
- The use of RStudio is also recommended. RStudio is an integrated development environment
  (IDE)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_normalizemets_cq
    doi: 10.1007/s11306-018-1347-7
    title: NormalizeMets
  dedup_kept_from: coll_normalizemets_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-018-1347-7
  all_source_dois:
  - 10.1007/s11306-018-1347-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-matrix-handling

## Summary

Structuring and preparing metabolomics feature data, sample metadata, and metabolite annotations into the standardized three-part input format required by the NormalizeMets package. This skill ensures data are correctly formatted before normalization, quality-control assessment, and biomarker analysis workflows.

## When to use

When you have raw metabolomics peak intensities or concentrations and accompanying sample metadata (batch, run order, sample type, factors of interest) and need to organize them into the featuredata, sampledata, and metabolitedata dataframes that NormalizeMets functions expect. Specifically when preparing data for RLSC normalization, QC-based batch correction, or relative log abundance diagnostic visualization.

## When NOT to use

- Input data are already correctly formatted in featuredata/sampledata/metabolitedata structure with validated row/column names and no missing cross-references.
- You are working with pre-processed, already-normalized feature tables from external sources that do not require reproducible batch correction or QC assessment.
- Your analysis only requires visualization or univariate statistical tests and does not depend on consistent data structures for downstream NormalizeMets functions.

## Inputs

- Raw peak intensity matrix (samples × metabolites)
- Sample metadata table (sample identifiers, batch/run order, sample type, factors)
- Metabolite annotation table (metabolite identifiers, standard/control designations)

## Outputs

- featuredata dataframe (samples × metabolites matrix with named rows and columns)
- sampledata dataframe (sample-level metadata with named rows)
- metabolitedata dataframe (metabolite-level annotations with named rows)

## How to apply

Organize your metabolomics data into three linked dataframes: (1) featuredata: a matrix with unique sample names as row names and unique metabolite names as column names, containing peak intensities or concentrations; (2) sampledata: a dataframe with unique sample names as row names and columns for sample type, run order, batch assignment, and factors of interest; (3) metabolitedata: a dataframe with unique metabolite names as row names and columns for metabolite-specific annotations (e.g., internal/external standard designation, positive/negative control flags). Ensure row/column names are unique and consistent across dataframes. When using QC-based normalization (e.g., NormQcsamples), sort featuredata and sampledata by the run order column before function calls. Verify that all samples in featuredata have corresponding rows in sampledata and all metabolites have corresponding rows in metabolitedata.

## Related tools

- **NormalizeMets** (R package that consumes the three-part featuredata/sampledata/metabolitedata structure for normalization, QC assessment, and biomarker identification workflows) — https://github.com/metabolomicstats/NormalizeMets
- **R** (Programming environment for constructing and manipulating the dataframes; functions like data.frame(), row.names(), and merge() are used to organize and validate the structure)
- **RStudio** (IDE for interactive data inspection, validation, and debugging of the dataframe structure before passing to NormalizeMets functions)
- **Microsoft Excel** (Alternative interface (via ExNormalizeMets) for preparing and entering featuredata, sampledata, and metabolitedata prior to analysis in the NormalizeMets package)

## Examples

```
featuredata <- read.csv('peaks.csv', row.names=1); sampledata <- read.csv('samples.csv', row.names=1); metabolitedata <- read.csv('metabolites.csv', row.names=1); sampledata <- sampledata[order(sampledata$order), ]; featuredata <- featuredata[rownames(sampledata), ]
```

## Evaluation signals

- featuredata has unique, non-empty row names (sample identifiers) and column names (metabolite identifiers); no duplicate or missing names.
- sampledata has unique row names matching all samples in featuredata; contains 'order' column (run sequence) for QC-based normalization; all required grouping columns (batch, sample type) are present and non-empty.
- metabolitedata has unique row names matching all metabolites in featuredata; standard/control designations are explicitly recorded where applicable.
- Cross-reference validation: nrow(featuredata) == nrow(sampledata) and ncol(featuredata) == nrow(metabolitedata); rownames(featuredata) == rownames(sampledata) and colnames(featuredata) == rownames(metabolitedata).
- NormQcsamples or RlaPlots functions execute without errors related to missing or mismatched data; output plots and normalized matrices are produced with expected dimensions and metadata associations.

## Limitations

- The package requires R version 3.4.3 or higher; older R installations will not support NormalizeMets or its dataframe operations.
- Missing values (NA, NaN) in featuredata require explicit handling via the MissingValues() function before normalization; the structure itself does not automatically impute or handle gaps.
- The sampledata 'order' column must reflect the actual run sequence and be numeric and sorted before calling QC-based normalization functions; inconsistent ordering will produce incorrect batch corrections.
- Metabolite names and sample names must be unique within their respective dataframes; duplicate identifiers will cause indexing failures and incorrect cross-referencing across featuredata, sampledata, and metabolitedata.

## Evidence

- [readme] Input data format requirement: "The input data format consists of three parts: (i) "featuredata" which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be"
- [other] Sorting by run order for QC normalization: "Sort featuredata and sampledata by run order (sampledata$order column)."
- [readme] Sample metadata content specification: ""sampledata" is a dataframe that contains sample-specific information. These information can include sample type, order of analysis, factors of interest and other sample-specific data relevant to the"
- [readme] Metabolite annotation content specification: ""metabolitedata" contains metabolite-specific information in a separate dataframe. These information can include, but is not limited to, designation of metabolites as internal/external standards, or"
- [readme] Name consistency across dataframes: "Unique sample names must be provided as row names and unique metabolite names as column names"
