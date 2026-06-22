---
name: feature-table-comparison-analysis
description: Use when after running Paramounter's peak-height optimization on XCMS CentWave–extracted metabolomic features when you need to decide whether to accept the optimized threshold (maximizing true positives) or apply a higher threshold to reduce false positives and software crashes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Paramounter
  - XCMS CentWave
derived_from:
- doi: 10.1021/acs.analchem.1c04758
  title: Paramounter
evidence_spans:
- github.com/HuanLab/Paramounter
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_paramounter_cq
    doi: 10.1021/acs.analchem.1c04758
    title: Paramounter
  dedup_kept_from: coll_paramounter_cq
schema_version: 0.2.0
---

# feature-table-comparison-analysis

## Summary

Compare feature extraction outputs from metabolomic data under different peak-height thresholds to evaluate the tradeoff between true positive recovery and false positive suppression. This skill quantifies how mitigation strategies (e.g., 2× peak-height adjustment) affect feature table quality, stability, and crash likelihood.

## When to use

Apply this skill after running Paramounter's peak-height optimization on XCMS CentWave–extracted metabolomic features when you need to decide whether to accept the optimized threshold (maximizing true positives) or apply a higher threshold to reduce false positives and software crashes. Use it specifically when comparing an optimized feature table against a mitigated (elevated threshold) variant to assess the cost–benefit of each approach for your downstream analysis.

## When NOT to use

- Input is already a final, validated feature table — comparison analysis is a pre-validation step, not a post-hoc quality check.
- No optimized peak-height threshold has been computed by Paramounter yet — run Paramounter first before attempting comparison.
- The analysis goal does not require balancing true positive recovery against false positive suppression (e.g., if false positives are acceptable or true positive sensitivity is not a concern).

## Inputs

- raw metabolomic data (NetCDF, mzML, or compatible format)
- XCMS CentWave feature extraction parameters
- Paramounter-computed optimized peak-height threshold

## Outputs

- feature table extracted with optimized peak-height threshold (with true positive, false positive, and crash statistics)
- feature table extracted with mitigated (2×) peak-height threshold (with true positive, false positive, and crash statistics)
- comparative summary report quantifying tradeoffs between the two extraction strategies

## How to apply

Load raw metabolomic data and run XCMS CentWave feature extraction with initial parameters. Use Paramounter to compute the optimized peak-height threshold that maximizes true positive feature count. Apply this optimized threshold to extract an initial feature set, producing the baseline feature table. Then multiply the optimized peak-height threshold by a mitigation factor (e.g., 2×) and re-extract features using the elevated threshold. Generate summary statistics for both tables, including counts of true positives, false positives, and extraction stability metrics (e.g., crash frequency). Compare the two feature tables side-by-side using these metrics to determine whether the gain in true positives from the optimized threshold justifies the higher false positive rate and crash risk, or whether the 2×-mitigated threshold provides acceptable tradeoffs for your analysis goals.

## Related tools

- **XCMS CentWave** (performs initial feature extraction from raw metabolomic data; provides raw feature set for Paramounter optimization and re-extraction with mitigated thresholds)
- **Paramounter** (computes optimized peak-height threshold maximizing true positive features; enables threshold multiplication and re-extraction for mitigation comparison) — github.com/HuanLab/Paramounter

## Evaluation signals

- Both feature tables (optimized and 2×-mitigated) are successfully generated from the same raw data using identical XCMS CentWave parameters except for peak-height threshold.
- Summary statistics are computed for each table, with explicit counts or proportions of true positives, false positives, and software crashes; the 2×-mitigated table shows lower false positive rate and crash likelihood than the optimized table.
- True positive count in the optimized table is equal to or greater than in the 2×-mitigated table, confirming the expected tradeoff direction.
- Comparison report is human-readable and presents metrics in comparable units (e.g., counts, percentages, or rates) to enable decision-making between the two strategies.
- Dereplication parameters (mzdiff tolerance) are held constant across both extractions so that threshold differences alone drive the observed feature table divergence.

## Limitations

- True positive and false positive ground truth must be available (e.g., from validated metabolite libraries or orthogonal detection) to compute summary statistics; the workflow does not infer ground truth from the feature tables alone.
- The 2× mitigation factor is a heuristic starting point; optimal threshold multiplication may vary by dataset, instrument, or metabolite class and should be tuned empirically.
- Software crash likelihood is reported qualitatively or as a frequency count; causality between peak-height threshold and crashes cannot be established from this workflow alone without controlled experimentation.
- Dereplication-related signal loss (true positives removed due to mzdiff tolerance below the mass difference of co-eluting features) is a separate issue from peak-height optimization and requires independent mitigation (e.g., setting mzdiff to a negative value to disable dereplication).

## Evidence

- [other] Paramounter tunes an optimized peak height to maximize true positive features, but users can mitigate the resulting higher false positive rate and crash likelihood by applying a higher peak height threshold, such as 2X the optimized peak height threshold.: "Paramounter tunes an optimized peak height to maximize true positive features, but users can mitigate the resulting higher false positive rate and crash likelihood by applying a higher peak height"
- [other] 1. Load raw metabolomic data and run XCMS CentWave feature extraction with initial parameters. 2. Use Paramounter to compute the optimized peak-height threshold that maximizes the count of true positive features. 3. Apply the optimized threshold to extract an initial feature set. 4. Multiply the optimized peak-height threshold by 2× as a mitigation factor. 5. Re-extract features using the elevated threshold and compare the false positive rate and crash likelihood against the non-mitigated result. 6. Output both feature tables (optimized and 2×-mitigated) with summary statistics on true positives, false positives, and extraction stability.: "1. Load raw metabolomic data and run XCMS CentWave feature extraction with initial parameters. 2. Use Paramounter to compute the optimized peak-height threshold that maximizes the count of true"
- [readme] Paramounter tunes an optimized peak height to maximize the number of true positive features. A drawback of that optimized value is the higher rate of false positive features and the likelihood of software crash.: "Paramounter tunes an optimized peak height to maximize the number of true positive features. A drawback of that optimized value is the higher rate of false positive features and the likelihood of"
- [readme] users can try a higher peak height threshold to reduce the number of false positive features (e.g., 2X the optimized peak height threshold).: "users can try a higher peak height threshold to reduce the number of false positive features (e.g., 2X the optimized peak height threshold)."
