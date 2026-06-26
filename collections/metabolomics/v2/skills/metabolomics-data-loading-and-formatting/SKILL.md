---
name: metabolomics-data-loading-and-formatting
description: Use when you have raw metabolomics count data (e.g., from mass spectrometry
  or NMR experiments) in tabular format and associated sample metadata (e.g., treatment
  groups, experimental factors) that need to be imported into R for analysis with
  packages like Omu.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - R
  - read.metabo
  - read.csv
  - transform_samples
  - assign_hierarchy
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1128/mra.00129-19
  title: omu metabolomics count data tool
evidence_spans:
- Omu is an R package that enables rapid analysis of Metabolomics data sets
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omu_metabolomics_count_data_tool_cq
    doi: 10.1128/mra.00129-19
    title: omu metabolomics count data tool
  dedup_kept_from: coll_omu_metabolomics_count_data_tool_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1128/mra.00129-19
  all_source_dois:
  - 10.1128/mra.00129-19
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-loading-and-formatting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load and structure raw metabolomics count data and metadata into R using specialized functions that ensure proper class assignment and hierarchical organization. This skill establishes the foundation for downstream statistical analysis and visualization of metabolite abundance patterns.

## When to use

You have raw metabolomics count data (e.g., from mass spectrometry or NMR experiments) in tabular format and associated sample metadata (e.g., treatment groups, experimental factors) that need to be imported into R for analysis with packages like Omu. Use this skill when you have two separate files: a count data matrix with metabolites as rows and samples as columns, and a metadata file with samples as rows and experimental factors as columns.

## When NOT to use

- Data is already in an R-native Omu object or ExpressionSet class
- Metabolite identifiers are already mapped to functional annotations
- Count data contains zero-variance metabolites or has already been filtered for quality control

## Inputs

- raw metabolomics count data matrix (rows=metabolites, columns=samples)
- sample metadata file (rows=samples, columns=experimental factors)
- metabolite identifier type (KEGG, KO_Number, Prokaryote, or Eukaryote)

## Outputs

- R data object with metabolomics count data (proper class for Omu)
- R metadata data frame with Sample column and experimental factor columns
- optionally: log-transformed count data
- optionally: count data with assigned hierarchical class information

## How to apply

Load the metabolomics count data using the read.metabo function, which ensures the data is assigned the correct class for compatibility with Omu workflows. Separately load the metadata file using read.csv, ensuring it contains a Sample column with row values matching the sample names in the count data, plus columns for each experimental factor (e.g., Treatment, Genotype). If necessary, optionally log-transform the count data column-wise using transform_samples with the natural log function to address overdispersion typical of metabolomics count data. Assign hierarchical class data using assign_hierarchy and specify the correct metabolite identifier (KEGG, KO_Number, Prokaryote, or Eukaryote) to enable functional downstream analysis.

## Related tools

- **read.metabo** (Loads metabolomics count data and ensures proper R class assignment for Omu workflow) — https://github.com/connor-reid-tiffany/Omu
- **read.csv** (Loads sample metadata file containing experimental factors and sample identifiers)
- **transform_samples** (Performs column-wise transformations (e.g., natural log) to address overdispersion in count data) — https://github.com/connor-reid-tiffany/Omu
- **assign_hierarchy** (Maps metabolite identifiers to hierarchical functional classes (KEGG, KO, Prokaryote, Eukaryote)) — https://github.com/connor-reid-tiffany/Omu

## Examples

```
count_data <- read.metabo('metabolomics_counts.csv'); metadata <- read.csv('sample_metadata.csv'); count_data_log <- transform_samples(count_data, log)
```

## Evaluation signals

- Count data object has correct R class recognized by Omu functions (verify via class() and str())
- Metadata data frame has exactly one Sample column with all sample names matching count data column names
- Metadata contains at least one experimental factor column with consistent, non-missing values
- If log-transformed: all count values are numeric and positive before transformation, no NaN or Inf values after
- If hierarchy assigned: metabolites have valid identifiers from the specified namespace (KEGG, KO_Number, Prokaryote, or Eukaryote)

## Limitations

- read.metabo function documentation does not specify expected file format (CSV, TSV, Excel); users should verify compatibility with their file type
- Metadata file must have exact column naming and row–column correspondence; mismatch between sample names in count data and metadata will cause silent failures in downstream functions
- assign_hierarchy requires metabolites to be labeled with recognizable KEGG/KO identifiers; identifiers not in the KEGG database will fail silently or be dropped
- No built-in quality control or duplicate-removal functions documented; overdispersion mitigation via log transformation is optional and user-driven

## Evidence

- [other] read.metabo recommendation: "For end users metabolomics data, it is recommended to use the ```read.metabo``` function to load it into R"
- [other] metadata file structure requirement: "The meta data file should have a Sample column, with row values being sample names, and then a column for each Factor in your dataset"
- [other] example metabolomics dataset: "Included with Omu is an example metabolomics dataset of data from fecal samples collected from a two factor experiment with wild type c57B6J mice and c57B6J mice with a knocked out nos2 gene"
- [other] log transformation for overdispersion: "```transform_samples``` will perform column-wise transformations across the data using the supplied function. This is useful for operations such as log transformation, or transforming by the square"
- [other] hierarchical class assignment: "To assign hierarchical class data, use the ```assign_hierarchy``` function and pick the correct identifier, either "KEGG", "KO_Number", "Prokaryote", or "Eukaryote""
