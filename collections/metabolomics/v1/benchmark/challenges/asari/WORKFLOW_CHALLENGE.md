# Workflow Challenge: `coll_asari_workflow`


> Asari is a transparent, scalable Python program for high-resolution LC-MS metabolomics data processing that prioritizes mass separation and alignment, performs peak detection on composite maps rather than individual samples, and enables reproducible tracking between features and mass tracks.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Asari implements a complete LC-MS metabolomics preprocessing workflow centered on high mass resolution and composite mass track construction. The pipeline extracts mass tracks from centroided mzML files, aligns them across samples into a MassGrid using either pairwise landmark-based or clustering-based approaches depending on study size, calibrates retention time via LOWESS regression on high-confidence anchor peaks, and constructs composite mass tracks by summing aligned signals across samples. Peak detection is performed once on composite tracks using scipy.signal.find_peaks with dynamically determined prominence thresholds, rather than repeatedly on individual samples, and detected peaks are mapped back to individual samples for quantification. The resulting features are annotated through isotope and adduct grouping and database matching. Asari is designed for reproducibility through JSON-centric data structures that enable tracking between features and extracted ion chromatograms, and for scalability through performance-conscious memory and CPU management suitable for processing >1000 samples on standard hardware.

## Research questions

- Does the asari pipeline successfully produce all five canonical output artifacts (preferred_Feature_table.tsv, full_Feature_table.tsv, _mass_grid_mapping.csv, cmap.pickle, and Annotated_empiricalCompounds.json) when executed on a publicly deposited centroided mzML dataset?
- How does performing peak detection on a single composite map rather than on individual samples improve computational efficiency in metabolomics data processing?
- How does asari determine which mass alignment algorithm to apply based on study size?
- How does the peak quality filtering mechanism using SNR (>2), peak shape goodness-of-fit, and minimum peak height (default 1e5 with >20% prominence) thresholds reduce the number of detected features in the feature table?
- How does asari's computational performance (wall-clock time and peak memory usage) scale with increasing numbers of LC-MS samples?

## Methods overview

