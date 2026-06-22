---
name: error-state-tracking-across-microservices
description: Use when building or maintaining a system that fetches metadata from multiple independent external web services and needs to diagnose why annotation runs fail or slow down. Use it specifically when you need to distinguish between service-level failures (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MSMetaEnhancer
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - pytest
  - Python
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# error-state-tracking-across-microservices

## Summary

Monitor the availability, error state, and latency of multiple external web services (CIR, CTS, PubChem, IDSM, BridgeDb) used during asynchronous annotation runs in MSMetaEnhancer by implementing a centralized Monitor class that aggregates per-service health metrics and produces timestamped JSON reports.

## When to use

Apply this skill when building or maintaining a system that fetches metadata from multiple independent external web services and needs to diagnose why annotation runs fail or slow down. Use it specifically when you need to distinguish between service-level failures (e.g., one converter is down) versus client-side or logic errors, or when you want to audit the availability and performance of dependent services over time.

## When NOT to use

- Input is a single, monolithic converter or local library (not a distributed set of external web services).
- Real-time response is required but asynchronous health-check latency is unacceptable.
- The external services do not expose HTTP endpoints or status codes (e.g., file-based or in-process converters).

## Inputs

- web service endpoint URLs for CIR, CTS, PubChem, IDSM, and BridgeDb
- HTTP request/response logs from WebConverter instances during annotation runs
- health-check probe configuration (interval, timeout thresholds)

## Outputs

- JSON status report with timestamp, per-service metrics (availability %, total errors, mean latency), and overall health state
- structured error logs routed from WebConverter to Monitor
- per-service state tracker objects (uptime, error counts, latency records)

## How to apply

Design a Monitor class that registers all five web services (CIR, CTS, PubChem, IDSM, BridgeDb) and initializes per-service state trackers recording uptime, error counts, and latency. Implement asynchronous health-check methods that probe each web converter's endpoint and record HTTP status codes and response times at configurable intervals. Attach error-logging callbacks to the WebConverter base class to capture failed requests (timeouts, invalid responses, API errors) and route them to the Monitor for aggregation. At each reporting interval, compute per-service metrics including availability percentage (uptime / total checks), total error count, and mean latency. Serialize the aggregated status to a JSON report file with timestamp, per-service summary (e.g., availability %, errors, mean latency in ms), and overall health state (pass/fail). The rationale is that asynchronous annotation relies on multiple external dependencies; without centralized error tracking, individual converter failures remain invisible until annotation completion, making debugging difficult.

## Related tools

- **MSMetaEnhancer** (Parent application that executes asynchronous annotation jobs and integrates the Monitor class to track health of dependent web converters) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (One of five external web services whose availability and error state are monitored) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (One of five external web services whose availability and error state are monitored) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (One of five external web services whose availability and error state are monitored) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (One of five external web services whose availability and error state are monitored) — https://idsm.elixir-czech.cz/
- **BridgeDb** (One of five external web services whose availability and error state are monitored) — https://bridgedb.github.io/
- **Python** (Language used to implement the Monitor class and asynchronous health-check methods)
- **pytest** (Testing framework used to validate report structure, service registration, and error count invariants)

## Examples

```
monitor = Monitor(services=['CIR', 'CTS', 'PubChem', 'IDSM', 'BridgeDb']); monitor.register_error_callback(web_converter); asyncio.run(monitor.health_check(interval=60)); monitor.aggregate_metrics(); monitor.export_report('service_status.json')
```

## Evaluation signals

- Verify that the JSON report file contains all five registered services (CIR, CTS, PubChem, IDSM, BridgeDb) in the per-service summary.
- Confirm that availability percentage is between 0 and 100 and that total error count and mean latency are non-negative integers or floats.
- Check that the report timestamp is present and that health-check probes have been executed at the expected interval.
- Validate that error counts logged to Monitor from WebConverter callbacks match the errors recorded in per-service state trackers.
- Confirm that a service marked as unavailable (e.g., 0% availability) has zero successful responses in its latency record.

## Limitations

- Monitor health checks depend on network connectivity; transient network partitions or DNS failures may incorrectly report service unavailability.
- Per-service metrics (availability %, latency) are aggregated at fixed intervals and do not capture real-time fluctuations or per-request granularity.
- The health-check mechanism does not validate the semantic correctness of converter responses; a service may return a 200 status code but invalid or malformed data.
- Availability percentage is computed from health-check probes, not from actual annotation requests; probe failures may not correlate with annotation job failures.

## Evidence

- [other] MSMetaEnhancer fetches metadata from five external web services: CIR, CTS, PubChem, IDSM, and BridgeDb, using an asynchronous implementation for the annotation process.: "MSMetaEnhancer fetches metadata from five external web services: CIR, CTS, PubChem, IDSM, and BridgeDb, using an asynchronous implementation for the annotation process."
- [other] Implement asynchronous service health-check methods that probe each web converter's endpoint and record HTTP status codes and response times.: "Implement asynchronous service health-check methods that probe each web converter's endpoint and record HTTP status codes and response times."
- [other] Add error-logging callbacks to the WebConverter base class to capture failed requests (timeouts, invalid responses, API errors) and route them to Monitor for aggregation.: "Add error-logging callbacks to the WebConverter base class to capture failed requests (timeouts, invalid responses, API errors) and route them to Monitor for aggregation."
- [other] Create a status-aggregation method that computes per-service metrics (availability percentage, total errors, mean latency) at configurable intervals.: "Create a status-aggregation method that computes per-service metrics (availability percentage, total errors, mean latency) at configurable intervals."
- [other] Serialize the aggregated status to a JSON report file with timestamp, per-service summary, and overall health state.: "Serialize the aggregated status to a JSON report file with timestamp, per-service summary, and overall health state."
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
