---
name: orchestrator-architecture-design
description: Use when when building a multi-backend visualization library where users
  specify both a plot type (spectrum, chromatogram, peakmap) and a backend (matplotlib
  for static output, Bokeh or Plotly for interactive), and you need to avoid code
  duplication across backends while keeping the user-facing API.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyOpenMS-Viz
  - Pandas
  - Matplotlib
  - Bokeh
  - Plotly
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyopenmsviz
    doi: 10.1021/acs.jproteome.4c00873
    title: pyopenmsviz
  dedup_kept_from: coll_pyopenmsviz
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00873
  all_source_dois:
  - 10.1021/acs.jproteome.4c00873
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# orchestrator-architecture-design

## Summary

Design and implement a layered orchestrator architecture that routes configuration and plot-type specifications through abstraction layers to dispatch rendering requests to the correct backend-specific implementation. This skill enables polymorphic backend selection (matplotlib, Bokeh, Plotly) while maintaining a unified user-facing API.

## When to use

When building a multi-backend visualization library where users specify both a plot type (spectrum, chromatogram, peakmap) and a backend (matplotlib for static output, Bokeh or Plotly for interactive), and you need to avoid code duplication across backends while keeping the user-facing API consistent and simple.

## When NOT to use

- When supporting only a single plotting backend; the orchestrator overhead is not justified for monolithic backends.
- When plot logic differs substantially across backends such that inheritance from a common base is not feasible; consider composition patterns instead.
- When the user-facing API itself must vary by backend (e.g., different method names or parameter names per backend); the architecture assumes a unified interface.

## Inputs

- pandas DataFrame containing mass spectrometry data (e.g., columns: m/z, intensity, rt, or z)
- Configuration parameters: backend string (e.g., 'ms_bokeh', 'ms_matplotlib', 'ms_plotly')
- Plot type specification: kind string (e.g., 'spectrum', 'chromatogram', 'peakmap')
- Axis name mappings and optional rendering flags (e.g., plot3d=True for 3D peakmap)

## Outputs

- Backend-specific plot object (e.g., BOKEHSpectrumPlot, MATPLOTLIBSpectrumPlot, PLOTLYSpectrumPlot)
- Rendered visualization (interactive HTML for Bokeh/Plotly, static matplotlib figure)

## How to apply

Structure the codebase into at least four layers: (1) Configuration Classes Layer that validates and stores plot parameters (e.g., SpectrumConfig inheriting from BasePlotConfig), (2) Core Base Layer that instantiates appropriate base classes (BasePlot or BaseMSPlot) based on the plot kind, (3) an Orchestrator that inspects the backend parameter and routes to the correct Extension Layer, and (4) Extension Layers (e.g., _bokeh, _matplotlib, _plotly) where each plot-type+backend combination is a concrete class inheriting from both the core base class and a backend-specific mixin (e.g., BOKEHPlot). This design separates concerns: configuration validation occurs once, plot logic is inherited from the base, and rendering-specific behavior is encapsulated in mixins. The user calls a single .plot() method on a pandas DataFrame with parameters like backend='ms_bokeh', kind='spectrum', and axis names; the orchestrator transparently selects the correct class (e.g., BOKEHSpectrumPlot) to instantiate and render.

## Related tools

- **pyOpenMS-Viz** (Primary library implementing the orchestrator architecture to route DataFrame plot requests across matplotlib, Bokeh, and Plotly backends) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Data container (DataFrame) that serves as the entry point for the .plot() method and holds mass spectrometry data)
- **Matplotlib** (Static plotting backend accessed via the _matplotlib Extension Layer and MATPLOTLIBSpectrumPlot (or other plot-type classes))
- **Bokeh** (Interactive plotting backend accessed via the _bokeh Extension Layer and BOKEHSpectrumPlot class, inheriting from BOKEHPlot mixin)
- **Plotly** (Interactive plotting backend accessed via the _plotly Extension Layer and PLOTLYSpectrumPlot class)

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum", backend="ms_bokeh")
```

## Evaluation signals

- User-facing .plot() method accepts backend parameter and dispatches to the correct concrete class without user knowledge of internal layer structure.
- All plot-type + backend combinations (spectrum, chromatogram, mobilogram, peakmap with matplotlib, Bokeh, Plotly) instantiate and render without errors.
- Configuration validation occurs in a single Configuration Classes Layer; backend-specific rendering code resides only in Extension Layers, not duplicated across layers.
- Switching backends (e.g., from 'ms_bokeh' to 'ms_matplotlib') requires only changing the backend parameter, not refactoring user code.
- Each concrete plot class correctly inherits rendering behavior from both its core base class (e.g., BaseMSPlot) and its backend mixin (e.g., BOKEHPlot).

## Limitations

- The architecture assumes backend rendering logic can be cleanly separated into mixins; very divergent backend APIs may require additional abstraction or composition patterns.
- Adding a new plot type (beyond spectrum, chromatogram, mobilogram, peakmap) requires creating new configuration and base classes, plus concrete implementations for each backend.
- 3D visualization support is backend-dependent (Matplotlib and Plotly support peakmap 3D; Bokeh does not), requiring conditional logic in the orchestrator.

## Evidence

- [other] The call enters the Configuration Classes Layer, which validates and stores plotting parameters in a configuration object: "The Configuration Classes Layer, which validates and stores plotting parameters in a configuration object (e.g., `SpectrumConfig` for spectrum plots) inheriting from `BasePlotConfig`."
- [other] The Core Base Layer receives the configuration and instantiates the appropriate base class—either `BasePlot` for simple plots or `BaseMSPlot`: "The Core Base Layer receives the configuration and instantiates the appropriate base class—either `BasePlot` for simple plots or `BaseMSPlot` for mass-spectrometry plots—matching the specified `kind`"
- [other] The orchestrator inspects the `backend` parameter and routes the base plot object to the corresponding Extension Layer: "The orchestrator inspects the `backend` parameter and routes the base plot object to the corresponding Extension Layer: `_bokeh` (yielding `BOKEHSpectrumPlot`), `_matplotlib` (yielding"
- [other] The selected Extension Layer's class inherits from both the core base class and a backend-specific mixin: "The selected Extension Layer's class inherits from both the core base class and a backend-specific mixin (e.g., `BOKEHPlot`), combining configuration validation and backend rendering logic."
- [readme] It integrates seamlessly with various plotting library backends (matplotlib, bokeh and plotly): "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation."
