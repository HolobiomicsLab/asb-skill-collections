---
name: differential-metabolite-abundance-analysis
description: Use when you have raw metabolomics data structured as a matrix with metabolites
  as rows and samples as columns, samples are annotated with group labels (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3172
  tools:
  - R
  - run_de()
  - enrichmet()
  license_tier: open
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed
  through a single R function call
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enrichmet_cq
    doi: 10.1101/2025.08.28.672951v2
    title: EnrichMET
  dedup_kept_from: coll_enrichmet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.08.28.672951v2
  all_source_dois:
  - 10.1101/2025.08.28.672951v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# differential-metabolite-abundance-analysis

## Summary

Compute differential abundance statistics (p-values, adjusted p-values, log2 fold changes) for metabolites across experimental groups using the run_de() function, which accepts a metabolomics matrix with metabolites as rows and samples as columns labeled with group assignments. This step produces the summary statistics required for downstream pathway enrichment analysis.

## When to use

You have raw metabolomics data structured as a matrix with metabolites as rows and samples as columns, samples are annotated with group labels (e.g., 'TK-CMV' and 'K-CMV'), and you need to identify metabolites with significant differences in abundance between two or more experimental groups before performing pathway enrichment or other downstream analyses.

## When NOT to use

- Input is already a precomputed summary statistics table (p-values, adjusted p-values, log2 fold changes already calculated) — pass directly to enrichment analysis instead.
- Data are not in the required matrix format (metabolites as rows, samples as columns) — data reformatting is needed before calling run_de().
- Single experimental group or unpaired/unstructured samples without clear group labels — differential analysis requires at least two annotated groups for comparison.

## Inputs

- metabolomics data matrix (metabolites × samples) with numeric abundance values
- sample annotation vector with group labels (e.g., 'TK-CMV', 'K-CMV')

## Outputs

- differential analysis results table with columns: metabolite identifier, p-value, adjusted p-value, log2 fold change
- summary statistics object suitable for pathway enrichment analysis

## How to apply

Load the raw metabolomics data matrix ensuring metabolites are rows and samples are columns, with each sample labeled with its group assignment. Call the run_de() function on this structured input to perform differential analysis, which internally computes p-values, adjusted p-values, and log2 fold changes for each metabolite. The function outputs a differential analysis results table containing metabolite identifiers and their associated statistics. These summary statistics serve as the required input for the enrichmet() enrichment analysis function; the workflow documentation explicitly states 'the workflow should begin with the run_de() function. This step generates the summary statistics required for enrichment, including p-values, adjusted p-values, and log2 fold changes.' Users can optionally supply precomputed summary statistics if differential analysis has been performed elsewhere, but run_de() is the integrated approach for computing them internally.

## Related tools

- **run_de()** (Performs differential abundance analysis on metabolomics matrix, computing p-values, adjusted p-values, and log2 fold changes for each metabolite between experimental groups) — https://github.com/biodatalab/enrichmet
- **R** (Statistical computing environment for executing the run_de() function and manipulating metabolomics data structures)
- **enrichmet()** (Accepts run_de() output (da_results parameter) as input for downstream pathway enrichment analysis) — https://github.com/biodatalab/enrichmet

## Examples

```
results <- run_de(metabolomics_matrix = data_matrix, group_labels = c('TK-CMV', 'K-CMV'))
```

## Evaluation signals

- Output table contains one row per input metabolite with non-null p-values (range 0–1) and adjusted p-values (range 0–1), with adjusted p-values ≥ corresponding raw p-values.
- Log2 fold changes have expected direction and magnitude; negative values indicate lower abundance in one group, positive in the other.
- Output table dimensions match input: number of rows equals number of unique metabolites in input matrix.
- No missing values in critical columns (p-value, adjusted p-value, log2fc); any rows with missing statistics indicate potential data quality issues.
- Output is compatible with enrichmet() function by matching expected column names and data types (e.g., da_results parameter accepts the output directly).

## Limitations

- run_de() requires properly annotated group labels; missing or inconsistent group annotations will cause function failure.
- The function assumes the two groups being compared are well-defined; complex experimental designs with multiple factors or continuous covariates may require alternative statistical approaches.
- Adjusted p-values depend on the multiple-testing correction method used internally by run_de(); the exact correction procedure is not detailed in the available documentation.
- No explicit filtering by p-value threshold occurs in run_de() itself; filtering to metabolites with p_value_cutoff (e.g., 0.05) is applied downstream during enrichment analysis via the enrichmet() function parameters.

## Evidence

- [other] The run_de() function accepts a metabolomics matrix with metabolites as rows and samples as columns, along with group labels ('TK-CMV' and 'K-CMV'), and produces differential analysis output containing p-values, adjusted p-values, and log2 fold changes: "The run_de() function accepts a metabolomics matrix with metabolites as rows and samples as columns, along with group labels ('TK-CMV' and 'K-CMV'), and produces differential analysis output"
- [other] Load the raw metabolomics data matrix and call run_de() to perform differential analysis, generating summary statistics: "Load the raw metabolomics data matrix with metabolites as rows and samples as columns, ensuring samples are labeled with group assignments ('TK-CMV' or 'K-CMV'). Call run_de() function to perform"
- [readme] The workflow should begin with the run_de() function to generate summary statistics required for enrichment: "the workflow should begin with the run_de() function. This step generates the summary statistics required for enrichment, including p-values, adjusted p-values, and log2 fold changes."
- [readme] Results can be supplied in one of two formats: precomputed summary statistics or raw metabolomics data: "These results can be supplied in one of two formats: 1. Precomputed summary statistics 2. Raw metabolomics data, from which the workflow will compute differential analysis results internally"
- [other] Output the differential analysis results table containing metabolite identifiers and their associated statistics: "Output the differential analysis results table containing metabolite identifiers and their associated statistics."
