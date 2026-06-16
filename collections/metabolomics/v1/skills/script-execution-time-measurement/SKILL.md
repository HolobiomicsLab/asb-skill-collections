---
name: script-execution-time-measurement
description: Use when you have a set of gallery or example scripts that must run consistently across multiple backend implementations (e.g., matplotlib, Bokeh, Plotly), and you need to verify that reported execution times are accurate or detect performance changes.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - pyOpenMS-Viz
  - Python time module
  - Pandas
  - matplotlib, Bokeh, Plotly
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyopenmsviz
    doi: 10.1021/acs.jproteome.4c00873
    title: pyopenmsviz
  dedup_kept_from: coll_pyopenmsviz
schema_version: 0.2.0
---

# script-execution-time-measurement

## Summary

Measure wall-clock execution time for a suite of scripts running against multiple backend implementations, aggregate per-script and total execution times, and compare measured values against reported benchmarks. This skill is essential for validating performance claims and detecting regressions across plotting backends.

## When to use

You have a set of gallery or example scripts that must run consistently across multiple backend implementations (e.g., matplotlib, Bokeh, Plotly), and you need to verify that reported execution times are accurate or detect performance changes. Use this skill when you have both a reference benchmark table with reported times and the ability to re-execute the scripts in a controlled environment.

## When NOT to use

- You only need to measure time for a single script or backend — use a simple timer instead.
- The scripts are not yet implemented or the gallery suite has not been finalized.
- You are measuring memory usage rather than execution time — use profiling tools (cProfile, memory_profiler) instead.

## Inputs

- 19 gallery scripts (e.g., Python files demonstrating plotting with pyOpenMS-Viz)
- Python 3.12 environment with pyOpenMS-Viz and all three plotting backends installed
- Reference benchmark table with reported execution times per script

## Outputs

- Per-script execution times (wall-clock, in seconds or HH:MM:SS format)
- Total gallery execution time (aggregate across all 19 scripts)
- Dataframe with columns: Example, Time, Mem (matching reported table structure)
- CSV export of benchmark results for comparison against reference

## How to apply

Set up a clean Python 3.12 environment with all required backends installed (e.g., via pip or conda). Sequentially execute each of the 19 gallery scripts in the suite, recording wall-clock execution time for each using Python's `time` module or Unix `time` command. Aggregate the per-script times and compute a total execution time across all scripts. Compare each measured execution time against the corresponding entry in the reported benchmark table (e.g., the 00:06.221 total reported in the reference). Tabulate results in a structured format (dataframe with Example, Time, Mem columns) and export to CSV for further comparison. The rationale is that multi-backend suites can experience performance drift; systematic re-measurement catches regressions and validates optimization claims.

## Related tools

- **pyOpenMS-Viz** (Library being benchmarked; provides the 19 gallery scripts and plotting backends (matplotlib, Bokeh, Plotly) to be timed) — https://github.com/OpenMS/pyopenms_viz
- **Python time module** (Timing utility for recording wall-clock execution time of each gallery script)
- **Pandas** (Data structure (dataframe) for aggregating and tabulating per-script times and metadata (Example, Time, Mem columns))
- **matplotlib, Bokeh, Plotly** (Plotting backends whose integration performance is being measured across the 19 gallery scripts)

## Evaluation signals

- Measured per-script execution times are recorded and match the number of scripts in the gallery (19 in this case).
- Total execution time aggregate matches the sum of per-script times; compare against reported total (00:06.221) — discrepancies > 5–10% warrant investigation.
- Dataframe structure matches the reference table (Example, Time, Mem columns); no missing or malformed entries.
- CSV export is valid and can be re-imported without data loss; row count equals number of scripts.
- Per-script times are consistent across re-runs (low variance) unless environmental factors (CPU load, I/O) are explicitly documented.

## Limitations

- Wall-clock times are sensitive to system load, I/O contention, and CPU frequency scaling; results should be collected on a quiet/dedicated system or averaged over multiple runs.
- The measurement framework assumes scripts are deterministic and reproducible; non-deterministic or long-tail behavior may require statistical aggregation (median, percentiles) rather than single-run times.
- Memory usage (Mem column) is not directly measured in the described workflow; profiling tools would be needed for accurate memory benchmarking alongside execution time.
- Timing overhead of the timer itself (e.g., Python `time` module resolution, context switching) is small but not zero; very fast scripts (<100 ms) may have relative timing noise.

## Evidence

- [other] Sequentially execute each of the 19 gallery scripts listed in the computation times table, recording wall-clock execution time for each script using a timer (e.g. Python's time module or Unix time command).: "Sequentially execute each of the 19 gallery scripts listed in the computation times table, recording wall-clock execution time for each script using a timer (e.g. Python's time module or Unix time"
- [other] Aggregate per-script execution times and compute the total execution time across all 19 scripts.: "Aggregate per-script execution times and compute the total execution time across all 19 scripts."
- [other] Compare reported execution time for each script against the measured value; compare reported total (00:06.221) against the measured aggregate.: "Compare reported execution time for each script against the measured value; compare reported total (00:06.221) against the measured aggregate."
- [other] Tabulate results in a dataframe matching the structure of the reported table (Example, Time, Mem columns) and export as CSV.: "Tabulate results in a dataframe matching the structure of the reported table (Example, Time, Mem columns) and export as CSV."
- [other] Set up a Python 3.12 environment with pyOpenMS-Viz installed via pip and all three plotting backends (matplotlib, Bokeh, Plotly) available.: "Set up a Python 3.12 environment with pyOpenMS-Viz installed via pip and all three plotting backends (matplotlib, Bokeh, Plotly) available."
