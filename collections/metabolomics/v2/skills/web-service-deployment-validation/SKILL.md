---
name: web-service-deployment-validation
description: Use when when you need to confirm that a publicly hosted academic web service (such as molDiscovery) is live and responding at a documented endpoint URL, or when troubleshooting access issues reported by end users.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0092
  tools:
  - molDiscovery
  - curl
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
---

# web-service-deployment-validation

## Summary

Verify that a scientific web service is deployed and accessible at its documented URL by performing HTTP health checks and capturing response metadata. This skill confirms service availability for downstream users before proceeding with integration or documentation updates.

## When to use

When you need to confirm that a publicly hosted academic web service (such as molDiscovery) is live and responding at a documented endpoint URL, or when troubleshooting access issues reported by end users.

## When NOT to use

- The web service URL is known to be private or behind authentication and no valid credentials are available.
- The endpoint is expected to be unavailable (e.g., during scheduled maintenance), making a positive 2xx response the wrong indicator.
- You need to validate the functional correctness of the service (e.g., that it returns correct predictions); this skill only confirms reachability.

## Inputs

- web service URL (documented or claimed)
- HTTP client tool (curl, requests, or equivalent)

## Outputs

- HTTP status code (integer)
- response headers (dictionary or text)
- request/response timestamp (ISO 8601 or Unix epoch)
- network latency in milliseconds
- content-type header value
- deployment check report (log file or JSON document)

## How to apply

Send an HTTP GET request to the documented web service URL using a standard HTTP client (curl, requests library, or similar). Capture the HTTP response status code, response headers, and request/response timing metadata. Verify that the status code falls in the 2xx success range (e.g., 200 OK). Log the response timestamp, latency, and content-type header to a deployment check report for audit and troubleshooting purposes. Compare the actual endpoint URL against the documented URL to ensure consistency.

## Related tools

- **molDiscovery** (target web service whose deployment status and endpoint accessibility is validated) — https://github.com/mohimanilab/molDiscovery
- **curl** (HTTP client used to send GET request and capture response)

## Examples

```
curl -i -w '\nLatency: %{time_total}s\n' https://metabologenomic.cbd.cs.cmu.edu/ 2>&1 | tee deployment-check-$(date +%Y%m%d_%H%M%S).log
```

## Evaluation signals

- HTTP response status code is in the 2xx range (e.g., 200 OK), not 4xx or 5xx.
- Response headers are present and include expected fields such as content-type.
- Request/response latency is within acceptable range (e.g., < 5 seconds for a health check).
- Timestamp is current (matches the time the check was performed).
- Endpoint URL in the response or redirect matches the documented URL, with no unexpected redirects to alternative hosts.

## Limitations

- HTTP status 200 indicates reachability and basic server responsiveness but does not validate that the service performs its intended scientific function correctly.
- Network intermittency or regional blocking may cause false negatives; repeated checks over time are recommended for reliability.
- Some web services may require authentication headers or API keys; a bare GET request will not validate authenticated endpoints.

## Evidence

- [other] Is the molDiscovery academic web service deployed and accessible at the documented URL?: "research_question: Is the molDiscovery academic web service deployed and accessible at the documented URL?"
- [other] Send HTTP GET request to https://metabologenomic.cbd.cs.cmu.edu/ using curl or standard HTTP client. Capture HTTP response status code and response headers. Verify HTTP status code is 200 or other success code (2xx range).: "Send HTTP GET request to https://metabologenomic.cbd.cs.cmu.edu/ using curl or standard HTTP client. Capture HTTP response status code and response headers. Verify HTTP status code is 200 or other"
- [other] Log response metadata (timestamp, latency, content-type) and save to deployment-check report.: "Log response metadata (timestamp, latency, content-type) and save to deployment-check report."
- [other] The molDiscovery tool is made available for academic users via a publicly hosted web service at https://metabologenomic.cbd.cs.cmu.edu/.: "The molDiscovery tool is made available for academic users via a publicly hosted web service at https://metabologenomic.cbd.cs.cmu.edu/."
- [readme] To test molDiscovery for academic users, please visit : https://metabologenomic.cbd.cs.cmu.edu/: "To test molDiscovery for academic users, please visit : https://metabologenomic.cbd.cs.cmu.edu/"
