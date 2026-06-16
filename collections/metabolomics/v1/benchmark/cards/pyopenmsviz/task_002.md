# SciTask Card: Reconstruct the layered architecture dispatch from Configuration and Core Base layers to backend-specific rendering

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:19:11.067804+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_pyopenmsviz/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `visualization`, `data-analysis`
- GitHub: `OpenMS/pyopenms_viz`
- Quality: Score 2/5 — Coherent: false, placeholder, 5 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`

## Research Question
How does pyOpenMS-viz route a user's backend specification through its layered architecture to dispatch the plot generation request to the correct plotting library backend?

## Connected Finding
pyOpenMS-viz integrates seamlessly with three plotting library backends: matplotlib, bokeh, and plotly, enabling users to specify which backend to use for visualization generation.

## Task Description
Reconstruct and document the fixed orchestrator control loop that routes a user's `.plot()` call with a `backend=` parameter through the Configuration Classes Layer and Core Base Layer to dispatch to exactly one of three backend Extension Layers (Bokeh, Matplotlib, or Plotly), producing the corresponding backend-specific plot object.

## Inputs
- A user call to `.plot()` on a pandas DataFrame with parameters: `x` (column name), `y` (column name), `kind` (plot type: 'spectrum', 'chromatogram', 'peakmap', or 'mobilogram'), `backend` (one of 'ms_bokeh', 'ms_matplotlib', 'ms_plotly'), and optional parameters from BasePlotConfig or type-specific configs
- Loaded pandas DataFrame containing mass spectrometry data with columns matching the specified x and y axis names

## Expected Outputs
- A backend-specific plot object instantiated from one of the nine Extension Layer classes (e.g., BOKEHSpectrumPlot, MATPLOTLIBChromatogramPlot, PLOTLYPeakMapPlot) with full configuration applied and ready for rendering or further interaction

## Tools
- pyOpenMS-Viz
- Pandas
- Bokeh
- Matplotlib
- Plotly
- Python

## Skills
- orchestrator-architecture-design
- backend-routing-and-dispatch
- multi-inheritance-class-hierarchy
- configuration-object-pattern
- dataframe-plotting-interface-design
- mass-spectrometry-plot-type-specialization

## Workflow Description
1. User invokes `.plot()` method on a pandas DataFrame with parameters including `backend='ms_bokeh'` (or `'ms_matplotlib'` or `'ms_plotly'`), `kind='spectrum'` (or other plot type), and axis names. 2. The call enters the Configuration Classes Layer, which validates and stores plotting parameters in a configuration object (e.g., `SpectrumConfig` for spectrum plots) inheriting from `BasePlotConfig`. 3. The Core Base Layer receives the configuration and instantiates the appropriate base class—either `BasePlot` for simple plots or `BaseMSPlot` for mass-spectrometry plots—matching the specified `kind` parameter. 4. The orchestrator inspects the `backend` parameter and routes the base plot object to the corresponding Extension Layer: `_bokeh` (yielding `BOKEHSpectrumPlot`), `_matplotlib` (yielding `MATPLOTLIBSpectrumPlot`), or `_plotly` (yielding `PLOTLYSpectrumPlot`). 5. The selected Extension Layer's class inherits from both the core base class and a backend-specific mixin (e.g., `BOKEHPlot`), combining configuration validation and backend rendering logic. 6. The backend-specific plot object is instantiated with the configuration and data, rendering the visualization according to backend capabilities (interactive for Bokeh/Plotly, static for Matplotlib).

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
- No changelog documenting the orchestrator architecture, backend routing mechanism, or version history is available in the provided discussion section.

## Domain Knowledge
- The library implements a three-layer architecture: Configuration Classes (e.g., SpectrumConfig, ChromatogramConfig) for parameter validation, Core Base Layer (BasePlot, BaseMSPlot) for plot-type logic, and Extension Layers (_bokeh, _matplotlib, _plotly) for backend-specific rendering.
- Backend routing is determined by the `backend=` parameter passed to `.plot()`, which must be one of 'ms_bokeh', 'ms_matplotlib', or 'ms_plotly' to select the corresponding Extension Layer.
- All mass-spectrometry plot types (Spectrum, Chromatogram, Mobilogram, PeakMap) inherit from BaseMSPlot in the Core layer and have parallel implementations in each of the three Extension Layers, maintaining consistent public API across backends.
- The Configuration Classes layer enforces parameter validation and defaults via Pydantic-style config objects before dispatch, ensuring that invalid parameter combinations fail early in the Configuration stage rather than in the backend-specific layer.
- Interactive backends (Bokeh, Plotly) render vector plots with zoom and hover interactions, while Matplotlib produces static publication-quality raster or vector output, requiring different rendering methods in each Extension Layer despite identical input parameters.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does pyOpenMS-viz route a user's backend specification through its layered architecture to dispatch the plot generation request to the correct plotting library backend?: 'It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] pyOpenMS-viz integrates seamlessly with three plotting library backends: matplotlib, bokeh, and plotly, enabling users to specify which backend to use for visualization generation.: 'It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] A user call to `.plot()` on a pandas DataFrame with parameters: `x` (column name), `y` (column name), `kind` (plot type: 'spectrum', 'chromatogram', 'peakmap', or 'mobilogram'), `backend` (one of 'ms_bokeh', 'ms_matplotlib', 'ms_plotly'), and optional parameters from BasePlotConfig or type-specific configs: 'ms_data.plot(x="m/z", y="intensity", kind="spectrum")'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Loaded pandas DataFrame containing mass spectrometry data with columns matching the specified x and y axis names: 'ms_data = pd.read_csv("path/to/ms_data.csv")
    pd.set_option("plotting.backend", "ms_bokeh")'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] A backend-specific plot object instantiated from one of the nine Extension Layer classes (e.g., BOKEHSpectrumPlot, MATPLOTLIBChromatogramPlot, PLOTLYPeakMapPlot) with full configuration applied and ready for rendering or further interaction: 'These are mass spectrometry plots that inherit from the BaseMSPlot class.

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: class.rst

   BOKEHChromatogramPlot'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] pyOpenMS-Viz: 'pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Pandas: 'ms_data = pd.read_csv("path/to/ms_data.csv")'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] Bokeh: 'Extension: BOKEH'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Matplotlib: 'Extension: MATPLOTLIB'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] Plotly: 'Extension: PLOTLY'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] Python: 'conda create --name=pyopenms-viz python=3.12'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting the orchestrator architecture, backend routing mechanism, or version history is available in the provided discussion section.: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- file_exists: verify that the pyopenms_viz package source code is accessible at github.com/OpenMS/pyopenms_viz
- file_format_is: verify that Configuration Classes Layer files (.py format) exist in the repository structure
- file_format_is: verify that Core Base Layer files (.py format) exist in the repository structure
- file_format_is: verify that Extension Layer files for Bokeh, Matplotlib, and Plotly (.py format) each exist in the repository structure
- contains_substring: verify that source code contains a routing mechanism (function or method) that accepts a 'backend=' keyword argument
- contains_substring: verify that the routing mechanism dispatches to exactly three distinct backend implementations (Bokeh, Matplotlib, Plotly)
- script_runs: verify that a minimal instantiation script (backend= keyword call) executes without error when backend='bokeh', backend='matplotlib', and backend='plotly' are each specified
- output_matches_reference: verify that each backend call produces an object of the correct type (bokeh Figure, matplotlib Axes, plotly Figure), no canonical answer—any of three distinct backend-specific types is valid

### Expert Review
- Confirm that the identified routing mechanism correctly implements the advertised control flow from Configuration Classes Layer → Core Base Layer → one of three Extension Layers
- Assess whether the dispatcher logic is architecturally sound and follows recognized orchestrator patterns for pluggable backends
- Evaluate the completeness of the three backend implementations: do Bokeh, Matplotlib, and Plotly each receive all necessary data and parameters from the Core Base Layer?

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Entry Point: User calls `.plot()` on a pandas DataFrame with `backend=`, `kind=`, `x=`, `y=`, and optional configuration parameters.
2. Configuration Validation Layer: The specified `kind` and optional parameters are passed to the corresponding Configuration Class (e.g., `SpectrumConfig`, `ChromatogramConfig`), which inherits from `BasePlotConfig` and validates all inputs.
3. Core Base Layer Dispatch: Based on `kind`, the orchestrator selects and instantiates the appropriate core base class (`BasePlot` for simple plots or `BaseMSPlot` for mass-spectrometry plots) with validated configuration.
4. Backend Router: The `backend=` parameter is inspected to determine which Extension Layer module (_bokeh, _matplotlib, or _plotly) will provide the final rendering implementation.
5. Backend-Specific Class Instantiation: The chosen Extension Layer's corresponding class (e.g., `BOKEHSpectrumPlot` inheriting from both `BOKEHPlot` and the core base class) is instantiated, binding configuration, data, and backend-specific rendering logic.
6. Validation: The returned plot object is an instance of the correct backend-specific class with all configuration applied, type-checked to ensure the inheritance hierarchy matches both the plot type and the selected backend.

## Workflow Ports

**Inputs:**

- `user_plot_call` — User call to .plot() with backend, kind, x, y, and config parameters
- `dataframe` — Pandas DataFrame with mass spectrometry data

**Outputs:**

- `backend_plot_object` — Instantiated backend-specific plot object ready for rendering

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:OpenMS__pyopenms_viz`
- **Synthesized at:** 2026-06-16T07:25:27+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (5):
  - research_question asks about 'layered architecture' and 'dispatch mechanism', but the finding only states that the tool 'integrates seamlessly' with three backends—this is a semantic gap. The finding does not address *how* routing occurs through layers.
  - evidence_span 'It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)' does not support the research_question's specificity about routing through Configuration and Core layers. The evidence describes *what backends exist*, not *how routing works*.
  - inputs field contains placeholder text: 'ms_data.plot(x="m/z", y="intensity", kind="spectrum")' is a generic example without article-specific method signature confirmation.
  - expected_outputs field uses placeholder class names ('BOKEHSpectrumPlot', 'MATPLOTLIBChromatogramPlot') without evidence they exist in source code or are documented in the provided evidence_span.
  - The evidence_span for tools ('Extension: BOKEH', 'Extension: MATPLOTLIB', 'Extension: PLOTLY') is overly generic and does not confirm implementation details.
- Notes: This card exhibits a significant disconnect between its ambitious research_question (asking for control-flow routing through a three-layer orchestrator architecture) and its minimal evidence base (a single sentence stating integration with three backends). The finding does not address the routing mechanism at all, rendering it incoherent with the research question. The task_description, workflow_description, and domain_knowledge sections are richly detailed but appear to be speculative reconstructions rather than evidence-based claims. No source code references, API documentation, or concrete architectural diagrams ground the multi-layer narrative. All class names and layer descriptions are generic placeholders that would need explicit source-code verification. The card would benefit from: (1) explicit evidence snippets showing the routing logic in actual source code, (2) reformulation of the finding to directly address the research_question's control-flow aspect, (3) removal of speculative architecture details unless grounded in cited documentation, and (4) replacement of generic examples with actual verified API signatures.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
