---
name: mass-spectral-library-benchmark-execution
description: Use when you have access to the Flash Entropy Search implementation and want to validate that real-time spectral library querying achieves the reported timing and throughput metrics under the same library sizes, query parameters, and measurement methodology documented in the paper.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MSEntropy
  - Python
  - FlashEntropySearch
  - ms_entropy (MSEntropy Python package)
  - Entropy Search GUI
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-023-02012-9
  all_source_dois:
  - 10.1038/s41592-023-02012-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectral-library-benchmark-execution

## Summary

Execute benchmark workflows to measure query latency and throughput performance of Flash Entropy Search against large mass spectral libraries, then compare observed results against published benchmarks to verify reproducibility and algorithm efficiency claims.

## When to use

You have access to the Flash Entropy Search implementation and want to validate that real-time spectral library querying achieves the reported timing and throughput metrics under the same library sizes, query parameters, and measurement methodology documented in the paper.

## When NOT to use

- The library file is in an unsupported format (not .mgf, .msp, .mzML, or .lbm2).
- You only want to query a single spectrum pair rather than systematically measure performance across library scales.
- The hardware platform or OS differs drastically from those used in the original benchmark (Windows-2019, Ubuntu-20.04, MacOS-11) and you cannot account for expected performance scaling.

## Inputs

- mass spectral library file (`.mgf`, `.msp`, `.mzML`, or `.lbm2` format)
- query spectrum collection or benchmark test set
- benchmark configuration file specifying library sizes and query parameters
- Flash Entropy Search implementation (Python package or GUI binary)

## Outputs

- query latency measurements (time per search in milliseconds or seconds)
- throughput metrics (queries per second)
- benchmark comparison table (observed vs. reported results)
- reproducibility assessment report

## How to apply

Clone the FlashEntropySearch repository to access benchmark data, configuration files, and scripts. Review the benchmark configuration to identify tested library sizes, query parameter ranges (e.g., precursor m/z tolerance, peak matching rules), and the timing measurement methodology (e.g., wall-clock time per query, queries per second). Execute the benchmark workflow on the provided dataset or your own spectral library of comparable size using the Flash Entropy Search implementation (either via the Python `ms_entropy` package with `FlashEntropySearch.build_index()` and `FlashEntropySearch.search()`, or the GUI tool). Collect query latency (time per search) and throughput (queries per second) for each library configuration. Tabulate results and perform a side-by-side comparison against the published benchmark metrics; acceptable variance typically depends on hardware and OS differences, but consistency in ranking and order of magnitude indicates correct implementation.

## Related tools

- **FlashEntropySearch** (Source repository containing original benchmark data, scripts, and figures to be reproduced) — https://github.com/YuanyueLi/FlashEntropySearch
- **ms_entropy (MSEntropy Python package)** (Python implementation of Flash Entropy Search algorithm for building library indices and executing searches programmatically) — https://github.com/YuanyueLi/MSEntropy
- **Entropy Search GUI** (Standalone graphical tool for real-time spectral library searching; alternative to scripted benchmarking) — https://github.com/YuanyueLi/EntropySearch/releases

## Examples

```
from ms_entropy import FlashEntropySearch; entropy_search = FlashEntropySearch(); entropy_search.build_index(spectral_library); entropy_similarity = entropy_search.search(precursor_mz=query_spectrum['precursor_mz'], peaks=query_spectrum['peaks'])
```

## Evaluation signals

- Observed query latency and throughput values are within 10–20% of published benchmark results (accounting for hardware and OS variation).
- Throughput ranking and order of magnitude (e.g., thousands of queries per second) match the paper's reported performance characteristics.
- Results scale predictably with library size (e.g., throughput decreases as library grows, or remains constant under indexed search).
- Benchmark configuration parameters (library sizes, query tolerances, peak matching thresholds) are identical to or explicitly documented deviations from those in the original paper.
- No runtime errors, crashes, or timeouts occur during the full benchmark workflow on the target hardware.

## Limitations

- Benchmark results depend heavily on hardware (CPU, RAM, disk I/O) and operating system version; direct numerical comparison with published results requires similar system specifications.
- The software is built and tested specifically on Windows-2019, Ubuntu-20.04, and MacOS-11; performance on significantly older or newer OS versions may differ.
- Library size and spectral complexity significantly influence throughput; benchmarks should use libraries of comparable scale to the published study.
- No changelog is available in the repository, making it difficult to determine if benchmark scripts or data have been updated since publication.

## Evidence

- [readme] This repository contains the original source code, benchmark data, and figures for the manuscript: "This repository contains the original source code, benchmark data, and figures for the manuscript"
- [other] Review the benchmark configuration to identify library sizes, query parameters, and performance measurement methodology.: "Review the benchmark configuration to identify library sizes, query parameters, and performance measurement methodology"
- [other] Execute the benchmark workflow using the provided dataset and Flash Entropy Search implementation to measure query latency and throughput.: "Execute the benchmark workflow using the provided dataset and Flash Entropy Search implementation to measure query latency and throughput"
- [other] Tabulate results and compare against the reported benchmark metrics in the paper to verify reproducibility.: "Tabulate results and compare against the reported benchmark metrics in the paper to verify reproducibility"
- [readme] The software is build with GitHub actions in Windows-2019 (Windows 10), Ubuntu-20.04 (Focal Fossa), and MacOS-11 (Big Sur).: "The software is build with GitHub actions in Windows-2019 (Windows 10), Ubuntu-20.04 (Focal Fossa), and MacOS-11 (Big Sur)"
