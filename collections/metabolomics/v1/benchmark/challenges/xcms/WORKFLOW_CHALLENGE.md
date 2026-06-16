# Workflow Challenge: `coll_xcms_workflow`


> The xcms package provides comprehensive workflows for preprocessing and analyzing LC-MS, GC-MS, and LC-MS/MS data, including chromatographic peak detection, sample alignment, feature grouping, and MS2-based compound annotation.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This benchmark demonstrates five key analytical workflows implemented in the xcms R package for mass spectrometry metabolomics. First, retention-time-based feature grouping using SimilarRtimeParam(20) on the faahKO dataset groups 159 features into a series of feature groups of varying sizes. Second, abundance-correlation refinement via AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE) sub-groups these into 94 feature groups, with within-group correlation analysis (e.g., FG.040) revealing heterogeneous correlation patterns above and below the 0.7 threshold. Third, EIC-similarity sub-grouping using EicSimilarityParam(threshold=0.7, n=2) further subdivides feature groups FG.013.001 and FG.045.001 based on peak-shape correlation, with features showing chromatographic misalignment excluded from same-compound groupings. Fourth, direct-injection FTICR-MS analysis on the HAM dataset demonstrates MSWParam peak detection followed by edgeshift calibration, producing m/z corrections that vary systematically with precursor mass via linear interpolation within the calibrant range and constant shift outside it. Fifth, DDA LC-MS/MS analysis of PestMix1 shows that the consensus MS2 spectrum derived from the m/z 304.1131 chromatographic peak exhibits high normalized dot-product similarity to Fenamiphos but not Flumazenil at 40 ppm tolerance, enabling compound identification.

## Research questions

- When groupFeatures is applied to the faahKO xcms result object with SimilarRtimeParam using a 20-second retention time window, how many distinct feature groups are produced and what is the distribution of features across group sizes?
- When applying AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE) to retention-time-based feature groups, how many feature sub-groups result, and what is the pairwise correlation pattern within the FG.040 feature group?
- What is the final count of feature groups after applying EIC similarity-based refinement with a correlation threshold of 0.7 on the top 2 samples, and how do the extracted ion chromatograms visually differ between sub-groups within feature groups FG.013.001 and FG.045.001?
- Does the 'edgeshift' calibration method successfully correct m/z values of identified peaks in direct injection MS data, and can the magnitude of these corrections be quantified across the m/z range?
- Can an experimental MS2 spectrum derived from a chromatographic peak at m/z 304.1131 in DDA data be matched against reference MS2 spectra from Flumazenil and Fenamiphos to identify the compound?

## Methods overview

Load preprocessed xcms result object containing detected chromatographic peaks from faahKO samples Apply groupFeatures() with SimilarRtimeParam(window=20) to group features within a 20-second retention time window Extract feature group assignments and compute group-wise statistics (count, size distribution) Validate: verify that the total feature group count and group size table match published reference results Load retention-time-based feature groups and abundance matrix Apply AbundanceSimilarityParam with threshold=0.7, log2 transformation, and gap-filling enabled to refine groups via Pearson correlation Extract and count resulting sub-group assignments Calculate pairwise Pearson correlations for all features in FG.040 Generate and validate correlation plot showing feature clustering under abundance similarity criterion Load pre-processed LC-MS data and abundance-correlation-refined feature groups from upstream xcms workflow. Apply groupFeatures() with EicSimilarityParam (threshold=0.7, n=2) to perform feature grouping based on EIC correlation. Compute and report final feature group count after EIC similarity refinement. Extract and visualize overlay EIC plots for specified feature groups (FG.013.001 and FG.045.001) to show peak shape alignment. Validation: confirm that final feature group count matches expected output and that overlay EIC plots display correlated peak shapes with similarity ≥0.7 for grouped features. Load FTICR HAM mzML files from Zenodo into xcms XCMSnExp container. Apply MSWParam chromatographic peak detection to all files in the experiment. Extract the first mzML file and retrieve its chromatographic peaks. Apply mass calibration using CalibrantMassParam with edgeshift method to correct m/z values. Extract m/z residuals (observed − expected) before and after calibration. Validation: Calibration difference plot shows reduced m/z error variance post-edgeshift; residuals cluster near zero across the m/z range with no systematic drift. Load mzML raw data and apply centWave chromatographic peak detection with specified signal-to-noise and mass accuracy thresholds. Extract all MS2 spectra associated with the target m/z 304.1131 chromatographic peak. Merge multiple MS2 spectra into a single consensus spectrum to improve signal and representation. Compare consensus spectrum against Flumazenil and Fenamiphos reference spectra using spectral similarity scoring. Validation: Mirror-plot successfully aligns experimental consensus peaks with reference spectra; spectral similarity scores (cosine or dot-product) ≥ 0.7 indicate high-confidence match to reference standards.