Parse mzML files and extract MS1 spectra indexed by binned m/z (0.001 amu) to form mzTree. Construct mass tracks per sample by grouping m/z values within 2× ppm tolerance (5 ppm default) and applying nearest-neighbor clustering where needed; establish anchor tracks via isotope/adduct patterns. Align mass tracks across samples via pairwise anchor-first matching (≤10 samples) or centroid-based clustering (>10 samples) to form a MassGrid; recalibrate m/z if systematic offset exceeds 1 ppm. Calibrate retention time per sample by identifying landmark peaks (mSelectivity >0.99, prominence >20% height) and fitting LOWESS regression to reference sample, storing scan-number mappings in rt_cal_dict. Assemble composite mass tracks by summing RT-aligned intensities across samples; detect elution peaks using local maxima with adaptive prominence and noise-based filtering; evaluate peaks for peakshape and SNR. Map detected features back to individual samples using RT calibration dictionaries; extract and report peak areas and intensities. Perform pre-annotation via khipu to group features into empirical compounds by isotope/adduct relationships; search against HMDB 4 via JMS to obtain formula and isomer matches. Validation: verify existence and format of canonical outputs (preferred_Feature_table.tsv, full_Feature_table.tsv, _mass_grid_mapping.csv, cmap.pickle, epd.pickle, Annotated_empiricalCompounds.json) and confirm row/record counts are non-empty and consistent across tables. References: source article (DOI: 10.1038/s41467-023-39889-1) Synchronize all sample mass tracks to reference retention-time coordinates using pre-computed rt_cal_dict mappings. Sum aligned intensity arrays element-wise across samples for each m/z, creating composite mass tracks of consistent length. Audit each composite track: rescale if ceiling exceeded, detect low-intensity baseline/noise, detrend if high-signal-high-noise, apply adaptive smoothing. Subtract baseline+noise filter to isolate positive-intensity regions and segment the track. Apply scipy.signal.find_peaks with dynamic prominence control (max of three criteria) on each segment to detect local maxima. Evaluate peaks for gaussian fit quality (goodness_fitting), chromatographic selectivity (cSelectivity), and SNR, filtering by SNR > 2 threshold. Validation: verify peak detection is called exactly once per composite track (not per sample) and all reported peaks contain cSelectivity, SNR, and goodness_fitting metrics. References: source article (DOI: 10.1038/s41467-023-39889-1) Determine alignment strategy by evaluating sample count: if ≤10, use pairwise anchor-prioritized alignment; else use nearest-neighbor clustering. Identify reference sample as the sample with the highest count of anchor mass tracks (isotopic/adduct pairs). For small studies, align anchor mass tracks first between each sample and the reference, then recalibrate all m/z values if systematic shift exceeds 1 ppm, then align remaining tracks. For large studies, apply nearest-neighbor clustering to bin mass tracks by m/z difference, using histogram-based m/z seed detection with peaks separated by at least mz_tolerance. Compute consensus m/z for each aligned bin as the mean of median m/z and m/z at highest intensity. Validation: _mass_grid_mapping.csv is produced with all samples represented, consensus m/z values are numeric and within instrument ppm tolerance, and pairwise/clustering dispatching is correctly applied based on sample count threshold (≤10 vs >10). References: source article (DOI: 10.1038/s41467-023-39889-1) Load full peak list from composite track detection with SNR, peakshape, peak height, and prominence annotations. Filter peaks by SNR > 2 to retain sufficient signal-to-noise measurements. Filter peaks by goodness_fitting > 0.5 using gaussian peak evaluation to select well-shaped peaks. Filter peaks by minimum peak height (1e5) AND prominence ≥20% of peak height to eliminate low-signal and poorly prominent peaks. Map retained peaks back to individual samples via RT alignment dictionaries and extract sample-specific peak areas. Compile filtered feature table with quantitative intensity values per sample. Validation: verify that row count in preferred_Feature_table.tsv is less than full_Feature_table.tsv and that all retained peaks meet the four thresholds (SNR > 2, peakshape > 0.5, height ≥ 1e5, prominence ≥ 20% height). References: source article (DOI: 10.1038/s41467-023-39889-1) Retrieve or construct public mzML test datasets at three scale points: 10, 50, and 100+ samples. Install asari from PyPI (pip install asari-metabolomics) using default configuration (5 ppm tolerance, positive mode). Execute asari process on each cohort using a system profiler (time, psutil, or Linux /usr/bin/time -v) to capture wall-clock duration and peak memory. Repeat each run 2–3 times and calculate mean, standard deviation, and throughput (samples/hour) per cohort. Plot wall-clock time and peak memory as functions of sample count; visually assess linearity and extrapolate to 1000-sample scenario. Validation: confirm that observed scaling behaviour supports or refutes the >1000-samples-on-laptop claim by verifying that extrapolated runtime for 1000 samples remains <24 hours on a single CPU core with ≤16 GB peak memory. References: source article (DOI: 10.1038/s41467-023-39889-1)

**Domain:** metabolomics

