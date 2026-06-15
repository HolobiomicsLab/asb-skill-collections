---
name: alternative-splicing-event-comparison-across-conditions
description: Use when you have PSI (percent-spliced-in) matrices calculated independently for two or more biological conditions, each with two or more replicate samples, and you want to identify which alternative splicing events show statistically significant changes in inclusion levels between conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_0099
  tools:
  - SUPPA2
derived_from:
- doi: 10.1186/s13059-018-1417-1
  title: suppa2
evidence_spans:
- 'SUPPA2: fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_suppa2
    doi: 10.1186/s13059-018-1417-1
    title: suppa2
  dedup_kept_from: coll_suppa2
schema_version: 0.2.0
---

# alternative-splicing-event-comparison-across-conditions

## Summary

Compute differential splicing statistics (ΔPSI and p-values) across biological conditions by consuming per-condition PSI matrices and transcript expression quantification. This skill applies SUPPA2's uncertainty-aware statistical framework to identify significant changes in exon inclusion between conditions.

## When to use

Apply this skill when you have PSI (percent-spliced-in) matrices calculated independently for two or more biological conditions, each with two or more replicate samples, and you want to identify which alternative splicing events show statistically significant changes in inclusion levels between conditions.

## When NOT to use

- Input data is unpaired or lacks proper replicate structure (fewer than 2 replicates per condition); SUPPA2 requires replicates to estimate the null distribution of ΔPSI.
- PSI matrices are already pre-filtered or transformed; diffSplice expects raw PSI values aligned to consistent event annotations.
- You have only a single sample per condition or single-condition data; differential analysis requires at least two conditions with replicates.

## Inputs

- PSI matrix file per condition (rows: events/transcripts, columns: samples)
- Transcript expression quantification files (e.g., from kallisto, RSEM, or similar)
- Condition labels and replicate group assignments
- Event or isoform annotation (.ioe or .ioi file from generateEvents subcommand)

## Outputs

- Differential PSI table (.dpsi file): event ID, ΔPSI value, p-value, adjusted p-value
- PSI vectors per condition (.psivec file): PSI values for each event across all samples

## How to apply

Load PSI matrix files and transcript expression quantification files for each condition, ensuring replicates are labeled consistently across conditions. Apply the SUPPA2 diffSplice subcommand, which computes per-event ΔPSI (difference in inclusion between conditions) and derives p-values using an uncertainty-aware method that models ΔPSI variation as a function of transcript expression levels or gene expression. For datasets with >10 replicates per condition, you may optionally apply a classical Wilcoxon statistical test instead. Compile results into a differential splicing table reporting event identifiers, ΔPSI magnitudes, and statistical significance metrics (p-values and/or adjusted p-values).

## Related tools

- **SUPPA2** (Computes ΔPSI and p-values for differential splicing analysis via the diffSplice subcommand) — https://github.com/comprna/SUPPA

## Examples

```
python3 suppa.py diffSplice -m PSI -i condition1.psi condition2.psi -e condition1.expression condition2.expression -o output_diff
```

## Evaluation signals

- All events in the output table have a defined ΔPSI value (no missing values) and a corresponding p-value or adjusted p-value.
- ΔPSI magnitudes are bounded to the range [−1, 1], reflecting the theoretical bounds of percent-spliced-in differences.
- Events with low expression (near zero transcript counts) have larger p-values or wider confidence intervals, reflecting higher uncertainty.
- Replicates within each condition show lower variation in PSI than between-condition variation for events flagged as significant.
- The number of significant events (after multiple-testing correction) is reasonable relative to the effect sizes (ΔPSI magnitudes) and sample sizes.

## Limitations

- Requires at least 2 replicates per condition; statistical power decreases with fewer replicates or highly variable samples.
- PSI calculations depend on accurate transcript quantification; errors or biases in expression input propagate to differential PSI estimates.
- Uncertainty-aware p-value calculation assumes that ΔPSI variation correlates with transcript/gene expression; validity may be compromised if expression varies independently of splicing noise.
- Complex splicing variations (e.g., combinatorial exon skipping) are better captured using transcript-level events (ioi format) than local events (ioe format), but transcript events increase multiple-testing burden.

## Evidence

- [other] diffSplice subcommand computation: "Apply the SUPPA2 diffSplice statistical test to compute per-event ΔPSI (difference in percent-spliced-in) between conditions."
- [readme] uncertainty-aware p-value method: "Statistical significance is calculated by comparing the observed ΔPSI between conditions with the distribution of the ΔPSI between replicates as a function of the expression of the transcripts"
- [other] input data requirements: "Load PSI matrix files for each condition and transcript expression quantification files."
- [other] output specification: "Compile results into a single differential splicing table with event identifiers, ΔPSI values, and statistical significance metrics."
- [readme] replicate-based null distribution: "using two or more replicates per condition. Conditions are analyzed in a sequential order specified as input."
