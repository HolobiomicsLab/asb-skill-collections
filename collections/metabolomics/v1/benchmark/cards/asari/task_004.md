# SciTask Card: Reconstruct the peak quality filtering step and verify SNR, peak-shape, and prominence threshold application

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:33:42.864961+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_asari/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `statistical-analysis`
- DOI: `10.1038/s41467-023-39889-1`
- GitHub: `shuzhao-li-lab/asari_pcpfm_tutorials`
- Input from: `task_001`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `lc-ms`, `feature-detection`, `chromatogram-alignment`, `quality-control`, `database-annotation`
- Keywords: `high-resolution metabolomics` · `lc-ms` · `gc-ms` · `peak detection` · `mass alignment` · `extracted ion chromatogram` · `untargeted metabolomics` · `composite map processing` · `peak quality tracking`

## Research Question
How does the peak quality filtering mechanism using SNR (>2), peak shape goodness-of-fit, and minimum peak height (default 1e5 with >20% prominence) thresholds reduce the number of detected features in the feature table?

## Connected Finding
Asari applies peak quality filtering by tracking selectivity metrics on m/z, chromatography, and annotation databases to refine detected features after composite map peak detection.

## Task Description
Implement quality-based filtering on detected peaks using signal-to-noise ratio (SNR > 2), peak shape (goodness_fitting > 0.5), and minimum peak height (1e5 with ≥20% prominence) thresholds, then generate a filtered feature table and verify row count reduction relative to the unfiltered full_Feature_table.tsv.

## Inputs
- Full unfiltered peak list from composite track peak detection (JSON format with SNR, goodness_fitting, peak_height, prominence, apex, left_base, right_base, parent_masstrack_id, mz, rtime fields)
- Composite mass tracks with aligned intensity vectors across all samples after RT calibration
- RT alignment dictionaries (rt_cal_dict) mapping sample scan numbers to reference sample scan numbers

## Expected Outputs
- Filtered feature table (preferred_Feature_table.tsv) containing only peaks meeting SNR > 2, peakshape > 0.5, and minimum peak height criteria with sample-specific peak areas
- Row count comparison report showing number of peaks in full_Feature_table.tsv vs. preferred_Feature_table.tsv
- QC summary metrics including SNR distribution, peakshape distribution, and peak height distribution of retained peaks

## Expected Output File

- `preferred_Feature_table.tsv`

## Landmark Outputs

- `full_Feature_table.tsv`
- `peak_filter_criteria_applied.json`
- `row_count_comparison.txt`
- `snr_distribution_histogram.png`
- `peakshape_distribution_histogram.png`

## Tools
- Python
- scipy.signal.find_peaks
- asari peaks module

## Skills
- peak-quality-threshold-filtering
- snr-based-signal-validation
- gaussian-peak-shape-evaluation
- prominence-controlled-peak-selection
- feature-table-row-count-validation
- quality-control-metric-distribution-analysis

## Workflow Description
1. Load the full unfiltered peak list (JSON or structured format) from composite track peak detection output containing SNR, goodness_fitting (peakshape), peak_height, and prominence values. 2. Apply SNR threshold filter (SNR > 2) to retain only peaks with sufficient signal-to-noise ratio. 3. Apply peakshape threshold filter (goodness_fitting > 0.5) using gaussian peak evaluation to retain well-shaped peaks. 4. Apply minimum peak height threshold (default 1e5) combined with prominence requirement (≥20% of peak_height) to retain only sufficiently tall and prominent peaks. 5. Compile filtered peak list and map back to individual samples via RT alignment dictionaries to extract sample-specific peak areas and intensities. 6. Generate filtered feature table (preferred_Feature_table.tsv) with peak area intensity values. 7. Count rows in both full and filtered tables and confirm row count reduction is appropriate relative to the unfiltered reference.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/conda_asari_screenshot.png` | figure | False |
| `figures/viz_screen_shot20220518.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history is documented

