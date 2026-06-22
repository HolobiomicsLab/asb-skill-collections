---
name: batch-script-performance-profiling
description: Use when you have a collection of N scripts (e.g., 19 gallery examples) that must run on multiple backends or configurations, and you need to produce a reproducible benchmark table showing per-script execution times and aggregate totals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - pyOpenMS-Viz
  - Python time module
  - Pandas
  - matplotlib
  - Bokeh
  - Plotly
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

# batch-script-performance-profiling

## Summary

Systematically measure wall-clock execution time and resource consumption for multiple scripts across different software backends or configurations to establish performance baselines and detect regressions. This skill is essential when validating that library integrations maintain consistent performance across plotting backends (matplotlib, Bokeh, Plotly) or when benchmarking reproducibility of gallery examples.

## When to use

You have a collection of N scripts (e.g., 19 gallery examples) that must run on multiple backends or configurations, and you need to produce a reproducible benchmark table showing per-script execution times and aggregate totals. Typical trigger: validating that reported benchmark results match measured values, or detecting performance drift across library versions or backend choices.

## When NOT to use

- Input scripts have external dependencies (network I/O, file I/O to non-local paths, interactive input) that cannot be deterministically timed in a batch context.
- You only need to profile a single script or function; use line-level profiling (cProfile, line_profiler) instead.
- Benchmark environment is heterogeneous (multiple simultaneous users, variable CPU load) and you need statistical certainty; use a dedicated benchmarking harness with multiple runs and confidence intervals.

## Inputs

- Python 3.12 conda environment with pyOpenMS-Viz, matplotlib, Bokeh, Plotly installed
- Batch of N gallery scripts (e.g., 19 .py files from a gallery directory)
- Reported baseline benchmark table or execution-time reference

## Outputs

- CSV file with columns: Example, Time (seconds), Mem (memory usage if measured)
- Aggregated total execution time across all scripts
- Comparison report showing measured vs. reported timings

## How to apply

Set up an isolated Python environment with all required dependencies (e.g., pyOpenMS-Viz, matplotlib, Bokeh, Plotly). Sequentially execute each script in the batch using a wall-clock timer (Python's `time` module or Unix `time` command), recording both per-script and total execution time. Run each script in the same process or shell session to ensure consistent baseline conditions. Aggregate results into a structured format (CSV or dataframe) with columns matching the benchmark table schema (Example, Time, Mem). Compare measured values against reported baselines; discrepancies >5–10% may indicate environment drift or backend performance variation. Export results as CSV for archival and version control.

## Related tools

- **pyOpenMS-Viz** (Library whose gallery scripts are to be benchmarked across plotting backends) — https://github.com/OpenMS/pyopenms_viz
- **Python time module** (Built-in timer for recording wall-clock execution time per script)
- **Pandas** (Data manipulation and aggregation of benchmark results into structured table format)
- **matplotlib** (Plotting backend whose gallery scripts are included in the batch benchmark)
- **Bokeh** (Interactive plotting backend whose gallery scripts are included in the batch benchmark)
- **Plotly** (Interactive plotting backend whose gallery scripts are included in the batch benchmark)

## Examples

```
import time
import pandas as pd
import subprocess

scripts = ['gallery_script_1.py', 'gallery_script_2.py', ...]
results = []
for script in scripts:
    start = time.time()
    subprocess.run(['python', script], check=True)
    elapsed = time.time() - start
    results.append({'Example': script, 'Time': elapsed})

df = pd.DataFrame(results)
df['Total'] = df['Time'].sum()
df.to_csv('benchmark_results.csv', index=False)
```

## Evaluation signals

- Per-script execution times are recorded for all 19 scripts with no missing or null values
- Total aggregated execution time matches reported baseline (e.g., 00:06.221) within ±10% margin
- Exported CSV has consistent schema with reported benchmark table (Example, Time, Mem columns present)
- Wall-clock timer invocations are deterministic: re-running the batch on the same environment yields times within ±5% of first run
- No script in the batch raises unhandled exceptions during timed execution

## Limitations

- Wall-clock timing is sensitive to system load, context switching, and cache state; results may vary 5–15% across runs on a shared system.
- Measurement does not capture memory usage or peak memory allocation unless explicitly instrumented (e.g., with `psutil` or `/usr/bin/time -v`).
- Scripts with file I/O or network calls introduce non-deterministic variance; isolate or mock external dependencies if reproducibility is critical.
- Reported baseline (00:06.221 total) assumes consistent Python 3.12 environment and backend versions; deviations may reflect library version drift rather than genuine regression.

## Evidence

- [other] per-script execution times for the 19 gallery scripts listed in the computation times table, recording wall-clock execution time for each script using a timer (e.g. Python's time module or Unix time command): "Sequentially execute each of the 19 gallery scripts listed in the computation times table, recording wall-clock execution time for each script using a timer (e.g. Python's time module or Unix time"
- [other] The library integrates seamlessly with three plotting library backends: matplotlib, Bokeh, and Plotly, which are the backends used for the 19 gallery scripts: "The library integrates seamlessly with three plotting library backends: matplotlib, Bokeh, and Plotly, which are the backends used for the 19 gallery scripts whose execution times must be measured."
- [other] Aggregate per-script execution times and compute the total execution time across all 19 scripts. Compare reported execution time for each script against the measured value; compare reported total (00:06.221) against the measured aggregate.: "Aggregate per-script execution times and compute the total execution time across all 19 scripts. 4. Compare reported execution time for each script against the measured value; compare reported total"
- [other] Tabulate results in a dataframe matching the structure of the reported table (Example, Time, Mem columns) and export as CSV: "Tabulate results in a dataframe matching the structure of the reported table (Example, Time, Mem columns) and export as CSV."
- [other] Set up a Python 3.12 environment with pyOpenMS-Viz installed via pip and all three plotting backends (matplotlib, Bokeh, Plotly) available: "Set up a Python 3.12 environment with pyOpenMS-Viz installed via pip and all three plotting backends (matplotlib, Bokeh, Plotly) available."
