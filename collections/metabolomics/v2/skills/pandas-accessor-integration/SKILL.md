---
name: pandas-accessor-integration
description: Use when you have mass-spectrometry data in a Pandas DataFrame and need
  to expose plot kinds (spectrum, chromatogram, mobilogram, peakmap) as a `.plot(kind='...
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# pandas-accessor-integration

## Summary

Integrate a custom visualization backend into Pandas DataFrames via the accessor pattern, enabling domain-specific plot kinds (spectrum, chromatogram, mobilogram, peakmap) to be called directly on DataFrame objects with a consistent API across multiple plotting backends (matplotlib, bokeh, plotly).

## When to use

You have mass-spectrometry data in a Pandas DataFrame and need to expose plot kinds (spectrum, chromatogram, mobilogram, peakmap) as a `.plot(kind='...')` interface that routes to backend-specific rendering (matplotlib for static, bokeh or plotly for interactive) without requiring users to import backend-specific classes directly.

## When NOT to use

- You are visualizing non-mass-spectrometry data; use standard pandas.plotting instead.
- You need custom plot kinds not in the supported set (spectrum, chromatogram, mobilogram, peakmap); extend the base classes first.
- Your data is already in a format other than Pandas DataFrame; convert to DataFrame first before using the accessor.

## Inputs

- pandas.DataFrame with mass-spectrometry columns (m/z, intensity, retention time, mobility, etc.)
- kind parameter (string: 'spectrum', 'chromatogram', 'mobilogram', 'peakmap')
- backend parameter (string: 'matplotlib', 'bokeh', or 'plotly')
- x, y, z column names (strings)
- optional configuration object (SpectrumConfig, ChromatogramConfig, MobilogramConfig, PeakMapConfig)

## Outputs

- plot object (matplotlib Figure, bokeh Figure, or plotly Figure)
- interactive or static visualization rendered to display or file

## How to apply

Register a custom pandas accessor (e.g., `@pd.api.extensions.register_dataframe_accessor('plot')`) that intercepts the `.plot(kind=...)` call. Inside the accessor's `__call__` or `plot()` method, implement a kind-dispatch mechanism that maps the `kind` argument ('spectrum', 'chromatogram', 'mobilogram', 'peakmap') to the appropriate concrete plot subclass (SpectrumPlot, ChromatogramPlot, MobilogramPlot, PeakMapPlot). Determine the backend from a user-supplied or default parameter (backend='matplotlib'|'bokeh'|'plotly'), then instantiate the corresponding backend-specific subclass (e.g., MATPLOTLIBSpectrumPlot, BOKEHSpectrumPlot) with x, y, and optional z column names and a configuration object (SpectrumConfig, ChromatogramConfig, etc.). Call the backend-specific `generate()` method to produce and return the plot object. This pattern allows users to write `df.plot(x='m/z', y='intensity', kind='spectrum', backend='bokeh')` without knowing the underlying class hierarchy.

## Related tools

- **Pandas** (Provides the DataFrame object and accessor registration pattern; used for data manipulation and as the entry point for plot dispatch) — https://pandas.pydata.org
- **matplotlib** (Backend for static plot rendering; instantiated via MATPLOTLIBPlot and concrete subclasses (MATPLOTLIBSpectrumPlot, MATPLOTLIBChromatogramPlot, etc.))
- **bokeh** (Backend for interactive plot rendering; instantiated via BOKEHPlot and concrete subclasses (BOKEHSpectrumPlot, BOKEHChromatogramPlot, etc.))
- **plotly** (Backend for interactive plot rendering; instantiated via PLOTLYPlot and concrete subclasses (PLOTLYSpectrumPlot, PLOTLYChromatogramPlot, etc.))
- **pyOpenMS-viz** (Implements the accessor integration, class hierarchy, and kind-dispatch mechanism for mass-spectrometry visualization) — https://github.com/OpenMS/pyopenms_viz

## Examples

```
ms_data.plot(x="m/z", y="intensity", kind="spectrum", backend="bokeh")
```

## Evaluation signals

- Verify that `df.plot(kind='spectrum')` returns a plot object of the expected backend type without raising AttributeError or NotImplementedError.
- Confirm that the same DataFrame and parameters produce consistent output when backend is switched from 'matplotlib' to 'bokeh' or 'plotly' (same data mapped to x, y, z axes).
- Check that invalid `kind` values raise a clear ValueError identifying supported plot kinds.
- Validate that configuration objects (SpectrumConfig, ChromatogramConfig, etc.) are passed through to the backend-specific `generate()` method and reflected in plot styling (axes labels, colors, etc.).
- Ensure that the accessor does not conflict with pandas' native `.plot()` method by testing backward compatibility on standard plot kinds (line, scatter, bar).

## Limitations

- The accessor pattern requires explicit registration and may conflict with other custom accessors on the same DataFrame class.
- All plot kinds must be predefined in the concrete subclass hierarchy; dynamic or ad-hoc plot kinds cannot be added via the accessor alone.
- Performance may degrade for very large DataFrames if data is not pre-filtered or aggregated before passing to the accessor.
- The accessor provides a unified API but backend-specific features (e.g., 3D plots in plotly but not bokeh for peakmap) may still require conditional logic or fallback behavior.

## Evidence

- [other] Implement a kind-dispatch mechanism in the pandas plotting backend accessor that routes kind='spectrum', 'chromatogram', 'mobilogram', 'peakmap' to the appropriate concrete plot class constructor based on backend selection.: "Implement a kind-dispatch mechanism in the pandas plotting backend accessor that routes kind='spectrum', 'chromatogram', 'mobilogram', 'peakmap' to the appropriate concrete plot class constructor"
- [readme] pyOpenMS-Viz provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data.: "provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry data"
- [readme] Flexible plotting API that interfaces directly with Pandas DataFrames; Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Flexible plotting API that interfaces directly with Pandas DataFrames; Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Consistent API across different plotting backends for easy switching between static and interactive plots: "Consistent API across different plotting backends for easy switching between static and interactive plots"
- [other] Plot directly from a pandas dataframe object: "Plot directly from a pandas dataframe object"
