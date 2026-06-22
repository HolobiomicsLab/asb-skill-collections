---
name: docker-environment-configuration
description: Use when you need to deploy CloMet for the first time on a new system, or when you want to ensure reproducible execution of metabolomics data harmonization tasks without manual dependency management.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3375
  tools:
  - Docker
  - CloMet
derived_from:
- doi: 10.1021/acs.jproteome.2c00602
  title: CloMet
evidence_spans:
- Follow these steps to install Docker and run CloMet for the first time
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_clomet_cq
    doi: 10.1021/acs.jproteome.2c00602
    title: CloMet
  dedup_kept_from: coll_clomet_cq
schema_version: 0.2.0
---

# docker-environment-configuration

## Summary

Set up and verify a containerized scientific tool (CloMet) for NMR-based metabolomics analysis by installing Docker, cloning the repository, building a container image, and executing an initial command to confirm functionality. This skill ensures reproducible, isolated execution of bioinformatics workflows across different operating systems.

## When to use

Use this skill when you need to deploy CloMet for the first time on a new system, or when you want to ensure reproducible execution of metabolomics data harmonization tasks without manual dependency management. Apply it when you have access to the official CloMet GitHub repository and need to verify that the containerized tool is functional before running production analyses on NMR datasets.

## When NOT to use

- CloMet is already installed and verified on your system — skip to direct execution
- You are running on a system where Docker cannot be installed or is explicitly unavailable (e.g., restricted HPC environments without container support)
- You intend to modify CloMet source code — use developer setup (clone, install dependencies locally) instead of containerization

## Inputs

- Docker installation binary or package for target OS
- CloMet GitHub repository (rmallol/clomet)
- Dockerfile from repository root
- Local file system path for volume mounting (optional NMR metabolomics datasets)

## Outputs

- Installed Docker engine on host system
- Cloned CloMet repository directory
- Built Docker image (tagged, ready to instantiate)
- Running CloMet container instance
- Verification output from initial CloMet command (help/version)

## How to apply

Follow the documented Docker-based installation procedure by first installing Docker for your target operating system via the official Docker installation channel. Clone the CloMet repository from github:rmallol__clomet and examine the provided Dockerfile. Build the CloMet Docker image using the Dockerfile in the repository root. Run the CloMet container with appropriate volume mounts (to bind local metabolomics data directories into the container) and verify startup without errors by inspecting container logs. Finally, execute an initial CloMet command such as `help` or a version check to confirm the tool is accessible and functional within the container environment. Success is indicated when the command executes without errors and produces expected output.

## Related tools

- **Docker** (Container runtime and orchestration engine for isolated, reproducible CloMet deployment across operating systems) — https://www.docker.com/
- **CloMet** (NMR-based metabolomics data harmonization and connection tool between public repositories and analysis platforms; deployed and executed via Docker) — https://github.com/rmallol/clomet

## Examples

```
docker build -t clomet:latest . && docker run --rm clomet:latest clomet --help
```

## Evaluation signals

- Docker daemon is running without errors on the host system
- CloMet repository is cloned to a local directory with all files present (Dockerfile, source code, configuration)
- Docker image build completes without errors and produces a tagged image (inspectable via `docker images`)
- CloMet container starts and reaches a ready state without crash/exit codes (inspectable via `docker ps` or logs)
- Initial CloMet command (e.g., `docker run <image> clomet --help`) executes and returns expected output or documentation

## Limitations

- Requires Docker installation and daemon availability; not suitable for systems where containerization is restricted or unavailable
- No changelog is available in the repository to track version-specific installation differences or breaking changes between CloMet releases
- The README provides a visual diagram (First steps) for guidance; users without graphics rendering may need text-based alternative documentation

## Evidence

- [intro] Docker-based installation procedure with visual guidance available: "Follow these steps to install Docker and run CloMet for the first time"
- [other] Workflow steps for first-run setup and verification: "1. Install Docker following the official installation procedure for the target operating system. 2. Clone the CloMet repository from github:rmallol__clomet. 3. Build the CloMet Docker image from the"
- [readme] CloMet's purpose and focus on metabolomics data harmonization: "CloMet eases the connection between public data repositories and data analysis platforms by harmonizing the file systems of available data sets, with a focus on NMR-based metabolomics."
- [readme] Modular architecture supporting extension by developers: "The software has been designed in such a modular way meeting the Object Oriented Programming standards to facilitate the extension of its capabilities"
