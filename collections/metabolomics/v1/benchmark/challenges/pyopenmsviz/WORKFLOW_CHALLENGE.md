# Workflow Challenge: `coll_pyopenmsviz_workflow`


> pyOpenMS-Viz is a Python library that provides Pandas DataFrame-based visualization of mass spectrometry data across multiple plotting backends (matplotlib, Bokeh, and Plotly). The library supports static and interactive visualizations of spectra, chromatograms, mobilograms, and peak maps.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

pyOpenMS-Viz integrates seamlessly with three plotting library backends—matplotlib, Bokeh, and Plotly—enabling users to specify which backend to use for visualization generation of mass spectrometry data. The library provides a simple interface for creating static or interactive visualizations by calling the .plot() method directly on Pandas DataFrames, supporting plot types including spectra, chromatograms, mobilograms, and peak maps. Execution times for 19 gallery scripts spanning all three backends were measured, with total execution time of 00:06.221 across all galleries. The library supports 3D plotting for peak maps through the matplotlib and Plotly backends via the plot_3d=True flag, enabling interactive three-dimensional visualization of mass spectrometry data.

## Research questions

- What are the per-script execution times for the 19 gallery scripts across the three plotting backends (matplotlib, Bokeh, Plotly), and what is the total gallery execution time?
- How does pyOpenMS-viz route a user's backend specification through its layered architecture to dispatch the plot generation request to the correct plotting library backend?
- Do the four core MS plot components (ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot) successfully render output figures across all three supported plotting backends (matplotlib, Bokeh, Plotly) when executed with publicly available example data?
- Which plotting backend (matplotlib, Bokeh, or Plotly) exhibits the fastest median execution time for each mass spectrometry plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots)?
- Can pyOpenMS-Viz successfully render a 3D peak-map visualization using the Plotly backend on real mass spectrometry data from mzML or Bruker .d format files?

## Methods overview

Create and activate a Python 3.12 conda environment with pyOpenMS-Viz and all three plotting backends installed. Sequentially execute each of the 19 gallery scripts, recording wall-clock time using Python's time module or Unix time command. Aggregate per-script execution times and compute total execution time across all scripts. Tabulate measured execution times in a dataframe matching the reported table structure (Example, Time, Mem columns). Validation: Compare measured per-script times and total aggregate time (00:06.221 minutes) against reported values; verify all 19 scripts executed successfully without errors. Entry Point: User calls `.plot()` on a pandas DataFrame with `backend=`, `kind=`, `x=`, `y=`, and optional configuration parameters. Configuration Validation Layer: The specified `kind` and optional parameters are passed to the corresponding Configuration Class (e.g., `SpectrumConfig`, `ChromatogramConfig`), which inherits from `BasePlotConfig` and validates all inputs. Core Base Layer Dispatch: Based on `kind`, the orchestrator selects and instantiates the appropriate core base class (`BasePlot` for simple plots or `BaseMSPlot` for mass-spectrometry plots) with validated configuration. Backend Router: The `backend=` parameter is inspected to determine which Extension Layer module (_bokeh, _matplotlib, or _plotly) will provide the final rendering implementation. Backend-Specific Class Instantiation: The chosen Extension Layer's corresponding class (e.g., `BOKEHSpectrumPlot` inheriting from both `BOKEHPlot` and the core base class) is instantiated, binding configuration, data, and backend-specific rendering logic. Validation: The returned plot object is an instance of the correct backend-specific class with all configuration applied, type-checked to ensure the inheritance hierarchy matches both the plot type and the selected backend. Install pyOpenMS-Viz library from PyPI or source repository. Load example mass spectrometry data (mzML or Bruker .d) using pymzml, pyOpenMS, or AlphaTims into a pandas DataFrame. For each plot type (spectrum, chromatogram, mobilogram, peakmap), call DataFrame.plot() with appropriate x/y/z columns and plot configuration parameters (SpectrumConfig, ChromatogramConfig, MobilogramConfig, PeakMapConfig). Execute plotting sequentially for all three backends (ms_matplotlib, ms_bokeh, ms_plotly) by setting pandas plotting backend option. Collect generated figure files and verify existence, format, and visual correspondence to gallery reference outputs. Validation: All 12 generated figures (4 plot types × 3 backends) must exist as files in the expected format and visual content must match reference gallery outputs without errors or missing data. Parse the 19 gallery script names and execution times from the computation-times table, extracting plot type and backend from each script filename. Group execution times by plot type and backend combination. Calculate median, minimum, and maximum execution time for each group. Rank backends within each plot type by median execution time (1 = fastest). Assemble results into a structured table and generate a comparative bar chart or heatmap. Validation: Confirm that all 19 scripts are accounted for in the aggregated groups, that median and range values are correctly computed from the original times, and that the ranking correctly reflects the median values. Load mzML or Bruker .d mass spectrometry file into a pandas DataFrame using appropriate parser (PyOpenMS, pymzML, pyteomics, or alphatims) with required columns: m/z, retention time, and intensity. Configure pandas plotting backend to 'ms_plotly' to enable Plotly-based rendering. Call DataFrame.plot() with x='m/z', y='rt', kind='peakmap', plot_3d=True to invoke 3D peak-map visualization. Export the resulting Plotly figure object to an interactive HTML file using write_html() method. Validation: Confirm that the output HTML file contains valid Plotly 3D trace data and renders without errors when opened in a web browser; verify presence of m/z, retention time, and intensity axes and interactive controls.

