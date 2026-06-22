---
name: abstract-base-class-implementation
description: Use when when building a visualization library that must support multiple plotting backends (e.g., matplotlib, bokeh, plotly) and multiple data types (e.g., chromatograms, spectra, peak maps) without duplicating core logic or configuration handling across backend–plot-type combinations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - plotly
  - pyOpenMS-viz
  - Pandas
  - matplotlib
  - bokeh
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- ms_data.plot(x="m/z", y="intensity", kind="spectrum")
- conda create --name=pyopenms-viz python=3.12
- Multiple backends supported including matplotlib, bokeh, and plotly
- Rendering is typically slower than the BOKEH backend
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from pandas dataframes
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyopenmsviz_cq
    doi: 10.1021/acs.jproteome.4c00873
    title: pyopenmsviz
  dedup_kept_from: coll_pyopenmsviz_cq
schema_version: 0.2.0
---

# abstract-base-class-implementation

## Summary

Design and implement a multi-level abstract base class (ABC) hierarchy that separates domain-agnostic plotting logic from domain-specific (mass-spectrometry) concerns, and that delegates to backend-specific concrete implementations via a kind-dispatch mechanism. This pattern enables consistent APIs across multiple plotting backends while avoiding code duplication and supporting extension.

## When to use

When building a visualization library that must support multiple plotting backends (e.g., matplotlib, bokeh, plotly) and multiple data types (e.g., chromatograms, spectra, peak maps) without duplicating core logic or configuration handling across backend–plot-type combinations. Use this skill when you need to route a single user-facing API call (e.g., `kind='spectrum'`) to the appropriate concrete plot class based on both plot kind and backend selection.

## When NOT to use

- Input data is not tabular or does not fit the Pandas DataFrame schema expected by the library.
- You need to support plot kinds not explicitly recognized by the domain-specific ABC (e.g., a novel MS data type not covered by chromatogram, mobilogram, spectrum, or peakmap); extend the ABC hierarchy rather than bypass it.
- Your library has only one plotting backend; the abstraction overhead outweighs the benefit of code reuse.

## Inputs

- Pandas DataFrame with mass-spectrometry data (columns for x-axis, y-axis, optional z-axis)
- kind parameter specifying plot type (string: 'spectrum', 'chromatogram', 'mobilogram', 'peakmap')
- backend parameter or default specifying which plotting library to use (string: 'matplotlib', 'bokeh', 'plotly')
- Configuration object (e.g., SpectrumConfig, ChromatogramConfig) with plot-specific parameters

## Outputs

- Plot object (backend-specific: matplotlib Figure/Axes, bokeh Figure, plotly Figure)
- Rendered visualization of mass-spectrometry data suitable for static (matplotlib) or interactive (bokeh, plotly) display

## How to apply

Establish a hierarchy: (1) define a domain-agnostic `BasePlot` ABC with shared configuration, initialization, and the abstract `generate()` method; (2) create an intermediate domain-specific ABC (e.g., `BaseMSPlot` inheriting from `BasePlot`) that adds mass-spectrometry-specific validation and methods for recognized plot kinds (chromatogram, mobilogram, spectrum, peakmap); (3) implement concrete plot subclasses (e.g., `ChromatogramPlot`, `SpectrumPlot`) inheriting from the domain-specific ABC, each overriding `generate()` with logic for axis labeling and data validation; (4) implement backend-specific abstract bases (e.g., `BOKEHPlot`, `PLOTLYPlot`) that override `generate()` to call backend-specific rendering; (5) implement backend–plot-type pairs as concrete classes (e.g., `BOKEHSpectrumPlot`, `PLOTLYSpectrumPlot`) inheriting from both the plot-kind class and the backend abstract class; (6) implement a kind-dispatch mechanism in a pandas plotting backend accessor that inspects the `kind` parameter and backend name, instantiates the appropriate concrete class, and calls its `generate()` method. This approach localizes backend-specific logic, centralizes MS-specific validation, and allows adding new backends or plot kinds with minimal changes to existing code.

## Related tools

- **Pandas** (Provides DataFrame structure for storing and manipulating mass-spectrometry tabular data; supports custom accessor registration for the plot() method.)
- **matplotlib** (Backend for static 2D and 3D plot rendering; concrete implementations inherit from BOKEHPlot/PLOTLIBPlot abstract classes and override generate() to call matplotlib-specific rendering.)
- **bokeh** (Backend for interactive 2D plot rendering; concrete implementations inherit from BOKEHPlot abstract class and call bokeh-specific Figure and glyph methods.)
- **plotly** (Backend for interactive 2D and 3D plot rendering; concrete implementations inherit from PLOTLYPlot abstract class and call plotly-specific go.Figure methods.)
- **pyOpenMS-viz** (Reference implementation library demonstrating the full ABC hierarchy, backend dispatch, and pandas accessor registration.) — https://github.com/OpenMS/pyopenms_viz

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum", backend="bokeh")
```

## Evaluation signals

- Each concrete plot subclass successfully overrides generate() without raising NotImplementedError, and produces output matching its backend (matplotlib Figure, bokeh Figure, or plotly Figure object).
- Kind-dispatch mechanism routes 'spectrum' + 'matplotlib' to BOKEHSpectrumPlot (or equivalent), 'chromatogram' + 'bokeh' to BOKEHChromatogramPlot, etc., with no manual if–elif chains in user-facing code.
- BaseMSPlot validation catches unsupported plot kinds (e.g., 'unknown_plot') before instantiation, raising a clear error message.
- Adding a new plot kind (e.g., 'ion_mobility_plot') requires changes only to the domain-specific ABC and concrete subclasses; backend-specific code remains unchanged.
- Pandas accessor registration allows invocation via df.plot(x='m/z', y='intensity', kind='spectrum', backend='bokeh') without explicit class instantiation by the user.

## Limitations

- Backend-specific rendering differences (e.g., 3D support available in matplotlib and plotly but not bokeh) require conditional logic in the kind-dispatch mechanism or separate concrete classes per backend, increasing maintenance burden.
- Multiple inheritance (plot-kind class + backend abstract class) can lead to method resolution order (MRO) ambiguities if not carefully managed; Python's C3 linearization helps but requires discipline.
- Adding a new backend requires implementing a new abstract base class and concrete implementations for each supported plot kind, which is labor-intensive for libraries with many plot types.
- Configuration objects (SpectrumConfig, etc.) must be kept in sync with backend-specific parameters; inconsistencies can lead to silent failures or unexpected plot output.

## Evidence

- [other] Define BasePlot as an abstract base class with common configuration and initialization logic: "Define BasePlot as an abstract base class with common configuration and initialization logic inherited by all plot types."
- [other] BaseMSPlot intermediate abstract class for mass-spectrometry-specific methods: "Define BaseMSPlot as an intermediate abstract class inheriting from BasePlot to add mass-spectrometry-specific methods and validation for chromatogram, mobilogram, spectrum, and peakmap plot kinds."
- [other] Backend-specific plot classes override generate() to call backend-specific rendering methods: "Implement backend-specific plot classes (BOKEHPlot, PLOTLYPlot, MATPLOTLIBPlot as abstract bases; BOKEHLinePlot, BOKEHSpectrumPlot, etc. as concrete implementations) that override generate() to call"
- [other] Kind-dispatch mechanism routes plot kind to appropriate concrete class based on backend: "Implement a kind-dispatch mechanism in the pandas plotting backend accessor that routes kind='spectrum', 'chromatogram', 'mobilogram', 'peakmap' to the appropriate concrete plot class constructor"
- [readme] pyOpenMS-Viz integrates with multiple plotting library backends: "integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation"
