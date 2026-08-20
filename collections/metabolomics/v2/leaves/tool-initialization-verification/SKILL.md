---
name: tool-initialization-verification
description: Use when after completing Docker installation and container build steps
  for CloMet, before attempting substantive data analysis or pipeline execution.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - Docker
  - CloMet
  techniques:
  - NMR
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.2c00602
  title: CloMet
evidence_spans: []
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00602
  all_source_dois:
  - 10.1021/acs.jproteome.2c00602
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tool-initialization-verification

## Summary

Verify that a containerized scientific tool (CloMet) has been correctly installed and is functionally accessible after initial Docker-based deployment. This skill ensures the tool environment is ready for downstream metabolomics analysis workflows.

## When to use

After completing Docker installation and container build steps for CloMet, before attempting substantive data analysis or pipeline execution. Use this skill when you need confirmation that the containerized environment is properly configured, the tool binary/executable is accessible within the container, and basic command-line invocations succeed without errors.

## When NOT to use

- The CloMet image has not yet been built from the Dockerfile; perform build first.
- The container is not running; start the container before verification.
- You already have confirmed tool functionality in a previous session and are resuming an existing containerized workflow.

## Inputs

- Running Docker container (CloMet image)
- Docker daemon/engine (running)
- Container execution context (shell access or docker exec capability)

## Outputs

- Exit code (0 = success, non-zero = failure)
- Tool version string or help text output
- Verification log confirming tool accessibility

## How to apply

Execute a non-destructive command (e.g., help, version check) within the running CloMet container to verify the tool is accessible and responding. Run the command from within the container context (via docker exec or by interactive shell entry) and capture the exit code and stdout/stderr. Confirm that the command returns a zero exit code and produces expected output (e.g., version string, usage documentation). If errors are returned, inspect container logs and verify that volume mounts and Docker image build steps completed without warnings. This approach confirms both Docker environment integrity and tool binary availability before proceeding to data ingestion or metabolomics harmonization tasks.

## Related tools

- **Docker** (Container runtime and orchestration engine for isolated CloMet deployment)
- **CloMet** (NMR-based metabolomics harmonization tool being verified) — https://github.com/rmallol/clomet

## Examples

```
docker exec clomet_container clomet --help
```

## Evaluation signals

- Exit code is 0 when running help or version command within container
- Tool output (help text or version string) is parseable and non-empty
- No error messages or stack traces appear in stderr
- Docker container remains running and responsive after command execution
- Repeat invocation of the same verification command yields consistent output

## Limitations

- This skill only verifies basic tool accessibility; it does not validate CloMet's ability to harmonize metabolomics datasets or connect to data repositories.
- Volume mounts and file system permissions must be correctly configured before verification; this skill does not diagnose mount or permission issues.
- No changelog is available in the repository to track version-specific compatibility or known issues affecting initialization.

## Evidence

- [readme] Follow these steps to install Docker and run CloMet for the first time: "Follow these steps to install Docker and run CloMet for the first time"
- [other] Execute an initial CloMet command (e.g., help or version check) to confirm the tool is functional and accessible within the container.: "Execute an initial CloMet command (e.g., help or version check) to confirm the tool is functional and accessible within the container"
- [other] Run the CloMet container with appropriate volume mounts and verify that the containerized tool starts without errors.: "Run the CloMet container with appropriate volume mounts and verify that the containerized tool starts without errors"
