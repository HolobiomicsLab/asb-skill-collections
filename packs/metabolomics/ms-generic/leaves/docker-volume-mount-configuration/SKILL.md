---
name: docker-volume-mount-configuration
description: Use when deploying the ipbhalle/metfragweb container and you need to
  supply custom MetFrag settings (ChemSpider tokens, proxy servers, local database
  connections) without modifying the container image.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Docker
  - ipbhalle/metfragweb
  - MetFrag
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans:
- docker run
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

# docker-volume-mount-configuration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Mount a host-side configuration file into a running Docker container at a specific path to enable automatic loading of application settings without rebuilding the image. This skill is essential when you need to inject environment-specific parameters (database credentials, API tokens, proxy settings) into containerized applications that support external configuration file discovery.

## When to use

Use this skill when deploying the ipbhalle/metfragweb container and you need to supply custom MetFrag settings (ChemSpider tokens, proxy servers, local database connections) without modifying the container image. Specifically, when the target container documents support for automatic configuration file loading at a fixed mount path (e.g., /resources/settings.properties).

## When NOT to use

- The target Docker image does not document automatic configuration file discovery at a specific mount path.
- Configuration parameters must be set via environment variables only (use docker run -e instead).
- The settings file contains secrets (API keys, passwords) that should not be stored on the host filesystem; use Docker secrets or external secret management instead.

## Inputs

- Local settings.properties file on host system (plain text key-value pairs)
- Docker container specification (e.g., ipbhalle/metfragweb image name and tag)
- Host filesystem path to settings file

## Outputs

- Running Docker container with injected configuration
- Application runtime behavior reflecting loaded settings
- Container logs confirming configuration load success

## How to apply

Prepare a local settings.properties file on the host system with MetFrag configuration parameters (ChemSpiderToken, proxy settings, local database credentials). Launch the ipbhalle/metfragweb Docker container using docker run with a --volume flag binding the local settings.properties to /resources/settings.properties inside the container. The container automatically detects and loads the mounted file at startup. Verify successful configuration injection by inspecting container logs or accessing the running web service to confirm that the settings were applied—for MetFragWeb, this means checking that proxies route correctly and database connections resolve.

## Related tools

- **Docker** (Container runtime and volume mount orchestration)
- **ipbhalle/metfragweb** (Target web application container that supports automatic settings.properties injection at /resources/settings.properties) — https://hub.docker.com/r/ipbhalle/metfragweb
- **MetFrag** (Underlying mass spectrometry fragmentation library packaged in the container) — https://github.com/ipb-halle/MetFragRelaunched

## Examples

```
docker run -it --rm -e JAVA_OPTS="-Xmx4g -Xms4g" -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb
```

## Evaluation signals

- Container starts without errors after docker run completes.
- Web service is accessible at the specified port and URL (e.g., http://localhost:8888/MetFragWeb).
- Container logs contain no errors related to missing or unparseable configuration file.
- Application behavior reflects injected settings (e.g., proxy requests route via configured MoNAProxyServer; local database queries succeed if LocalPubChemDatabase is configured).
- docker inspect <container_id> shows the --volume mount binding correctly in the Mounts section.

## Limitations

- The container must be built or configured to support automatic discovery of the settings file at the exact mount path (/resources/settings.properties); this is not a universal Docker feature.
- Settings file on host must be readable by the Docker daemon; permission mismatches will silently fail or cause the container to use defaults.
- Changes to the mounted settings.properties file on the host do not automatically reload in a running container; the container must be stopped and restarted.
- No changelog is documented for the MetFrag project, making it difficult to identify which container versions support this feature.

## Evidence

- [readme] automatic use of a metfrag settings file if provided at /resources/settings.properties: "automatic use of a metfrag settings file if provided at /resources/settings.properties"
- [readme] Run Metfrag at http://localhost:8888/mymetfrag with 4GB JVM size using a settings file from ./settings.properties: docker run -it --rm -e JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb: "docker run -it --rm -e  JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb"
- [readme] rename file settings.properties.template in MetFragWeb/src/main/webapp/resources to settings.properties and set necessary parameters: "rename file settings.properties.template in MetFragWeb/src/main/webapp/resources to settings.properties and set necessary parameters"
- [readme] define chemspider token to query ChemSpider database; if MetFragWeb host is connected via proxy to the internet provide proxy settings for different web services: "define chemspider token to query ChemSpider database; if MetFragWeb host is connected via proxy to the internet provide proxy settings"
- [other] The ipbhalle/metfragweb container supports automatic use of a metfrag settings file if provided at /resources/settings.properties, enabling configuration injection via Docker volume mount.: "The ipbhalle/metfragweb container supports automatic use of a metfrag settings file if provided at /resources/settings.properties, enabling configuration injection via Docker volume mount."