**Techniques:** lc-ms, feature-detection, chromatogram-alignment, quality-control, database-annotation

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Asari is a trackable and scalable Python program for high-resolution metabolomics data processing. _[grounded: SYS_ASARI]_
- **(finding)** Asari performs peak detection on a composite map instead of repeated on individual samples. _[grounded: SYS_ASARI]_
- **(finding)** Asari uses statistics guided peak detection based on local maxima and prominence with selective use of smoothing. _[grounded: SYS_ASARI]_
- **(finding)** LC-MS application of Asari was described in Li et al. Nature Communications 14.1 (2023): 4113. _[grounded: SYS_ASARI]_
- **(finding)** GC-MS workflow was added to Asari in version 1.16.6. _[grounded: SYS_ASARI]_
- **(finding)** A web server for Asari is available at https://asari.app. _[grounded: SYS_ASARI]_
- **(finding)** Mass tracks of unique m/z values are extracted from each mzML data file, then aligned into a MassGrid. _[grounded: COMP_MASSGRID]_
- **(finding)** Retention time is calibrated for each sample to a common reference sample.
- **(finding)** For each m/z value, corresponding mass tracks from all sample files are summarized into one composite mass track.
- **(finding)** Peak detection is performed on the composite mass tracks to generate a feature list for the experiment.
- **(finding)** The features are mapped back to each sample to extract peak area as intensity values.
- **(finding)** Asari's approach of MassGrid and composite mass tracks is highly scalable. _[grounded: SYS_ASARI]_
- **(finding)** In LC-MS metabolomics, a feature is defined by m/z and retention time across one experiment.
- **(finding)** Asari uses 'empirical compound' to group degenerate features into a tentative compound/metabolite. _[grounded: SYS_ASARI]_
- **(finding)** M/z values in data are indexed to a dictionary by int(mz * 1000) for efficiency retrieval.
- **(finding)** Each data bin has a m/z range around 0.001. _[grounded: COMP_MZTREE]_
- **(finding)** If the m/z range in a data bin is within 2 x tolerance ppm, the bin leads to a single mass track.
- **(finding)** A consensus m/z value is taken as the mean of median m/z and the m/z at highest intensity.
- **(finding)** When multiple data points exist in the same scan on the same mass track, max intensity is used.
- **(finding)** The sample with the highest number of anchor mass tracks is designated as the reference sample. _[grounded: ALG_ANCHOR_TRACKS]_
- **(finding)** If the sample number is no more than 10, this is considered a small study and pairwise alignment is performed. _[grounded: COND_SMALL_STUDY]_
- **(finding)** The default systematic m/z difference threshold for recalibration is 1 ppm.
- **(finding)** A set of landmark elution peaks are determined in the reference sample by the criterion: mSelectivity > 0.99. _[grounded: ALG_LANDMARK_PEAKS]_
- **(finding)** The default min_peak_height for landmark peaks is 1e5. _[grounded: METRIC_MSELECTIVITY]_
- **(finding)** Landmark peak prominence must be greater than 20% of peak height.
- **(finding)** LOWESS regression is used to obtain a function describing the relationship of RT values between good_landmark_peaks and selected_reference_landmark_peaks. _[grounded: TOOL_LOWESS]_
- **(finding)** A 10% extension out of both ends is added as boundaries for LOWESS regression convergence. _[grounded: TOOL_LOWESS]_
- **(finding)** Composite mass tracks sum intensity values on corresponding mass tracks across all samples after RT calibration.
- **(finding)** Asari detects an elution peak only once on the composite mass tracks instead of in every sample. _[grounded: SYS_ASARI]_
- **(finding)** If the max intensity of a mass track is higher than 1E8, the mass track is rescaled under 1E8 for peak detection.
- **(finding)** The default min_intensity_threshold for low-intensity tracks is 1e3 for Orbitrap data. _[grounded: PARAM_MIN_INTENSITY_THRESHOLD]_
- **(finding)** The default min_peak_height for Orbitrap data is 1e5. _[grounded: PARAM_MIN_PEAK_HEIGHT]_
- **(finding)** Smoothing is applied when the noise level is higher than 1% of max intensity and max intensity is lower than 10 times of the preset min_peak_height. _[grounded: PARAM_MIN_PEAK_HEIGHT]_
- **(finding)** The initial prominence value for peak detection is 1/3 of min_peak_height. _[grounded: PARAM_MIN_PEAK_HEIGHT]_
- **(finding)** For high-intensity and high-noise segments, prominence is set as the greater of prominence and 5% of max intensity.
- **(finding)** The default sliding window size for prominence computation is 25 scans.
- **(finding)** The default SNR threshold for peaks is greater than 2.
- **(finding)** The default peakshape threshold for peaks is greater than 0.5.
- **(finding)** The recommended feature table output by Asari is 'preferred_Feature_table.tsv'. _[grounded: SYS_ASARI]_
- **(finding)** All peaks are kept in 'export/full_Feature_table.tsv'. _[grounded: ARTIFACT_FULL_FEATURE_TABLE]_
- **(finding)** Asari uses the khipu package for pre-annotation where isotopes and adducts are grouped into empirical compounds. _[grounded: SYS_ASARI]_
- **(finding)** Empirical compounds are searched against HMDB 4 database via the JMS package. _[grounded: DS_HMDB4]_
- **(finding)** The dashboard is built using the panel library. _[grounded: TOOL_PANEL]_
- **(finding)** The dashboard uses the files: 'project.json', 'export/cmap.pickle', 'export/epd.pickle' and 'export/full_Feature_table.tsv'. _[grounded: ARTIFACT_FULL_FEATURE_TABLE]_
- **(finding)** Asari does not use smoothed data for visual inspection in the dashboard to avoid being misleading. _[grounded: SYS_ASARI]_
- **(finding)** The default m/z precision in Asari is set at 5 ppm. _[grounded: SYS_ASARI]_
- **(finding)** The default ionization mode in Asari is positive. _[grounded: SYS_ASARI]_
- **(finding)** Asari uses pymzml to parse mzML files by default. _[grounded: SYS_ASARI]_
- **(finding)** M/z values in Asari chromatogram building are binned to 0.001 amu. _[grounded: SYS_ASARI]_
- **(finding)** Asari is designed to run more than 1000 samples on a laptop computer. _[grounded: SYS_ASARI]_
- **(finding)** Asari requires Python 3.8 or higher. _[grounded: SYS_ASARI]_
- **(finding)** Asari installation time is approximately 5 seconds if common libraries already exist. _[grounded: SYS_ASARI]_
- **(finding)** Input data to Asari are centroided mzML files from LC-MS metabolomics. _[grounded: SYS_ASARI]_
- **(finding)** Asari ignores MS/MS spectra. _[grounded: SYS_ASARI]_
- **(finding)** Asari has a Docker image available at https://hub.docker.com/r/shuzhao/asari. _[grounded: SYS_ASARI]_
- **(finding)** The Asari Docker image includes ThermoRawFileParser for converting Thermo .raw files to .mzML files. _[grounded: SYS_ASARI]_
- **(finding)** The source code for Asari is hosted at https://github.com/shuzhao-li/asari. _[grounded: SYS_ASARI]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- dynamic time warp (DTW)
- univariate spline
- pairwise alignment
- nearest neighbor clustering by centroiding

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- mzML format required for input data
- MS/MS spectra are not processed by asari
- Pickle files should not be trusted from other people

