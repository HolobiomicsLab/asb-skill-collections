# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does pyOpenMS-viz route a user's backend specification through its layered architecture to dispatch the plot generation request to the correct plotting library backend?: 'It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] pyOpenMS-viz integrates seamlessly with three plotting library backends: matplotlib, bokeh, and plotly, enabling users to specify which backend to use for visualization generation.: 'It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] A user call to `.plot()` on a pandas DataFrame with parameters: `x` (column name), `y` (column name), `kind` (plot type: 'spectrum', 'chromatogram', 'peakmap', or 'mobilogram'), `backend` (one of 'ms_bokeh', 'ms_matplotlib', 'ms_plotly'), and optional parameters from BasePlotConfig or type-specific configs: 'ms_data.plot(x="m/z", y="intensity", kind="spectrum")'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Loaded pandas DataFrame containing mass spectrometry data with columns matching the specified x and y axis names: 'ms_data = pd.read_csv("path/to/ms_data.csv")
    pd.set_option("plotting.backend", "ms_bokeh")'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] A backend-specific plot object instantiated from one of the nine Extension Layer classes (e.g., BOKEHSpectrumPlot, MATPLOTLIBChromatogramPlot, PLOTLYPeakMapPlot) with full configuration applied and ready for rendering or further interaction: 'These are mass spectrometry plots that inherit from the BaseMSPlot class.

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: class.rst

   BOKEHChromatogramPlot'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] pyOpenMS-Viz: 'pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Pandas: 'ms_data = pd.read_csv("path/to/ms_data.csv")'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Bokeh: 'Extension: BOKEH'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Matplotlib: 'Extension: MATPLOTLIB'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Plotly: 'Extension: PLOTLY'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Python: 'conda create --name=pyopenms-viz python=3.12'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting the orchestrator architecture, backend routing mechanism, or version history is available in the provided discussion section.: '_No changelog found._'
