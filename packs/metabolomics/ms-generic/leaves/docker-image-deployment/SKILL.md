---
name: docker-image-deployment
description: Use when when you have a containerized scientific tool available on Docker
  Hub (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0625
  tools:
  - Docker
  - MetFrag
  - Tomcat
  - Java 21
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans:
- docker run -it --rm -p 8888:8080 ipbhalle/metfragweb
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

# docker-image-deployment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Deploy a containerized scientific application (MetFrag webapp) by pulling a Docker image, mapping network ports, configuring runtime environment variables, and verifying HTTP accessibility at the exposed endpoint. This skill bridges container orchestration with application deployment validation.

## When to use

When you have a containerized scientific tool available on Docker Hub (e.g., ipbhalle/metfragweb) and need to make it accessible on a host at a specified HTTP endpoint, or when you need to customize JVM memory, web application paths, or configuration files at container runtime without rebuilding the image.

## When NOT to use

- The containerized application requires persistent data storage across container restarts and you have not set up a named volume or bind mount for the application state.
- You need to run multiple instances with coordinated networking or service discovery; use Docker Compose or Kubernetes instead of single docker run commands.
- The host system does not have Docker installed or you lack permission to run privileged Docker commands.

## Inputs

- Docker image name and tag (string, e.g., 'ipbhalle/metfragweb')
- Host port number (integer)
- Container internal port number (integer, typically 8080 for Tomcat)
- Optional: JVM memory configuration string (e.g., '-Xmx4g -Xms4g')
- Optional: WEBPREFIX string (e.g., 'mymetfrag')
- Optional: settings.properties file (path on host filesystem)

## Outputs

- Running Docker container instance accessible at HOST:HOST_PORT
- HTTP endpoint responding with application homepage (HTTP 200)
- Container startup logs documenting Tomcat initialization
- Deployed MetFrag webapp accessible via web browser or HTTP client

## How to apply

Pull the Docker image from the registry (e.g., docker pull ipbhalle/metfragweb). Run the container using docker run with port mapping (-p HOST_PORT:CONTAINER_PORT, typically -p 8888:8080 for Tomcat). Set environment variables (JAVA_OPTS for JVM memory heap sizes, WEBPREFIX for the webapp path, or settings.properties file location) as needed. Mount configuration files via -v HOST_PATH:/resources/settings.properties if using custom settings. Allow time for the embedded Tomcat application server to initialize. Verify successful deployment by making a GET request to the exposed HTTP endpoint (e.g., http://localhost:8888/MetFragWeb) and confirming a 200 response or valid webpage content is returned.

## Related tools

- **Docker** (Container runtime and orchestration—pulls, runs, and manages the containerized MetFrag webapp with port mapping and environment variable configuration.)
- **Tomcat** (Embedded Java web application server inside the container—listens on internal port 8080 and serves the MetFrag webapp after initialization.)
- **Java 21** (Runtime environment required by MetFrag; JVM memory heap sizes are configured via JAVA_OPTS environment variable.)
- **MetFrag** (Scientific application packaged in the Docker image; provides mass spectrometry analysis web interface.) — https://github.com/ipb-halle/MetFragRelaunched

## Examples

```
docker run -it --rm -e JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb
```

## Evaluation signals

- HTTP GET request to http://localhost:HOST_PORT/WEBPREFIX returns HTTP status 200 and valid HTML content.
- Container logs show successful Tomcat startup messages with no ERROR or FATAL level entries during initialization.
- Port mapping is active: `docker ps` shows the container with PORTS column displaying `0.0.0.0:HOST_PORT->8080/tcp`.
- Custom environment variables are applied: if JAVA_OPTS is set, the JVM process inside the container reports the configured heap sizes via `jps -v` or container logs.
- Configuration file is mounted correctly: if settings.properties is provided via -v, the running container's /resources/settings.properties is readable and contains expected configuration parameters (e.g., ChemSpiderToken, proxy settings).

## Limitations

- The container requires the Docker daemon to be running and accessible; deployment will fail on systems without Docker or with permission restrictions.
- JVM memory limits (JAVA_OPTS) must be less than the host system's total available memory; misconfiguration causes out-of-memory container termination.
- Port 8080 inside the container is hardcoded; if you need the webapp on a different internal port, you must rebuild the image or use a reverse proxy.
- Configuration via settings.properties is not validated at container startup; invalid proxy or database credentials will only be detected when those services are first queried at runtime.
- No automatic health checks or restart policies are configured by default; the container will exit if Tomcat crashes, and manual intervention is required to restart.

## Evidence

- [readme] This container packages the MetFrag (https://github.com/ipb-halle/MetFragRelaunched) webapp and some text databases based on the latest official tomcat docker container.: "This container packages the MetFrag (https://github.com/ipb-halle/MetFragRelaunched) webapp and some text databases based on the latest official tomcat docker container."
- [readme] Run MetFrag at http://localhost:8888/MetFragWeb docker run -it --rm -p 8888:8080 ipbhalle/metfragweb: "docker run -it --rm -p 8888:8080 ipbhalle/metfragweb"
- [readme] environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust jvm memory: "environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust jvm memory"
- [readme] Run Metfrag at http://localhost:8888/mymetfrag with 4GB JVM size using a settings file from ./settings.properties docker run -it --rm -e JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb: "docker run -it --rm -e  JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb"
- [other] The MetFrag webapp is deployed by running the ipbhalle/metfragweb Docker container with port mapping (-p 8888:8080) to expose the internal Tomcat port 8080 to the host port 8888, making the application accessible at the specified HTTP endpoint.: "The MetFrag webapp is deployed by running the ipbhalle/metfragweb Docker container with port mapping (-p 8888:8080) to expose the internal Tomcat port 8080 to the host port 8888"
- [readme] automatic use of a metfrag settings file if provided at /resources/settings.properties: "automatic use of a metfrag settings file if provided at /resources/settings.properties"