## Steps

### Step `task_001`
- Title: Reproduce the asari end-to-end LC-MS processing pipeline on a public metabolomics dataset
- Task kind: `reproduction`
- Task: Execute the complete asari pipeline on a publicly deposited centroided mzML metabolomics dataset and verify production of all canonical output artifacts: preferred_Feature_table.tsv, full_Feature_table.tsv, _mass_grid_mapping.csv, cmap.pickle, epd.pickle, and Annotated_empiricalCompounds.json.
- Inputs:
  - Centroided mzML files from LC-MS metabolomics experiment in publicly accessible repository (e.g., GitHub, Zenodo, MassIVE, MetaboLights, or local directory)
  - Optional: custom parameters YAML file specifying ppm tolerance, min_peak_height, and other processing thresholds
- Expected outputs:
  - preferred_Feature_table.tsv: recommended feature intensity table with sample columns and feature rows
  - full_Feature_table.tsv: complete peak table including all features meeting SNR and peakshape thresholds
  - _mass_grid_mapping.csv: m/z alignment results mapping mass tracks across samples
  - cmap.pickle: serialized composite map object for dashboard inspection
  - epd.pickle: serialized empirical compound dictionary for dashboard and downstream analysis
  - Annotated_empiricalCompounds.json: pre-annotated empirical compounds with isotope/adduct grouping and database matches
