# Evaluation Strategy

## Direct Checks

- verify that a gallery or timing metrics artifact exists in the repository at github:OpenMS__pyopenms_viz (e.g., benchmark results file, gallery HTML, or timing log)
- verify file_format_is: timing data is structured with columns or fields for plot_type, backend, and execution_time (or equivalent labels)
- verify field_present: each timing record includes at least plot_type (one of: chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots), backend (one of: matplotlib, bokeh, plotly), and a numeric execution time value
- verify script_runs: a Python script can load the reported timing metrics, compute median and range (max − min) for each (plot_type, backend) pair, and output a summary table or dict — robust to parameter choices in binning or aggregation
- verify output_matches_reference: computed medians and ranges are consistent with any summary table or statistics already published in the gallery or article text

## Expert Review

- assess whether the three backends show a systematic ordering (fastest to slowest) that is consistent across all or most plot categories, and whether any differences are practically significant
- evaluate whether backend performance correlates with plot complexity (e.g., whether interactive backends are consistently slower for simple plots)
- judge whether the timing data represents a fair and representative sample (e.g., consistent hardware, sufficient replicates per plot type per backend, comparable data sizes)
