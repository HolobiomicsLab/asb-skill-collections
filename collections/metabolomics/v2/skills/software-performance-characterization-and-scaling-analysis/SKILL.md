---
name: software-performance-characterization-and-scaling-analysis
description: Use when when a tool claims to be 'scalable' or 'performance-conscious'
  but lacks published performance benchmarks, or when you need to confirm that runtime
  and memory scale linearly (or predictably) with sample count before deploying the
  tool on large LC-MS datasets (e.g., >100 samples).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - asari
  - Python
  - pymzml
  - Python psutil
  - Unix time command
  techniques:
  - LC-MS
  license_tier: restricted
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

# Software Performance Characterization and Scaling Analysis

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Empirically measure and verify how a computational tool (wall-clock time, peak resident memory) scales with increasing input size, validating performance claims and identifying bottlenecks. Essential for confirming scalability assertions in software designed for high-throughput metabolomics data processing.

## When to use

When a tool claims to be 'scalable' or 'performance-conscious' but lacks published performance benchmarks, or when you need to confirm that runtime and memory scale linearly (or predictably) with sample count before deploying the tool on large LC-MS datasets (e.g., >100 samples). Use this skill to validate whether a tool meets stated performance thresholds (e.g., laptop-class hardware with ≤16 GB RAM, single CPU core) under realistic conditions.

## When NOT to use

- The software has already been thoroughly benchmarked in peer-reviewed publications with multiple hardware configurations; repeating characterization adds no new evidence.
- You are profiling a single sample or a fixed small batch size; scaling analysis requires ≥3 distinct cohort sizes to detect growth patterns.
- Input data are not representative of production use (e.g., tiny toy datasets or synthetic data with atypical m/z density); benchmark results must reflect real-world data characteristics.

## Inputs

- Public mzML datasets (centroid format) from LC-MS metabolomics repositories (MetaboLights, MassIVE, or project-specific sources)
- Cohorts of test samples stratified by count (e.g., 10, 50, 100+ samples)
- Software installed with known version and default or specified parameters (e.g., asari v1.10+, 5 ppm m/z tolerance, positive ionization mode)

## Outputs

- Tabular summary of runtime (seconds) and peak resident memory (MB or GB) by cohort size
- Plots of wall-clock time vs. sample count and memory usage vs. sample count
- Computed throughput metric (samples/hour) and per-sample memory footprint (MB/sample)
- Scaling assessment (linear, near-linear, superlinear, or polynomial growth)

## How to apply

Execute the software on cohorts of increasing sample counts (e.g., 10, 50, 100+ mzML files) while recording wall-clock runtime and peak resident memory using system profiling tools (e.g., Unix `time` command, Python `psutil` module, or `top`). Repeat each run 2–3 times to establish mean and standard deviation. Tabulate results and plot wall-clock time and memory versus sample number to verify linear or near-linear scaling. Compare observed throughput (samples/hour) and memory per sample to the claimed benchmark threshold. If scaling is superlinear or memory grows polynomially, investigate which workflow steps are the bottleneck (e.g., mass track alignment, peak detection on composite map, or data structure indexing).

## Related tools

- **asari** (Target software for performance measurement; installed from pip (v1.10+) with specified parameters (5 ppm m/z tolerance, positive ionization mode); executed via `asari process` command) — https://github.com/shuzhao-li/asari
- **Python psutil** (System profiling library to record peak resident memory and CPU time programmatically during tool execution)
- **Unix time command** (Lightweight shell utility to measure wall-clock runtime and system resource usage for subprocess invocation)
- **pymzml** (Dependency used by asari to parse centroid mzML files; performance depends on parsing efficiency)

## Examples

```
for n in 10 50 100; do /usr/bin/time -v asari process --mode pos --input test_cohort_${n}samples 2>&1 | grep -E 'Elapsed|Maximum resident'; done
```

## Evaluation signals

- Mean runtime and memory metrics per cohort differ by <10% across 2–3 repeated runs (low variance indicates stable, reproducible measurement).
- Throughput (samples/hour) remains constant or increases slightly with cohort size (indicating true linear or near-linear scaling; severe degradation suggests O(n²) behavior).
- Observed per-sample memory footprint aligns with or is better than the claimed threshold (e.g., ≤16 GB peak memory for 100+ samples on single-core hardware).
- Scaling plot shows R² > 0.95 for linear regression on log-log axes if superlinear growth is suspected; a power law exponent close to 1.0 confirms linear behavior.
- No out-of-memory errors or process crashes occur during any cohort run; tool gracefully handles all tested sample counts.

## Limitations

- Performance is hardware-dependent (CPU core count, RAM speed, SSD vs. HDD, network I/O for remote data); benchmarks must specify host configuration and may not transfer to different machines.
- Scaling may differ across operating systems and Python versions; results are specific to the tested environment.
- Intermediate files (pickles, temporary JSON) can inflate I/O overhead and memory use; caching behavior and filesystem contention are not always predictable in shared computing environments.
- mzML file size and spectral density vary by instrument and ionization mode; cohorts must be representative of intended production workflows to avoid overfitting benchmarks to atypical datasets.

## Evidence

- [other] How does asari's computational performance (wall-clock time and peak memory usage) scale with increasing numbers of LC-MS samples?: "How does asari's computational performance (wall-clock time and peak memory usage) scale with increasing numbers of LC-MS samples?"
- [other] For each cohort, execute asari process command and record wall-clock runtime and peak resident memory usage using system profiling tools (e.g., time command, psutil, or top).: "For each cohort, execute asari process command and record wall-clock runtime and peak resident memory usage using system profiling tools (e.g., time command, psutil, or top)."
- [other] Tabulate results by sample count and plot wall-clock time and memory versus sample number to verify linear or near-linear scaling.: "Tabulate results by sample count and plot wall-clock time and memory versus sample number to verify linear or near-linear scaling."
- [other] Compare observed throughput (samples/hour) and memory per sample to the claimed benchmark threshold for laptop-class hardware (≤16 GB RAM, single CPU core).: "Compare observed throughput (samples/hour) and memory per sample to the claimed benchmark threshold for laptop-class hardware (≤16 GB RAM, single CPU core)."
- [other] Asari is designed as a scalable program with performance-conscious implementation prioritizing disciplined use of memory and CPU resources.: "Asari is designed as a scalable program with performance-conscious implementation prioritizing disciplined use of memory and CPU resources."
- [readme] Scalable, performance conscious, disciplined use of memory and CPU: "Scalable, performance conscious, disciplined use of memory and CPU"