- Tools: Python, pymzml, scipy.signal.find_peaks, scipy.signal.detrend, khipu, JMS, HMDB 4
- Landmark output files: mass_tracks_per_sample.json, _mass_grid_mapping.csv, composite_mass_tracks_detected_peaks.json, full_Feature_table.tsv, Annotated_empiricalCompounds.json
- Primary expected artifact: `preferred_Feature_table.tsv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the composite-map peak detection step and verify computational efficiency over per-sample detection
- Task kind: `component_reconstruction`
- Task: Construct composite mass tracks by summing intensity values across retention-time-aligned samples on the same m/z coordinate, then perform peak detection once on each composite track using scipy.signal.find_peaks with prominence control, confirming single-pass detection rather than per-sample repeated calls.
- Inputs:
  - Aligned mass tracks per sample with m/z and full-length intensity arrays
  - Retention time calibration dictionaries (rt_cal_dict) mapping sample scan numbers to reference coordinates
  - Mass grid structure with aligned m/z values across all samples
- Expected outputs:
  - Composite mass tracks (summed intensity arrays) indexed by consensus m/z and full RT scan length
  - Feature list with detected elution peaks on composite tracks: peak apex (scan), peak area, height, baseline boundaries, cSelectivity, SNR, goodness_fitting, and parent_masstrack_id
  - Execution log confirming single peak-detection pass on composite map vs. N per-sample passes
- Tools: Python, scipy.signal.find_peaks, scipy.signal.detrend
- Landmark output files: composite_mass_tracks.pickle, rt_aligned_indices.csv, track_audit_log.txt, peak_candidate_table.tsv
- Primary expected artifact: `composite_peaks.json`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct the MassGrid alignment step and verify its conditional pairwise vs. landmark-based routing
- Task kind: `component_reconstruction`
- Task: Implement the m/z alignment module that constructs a MassGrid by dispatching between pairwise alignment (≤10 samples) and nearest-neighbor clustering (>10 samples), producing a _mass_grid_mapping.csv file from aligned mass tracks across all samples.
- Inputs:
  - Mass track data from all samples, each containing m/z and full-RT-range intensity arrays
  - Anchor mass track pairs (isotopic or adduct differences) per sample for confidence-based alignment
  - Sample count and user-specified reference sample identifier (if provided)
- Expected outputs:
  - _mass_grid_mapping.csv file documenting aligned m/z values, sample-track associations, and consensus m/z per grid position
  - MassGrid object linking aligned mass tracks across all samples with consensus m/z identifiers
- Tools: Python, asari mass_functions module (nn_cluster_by_mz_seeds), asari MassGrid class (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs)
- Landmark output files: anchor_mass_track_registry.json, reference_sample_designation.txt, aligned_pairwise_sample_tracks.json, _mass_grid_mapping.csv
- Primary expected artifact: `_mass_grid_mapping.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct the peak quality filtering step and verify SNR, peak-shape, and prominence threshold application
- Task kind: `component_reconstruction`
- Task: Implement quality-based filtering on detected peaks using signal-to-noise ratio (SNR > 2), peak shape (goodness_fitting > 0.5), and minimum peak height (1e5 with ≥20% prominence) thresholds, then generate a filtered feature table and verify row count reduction relative to the unfiltered full_Feature_table.tsv.
- Inputs:
  - Full unfiltered peak list from composite track peak detection (JSON format with SNR, goodness_fitting, peak_height, prominence, apex, left_base, right_base, parent_masstrack_id, mz, rtime fields)
  - Composite mass tracks with aligned intensity vectors across all samples after RT calibration
  - RT alignment dictionaries (rt_cal_dict) mapping sample scan numbers to reference sample scan numbers
- Expected outputs:
  - Filtered feature table (preferred_Feature_table.tsv) containing only peaks meeting SNR > 2, peakshape > 0.5, and minimum peak height criteria with sample-specific peak areas
  - Row count comparison report showing number of peaks in full_Feature_table.tsv vs. preferred_Feature_table.tsv
  - QC summary metrics including SNR distribution, peakshape distribution, and peak height distribution of retained peaks
- Tools: Python, scipy.signal.find_peaks, asari peaks module
- Landmark output files: full_Feature_table.tsv, peak_filter_criteria_applied.json, row_count_comparison.txt, snr_distribution_histogram.png, peakshape_distribution_histogram.png
- Primary expected artifact: `preferred_Feature_table.tsv`

### Step `task_005`
- Title: Analyze scalability of asari by running it on increasing sample counts up to >100 mzML files and recording runtime and memory
- Task kind: `analysis`
- Task: Benchmark asari's computational performance and memory footprint on public metabolomics datasets across sample-set sizes (10, 50, 100+ samples) to validate the scalability claim of >1000 samples on a laptop computer.
- Inputs:
  - Public mzML files (minimum 100+ files) from MetaboLights or MassIVE repositories in centroided format
  - asari software installed from PyPI or cloned from source (v1.10+)
  - System profiling tools capable of capturing wall-clock runtime and peak memory usage
- Expected outputs:
  - Scalability benchmark table (CSV or TSV) with columns: sample_count, wall_clock_time_seconds, peak_memory_mb, run_number, mean_time, std_dev_time, mean_memory, std_dev_memory
  - Wall-clock time vs. sample count plot (PNG or PDF) showing linear or near-linear scaling up to 100+ samples
  - Peak memory usage vs. sample count plot (PNG or PDF) demonstrating memory efficiency across cohort sizes
  - Summary report (text or markdown) stating mean throughput (samples/hour) per cohort and extrapolated time estimate for 1000-sample project
