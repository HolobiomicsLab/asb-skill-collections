---
name: p-value-and-fold-change-computation
description: Use when you have raw metabolomics data organized as a matrix with metabolites
  as rows and samples as columns, sample group labels (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - run_de()
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

# p-value-and-fold-change-computation

## Summary

Compute differential analysis summary statistics (p-values, adjusted p-values, and log2 fold changes) from raw metabolomics matrices to quantify metabolite abundance changes between experimental groups. These statistics serve as the foundation for downstream pathway enrichment analysis.

## When to use

Apply this skill when you have raw metabolomics data organized as a matrix with metabolites as rows and samples as columns, sample group labels (e.g., 'TK-CMV' and 'K-CMV'), and need to identify which metabolites differ significantly in abundance between two or more experimental groups before performing enrichment analysis.

## When NOT to use

- Input data is already a precomputed summary statistics table (p-values, fold changes, etc.) — pass directly to enrichment.
- Samples lack clear group assignments or experimental design is not a simple two-group comparison without covariates.
- Metabolite matrix has not been normalized or batch-corrected; preprocessing should precede differential analysis.

## Inputs

- Metabolomics abundance matrix (metabolites × samples)
- Sample group labels ('TK-CMV', 'K-CMV', or equivalent)
- Raw or normalized metabolite intensities

## Outputs

- Summary statistics table with metabolite identifiers, p-values, adjusted p-values, and log2 fold changes
- Differential analysis results for enrichment input

## How to apply

Load the metabolomics data matrix ensuring metabolites are rows and samples are columns, with samples labeled by group assignment. Call the run_de() function to perform differential analysis, which internally computes p-values testing the null hypothesis of no group difference for each metabolite, calculates adjusted p-values (typically via Benjamini–Hochberg or similar multiple-testing correction), and derives log2 fold changes as the log-ratio of mean abundances between groups. The output is a table of summary statistics (p-values, adjusted p-values, log2fc) for each metabolite that can be filtered by p-value thresholds (e.g., p_value_cutoff = 0.05) and passed to enrichment analysis functions.

## Related tools

- **run_de()** (Core function that accepts metabolomics matrix and group labels, computes p-values, adjusted p-values, and log2 fold changes for differential analysis) — https://github.com/biodatalab/enrichmet
- **R** (Statistical programming environment in which run_de() is implemented and executed)

## Examples

```
da_out <- run_de(inputData = metabolomics_matrix, groups = c('TK-CMV', 'K-CMV'))
```

## Evaluation signals

- Output table contains one row per metabolite with valid numeric p-values in [0, 1] and adjusted p-values also in [0, 1].
- Adjusted p-values are greater than or equal to raw p-values (multiple-testing correction property).
- Log2 fold changes are numeric, centered near zero for unchanged metabolites, and reflect the direction of change (positive for increased, negative for decreased in treatment vs. control).
- All metabolites from the input matrix appear in the output; no metabolites are silently dropped unless filtered by a specified threshold.
- Results can be successfully ingested by enrichment functions using the p-value and log2fc columns as input.

## Limitations

- run_de() is designed for two-group comparisons; multi-group or continuous designs require alternative approaches.
- Function assumes samples are independent; paired or blocked designs are not explicitly handled in the documented workflow.
- No guidance is provided on handling missing values, outliers, or unequal variance between groups within the article or README.
- The article does not specify the underlying statistical test (e.g., t-test, Mann–Whitney, Welch's t-test) or multiple-testing correction method used by run_de().

## Evidence

- [other] The run_de() function accepts a metabolomics matrix with metabolites as rows and samples as columns, along with group labels ('TK-CMV' and 'K-CMV'), and produces differential analysis output containing p-values, adjusted p-values, and log2 fold changes that serve as input for downstream enrichment analysis.: "the run_de() function accepts a metabolomics matrix with metabolites as rows and samples as columns, along with group labels ('TK-CMV' and 'K-CMV'), and produces differential analysis output"
- [readme] These results can be supplied in one of two formats: 1. Precomputed summary statistics 2. Raw metabolomics data, from which the workflow will compute differential analysis results internally.: "These results can be supplied in one of two formats: 1. Precomputed summary statistics 2. Raw metabolomics data, from which the workflow will compute differential analysis results internally"
- [readme] the workflow should begin with the run_de() function. This step generates the summary statistics required for enrichment, including p-values, adjusted p-values, and log2 fold changes.: "the workflow should begin with the run_de() function. This step generates the summary statistics required for enrichment, including p-values, adjusted p-values, and log2 fold changes."
- [other] Load the raw metabolomics data matrix with metabolites as rows and samples as columns, ensuring samples are labeled with group assignments ('TK-CMV' or 'K-CMV'). Call run_de() function to perform differential analysis comparing the two groups, generating summary statistics including p-values, adjusted p-values, and log2 fold changes for each metabolite.: "Load the raw metabolomics data matrix with metabolites as rows and samples as columns, ensuring samples are labeled with group assignments ('TK-CMV' or 'K-CMV'). Call run_de() function to perform"
