---
name: execution-time-aggregation-by-category
description: 'Use when you have measured execution times from multiple scripts that
  exercise different combinations of categorical variables (e.g., plot types: chromatogram,
  mobilogram, peakmap, peakmap-marginals, spectrum, subplots;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - pandas
  - matplotlib
  - Python
  license_tier: restricted
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

# execution-time-aggregation-by-category

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Aggregate execution times from gallery scripts into median, min, and max metrics grouped by categorical features (plot type and backend), then rank backends within each category to enable comparative performance analysis. This skill transforms raw timing measurements into structured summaries suitable for visualization and performance benchmarking across software implementations.

## When to use

You have measured execution times from multiple scripts that exercise different combinations of categorical variables (e.g., plot types: chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots; and backends: matplotlib, Bokeh, Plotly), and you need to identify which backend is fastest for each plot type by computing robust central tendency and spread metrics.

## When NOT to use

- Input data contains only a single backend or plot type — ranking and comparison require ≥2 categories in both dimensions.
- Execution times are not independent measurements; e.g., they come from a single end-to-end run with sequential overhead rather than isolated script executions.
- You need to infer statistical significance or detect outliers — use statistical hypothesis testing or anomaly detection skills instead.

## Inputs

- computation-times table (19 gallery script execution times with columns: script_name, plot_type, backend, execution_time_ms)
- pandas DataFrame with at least: plot_type (categorical), backend (categorical), execution_time (numeric)

## Outputs

- summary table (plot_type, backend, median_time, min_time, max_time, rank_within_category)
- comparative visualization (bar chart or heatmap of median times per plot type × backend)
- ranked list of backends per plot type

## How to apply

Extract execution times from the computation-times table in the methods section, assigning each of the 19 gallery scripts to a (plot_type, backend) pair. Use pandas groupby() operations to compute median, minimum, and maximum execution time for each plot-type and backend combination. Within each plot type, rank backends by median execution time (ascending) to identify fastest and slowest performers. Organize results into a structured summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category. Median is preferred over mean because execution-time distributions are often right-skewed due to system interference; ranking within category allows fair comparison despite absolute time differences across plot types.

## Related tools

- **pandas** (groupby aggregation (median, min, max) and DataFrame construction for summary table) — https://pandas.pydata.org
- **matplotlib** (static visualization (bar chart or heatmap) of aggregated execution times) — https://matplotlib.org
- **Python** (scripting environment for executing pandas operations and matplotlib rendering)

## Examples

```
import pandas as pd
df = pd.read_csv('computation_times.csv')  # columns: plot_type, backend, execution_time_ms
summary = df.groupby(['plot_type', 'backend'])['execution_time_ms'].agg(['median', 'min', 'max']).reset_index()
summary['rank'] = summary.groupby('plot_type')['median'].rank()
print(summary)
```

## Evaluation signals

- Summary table contains exactly one row per (plot_type, backend) pair with no missing median/min/max values.
- Median execution time for each (plot_type, backend) pair is between min and max for that pair (median ∈ [min, max]).
- Rank values within each plot_type are sequential integers from 1 to number_of_backends, with no ties unless times are identical.
- Visualization (bar chart or heatmap) displays all (plot_type, backend) combinations with no missing cells or data points.
- Visual inspection confirms that backend ranking is consistent: the backend with smallest median time ranks #1, and rank increases monotonically with median time within each plot category.

## Limitations

- Source data (computation-times table) is not included in the article text provided; the article states 'The document provides no reported timing metrics or execution time data for any plot types' — this skill cannot be applied until the table is extracted from the full methods section.
- Execution time is sensitive to system load, CPU frequency scaling, memory pressure, and JIT compilation warmup; single measurements per script-backend-plottype combination may not represent typical performance.
- Ranking backends by median time assumes that plot type is the relevant stratification; if execution time depends on data size, dimensionality, or other properties not captured in plot_type labels, rankings may not generalize to new data.

## Evidence

- [other] Extract the 19 gallery script execution times from the computation-times table in the methods section, categorizing each by plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum, subplots) and backend (ms_bokeh, ms_matplotlib, ms_plotly).: "Extract the 19 gallery script execution times from the computation-times table in the methods section, categorizing each by plot type (chromatogram, mobilogram, peakmap, peakmap-marginals, spectrum,"
- [other] Compute median execution time for each plot-type and backend combination.: "Compute median execution time for each plot-type and backend combination."
- [other] Generate a structured summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category.: "Generate a structured summary table with columns: plot_type, backend, median_time, min_time, max_time, rank_within_category."
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [other] The document provides no reported timing metrics or execution time data for any plot types across the three backends, making backend performance comparison impossible from the available text.: "The document provides no reported timing metrics or execution time data for any plot types across the three backends, making backend performance comparison impossible from the available text."
