# SciTask Card: Reproduce the backend execution-time benchmark table across all three plotting backends

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:19:11.067804+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_pyopenmsviz/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `benchmark-evaluation`, `data-analysis`
- GitHub: `OpenMS/pyopenms_viz`
- Quality: Score 2/5 — Coherent: false, placeholder, 6 grounding failures

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`

## Research Question
What are the per-script execution times for the 19 gallery scripts across the three plotting backends (matplotlib, Bokeh, Plotly), and what is the total gallery execution time?

## Connected Finding
The library integrates seamlessly with three plotting library backends: matplotlib, Bokeh, and Plotly, which are the backends used for the 19 gallery scripts whose execution times must be measured.

## Task Description
Reproduce the per-script execution times for all 19 gallery scripts across three backends (ms_matplotlib, ms_bokeh, ms_plotly) and verify the reported total gallery execution time of 00:06.221 minutes.

## Inputs
- 19 gallery scripts (Python files) across ms_matplotlib, ms_bokeh, and ms_plotly backends from the pyOpenMS-Viz repository
- pyOpenMS-Viz library, pandas, matplotlib, Bokeh, and Plotly packages installed in Python 3.12 environment

## Expected Outputs
- A CSV or structured table file with columns (Example, Time, Mem (MB)) containing per-script execution times for all 19 gallery scripts, matching the reported computation times table
- Total aggregate execution time (minutes:seconds.milliseconds format) across all 19 scripts for verification against reported 00:06.221

## Expected Output File

- `gallery_execution_times.csv`

## Landmark Outputs

- `environment_setup.log`
- `per_script_times.csv`
- `total_execution_time.txt`

## Tools
- pyOpenMS-Viz
- Pandas
- matplotlib
- Bokeh
- Plotly
- Python

## Skills
- script-execution-time-measurement
- python-environment-setup-and-reproducibility
- batch-script-performance-profiling
- mass-spectrometry-visualization-backend-comparison
- computational-execution-table-generation

## Workflow Description
1. Set up a Python 3.12 environment with pyOpenMS-Viz installed via pip and all three plotting backends (matplotlib, Bokeh, Plotly) available. 2. Sequentially execute each of the 19 gallery scripts listed in the computation times table, recording wall-clock execution time for each script using a timer (e.g. Python's time module or Unix time command). 3. Aggregate per-script execution times and compute the total execution time across all 19 scripts. 4. Compare reported execution time for each script against the measured value; compare reported total (00:06.221) against the measured aggregate. 5. Tabulate results in a dataframe matching the structure of the reported table (Example, Time, Mem columns) and export as CSV.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/OpenMS.svg` | figure | False |
| `figures/feature_boundary.png` | figure | False |
| `figures/figure1.svg` | figure | False |
| `figures/peak_boundary.png` | figure | False |
| `figures/pyOpenMSviz_logo_color.png` | figure | False |
| `figures/test_chromatogram_plot[ms_matplotlib-kwargs0].png` | figure | False |
| `figures/test_chromatogram_plot[ms_matplotlib-kwargs1].png` | figure | False |
| `figures/test_chromatogram_plot[ms_matplotlib-kwargs2].png` | figure | False |
| `figures/test_chromatogram_plot[ms_matplotlib-kwargs3].png` | figure | False |
| `figures/test_chromatogram_plot[ms_matplotlib-kwargs4].png` | figure | False |
| `figures/test_chromatogram_with_annotation[ms_matplotlib-kwargs0].png` | figure | False |
| `figures/test_mobilogram_plot[ms_matplotlib-kwargs0].png` | figure | False |
| `figures/test_mobilogram_plot[ms_matplotlib-kwargs1].png` | figure | False |
| `figures/test_mobilogram_plot[ms_matplotlib-kwargs2].png` | figure | False |
| `figures/test_mobilogram_plot[ms_matplotlib-kwargs3].png` | figure | False |
| `figures/test_peakmap_mz_im[ms_matplotlib].png` | figure | False |
| `figures/test_peakmap_plot[ms_matplotlib-kwargs0].png` | figure | False |
| `figures/test_peakmap_plot[ms_matplotlib-kwargs1].png` | figure | False |
| `figures/test_peakmap_plot[ms_matplotlib-kwargs2].png` | figure | False |
| `figures/test_peakmap_plot[ms_matplotlib-kwargs3].png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history is provided for pyOpenMS-viz
- The section text does not specify where per-script execution times and gallery timing data are located or how they are reported
- Details on hardware platform, Python version, and environment configuration used for the reported gallery execution time are not documented
- No documentation of whether the 00:06.221 gallery time includes compilation, import overhead, or only script execution

## Domain Knowledge
- Wall-clock execution time measurement must account for system variability; multiple runs per script may be needed to establish representative baseline timings.
- The three plotting backends (matplotlib, Bokeh, Plotly) exhibit different performance characteristics: Bokeh and Plotly are interactive but may render slower than static matplotlib plots.
- Gallery script execution times depend on underlying data size, visualization complexity (2D vs. 3D), and whether interactive rendering is performed during execution.
- Total execution time is the sum of individual script times, not wall-clock time elapsed; parallel execution or system load can introduce variance between reported and measured times.
- The reported table groups scripts by backend (ms_plotly, ms_bokeh, ms_matplotlib) with execution times ranging from 00:00.052 to 00:01.476 minutes.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What are the per-script execution times for the 19 gallery scripts across the three plotting backends (matplotlib, Bokeh, Plotly), and what is the total gallery execution time?: 'pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] The library integrates seamlessly with three plotting library backends: matplotlib, Bokeh, and Plotly, which are the backends used for the 19 gallery scripts whose execution times must be measured.: 'It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] 19 gallery scripts (Python files) across ms_matplotlib, ms_bokeh, and ms_plotly backends from the pyOpenMS-Viz repository: '**from all galleries**: [contains list of 19 scripts with file paths like gallery_scripts/ms_plotly/plot_peakmap_marginals_ms_plotly.py]'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] pyOpenMS-Viz library, pandas, matplotlib, Bokeh, and Plotly packages installed in Python 3.12 environment: 'pip install pyopenmsviz --upgrade'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] A CSV or structured table file with columns (Example, Time, Mem (MB)) containing per-script execution times for all 19 gallery scripts, matching the reported computation times table: 'Computation times... **00:06.221** total execution time for 19 files'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Total aggregate execution time (minutes:seconds.milliseconds format) across all 19 scripts for verification against reported 00:06.221: '**00:06.221** total execution time for 19 files'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] pyOpenMS-Viz: 'pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Pandas: 'leverages the power of Pandas for data manipulation and representation'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] matplotlib: 'integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] Bokeh: 'integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_011` from `agent2_synthesis` (agent2_traced): [intro] Plotly: 'integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_012` from `agent2_synthesis` (agent2_traced): [other] Python: 'conda create --name=pyopenms-viz python=3.12'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history is provided for pyOpenMS-viz: '_No changelog found._'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] The section text does not specify where per-script execution times and gallery timing data are located or how they are reported: 'No reference to timing data location or format in provided text; only metadata provided: 'Source: github:OpenMS__pyopenms_viz, Synthesized at: 2026-06-16T07:19:09+00:00''
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] Details on hardware platform, Python version, and environment configuration used for the reported gallery execution time are not documented: 'Section text contains no information on execution environment, hardware specs, or Python configuration used for timing measurements'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] No documentation of whether the 00:06.221 gallery time includes compilation, import overhead, or only script execution: 'Section text does not clarify timing scope or boundaries'

