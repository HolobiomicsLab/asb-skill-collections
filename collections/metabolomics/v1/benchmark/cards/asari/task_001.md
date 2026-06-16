# SciTask Card: Reproduce the asari end-to-end LC-MS processing pipeline on a public metabolomics dataset

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-16T05:33:42.864961+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_asari/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `information-extraction`, `statistical-analysis`
- DOI: `10.1038/s41467-023-39889-1`
- GitHub: `shuzhao-li-lab/asari_pcpfm_tutorials`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `lc-ms`, `feature-detection`, `chromatogram-alignment`, `quality-control`, `database-annotation`
- Keywords: `high-resolution metabolomics` · `lc-ms` · `gc-ms` · `peak detection` · `mass alignment` · `extracted ion chromatogram` · `untargeted metabolomics` · `composite map processing` · `peak quality tracking`

## Research Question
Does the asari pipeline successfully produce all five canonical output artifacts (preferred_Feature_table.tsv, full_Feature_table.tsv, _mass_grid_mapping.csv, cmap.pickle, and Annotated_empiricalCompounds.json) when executed on a publicly deposited centroided mzML dataset?

## Connected Finding
Asari is designed as a transparent, JSON-centric program with reproducible data structures that enable tracking and backtracking between features and mass tracks (EICs), supporting output artifact generation and traceability.

## Task Description
Execute the complete asari pipeline on a publicly deposited centroided mzML metabolomics dataset and verify production of all canonical output artifacts: preferred_Feature_table.tsv, full_Feature_table.tsv, _mass_grid_mapping.csv, cmap.pickle, epd.pickle, and Annotated_empiricalCompounds.json.

## Inputs
- Centroided mzML files from LC-MS metabolomics experiment in publicly accessible repository (e.g., GitHub, Zenodo, MassIVE, MetaboLights, or local directory)
- Optional: custom parameters YAML file specifying ppm tolerance, min_peak_height, and other processing thresholds

## Expected Outputs
- preferred_Feature_table.tsv: recommended feature intensity table with sample columns and feature rows
- full_Feature_table.tsv: complete peak table including all features meeting SNR and peakshape thresholds
- _mass_grid_mapping.csv: m/z alignment results mapping mass tracks across samples
- cmap.pickle: serialized composite map object for dashboard inspection
- epd.pickle: serialized empirical compound dictionary for dashboard and downstream analysis
- Annotated_empiricalCompounds.json: pre-annotated empirical compounds with isotope/adduct grouping and database matches

## Expected Output File

- `preferred_Feature_table.tsv`

## Landmark Outputs

- `mass_tracks_per_sample.json`
- `_mass_grid_mapping.csv`
- `composite_mass_tracks_detected_peaks.json`
- `full_Feature_table.tsv`
- `Annotated_empiricalCompounds.json`

## Tools
- Python
- pymzml
- scipy.signal.find_peaks
- scipy.signal.detrend
- khipu
- JMS
- HMDB 4

## Skills
- mass-track-construction-from-centroided-spectra
- m/z-alignment-and-mass-grid-assembly
- retention-time-calibration-via-lowess-regression
- composite-mass-track-assembly-and-peak-detection
- feature-annotation-via-isotope-adduct-grouping
- peak-quality-assessment-by-selectivity-and-snr-metrics
- metabolomics-database-search-and-formula-matching

## Workflow Description
1. Build sample registry from input mzML directory using workflow.register_samples. 2. Extract mass tracks for each sample by parsing MS1 spectra with pymzml, binning m/z values to 0.001 amu using chromatograms.get_thousandth_bins, clustering with mass_functions.nn_cluster_by_mz_seeds where m/z ranges exceed 2× tolerance ppm (default 5 ppm), and establishing anchor mass tracks for 13C/12C isotopes and Na/H adducts. 3. Align mass tracks across all samples into a MassGrid using MassGrid.build_grid_sample_wise for ≤10 samples (with pairwise anchor-first alignment) or MassGrid.build_grid_by_centroiding for larger studies, with systematic recalibration when m/z deviation exceeds 1 ppm. 4. Calibrate retention time for each sample by identifying landmark peaks with mSelectivity >0.99 and prominence >20% of peak height, then apply chromatograms.rt_lowess_calibration with 10% boundary extension to obtain per-sample rt_cal_dict. 5. Build composite mass tracks by summing aligned intensity values across all samples after RT calibration. 6. Detect elution peaks on composite mass tracks using peaks.stats_detect_elution_peaks with scipy.signal.find_peaks (local maxima method), adaptive prominence (min 1/3 of min_peak_height, default 1e5), noise-based filtering, and optional detrending or smoothing; evaluate peaks with peaks.evaluate_gaussian_peak_on_intensity_list for peakshape >0.5 and SNR >2. 7. Map detected features back to individual samples via RT alignment dictionaries to extract peak areas and intensities, recording results in CompositeMap.FeatureTable. 8. Perform pre-annotation using khipu to group isotopes and adducts into empirical compounds, then search against HMDB 4 via JMS to obtain matched formulas and isomers. 9. Export results to preferred_Feature_table.tsv, full_Feature_table.tsv, _mass_grid_mapping.csv, cmap.pickle, epd.pickle, and Annotated_empiricalCompounds.json.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/conda_asari_screenshot.png` | figure | False |
| `figures/viz_screen_shot20220518.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog available to document version history, breaking changes, or artifact schema evolution