**Domain:** metabolomics

**Techniques:** lc-ms, feature-detection, chromatogram-alignment, clustering

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The xcms R package provides functionality to efficiently preprocess LC-MS, GC-MS, and LC-MS/MS data. _[grounded: xcms_package]_
- **(finding)** In LC-MS metabolomics experiments, different multiple ions can be generated from the same compound during ionization.
- **(finding)** Features of the same compound should have similar retention time.
- **(finding)** The abundance of features of the same compound should have a similar pattern across samples.
- **(finding)** The peak shape of extracted ion chromatograms of features of the same compound should be similar.
- **(finding)** xcms provides AbundanceSimilarityParam for feature grouping based on correlation of feature abundances across samples. _[grounded: xcms_package]_
- **(finding)** xcms provides EicSimilarityParam for feature grouping based on correlation of EICs. _[grounded: xcms_package]_
- **(finding)** The faahKO dataset consists of samples from 4 mice with knock-out of the fatty acid amide hydrolase and 4 wild type mice. _[grounded: faahko_dataset]_
- **(hypothesis)** Features grouped by retention time with a 20-second window were further subdivided into multiple feature groups.
- **(finding)** Abundance correlation analysis can split retention time-based feature groups further.
- **(finding)** EIC correlation analysis can provide additional sub-grouping of retention time and abundance-based feature groups.
- **(finding)** In direct injection mass spectrometry experiments, only a single spectrum with an artificial retention time is available for each sample.
- **(finding)** xcms uses functionality from the MassSpecWavelet package to identify peaks in the m/z dimension for direct injection MS data. _[grounded: xcms_package]_
- **(finding)** In peak detection with MSWParam, scales of 1, 4, and 9 were used. _[grounded: mswparam]_
- **(finding)** The calibrate method can adjust m/z values of identified peaks based on differences between calibrants' m/z values and closest peaks' m/z values.
- **(finding)** The edgeshift calibration method adjusts peaks within the range of calibrant m/z values using linear interpolation. _[grounded: edgeshift_calibration]_
- **(finding)** For LC-MS/MS data, data dependent acquisition (DDA) is the most used approach for generating fragmentation spectra. _[grounded: spectra_package]_
- **(finding)** In DDA, the top N most intense ions are selected for fragmentation before the cycle starts again.
- **(finding)** SWATH acquisition uses defined windows of m/z values to reduce overlap of fragment spectra while keeping high coverage. _[grounded: spectra_package]_
- **(finding)** The example DDA and SWATH data files are from reversed-phase LC-MS/MS runs of the Agilent Pesticide mix. _[grounded: swath_acquisition_mode]_
- **(finding)** Most signal in the DDA dataset was measured between approximately 200 and 600 seconds.
- **(hypothesis)** In the DDA dataset, chromatographic peak detection identified peaks at specific m/z values.
- **(finding)** Some MS manufacturers like Sciex do not export precursor intensity values for MS2 spectra. _[grounded: spectra_package]_
- **(finding)** The estimatePrecursorIntensity function can determine precursor intensity based on the intensity of the ion in the previous MS1 scan.
- **(finding)** CentWaveParam was used for chromatographic peak detection with snthresh of 5, noise of 100, ppm of 10, and peakwidth of 3 to 30. _[grounded: centwave_param]_
- **(finding)** The chromPeakSpectra method extracts MS2 spectra with precursor m/z and retention time within the range of chromatographic peaks. _[grounded: spectra_package]_
- **(finding)** The returned Spectra from chromPeakSpectra contains a chrom_peak_id spectra variable that identifies the associated chromatographic peak. _[grounded: spectra_package]_
- **(finding)** An example chromatographic peak of an ion with m/z 304.1131 was identified in the DDA dataset.
- **(finding)** Flumazenil (Metlin ID 2724) has experimental MS2 spectra available in reference databases. _[grounded: spectra_package]_
- **(finding)** Fenamiphos (Metlin ID 72445) has experimental MS2 spectra available in reference databases. _[grounded: spectra_package]_
- **(finding)** In the example, 5 MS2 spectra were associated with the candidate chromatographic peak. _[grounded: spectra_package]_
- **(finding)** The combineSpectra method can reduce multiple fragment spectra into a single consensus spectrum. _[grounded: spectra_package]_
- **(finding)** combinePeaks combines mass peaks from input spectra with m/z differences smaller than 20 ppm into one peak. _[grounded: spectra_package]_
- **(finding)** With minProp parameter set to 0.8, the resulting spectrum contains only peaks present in 80% of input spectra. _[grounded: spectra_package]_
- **(finding)** The example experimental spectrum matches Fenamiphos better than Flumanezil in similarity comparisons. _[grounded: fenamiphos_compound]_
- **(finding)** In SWATH mode, all ions within pre-defined isolation windows are fragmented and MS2 spectra are measured. _[grounded: spectra_package]_
- **(finding)** SWATH isolation window information is available as spectra variables isolationWindowLowerMz and isolationWindowUpperMz. _[grounded: spectra_package]_
- **(finding)** Between 422 and 423 MS2 spectra are measured in each isolation window of the SWATH dataset. _[grounded: spectra_package]_
- **(finding)** An isolation window target m/z of 270.85 was used as an example for extracting chromatograms from SWATH data. _[grounded: swath_acquisition_mode]_
- **(finding)** findChromPeaksIsolationWindow performs chromatographic peak detection in MS level 2 data separately for each isolation window.
- **(finding)** CentWaveParam with snthresh of 3, noise of 10, ppm of 10, and peakwidth of 3 to 30 was used for MS2 peak detection. _[grounded: centwave_param]_
- **(finding)** findChromPeaksIsolationWindow adds peaks to the chromPeaks matrix that can be identified through the isolationWindow column.
- **(finding)** The EicSimilarityParam is advisable to use as the last refinement step in feature grouping because it is computationally very expensive. _[grounded: eic_similarity_param]_
- **(finding)** AbundanceSimilarityParam uses a correlation coefficient threshold to group features together. _[grounded: abundance_similarity_param]_
- **(finding)** The featureDefinitions function extracts results from correspondence analysis.
- **(finding)** The peakidx column in featureDefinitions provides the index of each chromatographic peak assigned to a feature.
- **(finding)** featureValues function allows extracting feature abundances in a matrix format with one row per feature.
- **(finding)** Gap-filled data in featureValues integrates all signal from the m/z-retention time range defined by detected peaks.
- **(finding)** Any subsequent groupFeature call will sub-group and refine the previously identified feature groups.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Normalized dot-product similarity metric can be substituted with alternative similarity/distance metrics via FUN parameter in EicSimilarityParam
- Interpolation method can be used for estimating precursor intensity instead of previous scan method
- return.type = "List" can be used instead of default return type in chromPeakSpectra()

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Feature grouping based on EIC similarity is computationally expensive and should be applied last; works best when applied to pre-defined feature groups
- Abundance correlation-based grouping works best for features with higher variability in concentration across samples
- Peak shape correlation should be performed only on subset of samples due to computational intensity and noisy low-intensity peaks

