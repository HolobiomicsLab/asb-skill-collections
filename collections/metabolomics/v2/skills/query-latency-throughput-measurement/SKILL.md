---
name: query-latency-throughput-measurement
description: Use when when you have implemented or obtained a spectral library search algorithm (such as Flash Entropy Search) and need to empirically verify its performance against reported benchmark metrics, or when comparing query performance across different library sizes, mass spectral file formats (.mgf, .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MSEntropy
  - Python
  - Flash Entropy Search (Python implementation)
  - Entropy Search (GUI)
  - FlashEntropySearch (benchmark repository)
  - Python time/timeit modules
derived_from:
- doi: 10.1038/s41592-023-02012-9
  title: Flash entropy search
evidence_spans:
- we provide a Python implementation of the algorithm in the `MSEntropy` repository
- Python implementation of the algorithm
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_flash_entropy_search_cq
    doi: 10.1038/s41592-023-02012-9
    title: Flash entropy search
  dedup_kept_from: coll_flash_entropy_search_cq
schema_version: 0.2.0
---

# Query Latency and Throughput Measurement for Spectral Library Search

## Summary

Measure the computational performance of spectral library query algorithms by executing benchmark workflows that capture query latency (time per query) and throughput (queries per second) across varied library sizes and configurations. This skill validates whether real-time querying claims are reproducible and quantifies performance scaling.

## When to use

When you have implemented or obtained a spectral library search algorithm (such as Flash Entropy Search) and need to empirically verify its performance against reported benchmark metrics, or when comparing query performance across different library sizes, mass spectral file formats (.mgf, .msp, .mzML, .lbm2), or precursor m/z range configurations.

## When NOT to use

- Query performance data is already published and your goal is only to *use* the algorithm (not validate it) — skip measurement and proceed directly to application.
- You are measuring on radically different hardware (e.g., GPU vs. CPU, cloud VM vs. local workstation) without normalizing for computational budget — benchmark numbers will not be comparable to published results.
- The library is too small (<100 spectra) or query set too small (<10 queries) to show statistical variance — results will be dominated by initialization and system noise rather than algorithmic throughput.

## Inputs

- Spectral library file (.mgf, .msp, .mzML, or .lbm2 format) with known number of indexed spectra
- Query spectrum dataset (peaks and precursor m/z values) or query spectrum file in compatible format
- Benchmark configuration metadata (library size, query parameters, expected latency/throughput ranges)
- Flash Entropy Search implementation (Python MSEntropy package or GUI Entropy Search binary)
- Hardware and software environment specification (CPU, RAM, OS, Python version)

## Outputs

- Timing measurements table: latency (milliseconds per query) and throughput (queries per second) for each library configuration
- Performance comparison matrix: measured vs. reported benchmark metrics with percent difference
- Scalability plot or trend data: latency/throughput as a function of library size
- Reproducibility verdict: whether reported metrics are reproduced within acceptable tolerance

## How to apply

First, clone the FlashEntropySearch repository and locate the benchmark data and scripts provided alongside the manuscript. Second, review the benchmark configuration metadata to identify the library sizes (number of spectra), query parameters (precursor m/z ranges, entropy similarity thresholds), and the performance measurement methodology (e.g., wall-clock time per query, batch query throughput). Third, execute the benchmark workflow using the provided dataset and the Flash Entropy Search implementation, ensuring consistent hardware and software environment (Python version, platform). Fourth, collect timing results by instrumenting the search phase—measure latency as time elapsed per individual query and aggregate throughput as queries successfully completed per second across the full library. Fifth, tabulate the results alongside reported benchmark metrics in the paper to verify reproducibility within acceptable margins (typically <10% variance for deterministic algorithms). Use Python's `time` module or `timeit` for fine-grained measurement, and record both mean and standard deviation across multiple runs to account for system variance.

## Related tools

- **Flash Entropy Search (Python implementation)** (Core algorithm for spectral library querying whose latency and throughput are measured) — https://github.com/YuanyueLi/MSEntropy
- **Entropy Search (GUI)** (Alternative interface for spectral library search; can be benchmarked for throughput if batch query interface available) — https://github.com/YuanyueLi/EntropySearch
- **FlashEntropySearch (benchmark repository)** (Provides benchmark data, scripts, and manuscript-reported reference metrics for validation) — https://github.com/YuanyueLi/FlashEntropySearch
- **Python time/timeit modules** (Low-level timing instrumentation for latency measurement)

## Examples

```
from ms_entropy import FlashEntropySearch; import time; entropy_search = FlashEntropySearch(); entropy_search.build_index(spectral_library); start = time.time(); results = [entropy_search.search(q['precursor_mz'], q['peaks']) for q in queries]; elapsed = time.time() - start; throughput = len(queries) / elapsed; print(f'Latency: {(elapsed/len(queries))*1000:.2f} ms/query, Throughput: {throughput:.1f} queries/sec')
```

## Evaluation signals

- Measured query latency (ms/query) falls within ±10% of reported benchmark metrics for the same library size and hardware class.
- Throughput (queries/second) scales inversely with library size in a predictable manner (e.g., linear or logarithmic degradation) consistent with the algorithm's published complexity.
- Standard deviation of latency across repeated runs on same library is <15% of mean, indicating measurement stability and repeatability.
- Query latency remains sub-second (or meets the paper's 'real-time' claim threshold) for large libraries (e.g., >1 million spectra) as reported in the manuscript.
- Batch throughput (multiple queries on same indexed library) is at least 1 order of magnitude faster than sequential single-query latency multiplied by query count, confirming index acceleration benefit.

## Limitations

- Benchmark results are hardware-dependent; CPU clock speed, RAM bandwidth, and I/O subsystem significantly affect absolute latency/throughput numbers. Comparisons are only valid across runs on identical or normalized hardware.
- No changelog documented in the FlashEntropySearch repository; version drift between benchmark scripts, code, and reported metrics may introduce discrepancies if repository has been updated post-publication.
- Benchmark scripts and data in FlashEntropySearch repository are provided as-is; if benchmark methodology differs from the paper's experimental setup (e.g., different precursor m/z filtering, entropy similarity threshold, or file format conversion), reported metrics may not be reproducible.
- Flash Entropy Search algorithm is only available in Python for real-time library search; GUI (Entropy Search) performance may differ due to overhead from GUI rendering, file I/O, and inter-process communication.
- Query performance is sensitive to library composition (e.g., number of unique precursor m/z clusters, peak sparsity); benchmarks on a specific library may not generalize to user-supplied libraries with different statistical properties.

## Evidence

- [other] Benchmark data and scripts: "This repository contains the original source code, benchmark data, and figures for the manuscript"
- [other] Query latency and throughput metrics: "Collect timing results and throughput values (queries per second or similar) for each tested library configuration"
- [other] Reported benchmark reproducibility verification: "Tabulate results and compare against the reported benchmark metrics in the paper to verify reproducibility"
- [other] Benchmark configuration review: "Review the benchmark configuration to identify library sizes, query parameters, and performance measurement methodology"
- [readme] Real-time querying claim: "Flash entropy search to query all mass spectral libraries in real time"
- [readme] Python implementation availability: "we provide a Python implementation of the algorithm in the `MSEntropy` repository"
