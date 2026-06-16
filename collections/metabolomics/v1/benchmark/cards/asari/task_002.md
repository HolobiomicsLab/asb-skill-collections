# SciTask Card: Reconstruct the composite-map peak detection step and verify computational efficiency over per-sample detection

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:33:42.864961+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_asari/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `data-analysis`, `statistical-analysis`
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
How does performing peak detection on a single composite map rather than on individual samples improve computational efficiency in metabolomics data processing?

## Connected Finding
Asari implements peak detection using scipy.signal.find_peaks on a composite map constructed from summed mass tracks across all samples, reducing the number of peak-detection algorithm calls from N (one per sample) to one (composite), thereby improving scalability and computational efficiency.

## Task Description
Construct composite mass tracks by summing intensity values across retention-time-aligned samples on the same m/z coordinate, then perform peak detection once on each composite track using scipy.signal.find_peaks with prominence control, confirming single-pass detection rather than per-sample repeated calls.

## Inputs
- Aligned mass tracks per sample with m/z and full-length intensity arrays
- Retention time calibration dictionaries (rt_cal_dict) mapping sample scan numbers to reference coordinates
- Mass grid structure with aligned m/z values across all samples

## Expected Outputs
- Composite mass tracks (summed intensity arrays) indexed by consensus m/z and full RT scan length
- Feature list with detected elution peaks on composite tracks: peak apex (scan), peak area, height, baseline boundaries, cSelectivity, SNR, goodness_fitting, and parent_masstrack_id
- Execution log confirming single peak-detection pass on composite map vs. N per-sample passes

## Expected Output File

- `composite_peaks.json`

## Landmark Outputs

- `composite_mass_tracks.pickle`
- `rt_aligned_indices.csv`
- `track_audit_log.txt`
- `peak_candidate_table.tsv`

## Tools
- Python
- scipy.signal.find_peaks
- scipy.signal.detrend

## Skills
- composite-mass-track-construction
- retention-time-alignment-index-mapping
- chromatographic-peak-detection-with-prominence-control
- baseline-and-noise-level-estimation-from-quartile-statistics
- peak-evaluation-metrics-cSelectivity-SNR-gaussian-fit
- computational-efficiency-single-pass-vs-repeated-detection

