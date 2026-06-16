# SciTask Card: Extend pyOpenMS-Viz to produce a 3D PeakMap plot via the Plotly backend using the plot_3d=True flag

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:19:11.067804+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_pyopenmsviz/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `visualization`, `data-processing`
- GitHub: `OpenMS/pyopenms_viz`
- Input from: `task_004`
- Quality: Score 2/5 — Coherent: false, placeholder, 7 grounding failures

## Classification

- Task kind: `extension`
- Article type: `software-tool`
- Primary domain: `bioinformatics`

## Research Question
Can pyOpenMS-Viz successfully render a 3D peak-map visualization using the Plotly backend on real mass spectrometry data from mzML or Bruker .d format files?

## Connected Finding
pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including Plotly, which supports interactive visualizations of mass spectrometry data.

## Task Description
Implement a 3D peak-map rendering workflow using pyOpenMS-Viz with Plotly backend (`kind='peakmap', plot_3d=True, backend='ms_plotly'`) on real mzML or Bruker .d mass spectrometry data, producing a valid interactive 3D figure file that visualizes m/z (x-axis), retention time (y-axis), and intensity (z-axis or color).

## Inputs
- Mass spectrometry data file in mzML format or Bruker .d directory containing chromatographic and spectral information (m/z, retention time, intensity)
- Parsed pandas DataFrame with required columns for m/z, retention time, and intensity values

## Expected Outputs
- Interactive 3D peak-map visualization file in HTML format displaying intensity as a surface or scatter plot with m/z (x), retention time (y), and intensity (z) axes
- Confirmation that the Plotly backend successfully renders the 3D plot without errors

## Expected Output File

- `peakmap_3d.html`

## Landmark Outputs

- `ms_data_parsed.csv`
- `peakmap_3d.html`

## Tools
- pyOpenMS-Viz
- Pandas
- Plotly
- Python
- pyOpenMS
- pymzml
- pyteomics
- alphatims

## Skills
- mass-spectrometry-data-parsing-mzml-bruker
- pandas-dataframe-manipulation-ms-columns
- plotly-3d-surface-scatter-visualization
- peak-map-rendering-retention-time-mz-intensity
- interactive-html-figure-generation-plotly
- backend-compatibility-verification-visualization-library

## Workflow Description
1. Load mass spectrometry data from an mzML or Bruker .d file into a pandas DataFrame using PyOpenMS, pymzML, pyteomics (for mzML) or alphatims (for .d format), ensuring columns for m/z, retention time, and intensity are present. 2. Set the pandas plotting backend to 'ms_plotly' using `pd.set_option('plotting.backend', 'ms_plotly')`. 3. Call the DataFrame.plot() method with parameters `x='m/z'`, `y='rt'`, `z='intensity'` (or omit z for color mapping), `kind='peakmap'`, and `plot_3d=True` to invoke the Plotly 3D rendering engine. 4. Capture the returned Plotly figure object and save it as an interactive HTML file using `fig.write_html()` to verify successful 3D visualization and backend compatibility.

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
- No changelog or version history documentation is available; unclear which version of pyOpenMS-Viz supports 3D peakmap rendering with Plotly backend
- Section text provides no example code, API documentation, or parameter details for the 3D peakmap call (kind='peakmap', plot_3d=True, backend='ms_plotly')
- No sample mzML or Bruker .d datasets are deposited or referenced; unclear whether public test data exists for reproducible execution
- Synthesis date indicates 2026 (future); unclear whether this reflects a real release or a hypothetical/placeholder document