**Domain:** bioinformatics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data. _[grounded: pyopenms_viz_system]_
- **(finding)** pyOpenMS-Viz integrates seamlessly with various plotting library backends including matplotlib, bokeh, and plotly. _[grounded: pyopenms_viz_system]_
- **(finding)** The recommended way of installing pyOpenMS-viz is through the Python Package Index (PyPI). _[grounded: pyopenms_viz_system]_
- **(finding)** pyOpenMS-viz can be installed with the command 'pip install pyopenmsviz --upgrade'. _[grounded: pyopenms_viz_system]_
- **(finding)** The source code for pyOpenMS-Viz is freely open and accessible on Github at https://github.com/OpenMS/pyopenms_viz under the BSD-3-Clause license. _[grounded: pyopenms_viz_system]_
- **(finding)** Chromatograms can be plotted using kind = chromatogram with retention time on the x-axis and intensity on the y-axis.
- **(finding)** The 'by' parameter in chromatogram plots can be used to separate out different mass traces.
- **(finding)** Mobilograms are a type of plot used to visualize ion mobility data with ion mobility represented on the x-axis and intensity shown on the y-axis.
- **(finding)** Mobilograms are functionally similar to chromatograms.
- **(finding)** Peak Maps can be plotted using kind = peakmap with mass-to-charge on the x-axis, retention time on the y-axis, and intensity on the z-axis or represented by color.
- **(finding)** 3D plotting is enabled using plot_3d=True parameter in Peak Maps.
- **(finding)** 3D plotting for Peak Maps is currently only supported for ms_matplotlib and ms_plotly backends. _[grounded: tool_plotly]_
- **(finding)** A spectrum can be plotted using kind = 'spectrum' with mass-to-charge ratio on the x-axis and intensity on the y-axis.
- **(finding)** pyOpenMS-viz plotting occurs by calling the .plot() method on a pandas dataframe. _[grounded: pyopenms_viz_system]_
- **(finding)** Mandatory plotting values for pyOpenMS-viz include column names for the x and y axes and the kind of plot. _[grounded: pyopenms_viz_system]_
- **(finding)** BOKEH backend is available for simple plots including LinePlot, VLinePlot, and ScatterPlot. _[grounded: tool_bokeh]_
- **(finding)** PLOTLY backend is available for simple plots including PLOTLYLinePlot, PLOTLYVLinePlot, and PLOTLYScatterPlot. _[grounded: tool_plotly]_
- **(finding)** MATPLOTLIB backend is available for simple plots including MATPLOTLIBLinePlot, MATPLOTLIBVLinePlot, and MATPLOTLIBScatterPlot. _[grounded: tool_matplotlib]_
- **(finding)** BOKEH backend is available for mass spectrometry plots including BOKEHChromatogramPlot, BOKEHMobilogramPlot, BOKEHSpectrumPlot, and BOKEHPeakMapPlot. _[grounded: tool_bokeh]_
- **(finding)** PLOTLY backend is available for mass spectrometry plots including PLOTLYChromatogramPlot, PLOTLYMobilogramPlot, PLOTLYSpectrumPlot, and PLOTLYPeakMapPlot. _[grounded: tool_plotly]_
- **(finding)** MATPLOTLIB backend is available for mass spectrometry plots including MATPLOTLIBChromatogramPlot, MATPLOTLIBMobilogramPlot, MATPLOTLIBSpectrumPlot, and MATPLOTLIBPeakMapPlot. _[grounded: tool_matplotlib]_
- **(finding)** Configuration classes are available including BaseConfig, LegendConfig, BasePlotConfig, LineConfig, VLineConfig, ScatterConfig, ChromatogramConfig, MobilogramConfig, SpectrumConfig, and PeakMapConfig.
- **(finding)** Base abstract classes BasePlot and BaseMSPlot are inherited by other classes in pyOpenMS-Viz. _[grounded: pyopenms_viz_system]_
- **(finding)** Simple plot classes include LinePlot, VLinePlot, and ScatterPlot which inherit from the BasePlot class.
- **(finding)** Mass spectrometry plot classes include ChromatogramPlot, MobilogramPlot, SpectrumPlot, and PeakMapPlot which inherit from the BaseMSPlot class. _[grounded: comp_chromatogram_plot]_
- **(finding)** The total execution time for 19 files from all galleries was 00:06.221.
- **(finding)** Key features of pyOpenMS-Viz include DataFrame Based Plotting, Interactive and Static Plotting with multiple backends, and Usage Flexibility. _[grounded: pyopenms_viz_system]_
- **(finding)** pyOpenMS-Viz is licensed under the BSD 3-Clause license. _[grounded: pyopenms_viz_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- ms_plotly backend as alternative to ms_bokeh
- ms_matplotlib backend as alternative to ms_bokeh

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- 3D plotting only supported for ms_matplotlib and ms_plotly backends

## Steps

### Step `task_001`
- Title: Reproduce the backend execution-time benchmark table across all three plotting backends
- Task kind: `reproduction`
- Task: Reproduce the per-script execution times for all 19 gallery scripts across three backends (ms_matplotlib, ms_bokeh, ms_plotly) and verify the reported total gallery execution time of 00:06.221 minutes.
- Inputs:
  - 19 gallery scripts (Python files) across ms_matplotlib, ms_bokeh, and ms_plotly backends from the pyOpenMS-Viz repository
  - pyOpenMS-Viz library, pandas, matplotlib, Bokeh, and Plotly packages installed in Python 3.12 environment
- Expected outputs:
  - A CSV or structured table file with columns (Example, Time, Mem (MB)) containing per-script execution times for all 19 gallery scripts, matching the reported computation times table
  - Total aggregate execution time (minutes:seconds.milliseconds format) across all 19 scripts for verification against reported 00:06.221
- Tools: pyOpenMS-Viz, Pandas, matplotlib, Bokeh, Plotly, Python
- Landmark output files: environment_setup.log, per_script_times.csv, total_execution_time.txt
- Primary expected artifact: `gallery_execution_times.csv`

### Step `task_002`
- Title: Reconstruct the layered architecture dispatch from Configuration and Core Base layers to backend-specific rendering
- Task kind: `component_reconstruction`
- Task: Reconstruct and document the fixed orchestrator control loop that routes a user's `.plot()` call with a `backend=` parameter through the Configuration Classes Layer and Core Base Layer to dispatch to exactly one of three backend Extension Layers (Bokeh, Matplotlib, or Plotly), producing the corresponding backend-specific plot object.
- Inputs:
  - A user call to `.plot()` on a pandas DataFrame with parameters: `x` (column name), `y` (column name), `kind` (plot type: 'spectrum', 'chromatogram', 'peakmap', or 'mobilogram'), `backend` (one of 'ms_bokeh', 'ms_matplotlib', 'ms_plotly'), and optional parameters from BasePlotConfig or type-specific configs
  - Loaded pandas DataFrame containing mass spectrometry data with columns matching the specified x and y axis names
- Expected outputs:
  - A backend-specific plot object instantiated from one of the nine Extension Layer classes (e.g., BOKEHSpectrumPlot, MATPLOTLIBChromatogramPlot, PLOTLYPeakMapPlot) with full configuration applied and ready for rendering or further interaction
- Tools: pyOpenMS-Viz, Pandas, Bokeh, Matplotlib, Plotly, Python

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce chromatogram, mobilogram, spectrum, and peak-map plot outputs for all three backends
- Task kind: `reproduction`
- Task: Execute the four core MS plot types (Spectrum, Chromatogram, Mobilogram, PeakMap) using each of the three visualization backends (matplotlib, Bokeh, Plotly) on publicly available example mass spectrometry data, and verify that output figure files match the reference gallery outputs.
- Inputs:
  - mzML mass spectrometry data files loadable via pymzml or pyOpenMS
  - Bruker .d format ion mobility data loadable via AlphaTims
  - Gallery reference example scripts for spectrum, chromatogram, mobilogram, and peakmap plots
- Expected outputs:
  - Spectrum figure file (PNG or interactive HTML) generated with ms_matplotlib backend
  - Spectrum figure file (PNG or interactive HTML) generated with ms_bokeh backend
  - Spectrum figure file (PNG or interactive HTML) generated with ms_plotly backend
  - Chromatogram figure file (PNG or interactive HTML) generated with ms_matplotlib backend
  - Chromatogram figure file (PNG or interactive HTML) generated with ms_bokeh backend
  - Chromatogram figure file (PNG or interactive HTML) generated with ms_plotly backend
  - Mobilogram figure file (PNG or interactive HTML) generated with ms_matplotlib backend
  - Mobilogram figure file (PNG or interactive HTML) generated with ms_bokeh backend
  - Mobilogram figure file (PNG or interactive HTML) generated with ms_plotly backend
  - PeakMap figure file (PNG or interactive HTML) generated with ms_matplotlib backend
  - PeakMap figure file (PNG or interactive HTML) generated with ms_bokeh backend
  - PeakMap figure file (PNG or interactive HTML) generated with ms_plotly backend
- Tools: pyOpenMS-Viz, Pandas, matplotlib, Bokeh, Plotly, pymzml, pyOpenMS, AlphaTims
- Landmark output files: spectrum_*.png, chromatogram_*.png, mobilogram_*.png, peakmap_*.png, test_results_summary.txt

### Step `task_004`
- Depends on: `task_001`
- Title: Analyze relative execution-time performance across backends per plot type
- Task kind: `analysis`
- Task: Analyze the gallery execution-time data already reported in the methods section to compute and compare median and range of execution times for each plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots) across the three backends (Bokeh, Matplotlib, Plotly), and produce a summary table identifying which backend is systematically fastest or slowest per plot category.
- Inputs:
  - Gallery execution-time data table from methods section (19 scripts with per-script execution times in MM:SS.mmm format)
