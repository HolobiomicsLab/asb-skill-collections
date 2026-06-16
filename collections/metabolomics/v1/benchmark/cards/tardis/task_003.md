# SciTask Card: Reproduce the QC Feature Table and Metric CSV Output Files from full peak detection mode

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:24:56.964844+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_tardis/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `data-analysis`
- DOI: `10.1021/acs.analchem.5c00567`
- GitHub: `pablovgd/TARDIS`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `multi-omics`
- Subdomains: `lipidomics`, `untargeted-metabolomics`, `computational-metabolomics`
- Techniques: `lc-ms`, `feature-detection`, `chromatogram-alignment`, `quality-control`, `spectral-library-matching`

## Research Question
What quantitative metrics and output tables does tardisPeaks() generate when run in peak detection mode (screening_mode=FALSE) on LC-MS data?

## Connected Finding
tardisPeaks() with screening_mode=FALSE produces multiple output tables including: a data.frame with per-target AUC values across runs, a QC feature table tibble with average metrics, and CSV files containing Max Intensity, SNR, peak_cor, and points over the peak for all targets.

## Task Description
Run tardisPeaks() with screening_mode=FALSE on the vignette LC-MS dataset after retention-time adjustment for targets 1577 and 1583, and reproduce the output QC feature table tibble and per-metric CSV files (AUC, Max Intensity, SNR, peak_cor, pop) to the designated output directory.

## Inputs
- task_001.expected_outputs[0]: Formatted target data.frame with polarity-filtered rows and standardized column structure
- Vignette LC-MS dataset in .mzML centroided format with compound target list specifying compound ID, name, m/z, expected RT (minutes), and polarity

## Expected Outputs
- QC feature table tibble containing average metrics for each target in QC runs
- CSV file with AUC values for each target in each run
- CSV files with Max Intensity, SNR, peak_cor, and points over peak metrics
- Extracted Ion Chromatograms (EICs) saved in the output folder

## Expected Output File

- `qc_feature_table.csv`

## Landmark Outputs

- `targets_1577_1583_rt_adjusted.RData`
- `qc_feature_table.csv`
- `auc_metrics.csv`
- `max_intensity_metrics.csv`
- `snr_metrics.csv`
- `peak_cor_metrics.csv`

## Tools
- Spectra
- xcms
- R
- knitr
- kableExtra

## Skills
- chromatographic-peak-detection-and-integration
- retention-time-correction-and-alignment
- lc-ms-quality-metric-computation
- targeted-metabolite-extraction
- spectral-data-format-conversion
- polarity-aware-data-filtering

## Workflow Description
1. Load the vignette LC-MS dataset in .mzML centroided format using the Spectra package. 2. Adjust retention times for targets 1577 and 1583 using the xcms retention-time correction algorithm. 3. Execute tardisPeaks() with screening_mode=FALSE to perform peak detection across all runs with polarity filtering applied automatically within TARDIS. 4. Extract and write the QC feature table tibble (containing average metrics for each target in QC runs) to the output directory. 5. Export per-metric CSV files (AUC, Max Intensity, SNR, peak_cor, and points over peak) to the output directory. 6. Verify that extracted ion chromatograms (EICs) are saved to the output folder for inspection.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/Component_131.png` | figure | False |
| `figures/Component_14.png` | figure | False |
| `figures/Component_15.png` | figure | False |
| `figures/Component_1576.png` | figure | False |
| `figures/Component_1577.png` | figure | False |
| `figures/Component_1578.png` | figure | False |
| `figures/Component_1583.png` | figure | False |
| `figures/Component_17.png` | figure | False |
| `figures/Component_179.png` | figure | False |
| `figures/Component_183.png` | figure | False |
| `figures/Component_21.png` | figure | False |
| `figures/Component_22.png` | figure | False |
| `figures/Component_23.png` | figure | False |
| `figures/Component_24.png` | figure | False |
| `figures/Component_25.png` | figure | False |
| `figures/Component_331.png` | figure | False |
| `figures/Component_7.png` | figure | False |
| `figures/Component_9.png` | figure | False |
| `figures/tardis.png` | figure | False |
| `figures/tardis_new.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog documentation available

