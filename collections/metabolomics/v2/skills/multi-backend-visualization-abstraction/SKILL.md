---
name: multi-backend-visualization-abstraction
description: Use when when building a mass spectrometry visualization library that must support multiple plotting backends (matplotlib for static output, bokeh and plotly for interactive exploration) with a uniform DataFrame-based API, and where different plot kinds (spectrum, chromatogram, mobilogram, peakmap).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - plotly
  - pyOpenMS-viz
  - pandas
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

# multi-backend-visualization-abstraction

## Summary

Design and implement an abstract class hierarchy that decouples mass spectrometry visualization logic from rendering backend (matplotlib, bokeh, plotly), enabling consistent plotting APIs and kind-based dispatch across static and interactive backends. This skill bridges domain-specific plot semantics (spectrum, chromatogram, mobilogram, peakmap) with backend-specific rendering implementations.

## When to use

When building a mass spectrometry visualization library that must support multiple plotting backends (matplotlib for static output, bokeh and plotly for interactive exploration) with a uniform DataFrame-based API, and where different plot kinds (spectrum, chromatogram, mobilogram, peakmap) require both common configuration logic and backend-specific rendering. Essential when users should be able to switch backends without rewriting visualization code.

## When NOT to use

- Input data is not structured as a pandas DataFrame with named columns
- Only one backend (e.g., matplotlib-only) is required; simpler patterns suffice
- Plot kind is not one of the pre-defined MS kinds (spectrum, chromatogram, mobilogram, peakmap) and no subclass customization is feasible

## Inputs

- pandas.DataFrame with mass spectrometry data (m/z, intensity, retention time, ion mobility columns)
- Plot kind string (e.g., 'spectrum', 'chromatogram', 'mobilogram', 'peakmap')
- Backend identifier (e.g., 'matplotlib', 'bokeh', 'plotly')
- Configuration object (ChromatogramConfig, SpectrumConfig, MobilogramConfig, PeakMapConfig)
- Axis column names (x, y, z for peakmap)

## Outputs

- Backend-specific plot object (matplotlib Figure, bokeh Figure, plotly Figure)
- Rendered visualization (static image or interactive HTML widget)
- Plot with consistent styling, labels, and interactivity across backends

## How to apply

Define a multi-level abstract class hierarchy: (1) BasePlot as the root abstract class encapsulating common configuration, axis labeling, and initialization logic for all plot types; (2) BaseMSPlot as an intermediate abstract class inheriting from BasePlot to add mass-spectrometry-specific validation and methods for handling chromatogram, mobilogram, spectrum, and peakmap kinds; (3) Concrete plot subclasses (LinePlot, VLinePlot, ScatterPlot) inheriting from BasePlot, and MS-specific subclasses (ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot) inheriting from BaseMSPlot, each implementing a generate() method; (4) Backend-specific abstract classes (BOKEHPlot, PLOTLYPlot, MATPLOTLIBPlot) and concrete implementations (BOKEHLinePlot, BOKEHSpectrumPlot, etc.) that override generate() with backend-specific rendering calls; (5) Implement a kind-dispatch mechanism (typically in a pandas plotting backend accessor) that routes kind='spectrum'/'chromatogram'/'mobilogram'/'peakmap' to the correct concrete plot constructor based on selected backend. This pattern ensures new backends and plot types can be added by subclassing, not by modifying existing code.

## Related tools

- **pyOpenMS-viz** (Implements the multi-backend abstraction pattern for pandas DataFrame plotting of mass spectrometry data; provides the BasePlot/BaseMSPlot hierarchy and kind-dispatch mechanism) — https://github.com/OpenMS/pyopenms_viz
- **pandas** (DataFrame accessor extension point for registering the plot() method and kind-dispatch logic)
- **matplotlib** (Static plotting backend; receives rendering calls from MATPLOTLIBPlot concrete classes)
- **bokeh** (Interactive plotting backend; receives rendering calls from BOKEHPlot concrete classes)
- **plotly** (Interactive plotting backend; receives rendering calls from PLOTLYPlot concrete classes)

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum", backend="bokeh")
ms_data.plot(x="rt", y="intensity", kind="chromatogram", backend="matplotlib")
```

## Evaluation signals

- Verify that a DataFrame.plot(kind='spectrum', backend='matplotlib') and DataFrame.plot(kind='spectrum', backend='bokeh') produce semantically identical visualizations (same axes, labels, data representation) with only rendering differences
- Confirm that adding a new plot kind (e.g., 'isotope_pattern') requires only subclassing BaseMSPlot and implementing generate() once, with no changes to backend routing code
- Check that adding a new backend requires only subclassing the appropriate backend-specific abstract class (e.g., PLOTLYPlot) and implementing generate() for each plot kind, with no modification to BasePlot or dispatch logic
- Validate that all configuration objects (ChromatogramConfig, SpectrumConfig, etc.) inherit common properties from a base Config class and that configuration is applied consistently across backends
- Ensure that the kind-dispatch mechanism correctly routes kind='chromatogram'/'mobilogram'/'spectrum'/'peakmap' to the appropriate concrete subclass without manual if-else chains in the accessor

## Limitations

- The abstraction is most effective when plot kinds have well-defined semantics; adhoc or domain-specific plot types may require deeper subclass hierarchies
- Performance and feature parity across backends may differ: matplotlib is static-only, bokeh and plotly offer interactivity but with different capabilities (e.g., 3D PeakMap supported in matplotlib and plotly but not bokeh)
- Configuration objects must remain serializable and hashable across backends if caching or incremental updates are desired
- Switching backends at runtime requires re-instantiating the entire plot object; there is no in-place backend swap

## Evidence

- [other] Define BasePlot as an abstract base class with common configuration and initialization logic inherited by all plot types: "Define BasePlot as an abstract base class with common configuration and initialization logic inherited by all plot types."
- [other] BaseMSPlot as intermediate abstract class for mass-spectrometry-specific methods and validation: "Define BaseMSPlot as an intermediate abstract class inheriting from BasePlot to add mass-spectrometry-specific methods and validation for chromatogram, mobilogram, spectrum, and peakmap plot kinds."
- [other] Backend-specific abstract and concrete implementations with generate() method override: "Implement backend-specific plot classes (BOKEHPlot, PLOTLYPlot, MATPLOTLIBPlot as abstract bases; BOKEHLinePlot, BOKEHSpectrumPlot, etc. as concrete implementations) that override generate() to call"
- [other] Kind-dispatch mechanism in pandas plotting backend accessor: "Implement a kind-dispatch mechanism in the pandas plotting backend accessor that routes kind='spectrum', 'chromatogram', 'mobilogram', 'peakmap' to the appropriate concrete plot class constructor"
- [readme] Multiple backends supported including matplotlib, bokeh, and plotly: "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Integration with pandas DataFrames for data representation: "Flexible plotting API that interfaces directly with Pandas DataFrames"
