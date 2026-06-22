---
name: command-line-tool-verification
description: Use when after installing a command-line bioinformatics tool (e.g., via pip, conda, or package manager) and before attempting to use it on experimental data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - falcon
  - spectrum-utils
  - pip
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly efficient processing of millions of MS/MS spectra.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon_cq
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.9153
  all_source_dois:
  - 10.1002/rcm.9153
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# command-line-tool-verification

## Summary

Verify that a command-line scientific tool has been correctly installed and is executable by invoking it with diagnostic flags (help or version) and confirming successful output. This ensures the tool and its dependencies are properly configured before running analyses on real data.

## When to use

After installing a command-line bioinformatics tool (e.g., via pip, conda, or package manager) and before attempting to use it on experimental data. Apply this skill when you need confidence that the tool's binary is in the PATH, all runtime dependencies are satisfied, and the tool responds to basic invocations without crashing.

## When NOT to use

- Tool is already running an analysis job in production; verification is a pre-execution step, not a step to insert mid-pipeline.
- Verification of tool correctness on real data; this skill only confirms the tool responds to basic invocations, not that it produces scientifically valid results.
- Installation troubleshooting or debugging (e.g., resolving missing dependencies or permission errors); this skill assumes installation is complete and only confirms responsiveness.

## Inputs

- Installed command-line tool binary (should be in system PATH)
- Tool installation metadata (package name, version)

## Outputs

- Diagnostic output (help text or version string) printed to stdout
- Exit status code (0 for success, non-zero for failure)
- Validation signal: tool is executable and dependencies are satisfied

## How to apply

Invoke the installed tool with a diagnostic flag such as `--help`, `--version`, or `-h`. The correct application of this skill is to call the tool with these flags and verify that it returns output to standard output without raising an error code. For falcon specifically, after installing falcon-ms and spectrum-utils==0.3.5 via pip on a supported platform (Linux or OSX with Python 3.8+), run `falcon --help` or `falcon --version` and confirm the command returns without error. Success is indicated by the tool printing its help text or version string to the console and exiting with status code 0. Failure (non-zero exit code, 'command not found', or import errors) indicates a broken installation that must be debugged before proceeding to data analysis.

## Related tools

- **falcon** (Command-line spectrum clustering tool whose installation and responsiveness is verified by this skill) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Dependency of falcon (pinned to version 0.3.5) that must be co-installed and is implicitly validated when falcon responds to diagnostic invocations)
- **pip** (Package manager used to install falcon-ms and spectrum-utils; verification confirms pip installation was successful)

## Examples

```
falcon --help
```

## Evaluation signals

- Tool invocation with `--help` or `--version` returns help text or version string to stdout without error.
- Exit status code is 0 (indicating successful execution of the diagnostic invocation).
- Tool binary is found in the system PATH and is executable (no 'command not found' error).
- No import errors, missing dependency warnings, or runtime exceptions are raised during the diagnostic invocation.
- Version string output (if available) matches or is consistent with the installed package version (e.g., from `pip show falcon-ms`).

## Limitations

- This skill only verifies basic tool responsiveness; it does not validate the correctness of the tool's algorithms, the validity of output on real data, or the configuration of optional parameters.
- Verification on one platform (e.g., Linux) does not guarantee success on another (e.g., Windows); falcon is documented for Linux and OSX only, so verification should be repeated on each target platform.
- Help or version output does not confirm that all optional dependencies or plugins are installed; only the core binary and its direct imports are tested.
- falcon requires Python 3.8 or later; if an older Python version is in PATH, the tool may not be found or may fail to load, even after pip installation to the correct environment.

## Evidence

- [other] Verify installation success by invoking the falcon command-line tool with a help or version flag (e.g., falcon --help or falcon --version) and confirm the tool responds without error.: "Verify installation success by invoking the falcon command-line tool with a help or version flag (e.g., falcon --help or falcon --version) and confirm the tool responds without error."
- [readme] falcon requires Python 3.8+ and is available on the Linux and OSX platforms. You can easily install falcon with pip: pip install falcon-ms spectrum-utils==0.3.5: "falcon requires Python 3.8+ and is available on the Linux and OSX platforms. You can easily install falcon with pip: pip install falcon-ms spectrum-utils==0.3.5"
- [readme] For detailed information on all available settings, run `falcon -h` or `falcon --help`.: "For detailed information on all available settings, run `falcon -h` or `falcon --help`."
