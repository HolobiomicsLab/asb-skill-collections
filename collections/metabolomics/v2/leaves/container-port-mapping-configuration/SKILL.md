---
name: container-port-mapping-configuration
description: Use when you need to deploy a containerized web application (such as
  MetFrag webapp on Tomcat) and make it accessible at a specific HTTP endpoint on
  the host machine. Use this skill when you have a Docker image with an internal service
  listening on a known port (e.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - MetFrag
  - Docker
  - Tomcat
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans:
- This container packages the MetFrag (https://github.com/ipb-halle/MetFragRelaunched)
  webapp
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

# container-port-mapping-configuration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure Docker port mapping to expose containerized web services (e.g., Tomcat application servers) to a host network interface at a specified HTTP endpoint. This skill bridges the container's internal service port to an externally accessible host port, enabling network connectivity verification and downstream integration.

## When to use

You need to deploy a containerized web application (such as MetFrag webapp on Tomcat) and make it accessible at a specific HTTP endpoint on the host machine. Use this skill when you have a Docker image with an internal service listening on a known port (e.g., 8080 for Tomcat) and want to expose it to a different or the same port on the host (e.g., 8888).

## When NOT to use

- The application is not containerized or does not run in Docker
- You need to expose multiple services on the same host port (port conflicts)
- The container's internal service port is not known or documented

## Inputs

- Docker image name and tag (e.g., ipbhalle/metfragweb)
- container internal port number (e.g., 8080)
- desired host port number (e.g., 8888)
- optional environment variables (e.g., JAVA_OPTS, WEBPREFIX)
- optional volume mount paths (e.g., settings.properties file path)

## Outputs

- running Docker container instance with exposed HTTP endpoint
- HTTP endpoint URL accessible from host (e.g., http://localhost:8888/MetFragWeb)
- container startup logs confirming service readiness
- HTTP response verification (200 status or valid page content)

## How to apply

Use Docker's `-p` (port mapping) flag in the `docker run` command with the syntax `-p <host_port>:<container_port>` to map the internal application server port to the host port. For MetFrag webapp, the container runs Tomcat internally on port 8080; map this to a host port (e.g., 8888) using `-p 8888:8080`. After launching the container, allow time for the application server (Tomcat) to initialize before testing. Verify HTTP connectivity by making a GET request to the exposed endpoint (e.g., http://localhost:8888/MetFragWeb) and confirm a 200 response or valid webpage content is returned. Document the container startup logs to confirm the service is ready and the endpoint is accessible.

## Related tools

- **Docker** (container runtime and orchestration platform used to run the containerized MetFrag webapp and manage port mapping) — https://www.docker.com/
- **Tomcat** (embedded application server inside the container running on internal port 8080, serving the MetFrag webapp to the mapped host port) — https://hub.docker.com/_/tomcat
- **MetFrag** (mass spectrometry analysis webapp packaged in the Docker container and accessible via the mapped HTTP endpoint) — https://github.com/ipb-halle/MetFragRelaunched

## Examples

```
docker run -it --rm -p 8888:8080 ipbhalle/metfragweb
```

## Evaluation signals

- HTTP GET request to the mapped endpoint (http://localhost:<host_port>/<webapp_path>) returns HTTP 200 status code
- HTTP response contains valid HTML content or expected MetFrag webapp interface
- Docker container process remains running without errors after initialization period
- Container startup logs show Tomcat server initialized successfully and listening on the internal port
- Network connectivity is confirmed from the host machine to the container endpoint without timeout or connection refused errors

## Limitations

- Port mapping requires the host port to be available and not already in use by another service
- Network connectivity may be restricted by host firewall rules; firewall configuration may be necessary for external access
- Performance and latency depend on the host system's network stack and container resource allocation
- Multiple simultaneous port mappings to the same container require distinct host port numbers

## Evidence

- [readme] Docker port mapping flag and syntax specification: "docker run -it --rm -p 8888:8080 ipbhalle/metfragweb"
- [intro] Port mapping purpose and Tomcat internal port: "The MetFrag webapp is deployed by running the ipbhalle/metfragweb Docker container with port mapping (-p 8888:8080) to expose the internal Tomcat port 8080 to the host port 8888"
- [intro] Verification method via HTTP request: "Verify HTTP connectivity by making a GET request to the exposed endpoint and confirming a 200 response or valid webpage content"
- [readme] Endpoint accessibility example: "Run MetFrag at http://localhost:8888/MetFragWeb"
- [intro] Container server initialization requirement: "Wait for the Tomcat application server to initialize and the MetFrag webapp to become ready"