## Evaluation Strategy
### Direct Checks
- verify file exists: gallery execution log or timing report in github:OpenMS__pyopenms_viz repository
- file_format_is: timing report is structured (CSV, JSON, YAML, or table) with columns/fields for script_name, backend, and execution_time_seconds
- field_present: each of 19 scripts appears in timing report with entries for all three backends (ms_matplotlib, ms_bokeh, ms_plotly)
- value_in_range: total gallery execution time sum across all script-backend combinations equals 00:06.221 (372.221 seconds), robust to ±0.5 second measurement variance
- script_runs: reproduce gallery build command (e.g., sphinx-build or make gallery) on fresh clone of github:OpenMS__pyopenms_viz and capture wall-clock execution time
- output_matches_reference: reproduced total gallery execution time matches reported 00:06.221 within ±5% (measurement tolerance for hardware/load variation)

### Expert Review
- assess whether reported per-script times are plausible given typical visualization library overhead (matplotlib < bokeh < plotly expected pattern)
- confirm that timing methodology (single run per script vs. averaged runs) is documented and appropriate for performance claims
- evaluate whether 00:06.221 total is reasonable for 19 scripts across 3 backends on contemporary hardware (no obvious bottlenecks or anomalies)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Create and activate a Python 3.12 conda environment with pyOpenMS-Viz and all three plotting backends installed.
2. Sequentially execute each of the 19 gallery scripts, recording wall-clock time using Python's time module or Unix time command.
3. Aggregate per-script execution times and compute total execution time across all scripts.
4. Tabulate measured execution times in a dataframe matching the reported table structure (Example, Time, Mem columns).
5. Validation: Compare measured per-script times and total aggregate time (00:06.221 minutes) against reported values; verify all 19 scripts executed successfully without errors.

