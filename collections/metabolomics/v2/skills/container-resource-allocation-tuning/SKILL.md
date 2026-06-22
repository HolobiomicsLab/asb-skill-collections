---
name: container-resource-allocation-tuning
description: Use when deploying a containerized .NET Framework application (e.g., AirdPro) that performs computationally intensive batch operations such as vendor file conversion to Aird format.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - C#
  - ProteoWizard
  - XQuartz
  - Docker Desktop for Mac
  - Docker Engine
  - docker-compose
  - BuildKit
  - .NET Framework 4.8
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro is written in C#
- pwiz_bindings_cli.dll from the ProteoWizard project
- based on pwiz_bindings_cli.dll from the ProteoWizard project.
- XQuartz (for GUI display support)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aird_cq
    doi: 10.1186/s12859-021-04490-0
    title: aird
  dedup_kept_from: coll_aird_cq
schema_version: 0.2.0
---

# container-resource-allocation-tuning

## Summary

Configure Docker container memory and CPU limits to optimize multi-stage builds and runtime performance for resource-intensive applications like AirdPro. This skill ensures stable execution of complex workloads (e.g., large-scale mass spectrometry data conversion) without system resource exhaustion or out-of-memory failures.

## When to use

Apply this skill when deploying a containerized .NET Framework application (e.g., AirdPro) that performs computationally intensive batch operations such as vendor file conversion to Aird format. Resource allocation tuning is essential before running production conversion tasks, especially on shared systems or when processing large ion mobility datasets that are known to cause memory overflow without proper limits.

## When NOT to use

- When the application is stateless and requires minimal compute (e.g., simple file format conversion without batch processing) — generic defaults may suffice.
- If host system resources are unknown or uncontrolled (e.g., shared Kubernetes cluster) — defer to cluster-level resource policies rather than per-container tuning.
- When the input dataset size is trivial or memory usage is predictable from prior runs — one-time calibration may not justify ongoing tuning overhead.

## Inputs

- docker-compose.yml configuration file with memory and CPU service definitions
- Multi-stage Dockerfile with defined build and runtime stages
- Test dataset or conversion task representing peak workload (e.g., large vendor file or ion mobility raw data)

## Outputs

- Resource-limited Docker containers with verified memory and CPU allocations
- Health check validation report showing container stability under resource constraints
- Build and runtime logs confirming all image targets compile and execute without OOM or throttling failures

## How to apply

Define memory and CPU resource limits in docker-compose.yml or docker run commands based on the host machine's available capacity and the application's workload profile. For AirdPro, set memory to 8 GB and CPU to 4 cores as a baseline; monitor container health during initial test conversions using `docker inspect --format='{{.State.Health.Status}}'` to detect memory pressure or CPU throttling. If memory overflow errors occur during large-scale conversions (as noted in V6 release notes), incrementally increase limits and re-run configuration tests via the build-docker.sh script. Validate that all Docker image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) respect resource constraints and pass health checks before deploying to production batch tasks.

## Related tools

- **Docker Desktop for Mac** (Container runtime and orchestration platform for macOS; provides GUI for resource allocation settings and BuildKit optimization)
- **Docker Engine** (Core container runtime for Linux; executes resource-limited containers defined in docker-compose.yml and Dockerfile)
- **docker-compose** (Declarative configuration tool for defining memory and CPU limits under services.*.deploy.resources.limits in YAML)
- **BuildKit** (Advanced Docker build system; enables optimization flags (DOCKER_BUILDKIT=1) to reduce build time and memory footprint during multi-stage compilation)
- **.NET Framework 4.8** (Runtime environment for AirdPro C# GUI application; memory and CPU allocation directly impact compilation and conversion performance)

## Examples

```
export DOCKER_BUILDKIT=1 && docker run -m 8g --cpus=4 --health-cmd='docker inspect --format={{.State.Health.Status}} airdpro-container' csi-studio/airdpro:runtime-linux
```

## Evaluation signals

- All Docker image targets (runtime-windows, runtime-linux, runtime-cli, runtime-dev) build successfully without OOM or timeout errors.
- Health check validation passes: `docker inspect --format='{{.State.Health.Status}}' airdpro-container` returns 'healthy' during test conversion.
- Configuration test completes without memory overflow errors, especially for large ion mobility raw files or batch conversion queues.
- CPU usage remains below 100% throttle threshold (4 cores) during peak conversion load; memory footprint stays within 8 GB limit during large-scale conversions.
- Build time for multi-stage Dockerfile is reproducible across runs and does not degrade when resource limits are applied (BuildKit optimization confirms no cache loss).

## Limitations

- Resource limits are host-dependent: 8 GB memory and 4 cores is a baseline for AirdPro but may be insufficient for very large ion mobility datasets or concurrent batch tasks; requires empirical tuning per deployment environment.
- Memory overflow issues mentioned in AirdPro V6 release notes may persist if limits are set too conservatively; users must incrementally increase allocations and re-validate.
- Docker Desktop for Mac has additional overhead from virtualization; actual available memory to containers is less than host total; macOS users should allocate ≥12 GB to Docker Desktop itself.
- Health check validation (`docker inspect`) requires container to expose health endpoints; containers that crash immediately or enter unresponsive states may not be caught by status queries alone.
- Multi-stage build optimization (BuildKit) requires explicit enablement (export DOCKER_BUILDKIT=1); without it, resource limits may not apply consistently across build stages.

## Evidence

- [other] Enable BuildKit optimization and configure resource limits in docker-compose.yml for memory (8GB) and CPU (4 cores).: "Enable BuildKit optimization and configure resource limits in docker-compose.yml for memory (8GB) and CPU (4 cores)."
- [methods] Set memory and CPU limits in docker-compose.yml: "Resource limits configuration: 'Set memory and CPU limits in docker-compose.yml'"
- [methods] Health check validation using docker inspect: "Health check validation: 'docker inspect --format='{{.State.Health.Status}}' airdpro-container'"
- [readme] Resolves memory overflow issues during large-scale conversions: "[Stability improvement] Resolves memory overflow issues during large-scale conversions"
- [methods] export DOCKER_BUILDKIT=1: "Enable BuildKit: 'export DOCKER_BUILDKIT=1'"
