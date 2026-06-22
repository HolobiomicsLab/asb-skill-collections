---
name: web-service-health-monitoring
description: Use when your annotation pipeline depends on multiple external web converters and you need to diagnose why annotation jobs are failing, slow, or incomplete. Use it if you observe missing metadata fields in output .
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# web-service-health-monitoring

## Summary

Monitor the availability, error state, and performance of external web services (e.g., CIR, CTS, PubChem, IDSM, BridgeDb) that are called asynchronously during annotation runs. This skill tracks uptime, error counts, latency, and produces aggregated health-status reports to validate service reliability during metadata enrichment workflows.

## When to use

Apply this skill when your annotation pipeline depends on multiple external web converters and you need to diagnose why annotation jobs are failing, slow, or incomplete. Use it if you observe missing metadata fields in output .msp files, request timeouts, or sporadic API errors—the health report will reveal which services are degraded and whether the annotation process should retry, fall back, or alert the user.

## When NOT to use

- You are running a local, offline annotation pipeline with no external service calls—health monitoring is unnecessary.
- You only need ad-hoc troubleshooting of a single failed request; a full monitoring framework is over-engineered.
- Service uptime and latency are not relevant to your research question (e.g., you only care about final metadata correctness, not why it took time to compute).

## Inputs

- list of external web service endpoints (URLs for CIR, CTS, PubChem, IDSM, BridgeDb)
- asynchronous request/response logs from WebConverter instances during annotation runs
- configurable health-check probe interval (seconds)

## Outputs

- JSON health-status report file with timestamp, per-service metrics (availability %, error count, mean latency), and overall health state
- aggregated service state object in memory (for runtime inspection and decision-making)

## How to apply

Design a Monitor class that registers all external web services (CIR, CTS, PubChem, IDSM, BridgeDb) and initializes per-service state trackers for uptime, error counts, and latency measurements. Implement asynchronous health-check methods that probe each service endpoint at regular intervals, recording HTTP status codes and response times. Hook error-logging callbacks into the WebConverter base class to capture failed requests (timeouts, invalid responses, API errors) and route them to Monitor for aggregation. Periodically compute per-service metrics (availability percentage, total errors, mean latency) and serialize the aggregated status to a JSON report file with a timestamp, per-service summary, and overall health state. Validate the report by confirming all registered services are present, that error and uptime counts are non-negative, and that latency values are reasonable (e.g., within expected bounds for each service).

## Related tools

- **MSMetaEnhancer** (annotation application that calls external web converters; Monitor integrates into its WebConverter base class to log and track service health) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (external web service providing chemical structure lookups; subject to health monitoring) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (external web service for chemical structure conversion; subject to health monitoring) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (external web service for chemical metadata retrieval; subject to health monitoring) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (external web service for metabolite and chemical structure data; subject to health monitoring) — https://idsm.elixir-czech.cz/
- **BridgeDb** (external web service for biological identifier mapping; subject to health monitoring) — https://bridgedb.github.io/
- **pytest** (testing framework used to validate Monitor implementation, report structure, and error-handling logic)
- **Python** (implementation language for Monitor class and asynchronous health-check routines)

## Examples

```
from MSMetaEnhancer.libs.monitoring import Monitor; monitor = Monitor(services=['CIR', 'CTS', 'PubChem', 'IDSM', 'BridgeDb']); asyncio.run(monitor.health_check_loop(interval_seconds=30)); monitor.write_report('service_health.json')
```

## Evaluation signals

- JSON report is valid and well-formed; all required keys (timestamp, per-service summary, overall health state) are present.
- All five registered services (CIR, CTS, PubChem, IDSM, BridgeDb) appear in the report with complete metrics (availability %, error count, mean latency).
- Error and uptime counts are non-negative integers; availability percentages are in [0, 100]; latency values are non-negative and within plausible range (e.g., < 60 seconds for HTTP calls).
- Health-check probes successfully reach all service endpoints within the configured timeout; HTTP status codes (200, 503, timeout) are correctly recorded.
- Report timestamps increment monotonically across consecutive aggregation intervals; metrics trend correctly when services go down or recover (uptime % decreases after failures; error counts increment).

## Limitations

- Health monitoring reflects only the availability of the service endpoint itself; it does not guarantee that the service will return correct or complete metadata for a given chemical query.
- Asynchronous health checks add overhead to the annotation pipeline; frequent probing of all five services may slow down annotation runs if probe interval is too short.
- External service APIs and response formats may change without notice, invalidating the health-check logic or the error-logging callbacks; the Monitor must be maintained in sync with upstream API changes.
- Network latency and occasional transient failures (e.g., single timeout in a burst of requests) may be reported as service degradation even if the service is globally healthy; short-term local network issues can pollute the health report.

## Evidence

- [other] Monitor class to register available web services (CIR, CTS, PubChem, IDSM, BridgeDb) and initialize per-service state trackers for uptime, error counts, and latency: "Design the Monitor class to register available web services (CIR, CTS, PubChem, IDSM, BridgeDb) and initialize per-service state trackers for uptime, error counts, and latency."
- [other] asynchronous service health-check methods that probe each web converter's endpoint and record HTTP status codes and response times: "Implement asynchronous service health-check methods that probe each web converter's endpoint and record HTTP status codes and response times."
- [other] error-logging callbacks to the WebConverter base class to capture failed requests (timeouts, invalid responses, API errors) and route them to Monitor for aggregation: "Add error-logging callbacks to the WebConverter base class to capture failed requests (timeouts, invalid responses, API errors) and route them to Monitor for aggregation."
- [other] status-aggregation method that computes per-service metrics (availability percentage, total errors, mean latency) at configurable intervals: "Create a status-aggregation method that computes per-service metrics (availability percentage, total errors, mean latency) at configurable intervals."
- [other] Serialize the aggregated status to a JSON report file with timestamp, per-service summary, and overall health state: "Serialize the aggregated status to a JSON report file with timestamp, per-service summary, and overall health state."
- [other] MSMetaEnhancer fetches metadata from five external web services: CIR, CTS, PubChem, IDSM, and BridgeDb, using an asynchronous implementation for the annotation process: "MSMetaEnhancer fetches metadata from five external web services: CIR, CTS, PubChem, IDSM, and BridgeDb, using an asynchronous implementation for the annotation process."
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
