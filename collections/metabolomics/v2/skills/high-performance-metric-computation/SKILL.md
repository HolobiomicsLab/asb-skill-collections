---
name: high-performance-metric-computation
description: Use when you have implemented or are evaluating an algorithmic or system optimization (e.g., MASST+) that claims to reduce execution time, and you need to quantify and statistically validate the speedup against a baseline system (e.g., MASST).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
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
---

# high-performance-metric-computation

## Summary

Quantify search-time performance improvements by executing identical query sets on baseline and optimized systems, recording wall-clock execution times, and computing speedup ratios with statistical confidence intervals. This skill validates whether algorithmic or system-level optimizations (e.g., indexing, data structure changes) achieve predicted performance gains in metabolomics mass spectrometry search.

## When to use

Apply this skill when you have implemented or are evaluating an algorithmic or system optimization (e.g., MASST+) that claims to reduce execution time, and you need to quantify and statistically validate the speedup against a baseline system (e.g., MASST). Use it when reproducible timing comparisons are critical for claims of efficiency or scalability improvements.

## When NOT to use

- The query set is not representative of real-world usage patterns — timing results will not generalize.
- The baseline and optimized systems use different databases, parameter settings, or hardware — comparison is confounded.
- You only need to measure absolute throughput (queries per unit time) rather than relative speedup — use simpler throughput metrics instead.

## Inputs

- Query set (e.g., spectrum USI identifiers or spectral data)
- Baseline system configuration (e.g., MASST with identical database)
- Optimized system configuration (e.g., MASST+ with identical database)
- Identical parameter settings (e.g., mass tolerance, scoring thresholds)
- Hardware/environment specification

## Outputs

- Per-query wall-clock execution times (baseline and optimized)
- Aggregate execution time (baseline and optimized)
- Speedup ratio (baseline time ÷ optimized time)
- Confidence intervals or run variance statistics
- Tabulated timing report with statistical summaries

## How to apply

Obtain a representative query set and configure both the baseline system and optimized system with identical database contents, parameter settings, and hardware environment. Execute the full query set on the baseline system and record total wall-clock search time; repeat on the optimized system. Calculate the speedup ratio as (baseline time ÷ optimized time) and report it alongside per-query timing statistics. Compute confidence intervals or run variance to account for system noise; report aggregate statistics in a tabulated format. The rationale is that controlled, paired execution isolates the effect of the optimization while statistical bounds demonstrate reproducibility and robustness.

## Related tools

- **MASST** (Baseline mass spectrometry search system against which optimized performance is measured) — https://masst.ucsd.edu/
- **MASST+** (Optimized mass spectrometry search system whose speedup is quantified relative to MASST) — https://github.com/mohimanilab/MASSTplus
- **GNPS** (Platform providing public access to both MASST and MASST+ as web services and shared database) — https://gnps.ucsd.edu/

## Examples

```
# Execute query set on MASST and record time; repeat with MASST+; compute speedup
time_masst=$(time (for query in $(cat queries.txt); do masst_search --query $query --db gnps_db; done) 2>&1 | grep real)
time_masst_plus=$(time (for query in $(cat queries.txt); do masst_plus_search --query $query --db gnps_db; done) 2>&1 | grep real)
speedup=$((time_masst / time_masst_plus)); echo "Speedup: $speedup-fold"
```

## Evaluation signals

- Speedup ratio equals or exceeds the claimed improvement factor (e.g., ~100-fold for MASST+ versus MASST).
- Confidence intervals or run variance are reported and do not overlap between systems, indicating statistically significant difference.
- Per-query timing statistics are consistent with aggregate statistics (no outliers that dominate the sum).
- Identical database and parameter settings are verified before and after each system's execution.
- Query set size and composition are documented and representative of intended use cases.

## Limitations

- Timing measurements are sensitive to hardware configuration, system load, and I/O contention; results may not transfer to different computational environments.
- Wall-clock time conflates algorithmic efficiency with system-level factors (e.g., caching, memory bandwidth); speedup may not isolate algorithm alone.
- Query set composition and size affect measured speedup; results generalize only to query patterns similar to those in the test set.
- Confidence intervals require multiple independent runs; single-run measurements provide no variance estimate.

## Evidence

- [other] Execute the query set on the baseline MASST system and record total wall-clock search time. Execute the same query set on MASST+ and record total wall-clock search time. Calculate the speedup ratio (MASST time ÷ MASST+ time) and verify it equals approximately 100-fold.: "Execute the query set on the baseline MASST system and record total wall-clock search time. Execute the same query set on MASST+ and record total wall-clock search time. Calculate the speedup ratio"
- [other] Tabulate and report per-query and aggregate timing statistics with confidence intervals or run variance.: "Tabulate and report per-query and aggregate timing statistics with confidence intervals or run variance."
- [other] Obtain the query set and configure both MASST and MASST+ systems with identical database and parameter settings.: "Obtain the query set and configure both MASST and MASST+ systems with identical database and parameter settings."
- [readme] MASST+ reduces search time by two orders of magnitude compared to MASST: "MASST+ provides fast and error tolerant search of metabolomics mass spectrometry data while reducing the search time by two orders of magnitude."
