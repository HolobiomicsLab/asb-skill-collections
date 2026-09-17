---
name: multi-backend-plot-generation-and-benchmarking
description: Use when when you have a suite of Sphinx gallery example scripts targeting
  multiple plotting library backends and need to verify that all examples execute
  successfully within expected time constraints and produce output across matplotlib
  (static), bokeh (interactive), and plotly (interactive).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - pyOpenMS-viz
  - plotly
  - Python
  - Sphinx
  - matplotlib
  - bokeh
  - pandas
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- Chromatograms can be plotted using kind = chromatogram
- pyOpenMS-Viz is a visualization package for mass spectrometry data directly from
  pandas dataframes
- Multiple backends supported including matplotlib, bokeh, and plotly
- Rendering is typically slower than the BOKEH backend
- ms_data.plot(x="m/z", y="intensity", kind="spectrum")
- conda create --name=pyopenms-viz python=3.12
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Multi-backend plot generation and benchmarking

## Summary

Execute mass spectrometry visualization scripts across multiple plotting backends (matplotlib, bokeh, plotly) and measure aggregate execution time and resource usage to validate consistent performance and correctness across static and interactive visualization modes.

## When to use

When you have a suite of Sphinx gallery example scripts targeting multiple plotting library backends and need to verify that all examples execute successfully within expected time constraints and produce output across matplotlib (static), bokeh (interactive), and plotly (interactive) backends without performance regressions.

## When NOT to use

- Input is a single static visualization script rather than a multi-backend gallery suite; use this skill only when comparing performance across matplotlib, bokeh, and plotly implementations in parallel.
- Gallery scripts are already pre-rendered or cached; this skill requires fresh execution of all 19 example files to collect accurate timing metrics.
- Your objective is only to visualize one specific plot type (e.g., only spectra) and not to benchmark cross-backend consistency; this skill targets comprehensive gallery coverage and performance validation.

## Inputs

- pyOpenMS-viz repository source code (GitHub clone)
- 19 Sphinx gallery example scripts in gallery_scripts/ subdirectories (ms_bokeh/, ms_matplotlib/, ms_plotly/)
- Sphinx configuration files (conf.py, autodoc and autosummary settings)
- Python 3.12 environment with matplotlib, bokeh, plotly, and Sphinx installed

## Outputs

- Sphinx-generated HTML documentation with executed gallery examples
- Per-script execution time and memory usage metrics from Sphinx timer
- Aggregate total execution time across all 19 gallery files
- Validation report confirming all examples completed successfully across all three backends

## How to apply

Clone the pyOpenMS-viz repository and install dependencies in a Python 3.12 conda environment. Run sphinx-build to execute all gallery scripts organized by backend (ms_matplotlib/, ms_bokeh/, ms_plotly/) using Sphinx autosummary and autodoc extensions. Collect execution time and memory usage metrics reported by the Sphinx execution timer for each of the 19 example files. Aggregate the total execution time across all backends and verify it matches the reported benchmark (00:06.221) and that all examples complete without errors, indicating consistent backend support and stable performance across the plotting library ecosystem.

## Related tools

- **Sphinx** (Orchestrates gallery script execution, collects execution time and memory metrics via autosummary and autodoc extensions, and generates documentation with embedded timing reports)
- **matplotlib** (Static plotting backend for mass spectrometry visualizations; one of three backends to be benchmarked)
- **bokeh** (Interactive plotting backend for mass spectrometry visualizations; one of three backends to be benchmarked)
- **plotly** (Interactive plotting backend for mass spectrometry visualizations; one of three backends to be benchmarked)
- **pyOpenMS-viz** (Unified plotting API that interfaces directly with Pandas DataFrames and enables seamless switching between matplotlib, bokeh, and plotly backends for mass spectrometry data visualization) — https://github.com/OpenMS/pyopenms_viz
- **pandas** (DataFrame structures that hold mass spectrometry data (x, y, z coordinates) passed to pyOpenMS-viz plotting methods)

## Examples

```
cd pyopenms_viz && conda create --name=pyopenms-viz python=3.12 && conda activate pyopenms-viz && pip install -e . && sphinx-build -b html docs docs/_build
```

## Evaluation signals

- All 19 gallery example files execute without errors or warnings across all three backends (matplotlib, bokeh, plotly)
- Aggregate total execution time across all 19 examples matches or is less than the reported benchmark of 00:06.221 seconds
- Per-script execution time metrics are logged and reported by Sphinx timer for each example file
- Generated HTML gallery documentation contains rendered output for all plot types (chromatogram, mobilogram, spectrum, peakmap 2D/3D) across all backends
- Memory usage stays within expected bounds (no memory leaks or runaway allocations as reported by Sphinx metrics)

## Limitations

- Execution time metrics depend on host system performance (CPU, memory, I/O); benchmarks should be compared only against baselines from the same hardware or normalized per-core.
- Sphinx-reported timing includes overhead from documentation generation and autodoc introspection, not just gallery script runtime; true script-only timing may be lower.
- The 00:06.221 benchmark was measured in a specific environment (Python 3.12 with specific versions of matplotlib, bokeh, plotly); different dependency versions may yield different performance.
- 3D peakmap visualization (plotly-only feature) is not supported by bokeh and matplotlib backends, so some gallery examples may not render identically across all backends.

## Evidence

- [other] Validate cross-backend performance consistency: "Run sphinx-build to execute all 19 gallery scripts located in gallery_scripts/ (ms_bokeh/, ms_matplotlib/, ms_plotly/) using Sphinx autosummary and autodoc"
- [other] Benchmark aggregate execution time: "Collect execution time and memory usage metrics for each gallery script as reported by the Sphinx execution timer"
- [other] Benchmark target metric: "Verify that the aggregate total execution time matches the reported 00:06.221 metric and that all 19 example files complete successfully"
- [readme] Backend integration capability: "integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation"
- [readme] Installation prerequisite: "conda create --name=pyopenms_viz python=3.12"
