---
name: metfrag-settings-injection
description: Use when when deploying the ipbhalle/metfragweb container and you need
  to configure MetFrag parameters such as ChemSpider tokens, proxy settings for web
  services (MoNA, KEGG, MetaCyc), or local database connections (PubChem via MySQL/PostgreSQL)
  without modifying the container image itself.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - ipbhalle/metfragweb
  - Docker
  - Tomcat
  - Java 21
  license_tier: restricted
  provenance_tier: literature
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

# MetFrag Settings File Injection via Docker Volume Mount

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Inject MetFrag configuration parameters into the ipbhalle/metfragweb Docker container by mounting a local settings.properties file to the /resources/settings.properties path, enabling dynamic configuration without rebuilding the container image.

## When to use

When deploying the ipbhalle/metfragweb container and you need to configure MetFrag parameters such as ChemSpider tokens, proxy settings for web services (MoNA, KEGG, MetaCyc), or local database connections (PubChem via MySQL/PostgreSQL) without modifying the container image itself.

## When NOT to use

- If MetFrag configuration is embedded in the application code and does not support external file loading — verify container documentation before assuming settings injection will work.
- If you need to change settings frequently at runtime without restarting the container — settings injection requires a new docker run invocation.
- If the settings.properties file contains secrets that should not be stored on disk — use Docker secrets or environment variables instead (if supported by MetFragWeb).

## Inputs

- Local settings.properties file (host filesystem)
- ipbhalle/metfragweb Docker image
- Docker daemon / container runtime

## Outputs

- Running ipbhalle/metfragweb container with injected settings
- Container logs confirming settings file load
- Configured MetFragWeb service accessible via HTTP (port 8080 or mapped host port)

## How to apply

Prepare a settings.properties file on the host system containing required MetFrag configuration parameters (e.g., ChemSpiderToken, proxy server/port pairs, local database credentials). Launch the ipbhalle/metfragweb container using docker run with a --volume flag binding the host settings.properties to /resources/settings.properties inside the container. The container automatically loads the mounted file at startup. Verify successful injection by inspecting container logs or confirming that the running MetFragWeb service reflects the injected settings (e.g., proxy connectivity, database query performance, token-gated services). This approach leverages Docker's volume mount mechanism to externalize configuration, enabling environment-specific settings across development, testing, and production deployments.

## Related tools

- **Docker** (Container runtime that enables volume mounting and the --volume flag to bind host files into the container filesystem)
- **ipbhalle/metfragweb** (Docker image for MetFrag webapp that automatically loads settings.properties from /resources/settings.properties at startup) — https://hub.docker.com/r/ipbhalle/metfragweb
- **Tomcat** (Web server base layer in the ipbhalle/metfragweb container that hosts the MetFragWeb Java application)
- **Java 21** (Runtime for the MetFragWeb application and JVM memory configuration via JAVA_OPTS environment variable)

## Examples

```
docker run -it --rm -e JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb
```

## Evaluation signals

- Container starts without errors; docker logs show no file-not-found or parsing errors for /resources/settings.properties.
- MetFragWeb HTTP endpoint responds (e.g., http://localhost:8080/index.xhtml or http://localhost:8888/MetFragWeb depending on WEBPREFIX).
- Configured services (ChemSpider queries, proxy-dependent web services, or local database queries) function as expected — verify by testing a query that depends on injected settings (e.g., ChemSpider token usage, proxy connectivity).
- settings.properties file is readable inside the container at /resources/settings.properties; confirm via `docker exec <container_id> cat /resources/settings.properties`.
- No duplicate or conflicting settings.properties files exist in the container image itself (e.g., at /tomcat/webapps/ROOT/resources/settings.properties) that could override the mounted file.

## Limitations

- The container must be restarted to reload settings — changes to the mounted settings.properties file do not take effect in a running container without restart.
- If settings.properties is not provided or the path /resources/settings.properties is not properly mounted, the container may fall back to default or template settings, potentially silently failing for token-dependent or proxy-dependent features.
- No changelog or version history is available for the ipbhalle/metfragweb image, making it difficult to track when settings injection support was introduced or how it behaves across versions.
- The mechanism relies on the container's automatic file loading behavior; if this behavior is not documented for a specific image tag or version, behavior may be unpredictable.

## Evidence

- [readme] automatic use of a metfrag settings file if provided at /resources/settings.properties: "automatic use of a metfrag settings file if provided at /resources/settings.properties"
- [readme] Run Metfrag at http://localhost:8888/mymetfrag with 4GB JVM size using a settings file from `./settings.properties` with docker run -it --rm -e  JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb: "docker run -it --rm -e  JAVA_OPTS="-Xmx4g -Xms4g" -e WEBPREFIX=mymetfrag -v $(pwd)/settings.properties:/resources/settings.properties -p 8888:8080 ipbhalle/metfragweb"
- [readme] rename file settings.properties.template in MetFragWeb/src/main/webapp/resources to settings.properties and set necessary parameters including ChemSpiderToken, proxy servers and ports for MoNA, KEGG, MetaCyc, and local database configuration: "rename file settings.properties.template in MetFragWeb/src/main/webapp/resources to settings.properties and set necessary parameters"
- [other] The ipbhalle/metfragweb container supports automatic use of a metfrag settings file if provided at /resources/settings.properties, enabling configuration injection via Docker volume mount.: "The ipbhalle/metfragweb container supports automatic use of a metfrag settings file if provided at /resources/settings.properties, enabling configuration injection via Docker volume mount."
