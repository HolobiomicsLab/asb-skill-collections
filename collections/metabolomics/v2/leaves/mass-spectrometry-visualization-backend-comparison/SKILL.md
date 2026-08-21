---
name: mass-spectrometry-visualization-backend-comparison
description: 'Use when you have a mass spectrometry visualization library that claims
  to support multiple plotting backends and need to verify that: (1) all backends
  produce functionally equivalent outputs, (2) execution times are consistent with
  reported benchmarks, and (3) the library scales appropriately.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - pyOpenMS-Viz
  - matplotlib
  - Bokeh
  - Plotly
  - Pandas
  - Python time module
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans: []
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-visualization-backend-comparison

## Summary

Compare execution time and performance characteristics of mass spectrometry visualizations across multiple plotting backends (matplotlib, Bokeh, Plotly) to assess backend suitability for different deployment contexts. This skill validates whether a visualization library's cross-backend integration functions correctly and identifies performance trade-offs between static and interactive rendering.

## When to use

You have a mass spectrometry visualization library that claims to support multiple plotting backends and need to verify that: (1) all backends produce functionally equivalent outputs, (2) execution times are consistent with reported benchmarks, and (3) the library scales appropriately across backend choices. Apply this skill when validating a new release, evaluating backend-specific memory or latency constraints, or benchmarking visualization performance for production deployment.

## When NOT to use

- Input is a single visualization or small batch (< 5 scripts); backend comparison requires statistically meaningful sample size across diverse visualization types.
- You do not have all three backends installed or cannot isolate backend switching; comparison requires identical environment state except for the active backend.
- The library does not claim cross-backend API consistency; benchmark differences may reflect intentional design trade-offs rather than bugs or performance regressions.

## Inputs

- Python 3.12 environment with pyOpenMS-Viz installed
- Gallery script collection (19 representative mass spectrometry visualization scripts)
- Three installed plotting backends: matplotlib, Bokeh, Plotly
- Reported benchmark table (execution times and memory consumption)
- System with stable resource allocation for timing measurements

## Outputs

- Structured benchmark table (CSV or DataFrame) with columns: Script name, matplotlib execution time, Bokeh execution time, Plotly execution time, total gallery time
- Comparison report: measured times vs. reported benchmark values
- Per-backend performance profile (median, min, max execution times across all scripts)
- Outlier analysis identifying scripts with atypical backend behavior

## How to apply

Set up a Python 3.12 environment with the visualization library and all three backends (matplotlib, Bokeh, Plotly) installed. Execute a representative suite of gallery scripts (e.g., 19 scripts covering chromatogram, spectrum, mobilogram, and peakmap visualization types) sequentially on each backend, recording wall-clock execution time for each script using Python's time module or Unix time command. Aggregate per-script execution times and compute total gallery execution time across all scripts and all backends. Tabulate results in a structured format (columns: Example name, Time per backend, Memory usage) and compare measured values against reported benchmarks. Evaluate consistency of execution profiles across backends; investigate backend-specific outliers (scripts that deviate significantly from the median backend behavior) as potential compatibility or optimization issues.

## Related tools

- **pyOpenMS-Viz** (mass spectrometry visualization library providing Pandas DataFrame API with three plotting backend support (matplotlib, Bokeh, Plotly); subject of the benchmark comparison) — https://github.com/OpenMS/pyopenms_viz
- **matplotlib** (static plotting backend for rendering mass spectrometry visualizations (chromatograms, spectra, peakmap 2D/3D))
- **Bokeh** (interactive plotting backend for rendering mass spectrometry visualizations with web-based interactivity)
- **Plotly** (interactive plotting backend for rendering mass spectrometry visualizations including 3D peakmap support)
- **Pandas** (data manipulation and DataFrame interface for mass spectrometry data input; timing measurements recorded in DataFrame output)
- **Python time module** (wall-clock timing instrumentation for measuring per-script execution time)

## Examples

```
import time; import pandas as pd; backends = ['matplotlib', 'bokeh', 'plotly']; times = {b: [] for b in backends}; exec(open('gallery_script_1.py').read()); t0 = time.time(); exec(open('gallery_script_2.py').read()); times['matplotlib'].append(time.time() - t0); df = pd.DataFrame({'Example': script_names, **{b: times[b] for b in backends}}); df.to_csv('benchmark_results.csv', index=False)
```

## Evaluation signals

- All 19 gallery scripts execute without error on each of the three backends, producing functionally equivalent visualizations (no missing plots, rendering errors, or API mismatches).
- Total gallery execution time measured across all backends matches or is within 10% of the reported benchmark (e.g., reported 00:06.221; measured < 6.84 seconds).
- Per-script execution times show consistent ordering and magnitude across backends, with no backend showing anomalous outliers (> 2 standard deviations from the backend median).
- Comparison table structure matches the article's reported schema (Example, Time, Mem columns); CSV export is valid and complete with no missing entries.
- Memory consumption profiles (if measured) remain stable and proportional to visualization complexity across all three backends, with no backend leaking resources between script executions.

## Limitations

- Execution times depend on system load, CPU thermal state, and available memory; repeated runs on identical hardware are needed to establish statistical confidence. Measurements should be taken in a controlled environment with minimal competing processes.
- Interactive backends (Bokeh, Plotly) may show higher latency on headless systems or remote rendering contexts compared to static matplotlib, limiting applicability of direct time comparisons across deployment scenarios.
- Gallery script suite may not represent user-facing workloads (e.g., real-time streaming, large dataset visualization); benchmark reflects artificial representativeness and may not predict production performance.
- Backend interchangeability is API-level only; visual output may differ subtly (font rendering, axis styling, color palette defaults), requiring manual inspection to confirm semantic equivalence.

## Evidence

- [other] What are the per-script execution times for the 19 gallery scripts across the three plotting backends (matplotlib, Bokeh, Plotly), and what is the total gallery execution time?: "What are the per-script execution times for the 19 gallery scripts across the three plotting backends (matplotlib, Bokeh, Plotly), and what is the total gallery execution time?"
- [other] Sequentially execute each of the 19 gallery scripts listed in the computation times table, recording wall-clock execution time for each script using a timer (e.g. Python's time module or Unix time command).: "Sequentially execute each of the 19 gallery scripts listed in the computation times table, recording wall-clock execution time for each script using a timer (e.g. Python's time module or Unix time"
- [other] Aggregate per-script execution times and compute the total execution time across all 19 scripts. Compare reported execution time for each script against the measured value; compare reported total (00:06.221) against the measured aggregate.: "Aggregate per-script execution times and compute the total execution time across all 19 scripts. Compare reported execution time for each script against the measured value; compare reported total"
- [other] The library integrates seamlessly with three plotting library backends: matplotlib, Bokeh, and Plotly, which are the backends used for the 19 gallery scripts whose execution times must be measured.: "The library integrates seamlessly with three plotting library backends: matplotlib, Bokeh, and Plotly, which are the backends used for the 19 gallery scripts whose execution times must be measured."
- [readme] It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation.: "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation."
- [other] Tabulate results in a dataframe matching the structure of the reported table (Example, Time, Mem columns) and export as CSV.: "Tabulate results in a dataframe matching the structure of the reported table (Example, Time, Mem columns) and export as CSV."
- [other] Set up a Python 3.12 environment with pyOpenMS-Viz installed via pip and all three plotting backends (matplotlib, Bokeh, Plotly) available.: "Set up a Python 3.12 environment with pyOpenMS-Viz installed via pip and all three plotting backends (matplotlib, Bokeh, Plotly) available."
