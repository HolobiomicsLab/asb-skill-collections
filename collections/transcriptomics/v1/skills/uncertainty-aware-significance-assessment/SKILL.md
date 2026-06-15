---
name: uncertainty-aware-significance-assessment
description: Use when you have PSI matrices for two or more conditions with replicates per condition, and you need to determine which alternative splicing events show significant changes between conditions while accounting for measurement uncertainty that scales with transcript expression levels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_3308
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

# Uncertainty-aware significance assessment

## Summary

Assess statistical significance of differential splicing events by comparing observed changes (ΔPSI) against the distribution of within-replicate variation, accounting for transcript expression uncertainty. This method provides calibrated p-values that reflect biological noise rather than assuming constant variance across expression levels.

## When to use

You have PSI matrices for two or more conditions with replicates per condition, and you need to determine which alternative splicing events show significant changes between conditions while accounting for measurement uncertainty that scales with transcript expression levels.

## When NOT to use

- Samples are unpaired or replicate structure is unclear — the method requires at least 2 replicates per condition to estimate within-condition variance
- Input PSI values are already aggregated across replicates — the method requires individual per-sample PSI and expression values
- You only have a single biological condition — differential analysis requires two or more distinct conditions

## Inputs

- PSI matrix files (one per condition, rows = events, columns = samples)
- Transcript expression quantification files (TPM or equivalent units, one per sample)
- Sample-to-condition mapping and replicate structure

## Outputs

- Differential splicing table with event identifiers, ΔPSI values, p-values, and optional adjusted significance thresholds

## How to apply

Load PSI matrices and transcript expression quantification for each replicate within each condition. Compute the observed ΔPSI (difference in percent-spliced-in) between conditions for each event. Generate a null distribution of ΔPSI values by computing pairwise ΔPSI across replicates within each condition, stratified by expression level of transcripts defining the event. Compare the observed ΔPSI against this empirical null distribution to derive a p-value that accounts for expression-dependent measurement noise. For large replicate counts (>10 per condition), alternative classical tests such as Wilcoxon rank-sum can be applied instead of the empirical distribution method.

## Related tools

- **SUPPA2** (Computes differential splicing statistics (ΔPSI and uncertainty-aware p-values) from PSI matrices and expression data via the diffSplice subcommand) — https://github.com/comprna/SUPPA

## Examples

```
python3 suppa.py diffSplice -m psiPerEvent -i condition1.psi condition2.psi -e condition1.exp condition2.exp -o diff_splicing_results
```

## Evaluation signals

- Output p-values should span a range from near-zero to 1.0 and show calibration (not uniform or heavily left-skewed) when plotted as a histogram or Q-Q plot against expected null distribution
- Events with small ΔPSI but high expression should yield higher p-values than events with large ΔPSI and similar expression, demonstrating expression-dependent filtering
- Replicates within a condition should show small mean ΔPSI (close to zero) with p-values predominantly > 0.05, validating that within-condition variation is properly captured
- Results should be reproducible across independent runs with the same input data and parameters
- When using classical Wilcoxon test on high-replicate datasets (>10 per condition), p-values should correlate strongly with empirical distribution-based p-values, showing method consistency

## Limitations

- Requires minimum 2 replicates per condition; with fewer replicates, the empirical null distribution becomes sparse and p-values unreliable
- Assumes transcript expression measurements are reasonably accurate; severe quantification bias will inflate or deflate the expression-dependent variance estimate
- PSI values are bounded [0,1], creating distributional challenges near boundaries; the method may be less sensitive for events with mean PSI < 0.1 or > 0.9
- Computational cost scales with number of replicates and events; large studies (>500 samples, >100k events) may require memory optimization
- Does not account for isoform-level quantification uncertainty if using summary-level expression proxies (e.g., gene-level counts) rather than transcript-level abundances

## Evidence

- [readme] Statistical significance is calculated by comparing the observed ΔPSI between conditions with the distribution of the ΔPSI between replicates as a function of the expression of the transcripts defining the events: "Statistical significance is calculated by comparing the observed ΔPSI between conditions with the distribution of the ΔPSI between replicates as a function of the expression of the transcripts"
- [readme] SUPPA2: fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions: "SUPPA2: fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions"
- [readme] When there is a large (>10) number of replicates per condition, you can also run SUPPA with a classical statistical test (Wilcoxon) per local event or per transcript: "When there is a large (>10) number of replicates per condition, you can also run SUPPA with a classical statistical test (Wilcoxon) per local event or per transcript"
- [other] Calculate p-values for each event using the uncertainty-aware method implemented in SUPPA2: "Calculate p-values for each event using the uncertainty-aware method implemented in SUPPA2"
- [other] Apply the SUPPA2 diffSplice statistical test to compute per-event ΔPSI (difference in percent-spliced-in) between conditions: "Apply the SUPPA2 diffSplice statistical test to compute per-event ΔPSI (difference in percent-spliced-in) between conditions"
