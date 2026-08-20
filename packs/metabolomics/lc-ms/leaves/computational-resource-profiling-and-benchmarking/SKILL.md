---
name: computational-resource-profiling-and-benchmarking
description: Use when when evaluating a new or updated version of a data processing tool (especially asari or similar LC-MS workflows) before production deployment, or when verifying claims about scalability, memory efficiency, or throughput on specific hardware classes (e.g., ≤16 GB RAM single-core systems).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - asari
  - Python
  - pymzml
  - psutil
  - Unix time command
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
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

# computational-resource-profiling-and-benchmarking

## Summary

Systematically measure and characterize wall-clock runtime and peak memory consumption of a metabolomics processing tool across increasing sample cohort sizes to verify scalability claims and establish throughput benchmarks on target hardware. This skill validates whether software meets claimed performance targets for laptop-class and cloud deployments.

## When to use

When evaluating a new or updated version of a data processing tool (especially asari or similar LC-MS workflows) before production deployment, or when verifying claims about scalability, memory efficiency, or throughput on specific hardware classes (e.g., ≤16 GB RAM single-core systems). Apply this skill if you need to understand whether the tool can process your dataset size within acceptable time and memory constraints.

## When NOT to use

- Input data are already processed into feature tables or peak lists (profiling measures raw data processing, not downstream analysis)
- Benchmarking a tool on non-representative data or on hardware orders of magnitude different from target deployment (e.g., benchmarking on a GPU-accelerated cluster when the claim is for laptop single-core use)
- No access to system profiling tools or permission to monitor resource consumption on the target hardware

## Inputs

- mzML file cohorts of varying sizes (10, 50, 100+ centroid mzML files from public repositories)
- Tool executable and configuration parameters (asari version, ionization mode, m/z tolerance)
- Target hardware specification (RAM, CPU core count)

## Outputs

- Tabulated runtime and peak memory metrics (mean ± SD) by sample count
- Scatter plots or line plots of wall-clock time vs. sample count and memory vs. sample count
- Computed throughput metric (samples/hour) and memory-per-sample ratio
- Comparison summary against claimed benchmark thresholds
- Scalability assessment (linear, near-linear, sub-linear, super-linear)

## How to apply

Execute the target tool (asari v1.10+) on public mzML datasets organized into sample cohorts of increasing size (10, 50, 100+ samples) retrieved from MetaboLights or MassIVE repositories. For each cohort, run the tool 2–3 times with identical parameters (e.g., 5 ppm m/z tolerance, positive ionization mode, default settings) and capture wall-clock runtime and peak resident memory using system profiling tools (e.g., Unix `time` command, Python `psutil`, or `top`). Record mean and standard deviation for each metric. Plot both metrics against sample count to assess linearity of scaling. Compare observed throughput (samples/hour) and memory per sample to claimed benchmark thresholds (e.g., laptop-class hardware with ≤16 GB RAM, single CPU core). The rationale is that linear or near-linear scaling validates the design claim of 'scalable, performance conscious' resource management.

## Related tools

- **asari** (Target tool being profiled for scalability across increasing sample counts) — https://github.com/shuzhao-li-lab/asari
- **psutil** (Python library to capture peak resident memory and CPU metrics during execution)
- **Unix time command** (System utility to measure wall-clock runtime and resource usage per process)
- **pymzml** (mzML file parser used by asari to extract MS1 spectra; performance depends on file size and format)

## Examples

```
time asari process --mode pos --input /path/to/sample_cohort_10/ 2>&1 | grep -E 'real|user|sys' && python -c "import psutil; p=psutil.Process(); print(f'Peak RSS: {p.memory_info().rss / 1024**2:.1f} MB')"
```

## Evaluation signals

- Scaling plot shows linear or near-linear trend (R² > 0.95) across the sample count range; deviation from linearity indicates bottlenecks or unexpected algorithmic complexity
- Measured peak memory per sample remains constant or decreases slightly (not superlinear) as cohort size grows, confirming 'disciplined use of memory' claim
- Computed throughput (samples/hour) is ≥ claimed benchmark on target hardware (e.g., ≥ X samples/hour on ≤16 GB RAM single-core laptop)
- Coefficient of variation (SD/mean) for repeated runs ≤ 10–15% for both runtime and memory, indicating reproducibility and stable system state
- Tool completes without out-of-memory errors or crashes at the largest cohort size tested (100+ samples)

## Limitations

- Profiling results are hardware- and OS-specific; benchmarks on one machine (e.g., Linux desktop) may not generalize to another (e.g., macOS, Windows, or cloud VM) due to I/O, scheduler, and memory management differences.
- Variability in public dataset characteristics (file size, scan density, mass accuracy, complexity) can introduce noise; use consistent, representative subsets for reproducible comparison.
- System load and background processes during profiling can inflate memory and runtime measurements; isolate the tool and minimize other tasks on the target hardware.
- Benchmarking only reflects the data processing workflow (asari process command); annotation (asari annotate) and visualization (asari viz) are separate and may have different resource profiles.
- One-time profiling on a fixed set of parameters does not capture sensitivity to parameter choices (e.g., lower m/z tolerance, higher SNR threshold) which may alter resource consumption.

## Evidence

- [other] How does asari's computational performance (wall-clock time and peak memory usage) scale with increasing numbers of LC-MS samples?: "How does asari's computational performance (wall-clock time and peak memory usage) scale with increasing numbers of LC-MS samples?"
- [other] Retrieve public mzML datasets from MetaboLights or MassIVE repositories; select or subsample test data to create cohorts of 10, 50, and 100+ samples. 2. Install asari from pip (v1.10+) with default parameters (5 ppm m/z tolerance, positive ionization mode). 3. For each cohort, execute asari process command and record wall-clock runtime and peak resident memory usage using system profiling tools (e.g., time command, psutil, or top). 4. Repeat runs 2–3 times per cohort to establish mean and standard deviation of timing and memory metrics.: "For each cohort, execute asari process command and record wall-clock runtime and peak resident memory usage using system profiling tools (e.g., time command, psutil, or top). 4. Repeat runs 2–3 times"
- [other] Tabulate results by sample count and plot wall-clock time and memory versus sample number to verify linear or near-linear scaling. 6. Compare observed throughput (samples/hour) and memory per sample to the claimed benchmark threshold for laptop-class hardware (≤16 GB RAM, single CPU core).: "Compare observed throughput (samples/hour) and memory per sample to the claimed benchmark threshold for laptop-class hardware (≤16 GB RAM, single CPU core)."
- [readme] Scalable, performance conscious, disciplined use of memory and CPU: "Scalable, performance conscious, disciplined use of memory and CPU"
- [other] Asari is designed as a scalable program with performance-conscious implementation prioritizing disciplined use of memory and CPU resources.: "Asari is designed as a scalable program with performance-conscious implementation prioritizing disciplined use of memory and CPU resources."