## Domain Knowledge
- Mass tracks are intensity vectors of full retention-time range with a single consensus m/z; they differ from mass traces (EICs/XICs) by avoiding RT gaps.
- Peak detection uses local maxima with prominence defined as vertical distance to contour line; prominence is dynamically adjusted per mass track and segment based on noise level and max intensity (min 1/3 of min_peak_height, default 1e5 for Orbitrap).
- Anchor mass tracks (13C/12C isotopes and Na/H adducts) serve as high-confidence landmarks for m/z alignment and are prioritized to reduce ambiguity in pairing non-anchor tracks.
- Composite mass tracks superimpose aligned sample signals post-RT-calibration; peak detection occurs once on the composite rather than per-sample, enhancing signal and reducing computation.
- Feature selectivity comprises mSelectivity (m/z distinctness on a track) and cSelectivity (chromatographic peak distinctness); both are tracked and reported to allow user-defined filtering.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: pymzml, scipy.signal.find_peaks, scipy.signal.detrend, JMS, HMDB 4, preferred_Feature_table.tsv: recommended feature intensity table with sample columns and feature rows, full_Feature_table.tsv: complete peak table including all features meeting SNR and peakshape thresholds, _mass_grid_mapping.csv: m/z alignment results mapping mass tracks across samples, cmap.pickle: serialized composite map object for dashboard inspection, epd.pickle: serialized empirical compound dictionary for dashboard and downstream analysis, Annotated_empiricalCompounds.json: pre-annotated empirical compounds with isotope/adduct grouping and database matches.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does the asari pipeline successfully produce all five canonical output artifacts (preferred_Feature_table.tsv, full_Feature_table.tsv, _mass_grid_mapping.csv, cmap.pickle, and Annotated_empiricalCompounds.json) when executed on a publicly deposited centroided mzML dataset?: 'Trackable and scalable Python program for high-resolution metabolomics data processing.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Asari is designed as a transparent, JSON-centric program with reproducible data structures that enable tracking and backtracking between features and mass tracks (EICs), supporting output artifact generation and traceability.: 'Reproducible, track and backtrack between features and mass tracks (EICs); Transparent, JSON centric data structures, easy to chain other tools'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Centroided mzML files from LC-MS metabolomics experiment in publicly accessible repository (e.g., GitHub, Zenodo, MassIVE, MetaboLights, or local directory): 'Input data are centroied mzML files from LC-MS metabolomics.'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Optional: custom parameters YAML file specifying ppm tolerance, min_peak_height, and other processing thresholds: 'Users can supply a custom parameter file `xyz.yaml`, via `--parameters xyz.yaml` in command line.'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] preferred_Feature_table.tsv: recommended feature intensity table with sample columns and feature rows: 'The recommended feature table is `preferred_Feature_table.tsv`.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] full_Feature_table.tsv: complete peak table including all features meeting SNR and peakshape thresholds: 'All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] _mass_grid_mapping.csv: m/z alignment results mapping mass tracks across samples: 'MassGrid is exported as a csv file.'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] cmap.pickle: serialized composite map object for dashboard inspection: 'The composite map is exported as a pickle file, which is used by the visual dashboard.'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] epd.pickle: serialized empirical compound dictionary for dashboard and downstream analysis: 'The dashboard uses these files under the result folder: 'project.json', 'export/cmap.pickle', 'export/epd.pickle''
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Annotated_empiricalCompounds.json: pre-annotated empirical compounds with isotope/adduct grouping and database matches: 'Annotation is exported into both JSON and tsv formats.'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] Python: 'Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] pymzml: 'The default method uses `pymzml` to parse mzML files.'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] scipy.signal.find_peaks: 'Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] scipy.signal.detrend: 'detrend (scipy.signal.detrend) is performed on the mass track.'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] khipu: 'The preannotaion is done via another package khipu (https://github.com/shuzhao-li-lab/khipu)'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] JMS: 'The empirical compounds are searched against known compound database (default HMDB 4) via another package JMS (https://github.com/shuzhao-li/JMS).'
- `ev_017` from `agent2_synthesis` (agent2_traced): [methods] HMDB 4: 'known compound database (default HMDB 4)'
- `ev_018` from `agent2_synthesis` (agent2_traced): [discussion] No changelog available to document version history, breaking changes, or artifact schema evolution: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file 'preferred_Feature_table.tsv' exists in pipeline output directory
- verify file 'full_Feature_table.tsv' exists in pipeline output directory
- verify file '_mass_grid_mapping.csv' exists in pipeline output directory
- verify file 'cmap.pickle' exists in pipeline output directory
- verify file 'Annotated_empiricalCompounds.json' exists in pipeline output directory
- file_format_is 'preferred_Feature_table.tsv' TSV with tab-delimited rows
- file_format_is 'full_Feature_table.tsv' TSV with tab-delimited rows
- file_format_is '_mass_grid_mapping.csv' CSV with comma-delimited rows
- file_format_is 'cmap.pickle' binary pickle format (bytes match pickle magic number)
- file_format_is 'Annotated_empiricalCompounds.json' valid JSON (parseable by standard JSON parser)
- row_count_equals 'preferred_Feature_table.tsv' at least 1 (header row present)
- row_count_equals 'full_Feature_table.tsv' at least 1 (header row present)
- row_count_equals '_mass_grid_mapping.csv' at least 1 (header row present)
- script_runs: asari pipeline execution completes without fatal errors on centroided mzML input, robust to minor version variations in dependencies

