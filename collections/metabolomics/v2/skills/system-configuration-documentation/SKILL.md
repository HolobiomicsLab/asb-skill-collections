---
name: system-configuration-documentation
description: Use when after successfully installing and validating all components of a complex multi-tool workflow (such as ENPKG), when you have confirmed that all dependencies resolve, external tools (e.g., Sirius, MZmine) are accessible at their expected paths, and test commands execute without error.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3489
  tools:
  - uv
  - Sirius
  - GraphDB
  - enpkg_full
derived_from:
- doi: 10.1021/acscentsci.3c00800
  title: enpkg
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enpkg_cq
    doi: 10.1021/acscentsci.3c00800
    title: enpkg
  dedup_kept_from: coll_enpkg_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.3c00800
  all_source_dois:
  - 10.1021/acscentsci.3c00800
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# System Configuration Documentation

## Summary

Capture and record the environment configuration, dependency versions, system paths, and tool settings required to reproduce a computational workflow. This skill ensures that future executions can be validated against a baseline configuration and troubleshooting can reference the exact state in which the workflow was last known to work.

## When to use

After successfully installing and validating all components of a complex multi-tool workflow (such as ENPKG), when you have confirmed that all dependencies resolve, external tools (e.g., Sirius, MZmine) are accessible at their expected paths, and test commands execute without error. Document this snapshot before launching large-scale analyses to enable reproducibility and debugging.

## When NOT to use

- If the installation has not yet been validated (skip this skill until all setup validation checks pass and test commands execute cleanly).
- If the workflow is being run on a managed cluster or cloud environment where system configuration is ephemeral or auto-provisioned (document only user-controlled parameters and environment variables, not transient system state).
- If documenting configuration is not part of your project's reproducibility or compliance requirements (this skill adds overhead and is most valuable for long-term or collaborative workflows).

## Inputs

- Activated Python/Conda environment with all dependencies installed
- Installed external tools (Sirius, MZmine, GraphDB, etc.) at their configured paths
- .env file with machine-specific variables (PATH_TO_SIRIUS, SIRIUS_USERNAME, etc.)
- Completed setup validation tests (e.g., successful test workflow execution)

## Outputs

- Setup configuration report (plain text, JSON, or YAML file)
- Environment freeze/export file (pip freeze output or conda environment.yml)
- System information document (OS, CPU, RAM, disk space)
- Verification checklist with pass/fail status for each component

## How to apply

After completing installation and running verification tests, create a structured setup report that captures: (1) Python version and package versions in the active environment (use `uv pip freeze` or `conda list`); (2) absolute file system paths to critical external tools (e.g., PATH_TO_SIRIUS, MZmine executable location); (3) all environment variables loaded from `.env` or shell session (credentials and paths, excluding secrets); (4) OS and CPU architecture; (5) system RAM and disk space available; (6) version strings of dependent services (e.g., GraphDB, Java runtime). Store this report in a version-controlled location or alongside workflow outputs. When re-running the workflow on a different system or after dependency updates, compare the new configuration against the baseline report to identify version mismatches or path divergences that may explain unexpected failures.

## Related tools

- **uv** (Dependency manager and Python environment tool; used to create isolated .venv and freeze/export dependency versions) — https://docs.astral.sh/uv/latest/
- **Sirius** (External spectral annotation tool whose installation path and credentials must be captured in environment configuration) — https://boecker-lab.github.io/docs.sirius.github.io/install/
- **GraphDB** (RDF knowledge graph store; version and configuration must be documented for knowledge graph exploration) — https://graphdb.ontotext.com/download/
- **enpkg_full** (The parent workflow repository; its setup documentation and .env template define the configuration schema) — https://github.com/enpkg/enpkg_full

## Examples

```
uv pip freeze > environment_freeze.txt && python -c "import platform; print(f'OS: {platform.system()}\nArch: {platform.machine()}\nPython: {platform.python_version()}')" && echo "Configuration documented. Compare against baseline: diff environment_freeze.txt baseline_freeze.txt"
```

## Evaluation signals

- Configuration report is complete and contains all required fields (Python version, tool paths, environment variables, OS/CPU, RAM) with no missing or empty values.
- All paths in the configuration report resolve (can be verified by running `ls -la` or `where` on each tool path; no 'file not found' errors).
- Environment freeze/export file contains pinned versions for all dependencies; no 'version any' or floating version specifiers remain.
- Setup validation tests re-run against the documented configuration and produce identical pass/fail results, confirming reproducibility.
- Comparison of baseline configuration against a new system configuration identifies all divergences (version mismatches, missing tools, path conflicts) with actionable diagnostic output.

## Limitations

- Configuration documentation captures the state at a single point in time; it does not track how the environment evolves if packages are updated or tools are patched after documentation.
- System-level dependencies (Java, system libraries, graphical drivers) may not be fully captured by Python package freezes or environment variable exports; manual inspection of system package managers (apt, brew, conda) may be required.
- Credentials and API keys stored in .env files must be excluded from version control and shared reports; only the structure and non-sensitive parameter names should be documented.
- Platform-specific paths (e.g., /opt/sirius on Linux vs. /opt/sirius.app on macOS) and OS/CPU architecture mismatches can cause configuration divergence across systems; the report must be regenerated for each target platform.

## Evidence

- [other] Verify the installation by running provided setup validation checks or test commands to confirm all components are correctly configured.: "Verify the installation by running provided setup validation checks or test commands to confirm all components are correctly configured."
- [other] Document the environment configuration details (versions, paths, system information) in a setup report.: "Document the environment configuration details (versions, paths, system information) in a setup report."
- [readme] Runtime secrets and machine-specific paths (e.g., PATH_TO_SIRIUS, SIRIUS_USERNAME, SIRIUS_PASSWORD) live in a .env file that is ignored by git. Configure it as follows: cp .env.example .env. Edit .env with your editor of choice and provide the correct values (absolute path to the Sirius executable, Sirius account credentials, etc.). Before running the workflow, load the file into your shell session.: "Runtime secrets and machine-specific paths (e.g., PATH_TO_SIRIUS, SIRIUS_USERNAME, SIRIUS_PASSWORD) live in a .env file"
- [readme] With uv installed, sync the project dependencies into an isolated .venv: uv python install 3.11; uv sync: "With uv installed, sync the project dependencies into an isolated .venv"
- [readme] The script auto-detects the OS/CPU, but you can override them (e.g. macos x64) if needed. After installation, identify the full path to the sirius binary and store it in .env as PATH_TO_SIRIUS.: "identify the full path to the sirius binary and store it in .env as PATH_TO_SIRIUS"
