---
name: differential-splicing-statistical-testing
description: Use when you have PSI (percent-spliced-in) matrices for multiple samples grouped into two or more biological conditions, along with corresponding transcript expression quantification, and need to identify events or transcripts with statistically significant changes in inclusion levels between.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_0203
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

# differential-splicing-statistical-testing

## Summary

Statistical testing of differential splicing across multiple conditions by computing per-event ΔPSI (delta percent-spliced-in) values and their significance from PSI matrices and transcript expression data. This skill quantifies the magnitude and statistical significance of splicing changes between biological conditions using uncertainty-aware methods.

## When to use

Use this skill when you have PSI (percent-spliced-in) matrices for multiple samples grouped into two or more biological conditions, along with corresponding transcript expression quantification, and need to identify events or transcripts with statistically significant changes in inclusion levels between conditions with replicates (≥2 replicates per condition).

## When NOT to use

- Input samples lack clear biological replicates (≥2 per condition required for uncertainty estimation)
- PSI matrices already contain pre-computed differential statistics rather than raw per-sample values
- Study design involves only single time points or unpaired samples without condition grouping

## Inputs

- PSI matrix files (per-condition, event-level or isoform-level)
- Transcript expression quantification files (TPM, counts, or abundance estimates)
- Condition grouping specification (sample-to-condition assignments)

## Outputs

- Differential splicing results table with event/transcript identifiers, ΔPSI values, and p-values
- Per-sample PSI vectors (.psivec file format)

## How to apply

Load PSI matrix files for each condition and corresponding transcript expression quantification files. Align samples across conditions and normalize expression values if needed. Apply the SUPPA2 diffSplice statistical test to compute per-event ΔPSI between conditions, comparing the observed ΔPSI with the distribution of ΔPSI between replicates as a function of transcript expression. Calculate p-values for each event using the uncertainty-aware method; for studies with >10 replicates per condition, classical statistical tests (e.g., Wilcoxon) can be used instead. Compile results into a differential splicing table containing event identifiers, ΔPSI values, and statistical significance metrics for downstream interpretation.

## Related tools

- **SUPPA2** (implements diffSplice subcommand for computing differential splicing statistics with uncertainty-aware p-values from PSI matrices and expression data) — https://github.com/comprna/SUPPA

## Examples

```
python3.4 suppa.py diffSplice -m PSI -i condition1_PSI.psi condition2_PSI.psi -e condition1_expression.txt condition2_expression.txt -o differential_splicing_results
```

## Evaluation signals

- ΔPSI values fall within the expected range [−1.0, 1.0] for all events tested
- P-values are properly calibrated (no p-value = 0; uniform distribution under null hypothesis)
- Events with large |ΔPSI| (e.g., >0.3) corresponding to small p-values; low |ΔPSI| events have non-significant p-values
- Significance distribution differs between replicates (internal noise floor) and between-condition comparisons
- Results include all events present in input annotation; no expected events missing from output table

## Limitations

- Requires minimum of 2 replicates per condition to estimate uncertainty; power increases with more replicates
- Relies on accurate upstream PSI quantification—errors in transcript expression or event definition propagate to statistical results
- Method assumes PSI values and expression data are properly normalized; batch effects or library size differences must be corrected beforehand
- Classical statistical tests (Wilcoxon) are only recommended when >10 replicates per condition; smaller sample sizes rely on uncertainty-aware method
- Complex splicing patterns not captured by simple local events may be missed when using ioe (local events) rather than ioi (transcript isoforms)

## Evidence

- [readme] Statistical significance is calculated by comparing the observed ΔPSI between conditions with the distribution of the ΔPSI between replicates as a function of the expression of the transcripts defining the events: "Statistical significance is calculated by comparing the observed ΔPSI between conditions with the distribution of the ΔPSI between replicates as a function of the expression of the transcripts"
- [other] SUPPA2 performs fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions by consuming PSI matrices and expression data to generate differential splicing results: "SUPPA2 performs fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions"
- [other] Apply the SUPPA2 diffSplice statistical test to compute per-event ΔPSI (difference in percent-spliced-in) between conditions. Calculate p-values for each event using the uncertainty-aware method: "Apply the SUPPA2 diffSplice statistical test to compute per-event ΔPSI (difference in percent-spliced-in) between conditions. Calculate p-values for each event using the uncertainty-aware method"
- [readme] When there is a large (>10) number of replicates per condition, you can also run SUPPA with a classical statistical test (Wilcoxon) per local event or per transcript: "When there is a large (>10) number of replicates per condition, you can also run SUPPA with a classical statistical test (Wilcoxon)"
