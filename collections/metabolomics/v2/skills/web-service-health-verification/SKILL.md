---
name: web-service-health-verification
description: Use when after deploying a containerized web application (e.g., via `docker
  run`), before proceeding to functional testing or integration. Use this skill to
  confirm the application server (Tomcat, etc.) has fully initialized and the web
  service is listening on the mapped port and URL path.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3557
  tools:
  - Tomcat
  - Docker
  - curl or HTTP client
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans:
- latest official tomcat docker container
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metfrag
    doi: 10.1186/s13321-016-0115-9
    title: MetFrag
  dedup_kept_from: coll_metfrag
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

# web-service-health-verification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify that a containerized web application is accessible and operational by querying its HTTP endpoint and confirming a successful response code. This skill validates that the deployment pipeline—from container launch through application server initialization—has completed successfully.

## When to use

After deploying a containerized web application (e.g., via `docker run`), before proceeding to functional testing or integration. Use this skill to confirm the application server (Tomcat, etc.) has fully initialized and the web service is listening on the mapped port and URL path.

## When NOT to use

- The application is not containerized or has already been deployed to a running server—use standard web service monitoring tools instead.
- You need to verify the application's business logic or functional correctness—this skill only confirms HTTP reachability and a 200 status, not feature behavior.
- The web service is intentionally offline or in a maintenance state—a 200 response is not expected.

## Inputs

- Containerized web application image (e.g., Docker image URI: ipbhalle/metfragweb)
- Port mapping configuration (e.g., host_port:container_port, e.g., 8888:8080)
- Expected URL path (e.g., /MetFragWeb or /index.xhtml)

## Outputs

- HTTP 200 status code confirmation
- Accessibility confirmation of the web service at the mapped host:port/path
- Implicit verification of container runtime, application server initialization, and webapp deployment

## How to apply

Launch the container with documented port mapping, then poll the web service endpoint via HTTP GET. Wait for the application server (Tomcat) to fully initialize—typically 5–30 seconds depending on the image and resource constraints. Query the documented default URL path (e.g., http://localhost:8888/MetFragWeb for the MetFrag webapp) and verify the response status code is 200 (OK). If initialization has not completed, retry after a brief delay. Success indicates the container is running, the application server has bound to the mapped port, and the webapp is deployed and ready to serve requests.

## Related tools

- **Docker** (Container runtime to launch the web application image with port mapping)
- **Tomcat** (Application server packaged in the container; handles HTTP requests and webapp deployment) — https://hub.docker.com/_/tomcat
- **curl or HTTP client** (Tool to issue HTTP GET request to the deployed webapp endpoint and check response status code)

## Examples

```
curl -I http://localhost:8888/MetFragWeb && echo 'Webapp is accessible' || echo 'Webapp is not responding'
```

## Evaluation signals

- HTTP GET request to the mapped endpoint (e.g., http://localhost:8888/MetFragWeb) returns status code 200 (OK)
- HTTP response headers and body content are non-empty and match expected webapp structure (e.g., HTML, JSF response)
- Multiple sequential requests to the endpoint all return 200, confirming service stability rather than transient error
- Latency of the HTTP response is within reasonable bounds (< 5 seconds), indicating no resource exhaustion in the container
- Application server logs (visible via `docker logs container_id`) show successful initialization messages (e.g., Tomcat startup completed) before the health check succeeds

## Limitations

- A 200 status does not guarantee functional correctness—the webapp may be deployed but contain logic errors or database connection failures that only appear during interactive use.
- Container health depends on host resource availability (CPU, memory); if the host is overloaded, the application server may fail to initialize within a reasonable timeframe, causing this skill to time out.
- The skill assumes the documented port mapping and URL path are correct; misconfiguration (e.g., wrong WEBPREFIX environment variable) will cause the endpoint to be unreachable.
- Some web applications serve a 200 response even when partially initialized; a 200 status does not guarantee all internal services (databases, external APIs) are ready.
- HTTPS endpoints require additional setup (certificate, TLS configuration); this skill as described assumes HTTP.

## Evidence

- [other] Query http://localhost:8888/MetFragWeb via HTTP to verify the webapp is accessible and returns a 200 status code.: "Query http://localhost:8888/MetFragWeb via HTTP to verify the webapp is accessible and returns a 200 status code."
- [other] Wait for the Tomcat application server to fully initialize within the container.: "Wait for the Tomcat application server to fully initialize within the container."
- [other] Run the container using the docker run command, mapping the appropriate port to localhost:8888.: "Run the container using the docker run command, mapping the appropriate port to localhost:8888."
- [readme] This container packages the MetFrag (https://github.com/ipb-halle/MetFragRelaunched) webapp and some text databases based on the latest official tomcat docker container.: "This container packages the MetFrag webapp and some text databases based on the latest official tomcat docker container."
- [readme] after the successful build Tomcat web server runs on port 8080: "after the successful build Tomcat web server runs on port 8080"
