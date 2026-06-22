---
name: qc-sample-batch-drift-correction
description: Use when you have a QC-annotated feature table (samples × features with QC sample identifiers) from LC-MS untargeted metabolomic profiling and observe systematic signal drift across the run sequence or between batch blocks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetCorR
  - R
  - OUKS
derived_from:
- doi: 10.1021/acs.jproteome.1c00392
  title: Omics Untargeted Key Script
evidence_spans:
- New QC-GAM method (MetCorR) with associated scripts were introduced.
- R based open-source collection of scripts called :red_circle:*OUKS*
- R ≥4.1.2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omics_untargeted_key_script_cq
    doi: 10.1021/acs.jproteome.1c00392
    title: Omics Untargeted Key Script
  dedup_kept_from: coll_omics_untargeted_key_script_cq
schema_version: 0.2.0
---

# QC-Sample Batch Drift Correction

## Summary

Correct run-order and batch-dependent signal drift in LC-MS untargeted metabolomic feature tables using QC samples as reference points and Generalized Additive Models (GAM). This skill removes systematic variation introduced during sample acquisition while preserving biological signals.

## When to use

Apply this skill when you have a QC-annotated feature table (samples × features with QC sample identifiers) from LC-MS untargeted metabolomic profiling and observe systematic signal drift across the run sequence or between batch blocks. Use it after integration and imputation steps, before annotation or filtering, to ensure that downstream statistical comparisons are not confounded by instrumental signal decay or batch effects.

## When NOT to use

- Feature table lacks QC sample replicates — the method requires QC samples distributed across the run order to model drift trends.
- Input data are already corrected by instrument software or alternative methods — applying MetCorR on pre-corrected data may introduce circular bias.
- Batch effect is driven by biological group membership rather than technical run conditions — use alternative batch correction (e.g., ComBat) for biological confounding.

## Inputs

- QC-annotated feature intensity table (samples × features, numeric values)
- Sample metadata with run order (integer sequence) and batch block identifiers (categorical)
- QC sample labels to identify reference samples within metadata

## Outputs

- Corrected feature intensity table (same dimensions as input, numeric values)
- Correction factors per feature (numeric coefficients)
- Diagnostic plots (RLA-plot, intensity trajectories) showing drift removal

## How to apply

Load the QC-annotated feature table into R along with sample metadata (run order and batch identifiers). Execute the MetCorR QC-GAM algorithm by fitting Generalized Additive Models on QC sample intensities, with run order and batch as smooth terms to estimate correction factors for each feature. The algorithm models batch-dependent signal drift by using QC samples as reference points across the run sequence, then applies fitted correction factors to all sample features. Output the corrected feature table in CSV format, preserving sample and feature identifiers. Success is indicated by visual flattening of intensity trajectories in diagnostic plots (e.g., RLA-plot comparing before/after correction).

## Related tools

- **MetCorR** (Primary package implementing QC-GAM correction algorithm with run-order and batch smoothing terms) — https://github.com/plyush1993/MetCorR
- **R** (Runtime environment (≥4.1.2) for executing MetCorR package and feature table I/O) — https://cran.r-project.org/
- **OUKS** (Complete untargeted metabolomics workflow; MetCorR is integrated as step 4 (Correction)) — https://github.com/plyush1993/OUKS

## Examples

```
library(MetCorR); data(example_intensity); data(example_meta); out <- MetCorR(method=2, int_data=example_intensity, order=example_meta$order, class=example_meta$class, batch=example_meta$batch, qc_label="QC")
```

## Evaluation signals

- RLA-plot (Relative Log Abundance) shows mean intensity near zero post-correction, with reduced spread across run order compared to pre-correction
- Intensity trajectories of QC features flatten over run sequence; slope magnitude decreases after correction
- Corrected feature table has no negative values (if original was non-negative); preserves feature and sample identifiers
- D-Ratio metric (technical/biological variance ratio) improves post-correction; correlogram shows stronger biological clustering
- Feature correlation patterns match expected biology (e.g., co-regulated metabolite clusters) rather than reflecting run-order trends

## Limitations

- Requires QC samples to be well-distributed across the entire run order; sparse QC placement may produce unreliable trend estimates
- GAM fitting assumes smoothness in drift trajectory; abrupt instrumental failures or sudden batch shifts may not be adequately captured
- Method is designed for LC-MS untargeted metabolomics; applicability to other omics (e.g., GC-MS, proteomics) not validated in the article
- No explicit documentation of sensitivity to GAM hyperparameters (spline degrees of freedom) or guidance on parameter tuning
- Original article lacks validation on independent datasets or comparative benchmarking against other QC-based correction methods

## Evidence

- [other] Load QC-annotated feature table and run MetCorR: "Load the QC-annotated feature table (samples × features with QC sample identifiers) into R. 2. Execute the MetCorR QC-GAM correction algorithm via the MetCorR package, which models batch-dependent"
- [other] Apply correction factors to all features: "Apply the fitted correction factors to all feature abundances across the entire table. 4. Output the corrected feature table in CSV or tabular format, preserving sample and feature identifiers."
- [readme] MetCorR method overview: "MetCorR - QC-based metabolomic LC-MS signal drift correction using GAMs"
- [readme] MetCorR integration in workflow: ""4. Correction": D-Ratio metric, RLA-plot, correlogram, 2-factors PCA"
- [readme] Example invocation pattern: "out <- MetCorR( method = 2, int_data = example_intensity, order = example_meta$order, class = example_meta$class, batch = example_meta$batch, qc_label = "QC" )"
