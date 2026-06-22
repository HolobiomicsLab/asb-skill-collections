---
name: http-endpoint-connectivity-verification
description: Use when after deploying a web service in a Docker container with port mapping (e.g., -p 8888:8080), verify that the application is running and responding to HTTP requests at the mapped endpoint.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - MetFrag
  - Docker
  - Tomcat
  - curl or wget
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans:
- This container packages the MetFrag (https://github.com/ipb-halle/MetFragRelaunched) webapp
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metfrag_cq
    doi: 10.1186/s13321-016-0115-9
    title: MetFrag
  dedup_kept_from: coll_metfrag_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-016-0115-9
  all_source_dois:
  - 10.1186/s13321-016-0115-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# HTTP endpoint connectivity verification

## Summary

Verify that a containerized web application (e.g., MetFrag webapp deployed in Docker) is accessible and responsive at its exposed HTTP endpoint. This skill confirms correct port mapping, service initialization, and endpoint availability before downstream use.

## When to use

After deploying a web service in a Docker container with port mapping (e.g., -p 8888:8080), verify that the application is running and responding to HTTP requests at the mapped endpoint. Use this skill when you need to confirm that Tomcat or another application server has initialized, the mapped port is accessible from the host, and the service returns valid responses.

## When NOT to use

- The application is already confirmed to be running and responding; verification is redundant.
- No HTTP interface is exposed or expected (e.g., batch processing or CLI-only tools).
- The container is deployed in a private or air-gapped network with no external connectivity verification possible.

## Inputs

- Docker container ID or name (running with port mapping)
- HTTP endpoint URL (scheme, host, port, and optional path)
- Expected response content signature or status code

## Outputs

- HTTP response status code (e.g., 200, 503)
- Response body (HTML, JSON, or text)
- Connectivity status report (success or failure with diagnostics)
- Container startup logs (if captured for debugging)

## How to apply

Issue a GET request to the exposed HTTP endpoint (e.g., http://localhost:8888/MetFragWeb) and examine the response status and content. A successful verification requires a 200 HTTP status code or valid webpage content (e.g., HTML response body). If the initial request fails, wait for the Tomcat application server to complete initialization (typically 5–30 seconds after container startup) and retry. Document the response status, response headers, and whether the expected webapp interface or landing page appears. This validates that the port mapping is correctly configured, the container networking is functional, and the application is ready to serve requests.

## Related tools

- **Docker** (Container runtime and port mapping configuration; enables isolated deployment and port exposure (-p flag) of the web service)
- **Tomcat** (Application server inside the container that hosts and serves the MetFrag webapp; initializes and binds to port 8080 inside the container)
- **MetFrag** (Web application under verification; deployed in the container and served via Tomcat on the mapped HTTP endpoint) — https://github.com/ipb-halle/MetFragRelaunched
- **curl or wget** (HTTP client utility to issue GET requests and inspect response status and headers)

## Examples

```
curl -i http://localhost:8888/MetFragWeb && echo 'Connectivity verified' || echo 'Endpoint unreachable'
```

## Evaluation signals

- HTTP response status code is 200 (OK) or other 2xx success code, not 5xx server error or 3xx redirect loops.
- Response body contains expected content (e.g., HTML markup, JSON structure) matching the deployed application interface.
- No timeout or connection refused errors; socket connection to host:port succeeds within expected latency.
- Response headers include valid Content-Type and do not indicate service unavailable or maintenance mode.
- Repeated requests (after 5–10 second intervals if initial attempt fails) show consistent success, confirming stable service readiness rather than transient startup glitch.

## Limitations

- Verification assumes the Docker container is running and has been started with correct port mapping; does not diagnose container startup failures or image pull errors.
- Response verification only confirms HTTP connectivity and basic server response; does not validate that the application logic or database connections are functional.
- If Tomcat or the application server takes longer than expected to initialize (e.g., due to large database loads or slow disk I/O), early verification attempts may fail; retry logic and configurable timeouts are necessary.
- No changelog or version history is tracked in the MetFrag repository, making it difficult to confirm whether endpoint structure or response format has changed between versions.

## Evidence

- [other] Verify HTTP connectivity by making a GET request to the exposed endpoint and confirming a 200 response or valid webpage content.: "Verify HTTP connectivity by making a GET request to the exposed endpoint and confirming a 200 response or valid webpage content."
- [other] The MetFrag webapp is deployed by running the ipbhalle/metfragweb Docker container with port mapping (-p 8888:8080) to expose the internal Tomcat port 8080 to the host port 8888, making the application accessible at the specified HTTP endpoint.: "port mapping (-p 8888:8080) to expose the internal Tomcat port 8080 to the host port 8888, making the application accessible at the specified HTTP endpoint"
- [other] Wait for the Tomcat application server to initialize and the MetFrag webapp to become ready.: "Wait for the Tomcat application server to initialize and the MetFrag webapp to become ready."
- [readme] This container packages the MetFrag webapp and some text databases based on the latest official tomcat docker container.: "This container packages the MetFrag webapp and some text databases based on the latest official tomcat docker container."
- [readme] after the successful build Tomcat web server runs on port 8080; MetFragWeb can be accessed via pointing to http://localhost:8080/index.xhtml in the web browser: "after the successful build Tomcat web server runs on port 8080; MetFragWeb can be accessed via pointing to http://localhost:8080/index.xhtml"
