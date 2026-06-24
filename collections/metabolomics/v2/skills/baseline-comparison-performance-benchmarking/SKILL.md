---
name: baseline-comparison-performance-benchmarking
description: 'Use when when you have implemented a novel annotation algorithm or network
  and must verify it outperforms a simpler reference approach on held-out or independent
  spectral data. Specifically: (1) you have ground-truth annotations for a common
  test set;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - XCMS
  - CAMERA
  - LipidIN EQ Module
  - LipidIN Wide-spectrum Modeling Yield (WMY) network
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification.'
- 'CAMERA: an'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidin_cq
    doi: 10.1038/s41467-025-59683-5
    title: LipidIN
  dedup_kept_from: coll_lipidin_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-59683-5
  all_source_dois:
  - 10.1038/s41467-025-59683-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# baseline-comparison-performance-benchmarking

## Summary

Quantitatively compare a candidate annotation method against a reference baseline by computing precision, recall, and coverage metrics on the same spectral dataset, then calculating relative improvement as a percentage to verify achievement of a target performance threshold. This skill validates whether a novel approach (e.g., neural network fingerprint regeneration) delivers claimed gains over simpler methods (e.g., spectral library matching alone).

## When to use

When you have implemented a novel annotation algorithm or network and must verify it outperforms a simpler reference approach on held-out or independent spectral data. Specifically: (1) you have ground-truth annotations for a common test set; (2) you can run both the baseline method and the candidate method on that same set; (3) you have a quantitative success criterion (e.g., '~20% recall boost') and need to measure whether it is met. Do NOT use this skill if you lack ground-truth labels or cannot execute both methods on identical inputs.

## When NOT to use

- Input spectral dataset lacks ground-truth lipid annotations; baseline and candidate methods are applied to different subsets of data.
- Baseline method has not been benchmarked or validated independently; its reference performance is unknown or unstable.
- Candidate method is designed for a different ionization mode, lipid class, or MS instrument type than the baseline; direct comparison is confounded by these factors.

## Inputs

- MS/MS spectral data in mzML format (or preprocessed .rda format after XCMS/RaMS preprocessing)
- Initial baseline annotations from spectral library matching (e.g., EQ module output)
- Ground-truth lipid identities with structural metadata (chain composition, double bond positions)
- Candidate method predictions with confidence scores or probability outputs

## Outputs

- Baseline recall, precision, coverage scores
- Candidate method recall, precision, coverage scores
- Relative improvement percentages for each metric
- Boolean pass/fail outcome against target threshold
- Confidence intervals or cross-validation fold statistics

## How to apply

Load processed MS/MS spectral data with initial (baseline) annotations from spectral library matching. Execute the baseline annotation workflow to obtain baseline recall, precision, and coverage. Then execute the candidate method (e.g., Wide-spectrum Modeling Yield network) on the same spectral inputs to obtain candidate predictions with confidence scores. For each metric, compute the relative improvement as (candidate_metric − baseline_metric) / baseline_metric × 100%. Compare the observed improvement against the target threshold (e.g., 20% recall boost). Document whether the threshold is met and report 95% confidence intervals or cross-validation folds to assess reproducibility. Ground-truth lipid identities must be consistent across both runs to ensure fair comparison.

## Related tools

- **XCMS** (Processes mass spectrometry data for nonlinear peak alignment, matching, and initial peak detection prior to baseline annotation) — https://bioconductor.org/packages/XCMS/
- **CAMERA** (Integrated strategy for compound spectra extraction and annotation of LC/MS data to support spectral library matching baseline) — https://bioconductor.org/packages/CAMERA/
- **LipidIN EQ Module** (Performs spectral querying against lipid fragmentation library to generate baseline annotations for comparison) — https://github.com/LinShuhaiLAB/LipidIN
- **LipidIN Wide-spectrum Modeling Yield (WMY) network** (Candidate method that regenerates lipid fingerprints to produce enhanced predictions compared to baseline spectral matching) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
# Load baseline annotations and candidate WMY predictions, then compute metrics
recall_baseline <- sum(baseline_match & truth) / sum(truth)
recall_wmy <- sum(wmy_match & truth) / sum(truth)
improvement_pct <- (recall_wmy - recall_baseline) / recall_baseline * 100
if (improvement_pct >= 20) { print("Target 20% recall boost ACHIEVED") } else { print("Target NOT met") }
```

## Evaluation signals

- Baseline and candidate methods produce scores for all samples in the test set without errors or missing values; no samples are excluded from either pipeline.
- Recall, precision, and coverage metrics are computed identically for both baseline and candidate (e.g., same denominator definition, same ground-truth label source).
- Relative improvement percentage for the primary metric (e.g., recall) meets or exceeds the stated target threshold (e.g., ≥20% boost); cross-validation or bootstrap confidence intervals do not overlap zero.
- Precision and coverage do not degrade substantially in the candidate method; if one metric improves, others are held or improve in parallel (no single-metric cherry-picking).
- Results are reproducible across multiple random seeds, cross-validation folds, or independent test cohorts; no overfitting to the evaluation set is evident.

## Limitations

- Comparison is valid only for lipid classes and ionization modes (positive, negative [M+CH3COO]−, [M+COOH]−) represented in both baseline and candidate training data; performance gains may not generalize to unseen lipid types or instrument platforms.
- Ground-truth annotations must be curated and internally consistent; errors or ambiguities in ground truth propagate to both baseline and candidate measurements, potentially masking or inflating true performance differences.
- The Wide-spectrum Modeling Yield network requires pre-trained weights or sufficient labeled data for training; if weights are unavailable or training data is small, candidate method performance may degrade, yielding unfair comparison.
- Relative improvement is a ratio metric and can be misleading if baseline performance is already very high (e.g., 95% recall); report absolute improvements and effect sizes alongside percentages.
- Cross-species or multi-instrument validation is not provided in the LipidIN README; claimed 20% recall boost is observed in reported experiments but reproducibility on independent cohorts is not yet established.

## Evidence

- [other] Does applying the Wide-spectrum Modeling Yield (WMY) network to regenerate lipid fingerprints produce the reported ~20% estimated recall boost in lipid annotation coverage and accuracy?: "research_question: Does applying the Wide-spectrum Modeling Yield (WMY) network to regenerate lipid fingerprints produce the reported ~20% estimated recall boost in lipid annotation coverage and"
- [other] Compare regenerated fingerprints against baseline spectral-matching-only annotations to calculate recall, precision, and coverage metrics. Compute estimated recall boost as (recall_wmy − recall_baseline) / recall_baseline × 100% and verify achievement of ~20% improvement threshold.: "4. Compare regenerated fingerprints against baseline spectral-matching-only annotations to calculate recall, precision, and coverage metrics. 5. Compute estimated recall boost as (recall_wmy −"
- [readme] Wide-spectrum Modeling Yield network for regenerating lipid fingerprints to further improve coverage and accuracy with a 20% estimated recall boosting: "LipidIN integrates a Wide-spectrum Modeling Yield network for regenerating lipid fingerprints to further improve coverage and accuracy with a 20% estimated recall boosting."
- [readme] The application of LipidIN in multiple tasks demonstrated reliability and potential for lipid annotation and biomarker discovery.: "The application of LipidIN in multiple tasks demonstrated reliability and potential for lipid annotation and biomarker discovery."
