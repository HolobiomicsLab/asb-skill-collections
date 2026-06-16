# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What are the per-script execution times for the 19 gallery scripts across the three plotting backends (matplotlib, Bokeh, Plotly), and what is the total gallery execution time?: 'pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames for creating static or interactive visualizations of mass spectrometry'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The library integrates seamlessly with three plotting library backends: matplotlib, Bokeh, and Plotly, which are the backends used for the 19 gallery scripts whose execution times must be measured.: 'It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] 19 gallery scripts (Python files) across ms_matplotlib, ms_bokeh, and ms_plotly backends from the pyOpenMS-Viz repository: '**from all galleries**: [contains list of 19 scripts with file paths like gallery_scripts/ms_plotly/plot_peakmap_marginals_ms_plotly.py]'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] pyOpenMS-Viz library, pandas, matplotlib, Bokeh, and Plotly packages installed in Python 3.12 environment: 'pip install pyopenmsviz --upgrade'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] A CSV or structured table file with columns (Example, Time, Mem (MB)) containing per-script execution times for all 19 gallery scripts, matching the reported computation times table: 'Computation times... **00:06.221** total execution time for 19 files'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Total aggregate execution time (minutes:seconds.milliseconds format) across all 19 scripts for verification against reported 00:06.221: '**00:06.221** total execution time for 19 files'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] pyOpenMS-Viz: 'pyOpenMS-Viz is a Python library that provides a simple interface for extending the plotting capabilities of Pandas DataFrames'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Pandas: 'leverages the power of Pandas for data manipulation and representation'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] matplotlib: 'integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Bokeh: 'integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Plotly: 'integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Python: 'conda create --name=pyopenms-viz python=3.12'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history is provided for pyOpenMS-viz: '_No changelog found._'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The section text does not specify where per-script execution times and gallery timing data are located or how they are reported: 'No reference to timing data location or format in provided text; only metadata provided: 'Source: github:OpenMS__pyopenms_viz, Synthesized at: 2026-06-16T07:19:09+00:00''

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Details on hardware platform, Python version, and environment configuration used for the reported gallery execution time are not documented: 'Section text contains no information on execution environment, hardware specs, or Python configuration used for timing measurements'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No documentation of whether the 00:06.221 gallery time includes compilation, import overhead, or only script execution: 'Section text does not clarify timing scope or boundaries'