## Workflow Ports

**Inputs:**

- `gallery_scripts` — 19 gallery scripts from pyOpenMS-Viz repository
- `env_config` — Python 3.12 environment with pyOpenMS-Viz, pandas, matplotlib, Bokeh, Plotly installed

**Outputs:**

- `execution_times_table` — Per-script execution times table (CSV)
- `total_execution_time` — Total gallery execution time (minutes:seconds.milliseconds)

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:OpenMS__pyopenms_viz`
- **Synthesized at:** 2026-06-16T07:25:24+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (6):
  - inputs[0]: evidence_span not found in section 'other' (value='19 gallery scripts (Python files) across ms_matplotlib, ms_b', span='**from all galleries**: [contains list of 19 scripts with fi')
  - missing_information[1]: evidence_span not found in section 'discussion' (value='The section text does not specify where per-script execution', span='No reference to timing data location or format in provided t')
  - missing_information[2]: evidence_span not found in section 'discussion' (value='Details on hardware platform, Python version, and environmen', span='Section text contains no information on execution environmen')
  - missing_information[3]: evidence_span not found in section 'discussion' (value='No documentation of whether the 00:06.221 gallery time inclu', span='Section text does not clarify timing scope or boundaries')
  - SEMANTIC GAP: research_question asks for 'per-script execution times' and 'total gallery execution time', but finding only establishes that three backends exist—it does not assert that execution time data exists, is measurable, or has been reported
  - SEMANTIC GAP: research_question implies execution times are already documented/available ('What are the per-script execution times...'), but missing_information[1] explicitly states timing data location is unknown
- Notes: This card suffers from a fundamental coherence failure: the research_question presumes pre-measured execution time data exists and is queryable ('What are the per-script execution times...'), but the task_objective frames this as a reproduction task ('Measure and record...'), and missing_information explicitly states timing data location is unknown. The finding does not semantically support the research_question—it only establishes that three plotting backends are supported, not that execution times have been measured or documented. Critical quantitative assertions (e.g., '00:06.221 minutes') lack grounding evidence. The card conflates two distinct activities: (A) discovering and documenting pre-existing timing benchmarks, and (B) reproducing execution time measurements from scratch. The workflow and evaluation_strategy assume (B), but the research_question and task_objective imply (A). Before this card can be executed, clarify: (1) Does a timing report already exist in the repository? (2) If yes, provide its file path and format. (3) If no, reframe research_question as 'Can we measure...' rather than 'What are...'. (4) Document the hardware, Python version, and environment used for the baseline 00:06.221 measurement. Without this foundation, reproducibility and verification are not feasible.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
