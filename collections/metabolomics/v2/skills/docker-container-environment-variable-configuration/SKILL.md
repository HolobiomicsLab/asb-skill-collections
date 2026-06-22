---
name: docker-container-environment-variable-configuration
description: Use when when deploying a Java application in a Docker container and you need to adjust JVM heap memory settings (maximum and initial heap size) without modifying the container image.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Docker
  - Java 21
  - jps / jcmd
  - ipbhalle/metfragweb
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans:
- docker run
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
---

# docker-container-environment-variable-configuration

## Summary

Configure JVM memory heap settings in a Dockerized application by passing environment variables (JAVA_OPTS with -Xmx and -Xms parameters) at container launch time. This skill enables runtime tuning of memory allocation without rebuilding container images.

## When to use

When deploying a Java application in a Docker container and you need to adjust JVM heap memory settings (maximum and initial heap size) without modifying the container image. Use this skill if the container is based on Tomcat or another Java runtime and accepts JAVA_OPTS environment variables, and your analysis or workload requires non-default memory allocations.

## When NOT to use

- Container does not support JAVA_OPTS environment variable (check documentation first)
- JVM memory is already hardcoded in the container Dockerfile or startup script and environment variables are ignored
- Application is not Java-based or does not run on a JVM

## Inputs

- Docker container image URI (e.g., ipbhalle/metfragweb)
- desired JVM heap size parameters (e.g., 4GB maximum, 4GB initial)
- optional: additional environment variables (WEBPREFIX, settings file path)

## Outputs

- running Docker container with configured JVM memory settings
- JVM diagnostic output confirming heap size allocation

## How to apply

Pass the JAVA_OPTS environment variable with heap size parameters to the docker run command using the -e flag. Specify both -Xmx (maximum heap) and -Xms (initial heap) with gigabyte units, e.g., JAVA_OPTS="-Xmx4g -Xms4g". After container launch, verify the configuration by executing a JVM diagnostic command (jps or jcmd) inside the running container to parse and confirm that the maximum and initial heap sizes match the specified values. This approach allows dynamic memory tuning per deployment without rebuilding the image.

## Related tools

- **Docker** (container runtime for launching ipbhalle/metfragweb with environment variable configuration)
- **Java 21** (JVM runtime whose memory settings are configured via JAVA_OPTS)
- **jps / jcmd** (JVM diagnostic tools to verify heap memory settings in running container)
- **ipbhalle/metfragweb** (example Docker container image that accepts JAVA_OPTS for memory tuning) — https://hub.docker.com/r/ipbhalle/metfragweb

## Examples

```
docker run -it --rm -e JAVA_OPTS="-Xmx4g -Xms4g" -p 8888:8080 ipbhalle/metfragweb
```

## Evaluation signals

- docker run command executes without error and container enters running state
- JVM diagnostic command (jps or jcmd) returns output indicating the specified maximum heap size (e.g., -Xmx4g → max heap = 4GB)
- JVM diagnostic command output confirms initial heap size matches the specified -Xms parameter
- Container web application (e.g., MetFragWeb) is accessible at the expected URL and handles queries without out-of-memory errors
- No error logs in container stderr mentioning heap size mismatches or memory allocation failures

## Limitations

- JAVA_OPTS configuration applies only at container launch; changing memory requires stopping and restarting the container with new parameters
- Specified heap sizes must not exceed available host machine physical or cgroup-limited memory, or the JVM will fail to start
- Some container images may override or ignore JAVA_OPTS if they define competing JVM startup flags in their entry point script
- Environment variable syntax is case-sensitive and must match the exact format expected by the container's startup script

## Evidence

- [readme] environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust jvm memory: "environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust jvm memory"
- [other] The ipbhalle/metfragweb container accepts an environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust JVM memory, enabling users to set maximum and initial heap sizes by passing these parameters during container launch.: "The ipbhalle/metfragweb container accepts an environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust JVM memory"
- [other] Launch the container with Docker using the docker run command, passing JAVA_OPTS=-Xmx4g -Xms4g as an environment variable (-e flag).: "Launch the container with Docker using the docker run command, passing JAVA_OPTS=-Xmx4g -Xms4g as an environment variable (-e flag)."
- [other] Execute a JVM diagnostic command (e.g., jps or jcmd) inside the running container to retrieve the active heap memory settings.: "Execute a JVM diagnostic command (e.g., jps or jcmd) inside the running container to retrieve the active heap memory settings."
- [readme] docker run -it --rm -e  JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb: "docker run -it --rm -e  JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb"
