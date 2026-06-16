# Evaluation Strategy

## Direct Checks

- verify file exists: gallery execution log or timing report in github:OpenMS__pyopenms_viz repository
- file_format_is: timing report is structured (CSV, JSON, YAML, or table) with columns/fields for script_name, backend, and execution_time_seconds
- field_present: each of 19 scripts appears in timing report with entries for all three backends (ms_matplotlib, ms_bokeh, ms_plotly)
- value_in_range: total gallery execution time sum across all script-backend combinations equals 00:06.221 (372.221 seconds), robust to ±0.5 second measurement variance
- script_runs: reproduce gallery build command (e.g., sphinx-build or make gallery) on fresh clone of github:OpenMS__pyopenms_viz and capture wall-clock execution time
- output_matches_reference: reproduced total gallery execution time matches reported 00:06.221 within ±5% (measurement tolerance for hardware/load variation)

## Expert Review

- assess whether reported per-script times are plausible given typical visualization library overhead (matplotlib < bokeh < plotly expected pattern)
- confirm that timing methodology (single run per script vs. averaged runs) is documented and appropriate for performance claims
- evaluate whether 00:06.221 total is reasonable for 19 scripts across 3 backends on contemporary hardware (no obvious bottlenecks or anomalies)
