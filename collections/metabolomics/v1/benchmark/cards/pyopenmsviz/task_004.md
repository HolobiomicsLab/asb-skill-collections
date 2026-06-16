# SciTask Card: Analyze relative execution-time performance across backends per plot type

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:19:11.067804+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_pyopenmsviz/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `benchmark-evaluation`, `visualization`
- GitHub: `OpenMS/pyopenms_viz`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, placeholder, 4 grounding failures

## Classification

- Task kind: `analysis`
- Article type: `software-tool`
- Primary domain: `bioinformatics`

## Research Question
Which plotting backend (matplotlib, Bokeh, or Plotly) exhibits the fastest median execution time for each mass spectrometry plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots)?

## Connected Finding
The document provides no reported timing metrics or execution time data for any plot types across the three backends, making backend performance comparison impossible from the available text.

## Task Description
Analyze the gallery execution-time data already reported in the methods section to compute and compare median and range of execution times for each plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots) across the three backends (Bokeh, Matplotlib, Plotly), and produce a summary table identifying which backend is systematically fastest or slowest per plot category.

## Inputs
- Gallery execution-time data table from methods section (19 scripts with per-script execution times in MM:SS.mmm format)

## Expected Outputs
- Structured table (CSV or TSV) with columns: plot_type, backend, median_time_seconds, min_time_seconds, max_time_seconds, n_scripts, rank_within_category
- Comparative visualization (PNG or PDF) showing median execution times as a grouped bar chart or heatmap with plot types on one axis, backends on the other, and execution time as the value metric

## Expected Output File

- `backend_execution_time_comparison.csv`

## Landmark Outputs

- `parsed_timings.csv`
- `aggregated_by_category.csv`
- `backend_performance_table.csv`
- `median_times_heatmap.png`

## Tools
- pyOpenMS-Viz
- pandas
- matplotlib
- Python

## Skills
- execution-time-aggregation-by-category
- performance-metric-comparison-across-backends
- statistical-summary-computation-median-range
- backend-performance-benchmarking
- visualization-comparative-performance-metrics

## Workflow Description
1. Extract the 19 gallery script execution times from the computation-times table in the methods section, categorizing each by plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots) and backend (ms_bokeh, ms_matplotlib, ms_plotly). 2. Compute median execution time for each plot-type and backend combination. 3. Compute min and max execution times (range) for each plot-type and backend combination. 4. Rank backends by median execution time within each plot category to identify fastest and slowest. 5. Generate a structured summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category. 6. Produce a comparative visualization (bar chart or heatmap) showing median times across backends per plot type.

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
- No changelog found.
- No gallery or per-script timing metrics are mentioned in the provided section text. The location, format, and completeness of timing data for the six plot types across three backends is not specified.

## Domain Knowledge
- Gallery scripts are categorized by plot type (chromatogram, mobilogram, spectrum, peakmap) and backend implementation (ms_bokeh, ms_matplotlib, ms_plotly); each script reports a single execution time in MM:SS.mmm format.
- Median execution time per category is more robust than mean for identifying typical backend performance when sample sizes are small (e.g., 1–3 scripts per plot-type–backend combination).
- The range (min–max) reflects variability within a category; backends with consistent narrow ranges are more predictable than those with wide variance.
- Faster execution is desirable for interactive backends (Bokeh, Plotly) in dashboard contexts; static backends (Matplotlib) prioritize output quality over speed.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Which plotting backend (matplotlib, Bokeh, or Plotly) exhibits the fastest median execution time for each mass spectrometry plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots)?: 'It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] The document provides no reported timing metrics or execution time data for any plot types across the three backends, making backend performance comparison impossible from the available text.: '_No examples found.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Gallery execution-time data table from methods section (19 scripts with per-script execution times in MM:SS.mmm format): 'Computation times
=================
**00:06.221** total execution time for 19 files **from all galleries**:

.. list-table::
   :header-rows: 1
   :class: table table-striped sg-datatable

   * -'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Structured table (CSV or TSV) with columns: plot_type, backend, median_time_seconds, min_time_seconds, max_time_seconds, n_scripts, rank_within_category: '**00:06.221** total execution time for 19 files **from all galleries**'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Comparative visualization (PNG or PDF) showing median execution times as a grouped bar chart or heatmap with plot types on one axis, backends on the other, and execution time as the value metric: 'Computation times
