---
name: multi-inheritance-class-hierarchy
description: Use when when you need to support multiple plotting library backends
  (static or interactive) for the same data visualization domain (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyOpenMS-Viz
  - Pandas
  - Matplotlib
  - Bokeh
  - Plotly
  techniques:
  - mass-spectrometry
  license_tier: restricted
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

# Multi-inheritance class hierarchy for backend abstraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Design a layered class architecture using multiple inheritance to decouple plotting configuration, core rendering logic, and backend-specific implementations, enabling seamless switching between matplotlib, Bokeh, and Plotly without duplicating visualization code.

## When to use

When you need to support multiple plotting library backends (static or interactive) for the same data visualization domain (e.g., mass spectrometry spectra, chromatograms, peak maps), and want to avoid code duplication across backend implementations while maintaining a consistent user-facing API.

## When NOT to use

- Single-backend visualization needs where code duplication is not a concern and performance overhead of mixin resolution is unacceptable.
- Plotting domains with radically different rendering logic per backend where a shared core base class would impose artificial constraints.
- Frameworks already providing backend abstraction (e.g., Altair, Plotnine) where re-implementing the pattern would duplicate existing infrastructure.

## Inputs

- User invocation parameters (backend='ms_bokeh'|'ms_matplotlib'|'ms_plotly', kind='spectrum'|'chromatogram'|'peakmap', axis column names)
- Pandas DataFrame with mass spectrometry data columns (m/z, intensity, retention time, etc.)
- Configuration object inheriting from BasePlotConfig (e.g., SpectrumConfig)

## Outputs

- Concrete plot object (e.g., BOKEHSpectrumPlot, MAPLOTLIBSpectrumPlot, PLOTLYSpectrumPlot) instantiated and ready to render
- Rendered visualization in the selected backend format (static image for Matplotlib, interactive HTML for Bokeh/Plotly)

## How to apply

Establish a four-layer hierarchy: (1) Configuration Classes Layer (e.g., BasePlotConfig, SpectrumConfig) that validates and stores plotting parameters independent of backend; (2) Core Base Layer (BasePlot, BaseMSPlot) that handles domain-specific rendering logic (axis setup, data transformation) without backend assumptions; (3) Extension Layer with backend-specific mixins (BOKEHPlot, MAPLOTLIBPlot, PLOTLYPlot) encapsulating rendering calls; (4) Concrete plot classes (e.g., BOKEHSpectrumPlot) that inherit from both the core base class and backend mixin, combining logic through method resolution order. Route the user's backend parameter through an orchestrator that instantiates the appropriate concrete class, ensuring the mixin's backend-specific rendering methods override or extend the base class's generic ones. This pattern eliminates per-backend code duplication while keeping configuration validation and domain logic centralized.

## Related tools

- **pyOpenMS-Viz** (Implements multi-inheritance class hierarchy to dispatch DataFrame.plot() calls to backend-specific plot classes (BOKEHSpectrumPlot, MATLOTLIBSpectrumPlot, PLOTLYSpectrumPlot) via configuration and core base layers) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (Provides DataFrame interface that triggers the .plot() method and supplies data to configuration and base plot classes)
- **Matplotlib** (Backend mixin (MATLOTLIBPlot) and concrete implementation (MATLOTLIBSpectrumPlot) handle static rendering via axes and figure objects)
- **Bokeh** (Backend mixin (BOKEHPlot) and concrete implementation (BOKEHSpectrumPlot) handle interactive rendering with ColumnDataSource and glyphs)
- **Plotly** (Backend mixin (PLOTLYPlot) and concrete implementation (PLOTLYSpectrumPlot) handle interactive rendering with Figure and trace objects)

## Examples

```
ms_data.plot(x='m/z', y='intensity', kind='spectrum', backend='ms_bokeh')
```

## Evaluation signals

- Concrete plot class (e.g., BOKEHSpectrumPlot) successfully inherits from both core base class (BaseMSPlot) and backend mixin (BOKEHPlot) without AttributeError or method resolution conflicts.
- Backend parameter routing correctly instantiates the matching concrete class: 'ms_bokeh' → BOKEHSpectrumPlot, 'ms_matplotlib' → MATLOTLIBSpectrumPlot, 'ms_plotly' → PLOTLYSpectrumPlot.
- Configuration object (SpectrumConfig) validation is applied uniformly before instantiation, regardless of backend selection, with no backend-specific conditional logic in configuration layer.
- Rendered output matches expected format per backend: static image file for Matplotlib, interactive HTML with pan/zoom/hover for Bokeh, interactive HTML with legend toggle for Plotly.
- Code duplication across backends is eliminated: axis setup, data transformation, and labeling logic resides in core base class; only rendering calls (e.g., ax.plot() vs. figure.quad()) are in backend mixins.

## Limitations

- Method resolution order (MRO) complexity increases with multiple inheritance levels; incorrect mixin ordering can cause unintended method shadowing or missing backend-specific behavior.
- Backend-specific features (e.g., Bokeh hover tools, Plotly annotations) must be explicitly implemented in mixins; missing implementations silently fall back to core base class, potentially breaking interactive features.
- Configuration validation in BasePlotConfig does not account for backend-specific constraints (e.g., 3D peakmap supported only in Matplotlib and Plotly, not Bokeh); validation errors may surface late during instantiation.
- Performance overhead of mixin resolution and multiple inheritance can accumulate in high-throughput plotting scenarios; no lazy instantiation of backend classes is described.

## Evidence

- [other] Configuration Classes Layer validates and stores plotting parameters in a configuration object (e.g., SpectrumConfig) inheriting from BasePlotConfig: "the Configuration Classes Layer, which validates and stores plotting parameters in a configuration object (e.g., `SpectrumConfig` for spectrum plots) inheriting from `BasePlotConfig`"
- [other] Core Base Layer instantiates either BasePlot or BaseMSPlot matching the specified kind parameter: "The Core Base Layer receives the configuration and instantiates the appropriate base class—either `BasePlot` for simple plots or `BaseMSPlot` for mass-spectrometry plots—matching the specified `kind`"
- [other] Backend-specific plot class inherits from both core base class and backend mixin, combining configuration and rendering logic: "The selected Extension Layer's class inherits from both the core base class and a backend-specific mixin (e.g., `BOKEHPlot`), combining configuration validation and backend rendering logic"
- [other] Orchestrator inspects backend parameter and routes to corresponding Extension Layer class: "The orchestrator inspects the `backend` parameter and routes the base plot object to the corresponding Extension Layer: `_bokeh` (yielding `BOKEHSpectrumPlot`), `_matplotlib` (yielding"
- [other] Backend-specific plot object rendering varies by backend capability: "The backend-specific plot object is instantiated with the configuration and data, rendering the visualization according to backend capabilities (interactive for Bokeh/Plotly, static for Matplotlib)"
- [readme] Library integrates seamlessly with multiple plotting backends: "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
- [readme] Consistent API across backends enables easy switching: "Consistent API across different plotting backends for easy switching between static and interactive plots"
