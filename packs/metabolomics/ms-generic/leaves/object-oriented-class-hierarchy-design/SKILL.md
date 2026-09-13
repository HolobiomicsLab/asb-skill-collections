---
name: object-oriented-class-hierarchy-design
description: Use when when you need to create a plotting or visualization framework
  that must support multiple plot kinds (spectrum, chromatogram, mobilogram, peakmap)
  each backed by multiple rendering engines (matplotlib, bokeh, plotly), and you want
  to avoid combinatorial explosion of concrete classes while.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
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
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- ms_data.plot(x="m/z", y="intensity", kind="spectrum")
- conda create --name=pyopenms-viz python=3.12
- Multiple backends supported including matplotlib, bokeh, and plotly
- Rendering is typically slower than the BOKEH backend
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from
  pandas dataframes
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

# object-oriented-class-hierarchy-design

## Summary

Design and implement a multi-level abstract class hierarchy with inheritance dispatch to enable concrete plot components to inherit common functionality while routing behavior based on plot kind and backend selection. This skill is essential when building extensible visualization frameworks that must support multiple data types (1D spectra, chromatograms, 2D peak maps) across multiple plotting backends (matplotlib, bokeh, plotly) without code duplication.

## When to use

When you need to create a plotting or visualization framework that must support multiple plot kinds (spectrum, chromatogram, mobilogram, peakmap) each backed by multiple rendering engines (matplotlib, bokeh, plotly), and you want to avoid combinatorial explosion of concrete classes while maintaining a clear separation between domain logic (mass spectrometry–specific validation and configuration) and backend-specific rendering.

## When NOT to use

- Input data does not require multiple plot kinds or backend support — a single concrete class may suffice
- Mass spectrometry–specific validation and configuration are not needed; use generic plotting libraries directly
- Plot kinds and backends are tightly coupled with unique rendering logic for each combination — the overhead of the hierarchy may not justify the added complexity

## Inputs

- Pandas DataFrame with mass spectrometry data (m/z, intensity, retention time, or mobility columns)
- plot kind argument (string: 'spectrum', 'chromatogram', 'mobilogram', 'peakmap')
- backend argument (string: 'matplotlib', 'bokeh', 'plotly')
- x, y, z axis column names (strings)
- plot configuration object (e.g., SpectrumConfig, ChromatogramConfig, PeakMapConfig)

## Outputs

- Concrete plot instance (e.g., BOKEHSpectrumPlot, PLOTLYChromatogramPlot)
- Rendered plot object ready for display (matplotlib Figure, bokeh Figure, plotly Figure)

## How to apply

Begin by defining an abstract `BasePlot` class that encapsulates common initialization, configuration, and plotting interface logic shared across all plot types. Create an intermediate abstract class `BaseMSPlot` inheriting from `BasePlot` that adds mass-spectrometry-specific methods, validation, and configuration objects (e.g., ChromatogramConfig, SpectrumConfig) for the four MS plot kinds. Implement concrete plot subclasses (ChromatogramPlot, SpectrumPlot, PeakMapPlot) inheriting from `BaseMSPlot`, each with a `generate()` method accepting x, y, z axes and their respective configuration objects. At the backend layer, create abstract backend base classes (BOKEHPlot, PLOTLYPlot, MATPLOTLIBPlot) inheriting from the appropriate concrete plot class, then implement backend-specific concrete subclasses (e.g., BOKEHSpectrumPlot, PLOTLYSpectrumPlot) that override `generate()` to call backend-specific rendering methods. Finally, implement a kind-dispatch mechanism in the pandas plotting backend accessor (e.g., `.plot(kind='spectrum', backend='bokeh')`) that routes the kind and backend arguments to the correct concrete plot class constructor. This separation ensures that adding a new plot kind or backend requires only extending the appropriate level of the hierarchy, not modifying existing code.

## Related tools

- **pyOpenMS-viz** (provides the concrete implementation of class hierarchy for MS plot dispatch with support for spectrum, chromatogram, mobilogram, and peakmap kinds across matplotlib, bokeh, and plotly backends) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (provides DataFrame API and accessor mechanism (.plot()) that integrates the kind-dispatch routing into pandas workflow)
- **matplotlib** (backend-specific rendering engine for static plots)
- **bokeh** (backend-specific rendering engine for interactive plots)
- **plotly** (backend-specific rendering engine for interactive plots including 3D peakmap visualization)

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum", backend="bokeh")
```

## Evaluation signals

- Verify that all four MS plot kinds (spectrum, chromatogram, mobilogram, peakmap) can be instantiated and rendered through the same `.plot(kind=..., backend=...)` interface without conditional branches in user code
- Confirm that adding a new plot kind requires only creating one new concrete subclass inheriting from BaseMSPlot, not modifying backend classes
- Check that adding a new backend requires only creating backend-specific subclasses (e.g., BOKEHChromatogramPlot), not modifying BaseMSPlot or concrete plot classes
- Validate that MS-specific configuration (ChromatogramConfig, SpectrumConfig, etc.) is enforced consistently across all backends through the BaseMSPlot layer
- Ensure that the kind-dispatch mechanism correctly routes `.plot(kind='spectrum', backend='bokeh')` to BOKEHSpectrumPlot and `.plot(kind='peakmap', backend='plotly')` to PLOTLYPeakMapPlot without explicit if-else chains in the accessor code

## Limitations

- The hierarchy adds complexity and abstraction layers that may incur small performance overhead for simple, single-backend use cases
- PeakMap 3D plots are supported only in matplotlib and plotly, not bokeh — the hierarchy does not automatically prevent invalid kind–backend combinations; validation must be implemented in the dispatcher
- Extension to non-MS plot kinds (e.g., generic LinePlot, ScatterPlot) requires a parallel hierarchy branch rather than integration within BaseMSPlot
- Configuration objects (ChromatogramConfig, SpectrumConfig, etc.) must be kept synchronized with backend rendering methods; missing or deprecated config fields may silently fail at render time

## Evidence

- [other] Define BasePlot as an abstract base class with common configuration and initialization logic: "Define BasePlot as an abstract base class with common configuration and initialization logic inherited by all plot types"
- [other] BaseMSPlot adds MS-specific methods and validation for chromatogram, mobilogram, spectrum, and peakmap plot kinds: "Define BaseMSPlot as an intermediate abstract class inheriting from BasePlot to add mass-spectrometry-specific methods and validation for chromatogram, mobilogram, spectrum, and peakmap plot kinds"
- [other] Backend-specific plot classes override generate() to call backend-specific rendering methods: "Implement backend-specific plot classes (BOKEHPlot, PLOTLYPlot, MATPLOTLIBPlot as abstract bases; BOKEHLinePlot, BOKEHSpectrumPlot, etc. as concrete implementations) that override generate() to call"
- [other] Kind-dispatch mechanism routes kind argument to appropriate concrete plot class constructor based on backend selection: "Implement a kind-dispatch mechanism in the pandas plotting backend accessor that routes kind='spectrum', 'chromatogram', 'mobilogram', 'peakmap' to the appropriate concrete plot class constructor"
- [intro] pyOpenMS-Viz integrates multiple plotting backends and leverages Pandas for data manipulation: "integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation"
- [readme] Flexible plotting API interfaces directly with Pandas DataFrames and supports multiple backends: "Flexible plotting API that interfaces directly with Pandas DataFrames. Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