### Expert Review
- Verify that feature identifiers in preferred_Feature_table.tsv correspond to valid mass tracks in _mass_grid_mapping.csv
- Verify that Annotated_empiricalCompounds.json contains plausible compound annotations with mass-to-charge ratios consistent with input data m/z range
- Verify that cmap.pickle deserializes to a valid mass grid object with expected internal structure (dictionary or object with mass alignment metadata)
- Verify that full_Feature_table.tsv contains superset of features in preferred_Feature_table.tsv with expected quality/filtering differences

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Parse mzML files and extract MS1 spectra indexed by binned m/z (0.001 amu) to form mzTree.
2. Construct mass tracks per sample by grouping m/z values within 2× ppm tolerance (5 ppm default) and applying nearest-neighbor clustering where needed; establish anchor tracks via isotope/adduct patterns.
3. Align mass tracks across samples via pairwise anchor-first matching (≤10 samples) or centroid-based clustering (>10 samples) to form a MassGrid; recalibrate m/z if systematic offset exceeds 1 ppm.
4. Calibrate retention time per sample by identifying landmark peaks (mSelectivity >0.99, prominence >20% height) and fitting LOWESS regression to reference sample, storing scan-number mappings in rt_cal_dict.
5. Assemble composite mass tracks by summing RT-aligned intensities across samples; detect elution peaks using local maxima with adaptive prominence and noise-based filtering; evaluate peaks for peakshape and SNR.
6. Map detected features back to individual samples using RT calibration dictionaries; extract and report peak areas and intensities.
7. Perform pre-annotation via khipu to group features into empirical compounds by isotope/adduct relationships; search against HMDB 4 via JMS to obtain formula and isomer matches.
8. Validation: verify existence and format of canonical outputs (preferred_Feature_table.tsv, full_Feature_table.tsv, _mass_grid_mapping.csv, cmap.pickle, epd.pickle, Annotated_empiricalCompounds.json) and confirm row/record counts are non-empty and consistent across tables.
9. References: source article (DOI: 10.1038/s41467-023-39889-1)

## Workflow Ports

**Inputs:**

- `mzml_files` — Centroided mzML files from LC-MS metabolomics experiment
- `parameters_yaml` — Optional custom parameters YAML file

**Outputs:**

- `preferred_feature_table` — Recommended feature intensity table (TSV)
- `full_feature_table` — Complete peak table including all SNR/shape-passing features (TSV)
- `mass_grid_mapping` — m/z alignment results mapping mass tracks (CSV)
- `composite_map_pickle` — Serialized composite map for visualization (pickle)
- `empirical_compounds_pickle` — Serialized empirical compounds dictionary (pickle)
- `annotated_compounds_json` — Pre-annotated empirical compounds with database matches (JSON)

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:shuzhao-li-lab__asari`
- **Synthesized at:** 2026-06-16T05:44:32+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
