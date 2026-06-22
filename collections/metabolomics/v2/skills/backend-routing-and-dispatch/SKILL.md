---
name: backend-routing-and-dispatch
description: Use when you need to support multiple plotting backends for the same data visualization task, and you want to centralize backend selection logic so that users can specify their preferred rendering engine (matplotlib, bokeh, or plotly) at call time without modifying the core plotting logic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyOpenMS-Viz
  - Pandas
  - matplotlib
  - bokeh
  - plotly
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
---

# backend-routing-and-dispatch

## Summary

Route a user's backend specification through a layered software architecture to dispatch plot generation requests to the correct plotting library backend. This skill enables seamless switching between static (matplotlib) and interactive (bokeh, plotly) visualizations without changing application code.

## When to use

Use this skill when you need to support multiple plotting backends for the same data visualization task, and you want to centralize backend selection logic so that users can specify their preferred rendering engine (matplotlib, bokeh, or plotly) at call time without modifying the core plotting logic. Specifically applicable when users invoke `.plot()` on a pandas DataFrame with a `backend` parameter and you need to instantiate the correct backend-specific plot class.

## When NOT to use

- When the user has already committed to a single plotting backend and has no need to switch; the overhead of routing may be unnecessary.
- When the input data is not a pandas DataFrame or lacks the required columns (x, y axes); the architecture assumes DataFrame-based input.
- When implementing a new, unsupported plot type that does not fit the existing base class hierarchy (spectrum, chromatogram, mobilogram, peakmap); extension points must first be added to the base and configuration layers.

## Inputs

- pandas DataFrame with mass spectrometry data (m/z, intensity, retention time, or mobility columns)
- backend parameter (string: 'ms_matplotlib', 'ms_bokeh', or 'ms_plotly')
- plot kind parameter (string: 'spectrum', 'chromatogram', 'mobilogram', or 'peakmap')
- axis column names (x, y, and optionally z for 2D/3D plots)
- plotting configuration parameters (axes labels, titles, styling options)

## Outputs

- Backend-specific plot object (BOKEHSpectrumPlot, MATPLOTLIBSpectrumPlot, or PLOTLYSpectrumPlot)
- Rendered visualization (static image for matplotlib; interactive HTML widget for bokeh/plotly)
- Plot-type-specific configuration object (SpectrumConfig, ChromatogramConfig, etc.)

## How to apply

Implement a layered architecture with three tiers: (1) Configuration Classes Layer that validates and stores plotting parameters in a configuration object (e.g., `SpectrumConfig`) inheriting from `BasePlotConfig`; (2) Core Base Layer that instantiates the appropriate base class (`BasePlot` or `BaseMSPlot`) based on the plot `kind` parameter; (3) Extension Layer with backend-specific subclasses (e.g., `BOKEHSpectrumPlot`, `MATPLOTLIBSpectrumPlot`, `PLOTLYSpectrumPlot`) that each inherit from both their core base class and a backend-specific mixin. Use an orchestrator component that inspects the `backend` parameter (e.g., 'ms_bokeh', 'ms_matplotlib', 'ms_plotly') and routes the configuration and data to the corresponding Extension Layer class. The selected backend-specific plot object is instantiated with the configuration and data, then rendered according to that backend's capabilities.

## Related tools

- **pyOpenMS-Viz** (Implements the layered architecture and routing logic; provides the Configuration, Core Base, and Extension Layers) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Provides the DataFrame input structure and data manipulation context for the routing pipeline)
- **matplotlib** (Backend target for static visualization rendering via MATPLOTLIBPlot mixin)
- **bokeh** (Backend target for interactive visualization rendering via BOKEHPlot mixin)
- **plotly** (Backend target for interactive visualization rendering via PLOTLYPlot mixin)

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum", backend="ms_bokeh")
```

## Evaluation signals

- Verify that the correct backend-specific plot class is instantiated for each backend parameter value (e.g., backend='ms_bokeh' yields a BOKEHSpectrumPlot instance, not a matplotlib instance).
- Confirm that the configuration object is validated and propagated correctly through all layers without loss or mutation.
- Check that the rendered output matches the backend's expected format: static image for matplotlib, interactive HTML widget for bokeh, and interactive HTML widget for plotly.
- Validate that the plot respects the specified kind parameter by confirming the correct base class (BasePlot vs. BaseMSPlot) is used.
- Inspect the inheritance chain of the final plot object to ensure it inherits from both the correct core base class and the backend-specific mixin.

## Limitations

- Only supports three plotting backends: matplotlib (static), bokeh, and plotly (interactive); adding a new backend requires implementing a new Extension Layer class and backend-specific mixin.
- Limited to plot types with explicit support in the configuration layer (spectrum, chromatogram, mobilogram, peakmap); new plot types require extending the BasePlotConfig hierarchy.
- 3D plotting is not supported by the bokeh backend, only by matplotlib and plotly (peakmap plot3d=True works only with matplotlib or plotly).
- The architecture assumes mass spectrometry data in pandas DataFrame format; other data structures or file formats require conversion or wrapper layers.

## Evidence

- [other] The call enters the Configuration Classes Layer, which validates and stores plotting parameters in a configuration object (e.g., `SpectrumConfig` for spectrum plots) inheriting from `BasePlotConfig`.: "The call enters the Configuration Classes Layer, which validates and stores plotting parameters in a configuration object (e.g., `SpectrumConfig` for spectrum plots) inheriting from `BasePlotConfig`."
- [other] The orchestrator inspects the `backend` parameter and routes the base plot object to the corresponding Extension Layer: `_bokeh` (yielding `BOKEHSpectrumPlot`), `_matplotlib` (yielding `MATPLOTLIBSpectrumPlot`), or `_plotly` (yielding `PLOTLYSpectrumPlot`).: "The orchestrator inspects the `backend` parameter and routes the base plot object to the corresponding Extension Layer: `_bokeh` (yielding `BOKEHSpectrumPlot`), `_matplotlib` (yielding"
- [readme] It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation.: "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation."
- [other] The selected Extension Layer's class inherits from both the core base class and a backend-specific mixin (e.g., `BOKEHPlot`), combining configuration validation and backend rendering logic.: "The selected Extension Layer's class inherits from both the core base class and a backend-specific mixin (e.g., `BOKEHPlot`), combining configuration validation and backend rendering logic."
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
