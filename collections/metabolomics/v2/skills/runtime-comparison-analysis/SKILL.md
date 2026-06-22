---
name: runtime-comparison-analysis
description: Use when when a new version or variant of a tool claims performance improvements over a prior version (e.g., MASST+ vs. MASST), and you need empirical evidence that the claimed speedup (e.g., ~100-fold reduction in search time) is real, reproducible, and quantifiable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - MASST
  - GNPS
  - MASST+
derived_from:
- doi: 10.1038/s41587-023-01985-4
  title: MASST
evidence_spans:
- MASST+ is an improvement on GNPS Mass Spectrometry Search Tool (MASST)
- MASST+ is an improvement on GNPS Mass Spectrometry Search Tool
- MASST+ is publicly available as a web service on GNPS
- Like MASST, MASST+ is publicly available as a web service on GNPS.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_masst_3_cq
    doi: 10.1038/s41587-023-01985-4
    title: MASST
  dedup_kept_from: coll_masst_3_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-023-01985-4
  all_source_dois:
  - 10.1038/s41587-023-01985-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# runtime-comparison-analysis

## Summary

A benchmarking skill that compares wall-clock execution times of two or more implementations (baseline vs. optimized) on identical query workloads to quantify speedup ratios and verify claimed performance improvements. This skill is essential for validating algorithmic or system-level optimizations in mass spectrometry search tools and other compute-intensive workflows.

## When to use

When a new version or variant of a tool claims performance improvements over a prior version (e.g., MASST+ vs. MASST), and you need empirical evidence that the claimed speedup (e.g., ~100-fold reduction in search time) is real, reproducible, and quantifiable. Apply this skill when you have access to both implementations, identical parameter configurations, and a representative query set that reflects real-world usage patterns.

## When NOT to use

- You do not have access to both the baseline and optimized implementations, or cannot configure them identically.
- The query set is not representative of real-world usage patterns, or is too small to yield stable timing estimates.
- The systems run on fundamentally different hardware, operating systems, or network conditions, making direct wall-clock comparison invalid.

## Inputs

- query set (representative set of spectra or queries for the tool)
- baseline tool implementation (e.g., original MASST binary/server)
- optimized tool implementation (e.g., MASST+ binary/server)
- database configuration (identical for both systems)
- parameter settings (identical for both systems)

## Outputs

- per-query timing statistics (wall-clock time for each query)
- aggregate timing statistics (total time across query set)
- speedup ratio (baseline time ÷ optimized time)
- confidence intervals or run variance estimate
- tabulated timing report

## How to apply

Obtain or define a representative query set that spans the typical use cases of the tool. Configure both the baseline and optimized implementations with identical database, parameter settings, and hardware environment. Execute the query set sequentially on the baseline system, recording total wall-clock time; repeat for the optimized version. Calculate the speedup ratio as (baseline time ÷ optimized time). Repeat runs across multiple trials to capture variance and compute confidence intervals. Report per-query and aggregate timing statistics to verify the claimed performance improvement and detect any edge cases where speedup is anomalous.

## Related tools

- **MASST** (baseline mass spectrometry search implementation for timing comparison) — https://masst.ucsd.edu/
- **MASST+** (optimized mass spectrometry search implementation being benchmarked for speedup) — https://github.com/mohimanilab/MASSTplus
- **GNPS** (host platform for both MASST and MASST+ web services; provides query access and database) — https://gnps.ucsd.edu/

## Evaluation signals

- Speedup ratio is close to the claimed value (e.g., approximately 100-fold for MASST+ vs. MASST); verify it falls within a defensible margin (e.g., 90–110-fold or stated confidence interval).
- Confidence intervals or standard deviation across multiple runs are narrow relative to the speedup magnitude, indicating stable and reproducible performance.
- Per-query timing statistics show consistent speedup across the query set (no queries regress significantly), not just aggregate improvement masking slow outliers.
- Wall-clock times are measured end-to-end with identical overhead (network latency, I/O, database access patterns) for both implementations, ruling out measurement artifacts.
- Query sets complete successfully on both systems without errors or timeouts, and both return semantically equivalent results (e.g., same top-k matches).

## Limitations

- Wall-clock time measurements are sensitive to system load, network congestion (for web services), and hardware variability; controlled environments and multiple trials are needed for reliability.
- Speedup is only valid for the specific query set and database used in the benchmark; performance may differ on other workloads or larger/smaller databases.
- The comparison does not isolate which algorithmic or system-level changes drive the speedup (e.g., indexing, vectorization, parallelization), limiting insights into generalizability.
- MASST+ is designed to query databases of billions of mass spectra; this comparison may not reflect performance scaling to such extreme database sizes if the benchmark uses smaller datasets.

## Evidence

- [intro] confirming the ~100-fold speedup: "MASST+ reduces search time by two orders of magnitude compared to MASST, confirming the ~100-fold speedup."
- [other] workflow for runtime comparison: "1. Obtain the query set and configure both MASST and MASST+ systems with identical database and parameter settings. 2. Execute the query set on the baseline MASST system and record total wall-clock"
- [readme] core performance claim: "MASST+ provides fast and error tolerant search of metabolomics mass spectrometry data while reducing the search time by two orders of magnitude."
- [readme] scale of optimization: "It is capable of querying against databases of billions of mass spectra, which was not feasible with MASST."
