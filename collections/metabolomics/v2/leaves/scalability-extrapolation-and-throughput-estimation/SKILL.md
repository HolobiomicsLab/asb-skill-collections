---
name: scalability-extrapolation-and-throughput-estimation
description: Use when you have a new or modified LC-MS data processing tool and need
  to determine whether it can handle production-scale sample cohorts (50–100+ samples)
  on modest hardware (single-core CPU, ≤16 GB RAM).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - asari
  - Python
  - pymzml
  - Python (3.8+)
  - psutil
  - time command (or GNU time)
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- The default method uses `pymzml` to parse mzML files.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# scalability-extrapolation-and-throughput-estimation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantify how a metabolomics data processing pipeline (asari) scales with increasing sample cohort sizes by measuring wall-clock runtime and peak memory usage across 10–100+ LC-MS mzML files, then plot and extrapolate performance metrics to estimate laptop-class hardware requirements and throughput bounds.

## When to use

You have a new or modified LC-MS data processing tool and need to determine whether it can handle production-scale sample cohorts (50–100+ samples) on modest hardware (single-core CPU, ≤16 GB RAM). Run this skill when planning data analysis workflows, evaluating tool suitability for a lab environment, or benchmarking algorithmic changes that might affect memory or CPU efficiency.

## When NOT to use

- You already have a vendor-validated SLA or performance report for your specific hardware and sample matrix; scaling measurements are most informative for novel or modified pipelines.
- Your input data are already processed feature tables rather than raw mzML files; scalability testing must start from raw instrument data to capture true I/O and alignment costs.
- Your cohort sizes are below 10 samples; variability in single-digit runs provides insufficient signal for reliable trend estimation.

## Inputs

- mzML file collection (10, 50, 100+ centroid LC-MS files)
- asari pipeline executable (v1.10+)
- system profiling tools (time, psutil, top, or equivalent)

## Outputs

- Tabulated runtime and memory metrics (mean, std dev per cohort size)
- Scatter plot: wall-clock time vs. sample count
- Scatter plot: peak resident memory vs. sample count
- Linear/polynomial trend line fit to each plot
- Extrapolated throughput estimate (samples/hour) for target cohort size
- Hardware requirement assessment (CPU cores, RAM) for production use

## How to apply

Obtain or subsample public mzML datasets (e.g., from MetaboLights or MassIVE) to construct three test cohorts of 10, 50, and 100+ samples. Execute the pipeline (asari v1.10+, with default parameters: 5 ppm m/z tolerance, positive ionization mode) on each cohort 2–3 times, recording wall-clock runtime and peak resident memory using system profiling tools (time command, psutil, or top). Tabulate mean and standard deviation for each metric by sample count, then plot both metrics versus sample number on a scatter plot with linear or polynomial trend lines. Compare observed throughput (samples/hour) and memory per sample to the claimed hardware threshold. If scaling is linear or near-linear, extrapolate to estimate resource usage at larger cohorts; if superlinear, investigate bottleneck steps (mass alignment, peak detection, or I/O) and report findings.

## Related tools

- **asari** (Primary metabolomics data processing pipeline; core subject of scalability benchmarking.) — https://github.com/shuzhao-li-lab/asari
- **pymzml** (Parses mzML files into memory during asari execution; contributes to wall-clock time and memory usage.)
- **Python (3.8+)** (Runtime environment and scripting language for executing asari and capturing profiling metrics.)
- **psutil** (System profiling library for recording peak resident memory and CPU time per run.)
- **time command (or GNU time)** (OS-level tool to measure elapsed wall-clock runtime and resource consumption per cohort execution.)

## Examples

```
for cohort in 10 50 100; do for run in {1..3}; do /usr/bin/time -v asari process --mode pos --input test_mzML_${cohort}samples >> scalability_${cohort}_run${run}.log 2>&1; done; done
```

## Evaluation signals

- Scaling plot shows linear or near-linear trend (R² > 0.95) across the three cohort sizes, indicating predictable and reproducible performance.
- Repeated runs (2–3 per cohort) yield ≤10% coefficient of variation in both runtime and memory metrics, confirming stable system behavior.
- Measured throughput (samples/hour) at the largest cohort matches or exceeds the claimed benchmark threshold for laptop-class hardware (≤16 GB RAM, single CPU core).
- Extrapolated memory usage at 100+ samples remains below the target hardware ceiling; if it exceeds the ceiling, flag as a scalability bottleneck.
- Peak memory per sample remains constant or decreases with increasing cohort size, indicating no catastrophic memory fragmentation or leak during repeated processing runs.

## Limitations

- Scaling measurements depend heavily on hardware configuration (CPU frequency, RAM speed, storage I/O bandwidth, background processes); results may not directly transfer to different systems.
- mzML file size, complexity (scan density, m/z range), and instrument type (Orbitrap vs. QTOF) all affect runtime and memory; cohort compositions should be representative of production data.
- Extrapolation beyond the tested range (e.g., predicting performance at 500 samples from 10–100 data) assumes scaling behavior remains linear, which may fail if new algorithmic bottlenecks emerge.
- Wall-clock time includes I/O, system load, and Python GIL contention; differences of 10–20% between runs are typical even on idle systems.
- The asari codebase is actively developed; version differences (especially between v1.10 and later releases with GC-MS support added in v1.16.6) may alter scalability profiles.

## Evidence

- [other] Retrieve public mzML datasets from MetaboLights or MassIVE repositories; select or subsample test data to create cohorts of 10, 50, and 100+ samples.: "Retrieve public mzML datasets from MetaboLights or MassIVE repositories; select or subsample test data to create cohorts of 10, 50, and 100+ samples."
- [other] For each cohort, execute asari process command and record wall-clock runtime and peak resident memory usage using system profiling tools (e.g., time command, psutil, or top).: "For each cohort, execute asari process command and record wall-clock runtime and peak resident memory usage using system profiling tools (e.g., time command, psutil, or top)."
- [other] Repeat runs 2–3 times per cohort to establish mean and standard deviation of timing and memory metrics.: "Repeat runs 2–3 times per cohort to establish mean and standard deviation of timing and memory metrics."
- [other] Tabulate results by sample count and plot wall-clock time and memory versus sample number to verify linear or near-linear scaling.: "Tabulate results by sample count and plot wall-clock time and memory versus sample number to verify linear or near-linear scaling."
- [other] Asari is designed as a scalable program with performance-conscious implementation prioritizing disciplined use of memory and CPU resources.: "Asari is designed as a scalable program with performance-conscious implementation prioritizing disciplined use of memory and CPU resources."
- [other] Compare observed throughput (samples/hour) and memory per sample to the claimed benchmark threshold for laptop-class hardware (≤16 GB RAM, single CPU core).: "Compare observed throughput (samples/hour) and memory per sample to the claimed benchmark threshold for laptop-class hardware (≤16 GB RAM, single CPU core)."
- [readme] Scalable, performance conscious, disciplined use of memory and CPU: "Scalable, performance conscious, disciplined use of memory and CPU"
