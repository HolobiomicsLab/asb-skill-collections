---
name: configuration-object-pattern
description: Use when when designing a library that needs to support multiple plotting backends (e.g., matplotlib, bokeh, plotly) and you want to avoid reimplementing parameter validation, storage, and dispatch logic for each backend.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyOpenMS-Viz
  - Pandas
  - matplotlib
  - Bokeh
  - Plotly
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

# configuration-object-pattern

## Summary

A design pattern for decoupling user-facing API parameters from backend-specific rendering logic by validating and storing plotting parameters in intermediate configuration objects that inherit from a common base class. This enables flexible routing to multiple backend implementations without duplicating validation logic.

## When to use

When designing a library that needs to support multiple plotting backends (e.g., matplotlib, bokeh, plotly) and you want to avoid reimplementing parameter validation, storage, and dispatch logic for each backend. Specifically, use this pattern when users specify a backend parameter and plot type, and the library must route the request through distinct backend implementations while maintaining a consistent validation interface.

## When NOT to use

- When the library supports only a single plotting backend — the overhead of configuration objects and extension layers adds complexity without routing benefit.
- When parameter validation rules differ significantly between backends — shared base configuration validation may become overly generic or require complex conditional logic.
- When the plotting API is purely functional (stateless) rather than object-oriented — configuration objects are most useful when state must be preserved and passed through layered dispatch.

## Inputs

- Pandas DataFrame with mass spectrometry data (e.g., m/z, intensity, retention time columns)
- User parameters: backend name (string: 'ms_bokeh', 'ms_matplotlib', or 'ms_plotly'), plot kind (string: 'spectrum', 'chromatogram', 'peakmap', 'mobilogram'), and axis column names

## Outputs

- Backend-specific plot object (e.g., BOKEHSpectrumPlot, MATPLOTLIBSpectrumPlot, PLOTLYSpectrumPlot) instantiated with validated configuration and data
- Rendered visualization (static for matplotlib, interactive for bokeh/plotly)

## How to apply

Implement a base configuration class (e.g., `BasePlotConfig`) that validates and stores user parameters such as backend name, plot kind, and axis labels. Create backend-specific configuration subclasses (e.g., `SpectrumConfig` for spectrum plots) that inherit from the base class and are instantiated when the user calls `.plot()` on a Pandas DataFrame with parameters like `backend='ms_bokeh'`, `kind='spectrum'`, and axis names. Pass the validated configuration object to a core base layer (e.g., `BasePlot` or `BaseMSPlot`) that is instantiated based on the plot kind. Finally, route the base plot object to an Extension Layer class (e.g., `BOKEHSpectrumPlot`) selected by inspecting the backend parameter; the Extension Layer class inherits from both the core base class and a backend-specific mixin (e.g., `BOKEHPlot`), combining validation and rendering logic. This separation ensures that validation occurs once at the Configuration Layer and that each backend implementation focuses only on rendering according to its native capabilities.

## Related tools

- **pyOpenMS-Viz** (Platform implementing configuration-object pattern to route pandas DataFrames with mass spectrometry data to matplotlib, bokeh, or plotly backends via parameter validation and inheritance-based dispatch) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Provides DataFrame interface on which `.plot()` method is extended; user data input source)
- **matplotlib** (Static plotting backend accessed via MATPLOTLIBPlot mixin and platform-specific extension classes)
- **Bokeh** (Interactive plotting backend accessed via BOKEHPlot mixin and platform-specific extension classes)
- **Plotly** (Interactive plotting backend accessed via PLOTLYPlot mixin and platform-specific extension classes)

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum", backend="ms_bokeh")
```

## Evaluation signals

- Configuration object is instantiated with the correct derived class (e.g., SpectrumConfig) matching the user-specified plot kind.
- Configuration object contains validated attributes for backend name, plot type, and axis labels; no validation errors are raised for supported parameters.
- The orchestrator correctly inspects the backend parameter and routes the base plot object to the matching Extension Layer class (e.g., BOKEHSpectrumPlot, MATPLOTLIBSpectrumPlot, or PLOTLYSpectrumPlot).
- The instantiated Extension Layer object combines both the core base class interface and the backend-specific mixin, inheriting from both.
- The final rendered visualization displays the data using the correct backend library (interactive features in bokeh/plotly, static rendering in matplotlib).

## Limitations

- The pattern requires defining one configuration class per plot kind (e.g., SpectrumConfig, ChromatogramConfig), which adds maintenance burden as new plot types are added.
- Parameter validation logic in the Configuration Layer must be generic enough to avoid duplication but expressive enough to catch backend-specific constraints, which may require conditional logic.
- The Extension Layer class must inherit from both a core base class and a backend-specific mixin; if multiple inheritance is avoided, dispatch logic must be consolidated elsewhere, complicating the architecture.
- The pattern relies on the orchestrator correctly mapping the backend string parameter to the correct Extension Layer class; misconfiguration leads to routing errors.

## Evidence

- [other] The call enters the Configuration Classes Layer, which validates and stores plotting parameters in a configuration object (e.g., `SpectrumConfig` for spectrum plots) inheriting from `BasePlotConfig`.: "The call enters the Configuration Classes Layer, which validates and stores plotting parameters in a configuration object (e.g., `SpectrumConfig` for spectrum plots) inheriting from `BasePlotConfig`."
- [other] The Core Base Layer receives the configuration and instantiates the appropriate base class—either `BasePlot` for simple plots or `BaseMSPlot` for mass-spectrometry plots—matching the specified `kind` parameter.: "The Core Base Layer receives the configuration and instantiates the appropriate base class—either `BasePlot` for simple plots or `BaseMSPlot` for mass-spectrometry plots—matching the specified `kind`"
- [other] The orchestrator inspects the `backend` parameter and routes the base plot object to the corresponding Extension Layer: `_bokeh` (yielding `BOKEHSpectrumPlot`), `_matplotlib` (yielding `MATPLOTLIBSpectrumPlot`), or `_plotly` (yielding `PLOTLYSpectrumPlot`).: "The orchestrator inspects the `backend` parameter and routes the base plot object to the corresponding Extension Layer: `_bokeh` (yielding `BOKEHSpectrumPlot`), `_matplotlib` (yielding"
- [other] The selected Extension Layer's class inherits from both the core base class and a backend-specific mixin (e.g., `BOKEHPlot`), combining configuration validation and backend rendering logic.: "The selected Extension Layer's class inherits from both the core base class and a backend-specific mixin (e.g., `BOKEHPlot`), combining configuration validation and backend rendering logic."
- [other] pyOpenMS-viz integrates seamlessly with three plotting library backends: matplotlib, bokeh, and plotly, enabling users to specify which backend to use for visualization generation.: "pyOpenMS-viz integrates seamlessly with three plotting library backends: matplotlib, bokeh, and plotly, enabling users to specify which backend to use for visualization generation."
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