- Tools: asari, Python, pymzml
- Landmark output files: asari_process_run_10_samples.log, asari_process_run_50_samples.log, asari_process_run_100_samples.log, benchmark_raw_metrics.csv, time_vs_sample_count.png, memory_vs_sample_count.png
- Primary expected artifact: `scalability_benchmark_results.csv`

## Final expected outputs

- `Composite mass tracks (summed intensity arrays) indexed by consensus m/z and full RT scan length` (type: file, tolerance: hash)
- `Feature list with detected elution peaks on composite tracks: peak apex (scan), peak area, height, baseline boundaries, cSelectivity, SNR, goodness_fitting, and parent_masstrack_id` (type: file, tolerance: hash)
- `Execution log confirming single peak-detection pass on composite map vs. N per-sample passes` (type: file, tolerance: hash)
- `_mass_grid_mapping.csv file documenting aligned m/z values, sample-track associations, and consensus m/z per grid position` (type: file, tolerance: hash)
- `MassGrid object linking aligned mass tracks across all samples with consensus m/z identifiers` (type: file, tolerance: hash)
- `Filtered feature table (preferred_Feature_table.tsv) containing only peaks meeting SNR > 2, peakshape > 0.5, and minimum peak height criteria with sample-specific peak areas` (type: file, tolerance: hash)
- `Row count comparison report showing number of peaks in full_Feature_table.tsv vs. preferred_Feature_table.tsv` (type: file, tolerance: hash)
- `QC summary metrics including SNR distribution, peakshape distribution, and peak height distribution of retained peaks` (type: file, tolerance: hash)
- `Scalability benchmark table (CSV or TSV) with columns: sample_count, wall_clock_time_seconds, peak_memory_mb, run_number, mean_time, std_dev_time, mean_memory, std_dev_memory` (type: file, tolerance: hash)
- `Wall-clock time vs. sample count plot (PNG or PDF) showing linear or near-linear scaling up to 100+ samples` (type: file, tolerance: hash)
- `Peak memory usage vs. sample count plot (PNG or PDF) demonstrating memory efficiency across cohort sizes` (type: file, tolerance: hash)
- `Summary report (text or markdown) stating mean throughput (samples/hour) per cohort and extrapolated time estimate for 1000-sample project` (type: file, tolerance: hash)

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

- **Orchestration planning:** dynamic

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_asari_workflow",
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
    "Composite mass tracks (summed intensity arrays) indexed by consensus m/z and full RT scan length": "<locator>",
    "Feature list with detected elution peaks on composite tracks: peak apex (scan), peak area, height, baseline boundaries, cSelectivity, SNR, goodness_fitting, and parent_masstrack_id": "<locator>",
    "Execution log confirming single peak-detection pass on composite map vs. N per-sample passes": "<locator>",
    "_mass_grid_mapping.csv file documenting aligned m/z values, sample-track associations, and consensus m/z per grid position": "<locator>",
    "MassGrid object linking aligned mass tracks across all samples with consensus m/z identifiers": "<locator>",
    "Filtered feature table (preferred_Feature_table.tsv) containing only peaks meeting SNR > 2, peakshape > 0.5, and minimum peak height criteria with sample-specific peak areas": "<locator>",
    "Row count comparison report showing number of peaks in full_Feature_table.tsv vs. preferred_Feature_table.tsv": "<locator>",
    "QC summary metrics including SNR distribution, peakshape distribution, and peak height distribution of retained peaks": "<locator>",
    "Scalability benchmark table (CSV or TSV) with columns: sample_count, wall_clock_time_seconds, peak_memory_mb, run_number, mean_time, std_dev_time, mean_memory, std_dev_memory": "<locator>",
    "Wall-clock time vs. sample count plot (PNG or PDF) showing linear or near-linear scaling up to 100+ samples": "<locator>",
    "Peak memory usage vs. sample count plot (PNG or PDF) demonstrating memory efficiency across cohort sizes": "<locator>",
    "Summary report (text or markdown) stating mean throughput (samples/hour) per cohort and extrapolated time estimate for 1000-sample project": "<locator>"
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
