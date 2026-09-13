---
name: peak-filtering-and-quality-control
description: Use when after peak picking and alignment have been performed on MSImagingArrays
  data (via peakPick() and peakProcess()), apply this skill when you need to remove
  noise-driven or low-frequency peaks before summarizing reference peaks across the
  full imaging dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Cardinal
  - BiocParallel
  - R
  - matter
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btv146
  title: Cardinal
evidence_spans:
- library(Cardinal)
- '*Cardinal 3.6* is a major update with breaking changes. It bring support many of
  the new low-level signal processing functions'
- Parallel processing support via the *BiocParallel* package for all pre-processing
  methods
- Parallel processing support via the *BiocParallel* package for all pre-processing
  methods and any statistical analysis methods with a `BPPARAM` option
- 'Once installed, Cardinal can be loaded with library(): library(Cardinal)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cardinal_cq
    doi: 10.1093/bioinformatics/btv146
    title: Cardinal
  dedup_kept_from: coll_cardinal_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btv146
  all_source_dois:
  - 10.1093/bioinformatics/btv146
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-filtering-and-quality-control

## Summary

Filter and validate detected peaks in mass spectrometry imaging data by applying signal-to-noise ratio (SNR), frequency thresholds, and quality criteria to remove spurious peaks and retain only high-confidence reference peaks. This skill ensures the final MSImagingExperiment contains only peaks meeting specified quality standards.

## When to use

After peak picking and alignment have been performed on MSImagingArrays data (via peakPick() and peakProcess()), apply this skill when you need to remove noise-driven or low-frequency peaks before summarizing reference peaks across the full imaging dataset. Use when you have preset quality thresholds (SNR, frequency cutoff) that distinguish signal from noise in your specific experiment.

## When NOT to use

- Input is already a feature table or reference peak set that has been validated in a prior run — re-filtering may discard validated peaks.
- Experiment design requires detection of all peaks, including rare or singleton peaks — frequency filtering would eliminate biologically relevant rare features.
- SNR and filterFreq thresholds are not justified by your instrument calibration or biological prior — applying arbitrary cutoffs may remove true signal.

## Inputs

- MSImagingArrays object with detected and aligned peaks
- peak picking results (m/z positions and intensities)
- noise estimation model (derivative, quantile, or SD/MAD-based)

## Outputs

- Filtered reference peak table (m/z positions meeting SNR and frequency thresholds)
- MSImagingExperiment with quality-controlled reference peaks and metadata

## How to apply

Within the peakProcess() workflow, filter detected peaks by specifying SNR and filterFreq parameters. SNR (e.g., SNR=6) removes peaks below the noise floor by comparing peak height to estimated noise level using derivative-based, quantile-based, or SD/MAD-based noise estimation. The filterFreq parameter (e.g., filterFreq=0.02) eliminates peaks that occur infrequently across the sampled spectra (sampleSize=0.3), retaining only peaks detected consistently enough to be biologically meaningful. These filtered peaks become the reference peak table summarized across every spectrum in the full MSImagingExperiment. Validate by checking that the number of reference peaks is reduced but remains sufficient for downstream statistical analysis.

## Related tools

- **Cardinal** (Implements peakProcess() and peakPick() functions with SNR and frequency-based filtering parameters; handles MSImagingArrays and MSImagingExperiment classes) — github.com/kuwisdelu/Cardinal
- **BiocParallel** (Enables parallel processing of peak filtering across all spectra via BPPARAM option in peakProcess())
- **matter** (Provides low-level signal processing functions underlying Cardinal 3.6 peak filtering methods)

## Examples

```
peakProcess(msi_array, method="diff", SNR=6, sampleSize=0.3, filterFreq=0.02, BPPARAM=BiocParallel::bpparam())
```

## Evaluation signals

- Reference peak count is substantially reduced compared to raw peak-picked output, indicating SNR and frequency filtering removed spurious peaks.
- Filtered reference peaks show consistent m/z positions and frequency of detection across sampled spectra above the filterFreq threshold.
- Signal-to-noise ratio of retained peaks exceeds the SNR parameter threshold (e.g., SNR ≥ 6) when noise is re-estimated on the full dataset.
- Downstream statistical analysis (e.g., PCA, spatialKMeans) on the filtered MSImagingExperiment shows improved class separation or reduced noise artifacts compared to unfiltered results.
- Peak intensity distributions in the final reference peak table show expected biological range with minimal tail of very-low-intensity 'noise' peaks.

## Limitations

- SNR threshold is method-dependent: derivative-based, quantile-based, and SD/MAD-based noise estimation may yield different results on the same data; choice must be justified by noise characteristics.
- Frequency filtering (filterFreq) uses only the sampleSize fraction of spectra to determine reference peaks; rare peaks in the full dataset may be underrepresented or missed if they occur primarily in non-sampled spectra.
- No changelog provided to clarify changes in peak filtering behavior between Cardinal versions; reproducibility may be affected by version differences.
- Out-of-memory MSImagingExperiment datasets may require sequential filtering on chunks; filtering parameters and thresholds may not be uniformly applied across partitions if not carefully managed.

## Evidence

- [other] SNR and frequency threshold filtering mechanism: "Filter peaks according to quality criteria (e.g., frequency threshold, signal-to-noise ratio)."
- [other] peakProcess() integrates SNR estimation and frequency filtering: "peakProcess() performs peak picking and alignment on a subset of spectra (specified by sampleSize) to create reference peaks, then summarizes these reference peaks for every spectrum in the full"
- [intro] Multiple SNR estimation methods available in Cardinal 3.6: "New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimatino, Dynamic peak filtering, Continuous wavelet transform (CWT)"
- [intro] Parallel processing support for peak filtering: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