================='
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] pandas: 'import pandas as pd
    ms_data = pd.read_csv("path/to/ms_data.csv")'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] matplotlib: 'integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Python: 'conda create --name=pyopenms-viz python=3.12'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found.: '_No changelog found._'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] No gallery or per-script timing metrics are mentioned in the provided section text. The location, format, and completeness of timing data for the six plot types across three backends is not specified.: '[UNTRUSTED_DOCUMENT content does not reference timing metrics, gallery, or benchmark results]'

## Evaluation Strategy
### Direct Checks
- verify that a gallery or timing metrics artifact exists in the repository at github:OpenMS__pyopenms_viz (e.g., benchmark results file, gallery HTML, or timing log)
- verify file_format_is: timing data is structured with columns or fields for plot_type, backend, and execution_time (or equivalent labels)
- verify field_present: each timing record includes at least plot_type (one of: chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots), backend (one of: matplotlib, bokeh, plotly), and a numeric execution time value
- verify script_runs: a Python script can load the reported timing metrics, compute median and range (max − min) for each (plot_type, backend) pair, and output a summary table or dict — robust to parameter choices in binning or aggregation
- verify output_matches_reference: computed medians and ranges are consistent with any summary table or statistics already published in the gallery or article text

### Expert Review
- assess whether the three backends show a systematic ordering (fastest to slowest) that is consistent across all or most plot categories, and whether any differences are practically significant
- evaluate whether backend performance correlates with plot complexity (e.g., whether interactive backends are consistently slower for simple plots)
- judge whether the timing data represents a fair and representative sample (e.g., consistent hardware, sufficient replicates per plot type per backend, comparable data sizes)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Parse the 19 gallery script names and execution times from the computation-times table, extracting plot type and backend from each script filename.
2. Group execution times by plot type and backend combination.
3. Calculate median, minimum, and maximum execution time for each group.
4. Rank backends within each plot type by median execution time (1 = fastest).
5. Assemble results into a structured table and generate a comparative bar chart or heatmap.
6. Validation: Confirm that all 19 scripts are accounted for in the aggregated groups, that median and range values are correctly computed from the original times, and that the ranking correctly reflects the median values.

## Workflow Ports

**Inputs:**

- `gallery_timings` — Gallery execution-time data table from methods section ← `task_001/execution_times_table`

**Outputs:**

- `backend_performance_table` — Structured summary table of median and range execution times per plot type and backend
- `backend_comparison_plot` — Comparative visualization of median execution times across backends by plot type

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:OpenMS__pyopenms_viz`
- **Synthesized at:** 2026-06-16T07:25:32+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (4):
  - finding: evidence_span '_No examples found.' not found in section 'intro' — finding claims no timing data exists, but this is an inferred absence, not grounded text
  - inputs[0]: evidence_span truncated and incomplete — snippet shows table header but not actual timing data rows needed to verify 19 scripts exist with plot_type and backend labels
  - tools[1]: evidence_span mislabeled — cited span 'integrates seamlessly with various plotting library backends' references library integration, not matplotlib as a tool in the workflow
  - missing_information[1]: evidence_span '[UNTRUSTED_DOCUMENT content does not reference timing metrics]' is a meta-comment, not a substring from the actual article section
- Notes: This card exhibits severe internal contradictions and groundedness failures. The research_question and task_objective assume the existence of detailed per-script timing metrics in a gallery computation-times table, while the finding explicitly claims no such timing data exists in the document. The inputs[0] evidence_span is truncated and shows only a table header, making it impossible to verify that the required 19 scripts and their timing breakdowns are actually present. Key fields (tools[1], tools[0]) are either mislabeled or contain generic placeholders rather than article-specific evidence. Before proceeding, the reviewer must: (1) obtain and verify the complete computation-times table from the methods section, (2) confirm that all 19 scripts are listed with their plot_type, backend, and execution_time values, (3) reconcile the contradiction between research_question/task_objective and finding, and (4) re-ground all evidence_spans with exact substrings from the source document. The current card should not proceed to execution.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
