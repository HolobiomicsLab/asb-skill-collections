---
name: gap-filling-algorithm-selection
description: Use when when processing untargeted LC-MS data with SLAW and observing incomplete feature detection across the sample cohort—i.e., features present in some samples but with missing values (zeros or NAs) in others due to signal dropout, retention time drift, or mass calibration drift.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Centwave
  - FeatureFinderMetabo
  - ADAP
  - SLAW
  - xcms (XCMS Online)
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans:
- 'Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw_cq
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02687
  all_source_dois:
  - 10.1021/acs.analchem.1c02687
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gap-filling-algorithm-selection

## Summary

Selection and optimization of gap-filling parameters within untargeted LC-MS workflows to recover missing feature intensities across samples. This skill ensures that features detected in some samples but absent in others are imputed or recovered, improving feature table completeness and reproducibility.

## When to use

When processing untargeted LC-MS data with SLAW and observing incomplete feature detection across the sample cohort—i.e., features present in some samples but with missing values (zeros or NAs) in others due to signal dropout, retention time drift, or mass calibration drift. Apply this skill after peak picking and alignment have been completed but before final feature matrix consolidation.

## When NOT to use

- Input is already a fully consolidated and gap-filled feature matrix with no missing values per sample.
- LC-MS data are profile-mode (non-centroided); SLAW requires centroided mzML input.
- Data include mixed polarity or DIA-MS (Data-Independent Acquisition); SLAW processes DDA only and requires uniform polarity.

## Inputs

- peak-picked feature table (one or more samples, with m/z and retention time coordinates)
- aligned feature table (features matched across samples)
- raw LC-MS mzML files (centroided, DDA, single polarity)
- candidate gap-filling parameter ranges

## Outputs

- consolidated feature table with gap-filled intensities
- optimized gap-filling parameter set
- quality metric scores for each parameter combination tested

## How to apply

Within SLAW's automated parameter optimization loop, gap-filling parameters are iterated alongside peak picking and alignment parameters. For each candidate parameter combination, the workflow applies peak picking with current parameters, then alignment, then gap-filling using data recursion (re-mining raw mzML files at predicted retention time and m/z windows for detected features). Each parameter combination is scored using a quality metric such as feature reproducibility, total number of features detected, or signal-to-noise ratio. The parameter set yielding the highest quality score is selected as the optimized gap-filling configuration. The rationale is that gap-filling by data recursion reconstructs missing intensities by searching raw LC-MS data at feature-specific m/z and retention time windows, thereby recovering low-abundance features that may have been missed in initial peak picking across some samples.

## Related tools

- **SLAW** (Automated parameter optimization framework that wraps gap-filling and selects optimal parameters via quality metric scoring) — https://github.com/zamboni-lab/SLAW
- **xcms (XCMS Online)** (Underlying peak picking and alignment algorithms; gap-filling logic integrated into SLAW's parameter search)

## Examples

```
docker run --rm -v /path/to/mzML:/input -v /path/to/output:/output zambonilab/slaw:latest
```

## Evaluation signals

- Optimized gap-filling parameter set converges to a single best combination (higher quality score than random or default parameters).
- Feature count in final peaktable increases after gap-filling relative to pre-gap-filling peak table, indicating recovery of missing features.
- Feature reproducibility (e.g., detection rate across QC replicates) improves after gap-filling; QC samples show consistent feature presence.
- No introduction of spurious features or artifactual intensities; re-mined intensities align with expected m/z and retention time coordinates within feature tolerance.
- Signal-to-noise ratio and intensity distribution of gap-filled features are consistent with non-gap-filled features in the same feature table.

## Limitations

- Optimization is performed on QC samples only; parameter set optimized for QC may not generalize to all sample types (e.g., blanks or study samples with different metabolite distributions).
- Gap-filling by data recursion requires raw mzML files to be retained; processing speed scales with total number of raw MS scans and candidate parameter combinations.
- DIA-MS and profile-mode data are not supported; centroided, DDA mzML input is mandatory.
- Optimization can be disabled for speed; if turned off, SLAW applies default gap-filling parameters rather than dataset-specific optimized ones.
- Low-abundance or noisy features recovered by gap-filling may increase false-positive detection rates if quality thresholds are not stringent.

## Evidence

- [intro] SLAW applies automated parameter optimization to peak picking, alignment, and gap-filling parameters, producing an optimized parameter set for processing untargeted LC-MS data.: "SLAW applies automated parameter optimization to peak picking, alignment, and gap-filling parameters, producing an optimized parameter set for processing untargeted LC-MS data."
- [other] Execute parameter optimization loop: iterate through candidate parameter combinations, applying peak picking with current parameters, then alignment and gap-filling. Evaluate each parameter combination using a quality metric (e.g., feature reproducibility, number of features detected, or signal-to-noise ratio) to score the LC-MS processing outcome.: "Execute parameter optimization loop: iterate through candidate parameter combinations, applying peak picking with current parameters, then alignment and gap-filling. Evaluate each parameter"
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic data: "Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic"
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."
- [readme] SLAW can process thousands of SAMPLES efficiently: "SLAW can process thousands of SAMPLES efficiently"
