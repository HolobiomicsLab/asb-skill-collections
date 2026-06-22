---
name: gallery-benchmark-data-extraction
description: Use when you have access to a computation-times table or performance log documenting rendering execution times for multiple visualization examples across different plotting backends (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - pyOpenMS-viz
  - Python
  - plotly
  - Pandas
  - bokeh
  - matplotlib
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from pandas dataframes
- ms_data.plot(x="m/z", y="intensity", kind="spectrum")
- conda create --name=pyopenms-viz python=3.12
- Multiple backends supported including matplotlib, bokeh, and plotly
- Rendering is typically slower than the BOKEH backend
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyopenmsviz_cq
    doi: 10.1021/acs.jproteome.4c00873
    title: pyopenmsviz
  dedup_kept_from: coll_pyopenmsviz_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00873
  all_source_dois:
  - 10.1021/acs.jproteome.4c00873
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gallery-benchmark-data-extraction

## Summary

Extract execution-time metrics from a gallery of visualization examples to enable comparative performance analysis across multiple plotting backends. This skill isolates rendering times for each visualization type and backend combination, forming the foundation for systematic speedup and performance comparison workflows.

## When to use

Apply this skill when you have access to a computation-times table or performance log documenting rendering execution times for multiple visualization examples across different plotting backends (e.g., matplotlib, bokeh, plotly), and you need to systematically compare backend performance or identify rendering bottlenecks by visualization category (e.g., chromatogram, spectrum, peakmap, mobilogram).

## When NOT to use

- Execution times are not separately reported for each backend—only aggregate times across all backends are available.
- The computation-times table does not distinguish between rendering time and data-loading or preprocessing overhead.
- Only summary statistics (e.g., 'bokeh is faster') are reported without individual example timings.

## Inputs

- computation-times table (from article results or supplementary materials)
- list of 19 gallery example names and their visualization types
- mapping of examples to supported backends (from Supported Plots table or text)

## Outputs

- structured DataFrame with columns: example_name, visualization_type, backend, execution_time_seconds
- per-category aggregated rendering times (e.g., mean, median, std by visualization_type and backend)
- summary table of extracted execution times indexed by backend and visualization category

## How to apply

From the computation-times table, extract execution times for each of the 19 gallery examples, segregating entries by plotting backend (bokeh, plotly, matplotlib). Use Pandas to organize the extracted times into a structured DataFrame indexed by example name, visualization type, and backend. For examples available across multiple backends, create separate rows to preserve backend identity. Aggregate times by visualization category (chromatogram, spectrum, peakmap, mobilogram, etc.) to compute per-category mean rendering times. Validate that all entries are numeric and that no backend-example pairs are missing unexpectedly; flag any zero or null times for investigation. The extracted table becomes the input for downstream comparative analyses, such as mean speedup ratio calculation or rendering-time trend analysis.

## Related tools

- **Pandas** (Organize extracted execution times into DataFrames, aggregate by backend and visualization type, and prepare data for comparison)
- **Python** (Scripting environment for parsing computation-times table and iterating extraction logic)
- **pyOpenMS-viz** (Source of the 19 gallery examples and their documented rendering times across backends) — https://github.com/OpenMS/pyopenms_viz
- **bokeh** (One of the plotting backends whose rendering times are extracted and compared)
- **plotly** (One of the plotting backends whose rendering times are extracted and compared)
- **matplotlib** (One of the plotting backends whose rendering times are extracted and compared)

## Examples

```
import pandas as pd
df = pd.read_csv('computation_times.csv')
df_extracted = df[['example', 'visualization_type', 'backend', 'execution_time_seconds']]
df_agg = df_extracted.groupby(['visualization_type', 'backend'])['execution_time_seconds'].agg(['mean', 'std', 'count'])
print(df_agg)
```

## Evaluation signals

- All 19 gallery examples are represented in the extracted DataFrame with non-null execution times.
- Each example appears exactly once per supported backend (e.g., if spectrum is supported in bokeh and plotly, it appears in two rows with distinct execution_time values).
- Aggregated per-category times are computed correctly: mean and std of execution times for examples within each (visualization_type, backend) pair match manual spot checks.
- No execution times are zero, negative, or implausibly large (e.g., > 100 seconds for interactive rendering of a single example).
- Backend column values are exactly one of: 'bokeh', 'plotly', 'matplotlib'; visualization_type values match the Supported Plots table (chromatogram, mobilogram, spectrum, peakmap).

## Limitations

- Extracted times may conflate rendering latency with data-loading or preprocessing overhead if not separately measured in the source table.
- Execution-time metrics are hardware-dependent; timings from the article may not replicate on different machines or software versions.
- Not all visualization types are supported by all backends; missing (example, backend) pairs must be explicitly handled as 'not applicable' rather than treated as zero or missing data.
- The article abstract and intro do not report detailed execution-time metrics; extraction depends on the availability of a computation-times table in the results or supplementary materials.

## Evidence

- [other] No execution-time metrics comparing bokeh and plotly rendering performance are reported in the available abstract/intro/results text.: "No execution-time metrics comparing bokeh and plotly rendering performance are reported in the available abstract/intro/results text."
- [other] Extract execution times from the computation-times table for all 19 gallery examples, separating bokeh, plotly, and matplotlib entries.: "Extract execution times from the computation-times table for all 19 gallery examples, separating bokeh, plotly, and matplotlib entries."
- [other] Calculate aggregate and per-category rendering times for bokeh versus plotly backends.: "Calculate aggregate and per-category rendering times for bokeh versus plotly backends."
- [readme] Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive): "Support for multiple plotting backends: matplotlib (static), bokeh and plotly (interactive)"
- [readme] Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps: "Visualization of various mass spectrometry data types, including 1D chromatograms, spectra, and 2D peak maps"
