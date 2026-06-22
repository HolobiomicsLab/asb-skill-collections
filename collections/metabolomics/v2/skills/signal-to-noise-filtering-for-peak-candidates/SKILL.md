---
name: signal-to-noise-filtering-for-peak-candidates
description: Use when immediately after peak detection in the IDSL.IPA workflow, when you have a list of candidate peaks extracted from EIC data and need to remove noise-dominated signals before downstream peak property evaluation and annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - IDSL.IPA
  - R
  - xcms
  - MZmine 2
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.jproteome.2c00120
  title: IDSL.IPA
evidence_spans:
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight R package'
- light-weight R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_ipa_cq
    doi: 10.1021/acs.jproteome.2c00120
    title: IDSL.IPA
  dedup_kept_from: coll_idsl_ipa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00120
  all_source_dois:
  - 10.1021/acs.jproteome.2c00120
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# signal-to-noise-filtering-for-peak-candidates

## Summary

Filter detected peaks from LC/HRMS EIC candidates using signal-to-noise ratio (S/N) thresholds to remove low-confidence detections and retain only chemically meaningful signals. This skill is critical for reducing false positives in untargeted metabolomics workflows where peak detection must operate across thousands of m/z traces.

## When to use

Apply this skill immediately after peak detection in the IDSL.IPA workflow, when you have a list of candidate peaks extracted from EIC data and need to remove noise-dominated signals before downstream peak property evaluation and annotation. Use it whenever S/N falls below acceptable thresholds (typically user-configurable) or when peak detection has generated spurious candidates from chromatographic baseline noise or instrument artifact.

## When NOT to use

- Targeted analysis with known peak locations (m/z–RT pairs): use IDSL.IPA's IPA_targeted function instead of general peak detection filtering.
- Data already pre-filtered or from instruments with very low baseline noise: verify S/N filtering is not double-filtering and removing true signals.
- Comparisons across studies with different instrumental S/N profiles: ensure S/N thresholds are instrument-calibrated or harmonized before pooling results.

## Inputs

- Detected peak list with retention time, m/z, peak apex intensity, and per-peak S/N values
- User-defined S/N threshold parameter (numeric, unitless ratio)

## Outputs

- Filtered peak list (subset of input, containing only peaks with S/N ≥ threshold)
- S/N values for retained peaks
- Count of peaks removed and retained (quality control metrics)

## How to apply

After the IDSL.IPA peak detection algorithm identifies peaks within each EIC candidate by analyzing signal continuity and intensity transitions, compute or retrieve the S/N metric for each detected peak. IDSL.IPA supports three S/N calculation methods: (1) S/N using baseline (local noise estimation around the peak), (2) S/N using the xcms method, and (3) S/N using the RMS method. Retain only peaks whose S/N exceeds a user-defined threshold (specify in the IPA parameter spreadsheet). This filtering step is performed before peak property evaluation to reduce computational burden and improve downstream alignment and annotation specificity. Document which S/N method was used for reproducibility.

## Related tools

- **IDSL.IPA** (Implements peak detection and S/N filtering pipeline; provides three S/N calculation methods and user-configurable thresholds via parameter spreadsheet) — https://github.com/idslme/IDSL.IPA
- **R** (Runtime environment for IDSL.IPA package and S/N computation)
- **xcms** (Alternative peak picking tool; IDSL.IPA's xcms S/N method is compatible with xcms definition)
- **MZmine 2** (Comparative peak picking tool; IDSL.IPA outperforms it on S/N-based filtering)

## Examples

```
library(IDSL.IPA); IPA_workflow("Address of the IPA parameter spreadsheet")
# where the spreadsheet specifies S/N threshold (e.g., S/N > 3) and method (baseline/xcms/RMS) in PARAM rows
```

## Evaluation signals

- S/N distribution of retained vs. removed peaks: retained peaks should have median S/N well above threshold; removed peaks should cluster below it.
- Peak count before and after filtering: filtering should reduce peak count by 20–60% depending on threshold stringency and data quality; extreme reduction (>95%) suggests threshold may be too high.
- Consistency of retained peaks across technical replicates: S/N-filtered peaks should show reproducible detection at similar m/z–RT coordinates in replicate samples.
- Downstream alignment rate: peak alignment (cross-sample feature matching) should improve after S/N filtering due to removal of spurious candidates.
- Manual spot-check: sample output *.csv peaklist and verify that removed peaks have visibly low signal or baseline contamination in raw EICs; retained peaks should show clear, well-resolved signals.

## Limitations

- S/N threshold is user-specified and not automatically optimized; suboptimal thresholds may over-filter true low-abundance metabolites or under-filter noise.
- The three S/N methods (baseline, xcms, RMS) can produce different rankings of peak quality; method choice should be documented and consistent across batches.
- Instrument-specific S/N profiles may require recalibration when switching platforms or ionization modes (ESI-POS vs. ESI-NEG); thresholds derived from one instrument may not transfer.
- Peaks at chromatographic boundaries or with overlapping isotopologues may have artificially inflated or suppressed S/N; manual review of borderline cases (S/N near threshold) is recommended for high-stakes analyses.

## Evidence

- [other] Filter detected peaks according to algorithm-defined quality criteria (signal-to-noise ratio, peak width constraints, baseline separation).: "Filter detected peaks according to algorithm-defined quality criteria (signal-to-noise ratio, peak width constraints, baseline separation)."
- [readme] S/N using baseline, S/N using the xcms method, S/N using the RMS method: "S/N using baseline, S/N using the *xcms* method, S/N using the RMS method"
- [readme] Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R13C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor, skewness using derivative method, symmetry using pseudo-moments, skewness using pseudo-moments, gaussianity, S/N using baseline, S/N using the xcms method, S/N using the RMS method, and sharpness.: "Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R13C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor, skewness"
- [readme] algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation: "algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation"
- [readme] Parameter selection through a user-friendly and well-described parameter spreadsheet: "Parameter selection through a user-friendly and well-described parameter spreadsheet"
