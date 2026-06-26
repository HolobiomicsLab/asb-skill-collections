---
name: port-mapping-configuration
description: Use when when you have a containerized web application with a fixed internal
  port (e.g., Tomcat on port 8080) and need to expose it on a different localhost
  port for local access or testing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3593
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Tomcat
  - Docker
  - ipbhalle/metfragweb
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

# port-mapping-configuration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure Docker port mapping to expose containerized web applications at a specified localhost port, enabling HTTP access to the service. This skill is essential when deploying containerized scientific software (such as MetFrag webapp) that runs on a fixed internal port but must be accessible at a user-specified external port.

## When to use

When you have a containerized web application with a fixed internal port (e.g., Tomcat on port 8080) and need to expose it on a different localhost port for local access or testing. Specifically applicable when validating that a Docker container successfully launches and serves an HTTP endpoint at a documented URL.

## When NOT to use

- When the container requires bidirectional communication (socket/streaming) beyond simple HTTP request–response; use `-it` flag and volume mounts instead.
- When port HOST_PORT is already in use on the host system; choose an alternative port or stop the conflicting service first.
- When the image documentation does not specify the internal container port; inspect the Dockerfile or container logs first.

## Inputs

- Docker image name and tag (e.g., ipbhalle/metfragweb)
- Desired host port (integer, typically 8000–9000 for development)
- Container internal port (from image documentation, e.g., 8080 for Tomcat)
- Optional environment variables (WEBPREFIX, JAVA_OPTS)

## Outputs

- Running Docker container accessible via mapped host port
- HTTP endpoint accessible at http://localhost:HOST_PORT/WEBPREFIX
- HTTP 200 status code response confirming service availability

## How to apply

Use the Docker `docker run` command with the `-p` flag to map the host port to the container's internal port in the format `-p HOST_PORT:CONTAINER_PORT`. For MetFrag, the container's Tomcat server runs on internal port 8080; mapping `-p 8888:8080` makes it accessible at http://localhost:8888. After launching, wait for the application server (Tomcat) to fully initialize within the container, then verify accessibility by sending an HTTP GET request to the mapped URL and confirming a 200 status code response. The WEBPREFIX environment variable can further customize the webapp path (e.g., `/MetFragWeb` or `/mymetfrag`) within the exposed port.

## Related tools

- **Docker** (Container runtime and orchestration engine used to run and expose the MetFrag webapp container via port mapping) — https://www.docker.com/
- **Tomcat** (Java application server running inside the MetFrag container on internal port 8080, mapped to host port via -p flag) — https://hub.docker.com/_/tomcat
- **ipbhalle/metfragweb** (Pre-built Docker image containing MetFrag webapp and Tomcat; pulled from Docker Hub and run with port mapping configuration) — https://hub.docker.com/r/ipbhalle/metfragweb

## Examples

```
docker run -it --rm -p 8888:8080 ipbhalle/metfragweb
```

## Evaluation signals

- Docker container launches without errors and remains running after the `docker run` command completes initialization
- HTTP GET request to http://localhost:HOST_PORT/WEBPREFIX returns status code 200 and valid HTML content
- Tomcat logs visible in container output show successful application deployment (e.g., 'INFO: Server startup in ... ms')
- Repeated requests to the mapped URL consistently return 200 status and expected webapp interface
- Port mapping is verified via `docker ps` showing the correct port mapping (e.g., '0.0.0.0:8888->8080/tcp')

## Limitations

- Port mapping only works for TCP-based protocols; UDP or other protocols require different Docker networking modes.
- The mapped host port must be unprivileged (≥1024) unless Docker daemon runs as root; ports <1024 may fail on non-root systems.
- Port mapping does not persist across container restarts unless the same `-p` flag is reapplied; use Docker Compose or volume definitions for persistence.
- WEBPREFIX environment variable is specific to the ipbhalle/metfragweb image; other containers may use different configuration mechanisms.
- If the container's application server takes significant time to initialize (>30 seconds), immediate requests may fail before readiness; add explicit wait logic.

## Evidence

- [readme] Run MetFrag at http://localhost:8888/MetFragWeb: "Run MetFrag at http://localhost:8888/MetFragWeb
```
docker run -it --rm -p 8888:8080 ipbhalle/metfragweb
```"
- [readme] Port mapping with WEBPREFIX environment variable: "Run Metfrag at http://localhost:8888/mymetfrag with 4GB JVM size using a settings file from `./settings.properties`
```
docker run -it --rm -e  JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag"
- [other] Workflow validation step: "Query http://localhost:8888/MetFragWeb via HTTP to verify the webapp is accessible and returns a 200 status code."
- [other] Tomcat initialization requirement: "Wait for the Tomcat application server to fully initialize within the container."
- [readme] Container configuration options: "Following options are supported:
* environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust jvm memory
* environment variable WEBPREFIX to adjust the web app name"
