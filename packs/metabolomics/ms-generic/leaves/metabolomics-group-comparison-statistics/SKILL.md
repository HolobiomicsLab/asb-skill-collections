---
name: metabolomics-group-comparison-statistics
description: Use when you have a metabolomics matrix with metabolites as rows and
  samples as columns, each sample labeled with one of two experimental group identifiers
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - run_de()
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# metabolomics-group-comparison-statistics

## Summary

Compute differential abundance statistics (p-values, adjusted p-values, log2 fold changes) from raw metabolomics data matrices by comparing two experimental groups. This skill produces summary statistics that serve as input for downstream pathway enrichment analysis.

## When to use

You have a metabolomics matrix with metabolites as rows and samples as columns, each sample labeled with one of two experimental group identifiers (e.g., 'TK-CMV' or 'K-CMV'), and you need to identify which metabolites differ significantly between the groups before performing enrichment analysis.

## When NOT to use

- Input is already a precomputed summary statistics table with p-values and fold changes — skip to enrichment analysis directly.
- Sample sizes are extremely small (< 3 replicates per group) — statistical power will be insufficient to detect true differences.
- Metabolites have been heavily filtered or preprocessed independently by group — violates assumption of computing statistics on the full raw matrix.

## Inputs

- Metabolomics data matrix (metabolites × samples) with numeric abundance values
- Sample metadata table with group assignments ('TK-CMV', 'K-CMV', or equivalent binary group labels)
- Metabolite identifier annotations (e.g., KEGG IDs, m/z values, retention times)

## Outputs

- Differential analysis results table (data.frame) with columns: metabolite_id, p_value, adjusted_p_value, log2_fold_change
- Summary statistics table suitable for downstream enrichment analysis

## How to apply

Load the metabolomics data matrix ensuring metabolites are rows and samples are columns, with sample metadata including group assignment. Call the run_de() function, which performs statistical testing (typically t-test or Mann-Whitney U) to generate p-values for each metabolite. The function also computes adjusted p-values (using methods like Benjamini-Hochberg) and log2 fold changes comparing mean abundance between groups. Filter metabolites using a p-value cutoff (commonly p < 0.05) to retain statistically significant results. Output the differential analysis results table containing metabolite identifiers, p-values, adjusted p-values, and log2 fold changes for input to enrichment analysis.

## Related tools

- **run_de()** (Performs differential abundance analysis comparing two groups, generating p-values, adjusted p-values, and log2 fold changes for each metabolite) — https://github.com/biodatalab/enrichmet
- **R** (Statistical computing environment in which run_de() is executed and metabolomics matrices are manipulated)

## Examples

```
da_out <- run_de(inputMetabolites = metabolite_matrix, groups = sample_groups); results <- enrichmet(inputMetabolites = NULL, PathwayVsMetabolites = PathwayVsMetabolites, da_results = da_out, p_value_cutoff = 0.05)
```

## Evaluation signals

- Output table has one row per metabolite and contains no missing values in p_value, adjusted_p_value, and log2_fold_change columns.
- P-values and adjusted p-values fall within [0, 1]; adjusted p-values are ≥ corresponding raw p-values (monotonicity check).
- Log2 fold changes reflect the direction and magnitude of group difference; metabolites with significant p-values (p < 0.05) show non-zero fold changes.
- Row count of output matches input metabolite count (or is less only if filtering was applied with explicit criteria).
- Output is compatible with enrichmet() function input format (da_results parameter accepts the table schema directly).

## Limitations

- run_de() assumes data are suitable for parametric or non-parametric tests; highly zero-inflated or bimodal distributions may require specialized methods (e.g., zero-inflated models, compositional analysis).
- Statistical power depends critically on sample size and biological variance; small sample sizes (n < 5 per group) yield high false discovery rates.
- Adjusted p-values are sensitive to the multiple-testing correction method; Benjamini-Hochberg is standard but may be conservative if many true signals are present.
- The function requires group labels to be binary or explicitly specified; multi-group comparisons require pairwise post-hoc testing.
- No changelog is available for the enrichmet package, making it difficult to track changes to run_de() behavior across versions.

## Evidence

- [other] Load the raw metabolomics data matrix with metabolites as rows and samples as columns, ensuring samples are labeled with group assignments ('TK-CMV' or 'K-CMV').: "Load the raw metabolomics data matrix with metabolites as rows and samples as columns, ensuring samples are labeled with group assignments ('TK-CMV' or 'K-CMV')"
- [other] Call run_de() function to perform differential analysis comparing the two groups, generating summary statistics including p-values, adjusted p-values, and log2 fold changes for each metabolite.: "Call run_de() function to perform differential analysis comparing the two groups, generating summary statistics including p-values, adjusted p-values, and log2 fold changes for each metabolite"
- [other] The run_de() function accepts a metabolomics matrix with metabolites as rows and samples as columns, along with group labels ('TK-CMV' and 'K-CMV'), and produces differential analysis output containing p-values, adjusted p-values, and log2 fold changes that serve as input for downstream enrichment analysis.: "The run_de() function accepts a metabolomics matrix with metabolites as rows and samples as columns, along with group labels ('TK-CMV' and 'K-CMV'), and produces differential analysis output"
- [intro] the workflow should begin with the run_de() function. This step generates the summary statistics required for enrichment, including p-values, adjusted p-values, and log2 fold changes.: "the workflow should begin with the run_de() function. This step generates the summary statistics required for enrichment, including p-values, adjusted p-values, and log2 fold changes"
- [intro] Filter metabolites using p_value_cutoff parameter  [section=intro; evidence='p_value_cutoff = 0.05']: "p_value_cutoff = 0.05"