## Domain Knowledge
- Retention-time adjustment is required before peak detection to ensure accurate alignment of target compounds across multiple LC-MS runs, especially when baseline drift or instrumental variation occurs.
- Screening mode identifies whether target m/z and retention-time windows contain visible signals before committing computational resources to full peak detection; setting screening_mode=FALSE enables peak detection across all runs after screening confirmation.
- QC feature tables (tibbles) aggregate per-run metrics into a single summary for quality control oversight, while individual run metrics (AUC, Max Intensity, SNR, peak_cor, points-over-peak) allow detection of run-specific anomalies or instrument performance degradation.
- Polarity filtering within TARDIS automatically separates positive and negative ion-mode data based on the polarity column in the target list, eliminating the need for pre-processing subsetting.
- Extracted Ion Chromatograms (EICs) serve as visual validation artifacts that allow manual inspection of peak shape, baseline noise, and potential co-elution interference before accepting automated integration results.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] What quantitative metrics and output tables does tardisPeaks() generate when run in peak detection mode (screening_mode=FALSE) on LC-MS data?: 'The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run and a `tibble` that contains a feature table with the average metrics for each target in the QC'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] tardisPeaks() with screening_mode=FALSE produces multiple output tables including: a data.frame with per-target AUC values across runs, a QC feature table tibble with average metrics, and CSV files containing Max Intensity, SNR, peak_cor, and points over the peak for all targets.: 'Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak) and are saved into the output folder.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Vignette LC-MS dataset in .mzML centroided format with compound target list specifying compound ID, name, m/z, expected RT (minutes), and polarity: 'Input files need to be converted to the .mzML format and have to be centroided; compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column'
- `ev_004` from `agent2_synthesis` (agent2_traced): [results] QC feature table tibble containing average metrics for each target in QC runs: 'a `tibble` that contains a feature table with the average metrics for each target in the QC runs'
- `ev_005` from `agent2_synthesis` (agent2_traced): [results] CSV file with AUC values for each target in each run: 'The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run'
- `ev_006` from `agent2_synthesis` (agent2_traced): [results] CSV files with Max Intensity, SNR, peak_cor, and points over peak metrics: 'Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak)'
- `ev_007` from `agent2_synthesis` (agent2_traced): [results] Extracted Ion Chromatograms (EICs) saved in the output folder: 'The resulting EICs are again saved in the output folder and can be inspected'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Spectra: 'loads MS data as `Spectra` objects so it's easily integrated with other tools'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] xcms: 'It makes use of an established retention time correction algorithm from the `xcms` package'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] R: 'R package for *TArgeted Raw Data Integration In Spectrometry*'
- `ev_011` from `agent2_synthesis` (agent2_traced): [results] knitr: 'knitr::include_graphics'
- `ev_012` from `agent2_synthesis` (agent2_traced): [results] kableExtra: 'kableExtra::kable'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documentation available: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file_exists: output directory contains per-metric CSV files named 'AUC.csv', 'Max Intensity.csv', 'SNR.csv', 'peak_cor.csv', and 'pop.csv' (or 'points over the peak.csv')
- verify file_format_is: each per-metric CSV file is valid comma-separated format with row_count_equals at least 1 data row plus header
- verify output_matches_reference: QC feature table tibble structure contains columns for target identifiers and average metric values across QC runs
- verify script_runs: tardisPeaks() function executes without error when called with screening_mode=FALSE on vignette dataset after RT adjustment for targets 1577 and 1583
- verify field_present: output tibble contains expected columns corresponding to metrics (AUC, Max Intensity, SNR, peak_cor, pop)
- verify row_count_equals: number of rows in output tibble matches number of unique targets in vignette target list

### Expert Review
- Verify that QC feature table tibble values (average metrics per target) are scientifically plausible given typical LC–MS metabolomics data ranges and peak quality thresholds
- Assess whether per-metric CSV files contain sufficient detail and consistency to support targeted metabolomics quality assessment workflows
- Review RT adjustment procedure applied to targets 1577 and 1583 for correctness relative to xcms retention time correction methodology

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load vignette LC-MS data in centroided .mzML format using Spectra package.
2. Apply xcms retention-time correction algorithm to align targets 1577 and 1583 across runs.
3. Execute tardisPeaks() with screening_mode=FALSE to perform targeted peak detection with automatic polarity filtering.
4. Calculate area-under-curve (AUC), max intensity, signal-to-noise ratio (SNR), peak correlation (peak_cor), and points-over-peak for each target in each run.
5. Aggregate per-run metrics into QC feature table tibble (average metrics per target across QC runs) and export individual metric tables (AUC, Max Intensity, SNR, peak_cor, pop) as CSV files.
6. Save extracted ion chromatograms (EICs) to output directory for manual quality inspection.
7. Validation: Verify that QC feature table tibble and all per-metric CSV files (AUC, Max Intensity, SNR, peak_cor, pop) are successfully written to the output directory with correct structure and non-empty content matching expected metric columns.
8. References: source article (DOI: 10.1021/acs.analchem.5c00567)

## Workflow Ports

**Inputs:**

- `raw_mzml_data` — Vignette LC-MS dataset in .mzML centroided format
- `target_list` — Compound target list (ID, name, m/z, RT, polarity)

**Outputs:**

- `qc_feature_table` — QC feature table tibble with average metrics per target
- `auc_csv` — AUC metrics table (CSV)
- `intensity_snr_metrics` — Max Intensity, SNR, peak_cor, points-over-peak tables (CSV)
- `eic_chromatograms` — Extracted Ion Chromatograms (EICs)

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:UGent-LIMET__TARDIS`
- **Synthesized at:** 2026-06-16T07:31:03+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
