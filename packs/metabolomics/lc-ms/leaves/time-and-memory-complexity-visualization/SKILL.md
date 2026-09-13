---
name: time-and-memory-complexity-visualization
description: Use when when deploying a metabolomics processing tool (such as asari)
  and needing to predict resource requirements or validate claimed scalability on
  laptop-class hardware (≤16 GB RAM, single CPU core).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - asari
  - Python
  - pymzml
  - psutil
  - Unix time command
  techniques:
  - LC-MS
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

# time-and-memory-complexity-visualization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantify and visualize how wall-clock runtime and peak memory usage scale with increasing sample numbers in LC-MS metabolomics data processing, enabling empirical verification of claimed computational efficiency on resource-constrained hardware.

## When to use

When deploying a metabolomics processing tool (such as asari) and needing to predict resource requirements or validate claimed scalability on laptop-class hardware (≤16 GB RAM, single CPU core). Apply this skill when tool documentation claims 'scalable, performance conscious' implementation but provides no empirical scaling curves, or when you must decide whether to process cohorts of 10, 50, or 100+ samples on available hardware.

## When NOT to use

- Input data have already been processed into a feature table; use this skill only on raw mzML cohorts.
- Tool documentation already includes detailed scaling benchmarks for your hardware class and sample size range; re-measuring is redundant.
- You only need to process a single sample or a fixed small cohort; scaling analysis is unnecessary when cohort size is not a decision variable.

## Inputs

- mzML files from public repositories (MetaboLights, MassIVE) organized into test cohorts of varying sizes (10, 50, 100+ samples)
- Installed tool (asari v1.10+) with specified parameters (5 ppm m/z tolerance, positive ionization mode)

## Outputs

- Tabulated timing and memory metrics (mean, standard deviation) indexed by sample count
- Wall-clock time vs. sample count plot (linear or near-linear curve)
- Peak resident memory vs. sample count plot
- Computed throughput metric (samples/hour) and memory per sample (GB/sample)
- Comparison table: observed resource usage vs. claimed benchmark for laptop-class hardware

## How to apply

Execute the processing tool (asari with default parameters: 5 ppm m/z tolerance, positive ionization mode) on successive cohorts of increasing sample size (e.g., 10, 50, 100+ mzML files). For each cohort, measure wall-clock runtime and peak resident memory using system profiling tools (e.g., Unix `time` command, Python `psutil`, or `top`). Repeat each cohort 2–3 times to establish mean and standard deviation. Tabulate results by sample count and plot both metrics versus sample number on linear axes. Verify that the relationship is linear or near-linear (slope approximately constant), confirming the tool's throughput claim (samples/hour). Compare observed memory per sample to the documented threshold for laptop-class hardware to identify the largest cohort processable without swap or OOM failure.

## Related tools

- **asari** (primary tool under evaluation; invoked with process command on successive mzML cohorts to measure wall-clock runtime and memory consumption) — https://github.com/shuzhao-li/asari
- **psutil** (Python library for programmatic collection of peak resident memory and CPU metrics during tool execution)
- **Unix time command** (system utility to measure wall-clock runtime and resource usage of asari invocations)
- **pymzml** (underlying library used by asari to parse mzML files; understanding its performance is part of understanding overall scalability)

## Examples

```
for n in 10 50 100; do time python3 -m asari.main process -i test_cohort_${n}samples -o result_${n} --mode pos 2>&1 | tee timing_${n}.log; done
```

## Evaluation signals

- Computed slopes of wall-clock time vs. sample count and memory vs. sample count are approximately constant, indicating linear or near-linear scaling.
- Reported throughput (samples/hour) matches or exceeds the tool's documented benchmark; if lower, investigate hardware, parameter choices, or file I/O bottlenecks.
- Peak memory observed in the largest cohort remains below the claimed hardware threshold (e.g., 16 GB for laptop-class); failure indicates unsuitability for that cohort size.
- Repeat runs (2–3 iterations per cohort) show low standard deviation in both timing and memory metrics, indicating stable, reproducible performance.
- No OOM errors, swap file usage, or process termination during the largest cohort run; resource exhaustion signals scaling failure at that size.

## Limitations

- Hardware heterogeneity: wall-clock time and memory are system-dependent; results on a laptop with spinning disk differ from SSD and multi-core CPU; comparison to laptop-class threshold requires matching hardware class.
- File I/O variability: mzML file format, vendor source, and filesystem caching can introduce ±10–30% variance in measured time; use sufficiently large cohorts to amortize I/O overhead.
- Parameter sensitivity: tool behavior (and resource consumption) may change with different m/z tolerance, ionization mode, or peak detection thresholds; scaling curves are valid only for the exact parameters tested.
- Single-run snapshots: peak memory is measured at a single point in time during execution; true worst-case memory (e.g., during intermediate data structure allocation) may be higher if not sampled frequently enough.
- No predictive model: plotting observed data does not extrapolate reliably to cohort sizes not tested; assume linear trend only within the tested range.

## Evidence

- [other] asari is designed as a scalable program with performance-conscious implementation prioritizing disciplined use of memory and CPU resources: "Asari is designed as a scalable program with performance-conscious implementation prioritizing disciplined use of memory and CPU resources."
- [other] For each cohort, execute asari process command and record wall-clock runtime and peak resident memory usage using system profiling tools: "For each cohort, execute asari process command and record wall-clock runtime and peak resident memory usage using system profiling tools (e.g., time command, psutil, or top)."
- [other] Repeat runs 2–3 times per cohort to establish mean and standard deviation of timing and memory metrics: "Repeat runs 2–3 times per cohort to establish mean and standard deviation of timing and memory metrics."
- [other] Plot wall-clock time and memory versus sample number to verify linear or near-linear scaling: "Tabulate results by sample count and plot wall-clock time and memory versus sample number to verify linear or near-linear scaling."
- [other] Compare observed throughput (samples/hour) and memory per sample to the claimed benchmark threshold for laptop-class hardware (≤16 GB RAM, single CPU core): "Compare observed throughput (samples/hour) and memory per sample to the claimed benchmark threshold for laptop-class hardware (≤16 GB RAM, single CPU core)."
- [readme] Scalable, performance conscious, disciplined use of memory and CPU: "Scalable, performance conscious, disciplined use of memory and CPU"
