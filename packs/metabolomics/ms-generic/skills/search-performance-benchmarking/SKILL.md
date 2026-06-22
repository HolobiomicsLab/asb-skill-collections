---
name: search-performance-benchmarking
description: Use when when you have two or more implementations of a spectral search tool (e.g., MASST vs. MASST+) and need to quantify whether claimed performance improvements (e.g., '100-fold speedup') are reproducible.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - GNPS
  - MASST
  - MASST+
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1038/s41587-023-01985-4
  title: MASST
evidence_spans:
- MASST+ is publicly available as a web service on GNPS
- Like MASST, MASST+ is publicly available as a web service on GNPS.
- MASST+ is an improvement on GNPS Mass Spectrometry Search Tool (MASST)
- MASST+ is an improvement on GNPS Mass Spectrometry Search Tool
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

# search-performance-benchmarking

## Summary

Benchmark and compare the search performance of spectral library query tools by executing identical query sets on baseline and improved systems, measuring wall-clock time, resource consumption, and speedup ratios. This skill validates whether algorithmic or infrastructure improvements achieve claimed performance gains at scale.

## When to use

When you have two or more implementations of a spectral search tool (e.g., MASST vs. MASST+) and need to quantify whether claimed performance improvements (e.g., '100-fold speedup') are reproducible. Use this skill to establish empirical evidence of speedup under controlled conditions with identical database and parameter settings.

## When NOT to use

- Query sets are not identical or not executed in the same order on both systems — uncontrolled variance will obscure true speedup.
- Database indices, parameters (mass tolerance, scoring), or data splits differ between baseline and candidate — results will reflect configuration differences, not algorithmic improvement.
- Only a single or very small query set is used — variance and statistical confidence will be too low to claim reproducible speedup.

## Inputs

- query mass spectrum set (MGF or USI format)
- baseline spectral database (indexed or reference)
- candidate spectral database (identically configured)
- mass tolerance parameter (ppm or Da)
- spectral similarity scoring method (e.g., cosine, dot product)

## Outputs

- wall-clock search time for baseline system (seconds or minutes)
- wall-clock search time for candidate system (seconds or minutes)
- speedup ratio (scalar, unitless)
- per-query timing statistics (mean, std dev, confidence interval)
- aggregate search completion status and result count validation
- resource consumption log (CPU, memory utilization)

## How to apply

Obtain or prepare a representative query set (e.g., metabolite spectra from public data or a curated benchmark set). Configure both the baseline system (e.g., MASST) and the candidate system (e.g., MASST+) with identical database indices, mass tolerance, and scoring parameters. Execute the entire query set on the baseline system using a single continuous session, recording total wall-clock elapsed time and per-query timing. Repeat identically on the candidate system. Calculate the speedup ratio as (baseline_time ÷ candidate_time) and report with per-query and aggregate statistics (mean, variance, confidence intervals). Document resource consumption (CPU, memory) during both runs to contextualize the speedup claim.

## Related tools

- **MASST** (baseline spectral search system for performance comparison) — https://masst.ucsd.edu/
- **MASST+** (candidate improved spectral search system to benchmark against MASST) — https://github.com/mohimanilab/MASSTplus
- **GNPS** (public web service and database hosting for MASST+ and spectral library data) — https://gnps.ucsd.edu/

## Evaluation signals

- Speedup ratio equals or exceeds the claimed threshold (e.g., ~100-fold reduction asserted in abstract); report actual ratio with confidence interval.
- Per-query timing distributions are consistent (low variance or monotonic trend) on both systems, indicating stable and repeatable performance.
- Result count and rank order of spectral similarity hits are identical between baseline and candidate, confirming correctness is preserved during optimization.
- Resource consumption (CPU, memory) during candidate search is proportional to the speedup — e.g., 100-fold time reduction should correlate with equivalent or lower resource usage.
- Benchmark completes on billion-scale database without timeout or resource exhaustion, validating scalability claim stated in finding.

## Limitations

- Speedup measurements are sensitive to hardware (CPU model, memory bandwidth, I/O subsystem) and system load; benchmark should be repeated on identical or similar hardware to ensure reproducibility.
- Wall-clock time includes database load and initialization overhead; if baseline system loads database slower, speedup ratio may overstate algorithmic improvement.
- Query set must be representative of real-world usage; a carefully curated benchmark set may not reflect performance on diverse or pathological queries in production.
- Comparisons are valid only when both systems query the same database state (version, indexing, clustering); schema changes or data drift between runs invalidate the benchmark.

## Evidence

- [other] Execute the query set on the baseline MASST system and record total wall-clock search time: "Execute the query set on the baseline MASST system and record total wall-clock search time."
- [other] Execute the same query set on MASST+ and record total wall-clock search time: "Execute the same query set on MASST+ and record total wall-clock search time."
- [other] Calculate the speedup ratio and verify it equals approximately 100-fold: "Calculate the speedup ratio (MASST time ÷ MASST+ time) and verify it equals approximately 100-fold."
- [intro] reducing the search time by two orders of magnitude: "reducing the search time by two orders of magnitude"
- [readme] querying against databases of billions of mass spectra, which was not feasible with MASST: "It is capable of querying against databases of billions of mass spectra, which was not feasible with MASST"
