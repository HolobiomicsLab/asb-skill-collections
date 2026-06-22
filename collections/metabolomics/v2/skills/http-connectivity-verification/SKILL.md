---
name: http-connectivity-verification
description: Use when you need to confirm that a documented web service URL is live and reachable before attempting to submit analysis jobs, download results, or integrate the service into an automated pipeline. Use it as a prerequisite check when the service documentation claims academic or public availability.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0224
  edam_topics:
  - http://edamontology.org/topic_0219
  tools:
  - molDiscovery
derived_from:
- doi: 10.1038/s41467-021-23986-0
  title: moldiscovery
evidence_spans:
- To test molDiscovery for academic users, please visit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moldiscovery
    doi: 10.1038/s41467-021-23986-0
    title: moldiscovery
  dedup_kept_from: coll_moldiscovery
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-021-23986-0
  all_source_dois:
  - 10.1038/s41467-021-23986-0
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# http-connectivity-verification

## Summary

Verify that a scientific web service or API endpoint is deployed, accessible, and responding with expected HTTP status codes. This skill validates service availability before downstream analysis tasks depend on it.

## When to use

Apply this skill when you need to confirm that a documented web service URL is live and reachable before attempting to submit analysis jobs, download results, or integrate the service into an automated pipeline. Use it as a prerequisite check when the service documentation claims academic or public availability.

## When NOT to use

- The service URL is not yet documented or is under embargo — verify publication status first.
- You only need to check whether a static file (e.g., GitHub README, published dataset) exists — use standard file-based checks instead.
- The endpoint requires authentication and you do not have valid credentials — extend the skill to include credential submission before status validation.

## Inputs

- Service URL (string; e.g., https://metabologenomic.cbd.cs.cmu.edu/)
- HTTP method (GET; optional timeout threshold in seconds)

## Outputs

- HTTP status code (integer; 2xx/3xx/4xx/5xx)
- Response headers (dictionary)
- Request latency (milliseconds)
- Timestamp of check (ISO 8601)
- Deployment-check report (structured log or JSON)

## How to apply

Send an HTTP GET request to the documented service URL using a standard HTTP client (curl, requests library, etc.). Capture the HTTP response status code, response headers, and request latency. Verify that the status code falls in the 2xx success range (typically 200 OK). Log the response metadata (timestamp, latency, content-type) and compare against known-good baseline responses to detect degradation. Document the results in a deployment-check report for audit and troubleshooting.

## Related tools

- **molDiscovery** (Academic web service for metabologenomic analysis whose availability and response status is being verified) — https://github.com/mohimanilab/molDiscovery

## Examples

```
curl -w '\nStatus: %{http_code}\nLatency: %{time_total}s\n' -o /dev/null -s https://metabologenomic.cbd.cs.cmu.edu/
```

## Evaluation signals

- HTTP status code is 200 or other 2xx success code; non-2xx codes (4xx, 5xx) indicate service unavailable or misconfigured endpoint.
- Response latency is below documented or expected threshold (e.g., <5 seconds); unusually high latency may signal network or server degradation.
- Content-Type header is present and matches expected type (e.g., 'text/html', 'application/json'); missing or unexpected content-type may indicate server misconfiguration.
- Repeated checks over time show consistent 2xx responses; sporadic 5xx responses may indicate transient outages.
- Deployment-check report is generated with timestamp and logged to persistent storage for audit trail and trend analysis.

## Limitations

- HTTP GET checks only verify basic reachability; they do not validate that the service's functional endpoints or computational methods are working correctly.
- A 200 status code does not guarantee the service will accept job submissions or return correct results; functional testing requires end-to-end workflow validation.
- Network timeouts, DNS failures, or firewalls may block access from specific geographic regions or networks, limiting the generalizability of a single check.
- Some services may require specific headers or authentication tokens; a bare GET may succeed but masked API endpoints may require additional verification.

## Evidence

- [other] Is the molDiscovery academic web service deployed and accessible at the documented URL?: "Is the molDiscovery academic web service deployed and accessible at the documented URL?"
- [other] Send HTTP GET request to https://metabologenomic.cbd.cs.cmu.edu/ using curl or standard HTTP client. Capture HTTP response status code and response headers. Verify HTTP status code is 200 or other success code (2xx range). Log response metadata (timestamp, latency, content-type) and save to deployment-check report.: "Send HTTP GET request to https://metabologenomic.cbd.cs.cmu.edu/ using curl or standard HTTP client. Capture HTTP response status code and response headers. Verify HTTP status code is 200 or other"
- [readme] To test molDiscovery for academic users, please visit : https://metabologenomic.cbd.cs.cmu.edu/: "To test molDiscovery for academic users, please visit : https://metabologenomic.cbd.cs.cmu.edu/"