## Domain Knowledge
- Peak maps represent mass spectrometry data with m/z on x-axis, retention time on y-axis, and intensity as z-axis or color dimension, enabling visualization of elution and fragmentation patterns across chromatographic time.
- The Plotly backend in pyOpenMS-Viz is the only implementation currently supporting true 3D rendering of peak maps, while matplotlib supports 3D but with different rendering characteristics suitable for publication.
- Ion intensity in mass spectrometry is typically stored as non-negative numeric values representing detector signal; normalization and log-scaling are common preprocessing steps but not required for 3D visualization.
- Bruker .d directories contain binary data files (e.g., analysis.tdf, analysis.tdf_bin) requiring specialized readers like alphatims; mzML is an open XML format readable by multiple parsers (pyOpenMS, pymzML, pyteomics) with equivalent information content.
- Interactive 3D plots rendered by Plotly must be saved as HTML files to preserve interactivity (rotation, zoom, hover tooltips); static PNG export loses the 3D interaction capability.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Can pyOpenMS-Viz successfully render a 3D peak-map visualization using the Plotly backend on real mass spectrometry data from mzML or Bruker .d format files?: 'It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] pyOpenMS-Viz integrates seamlessly with multiple plotting library backends including Plotly, which supports interactive visualizations of mass spectrometry data.: 'It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Mass spectrometry data file in mzML format or Bruker .d directory containing chromatographic and spectral information (m/z, retention time, intensity): '.mzML ... .d'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Parsed pandas DataFrame with required columns for m/z, retention time, and intensity values: 'ms_data = pd.read_csv("path/to/ms_data.csv")'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Interactive 3D peak-map visualization file in HTML format displaying intensity as a surface or scatter plot with m/z (x), retention time (y), and intensity (z) axes: 'intensity is on the z-axis (or represented by color)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Confirmation that the Plotly backend successfully renders the 3D plot without errors: 'Currently 3D plotting only supported for `ms_matplotlib` and `ms_plotly` backends'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] pyOpenMS-Viz: 'pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Pandas: 'leverages the power of Pandas for data manipulation and representation'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] Plotly: 'integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] Python: 'pyOpenMS-Viz is a Python library'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] pyOpenMS: 'pyopenms ... pymzml ... pyteomics'
- `ev_012` from `agent2_synthesis` (agent2_traced): [other] pymzml: 'pyopenms ... pymzml ... pyteomics'
- `ev_013` from `agent2_synthesis` (agent2_traced): [other] pyteomics: 'pyopenms ... pymzml ... pyteomics'
- `ev_014` from `agent2_synthesis` (agent2_traced): [other] alphatims: 'alphatims'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history documentation is available; unclear which version of pyOpenMS-Viz supports 3D peakmap rendering with Plotly backend: 'No changelog found.'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] Section text provides no example code, API documentation, or parameter details for the 3D peakmap call (kind='peakmap', plot_3d=True, backend='ms_plotly'): '[UNTRUSTED_DOCUMENT] ... [/UNTRUSTED_DOCUMENT] (entire provided section contains only metadata; no method or API reference)'
- `ev_017` from `agent2_synthesis` (agent2_traced): [discussion] No sample mzML or Bruker .d datasets are deposited or referenced; unclear whether public test data exists for reproducible execution: '[UNTRUSTED_DOCUMENT] ... [/UNTRUSTED_DOCUMENT] (no dataset accessions or file paths provided)'
- `ev_018` from `agent2_synthesis` (agent2_traced): [discussion] Synthesis date indicates 2026 (future); unclear whether this reflects a real release or a hypothetical/placeholder document: 'Synthesized at: 2026-06-16T07:19:09+00:00'

## Evaluation Strategy
### Direct Checks
- verify file exists: input mzML or Bruker .d dataset (artifact path must be concrete file or public accession)
- script_runs: Python script calling pyOpenMS-Viz with parameters kind='peakmap', plot_3d=True, backend='ms_plotly' on the input dataset completes without exception
- file_exists: output 3D figure file (HTML or interactive format) is generated by the Plotly backend
- file_format_is: output figure file is valid Plotly HTML (contains 'plotly' in file content or has .html extension with interactive Plotly JSON structure)
- contains_substring: output HTML file contains Plotly.js library reference or '"type":"scatter3d"' indicating 3D rendering
- robust to parameter choices: 3D peakmap renders correctly across multiple representative mzML/Bruker datasets with varying peak densities and m/z ranges

