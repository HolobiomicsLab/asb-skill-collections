---
name: dataframe-plotting-interface-design
description: 'Use when when building a scientific visualization library that must
  support multiple plotting backends and needs to avoid backend-specific code duplication.
  Specifically: (1) your domain (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - pandas
  - matplotlib
  - Bokeh
  - Plotly
  - pyOpenMS-Viz
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

# dataframe-plotting-interface-design

## Summary

Design and implement a layered architecture that abstracts plotting logic across multiple backends (matplotlib, Bokeh, Plotly) while exposing a unified, backend-agnostic interface on Pandas DataFrames. This skill enables users to switch between static and interactive visualization libraries without changing application code.

## When to use

When building a scientific visualization library that must support multiple plotting backends and needs to avoid backend-specific code duplication. Specifically: (1) your domain (e.g., mass spectrometry) has multiple plot types (spectrum, chromatogram, peak map) that should work across all backends; (2) end users need to specify backend choice at call time without rewriting logic; (3) you want to extend Pandas DataFrame methods with domain-specific plotting without modifying Pandas itself.

## When NOT to use

- When only a single plotting backend is required; a monolithic design is simpler and faster to maintain.
- When plot types are heterogeneous and cannot be unified under shared base abstractions; layering adds complexity without reuse.
- When end users cannot or should not specify backend choice at runtime; hardcoding a single backend eliminates dispatcher overhead.

## Inputs

- Pandas DataFrame with mass spectrometry data (e.g., m/z, intensity, retention time columns)
- User-supplied parameters: backend name (string: 'ms_matplotlib', 'ms_bokeh', 'ms_plotly'), plot type (string: 'spectrum', 'chromatogram', 'peakmap'), axis column names (strings), optional plot configuration parameters

## Outputs

- Backend-specific plot object (e.g., MATPLOTLIBSpectrumPlot, BOKEHSpectrumPlot, PLOTLYSpectrumPlot) ready for rendering
- Rendered visualization (static image for Matplotlib, interactive widget for Bokeh/Plotly)

## How to apply

Implement a four-layer architecture: (1) **Configuration Layer**: define immutable config classes (e.g., `SpectrumConfig`, `BasePlotConfig`) that validate and store user-supplied parameters (backend, plot kind, axis names, data columns). (2) **Core Base Layer**: create abstract base classes (`BasePlot`, `BaseMSPlot`) that accept config objects and define plot-agnostic logic (data validation, axis mapping). (3) **Orchestrator**: route the backend parameter (e.g., `backend='ms_bokeh'`) to the appropriate Extension Layer and instantiate the matching plot class. (4) **Extension Layer**: implement backend-specific classes via multiple inheritance—each combines a core base class with a backend-specific mixin (e.g., `BOKEHSpectrumPlot` inherits from both `SpectrumPlot` and `BOKEHPlot`), deferring rendering to the mixin. Expose the entry point as a Pandas extension method (`.plot()`), passing `backend`, `kind`, and data column names as parameters. This design isolates backend code, reuses configuration and validation logic, and ensures consistent behavior across libraries.

## Related tools

- **pandas** (DataFrame data structure and extension mechanism for exposing .plot() method)
- **matplotlib** (Static plotting backend producing rendered figures)
- **Bokeh** (Interactive plotting backend with JavaScript rendering)
- **Plotly** (Interactive plotting backend supporting 2D and 3D visualizations)
- **pyOpenMS-Viz** (Reference implementation of the architecture for mass spectrometry visualization) — https://github.com/OpenMS/pyopenms_viz

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum", backend="ms_bokeh")
```

## Evaluation signals

- User can invoke `.plot(backend='ms_bokeh', kind='spectrum')` on a DataFrame and receive a BOKEHSpectrumPlot object without knowing internal class names or backend-specific code.
- Swapping `backend='ms_matplotlib'` in the same call produces a MATPLOTLIBSpectrumPlot with identical configuration validation and data handling, proving configuration reuse across backends.
- Configuration objects validate parameters (e.g., axis column names exist in DataFrame) before any backend class is instantiated; invalid configs raise errors consistently regardless of backend.
- Each Extension Layer class inherits from exactly one core base class and one backend mixin, confirming the multiple-inheritance pattern and absence of code duplication in rendering logic.
- All supported plot types (spectrum, chromatogram, peakmap) render correctly on all three backends (Matplotlib, Bokeh, Plotly) as shown in the supported plots table.

## Limitations

- 3D plotting is only supported on Matplotlib and Plotly; Bokeh does not provide 3D primitives, so 3D peak maps cannot be rendered in that backend.
- Performance and visual fidelity vary across backends; Matplotlib is optimized for static publication, while Bokeh and Plotly prioritize interactivity. Switching backends may require tuning render parameters (e.g., marker sizes, hover tooltips).
- Custom backend-specific features (e.g., Plotly's 3D rotation, Bokeh's server-side filtering) cannot be exposed through the unified interface without breaking abstraction; users who need these features may need to access backend objects directly.

## Evidence

- [other] The call enters the Configuration Classes Layer, which validates and stores plotting parameters in a configuration object (e.g., `SpectrumConfig` for spectrum plots) inheriting from `BasePlotConfig`.: "The call enters the Configuration Classes Layer, which validates and stores plotting parameters in a configuration object"
- [other] The selected Extension Layer's class inherits from both the core base class and a backend-specific mixin (e.g., `BOKEHPlot`), combining configuration validation and backend rendering logic.: "The selected Extension Layer's class inherits from both the core base class and a backend-specific mixin, combining configuration validation and backend rendering logic"
- [readme] pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data.: "pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames"
- [readme] It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation.: "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
