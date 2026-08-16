---
name: mass-spectrometry-plot-taxonomy-implementation
description: Use when you are building a visualization library that must support multiple
  plot kinds (chromatogram, spectrum, mobilogram, peakmap) across multiple rendering
  backends (matplotlib, bokeh, plotly) and want to avoid code duplication.
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
  - Pandas
  - matplotlib
  - bokeh
  - OpenMS
  techniques:
  - ion-mobility-MS
  license_tier: open
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

# mass-spectrometry-plot-taxonomy-implementation

## Summary

Design and implement a polymorphic class hierarchy that routes mass spectrometry visualization requests (spectrum, chromatogram, mobilogram, peakmap) through abstract base classes to backend-specific concrete plot implementations. This skill enables a single Pandas plotting interface to delegate to matplotlib (static), bokeh, or plotly (interactive) renderers while maintaining consistent method signatures and validation logic across plot kinds.

## When to use

You are building a visualization library that must support multiple plot kinds (chromatogram, spectrum, mobilogram, peakmap) across multiple rendering backends (matplotlib, bokeh, plotly) and want to avoid code duplication. Specifically: when you have MS data in a Pandas DataFrame and need to route `.plot(kind='spectrum')` or `.plot(kind='chromatogram')` calls to the appropriate plot class without hard-coding backend selection in user code.

## When NOT to use

- You are plotting non-MS data (e.g., generic XY scatter plots) — use the generic `LinePlot` or `ScatterPlot` classes instead, which skip MS-specific validation.
- Your input is already a rendered plot object or a plot file (PNG, SVG, HTML) — the hierarchy expects raw MS data in tabular form.
- You need real-time streaming or live updating of plots — the current architecture assumes static DataFrame input, not streaming data sources.

## Inputs

- Pandas DataFrame with mass spectrometry data (m/z, intensity, retention time, ion mobility, or equivalent columns)
- kind parameter (string: 'spectrum', 'chromatogram', 'mobilogram', 'peakmap')
- backend parameter (string: 'matplotlib', 'bokeh', 'plotly')
- configuration object (SpectrumConfig, ChromatogramConfig, MobilogramConfig, or PeakMapConfig with axis names, labels, colors, etc.)

## Outputs

- Plot object (backend-specific: matplotlib Figure/Axes, bokeh Figure, or plotly Figure)
- Rendered visualization (static or interactive depending on backend)

## How to apply

Establish a three-tier inheritance hierarchy: (1) Define `BasePlot` as an abstract base with common configuration and initialization shared by all plot types; (2) Define `BaseMSPlot` as an intermediate abstract class inheriting from `BasePlot` to add mass-spectrometry-specific validation (axis counts, required columns) and factory logic for the four MS plot kinds; (3) Implement backend-agnostic concrete classes (`ChromatogramPlot`, `SpectrumPlot`, `MobilogramPlot`, `PeakMapPlot`) that inherit from `BaseMSPlot` and define a `generate()` method accepting x, y, z axes and a configuration object (e.g., `SpectrumConfig`); (4) Create backend-specific abstract classes (e.g., `MATLOTLIBPlot`) and their concrete subclasses (e.g., `MATLOTLIBSpectrumPlot`) that override `generate()` to call backend-specific rendering methods; (5) Implement a `kind`-dispatch mechanism in the Pandas accessor that routes `kind='spectrum'` to `SpectrumPlot`, then instantiates the appropriate backend subclass based on the user's backend selection. This pattern ensures validation, configuration, and axis mapping are defined once at the plot-kind level, while rendering logic is cleanly separated by backend.

## Related tools

- **pyOpenMS-viz** (Primary implementation library that provides the Pandas plotting accessor and concrete plot classes for spectrum, chromatogram, mobilogram, and peakmap visualization) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (DataFrame input format and plotting API extension point (accessor registration))
- **matplotlib** (Static rendering backend; concrete subclasses (MATLOTLIBSpectrumPlot, etc.) override generate() to produce Figure/Axes objects)
- **bokeh** (Interactive rendering backend; concrete subclasses (BOKEHSpectrumPlot, etc.) produce bokeh Figure objects)
- **plotly** (Interactive rendering backend; concrete subclasses (PLOTLYSpectrumPlot, etc.) produce plotly Figure objects)
- **OpenMS** (Source of MS data processing and algorithm library integrated with pyOpenMS bindings)