- Expected outputs:
  - Structured table (CSV or TSV) with columns: plot_type, backend, median_time_seconds, min_time_seconds, max_time_seconds, n_scripts, rank_within_category
  - Comparative visualization (PNG or PDF) showing median execution times as a grouped bar chart or heatmap with plot types on one axis, backends on the other, and execution time as the value metric
- Tools: pyOpenMS-Viz, pandas, matplotlib, Python
- Landmark output files: parsed_timings.csv, aggregated_by_category.csv, backend_performance_table.csv, median_times_heatmap.png
- Primary expected artifact: `backend_execution_time_comparison.csv`

### Step `task_005`
- Depends on: `task_004`
- Title: Extend pyOpenMS-Viz to produce a 3D PeakMap plot via the Plotly backend using the plot_3d=True flag
- Task kind: `extension`
- Task: Implement a 3D peak-map rendering workflow using pyOpenMS-Viz with Plotly backend (`kind='peakmap', plot_3d=True, backend='ms_plotly'`) on real mzML or Bruker .d mass spectrometry data, producing a valid interactive 3D figure file that visualizes m/z (x-axis), retention time (y-axis), and intensity (z-axis or color).
- Inputs:
  - Mass spectrometry data file in mzML format or Bruker .d directory containing chromatographic and spectral information (m/z, retention time, intensity)
  - Parsed pandas DataFrame with required columns for m/z, retention time, and intensity values