## Steps

### Step `task_001`
- Title: Reproduce retention-time-based feature grouping using SimilarRtimeParam(20) on the faahKO dataset
- Task kind: `reproduction`
- Task: Apply SimilarRtimeParam with a 20-second retention time window to group features in a preprocessed faahKO xcms result object, and reproduce the reported feature group count and distribution of group sizes.
- Inputs:
  - Preprocessed faahKO xcms result object (XcmsExperiment or xcmsSet with detected chromatographic peaks)
- Expected outputs:
  - Feature group count and table of group sizes showing distribution of features across groups
- Tools: xcms, MsFeatures
- Landmark output files: feature_groups_raw.txt, group_size_distribution.txt
- Primary expected artifact: `feature_groups_summary.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce abundance-correlation sub-grouping using AbundanceSimilarityParam(threshold=0.7, log2) on faahKO feature groups
- Task kind: `reproduction`
- Task: Starting from retention-time-based feature groups, apply groupFeatures with AbundanceSimilarityParam (threshold=0.7, transform=log2, filled=TRUE) to refine groups based on abundance correlation, then reproduce the reported sub-group count and generate the pairwise correlation plot for feature group FG.040.
- Inputs:
  - Retention-time-based feature groups from SimilarRtimeParam grouping
  - Preprocessed LC-MS feature table with abundances across samples
- Expected outputs:
  - Count of sub-groups generated by AbundanceSimilarityParam refinement
  - Pairwise correlation plot for FG.040 showing abundance similarities between features
- Tools: xcms, MsFeatures, pheatmap
- Landmark output files: refined_feature_groups.csv, subgroup_assignments.csv, fg040_correlation_matrix.csv
- Primary expected artifact: `fg040_correlation_plot.png`

### Step `task_003`
- Depends on: `task_002`
- Title: Reproduce EIC-similarity sub-grouping using EicSimilarityParam(threshold=0.7, n=2) on faahKO feature groups
- Task kind: `reproduction`
- Task: Apply groupFeatures with EicSimilarityParam (threshold=0.7, n=2) to abundance-correlation-refined feature groups and reproduce the final feature group count and overlay EIC plots for groups FG.013.001 and FG.045.001.
- Inputs:
  - Abundance-correlation-refined feature groups (output from AbundanceSimilarityParam refinement)
- Expected outputs:
  - Final count of feature groups after EIC similarity refinement
  - Overlay EIC plot for feature group FG.013.001
  - Overlay EIC plot for feature group FG.045.001
- Tools: xcms, MsFeatures
- Landmark output files: refined_feature_groups.csv, eic_similarity_grouping_stats.txt, eic_plot_fg013001.png, eic_plot_fg045001.png
- Primary expected artifact: `eic_similarity_feature_groups.rda`

### Step `task_004`
- Depends on: `task_002`
- Title: Reproduce MSWParam peak detection and edgeshift calibration on the FTICR-MS HAM dataset
- Task kind: `reproduction`
- Task: Load FTICR HAM mzML files from Zenodo (doi:10.5281/zenodo.18494293), detect chromatographic peaks using findChromPeaks with MSWParam, calibrate the first file using CalibrantMassParam with method='edgeshift', and reproduce the calibration difference plot.
- Inputs:
  - FTICR HAM mzML files from Zenodo deposit doi:10.5281/zenodo.18494293
- Expected outputs:
  - Calibration difference plot (m/z error before and after edgeshift calibration) for the first FTICR file
  - XCMSnExp object with detected chromatographic peaks and calibrated m/z values
- Tools: xcms
- Landmark output files: ham_peaks_detected.rds, ham_first_file_precalibration.rds, ham_first_file_postcalibration.rds
- Primary expected artifact: `calibration_difference_plot.png`

### Step `task_005`
- Depends on: `task_002`
- Title: Reproduce DDA chromatographic peak detection and MS2 spectrum annotation for m/z 304.1131 in PestMix1_DDA
- Task kind: `reproduction`
- Task: Load the PestMix1_DDA.mzML file, detect chromatographic peaks using centWave (snthresh=5, noise=100, ppm=10), extract MS2 spectra for the peak at m/z 304.1131, build a consensus spectrum, and generate a mirror-plot comparison against Flumazenil and Fenamiphos reference spectra.
- Inputs:
  - PestMix1_DDA.mzML file from Agilent Pesticide mix LC-MS/MS runs
  - Flumazenil (Metlin ID 2724) reference spectrum in MGF format
  - Fenamiphos (Metlin ID 72445) reference spectrum in MGF format
- Expected outputs:
  - Mirror-plot comparison figure showing consensus MS2 spectrum for m/z 304.1131 aligned with Flumazenil and Fenamiphos reference spectra
  - Consensus MS2 spectrum for the chromatographic peak at m/z 304.1131
  - Peak detection table listing detected chromatographic peaks with retention time, m/z, and intensity
- Tools: xcms, MsFeatures, Spectra, MsBackendMgf, MetaboCoreUtils
- Landmark output files: peak_detection_results.csv, ms2_spectra_for_mz_304.1131.msp, consensus_spectrum_mz_304.1131.msp, spectral_similarity_scores.csv
- Primary expected artifact: `mirror_plot_consensus_vs_standards.png`

## Final expected outputs

- `Final count of feature groups after EIC similarity refinement` (type: file, tolerance: hash)
- `Overlay EIC plot for feature group FG.013.001` (type: file, tolerance: hash)
- `Overlay EIC plot for feature group FG.045.001` (type: file, tolerance: hash)
- `Calibration difference plot (m/z error before and after edgeshift calibration) for the first FTICR file` (type: file, tolerance: hash)
- `XCMSnExp object with detected chromatographic peaks and calibrated m/z values` (type: file, tolerance: hash)
- `Mirror-plot comparison figure showing consensus MS2 spectrum for m/z 304.1131 aligned with Flumazenil and Fenamiphos reference spectra` (type: file, tolerance: hash)
- `Consensus MS2 spectrum for the chromatographic peak at m/z 304.1131` (type: file, tolerance: hash)
- `Peak detection table listing detected chromatographic peaks with retention time, m/z, and intensity` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** concrete

- **Orchestration planning:** static

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_xcms_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Final count of feature groups after EIC similarity refinement": "<locator>",
    "Overlay EIC plot for feature group FG.013.001": "<locator>",
    "Overlay EIC plot for feature group FG.045.001": "<locator>",
    "Calibration difference plot (m/z error before and after edgeshift calibration) for the first FTICR file": "<locator>",
    "XCMSnExp object with detected chromatographic peaks and calibrated m/z values": "<locator>",
    "Mirror-plot comparison figure showing consensus MS2 spectrum for m/z 304.1131 aligned with Flumazenil and Fenamiphos reference spectra": "<locator>",
    "Consensus MS2 spectrum for the chromatographic peak at m/z 304.1131": "<locator>",
    "Peak detection table listing detected chromatographic peaks with retention time, m/z, and intensity": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
