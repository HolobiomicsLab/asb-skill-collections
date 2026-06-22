---
name: command-line-interface-invocation
description: Use when when you have installed a Python package and need to verify that its command-line entry point is accessible, or when you need to discover available commands and options for NMR data processing workflows without consulting external documentation.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - metabolabpy
  - Python
derived_from:
- doi: 10.3390/metabo15010048
  title: MetaboLabPy
evidence_spans:
- github.com__ludwigc__metabolabpy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabolabpy_cq
    doi: 10.3390/metabo15010048
    title: MetaboLabPy
  dedup_kept_from: coll_metabolabpy_cq
schema_version: 0.2.0
---

# command-line-interface-invocation

## Summary

Invoke a Python package's command-line interface entry point to access tool functionality and display usage documentation. This skill verifies that a CLI is properly exposed and responds to standard help flags.

## When to use

When you have installed a Python package and need to verify that its command-line entry point is accessible, or when you need to discover available commands and options for NMR data processing workflows without consulting external documentation.

## When NOT to use

- Package installation failed or entry point is not registered in setup.py/pyproject.toml
- You need to run actual NMR data processing — this skill only verifies CLI availability, not data analysis

## Inputs

- Installed Python package with registered command-line entry point
- System shell environment with package in PATH

## Outputs

- Help text output containing usage information and command documentation
- Confirmation that the command-line interface is accessible and functional

## How to apply

After installing the package in development mode (pip install -e .), invoke the command-line entry point name followed by the '--help' flag at the system shell. For MetaboLabPy, execute `metabolabpy --help` to retrieve usage information and command documentation. Capture and validate the help output text for presence of structured usage information and command documentation. This confirms the entry point is properly registered and the package is ready for data processing tasks.

## Related tools

- **metabolabpy** (command-line entry point for NMR spectroscopic data processing) — https://github.com/ludwigc/MetaboLabPy
- **Python** (language runtime and package management context)

## Examples

```
metabolabpy --help
```

## Evaluation signals

- Help output is displayed without error and contains usage documentation
- Exit code is 0 (successful execution)
- Output text includes structured information about available commands or flags
- Command responds consistently across repeated invocations
- No traceback or import errors appear in stderr

## Limitations

- This skill only verifies CLI accessibility, not the correctness or functionality of downstream commands
- The '--help' flag must be explicitly supported by the entry point implementation
- Package must be installed in an environment where the entry point is registered in PATH

## Evidence

- [other] Does the MetaboLabPy package expose a command-line interface entry point named 'metabolabpy' that responds to the '--help' flag?: "Does the MetaboLabPy package expose a command-line interface entry point named 'metabolabpy' that responds to the '--help' flag?"
- [other] MetaboLabPy provides a command-line interface accessible via the 'metabolabpy' command that accepts a '--help' flag to display usage information.: "MetaboLabPy provides a command-line interface accessible via the 'metabolabpy' command that accepts a '--help' flag to display usage information."
- [other] Execute the command `metabolabpy --help` at the system shell. Capture and validate the help output text for presence of usage information and command documentation.: "Execute the command `metabolabpy --help` at the system shell. Capture and validate the help output text for presence of usage information and command documentation."
- [other] Install the package in development mode using pip install -e . from the repository root.: "Install the package in development mode using pip install -e . from the repository root."
- [readme] $ metabolabpy --help: "$ metabolabpy --help"
