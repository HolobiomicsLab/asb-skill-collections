# Evaluation Strategy

## Direct Checks

- Verify file exists for each of: ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot output figures under matplotlib backend
- Verify file exists for each of: ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot output figures under Bokeh backend
- Verify file exists for each of: ChromatogramPlot, MobilogramPlot, SpectrumPlot, PeakMapPlot output figures under Plotly backend
- Verify file_format_is for each generated plot output (PNG, HTML, or SVG as appropriate to backend)
- Verify script_runs: execution of plot generation code using mzML input via pymzml/pyOpenMS without errors
- Verify script_runs: execution of plot generation code using Bruker .d input via AlphaTims without errors
- Output matches reference deposit: byte-for-byte comparison of static plot outputs (matplotlib/SVG) against gallery reference files; robust to parameter choices for interactive outputs (Bokeh/Plotly HTML)

## Expert Review

- Visual inspection of generated ChromatogramPlot figures across all three backends for correct intensity vs. retention time representation
- Visual inspection of generated MobilogramPlot figures across all three backends for correct intensity vs. ion mobility representation
- Visual inspection of generated SpectrumPlot figures across all three backends for correct m/z vs. intensity representation
- Visual inspection of generated PeakMapPlot figures across all three backends for correct 2D m/z vs. retention time heatmap/scatter representation
- Verification that interactive features (zoom, pan, hover tooltips) function correctly in Bokeh and Plotly outputs
