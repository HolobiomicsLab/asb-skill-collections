---
name: performance-benchmarking-computational-systems
description: Use when you have implemented or reconstructed a performance-critical computational module (e.g., an expeditious querying engine, a database lookup accelerator, or a real-time matching algorithm) and need to validate that it achieves claimed throughput targets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - XCMS
  - CAMERA
  - LipidIN
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification.'
- 'CAMERA: an'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidin_cq
    doi: 10.1038/s41467-025-59683-5
    title: LipidIN
  dedup_kept_from: coll_lipidin_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-59683-5
  all_source_dois:
  - 10.1038/s41467-025-59683-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Performance Benchmarking of Computational Systems

## Summary

Measure and validate the throughput, speed, and resource efficiency of specialized computational modules (e.g., spectral query engines) against standardized benchmark datasets and wall-clock metrics. This skill is essential for verifying that optimized algorithms meet claimed performance targets in high-throughput applications like mass spectrometry analysis.

## When to use

Apply this skill when you have implemented or reconstructed a performance-critical computational module (e.g., an expeditious querying engine, a database lookup accelerator, or a real-time matching algorithm) and need to validate that it achieves claimed throughput targets. Trigger conditions include: (1) the module claims to process a large number of operations (e.g., billions of queries) in a short time window (e.g., < 1 second), (2) you have access to a standardized benchmark dataset of experimental inputs (e.g., experimental MS/MS spectra), and (3) you can measure wall-clock execution time on controlled hardware.

## When NOT to use

- The module has not yet been implemented or compiled; benchmarking pre-release or pseudocode is not meaningful.
- You do not have access to a representative standardized benchmark dataset; ad-hoc or toy inputs will not reflect real-world performance and will not validate claimed throughput.
- Hardware resources are highly variable or uncontrolled (e.g., shared cluster nodes, virtualized environments with no CPU affinity); throughput measurements will be confounded and not reproducible.

## Inputs

- Compiled or executable computational module (e.g., C++ binary, R/Python function)
- Large indexed reference library or lookup table (e.g., hierarchical lipid fragmentation library with 168+ million entries)
- Standardized benchmark dataset of experimental inputs (e.g., MS/MS spectra in .rda or matrix format)
- Hardware specification sheet or system info (CPU model, core count, RAM, OS)

## Outputs

- Throughput metric (queries/second or operations/second)
- Wall-clock execution time (seconds)
- Comparison table: claimed vs. measured throughput
- Performance trace or profiling log (optional)
- Reproducibility report including hardware, library load time, and input size

## How to apply

Load your performance-critical module and a large, indexed reference library (e.g., 168.6 million lipid fragmentation entries organized hierarchically by chain composition and double-bond locations) into an optimized in-memory data structure designed for rapid lookup. Execute the module on a standardized benchmark dataset of experimental spectra, recording total number of operations performed and wall-clock time elapsed. Compute throughput as (operations / time), compare against claimed targets, and record hardware specifications (CPU model, core count, RAM, operating system). If throughput falls short, profile bottlenecks using timing instrumentation or profilers to identify whether the issue is I/O-bound, CPU-bound, or memory-bound. Document actual vs. claimed metrics, benchmark reproducibility, and sensitivity to input size or parameter tuning.

## Related tools

- **XCMS** (Mass spectrometry peak processing and alignment prior to expeditious querying module input)
- **CAMERA** (Compound spectra extraction and annotation as preprocessing step before spectral querying)
- **LipidIN** (Reference system implementing expeditious querying module against 168.6 million lipid fragmentation library) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
# After loading LipidIN EQ module and benchmark spectra, measure throughput on the LCI-processed .rda file:
source('EQ.r')
start_time <- Sys.time()
EQ(filename='QC_POS1.rda', ppm1=5, ppm2=10, ESI='p')
end_time <- Sys.time()
queries_performed <- nrow(experimental_spectra) * nrow(library_entries)
throughput <- queries_performed / as.numeric(end_time - start_time)
print(paste('Throughput:', throughput, 'queries/second'))
```

## Evaluation signals

- Measured throughput (queries/second) meets or exceeds claimed target (e.g., ~70 billion queries in < 1 second for LipidIN EQ module).
- Wall-clock execution time on benchmark dataset is consistent across repeated runs on the same hardware, with coefficient of variation < 5%.
- Throughput scales predictably with input size: doubling query count should roughly double execution time (linear scaling).
- Memory usage remains stable and does not exhaust available RAM; profiling shows library is held in-memory and not repeatedly reloaded.
- Hardware specifications and library configuration are documented; benchmark is reproducible by independent implementation on equivalent hardware.

## Limitations

- Throughput is highly dependent on hardware (CPU generation, core count, RAM bandwidth, cache hierarchy); claims must specify target hardware or show performance on multiple platforms.
- In-memory library load time is not included in query throughput metrics; total end-to-end latency may be higher than reported query throughput if the module is used in a single-query or online setting.
- Benchmark dataset composition (spectral complexity, m/z range, intensity distribution) can affect query time; performance measured on one instrument or sample type may not generalize to others.
- Throughput measurement is sensitive to OS background processes, memory fragmentation, and CPU frequency scaling; measurements should be taken under controlled conditions (dedicated hardware, OS idle, CPU frequency pinned).
- The README notes data format conversion (e.g., mzML to .rda) takes ~2 minutes for the LCI module; this overhead is separate from EQ module query throughput but affects total pipeline latency.

## Evidence

- [other] LipidIN implements an expeditious querying module that performs spectral matching against a 168.6 million lipid fragmentation hierarchical library, achieving throughput of approximately 70 billion spectral queries in less than 1 second.: "expeditious querying module that performs spectral matching against a 168.6 million lipid fragmentation hierarchical library, achieving throughput of approximately 70 billion spectral queries in less"
- [other] Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid spectral similarity lookup.: "Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid"
- [other] Execute the query engine on a standardized benchmark dataset of experimental spectra and measure wall-clock time and query throughput (queries/second).: "Execute the query engine on a standardized benchmark dataset of experimental spectra and measure wall-clock time and query throughput (queries/second)"
- [other] Validate that the system achieves approximately 70 billion queries in under 1 second, recording actual throughput metrics.: "Validate that the system achieves approximately 70 billion queries in under 1 second, recording actual throughput metrics"
- [readme] All benchmark tests were performed on a personal computer with 13th Gen Intel® Core™ i7-13700F × 16-Core Processor, 64 GB memory, and installed with Windows11 operation system: "All benchmark tests were performed on a personal computer with 13th Gen Intel® Core™ i7-13700F × 16-Core Processor, 64 GB memory, and installed with Windows11 operation system"
