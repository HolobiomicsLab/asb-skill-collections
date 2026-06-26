---
name: package-entry-point-verification
description: Use when you need to confirm that a Python package (especially one distributed
  via pip or conda) has been correctly configured with a console script entry point
  and that the CLI is callable from the system shell.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - metabolabpy
  - Python
  license_tier: open
  provenance_tier: literature
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo15010048
  all_source_dois:
  - 10.3390/metabo15010048
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# package-entry-point-verification

## Summary

Verify that a Python package exposes a functional command-line interface (CLI) entry point by installing the package and testing it against the `--help` flag. This skill confirms that the package's setup configuration correctly registers a console script entry point and that the CLI responds with valid usage documentation.

## When to use

Use this skill when you need to confirm that a Python package (especially one distributed via pip or conda) has been correctly configured with a console script entry point and that the CLI is callable from the system shell. This is particularly useful after cloning a development repository, installing an updated package version, or validating CI/CD deployment configurations for command-line tools.

## When NOT to use

- The package is already installed system-wide or in a virtual environment and you only need to invoke the CLI without validation—just call the command directly.
- The package does not declare any console script entry points and is designed only as an importable library module.
- You are testing internal module functions rather than public CLI user interfaces.

## Inputs

- Python package source code repository
- Package setup.py or pyproject.toml with console_scripts or entry_points configuration

## Outputs

- CLI help text (stdout)
- Exit code (0 on success, non-zero on failure)
- Validation report confirming entry point accessibility and help output presence

## How to apply

Clone or obtain the source repository of the target Python package. Install the package in development mode (using `pip install -e .` from the repository root) to ensure entry points are registered. Execute the entry point command (e.g., `metabolabpy --help`) at the system shell. Capture the help output and verify that it contains expected sections: usage information, command documentation, available flags, and option descriptions. The presence of structured help text indicates the entry point is correctly wired; absence or error messages indicate a configuration or installation failure.

## Related tools

- **metabolabpy** (CLI entry point target being verified for accessibility and help documentation) — https://github.com/ludwigc/MetaboLabPy
- **Python** (Runtime environment and package management via pip for installing and testing the entry point)

## Examples

```
pip install -e . && metabolabpy --help
```

## Evaluation signals

- The command `metabolabpy --help` completes with exit code 0 (success).
- Help output contains structured documentation including usage syntax and flag descriptions, not an error traceback.
- The entry point name matches the declared console_scripts entry in setup.py or pyproject.toml.
- Help text is produced on stdout (not stderr) and is non-empty (>0 characters).
- Repeated calls to `metabolabpy --help` produce consistent output, indicating stable registration.

## Limitations

- This skill verifies only the CLI entry point mechanism itself; it does not validate the correctness of the underlying command logic or subcommands.
- Installation in development mode (`pip install -e .`) is required; testing a pre-built wheel or system package may not reflect live repository state.
- Platform-specific shell environments (Windows CMD, PowerShell, bash, zsh) may behave differently; test in the target deployment environment.
- The package README observed in this analysis contains no changelog, limiting ability to track when entry point support was added or modified.

## Evidence

- [other] research_question: Does the MetaboLabPy package expose a command-line interface entry point named 'metabolabpy' that responds to the '--help' flag?: "Does the MetaboLabPy package expose a command-line interface entry point named 'metabolabpy' that responds to the '--help' flag?"
- [other] MetaboLabPy provides a command-line interface accessible via the 'metabolabpy' command that accepts a '--help' flag to display usage information.: "MetaboLabPy provides a command-line interface accessible via the 'metabolabpy' command that accepts a '--help' flag to display usage information."
- [other] Execute the command `metabolabpy --help` at the system shell. Capture and validate the help output text for presence of usage information and command documentation.: "Execute the command `metabolabpy --help` at the system shell. Capture and validate the help output text for presence of usage information and command documentation."
- [other] Install the package in development mode using pip install -e . from the repository root.: "Install the package in development mode using pip install -e . from the repository root."
- [readme] Command line :: $ metabolabpy --help: "$ metabolabpy --help"
