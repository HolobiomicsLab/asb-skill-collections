---
name: java-diagnostic-tool-operation
description: Use when when you have deployed a JVM application in a Docker container with JAVA_OPTS heap size parameters and need to verify that the maximum and initial heap sizes are correctly configured before running memory-intensive workflows like metabolite fragmentation analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Java 21
  - Docker
  - jps
  - jcmd
  - ipbhalle/metfragweb
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans:
- Java 21
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

# java-diagnostic-tool-operation

## Summary

Execute JVM diagnostic commands (jps, jcmd) inside a running container to retrieve and validate active heap memory settings, confirming that environment variable configurations have been correctly applied to the JVM.

## When to use

When you have deployed a JVM application in a Docker container with JAVA_OPTS heap size parameters and need to verify that the maximum and initial heap sizes are correctly configured before running memory-intensive workflows like metabolite fragmentation analysis.

## When NOT to use

- The application is not running in a container—use native JVM diagnostic tools on the host instead.
- The JVM process has already exited or the container is not in a running state; start the container before attempting diagnosis.
- You only need to inspect the JAVA_OPTS variable itself without validating its effect on the running JVM; examine the environment variable directly instead.

## Inputs

- running Docker container (ipbhalle/metfragweb or similar Tomcat-based JVM application)
- JAVA_OPTS environment variable configuration string (e.g., '-Xmx4g -Xms4g')
- container runtime environment (Docker daemon accessible via CLI)

## Outputs

- JVM diagnostic command output (text report from jps or jcmd)
- parsed heap size values (numeric, in GB or MB)
- validation result (pass/fail confirmation of heap configuration)

## How to apply

After launching the ipbhalle/metfragweb container with JAVA_OPTS=-Xmx?g -Xms?g environment variables, execute a JVM diagnostic command (jps to list Java processes, or jcmd to query process details) inside the running container using docker exec or equivalent. Parse the JVM diagnostic output to extract heap size values and compare them against the expected configuration (e.g., -Xmx4g should yield 4 GB maximum heap). Validate that both maximum heap size (-Xmx) and initial heap size (-Xms) match the parameters passed in JAVA_OPTS; if they do not, the environment variable was not properly propagated or the container does not inherit the setting correctly.

## Related tools

- **Docker** (container runtime and execution environment for the MetFrag JVM application; enables passing environment variables and executing diagnostic commands inside running containers)
- **Java 21** (JVM runtime that hosts the MetFrag web application and provides diagnostic tools (jps, jcmd) for introspecting heap configuration)
- **jps** (JVM Process Status tool; lists Java processes running inside the container to identify the MetFrag/Tomcat process)
- **jcmd** (JVM diagnostic command utility; queries detailed process information including heap size settings from the running JVM)
- **ipbhalle/metfragweb** (target Docker container image packaging MetFrag web application; accepts JAVA_OPTS environment variable for heap configuration) — https://hub.docker.com/r/ipbhalle/metfragweb

## Examples

```
docker exec <container_id> jcmd 1 VM.system_properties | grep -i heap
```

## Evaluation signals

- jps command returns a process ID corresponding to the Tomcat/MetFrag application running inside the container.
- jcmd output explicitly reports heap memory values that match the -Xmx and -Xms parameters passed in JAVA_OPTS (e.g., output contains '4294967296 bytes' or '4096 MB' when -Xmx4g was specified).
- Comparison of expected vs. actual heap size shows zero discrepancy: if JAVA_OPTS=-Xmx4g -Xms4g was passed, jcmd reports MaxHeapSize=4GB and InitialHeapSize=4GB.
- Repeated invocation of the diagnostic command over time shows consistent heap values, indicating stable JVM configuration throughout the container lifetime.
- No error or permission-denied messages appear when executing jps or jcmd inside the container; diagnostic tools are accessible and executable.

## Limitations

- Diagnostic commands (jps, jcmd) must be available in the container image; minimal or hardened containers may not include these tools.
- Some container environments or orchestration systems (e.g., Kubernetes with restricted security contexts) may prevent execution of diagnostic tools or visibility into process internals.
- Heap size values reported by jcmd are snapshots at the moment of execution; they do not account for runtime heap fluctuations or garbage collection events.
- If the JAVA_OPTS variable is not correctly documented or the container entrypoint does not explicitly propagate environment variables to the JVM, the diagnostic output may not reflect the intended configuration.

## Evidence

- [other] Execute a JVM diagnostic command (e.g., jps or jcmd) inside the running container to retrieve the active heap memory settings.: "Execute a JVM diagnostic command (e.g., jps or jcmd) inside the running container to retrieve the active heap memory settings."
- [other] Parse and validate the JVM output to confirm maximum heap size is 4GB and initial heap size is 4GB.: "Parse and validate the JVM output to confirm maximum heap size is 4GB and initial heap size is 4GB."
- [readme] environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust jvm memory: "environment variable JAVA_OPTS="-Xmx?g -Xms?g" to adjust jvm memory"
- [readme] Run Metfrag at http://localhost:8888/mymetfrag with 4GB JVM size using a settings file: "docker run -it --rm -e  JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag"
