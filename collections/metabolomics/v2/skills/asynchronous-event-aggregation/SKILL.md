---
name: asynchronous-event-aggregation
description: Use when your workflow fetches data from multiple external web services (e.g., CIR, CTS, PubChem, IDSM, BridgeDb) asynchronously and you need to track which services are available, how often they fail, and their response latencies during a long-running annotation job.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
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
  - Python asyncio
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

# asynchronous-event-aggregation

## Summary

Design and implement asynchronous monitoring of multiple external web service endpoints to track availability, error rates, and latency, then aggregate metrics into a timestamped JSON health report. This skill is essential when annotation or data-fetching workflows depend on multiple remote services and require real-time visibility into service reliability without blocking the main annotation pipeline.

## When to use

Apply this skill when your workflow fetches data from multiple external web services (e.g., CIR, CTS, PubChem, IDSM, BridgeDb) asynchronously and you need to track which services are available, how often they fail, and their response latencies during a long-running annotation job. Use it to detect service degradation or outages that would otherwise cause silent failures in metadata enrichment.

## When NOT to use

- Input is a single synchronous service call or batch job with no external dependencies—use simple try/catch error handling instead.
- You have only one external service dependency—the overhead of a Monitor class is not justified; use direct health-check logic in the converter.
- The annotation job does not require real-time visibility into service health; deferred or post-hoc error reporting is acceptable.

## Inputs

- list of external web service endpoints (CIR, CTS, PubChem, IDSM, BridgeDb URLs)
- asynchronous annotation process with embedded WebConverter requests
- error callbacks from failed HTTP requests (timeouts, status codes, response exceptions)

## Outputs

- JSON status report file with timestamp, per-service availability percentage, error counts, and mean latency
- overall health state summary (all services up, degraded, or down)
- per-service metric objects (uptime, error_count, latency_ms)

## How to apply

Create a Monitor class that registers each external web service and initializes per-service state trackers for uptime, error counts, and latency. Implement asynchronous health-check methods that probe each service endpoint and record HTTP status codes and response times without blocking annotation tasks. Add error-logging callbacks to the WebConverter base class to capture failed requests (timeouts, invalid responses, API errors) and route them to Monitor for aggregation. At configurable intervals, compute per-service metrics (availability percentage, total errors, mean latency) and serialize the aggregated status to a JSON report file with timestamp, per-service summary, and overall health state. This approach allows the annotation process to proceed while health data accumulates in the background.

## Related tools

- **MSMetaEnhancer** (annotation framework that fetches metadata asynchronously from multiple web services; embeds the Monitor for tracking service availability during annotation runs) — https://github.com/RECETOX/MSMetaEnhancer
- **Python asyncio** (asynchronous runtime for non-blocking health-check probes and event loop integration)
- **pytest** (test framework for validating Monitor class behavior, report schema, and per-service metric aggregation)
- **CIR** (one of five external web services whose availability and latency are monitored) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (one of five external web services whose availability and latency are monitored) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (one of five external web services whose availability and latency are monitored) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (one of five external web services whose availability and latency are monitored) — https://idsm.elixir-czech.cz/
- **BridgeDb** (one of five external web services whose availability and latency are monitored) — https://bridgedb.github.io/

## Examples

```
from MSMetaEnhancer.libs.monitoring import Monitor; monitor = Monitor(['CIR', 'CTS', 'PubChem', 'IDSM', 'BridgeDb']); asyncio.run(monitor.start_health_checks(interval=60)); asyncio.run(app.annotate_spectra(services, jobs)); monitor.save_report('service_status.json')
```

## Evaluation signals

- Verify all five registered services (CIR, CTS, PubChem, IDSM, BridgeDb) are present in the JSON report with non-null availability and error metrics.
- Confirm per-service error counts and uptime counts are non-negative integers; availability percentage is between 0 and 100.
- Check that mean latency is recorded in milliseconds and is non-negative for each service.
- Validate the JSON report structure contains timestamp, per-service summary object, and overall health state (e.g., 'up', 'degraded', 'down').
- Assert that error callbacks from failed requests (timeouts, HTTP errors, API errors) are aggregated and reflected in the corresponding service's error count within the report.

## Limitations

- Monitor depends on external service availability; if all services are offline, the Monitor cannot probe them and will report zero uptime but will record that it attempted checks.
- Asynchronous health-check probes add latency to the annotation startup; probe frequency must be tuned to balance visibility with overhead.
- The JSON report is point-in-time; it reflects aggregated metrics since the last reset and does not persist historical trends across multiple annotation runs without explicit serialization logic.
- Error classification is based on HTTP status codes and exception types; subtle failures (e.g., incorrect but syntactically valid API responses) may not be detected by the Monitor and will not be logged as errors.

## Evidence

- [other] MSMetaEnhancer fetches metadata from five external web services: CIR, CTS, PubChem, IDSM, and BridgeDb, using an asynchronous implementation for the annotation process.: "MSMetaEnhancer fetches metadata from five external web services: CIR, CTS, PubChem, IDSM, and BridgeDb, using an asynchronous implementation for the annotation process."
- [other] Design the Monitor class to register available web services (CIR, CTS, PubChem, IDSM, BridgeDb) and initialize per-service state trackers for uptime, error counts, and latency.: "Design the Monitor class to register available web services (CIR, CTS, PubChem, IDSM, BridgeDb) and initialize per-service state trackers for uptime, error counts, and latency."
- [other] Implement asynchronous service health-check methods that probe each web converter's endpoint and record HTTP status codes and response times.: "Implement asynchronous service health-check methods that probe each web converter's endpoint and record HTTP status codes and response times."
- [other] Add error-logging callbacks to the WebConverter base class to capture failed requests (timeouts, invalid responses, API errors) and route them to Monitor for aggregation.: "Add error-logging callbacks to the WebConverter base class to capture failed requests (timeouts, invalid responses, API errors) and route them to Monitor for aggregation."
- [other] Create a status-aggregation method that computes per-service metrics (availability percentage, total errors, mean latency) at configurable intervals.: "Create a status-aggregation method that computes per-service metrics (availability percentage, total errors, mean latency) at configurable intervals."
- [other] Serialize the aggregated status to a JSON report file with timestamp, per-service summary, and overall health state.: "Serialize the aggregated status to a JSON report file with timestamp, per-service summary, and overall health state."
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
