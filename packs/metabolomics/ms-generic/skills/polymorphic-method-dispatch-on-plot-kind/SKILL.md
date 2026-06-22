---
name: polymorphic-method-dispatch-on-plot-kind
description: Use when when building a plotting library that must support multiple visualization types (1D spectra, chromatograms, mobilograms, 2D peak maps) across heterogeneous rendering backends, and you want users to specify plot type via a single kind parameter rather than importing backend-specific classes.
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
  techniques:
  - mass-spectrometry
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

# polymorphic-method-dispatch-on-plot-kind

## Summary

A class hierarchy and dispatch mechanism that routes plot kind arguments (spectrum, chromatogram, mobilogram, peakmap) to concrete plot subclasses, each implementing backend-specific rendering for mass spectrometry data visualization. This enables consistent Pandas-style plotting API across matplotlib (static) and bokeh/plotly (interactive) backends.

## When to use

When building a plotting library that must support multiple visualization types (1D spectra, chromatograms, mobilograms, 2D peak maps) across heterogeneous rendering backends, and you want users to specify plot type via a single kind parameter rather than importing backend-specific classes directly. Specifically useful when integrating with Pandas DataFrame.plot() accessor pattern and mass spectrometry data requires MS-specific validation and axis semantics.

## When NOT to use

- When the user has already selected and imported a specific backend plotting class directly (e.g., instantiated BOKEHSpectrumPlot directly) — dispatch adds no value in this case.
- When input data does not have the required x, y (or x, y, z for peakmap) columns, or when columns are not mass spectrometry-specific — validation should fail before dispatch.
- When plot kind is not one of the four supported types (spectrum, chromatogram, mobilogram, peakmap) — kind dispatcher should raise ValueError rather than attempting polymorphic dispatch.

## Inputs

- Pandas DataFrame with mass spectrometry columns (m/z, intensity, retention time, mobility)
- kind parameter (string: 'spectrum', 'chromatogram', 'mobilogram', 'peakmap')
- backend parameter (string: 'matplotlib', 'bokeh', 'plotly')
- x, y, z column names (strings)
- configuration object (ChromatogramConfig, SpectrumConfig, PeakMapConfig, MobilogramConfig)

## Outputs

- Plot object (matplotlib Figure, bokeh Figure, or plotly Figure)
- Rendered visualization displayed in notebook or saved to file
- Backend-specific plot instance with generate() method called

## How to apply

Establish a two-tier abstract class hierarchy: (1) BasePlot with common configuration and initialization; (2) BaseMSPlot inheriting from BasePlot to add MS-specific validation for plot kinds and axis requirements. Implement concrete plot subclasses (ChromatogramPlot, SpectrumPlot, PeakMapPlot, MobilogramPlot) inheriting from BaseMSPlot, each with a generate() method accepting x, y, z axes and a kind-specific config object (ChromatogramConfig, SpectrumConfig, etc.). Create backend-specific abstract bases (BOKEHPlot, PLOTLYPlot, MATPLOTLIBPlot) and concrete implementations (BOKEHSpectrumPlot, PLOTLYSpectrumPlot) that override generate() to call backend-specific rendering. Implement a kind-dispatch mechanism in the Pandas plotting backend accessor that maps kind='spectrum'|'chromatogram'|'mobilogram'|'peakmap' to the appropriate concrete plot class constructor, with backend selection passed separately. The dispatcher should validate that required axes (x, y for 1D plots; x, y, z for peakmap 2D) are present before instantiation.

## Related tools

- **Pandas** (DataFrame accessor integration point for kind dispatch and column selection)
- **matplotlib** (Static rendering backend; concrete MATPLOTLIBPlot subclasses call matplotlib rendering methods)
- **bokeh** (Interactive rendering backend; concrete BOKEHPlot subclasses call bokeh rendering methods)
- **plotly** (Interactive rendering backend; concrete PLOTLYPlot subclasses call plotly rendering methods)
- **pyOpenMS-viz** (Reference implementation of polymorphic dispatch on kind argument across backends) — https://github.com/OpenMS/pyopenms_viz

## Examples

```
ms_data.plot(x='m/z', y='intensity', kind='spectrum', backend='bokeh')
```

## Evaluation signals

- Verify that calling df.plot(x='m/z', y='intensity', kind='spectrum', backend='bokeh') returns a bokeh Figure (not matplotlib), confirming backend dispatch worked.
- Verify that calling df.plot(..., kind='peakmap') with only x and y columns (no z) raises ValueError with clear MS-specific validation message before instantiation.
- Verify that identical kind and column arguments produce visually equivalent plots across backends (matplotlib, bokeh, plotly) by comparing axis ranges, title, and data point counts.
- Verify that the appropriate concrete subclass (ChromatogramPlot, SpectrumPlot, etc.) is instantiated by inspecting type(plot_obj).__name__ or using isinstance() checks.
- Verify that configuration objects are passed to and respected by the chosen backend class (e.g., SpectrumConfig.mz_range constrains x-axis in all three backends).

## Limitations

- PeakMap 3D visualization is only supported on matplotlib and plotly; bokeh does not support 3D rendering, so kind='peakmap' with plot3d=True will raise NotImplementedError for bokeh backend.
- Column selection is versatile but requires exact string matching; if user specifies x='m/z_ppm' but DataFrame column is 'm/z', dispatch will fail silently or raise KeyError.
- Dispatch mechanism requires backend parameter to be passed explicitly or inferred from environment; if neither is available, the dispatcher has no deterministic way to select a backend.
- MS-specific validation (e.g., m/z ranges, intensity positivity) is enforced at BaseMSPlot level, so non-MS data may pass dispatch but fail at render time with cryptic backend-specific errors.

## Evidence

- [other] Define BaseMSPlot as an intermediate abstract class inheriting from BasePlot to add mass-spectrometry-specific methods and validation for chromatogram, mobilogram, spectrum, and peakmap plot kinds.: "Define BaseMSPlot as an intermediate abstract class inheriting from BasePlot to add mass-spectrometry-specific methods and validation for chromatogram, mobilogram, spectrum, and peakmap plot kinds."
- [other] Implement a kind-dispatch mechanism in the pandas plotting backend accessor that routes kind='spectrum', 'chromatogram', 'mobilogram', 'peakmap' to the appropriate concrete plot class constructor based on backend selection.: "Implement a kind-dispatch mechanism in the pandas plotting backend accessor that routes kind='spectrum', 'chromatogram', 'mobilogram', 'peakmap' to the appropriate concrete plot class constructor"
- [other] Implement backend-specific plot classes (BOKEHPlot, PLOTLYPlot, MATPLOTLIBPlot as abstract bases; BOKEHLinePlot, BOKEHSpectrumPlot, etc. as concrete implementations) that override generate() to call backend-specific rendering methods.: "Implement backend-specific plot classes (BOKEHPlot, PLOTLYPlot, MATPLOTLIBPlot as abstract bases; BOKEHLinePlot, BOKEHSpectrumPlot, etc. as concrete implementations) that override generate() to call"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Flexible plotting API that interfaces directly with Pandas DataFrames: "Flexible plotting API that interfaces directly with Pandas DataFrames"
- [readme] Consistent API across different plotting backends for easy switching between static and interactive plots: "Consistent API across different plotting backends for easy switching between static and interactive plots"
