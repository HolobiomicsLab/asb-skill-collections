---
name: jvm-heap-memory-tuning-verification
description: Use when when deploying the ipbhalle/metfragweb Docker container and you need to confirm that custom JVM heap sizes (specified via JAVA_OPTS=-Xmx?g -Xms?g) have taken effect, or when troubleshooting memory-related runtime issues in the running container.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Docker
  - Java 21
  - ipbhalle/metfragweb
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans: []
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

# JVM Heap Memory Tuning Verification

## Summary

Verify that JVM heap memory settings have been correctly configured in a containerized Java application by passing JAVA_OPTS environment variables and then validating the active heap size using JVM diagnostic tools. This skill ensures that memory constraints are properly applied to avoid out-of-memory errors or suboptimal performance in containerized MetFrag deployments.

## When to use

When deploying the ipbhalle/metfragweb Docker container and you need to confirm that custom JVM heap sizes (specified via JAVA_OPTS=-Xmx?g -Xms?g) have taken effect, or when troubleshooting memory-related runtime issues in the running container.

## When NOT to use

- When the container is not running or the JVM process is not accessible via docker exec.
- When using a non-Tomcat-based Java application where JAVA_OPTS environment variable handling may differ or not be supported.

## Inputs

- Running ipbhalle/metfragweb Docker container instance
- JAVA_OPTS environment variable string with heap parameters
- Container process ID or name

## Outputs

- Validated heap memory configuration report (maximum heap size in GB)
- Validated heap memory configuration report (initial heap size in GB)
- JVM diagnostic command output (jps or jcmd format)

## How to apply

Launch the ipbhalle/metfragweb container using docker run with the -e flag to pass JAVA_OPTS environment variables specifying maximum (-Xmx) and initial (-Xms) heap sizes in gigabytes (e.g., JAVA_OPTS="-Xmx4g -Xms4g"). After the container is running, execute a JVM diagnostic command such as jps (to list running JVM processes) or jcmd (to inspect JVM settings) inside the container using docker exec. Parse the diagnostic output to extract the actual heap size configuration and compare it against the requested values to confirm both maximum and initial heap sizes match the specified parameters.

## Related tools

- **Docker** (Container runtime for launching and executing commands within the ipbhalle/metfragweb container)
- **Java 21** (JVM runtime that interprets JAVA_OPTS and runs diagnostic commands (jps, jcmd) to inspect heap memory settings)
- **ipbhalle/metfragweb** (Docker container image being configured and verified for correct JVM memory settings) — https://hub.docker.com/r/ipbhalle/metfragweb

## Examples

```
docker run -it --rm -e JAVA_OPTS="-Xmx4g -Xms4g" -p 8888:8080 ipbhalle/metfragweb & sleep 5 && docker exec $(docker ps -q --filter ancestor=ipbhalle/metfragweb) jcmd $(jps | grep Catalina | cut -d' ' -f1) VM.system_properties | grep -E '(Xmx|Xms)'
```

## Evaluation signals

- jps command output lists the Tomcat/MetFragWeb process with correct identifier
- jcmd output includes heap memory flags (-Xmx and -Xms) matching the requested values in JAVA_OPTS
- Maximum heap size reported equals the value specified in JAVA_OPTS (e.g., 4GB when -Xmx4g is passed)
- Initial heap size reported equals the value specified in JAVA_OPTS (e.g., 4GB when -Xms4g is passed)
- Container continues running without out-of-memory errors during typical MetFrag query workloads

## Limitations

- Verification requires the container to be actively running; heap settings cannot be inspected on stopped or exited containers.
- The JAVA_OPTS environment variable is supported by the official Tomcat Docker base image; custom or non-standard Java application containers may not honor this variable.
- JVM diagnostic tools (jps, jcmd) must be available in the container image; some minimal or Alpine-based images may not include them.

## Evidence

- [readme] environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust jvm memory: "environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust jvm memory"
- [other] Execute a JVM diagnostic command (e.g., jps or jcmd) inside the running container to retrieve the active heap memory settings.: "Execute a JVM diagnostic command (e.g., jps or jcmd) inside the running container to retrieve the active heap memory settings."
- [other] Parse and validate the JVM output to confirm maximum heap size is 4GB and initial heap size is 4GB.: "Parse and validate the JVM output to confirm maximum heap size is 4GB and initial heap size is 4GB."
- [readme] docker run -it --rm -e  JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb: "docker run -it --rm -e  JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb"
