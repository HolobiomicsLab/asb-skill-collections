---
name: command-line-tool-invocation
description: Use when you need to bootstrap a tool workflow by generating a version- or instrument-specific default configuration file (e.g., for MS-DIAL 4 vs. 5), execute an analysis on formatted input files (e.g., MS-DIAL export .txt files), or capture tool output for downstream validation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - LipoCLEAN
  - MS-DIAL 4
  - MS-DIAL 5
  - Docker
  - OpenMS
  - Rust (cargo)
  - mzpeak_prototyping
  - Apache Parquet
derived_from:
- doi: 10.1021/acs.analchem.4c04040
  title: lipoclean
- doi: 10.1021/acs.jproteome.5c00435
  title: ''
evidence_spans:
- LipoCLEAN is a command line tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipoclean_cq
    doi: 10.1021/acs.analchem.4c04040
    title: lipoclean
  - build: coll_mzpeak
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  dedup_kept_from: coll_lipoclean_cq
schema_version: 0.2.0
---

# command-line-tool-invocation

## Summary

Invoke command-line bioinformatics tools with version-specific or mode-specific arguments to generate configuration files, run analyses, or produce formatted output. This skill is essential for reproducible automation of tool-driven workflows where configuration and execution are separated.

## When to use

Use this skill when you need to bootstrap a tool workflow by generating a version- or instrument-specific default configuration file (e.g., for MS-DIAL 4 vs. 5), execute an analysis on formatted input files (e.g., MS-DIAL export .txt files), or capture tool output for downstream validation. Triggers include: (1) first-time tool setup with no existing options file, (2) version migration (MS-DIAL 4 → 5), or (3) need to validate tool output format before full-scale analysis.

## When NOT to use

- Input is already a fully configured, version-matched options file in use by the same tool version — regenerating it will overwrite manual edits.
- Tool invocation is non-interactive or embedded in a compiled pipeline — use API or programmatic bindings instead of shell commands.
- Analysis environment does not support the chosen invocation method (e.g., Docker unavailable on the deployment system, or Conda not installed).

## Inputs

- Command-line invocation context (shell/bash/cmd.exe)
- Version specifier (e.g., 'MSD4', 'MSD5')
- Optionally: existing TOML options file for editing

## Outputs

- TOML-formatted options.txt configuration file
- Tool log file (e.g., LipoCLEAN.log) with execution summary
- Analysis results directory (e.g., example_output/)

## How to apply

Invoke the tool via its executable, Python module, or Docker image using the `--print` flag with a version specifier (e.g., `--print MSD4` or `--print MSD5`) to generate a default TOML-formatted `options.txt` file. Capture and validate the generated file for correct TOML syntax and required fields (e.g., MS-DIAL export file paths, model selection, filtering parameters). Then edit the options file to specify input/output paths and instrument-specific parameters before running the full analysis with the `--options` argument pointing to your customized configuration. Choose invocation method (executable, Python package, or Docker) based on environment constraints and performance requirements; note that executable is slowest but requires no installation, while Conda package is faster but requires environment setup.

## Related tools

- **LipoCLEAN** (Primary tool invoked via command-line to generate version-specific configuration files and execute lipid quality filtering on MS-DIAL exports.) — https://github.com/stavis1/lipoCLEAN
- **MS-DIAL 4** (Data source; LipoCLEAN generates MS-DIAL-4-specific default options via --print MSD4.)
- **MS-DIAL 5** (Data source; LipoCLEAN generates MS-DIAL-5-specific default options via --print MSD5.)
- **Docker** (Execution environment for LipoCLEAN; allows tool invocation without local installation via docker run with mounted data volumes.)

## Examples

```
LipoCLEAN.exe --print MSD4
```

## Evaluation signals

- Generated options.txt file is valid TOML syntax (parseable by standard TOML readers) and contains all required fields for the specified MS-DIAL version.
- Version-specific fields in the generated file match the invoked version specifier (e.g., --print MSD4 produces MSD4-compatible column names and scaling; --print MSD5 produces MSD5-compatible variants).
- Tool produces a log file (LipoCLEAN.log) documenting invocation parameters, input file validation, and execution status without fatal errors.
- Executable/package/Docker invocation method is supported on the target operating system (Windows 10, Ubuntu 22.04 confirmed; Macs with Intel chips and other systems with Conda should work but are untested).
- Analysis output directory (e.g., example_output/) is created with expected subdirectories (e.g., QC/ for plots) and result files, confirming successful tool execution.

## Limitations

- Models trained on one MS-DIAL version (4 vs. 5) do not generalize to the other due to renamed columns and different scaling; version mismatch will produce incorrect predictions.
- On some systems, the warning 'No module named brainpy._c.composition' appears during invocation; this is cosmetic and does not affect tool execution, but may cause user confusion.
- LipoCLEAN executable version is slower than Conda or Docker alternatives due to lack of pre-compiled optimization; for large-scale analyses, Conda or Docker is preferred.
- Instrument-model generalization is limited: QE_Pro_model is expected to work on all Orbitrap systems, but TOF_model generalization to all TOF instruments (e.g., TimsTOF) is unknown and should be validated before production use.
- The tool is not associated with MS-DIAL developers; configuration must follow MS-DIAL export conventions (msp format, m/z matrix export, blank filtering disabled) or analysis will fail.

## Evidence

- [readme] Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively.: "Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively."
- [readme] These will create an `options.txt` file that you can edit.: "These will create an `options.txt` file that you can edit."
- [readme] All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file.: "All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file."
- [readme] Run `LipoCLEAN.exe --print MSD4`. ... To use the tool on other data edit the `options.txt` file.: "Run `LipoCLEAN.exe --print MSD4`. ... To use the tool on other data edit the `options.txt` file."
- [readme] some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other.: "some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other."
- [readme] There are three ways to install and run LipoCLEAN: as an executable, as a Python package, and as a Docker container: "There are three ways to install and run LipoCLEAN: as an executable, as a Python package, and as a Docker container"
- [readme] On some systems the warning `No module named 'brainpy._c.composition'` will be displayed. This is not an error and does not impact the running of the tool.: "On some systems the warning `No module named 'brainpy._c.composition'` will be displayed. This is not an error and does not impact the running of the tool."
