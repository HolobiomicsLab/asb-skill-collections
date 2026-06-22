---
name: computational-execution-table-generation
description: Use when when you have a set of gallery or benchmark scripts (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2996
  edam_topics:
  - http://edamontology.org/topic_0091
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

# computational-execution-table-generation

## Summary

Systematically execute a suite of computational scripts across multiple software backends, measure wall-clock execution time and resource consumption for each script, and aggregate results into a tabular format for performance comparison and reproducibility verification.

## When to use

When you have a set of gallery or benchmark scripts (e.g., 19 visualization examples) that must be executed against multiple plotting backends (matplotlib, Bokeh, Plotly) and you need to measure and report per-script execution times and total runtime to verify performance claims or establish baseline metrics.

## When NOT to use

- The scripts are designed to run in parallel or have asynchronous/background execution modes where sequential wall-clock timing would not capture true performance.
- Execution time variability is expected to be very high (>50% between runs) without explicit control of system load, in which case you would need multiple runs and statistical analysis (mean, stdev) rather than a single pass.
- The library or backends are still under active development with no stable/reproducible baseline, making time comparison against a fixed table unreliable.

## Inputs

- A directory or manifest listing N computational scripts (e.g., 19 gallery examples)
- A target Python environment with the library and all plotting backends pre-installed
- Expected or baseline execution time table (for validation comparison)

## Outputs

- Tabular result file (CSV or dataframe) with per-script execution times
- Aggregate total execution time across all scripts
- Comparison report: measured vs. reported times

## How to apply

Set up a Python 3.12 environment with the target library (e.g., pyOpenMS-Viz) and all required backends installed. Sequentially execute each script in the suite using a wall-clock timer (Python's `time` module or Unix `time` command), recording execution time for each run. After all scripts complete, aggregate per-script times and compute the total execution time across the suite. Compare measured values against any reported or claimed execution times to validate performance claims. Tabulate results in a structured dataframe with columns matching the expected output schema (Example/Script Name, Time, optional Memory columns) and export to CSV or other tabular format for inspection and archival.

## Related tools

- **pyOpenMS-Viz** (Target library whose gallery scripts are executed and timed across multiple plotting backends) — https://github.com/OpenMS/pyopenms_viz
- **Python time module** (Timer for measuring wall-clock execution duration of each script)
- **Pandas** (Data structure (dataframe) for organizing and exporting per-script execution times into tabular result)
- **matplotlib** (One of three plotting backends against which gallery scripts are executed)
- **Bokeh** (One of three plotting backends against which gallery scripts are executed)
- **Plotly** (One of three plotting backends against which gallery scripts are executed)

## Examples

```
import pandas as pd
import time
import subprocess

scripts = ['script_1.py', 'script_2.py', ..., 'script_19.py']
times = []
for script in scripts:
    start = time.time()
    subprocess.run(['python', script], check=True)
    elapsed = time.time() - start
    times.append({'Example': script, 'Time': elapsed})

df = pd.DataFrame(times)
df.to_csv('execution_times.csv', index=False)
print(f"Total time: {df['Time'].sum():.3f} seconds")
```

## Evaluation signals

- All 19 scripts in the suite executed without error and returned a measured execution time for each.
- Aggregate total execution time is computed correctly as the sum of per-script times.
- Measured per-script times match reported times within an acceptable tolerance (e.g., within 5–10% or within one standard deviation if multiple runs are averaged).
- Tabular output schema matches the expected structure (Example, Time, optional Mem columns) and can be imported as a Pandas dataframe or CSV without parsing errors.
- Wall-clock timer is consistent across runs (e.g., sequential re-execution of the same script produces similar times, confirming measurement stability).

## Limitations

- Wall-clock execution time is sensitive to system load, background processes, and hardware state; results may vary by >5% across runs on the same machine without explicit isolation or warm-up.
- The task measures only sequential execution; if scripts can run in parallel or if certain backends cache results, the measured times may not reflect real-world concurrent usage patterns.
- Memory consumption is not explicitly measured in the reported workflow; if memory profiling is required, additional instrumentation (e.g., `memory_profiler` module) would be needed.
- No statistical replication (e.g., n=3 runs per script) is described, so a single measured value has no confidence interval and may be an outlier.

## Evidence

- [other] Sequentially execute each of the 19 gallery scripts listed in the computation times table, recording wall-clock execution time for each script using a timer (e.g. Python's time module or Unix time command).: "Sequentially execute each of the 19 gallery scripts listed in the computation times table, recording wall-clock execution time for each script using a timer (e.g. Python's time module or Unix time"
- [other] Aggregate per-script execution times and compute the total execution time across all 19 scripts. Compare reported execution time for each script against the measured value; compare reported total (00:06.221) against the measured aggregate.: "Aggregate per-script execution times and compute the total execution time across all 19 scripts. Compare reported execution time for each script against the measured value; compare reported total"
- [other] Tabulate results in a dataframe matching the structure of the reported table (Example, Time, Mem columns) and export as CSV.: "Tabulate results in a dataframe matching the structure of the reported table (Example, Time, Mem columns) and export as CSV."
- [other] The library integrates seamlessly with three plotting library backends: matplotlib, Bokeh, and Plotly, which are the backends used for the 19 gallery scripts whose execution times must be measured.: "The library integrates seamlessly with three plotting library backends: matplotlib, Bokeh, and Plotly, which are the backends used for the 19 gallery scripts whose execution times must be measured."
- [other] Set up a Python 3.12 environment with pyOpenMS-Viz installed via pip and all three plotting backends (matplotlib, Bokeh, Plotly) available.: "Set up a Python 3.12 environment with pyOpenMS-Viz installed via pip and all three plotting backends (matplotlib, Bokeh, Plotly) available."
