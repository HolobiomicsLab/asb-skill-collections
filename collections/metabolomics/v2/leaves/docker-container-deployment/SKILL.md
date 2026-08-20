---
name: docker-container-deployment
description: Use when you need to launch a pre-built Docker image of a scientific
  tool (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0003
  - http://edamontology.org/topic_3372
  tools:
  - Docker
  - Tomcat
  - Java 21
  - ipbhalle/metfragweb
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans:
- docker run
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

# docker-container-deployment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Deploy a containerized scientific application (MetFrag webapp) using Docker, with configurable runtime parameters (JVM memory, URL prefix, settings files) and verify accessibility via HTTP status checks. This skill enables reproducible, isolated execution of complex software stacks without manual dependency installation.

## When to use

Use this skill when you need to launch a pre-built Docker image of a scientific tool (e.g., ipbhalle/metfragweb) for local or remote access, want to isolate the application environment from the host system, or need to configure runtime parameters like memory allocation and web application URL prefix without rebuilding the image.

## When NOT to use

- You require modifications to the application code or build configuration — rebuild the image from source using Maven and a Dockerfile instead of pulling a pre-built image.
- The container image is not available in any accessible Docker registry — you must clone the source repository and build the image locally.
- You need to deploy to a production Kubernetes cluster — use Helm charts or Kubernetes manifests rather than docker run.

## Inputs

- Docker image reference (registry/image:tag, e.g., ipbhalle/metfragweb)
- Host port number (e.g., 8888)
- Container port number (typically 8080 for Tomcat)
- Optional: JAVA_OPTS environment variable string (e.g., '-Xmx4g -Xms4g')
- Optional: WEBPREFIX environment variable (e.g., 'mymetfrag')
- Optional: local settings.properties file path

## Outputs

- Running Docker container with accessible web application
- HTTP 200 response from application endpoint (e.g., http://localhost:8888/MetFragWeb)
- Container logs confirming Tomcat initialization and application deployment

## How to apply

Pull the target Docker image from a registry (Docker Hub), then invoke docker run with port mapping (typically host:container, e.g., 8888:8080) and optional environment variables for JAVA_OPTS (memory settings) and WEBPREFIX (URL path). Allow Tomcat to initialize fully (typically 10–30 seconds), then query the application via HTTP (e.g., http://localhost:8888/MetFragWeb) and verify a 200 status code is returned. For persistent configuration, mount a settings.properties file to /resources/settings.properties within the container using the -v flag.

## Related tools

- **Docker** (Container runtime for launching and managing the MetFrag webapp image with port mapping and environment variable configuration)
- **Tomcat** (Application server embedded in the ipbhalle/metfragweb Docker image; handles web application deployment and HTTP request serving)
- **Java 21** (Runtime environment required by MetFrag; configured via JAVA_OPTS environment variable (e.g., heap size -Xmx) inside the container)
- **ipbhalle/metfragweb** (Pre-built Docker image containing MetFrag webapp, Tomcat server, and text databases) — https://hub.docker.com/r/ipbhalle/metfragweb

## Examples

```
docker run -it --rm -e JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb
```

## Evaluation signals

- HTTP GET request to the application URL (e.g., http://localhost:8888/MetFragWeb) returns status code 200 within 30 seconds of container launch.
- Docker container is running and reports 'Up' status when checked via 'docker ps'.
- Container logs show 'Tomcat started' or similar application-ready message without error or exception stack traces.
- If WEBPREFIX is set, the application is accessible at the specified custom path (e.g., http://localhost:8888/mymetfrag) and returns 200.
- If a settings.properties file is mounted, MetFrag logs confirm its loading (e.g., 'Loading settings from /resources/settings.properties') and the application responds with expected behavior.

## Limitations

- The ipbhalle/metfragweb image is pre-built and frozen; modifications to MetFrag code or configuration require rebuilding the image or mounting override files, which may not update all internal dependencies.
- Tomcat initialization time varies; the application may not be immediately accessible upon docker run completion; a wait loop or retry mechanism is recommended in automated workflows.
- The WEBPREFIX environment variable adjusts the URL path but does not modify hard-coded internal links within the webapp; some functionality may break if deep links are expected at a non-default path.
- Database access (PubChem, ChemSpider, KEGG, MoNA) requires external network connectivity and valid credentials (e.g., ChemSpider token in settings.properties); deployment in air-gapped environments will fail at query time.

## Evidence

- [readme] Docker image and container management; Tomcat integration: "This container packages the MetFrag (https://github.com/ipb-halle/MetFragRelaunched) webapp and some text databases based on the latest official tomcat docker container."
- [readme] Configuration of JVM memory and URL prefix: "environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust jvm memory, environment variable WEBPREFIX to adjust the web app name"
- [readme] Default docker run command and port mapping: "Run MetFrag at http://localhost:8888/MetFragWeb: docker run -it --rm -p 8888:8080 ipbhalle/metfragweb"
- [readme] Settings file mounting and initialization: "automatic use of a metfrag settings file if provided at /resources/settings.properties"
- [other] Verification of webapp accessibility and HTTP response: "Query http://localhost:8888/MetFragWeb via HTTP to verify the webapp is accessible and returns a 200 status code."