## Domain Knowledge
- SNR (signal-to-noise ratio) threshold of >2 is the default minimum acceptance criterion for reliable peak detection in LC-MS, balancing sensitivity and specificity across metabolomic datasets.
- Goodness of fitting (peakshape) > 0.5 quantifies how well a detected peak conforms to an expected Gaussian or peak-like distribution; values below 0.5 indicate poor peak shape or potential noise/baseline artifacts.
- Prominence is the vertical distance from peak apex to its lowest contour line and must be ≥20% of peak height to distinguish true metabolite elution peaks from baseline drift or instrument noise in composite mass tracks.
- Minimum peak height threshold (default 1e5) is instrument-specific (tuned for Orbitrap data) and establishes a baseline signal intensity below which peaks are too weak for reliable quantification across samples.
- Peak quality filtering occurs AFTER composite track peak detection (not per-sample) because asari's composite mass track approach sums signals across all samples, enhancing SNR and peak prominence relative to individual sample detection.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: scipy.signal.find_peaks, Filtered feature table (preferred_Feature_table.tsv) containing only peaks meeting SNR > 2, peakshape > 0.5, and minimum peak height criteria with sample-specific peak areas, Row count comparison report showing number of peaks in full_Feature_table.tsv vs. preferred_Feature_table.tsv.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does the peak quality filtering mechanism using SNR (>2), peak shape goodness-of-fit, and minimum peak height (default 1e5 with >20% prominence) thresholds reduce the number of detected features in the feature table?: 'Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Asari applies peak quality filtering by tracking selectivity metrics on m/z, chromatography, and annotation databases to refine detected features after composite map peak detection.: 'Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Full unfiltered peak list from composite track peak detection (JSON format with SNR, goodness_fitting, peak_height, prominence, apex, left_base, right_base, parent_masstrack_id, mz, rtime fields): 'The peaks passing the thresholds (default SNR > 2 and peakshape > 0.5) are reported in a JSON format, with link to the composite mass track identifier.'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Composite mass tracks with aligned intensity vectors across all samples after RT calibration: 'composite mass tracks, where the intensity values are summed on corresponding mass tracks across all samples after RT calibration.'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] RT alignment dictionaries (rt_cal_dict) mapping sample scan numbers to reference sample scan numbers: 'The retention time is converted from scan numbers to seconds. The features have peak positions and boundaries on the composite mass tracks, which are translated to positions on the individual'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Filtered feature table (preferred_Feature_table.tsv) containing only peaks meeting SNR > 2, peakshape > 0.5, and minimum peak height criteria with sample-specific peak areas: 'The recommended feature table is `preferred_Feature_table.tsv`. All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Row count comparison report showing number of peaks in full_Feature_table.tsv vs. preferred_Feature_table.tsv: 'All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards (part of input parameters but default values are fine for most people).'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] QC summary metrics including SNR distribution, peakshape distribution, and peak height distribution of retained peaks: 'The detected elution peaks are evaluated for peakshape, cSelectivity and SNR. The default filters are set low for these values, so that users can decide on their filtering on the feature table.'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Python: 'Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] scipy.signal.find_peaks: 'Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] asari peaks module: 'See [peaks.evaluate_gaussian_peak_on_intensity_list](peaks.evaluate_gaussian_peak_on_intensity_list), [peaks.__peaks_cSelectivity_stats_](peaks.__peaks_cSelectivity_stats_),'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history is documented: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that the asari package repository (github:shuzhao-li-lab/asari) contains peak quality filter implementation with METRIC_SNR, METRIC_PEAKSHAPE, and PARAM_MIN_PEAK_HEIGHT parameters in the peaks module or configuration
- file_exists: full_Feature_table.tsv in test dataset or example output directory
- file_exists: filtered feature table output after applying peak quality thresholds
- row_count_equals: filtered feature table row count is less than or equal to full_Feature_table.tsv row count
- verify that filtered feature table row count demonstrates appropriate reduction relative to unfiltered table (multiple defensible approaches for 'appropriate'—threshold-dependent)
- script_runs: asari peak quality filter function accepts METRIC_SNR (>2), METRIC_PEAKSHAPE goodness_fitting, and PARAM_MIN_PEAK_HEIGHT (default 1e5 with >20% prominence) as parameters without error
- output_matches_reference: filtered feature table structure preserves expected columns from unfiltered full_Feature_table.tsv

### Expert Review
- verify that METRIC_SNR threshold of >2 is scientifically defensible for metabolomics LC-MS peak quality
- verify that METRIC_PEAKSHAPE goodness_fitting metric is an appropriate measure of Gaussian fit quality for chromatographic peaks
- verify that PARAM_MIN_PEAK_HEIGHT default of 1e5 with >20% prominence threshold is reasonable for the instrument sensitivity and sample complexity assumed in test/example datasets
- assess whether row count reduction magnitude is consistent with expected filtering stringency for the thresholds applied

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load full peak list from composite track detection with SNR, peakshape, peak height, and prominence annotations.
2. Filter peaks by SNR > 2 to retain sufficient signal-to-noise measurements.
3. Filter peaks by goodness_fitting > 0.5 using gaussian peak evaluation to select well-shaped peaks.
4. Filter peaks by minimum peak height (1e5) AND prominence ≥20% of peak height to eliminate low-signal and poorly prominent peaks.
5. Map retained peaks back to individual samples via RT alignment dictionaries and extract sample-specific peak areas.
6. Compile filtered feature table with quantitative intensity values per sample.
7. Validation: verify that row count in preferred_Feature_table.tsv is less than full_Feature_table.tsv and that all retained peaks meet the four thresholds (SNR > 2, peakshape > 0.5, height ≥ 1e5, prominence ≥ 20% height).
8. References: source article (DOI: 10.1038/s41467-023-39889-1)

## Workflow Ports

**Inputs:**

- `full_peak_list_json` — Full unfiltered peak list from composite track detection ← `task_001/preferred_feature_table`
- `composite_tracks` — Composite mass tracks with summed intensities
- `rt_calibration_dicts` — RT alignment dictionaries (rt_cal_dict per sample)

**Outputs:**

- `filtered_feature_table` — Filtered feature table meeting quality thresholds
- `row_count_report` — Row count comparison and filtering summary
- `qc_metrics` — QC summary of SNR, peakshape, and height distributions

**Used:** `urn:asb:port:task_001/preferred_feature_table`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:shuzhao-li-lab__asari`
- **Synthesized at:** 2026-06-16T05:44:32+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
