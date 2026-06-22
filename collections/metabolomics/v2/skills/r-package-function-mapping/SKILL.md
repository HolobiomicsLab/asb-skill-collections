---
name: r-package-function-mapping
description: Use when you have a working R package (e.g., IonFlow for ionomics analysis) with documented functions and parameters, and you need to wrap it as a Galaxy tool so end users can invoke the R workflow through Galaxy's web interface without command-line expertise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - ionflow
  - Galaxy
  - IonFlow
  - planemo
derived_from:
- doi: 10.1007/s11306-021-01841-z
  title: IonFlow
evidence_spans:
- based on the modification of R package
- github.com__wanchanglin__ionflow
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ionflow_cq
    doi: 10.1007/s11306-021-01841-z
    title: IonFlow
  dedup_kept_from: coll_ionflow_cq
schema_version: 0.2.0
---

# R Package Function Mapping to Galaxy Tool XML

## Summary

Map R package functions and parameters to Galaxy tool XML wrapper definitions, enabling exposure of R-based analytical workflows as graphical Galaxy tools. This skill bridges R function signatures to Galaxy's input/output port bindings and command-line invocation patterns.

## When to use

You have a working R package (e.g., IonFlow for ionomics analysis) with documented functions and parameters, and you need to wrap it as a Galaxy tool so end users can invoke the R workflow through Galaxy's web interface without command-line expertise. Specifically useful when the R package performs domain-specific data transformations (e.g., pre-processing, outlier detection, batch correction) on tabular or matrix data formats.

## When NOT to use

- R package functions lack clear input/output contracts or are highly interactive (e.g., require user input during execution).
- Data is not tabular or matrix-like (e.g., unstructured text, images, networks); Galaxy's input/output binding model assumes structured data types.
- Your use case requires dynamic branching, conditional function calls, or complex control flow not easily expressed in Galaxy XML command templates.

## Inputs

- Raw ionomics data frame (tabular format: samples × ions, e.g., ion concentrations in ppm)
- Optional: pre-defined ion standard deviation vector (numeric, one per ion type)
- Analysis parameters: outlier fence multiplier (e.g., 3×IQR), batch grouping variable, log-transformation flag

## Outputs

- Cleaned/preprocessed ionomics dataset (tabular: outliers removed, batch-corrected)
- Pre-processing statistics object (summary table: min, Q1, median, mean, Q3, max, variance per ion)
- Outlier summary table (ion-wise counts: not_outlier, outlier, outlier_%)
- Batch-corrected data statistics (log-transformed, median-scaled per ion per batch)

## How to apply

First, inventory the R package's key functions, their formal arguments, input data types (e.g., data frame, numeric vector), and expected output objects. Second, define a Galaxy tool XML file specifying input parameters as Galaxy inputs (using appropriate data type tags: tabular for ion concentration matrices, text for optional standard deviation vectors), command-line invocation that calls `Rscript` or `R CMD BATCH` with the ionflow package loaded, and output file declarations matching the R function's return objects (e.g., preprocessed data frame, outlier statistics). Third, implement input/output port bindings by mapping Galaxy input names to R function arguments via command substitution (e.g., `$input_data` → `data=read.csv('$input_data')`). Fourth, test the wrapper locally against the IonFlow R package using representative ionomics datasets (e.g., ICP-MS ion concentration matrices with 1454 samples and 14 ion types) to verify parameter passing, function execution, and output file generation. Finally, validate wrapper syntax and Galaxy compliance using planemo lint and Galaxy test harness to ensure proper data type handling and error messaging.

## Related tools

- **R** (Runtime environment for ionflow package functions; invoked via Rscript in Galaxy command tag)
- **Galaxy** (Workflow platform; tool XML wrapper exposes R functions through web interface and manages input/output data staging) — https://github.com/galaxyproject/galaxy
- **IonFlow** (Core R package providing pre-processing, exploratory analysis, clustering, and network analysis functions for ionomics data) — https://github.com/AlinaPeluso/MetaboFlow
- **planemo** (Validation and testing harness; used to lint Galaxy tool XML syntax and test wrapper compliance)

## Examples

```
devtools::install_github('AlinaPeluso/MetaboFlow', subdir='IonFlow'); library(IonFlow); pre_proc <- PreProcessing(data=IonData, stdev=pre_defined_sd); print(pre_proc$stats.raw_data)
```

## Evaluation signals

- Galaxy tool XML passes planemo lint validation with no schema or syntax errors.
- Input data binding: tabular ion concentration file is successfully parsed by R function; command substitution correctly maps Galaxy inputs ($input_data, $stdev) to R function arguments (data=, stdev=).
- Output files are generated and written to Galaxy's expected output directory with correct format (e.g., stats.raw_data table matches structure in README example with Min/Q1/Median/Mean/Q3/Max/Variance columns per ion).
- Test run on representative ionomics dataset (1454 samples, 14 ions) produces consistent pre-processing statistics (e.g., outlier counts, batch correction transformations) matching standalone R package execution.
- Galaxy test harness confirms parameter passing: varying outlier multiplier, batch variable, or log-transformation flag produces expected downstream changes in statistics output.

## Limitations

- R package version lock: Galaxy wrapper is tightly coupled to a specific IonFlow R package version; updates to package function signatures or argument names require wrapper re-authoring and re-validation.
- No changelog documented in the ionflow repository; reproducibility may be compromised if prior wrapper versions are not archived or tagged.
- Batch correction assumes control strain (e.g., YDL227C mutant measured multiple times per batch); workflows on datasets lacking batch replicates or control samples will produce uninformative batch statistics.
- High-dimensionality corner cases: datasets with very large numbers of ions or extreme outlier ratios (>1%) may trigger numerical instability in standardization or produce difficult-to-interpret downstream results.

## Evidence

- [other] IonFlow for Galaxy is implemented as a Galaxy tool wrapper based on modification of the IonFlow R package: "IonFlow for Galaxy is implemented as a Galaxy tool wrapper based on modification of the IonFlow R package to enable processing and analysis of ionomics data."
- [other] Workflow steps for wrapping: Define Galaxy XML, implement input/output bindings, test locally, validate with planemo: "Define the Galaxy tool XML wrapper specifying input parameters (data formats, analysis options), command-line invocation of R and the ionflow package functions, and output file declarations. 3."
- [readme] ICP-MS data of yeast ion concentrations measured for 1454 single-gene haploid knockouts with 14 ions: "We illustrate the Ionomics workflow with ICP-MS data of yeast intracellular ion concentrations measured for 1454 single-gene haploid knockouts (data from Danku, 2009). Ions measured include Ca44,"
- [readme] Pre-processing removes outliers beyond Q1 - 3*IQR (lower) and Q3 + 3*IQR (upper) fences: "We define a lower outer fence: Q1 - 3*IQ and a upper outer fence: Q3 + 3*IQ where Q1 and Q3 are the first and the third quantile of the distribution, respectively. A point beyond the outer fence is"
- [readme] Batch correction via log-transform and median scaling per ion per batch: "First we take the logarithmm of the concentration value. Then, the data are scaled to the median taken for each ion within each batch."
- [readme] Installation via git clone and tool_conf.xml configuration: "Use git to clone this tool: git clone https://github.com/wanchanglin/ionflow.git. Add this tool's location into Galaxy' tool config file: ~/Galaxy/config/tool_conf.xml."
