---
name: container-runtime-verification
description: Use when when deploying a containerized application (e.g., ipbhalle/metfragweb) with injected configuration files via Docker volume mounts, and you need to confirm that the container accepted the mounted file and applied its settings before proceeding with downstream analysis or services.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - ipbhalle/metfragweb
  - Docker
  - Tomcat
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans:
- https://hub.docker.com/r/ipbhalle/metfragweb
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

# container-runtime-verification

## Summary

Verify that a Docker container has successfully loaded configuration files mounted at a specific path and applied the settings correctly. This skill confirms that volume mounts are properly linked and that the application has ingested the injected configuration.

## When to use

When deploying a containerized application (e.g., ipbhalle/metfragweb) with injected configuration files via Docker volume mounts, and you need to confirm that the container accepted the mounted file and applied its settings before proceeding with downstream analysis or services.

## When NOT to use

- The container does not expose any logs, metrics, or API to inspect (verification becomes impossible).
- Configuration is hardcoded into the container image and does not support runtime injection via mounted files.
- The application design does not require external settings files—i.e., all config is environment-variable-driven or embedded in the Dockerfile.

## Inputs

- Running Docker container with volume mount (from docker run with --volume)
- Local settings file path on host system (e.g., ./settings.properties)
- Container image identifier (e.g., ipbhalle/metfragweb)

## Outputs

- Container logs confirming settings file was loaded
- Service response or access log showing configuration was applied
- Verification report documenting mount success and setting activation

## How to apply

After launching the container with a --volume mount binding a local settings file to a target path (e.g., /resources/settings.properties), inspect the running container's logs using docker logs to look for evidence that the settings file was loaded and parsed. Cross-validate by accessing the running service (e.g., via HTTP if it exposes a web interface or API) and verify that configuration parameters—such as environment variables, database connection strings, or API tokens—are reflected in the application's behavior or output. If logs are unavailable, use docker exec to directly inspect the mounted path inside the container and confirm the file exists and contains expected content. Document the verification results (logs, service response, file inspection) to confirm the mount succeeded before considering the container deployment complete.

## Related tools

- **Docker** (Container orchestration and volume mount execution; used to launch containers and inspect logs and running state)
- **ipbhalle/metfragweb** (Target containerized application that accepts a settings.properties file at /resources/settings.properties and loads it at startup) — https://hub.docker.com/r/ipbhalle/metfragweb
- **Tomcat** (Underlying web server packaged in the container; verification may involve inspecting Tomcat logs or accessing the web service)

## Examples

```
docker run -it --rm -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb && docker logs <container_id>
```

## Evaluation signals

- Container logs (docker logs <container_id>) contain no errors related to file not found or parse failures at /resources/settings.properties
- The mounted settings file is readable inside the container at the expected path (docker exec <container_id> cat /resources/settings.properties returns content)
- Web service (http://localhost:8888/MetFragWeb or custom WEBPREFIX) is accessible and responds without configuration errors
- Configuration parameters from the settings file (e.g., ChemSpider tokens, proxy settings, local database connections) are reflected in service behavior or logs
- No mismatch between host-side settings file and in-container behavior indicates the volume mount was properly bound

## Limitations

- Verification depends on the application exposing logs; containers with suppressed or redirected logs may be difficult to inspect.
- If the application loads settings only at startup, changes to the mounted file after container launch will not take effect without restart.
- Verification via HTTP access requires the service to be reachable and the port to be properly mapped; network policies or port conflicts may obstruct this check.
- Some configuration parameters (e.g., optional database credentials) may not be validated until actual use, so absence of startup errors does not guarantee all settings are correct.

## Evidence

- [readme] automatic use of a metfrag settings file if provided at /resources/settings.properties: "automatic use of a metfrag settings file if provided at /resources/settings.properties"
- [other] Verify that the container successfully loaded the mounted file by inspecting container logs or accessing the running service to confirm settings were applied.: "Verify that the container successfully loaded the mounted file by inspecting container logs or accessing the running service to confirm settings were applied."
- [readme] Run Metfrag at http://localhost:8888/mymetfrag with 4GB JVM size using a settings file from `./settings.properties`: "docker run -it --rm -e  JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb"
