---
name: json-structured-reporting
description: Use when you need to persist and communicate the health status of multiple external web services queried during an annotation run.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0089
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer
schema_version: 0.2.0
---

# json-structured-reporting

## Summary

Serialize aggregated system state metrics (service availability, error counts, latency) into a time-stamped JSON report file with structured per-service summaries and overall health state. This skill enables reproducible monitoring and auditing of external service dependencies during annotation workflows.

## When to use

Apply this skill when you need to persist and communicate the health status of multiple external web services queried during an annotation run. Specifically, use it after aggregating per-service metrics (uptime percentage, error counts, mean latency) to create an auditable record suitable for debugging integration failures, documenting service reliability during a batch job, or alerting downstream systems to degraded availability.

## When NOT to use

- The annotation run involves only local, in-process converters (e.g., RDKit) with no external web service calls; no monitoring data will exist.
- Service health metrics need to be streamed in real-time rather than aggregated and persisted at the end of a run.
- The target environment cannot write to the file system or requires binary output formats other than JSON.

## Inputs

- Per-service state tracker objects (uptime counts, error counts, latency samples)
- HTTP status code and response time records from WebConverter instances
- List of registered service names (CIR, CTS, PubChem, IDSM, BridgeDb)
- Report output file path

## Outputs

- JSON report file with timestamp, per-service availability/error/latency metrics, and overall health state
- Structured report object in memory (dict or JSON-serializable object) before writing to disk

## How to apply

After collecting HTTP status codes, response times, and error events from all registered web services (CIR, CTS, PubChem, IDSM, BridgeDb), compute per-service summary statistics: availability percentage (successful requests / total requests), total error count, and mean latency. Construct a JSON object containing a top-level timestamp, an overall health state (inferred from per-service availability thresholds), and a nested dictionary mapping each service name to its metrics. Write this structure to a JSON file at a configurable path, ensuring the file is valid JSON and all services registered at runtime are present in the report. This creates a machine-readable audit trail that can be parsed by downstream validation or alerting pipelines.

## Related tools

- **MSMetaEnhancer** (Parent application framework that orchestrates annotation and calls the Monitor class to serialize health reports) — https://github.com/RECETOX/MSMetaEnhancer
- **pytest** (Testing framework used to validate report structure, verify all registered services are present, and confirm error and uptime counts are non-negative)
- **Python** (Language in which the Monitor class and JSON serialization are implemented)

## Examples

```
from MSMetaEnhancer import Monitor; monitor = Monitor(); monitor.register_services(['CIR', 'CTS', 'PubChem', 'IDSM', 'BridgeDb']); monitor.aggregate_status(); monitor.serialize_report('service_status.json')
```

## Evaluation signals

- Report file is valid JSON and can be parsed without errors.
- All five registered services (CIR, CTS, PubChem, IDSM, BridgeDb) appear as keys in the per-service summary.
- Availability percentage for each service is between 0 and 100, error count is non-negative, and mean latency is a positive number.
- Report contains a top-level timestamp field in ISO 8601 or Unix epoch format that matches the aggregation time window.
- Overall health state is correctly inferred from per-service availability metrics (e.g., marked 'degraded' if any service has availability < configurable threshold).

## Limitations

- JSON serialization assumes all metrics (availability, error counts, latencies) are numeric and JSON-compatible; custom objects or numpy arrays must be converted to primitive types first.
- Report aggregation is a point-in-time snapshot; it does not capture time-series data or historical trends across multiple runs without manual archiving or external storage.
- File write operations may fail silently if the target directory does not exist or lacks write permissions; explicit error handling and validation of file paths before report generation is recommended.

## Evidence

- [other] Serialize the aggregated status to a JSON report file with timestamp, per-service summary, and overall health state.: "Serialize the aggregated status to a JSON report file with timestamp, per-service summary, and overall health state."
- [other] Create a status-aggregation method that computes per-service metrics (availability percentage, total errors, mean latency) at configurable intervals.: "Create a status-aggregation method that computes per-service metrics (availability percentage, total errors, mean latency) at configurable intervals."
- [other] Validate the report structure, verify all registered services are present, and confirm error and uptime counts are non-negative.: "Validate the report structure, verify all registered services are present, and confirm error and uptime counts are non-negative."
- [other] MSMetaEnhancer fetches metadata from five external web services: CIR, CTS, PubChem, IDSM, and BridgeDb, using an asynchronous implementation for the annotation process.: "MSMetaEnhancer fetches metadata from five external web services: CIR, CTS, PubChem, IDSM, and BridgeDb, using an asynchronous implementation for the annotation process."