- Expected outputs:
  - Interactive 3D peak-map visualization file in HTML format displaying intensity as a surface or scatter plot with m/z (x), retention time (y), and intensity (z) axes
  - Confirmation that the Plotly backend successfully renders the 3D plot without errors
- Tools: pyOpenMS-Viz, Pandas, Plotly, Python, pyOpenMS, pymzml, pyteomics, alphatims
- Landmark output files: ms_data_parsed.csv, peakmap_3d.html
- Primary expected artifact: `peakmap_3d.html`

## Final expected outputs

- `A backend-specific plot object instantiated from one of the nine Extension Layer classes (e.g., BOKEHSpectrumPlot, MATPLOTLIBChromatogramPlot, PLOTLYPeakMapPlot) with full configuration applied and ready for rendering or further interaction` (type: file, tolerance: hash)
- `Spectrum figure file (PNG or interactive HTML) generated with ms_matplotlib backend` (type: file, tolerance: hash)
- `Spectrum figure file (PNG or interactive HTML) generated with ms_bokeh backend` (type: file, tolerance: hash)
- `Spectrum figure file (PNG or interactive HTML) generated with ms_plotly backend` (type: file, tolerance: hash)
- `Chromatogram figure file (PNG or interactive HTML) generated with ms_matplotlib backend` (type: file, tolerance: hash)
- `Chromatogram figure file (PNG or interactive HTML) generated with ms_bokeh backend` (type: file, tolerance: hash)
- `Chromatogram figure file (PNG or interactive HTML) generated with ms_plotly backend` (type: file, tolerance: hash)
- `Mobilogram figure file (PNG or interactive HTML) generated with ms_matplotlib backend` (type: file, tolerance: hash)
- `Mobilogram figure file (PNG or interactive HTML) generated with ms_bokeh backend` (type: file, tolerance: hash)
- `Mobilogram figure file (PNG or interactive HTML) generated with ms_plotly backend` (type: file, tolerance: hash)
- `PeakMap figure file (PNG or interactive HTML) generated with ms_matplotlib backend` (type: file, tolerance: hash)
- `PeakMap figure file (PNG or interactive HTML) generated with ms_bokeh backend` (type: file, tolerance: hash)
- `PeakMap figure file (PNG or interactive HTML) generated with ms_plotly backend` (type: file, tolerance: hash)
- `Interactive 3D peak-map visualization file in HTML format displaying intensity as a surface or scatter plot with m/z (x), retention time (y), and intensity (z) axes` (type: file, tolerance: hash)
- `Confirmation that the Plotly backend successfully renders the 3D plot without errors` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: open — validity-first.** The deterministic match-rubrics above are demoted to *informational*. The binding evaluator is **SCIENTIFIC_VALIDITY** (below). Any scientifically sound method that addresses the research question is valid, and novel findings or unexplored aspects can score positively — **different is not wrong**.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** implicit

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
  "workflow_id": "coll_pyopenmsviz_workflow",
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
    "A backend-specific plot object instantiated from one of the nine Extension Layer classes (e.g., BOKEHSpectrumPlot, MATPLOTLIBChromatogramPlot, PLOTLYPeakMapPlot) with full configuration applied and ready for rendering or further interaction": "<locator>",
    "Spectrum figure file (PNG or interactive HTML) generated with ms_matplotlib backend": "<locator>",
    "Spectrum figure file (PNG or interactive HTML) generated with ms_bokeh backend": "<locator>",
    "Spectrum figure file (PNG or interactive HTML) generated with ms_plotly backend": "<locator>",
    "Chromatogram figure file (PNG or interactive HTML) generated with ms_matplotlib backend": "<locator>",
    "Chromatogram figure file (PNG or interactive HTML) generated with ms_bokeh backend": "<locator>",
    "Chromatogram figure file (PNG or interactive HTML) generated with ms_plotly backend": "<locator>",
    "Mobilogram figure file (PNG or interactive HTML) generated with ms_matplotlib backend": "<locator>",
    "Mobilogram figure file (PNG or interactive HTML) generated with ms_bokeh backend": "<locator>",
    "Mobilogram figure file (PNG or interactive HTML) generated with ms_plotly backend": "<locator>",
    "PeakMap figure file (PNG or interactive HTML) generated with ms_matplotlib backend": "<locator>",
    "PeakMap figure file (PNG or interactive HTML) generated with ms_bokeh backend": "<locator>",
    "PeakMap figure file (PNG or interactive HTML) generated with ms_plotly backend": "<locator>",
    "Interactive 3D peak-map visualization file in HTML format displaying intensity as a surface or scatter plot with m/z (x), retention time (y), and intensity (z) axes": "<locator>",
    "Confirmation that the Plotly backend successfully renders the 3D plot without errors": "<locator>"
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