## Workflow Description
1. Load aligned mass tracks from all samples and retention-time calibration dictionaries (rt_cal_dict per sample). 2. Synchronize scan-number indices across samples by applying rt_cal_dict to map each sample's scan numbers to reference sample coordinates. 3. Sum intensity values element-wise across all samples for each unique m/z value in the mass grid, producing composite mass tracks as full-length intensity arrays. 4. Audit each composite mass track (peaks.audit_mass_track): check max intensity ceiling (1E8), apply rescaling if needed, detect low-intensity tracks (median < 1e3), perform detrend if median > 10× min_peak_height and >50% of points exceed threshold, compute baseline and noise from bottom-signal quartiles, apply smoothing (moving average) when noise > 1% of max intensity and max intensity < 10× min_peak_height. 5. Subtract baseline+noise filter to isolate positive regions, splitting track into segments. 6. Apply scipy.signal.find_peaks on each segment with dynamic prominence (max of 1/3 min_peak_height, noise level, and 5% of segment max intensity), using min_peak_height and min_timepoints (default 25 scans) for window control. 7. Evaluate detected peaks for gaussian fit (goodness_fitting), chromatographic selectivity (cSelectivity), and signal-to-noise ratio (SNR > 2), retaining only peaks meeting thresholds. Validation: confirm that peak detection invokes find_peaks exactly once per composite track (not N times), and that reported peaks include cSelectivity, SNR, and gaussian fit metrics.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/conda_asari_screenshot.png` | figure | False |
| `figures/viz_screen_shot20220518.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found.

## Domain Knowledge
- Composite mass tracks represent the superposition of aligned signals across all samples at a single m/z coordinate; peaks detected once on the composite map are equivalent to experiment-wide features, avoiding N redundant peak-detection calls.
- Prominence in scipy.signal.find_peaks is the vertical distance from peak apex to its lowest contour line; asari dynamically computes prominence per segment as the maximum of 1/3 min_peak_height, track noise level, and 5% of segment max intensity to account for local signal variability.
- cSelectivity (chromatographic selectivity) quantifies how distinctly an elution peak is resolved from adjacent peaks on the same mass track; values > 0.99 indicate high confidence landmark peaks suitable for retention-time calibration.
- Rescaling of composite tracks with max intensity > 1E8 (ceiling) to a normalized level serves to make peak detection thresholds robust across instruments and studies with varying total signal intensities, with rescaling factors applied back after detection.
- Low-intensity tracks (median intensity < 1e3 threshold) are treated separately with baseline and noise both set to the threshold value, avoiding spurious peak detection in near-noise regions.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: scipy.signal.find_peaks, scipy.signal.detrend.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does performing peak detection on a single composite map rather than on individual samples improve computational efficiency in metabolomics data processing?: 'Peak detection on a composite map instead of repeated on individual samples'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Asari implements peak detection using scipy.signal.find_peaks on a composite map constructed from summed mass tracks across all samples, reducing the number of peak-detection algorithm calls from N (one per sample) to one (composite), thereby improving scalability and computational efficiency.: 'Peak detection on a composite map instead of repeated on individual samples'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Aligned mass tracks per sample with m/z and full-length intensity arrays: 'intensity_track is np.array(full RT length). This increases storage for processed samples, but simplifies i) CMAP construction'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Retention time calibration dictionaries (rt_cal_dict) mapping sample scan numbers to reference coordinates: 'The RT alignment dictionaries only keep differing values and set within sample RT boundaries. This is efficient by ignoring unnecessary tracking'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Mass grid structure with aligned m/z values across all samples: 'Aignment of mass tracks across samples, resulting in the MassGrid'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Composite mass tracks (summed intensity arrays) indexed by consensus m/z and full RT scan length: 'composite mass tracks, where the intensity values are summed on corresponding mass tracks across all samples after RT calibration'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Feature list with detected elution peaks on composite tracks: peak apex (scan), peak area, height, baseline boundaries, cSelectivity, SNR, goodness_fitting, and parent_masstrack_id: 'The peaks passing the thresholds (default SNR > 2 and peakshape > 0.5) are reported in a JSON format, with link to the composite mass track identifier'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Execution log confirming single peak-detection pass on composite map vs. N per-sample passes: 'Peak detection on a composite map instead of repeated on individual samples'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Python: 'Trackable and scalable Python program for high-resolution metabolomics data processing.'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] scipy.signal.find_peaks: 'Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] scipy.signal.detrend: 'detrend (scipy.signal.detrend) is performed on the mass track'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found.: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file exists in asari source repository (github:shuzhao-li-lab/asari) containing COMP_COMPOSITEMAP construction logic
- verify scipy.signal.find_peaks is imported and called exactly once per composite map construction in the peak detection module
- verify function signature of composite map builder accepts summed intensity array as input
- script_runs: execute asari peak detection pipeline on test dataset (github:shuzhao-li/data/tree/main/data) and confirm no errors occur during composite map construction and scipy.signal.find_peaks invocation
- value_in_range: confirm number of find_peaks function calls in execution trace equals 1 (not N where N = number of samples), parameter-sensitive to sample count and batch processing configuration
- file_format_is: verify output composite peak detection result is a structured record (JSON, pickle, or numpy array) containing detected peak indices and properties

### Expert Review
- Confirm that composite map construction (COMP_COMPOSITEMAP) correctly sums intensity values across all samples at each retention time and m/z coordinate before peak detection
- Confirm that single composite-level find_peaks call produces equivalent or superior peak detection sensitivity compared to per-sample peak detection baseline (RESULT_COMPOSITE_EFFICIENCY claim)
- Verify prominence control parameters used in scipy.signal.find_peaks call are appropriate for metabolomics data and documented in code or configuration

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Synchronize all sample mass tracks to reference retention-time coordinates using pre-computed rt_cal_dict mappings.
2. Sum aligned intensity arrays element-wise across samples for each m/z, creating composite mass tracks of consistent length.
3. Audit each composite track: rescale if ceiling exceeded, detect low-intensity baseline/noise, detrend if high-signal-high-noise, apply adaptive smoothing.
4. Subtract baseline+noise filter to isolate positive-intensity regions and segment the track.
5. Apply scipy.signal.find_peaks with dynamic prominence control (max of three criteria) on each segment to detect local maxima.
6. Evaluate peaks for gaussian fit quality (goodness_fitting), chromatographic selectivity (cSelectivity), and SNR, filtering by SNR > 2 threshold.
7. Validation: verify peak detection is called exactly once per composite track (not per sample) and all reported peaks contain cSelectivity, SNR, and goodness_fitting metrics.
8. References: source article (DOI: 10.1038/s41467-023-39889-1)

## Workflow Ports

**Inputs:**

- `aligned_mass_tracks` — Aligned mass tracks per sample with m/z and full-length intensity arrays ← `task_001/preferred_feature_table`
- `rt_calibration_dicts` — Retention time calibration dictionaries mapping sample to reference scan coordinates
- `mass_grid` — Mass grid structure with aligned m/z values across all samples

**Outputs:**

- `composite_tracks` — Composite mass tracks (summed intensity arrays) indexed by m/z
- `feature_list_json` — Feature list with detected peaks: apex, area, height, boundaries, cSelectivity, SNR, goodness_fitting, parent_masstrack_id
- `execution_log` — Execution log confirming single peak-detection pass on composite map

**Used:** `urn:asb:port:task_001/preferred_feature_table`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:shuzhao-li-lab__asari`
- **Synthesized at:** 2026-06-16T05:44:32+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
