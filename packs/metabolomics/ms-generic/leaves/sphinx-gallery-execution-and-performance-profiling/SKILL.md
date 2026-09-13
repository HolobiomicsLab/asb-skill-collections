---
name: sphinx-gallery-execution-and-performance-profiling
description: Use when you have a Sphinx-based documentation project with multiple
  gallery scripts (e.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - pyOpenMS-viz
  - plotly
  - Sphinx
  - Python
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
- Build docs with sphinx-build
- ms_data.plot(x="m/z", y="intensity", kind="spectrum")
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

# sphinx-gallery-execution-and-performance-profiling

## Summary

Measure and verify the aggregate execution time and memory footprint of a multi-backend Sphinx gallery by running all gallery scripts and comparing reported metrics against expected benchmarks. This skill ensures reproducibility and performance compliance across static and interactive visualization backends.

## When to use

Apply this skill when you have a Sphinx-based documentation project with multiple gallery scripts (e.g., organized by plotting backend: matplotlib, bokeh, plotly) and need to validate that the total gallery execution time matches a known reference metric or baseline, or when establishing performance budgets for documentation builds.

## When NOT to use

- When gallery scripts are not organized within a Sphinx project or do not use sphinx_gallery extension; use ad-hoc profiling (e.g., timeit, cProfile) instead.
- When only a single backend or a subset of gallery examples needs profiling; simpler profiling tools suffice for isolated script timing.
- When the reference benchmark is unknown or intentionally being established for the first time; this skill assumes a known target metric for validation.

## Inputs

- Sphinx gallery script directory tree (gallery_scripts/ with backend subdirectories)
- conf.py and gallery configuration (sphinx_gallery_conf)
- 19 example gallery scripts (Python files with docstrings and executable code blocks)
- Python 3.12 conda environment with matplotlib, bokeh, plotly, and pyOpenMS-viz installed

## Outputs

- Aggregate execution time (e.g., 00:06.221 in HH:MM.SSS format)
- Per-script execution time and memory usage metrics (from Sphinx timer)
- Exit code and build log indicating success or failure of all 19 gallery scripts
- HTML gallery documentation with rendered plots (static and interactive)

## How to apply

Clone the repository and install dependencies in a Python 3.12 conda environment. Run `sphinx-build` to execute all gallery scripts via Sphinx autosummary and autodoc, collecting execution time and memory usage metrics reported by Sphinx's built-in execution timer. Sum the per-script execution times and compare the aggregate total against the reference benchmark (e.g., 00:06.221). Verify that all 19 example files (across ms_bokeh/, ms_matplotlib/, ms_plotly/ subdirectories) complete without error. Use this workflow to detect performance regressions, memory leaks, or backend-specific bottlenecks across visualizations of mass spectrometry data types (chromatograms, spectra, peakmaps).

## Related tools

- **Sphinx** (Documentation build system and gallery executor; runs sphinx-build to invoke autosummary and autodoc, measuring per-script execution time)
- **pyOpenMS-viz** (Source library providing mass spectrometry visualization API (spectrum, chromatogram, peakmap plots) executed by gallery scripts across matplotlib, bokeh, plotly backends) — https://github.com/OpenMS/pyopenms_viz
- **matplotlib** (Static plotting backend; one of three backends tested in the gallery example suite)
- **bokeh** (Interactive plotting backend; one of three backends tested in the gallery example suite)
- **plotly** (Interactive plotting backend; one of three backends tested in the gallery example suite)
- **pandas** (Data manipulation and DataFrame interface for mass spectrometry data input to pyOpenMS-viz plot methods)
- **Python** (Runtime environment (version 3.12) for executing gallery scripts and Sphinx build system)

## Examples

```
conda create --name=pyopenms-viz python=3.12 && conda activate pyopenms-viz && git clone https://github.com/OpenMS/pyopenms_viz.git && cd pyopenms_viz && pip install -e . && sphinx-build -b html docs/ docs/_build/
```

## Evaluation signals

- Aggregate execution time reported by Sphinx matches the reference metric (00:06.221) within a tolerance (e.g., ±5%)
- All 19 gallery scripts (across ms_bokeh/, ms_matplotlib/, ms_plotly/ directories) complete without error; sphinx-build exit code is 0
- Per-script execution times are logged and individually plausible (no outliers >2× interquartile range suggesting hangs or failures)
- Memory usage metrics are captured for each script; peak memory does not exceed system limits or documented budget
- HTML gallery documentation builds successfully with all plots rendered (static matplotlib images, interactive bokeh/plotly widgets)

## Limitations

- Execution time is system-dependent (CPU, I/O, available memory); reproducibility across different hardware may vary; consider running on a standardized CI/CD environment.
- Sphinx execution timer precision may be coarse (millisecond or second granularity); for fine-grained profiling use Python's timeit or cProfile.
- Memory usage reported by Sphinx may not capture peak heap usage for all backends (e.g., bokeh/plotly may defer rendering to browser/client); consider supplementary tools (memory_profiler, tracemalloc).
- Gallery script execution order and caching behavior (e.g., Sphinx gallery's image cache) can affect total time; clear caches or use --fresh-env flag for consistent baselines.

## Evidence

- [other] Verify that the aggregate total execution time matches the reported 00:06.221 metric and that all 19 example files complete successfully.: "Verify that the aggregate total execution time matches the reported 00:06.221 metric and that all 19 example files complete successfully"
- [other] Run sphinx-build to execute all 19 gallery scripts located in gallery_scripts/ (ms_bokeh/, ms_matplotlib/, ms_plotly/) using Sphinx autosummary and autodoc.: "Run sphinx-build to execute all 19 gallery scripts located in gallery_scripts/ (ms_bokeh/, ms_matplotlib/, ms_plotly/) using Sphinx autosummary and autodoc"
- [other] Collect execution time and memory usage metrics for each gallery script as reported by the Sphinx execution timer.: "Collect execution time and memory usage metrics for each gallery script as reported by the Sphinx execution timer"
- [other] Clone the pyOpenMS-viz repository from GitHub and install dependencies via pip in a conda environment with Python 3.12.: "Clone the pyOpenMS-viz repository from GitHub and install dependencies via pip in a conda environment with Python 3.12"
- [readme] integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly): "integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly)"
