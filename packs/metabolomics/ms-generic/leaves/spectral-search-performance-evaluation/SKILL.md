---
name: spectral-search-performance-evaluation
description: Use when when you have implemented or obtained a spectral library search
  tool (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Entropy Search
  - MSEntropy
  - Python
  - FlashEntropySearch
  - Entropy Search (GUI)
  - MSEntropy (Python package)
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-023-02012-9
  title: Flash entropy search
evidence_spans:
- a standalone software with a Graphical User Interface (GUI) named Entropy Search
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-023-02012-9
  all_source_dois:
  - 10.1038/s41592-023-02012-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Search Performance Evaluation

## Summary

Measure and validate query latency, throughput, and accuracy metrics for spectral library search algorithms against reported benchmarks. This skill enables reproducible assessment of real-time spectral search performance across varying library sizes and query parameters.

## When to use

When you have implemented or obtained a spectral library search tool (e.g., Flash Entropy Search) and need to verify that its query performance (latency, throughput measured in queries per second) matches the reported benchmark results in the manuscript, or when comparing performance across different library configurations, precursor m/z filtering strategies, or entropy similarity scoring modes.

## When NOT to use

- You do not have access to the original benchmark dataset or scripts—reproduction requires the exact configuration and spectral library versions used in the manuscript.
- Your hardware differs drastically from the benchmark platform (e.g., embedded device vs. high-performance computing cluster); absolute timing values will not be comparable without normalization.
- You only need to confirm the algorithm produces correct similarity scores, not evaluate throughput—use unit tests or accuracy validation instead.

## Inputs

- FlashEntropySearch repository (source code and benchmark scripts)
- Spectral library in .mgf, .msp, .mzML, or .lbm2 format
- Query spectrum dataset (same format as library)
- Benchmark configuration file (library sizes, query parameters, performance measurement settings)

## Outputs

- Timing results table (query latency in milliseconds per library size)
- Throughput metrics (queries per second for each configuration)
- Performance comparison report (actual vs. reported benchmark values)
- System configuration log (CPU, RAM, OS details)

## How to apply

Clone the FlashEntropySearch repository and locate its benchmark data and scripts directory. Review the benchmark configuration to identify the tested library sizes, query parameter settings (e.g., precursor m/z tolerance windows, peak intensity thresholds), and performance measurement methodology. Execute the benchmark workflow using the provided dataset and Flash Entropy Search implementation, collecting raw timing results (query latency in milliseconds) and throughput values (queries per second or similar). Tabulate results for each tested library configuration (e.g., library sizes from thousands to millions of spectra). Compare your collected metrics against the reported benchmark values in the paper using relative error calculations; investigate discrepancies >5–10% by checking system configuration, library preprocessing steps, and whether all query filtering modes (identity search, neutral loss search, open search, hybrid search) were executed. Document the system specifications (CPU, RAM, OS) since performance is hardware-dependent.

## Related tools

- **FlashEntropySearch** (Provides benchmark data, scripts, and the reference implementation for measuring real-time spectral library query performance) — https://github.com/YuanyueLi/FlashEntropySearch
- **Entropy Search (GUI)** (Standalone software tool for executing spectral searches; used to measure query latency and throughput in a production-like environment) — https://github.com/YuanyueLi/EntropySearch/releases
- **MSEntropy (Python package)** (Python implementation of Flash Entropy Search algorithm; enables programmatic access to search methods and performance profiling) — https://github.com/YuanyueLi/MSEntropy

## Examples

```
from ms_entropy import FlashEntropySearch
import time
entropy_search = FlashEntropySearch()
entropy_search.build_index(spectral_library)
start = time.time()
for query in query_spectra:
    similarity = entropy_search.search(precursor_mz=query['precursor_mz'], peaks=query['peaks'])
latency_ms = (time.time() - start) / len(query_spectra) * 1000
throughput_qps = len(query_spectra) / (time.time() - start)
```

## Evaluation signals

- Collected query latency values for each library size fall within ±5–10% of reported benchmark timings, accounting for hardware variation.
- Throughput (queries/second) scales inversely with library size in the expected manner; throughput does not degrade non-linearly.
- All four entropy similarity search modes (identity_search, neutral_loss_search, open_search, hybrid_search) complete successfully and return non-empty similarity arrays with values in [0, 1].
- Total benchmark execution time is reasonable (completes within 1–2 hours for standard library configurations); pathological slowness indicates misconfiguration or missing index optimization.
- System specifications (CPU, RAM, OS) are recorded and match or exceed the reported benchmark platform to ensure fair comparison.

## Limitations

- Benchmark reproducibility is sensitive to spectral library preprocessing (peak normalization, noise filtering); even minor library modifications will alter throughput.
- Performance is highly hardware-dependent (CPU architecture, cache size, RAM speed); absolute timing values are meaningful only on identical or comparable systems.
- The benchmark dataset may be proprietary or require manual curation; if the original library is unavailable, results cannot be directly compared to published values.
- No changelog is available in the repository, making it difficult to track how code changes over time and whether performance regressions have been introduced.

## Evidence

- [other] The repository contains benchmark data and scripts for Flash Entropy Search performance: "This repository contains the original source code, benchmark data, and figures for the manuscript"
- [other] Workflow requires identifying library sizes, query parameters, and performance measurement methodology: "Review the benchmark configuration to identify library sizes, query parameters, and performance measurement methodology"
- [other] Metrics collected are query latency and throughput (queries per second): "Collect timing results and throughput values (queries per second or similar) for each tested library configuration"
- [other] Results must be compared against reported benchmark metrics in the paper: "Tabulate results and compare against the reported benchmark metrics in the paper to verify reproducibility"
- [intro] Flash Entropy Search algorithm enables real-time querying of spectral libraries: "Flash entropy search to query all mass spectral libraries in real time"
- [readme] Search results include multiple entropy similarity modes: "{'hybrid_search': array([...], dtype=float32), 'identity_search': array([...], dtype=float32), 'neutral_loss_search': array([...], dtype=float32), 'open_search': array([...], dtype=float32)}"