## Examples

```
import pandas as pd; from pyopenms_viz import SpectrumConfig; df = pd.DataFrame({'m/z': [100, 101, 102], 'intensity': [10, 50, 15]}); config = SpectrumConfig(x_label='m/z', y_label='Intensity'); df.plot(x='m/z', y='intensity', kind='spectrum', backend='matplotlib', config=config)
```

## Evaluation signals

- Verify that each plot kind (spectrum, chromatogram, mobilogram, peakmap) instantiates the correct concrete plot class (SpectrumPlot, ChromatogramPlot, etc.) without user awareness of backend choice.
- Confirm that `BaseMSPlot` validation rejects invalid axis counts (e.g., peakmap without z-axis) before backend rendering begins.
- Check that the same Pandas DataFrame and `.plot(kind='spectrum', backend='matplotlib')` vs. `.plot(kind='spectrum', backend='plotly')` calls produce equivalent data rendering (same x, y values) with different visual rendering (static vs. interactive).
- Ensure that configuration objects (SpectrumConfig, etc.) are validated and applied consistently across backends — e.g., axis labels, color maps, and data ranges are identical.
- Verify that the `kind`-dispatch mechanism in the pandas accessor correctly routes unknown `kind` values to a fallback or raises an informative error message.

## Limitations

- The hierarchy assumes x, y, z axes align with DataFrame columns; if column names or semantics vary significantly between datasets, users must provide mapping via configuration objects, which adds verbosity.
- 3D PeakMap plots are supported only in matplotlib and plotly; bokeh lacks 3D rendering, so users selecting `backend='bokeh'` with `plot3d=True` will fail or fall back to 2D rendering.
- The kind-dispatch mechanism is tied to Pandas' plotting API; any DataFrame not adhering to the expected column structure (e.g., missing m/z or intensity columns) will fail validation at the `BaseMSPlot` level with a generic error.
- The implementation does not handle asynchronous or streaming data; all plots expect a complete Pandas DataFrame in memory, limiting scalability for very large MS datasets.

## Evidence

- [other] Define BasePlot as an abstract base class with common configuration and initialization logic inherited by all plot types.: "Define BasePlot as an abstract base class with common configuration and initialization logic inherited by all plot types."
- [other] BaseMSPlot as an intermediate abstract class inheriting from BasePlot to add mass-spectrometry-specific methods and validation for chromatogram, mobilogram, spectrum, and peakmap plot kinds.: "Define BaseMSPlot as an intermediate abstract class inheriting from BasePlot to add mass-spectrometry-specific methods and validation for chromatogram, mobilogram, spectrum, and peakmap plot kinds."
- [other] Concrete MS plot subclasses inheriting from BaseMSPlot, each with generate() method accepting x, y, z axes and configuration objects.: "Implement concrete MS plot subclasses (ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot) inheriting from BaseMSPlot, each with generate() method accepting x, y, z axes and configuration"
- [other] Backend-specific plot classes that override generate() to call backend-specific rendering methods.: "Implement backend-specific plot classes (BOKEHPlot, PLOTLYPlot, MATPLOTLIBPlot as abstract bases; BOKEHLinePlot, BOKEHSpectrumPlot, etc. as concrete implementations) that override generate() to call"
- [other] Kind-dispatch mechanism in the pandas plotting backend accessor routes plot kinds to appropriate concrete plot class.: "Implement a kind-dispatch mechanism in the pandas plotting backend accessor that routes kind='spectrum', 'chromatogram', 'mobilogram', 'peakmap' to the appropriate concrete plot class constructor"
- [intro] pyOpenMS-Viz integrates seamlessly with various plotting library backends and leverages Pandas for data manipulation.: "integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation"
- [readme] Support for multiple plotting backends including matplotlib, bokeh, and plotly.: "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Visualization of various mass spectrometry data types including chromatograms, spectra, and peak maps.: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
