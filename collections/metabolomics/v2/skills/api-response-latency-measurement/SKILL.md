---
name: api-response-latency-measurement
description: Use when when annotating .msp files with metadata from multiple external web services and you need to monitor which services are slow or unreliable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - MSMetaEnhancer
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - pytest
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
- 'fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb'
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.04494
  all_source_dois:
  - 10.21105/joss.04494
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# api-response-latency-measurement

## Summary

Measure and aggregate HTTP response latencies from external web services (CIR, CTS, PubChem, IDSM, BridgeDb) during asynchronous annotation runs in MSMetaEnhancer. This skill enables detection of service degradation and bottlenecks in metadata fetching workflows.

## When to use

When annotating .msp files with metadata from multiple external web services and you need to monitor which services are slow or unreliable. Apply this skill if you are running asynchronous annotation jobs and want to track per-service performance degradation over time or across multiple annotation runs.

## When NOT to use

- You are using only local, in-process converters (e.g., RDKit) with no external web service calls.
- Your annotation workflow is synchronous and does not require concurrent service monitoring.
- You only care about whether a service succeeded or failed, not timing performance.

## Inputs

- HTTP request/response pairs from external web services during annotation
- Asynchronous task logs containing request start and end timestamps
- Service endpoint URLs (CIR, CTS, PubChem, IDSM, BridgeDb)
- .msp file annotation job configuration with service list

## Outputs

- JSON report file with per-service latency metrics (mean, std, percentiles, min/max)
- Monitor object with aggregated latency state for each registered service
- Time-series latency logs for trend analysis across annotation runs

## How to apply

Design a Monitor class that registers all available web services (CIR, CTS, PubChem, IDSM, BridgeDb) and initializes per-service state trackers. Implement asynchronous health-check methods that probe each web converter's endpoint and record HTTP status codes and response times. Add error-logging callbacks to the WebConverter base class to capture request timing data and route it to Monitor for aggregation. At configurable intervals, compute per-service metrics including mean latency, latency percentiles, and latency trends. Serialize aggregated latency statistics to a JSON report file with timestamp and per-service summary, allowing downstream analysis of service performance patterns.

## Related tools

- **MSMetaEnhancer** (Host application that executes asynchronous annotation jobs and owns the Monitor class for latency tracking) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (External web service for chemical structure queries; response latency measured and aggregated by Monitor) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (External web service for chemical name/structure conversion; latency tracked per-request) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (External web service for chemical metadata; HTTP response times recorded and aggregated) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (External web service for chemical structure and name queries; latency monitored) — https://idsm.elixir-czech.cz/
- **BridgeDb** (External web service for identifier mapping; response latency measured per-call) — https://bridgedb.github.io/
- **pytest** (Testing framework to validate Monitor report structure, latency values, and service registration completeness)

## Examples

```
from MSMetaEnhancer.libs.monitor import Monitor; monitor = Monitor(services=['CIR', 'CTS', 'PubChem', 'IDSM', 'BridgeDb']); await monitor.run_health_checks(); report = monitor.aggregate_metrics(); monitor.serialize_report('service_latency_report.json')
```

## Evaluation signals

- JSON report file is valid JSON schema with 'timestamp', 'services', and 'overall_health' keys present
- All five registered services (CIR, CTS, PubChem, IDSM, BridgeDb) appear in the latency report
- Per-service latency metrics (mean, min, max, count) are non-negative numbers and mean ≥ min and mean ≤ max
- Latency values are within reasonable bounds for network requests (> 0ms, typically < 30,000ms for web APIs)
- Report timestamp is valid and recent relative to annotation job completion time

## Limitations

- Latency measurement reflects network round-trip time only; does not account for local processing overhead in annotation logic.
- Measurement accuracy depends on system clock precision and may be affected by high CPU contention on the host machine.
- Asynchronous scheduling overhead (task queue, event loop latency) is not separated from actual HTTP service latency.
- If a service is completely unavailable (connection refused), latency may be recorded as timeout duration rather than true response time.
- Latency aggregation at configurable intervals may miss transient spikes or brief service degradation between report windows.

## Evidence

- [other] MSMetaEnhancer fetches metadata from five external web services: CIR, CTS, PubChem, IDSM, and BridgeDb: "MSMetaEnhancer fetches metadata from five external web services: CIR, CTS, PubChem, IDSM, and BridgeDb, using an asynchronous implementation for the annotation process."
- [other] Implement asynchronous service health-check methods that probe each web converter's endpoint and record HTTP status codes and response times: "Implement asynchronous service health-check methods that probe each web converter's endpoint and record HTTP status codes and response times."
- [other] Create a status-aggregation method that computes per-service metrics (availability percentage, total errors, mean latency) at configurable intervals: "Create a status-aggregation method that computes per-service metrics (availability percentage, total errors, mean latency) at configurable intervals."
- [other] Serialize the aggregated status to a JSON report file with timestamp, per-service summary, and overall health state: "Serialize the aggregated status to a JSON report file with timestamp, per-service summary, and overall health state."
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
