# SciTask Card: Reproduce chromatogram, mobilogram, spectrum, and peak-map plot outputs for all three backends

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:19:11.067804+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_pyopenmsviz/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `visualization`, `benchmark-evaluation`
- GitHub: `OpenMS/pyopenms_viz`
- Input from: `task_001`
- Quality: Score 4/5 — clean

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`

## Research Question
Do the four core MS plot components (ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot) successfully render output figures across all three supported plotting backends (matplotlib, Bokeh, Plotly) when executed with publicly available example data?

## Connected Finding
pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including matplotlib, Bokeh, and Plotly, enabling multi-backend visualization of mass spectrometry data.

## Task Description
Execute the four core MS plot types (Spectrum, Chromatogram, Mobilogram, PeakMap) using each of the three visualization backends (matplotlib, Bokeh, Plotly) on publicly available example mass spectrometry data, and verify that output figure files match the reference gallery outputs.

## Inputs
- mzML mass spectrometry data files loadable via pymzml or pyOpenMS
- Bruker .d format ion mobility data loadable via AlphaTims
- Gallery reference example scripts for spectrum, chromatogram, mobilogram, and peakmap plots

## Expected Outputs
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

## Artifact References

### Expected outputs

- `Chromatogram figure file (PNG or interactive HTML) generated with ms_matplotlib backend` → **package_artifact** `figures/test_chromatogram_plot[ms_matplotlib-kwargs0].png` (score 0.2857)
- `Mobilogram figure file (PNG or interactive HTML) generated with ms_matplotlib backend` → **package_artifact** `figures/test_mobilogram_plot[ms_matplotlib-kwargs0].png` (score 0.2857)
- `PeakMap figure file (PNG or interactive HTML) generated with ms_matplotlib backend` → **package_artifact** `figures/test_peakmap_mz_im[ms_matplotlib].png` (score 0.2857)

## Landmark Outputs

- `spectrum_*.png`
- `chromatogram_*.png`
- `mobilogram_*.png`
- `peakmap_*.png`
- `test_results_summary.txt`

## Tools
- pyOpenMS-Viz
- Pandas
- matplotlib
- Bokeh
- Plotly
- pymzml
- pyOpenMS
- AlphaTims

## Skills
- mass-spectrometry-data-visualization-pandas
- chromatogram-plot-generation-retention-time
- spectrum-plot-generation-mz-intensity
- ion-mobility-mobilogram-visualization
- peakmap-heatmap-rendering-mz-rt
- matplotlib-bokeh-plotly-backend-switching
- mzml-data-parsing-pymzml-pyopenms

## Workflow Description
1. Install pyOpenMS-Viz from PyPI using pip install pyopenmsviz --upgrade or clone and install from source (https://github.com/OpenMS/pyopenms_viz) using git clone and pip install -e. 2. Load example mass spectrometry data from publicly available sources (mzML files via pymzml/pyOpenMS, or Bruker .d format via AlphaTims) into a pandas DataFrame. 3. For each of the four plot kinds (spectrum, chromatogram, mobilogram, peakmap), call the DataFrame .plot() method with the appropriate x, y (and z for peakmap) column names, set kind parameter to the plot type, and set backend to ms_matplotlib, ms_bokeh, or ms_plotly sequentially. 4. For spectrum plots, use m/z on x-axis and intensity on y-axis with SpectrumConfig parameters. 5. For chromatogram plots, use retention time on x-axis and intensity on y-axis with optional by parameter for mass trace separation and ChromatogramConfig parameters. 6. For mobilogram plots, use ion mobility on x-axis and intensity on y-axis with optional by parameter for mass trace separation and MobilogramConfig parameters. 7. For peakmap plots, use m/z on x-axis and retention time on y-axis with intensity on z-axis (or color), optionally enabling add_marginals and plot_3d with PeakMapConfig parameters. 8. Verify that each generated figure file matches the corresponding reference output in the gallery (gallery_scripts/ms_matplotlib/, gallery_scripts/ms_bokeh/, gallery_scripts/ms_plotly/) by comparing file existence, format, and visual structure.

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
- No changelog provided to document version history, feature additions, or breaking changes

## Domain Knowledge
- Spectrum plots display m/z ratios (x-axis) versus signal intensity (y-axis), with peaks representing charged molecules detected by the mass spectrometer.
- Chromatograms plot retention time (x-axis) versus intensity (y-axis) and may be separated by the 'by' parameter into distinct mass traces for different ion species or precursor masses.
- Mobilograms are analogous to chromatograms but use ion mobility (inverse reduced mobility or 1/K0) on the x-axis, enabling visualization of conformational separation in drift-tube or traveling-wave ion mobility spectrometry.
- PeakMaps are 2D heatmaps with m/z on x-axis and retention time (or ion mobility) on y-axis, with color or z-axis intensity representing abundance; marginal 1D chromatograms or spectra can be added via add_marginals.
- The three backends (matplotlib, Bokeh, Plotly) produce different output formats: matplotlib generates static PNG/PDF, Bokeh generates interactive HTML with client-side rendering, and Plotly generates interactive HTML with WebGL support for 3D plots.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Do the four core MS plot components (ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot) successfully render output figures across all three supported plotting backends (matplotlib, Bokeh, Plotly) when executed with publicly available example data?: 'integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including matplotlib, Bokeh, and Plotly, enabling multi-backend visualization of mass spectrometry data.: 'It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] mzML mass spectrometry data files loadable via pymzml or pyOpenMS: 'Below are a few examples of how to format data as a pandas dataframe from various python libraries'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Bruker .d format ion mobility data loadable via AlphaTims: '.d
--

.. toctree::
   :maxdepth: 1

   alphatims'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Gallery reference example scripts for spectrum, chromatogram, mobilogram, and peakmap plots: 'gallery_scripts/ms_matplotlib/plot_spectrum_ms_matplotlib.py
   gallery_scripts/ms_bokeh/plot_spectrum_ms_bokeh.py'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Spectrum figure file (PNG or interactive HTML) generated with ms_matplotlib backend: 'gallery_scripts/ms_matplotlib/plot_spectrum_ms_matplotlib.py'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Spectrum figure file (PNG or interactive HTML) generated with ms_bokeh backend: 'gallery_scripts/ms_bokeh/plot_spectrum_ms_bokeh.py'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] Spectrum figure file (PNG or interactive HTML) generated with ms_plotly backend: 'gallery_scripts/ms_plotly/plot_spectrum_ms_plotly.py'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Chromatogram figure file (PNG or interactive HTML) generated with ms_matplotlib backend: 'gallery_scripts/ms_matplotlib/plot_chromatogram_ms_matplotlib.py'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] Chromatogram figure file (PNG or interactive HTML) generated with ms_bokeh backend: 'gallery_scripts/ms_bokeh/plot_chromatogram_ms_bokeh.py'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] Chromatogram figure file (PNG or interactive HTML) generated with ms_plotly backend: 'gallery_scripts/ms_plotly/plot_chromatogram_ms_plotly.py'
- `ev_012` from `agent2_synthesis` (agent2_traced): [other] Mobilogram figure file (PNG or interactive HTML) generated with ms_matplotlib backend: 'gallery_scripts/ms_matplotlib/plot_mobilogram_ms_matplotlib.py'
- `ev_013` from `agent2_synthesis` (agent2_traced): [other] Mobilogram figure file (PNG or interactive HTML) generated with ms_bokeh backend: 'gallery_scripts/ms_bokeh/plot_mobilogram_ms_bokeh.py'
- `ev_014` from `agent2_synthesis` (agent2_traced): [other] Mobilogram figure file (PNG or interactive HTML) generated with ms_plotly backend: 'gallery_scripts/ms_plotly/plot_mobilogram_ms_plotly.py'
- `ev_015` from `agent2_synthesis` (agent2_traced): [other] PeakMap figure file (PNG or interactive HTML) generated with ms_matplotlib backend: 'gallery_scripts/ms_matplotlib/plot_peakmap_ms_matplotlib.py'
- `ev_016` from `agent2_synthesis` (agent2_traced): [other] PeakMap figure file (PNG or interactive HTML) generated with ms_bokeh backend: 'gallery_scripts/ms_bokeh/plot_peakmap_ms_bokeh.py'
- `ev_017` from `agent2_synthesis` (agent2_traced): [other] PeakMap figure file (PNG or interactive HTML) generated with ms_plotly backend: 'gallery_scripts/ms_plotly/plot_peakmap_ms_plotly.py'
- `ev_018` from `agent2_synthesis` (agent2_traced): [other] pyOpenMS-Viz: 'pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames'
- `ev_019` from `agent2_synthesis` (agent2_traced): [other] Pandas: 'ms_data = pd.read_csv("path/to/ms_data.csv")'
- `ev_020` from `agent2_synthesis` (agent2_traced): [other] matplotlib: 'Extension: MATPLOTLIB'
- `ev_021` from `agent2_synthesis` (agent2_traced): [other] Bokeh: 'Extension: BOKEH'
- `ev_022` from `agent2_synthesis` (agent2_traced): [other] Plotly: 'Extension: PLOTLY'
- `ev_023` from `agent2_synthesis` (agent2_traced): [other] pymzml: '.mzML
-----

.. toctree::
   :maxdepth: 1

   pyopenms
   pymzml'
- `ev_024` from `agent2_synthesis` (agent2_traced): [other] pyOpenMS: '.mzML
-----

.. toctree::
   :maxdepth: 1

   pyopenms
   pymzml'
- `ev_025` from `agent2_synthesis` (agent2_traced): [other] AlphaTims: '.d
--

.. toctree::
   :maxdepth: 1

   alphatims'
- `ev_026` from `agent2_synthesis` (agent2_traced): [discussion] No changelog provided to document version history, feature additions, or breaking changes: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- Verify file exists for each of: ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot output figures under matplotlib backend
- Verify file exists for each of: ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot output figures under Bokeh backend
- Verify file exists for each of: ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot output figures under Plotly backend
- Verify file_format_is for each generated plot output (PNG, HTML, or SVG as appropriate to backend)
- Verify script_runs: execution of plot generation code using mzML input via pymzml/pyOpenMS without errors
- Verify script_runs: execution of plot generation code using Bruker .d input via AlphaTims without errors
- Output matches reference deposit: byte-for-byte comparison of static plot outputs (matplotlib/SVG) against gallery reference files; robust to parameter choices for interactive outputs (Bokeh/Plotly HTML)

### Expert Review
- Visual inspection of generated ChromatogramPlot figures across all three backends for correct intensity vs. retention time representation
- Visual inspection of generated MobilogramPlot figures across all three backends for correct intensity vs. ion mobility representation
- Visual inspection of generated SpectrumPlot figures across all three backends for correct m/z vs. intensity representation
- Visual inspection of generated PeakMapPlot figures across all three backends for correct 2D m/z vs. retention time heatmap/scatter representation
- Verification that interactive features (zoom, pan, hover tooltips) function correctly in Bokeh and Plotly outputs

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Install pyOpenMS-Viz library from PyPI or source repository.
2. Load example mass spectrometry data (mzML or Bruker .d) using pymzml, pyOpenMS, or AlphaTims into a pandas DataFrame.
3. For each plot type (spectrum, chromatogram, mobilogram, peakmap), call DataFrame.plot() with appropriate x/y/z columns and plot configuration parameters (SpectrumConfig, ChromatogramConfig, MobilogramConfig, PeakMapConfig).
4. Execute plotting sequentially for all three backends (ms_matplotlib, ms_bokeh, ms_plotly) by setting pandas plotting backend option.
5. Collect generated figure files and verify existence, format, and visual correspondence to gallery reference outputs.
6. Validation: All 12 generated figures (4 plot types × 3 backends) must exist as files in the expected format and visual content must match reference gallery outputs without errors or missing data.

## Workflow Ports

**Inputs:**

- `mzml_data` — mzML mass spectrometry data files ← `task_001/execution_times_table`
- `bruker_d_data` — Bruker .d format ion mobility data
- `gallery_references` — Gallery reference example scripts

**Outputs:**

- `spectrum_matplotlib_fig` — Spectrum figure from ms_matplotlib backend
- `spectrum_bokeh_fig` — Spectrum figure from ms_bokeh backend
- `spectrum_plotly_fig` — Spectrum figure from ms_plotly backend
- `chromatogram_matplotlib_fig` — Chromatogram figure from ms_matplotlib backend
- `chromatogram_bokeh_fig` — Chromatogram figure from ms_bokeh backend
- `chromatogram_plotly_fig` — Chromatogram figure from ms_plotly backend
- `mobilogram_matplotlib_fig` — Mobilogram figure from ms_matplotlib backend
- `mobilogram_bokeh_fig` — Mobilogram figure from ms_bokeh backend
- `mobilogram_plotly_fig` — Mobilogram figure from ms_plotly backend
- `peakmap_matplotlib_fig` — PeakMap figure from ms_matplotlib backend
- `peakmap_bokeh_fig` — PeakMap figure from ms_bokeh backend
- `peakmap_plotly_fig` — PeakMap figure from ms_plotly backend

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:OpenMS__pyopenms_viz`
- **Synthesized at:** 2026-06-16T07:25:29+00:00

## Extraction Quality
- Score: 4/5 — coherent, no placeholders, no flags.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