### Expert Review
- Verify that the 3D peakmap visual representation correctly maps m/z (x-axis), retention time or scan number (y-axis), and intensity (z-axis) according to mass spectrometry conventions
- Assess that the interactive Plotly 3D figure is navigable (pan, zoom, rotate) and that peak clusters are visually distinguishable in 3D space
- Confirm that the 3D rendering does not introduce visual artifacts or misalignment of peaks relative to the underlying data values

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load mzML or Bruker .d mass spectrometry file into a pandas DataFrame using appropriate parser (PyOpenMS, pymzML, pyteomics, or alphatims) with required columns: m/z, retention time, and intensity.
2. Configure pandas plotting backend to 'ms_plotly' to enable Plotly-based rendering.
3. Call DataFrame.plot() with x='m/z', y='rt', kind='peakmap', plot_3d=True to invoke 3D peak-map visualization.
4. Export the resulting Plotly figure object to an interactive HTML file using write_html() method.
5. Validation: Confirm that the output HTML file contains valid Plotly 3D trace data and renders without errors when opened in a web browser; verify presence of m/z, retention time, and intensity axes and interactive controls.

## Workflow Ports

**Inputs:**

- `raw_ms_data` — mzML or Bruker .d mass spectrometry dataset ← `task_004/backend_performance_table`
- `parsed_dataframe` — Pandas DataFrame with m/z, retention time, and intensity columns

**Outputs:**

- `peakmap_3d_html` — Interactive 3D peak-map visualization in HTML format
- `rendering_success_log` — Execution log confirming successful Plotly 3D rendering and backend compatibility

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:OpenMS__pyopenms_viz`
- **Synthesized at:** 2026-06-16T07:25:35+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (7):
  - inputs[0]: evidence_span not found in section 'other' (value='Mass spectrometry data file in mzML format or Bruker .d dire', span='.mzML ... .d')
  - tools[4]: evidence_span not found in section 'other' (value='pyOpenMS', span='pyopenms ... pymzml ... pyteomics')
  - tools[5]: evidence_span not found in section 'other' (value='pymzml', span='pyopenms ... pymzml ... pyteomics')
  - tools[6]: evidence_span not found in section 'other' (value='pyteomics', span='pyopenms ... pymzml ... pyteomics')
  - missing_information[1]: evidence_span not found in section 'discussion' (value='Section text provides no example code, API documentation, or', span='[UNTRUSTED_DOCUMENT] ... [/UNTRUSTED_DOCUMENT] (entire provi')
  - missing_information[2]: evidence_span not found in section 'discussion' (value='No sample mzML or Bruker .d datasets are deposited or refere', span='[UNTRUSTED_DOCUMENT] ... [/UNTRUSTED_DOCUMENT] (no dataset a')
  - SEMANTIC GAP: research_question asks 'Can pyOpenMS-Viz successfully render...' (testability/validation) but finding merely asserts 'integrates seamlessly with... Plotly' (capability existence) — finding does not address the core 'can it succeed on real data' question
- Notes: This task card exhibits severe coherence and grounding issues. The research_question focuses on validation ('Can pyOpenMS-Viz successfully render...') but the supporting finding merely confirms capability existence ('integrates with Plotly'), which does not answer the testability claim. Most critically, 6 out of 27 evidence spans fail substring matching, including all references to tool names (pyOpenMS, pymzML, pyteomics) and sample evidence sections. The workflow and API parameters (e.g., `backend='ms_plotly'`, `kind='peakmap'`, `plot_3d=True`) lack grounding in actual source documentation — they appear to be speculative API design. The synthesis date (2026) combined with '[UNTRUSTED_DOCUMENT]' markers and a 'No changelog found' note strongly suggests this is a hypothetical/template task rather than one validated against real pyOpenMS-Viz documentation. The evaluation strategy is sound in principle but cannot be executed without concrete input data and verified API signatures. Recommendation: Return to source documentation to validate that the Plotly 3D rendering API exists, obtain a real mzML/Bruker .d test file with a public accession, and remove future-dated or speculative claims.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
