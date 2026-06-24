---
name: mass-spectrometry-benchmark-analysis
description: Use when you have implemented or modified a tandem mass spectrometry
  formula inference model and need to measure whether a specific architectural change
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0601
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - MIST
  - MIST-CF
  - SIRIUS
  - SCARF
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum
  using an end-to-end energy based modeling approach
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-benchmark-analysis

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantitatively evaluate chemical formula ranking accuracy and adduct assignment performance across MS/MS inference methods using standardized benchmark datasets and ranking metrics. This skill isolates the contribution of individual model innovations (e.g., multi-adduct support) by computing top-k accuracy deltas against controlled baseline modes.

## When to use

You have implemented or modified a tandem mass spectrometry formula inference model and need to measure whether a specific architectural change (e.g., enabling multi-adduct support, switching from fragmentation trees to transformer networks) improves formula-adduct ranking accuracy relative to a restricted baseline or competing tool. Apply this skill when you have a published or standardized benchmark dataset with ground-truth formula and adduct annotations.

## When NOT to use

- Input spectra lack corresponding ground-truth formula or adduct labels — benchmarking requires annotated reference data.
- You are evaluating model performance on the same dataset used for training; use a held-out test or external benchmark (e.g., CASMI22) to avoid inflated accuracy estimates.
- Your goal is to rank spectra by confidence or filter low-quality spectra rather than compare competing formula ranking models — use filtering or scoring workflows instead.

## Inputs

- MS/MS spectra in MGF or equivalent format
- Benchmark dataset with ground-truth formula annotations
- Ground-truth adduct type assignments
- Model weights or trained checkpoint
- Configuration YAML specifying inference mode (e.g., single vs. multi-adduct)

## Outputs

- Ranked formula predictions (scored list per spectrum)
- Ranked adduct assignments per spectrum
- Top-1 and top-k accuracy metrics for each mode
- Performance delta report (accuracy improvement by feature)
- Per-spectrum and aggregate comparison table

## How to apply

Load a benchmark dataset (e.g., NPLIB1, NIST20, or CASMI22) with MS/MS spectra annotated with correct formula and adduct type. Run inference on the same spectra twice: once in restricted mode (e.g., [M+H]+ only) and once in full mode (e.g., multi-adduct energy-based ranking). For each run, record ranked formula-adduct pair predictions. Compute ranking accuracy metrics (top-1 and top-k correct pair identification rates) for both modes. Calculate the performance delta (full mode accuracy minus restricted mode accuracy) to isolate the contribution of the specific feature. Generate a comparison report listing accuracy improvements, failure modes, and dataset-specific patterns.

## Related tools

- **MIST-CF** (End-to-end energy-based chemical formula inference model supporting multi-adduct ranking; used to generate ranked predictions in full-mode and restricted-mode configurations for delta comparison.) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Baseline formula enumeration and fragmentation tree method used for comparison and to generate candidate formula lists via SIRIUS decomp dynamic programming.) — https://bio.informatik.uni-jena.de/software/sirius/
- **SCARF** (Sinusoidal formula embedding technique integrated into MIST-CF architecture; enables comparison of embedding-based vs. tree-based formula ranking.) — https://arxiv.org/abs/2303.06470

## Examples

```
python run_scripts/benchmarking/eval_models.py --config configs/mist_cf_canopus.yaml --test_data data/canopus_train/test_split.csv --output_dir results/ --restricted_mode [M+H]_only
```

## Evaluation signals

- Top-1 accuracy (fraction of spectra with correct formula-adduct pair ranked first) is higher in full mode than restricted mode; delta is quantifiable and statistically meaningful.
- Top-k accuracy curves (k=1–5, 1–10) are monotonically increasing and show steeper improvement in full mode, indicating the feature enables better ranking discrimination.
- Per-spectrum rankings are reproducible: running inference twice on the same spectrum produces identical ranked lists and scores.
- Formula-adduct pairs in the top-k predictions are chemically plausible (correct monoisotopic mass, consistent with adduct ionization rules) even when not top-1.
- Performance delta is consistent across dataset partitions (e.g., multiple folds, different adduct subsets, different m/z ranges) and does not reflect overfitting to a single spectrum subset.

## Limitations

- Multi-adduct support in MIST-CF is limited to positive-mode ionization; negative-mode or mixed-polarity datasets will not benefit from adduct diversity.
- Benchmark performance on public data (NPLIB1) may not transfer to proprietary datasets (NIST20) due to spectrum preprocessing, instrument type, and intensity distribution differences; model trained on NIST20 is reportedly more performant but available only under license.
- Ranking accuracy depends on the candidate formula list enumerated by SIRIUS decomp; if the ground-truth formula is not in the candidate set, both restricted and full modes will fail to rank it, masking upstream enumeration errors.
- Top-k metrics require a choice of k; small k values (k=1–3) may underestimate practical utility for high-throughput screening where top-10 predictions are acceptable.

## Evidence

- [other] What is the performance improvement in chemical formula ranking accuracy when MIST-CF incorporates support for multiple adduct types compared to restricting predictions to [M+H]+ only?: "What is the performance improvement in chemical formula ranking accuracy when MIST-CF incorporates support for multiple adduct types compared to restricting predictions to [M+H]+ only?"
- [other] Run MIST-CF inference in [M+H]+-only mode, restricting the model to rank formulas without multi-adduct support, and record ranked formula predictions and adduct assignments.: "Run MIST-CF inference in [M+H]+-only mode, restricting the model to rank formulas without multi-adduct support, and record ranked formula predictions and adduct assignments."
- [other] Compute ranking accuracy metrics (top-1 and top-k correct formula-adduct pair identification) for both modes.: "Compute ranking accuracy metrics (top-1 and top-k correct formula-adduct pair identification) for both modes."
- [other] Calculate the performance delta (multi-adduct accuracy minus [M+H]+-only accuracy) to isolate MULTI_ADDUCT_SUPPORT contribution and generate a comparison report.: "Calculate the performance delta (multi-adduct accuracy minus [M+H]+-only accuracy) to isolate MULTI_ADDUCT_SUPPORT contribution and generate a comparison report."
- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [other] Load the published benchmark dataset containing MS/MS spectra with known formula and adduct ground truth.: "Load the published benchmark dataset containing MS/MS spectra with known formula and adduct ground truth."
- [other] Run MIST-CF inference in full multi-adduct mode using the complete energy-based modeling approach, allowing ranking across multiple positive-mode adduct types, and record ranked predictions.: "Run MIST-CF inference in full multi-adduct mode using the complete energy-based modeling approach, allowing ranking across multiple positive-mode adduct types, and record ranked predictions."
