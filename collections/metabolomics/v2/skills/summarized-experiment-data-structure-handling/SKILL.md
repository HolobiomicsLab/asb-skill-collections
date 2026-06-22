---
name: summarized-experiment-data-structure-handling
description: Use when you have high-dimensional metabolomics or genomics data stored as a SummarizedExperiment object (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3209
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - devtools
  - Bioconductor
  - marr
derived_from:
- doi: 10.1186/s12859-021-04336-9
  title: marr
- doi: 10.1080/01621459.2017.1397521
  title: ''
evidence_spans:
- 'marr: An R/Bioconductor package for Maximum Rank Reproducibility'
- The R-package **marr** can be installed from GitHub using the R package [devtools]
- '`marr`: An R/Bioconductor package for Maximum Rank Reproducibility'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_marr_cq
    doi: 10.1186/s12859-021-04336-9
    title: marr
  dedup_kept_from: coll_marr_cq
schema_version: 0.2.0
---

# Summarized Experiment Data Structure Handling

## Summary

Load, validate, and extract data from SummarizedExperiment objects—a Bioconductor container format for high-dimensional biological assays with row (feature) and column (sample) metadata. This skill enables reproducible analysis workflows in R by ensuring correct orientation, accessor patterns, and downstream compatibility with statistical functions.

## When to use

You have high-dimensional metabolomics or genomics data stored as a SummarizedExperiment object (e.g., msprepCOPD from the marr package) and need to pass it to a Bioconductor or R statistical function that expects a SummarizedExperiment interface with properly annotated assays, row metadata (feature annotations), and column metadata (sample annotations).

## When NOT to use

- Input is a raw data matrix or data frame without row/column annotations—use data frame validation and metadata assembly first
- Input is already in wide or long tabular format without SummarizedExperiment wrapping—convert to SummarizedExperiment using SummarizedExperiment() constructor before applying this skill
- Analysis requires direct matrix operations (e.g., principal component analysis) where you need raw numerical data only—extract assay() without SummarizedExperiment overhead

## Inputs

- SummarizedExperiment object (e.g., msprepCOPD)
- Assay matrix with metabolites/genes on rows, samples on columns
- Row metadata (feature annotations)
- Column metadata (sample annotations)

## Outputs

- Validated SummarizedExperiment object in R memory
- Extracted assay data frame or matrix
- Result objects from downstream functions (e.g., MarrOutput with four accessor-extractable tables)

## How to apply

Load the SummarizedExperiment object using library() and data() or by retrieving it from a package (e.g., data(msprepCOPD, package='marr')). Verify the object structure and metadata using str(), colData(), and rowData(). Confirm the assay matrix has observations (metabolites or genes) on rows and samples on columns. Pass the SummarizedExperiment object directly to functions that accept it as input (e.g., Marr(object = dataSE, ...)). Extract results using accessor methods specific to the output object (e.g., MarrFeatures(), MarrSamplepairs()). Validate that output tables are non-empty and contain expected columns for reproducibility metrics.

## Related tools

- **marr** (Statistical function that accepts SummarizedExperiment objects as input and generates reproducibility tables via accessor methods (MarrFeatures, MarrSamplepairs, etc.)) — https://github.com/Ghoshlab/marr
- **Bioconductor** (Bioconductor framework providing SummarizedExperiment class definition and standard assay/metadata accessor interface)
- **R** (Language runtime for loading, validating, and passing SummarizedExperiment objects to downstream functions)

## Examples

```
library(marr); data(msprepCOPD); MarrOutput <- Marr(object = msprepCOPD, pSamplepairs=0.75, pFeatures=0.75, alpha=0.05); MarrFeatures(MarrOutput)
```

## Evaluation signals

- SummarizedExperiment object loads without errors and str() shows expected assay, rowData, and colData slots
- Assay matrix dimensions match expected feature count × sample count (e.g., 645 metabolites × 20 samples for msprepCOPD)
- Accessor methods (e.g., MarrFeatures(output)) return non-empty data frames with expected columns (e.g., reproducibility ranks, percent reproducible signals)
- Extracted tables have no missing required columns and numeric values fall within expected ranges (e.g., percent reproducibility 0–100)
- Downstream statistical functions execute without dimension mismatch or metadata alignment errors

## Limitations

- SummarizedExperiment requires Bioconductor installation; not available in base R or CRAN-only environments
- Accessor method names and output structures vary by package (e.g., MarrFeatures vs. assay); users must consult package documentation for correct extraction patterns
- Metadata annotations are optional; missing row or column metadata may limit interpretability but do not prevent analysis—validation of metadata completeness is user responsibility
- Large assay objects (e.g., >10,000 features, >1,000 samples) may consume significant memory; subsetting or filtering before downstream operations is recommended

## Evidence

- [intro] Load the msprepCOPD SummarizedExperiment object from the marr R package and pass to Marr() function: "Load the msprepCOPD SummarizedExperiment object from the marr R package"
- [readme] SummarizedExperiment with observations on rows and samples as columns: "a data frame or a matrix or a Summarized Experiment with one assay object with observations (e.g., metabolites or genes) on the rows and samples as the columns"
- [readme] Extract four output tables using accessor methods MarrFeatures, MarrSamplepairs, MarrFeaturesfiltered, MarrSamplepairsfiltered: "Individual slots can be extracted using accessor methods: MarrSamplepairs(MarrOutput) ... MarrFeatures(MarrOutput) ... MarrSamplepairsfiltered(MarrOutput) ... MarrFeaturesfiltered(MarrOutput)"
- [intro] Validate that all four tables are non-empty and contain expected columns: "Validate that all four tables are non-empty and contain expected columns for reproducibility metrics and rankings"
- [readme] msprepCOPD pre-processed data SummarizedExperiment object containing 645 metabolites measured in 20 biological replicates: "The **marr** package contains a pre-processed data `SummarizedExperiment` assay object of 645 metabolites (features) measured in plasma and 20 biological replicates"
