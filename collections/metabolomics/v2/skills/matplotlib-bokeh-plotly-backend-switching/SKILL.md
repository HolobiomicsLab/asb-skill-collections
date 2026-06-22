---
name: matplotlib-bokeh-plotly-backend-switching
description: Use when when you have mass spectrometry data (chromatograms, spectra, mobilograms, or peak maps) in a Pandas DataFrame and need to generate the same visualization in multiple formats—e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matplotlib
  - Bokeh
  - Plotly
  - AlphaTims
  - pyOpenMS-Viz
  - Pandas
  - pymzml
  - pyOpenMS
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)
- 'Extension: MATPLOTLIB'
- 'Extension: BOKEH'
- 'Extension: PLOTLY'
- '.d -- .. toctree:: :maxdepth: 1 alphatims'
- alphatims
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# matplotlib-bokeh-plotly-backend-switching

## Summary

Switch mass spectrometry visualization output between matplotlib (static), Bokeh (interactive), and Plotly (interactive) backends using a consistent pyOpenMS-Viz API, enabling users to choose between publication-ready static figures and interactive web-based exploration without rewriting plot code.

## When to use

When you have mass spectrometry data (chromatograms, spectra, mobilograms, or peak maps) in a Pandas DataFrame and need to generate the same visualization in multiple formats—e.g., static PNG/PDF for publication via matplotlib, or interactive HTML dashboards via Bokeh or Plotly for exploratory data analysis—or when you need to switch backends to accommodate audience or deployment constraints (e.g., static output for LaTeX documents vs. interactive output for Jupyter notebooks or web applications).

## When NOT to use

- If your input is not a Pandas DataFrame or lacks the required x, y (or x, y, z for peak maps) columns—use data preparation and reshaping steps first.
- If you need 3D visualization and are restricted to Bokeh backend, as Bokeh does not support plot_3d=True parameter.
- If your data is not mass spectrometry data (e.g., generic tabular data with no MS semantics), as the plot kinds (spectrum, chromatogram, mobilogram, peakmap) are MS-domain-specific.

## Inputs

- Pandas DataFrame with mass spectrometry data (columns: x, y for 1D plots; x, y, z for 2D peak maps)
- mzML files loaded via pymzml or pyOpenMS
- Bruker .d format files loaded via AlphaTims

## Outputs

- Static figure file (PNG, PDF, SVG) for matplotlib backend
- Interactive HTML figure file for Bokeh backend
- Interactive HTML figure file for Plotly backend

## How to apply

Load your MS data into a Pandas DataFrame with columns for x (m/z or retention time or ion mobility), y (intensity), and optionally z (intensity for 2D peak maps). Call the DataFrame's `.plot()` method with `kind` set to one of the four supported plot types (spectrum, chromatogram, mobilogram, or peakmap) and `backend` set to either ms_matplotlib, ms_bokeh, or ms_plotly. For multi-backend output, invoke the same `.plot()` call three times with different backend values—the API remains constant, so only the backend parameter changes. For peakmap plots, you may optionally set `add_marginals=True` or `plot_3d=True`; note that 3D rendering is supported by matplotlib and Plotly but not Bokeh. Verify output by checking that the generated figure file exists in the expected format (PNG/PDF for matplotlib, HTML for Bokeh/Plotly) and visually inspect that axis labels, title, and data rendering are correct.

## Related tools

- **pyOpenMS-Viz** (Core library providing the multi-backend plot API and plot kinds (SpectrumPlot, ChromatogramPlot, MobilogramPlot, PeakMapPlot)) — https://github.com/OpenMS/pyopenms_viz
- **Pandas** (DataFrame container and data manipulation for loading and structuring MS data with x, y, z columns)
- **matplotlib** (Static plotting backend (ms_matplotlib) for publication-ready figures)
- **Bokeh** (Interactive plotting backend (ms_bokeh) for web-based visualization)
- **Plotly** (Interactive plotting backend (ms_plotly) for web-based and 3D visualization)
- **pymzml** (Load mzML format MS data files into Pandas DataFrames)
- **pyOpenMS** (Load mzML format MS data files and provide MS algorithm support)
- **AlphaTims** (Load Bruker .d format MS data files into Pandas DataFrames)

## Examples

```
ms_data.plot(x='m/z', y='intensity', kind='spectrum', backend='ms_matplotlib'); ms_data.plot(x='m/z', y='intensity', kind='spectrum', backend='ms_bokeh'); ms_data.plot(x='m/z', y='intensity', kind='spectrum', backend='ms_plotly')
```

## Evaluation signals

- Output file exists in the correct format: PNG/PDF/SVG for matplotlib, HTML for Bokeh and Plotly.
- Visual inspection confirms that x and y axes are labeled correctly, plot title is present, and data points/traces are rendered (compare to reference gallery outputs in gallery_scripts/ms_matplotlib/, gallery_scripts/ms_bokeh/, gallery_scripts/ms_plotly/).
- For interactive backends (Bokeh, Plotly), verify that the HTML file is valid, embeds interactive widgets (hover tooltips, zoom, pan), and can be opened in a web browser without errors.
- For peakmap plots with add_marginals=True, confirm that marginal plots (1D projections) appear on the top and right edges of the 2D peak map.
- For peakmap plots with plot_3d=True (matplotlib and Plotly only), verify that the 3D surface or scatter plot renders with three axes (m/z, retention time, intensity) without errors.

## Limitations

- Bokeh backend does not support 3D visualization (plot_3d parameter is ignored); use matplotlib or Plotly for 3D peak maps.
- The backend parameter is fixed at plot time—switching backends requires re-running the .plot() call with a different backend value; there is no post-hoc backend conversion.
- Column naming flexibility is provided, but x, y, z labels must map to real columns in the input DataFrame; mismatched column names will raise an error.
- Interactive backends (Bokeh, Plotly) produce larger HTML files than static matplotlib output, which may impact performance in large-scale batch processing or storage-constrained environments.

## Evidence

- [readme] It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly): "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
- [other] For each of the four plot kinds (spectrum, chromatogram, mobilogram, peakmap), call the DataFrame .plot() method with the appropriate x, y (and z for peakmap) column names, set kind parameter to the plot type, and set backend to ms_matplotlib, ms_bokeh, or ms_plotly sequentially.: "For each of the four plot kinds (spectrum, chromatogram, mobilogram, peakmap), call the DataFrame .plot() method with the appropriate x, y (and z for peakmap) column names, set kind parameter to the"
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Consistent API across different plotting backends for easy switching between static and interactive plots: "Consistent API across different plotting backends for easy switching between static and interactive plots"
- [other] For peakmap plots, use m/z on x-axis and retention time on y-axis with intensity on z-axis (or color), optionally enabling add_marginals and plot_3d with PeakMapConfig parameters.: "For peakmap plots, use m/z on x-axis and retention time on y-axis with intensity on z-axis (or color), optionally enabling add_marginals and plot_3d with PeakMapConfig parameters"
- [readme] PeakMap 3D | x, y, z | peakmap (plot3d=True) | ✓ | | ✓: "PeakMap 3D | x, y, z | peakmap (plot3d=True) | ✓ | | ✓"
