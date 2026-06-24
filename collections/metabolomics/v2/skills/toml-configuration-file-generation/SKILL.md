---
name: toml-configuration-file-generation
description: Use when when beginning a LipoCLEAN analysis workflow and needing to
  configure MS-DIAL export file locations, filtering parameters, and other tool options.
  Specifically when you have MS-DIAL 4 or MS-DIAL 5 exported data and need to prepare
  an options.txt file before running lipid quality filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - LipoCLEAN
  - MS-DIAL 4
  - MS-DIAL 5
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.4c04040
  title: lipoclean
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
  dedup_kept_from: coll_lipoclean_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c04040
  all_source_dois:
  - 10.1021/acs.analchem.4c04040
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# toml-configuration-file-generation

## Summary

Generate version-specific default TOML-formatted configuration files for MS-DIAL integration by invoking command-line print arguments. This skill enables rapid initialization of tool-specific options files that users can then customize for their analysis pipeline.

## When to use

When beginning a LipoCLEAN analysis workflow and needing to configure MS-DIAL export file locations, filtering parameters, and other tool options. Specifically when you have MS-DIAL 4 or MS-DIAL 5 exported data and need to prepare an options.txt file before running lipid quality filtering.

## When NOT to use

- If you already have an existing, validated options.txt file from a previous analysis that you wish to reuse — regenerating it may overwrite customizations.
- If your MS-DIAL export files are from a version different from those available in the print arguments (e.g., MS-DIAL 6 or earlier versions like MS-DIAL 3) — the generated defaults will not be compatible.
- If you need to generate a training data configuration file — the README notes that training data preparation requires a different tab-delimited format with a label column, not TOML options files.

## Inputs

- MS-DIAL version identifier (4 or 5)
- Command-line invocation environment (terminal/shell access to LipoCLEAN)

## Outputs

- options.txt file (TOML-formatted)
- Default configuration with populated fields for MS-DIAL export file paths and tool parameters

## How to apply

Invoke LipoCLEAN with either the `--print MSD4` command-line argument (for MS-DIAL 4 data) or `--print MSD5` argument (for MS-DIAL 5 data) to generate a version-specific default TOML-formatted options file. The generated options.txt file will contain all required configuration fields including MS-DIAL export file locations and filtering parameters pre-populated with sensible defaults. This file can then be edited in a text editor to specify your actual data paths and override parameters as needed. The version-specific generation is critical because MS-DIAL 4 and 5 use different column names and scaling, so models and configuration structures are not interchangeable between versions. Verify the generated file contains valid TOML syntax and all expected sections before proceeding to the analysis step.

## Related tools

- **LipoCLEAN** (Command-line tool invoked with --print MSD4 or --print MSD5 arguments to generate version-specific TOML configuration files) — https://github.com/stavis1/LipoCLEAN
- **MS-DIAL 4** (Source data format; LipoCLEAN must be configured with version-specific defaults when processing MS-DIAL 4 exports)
- **MS-DIAL 5** (Source data format; LipoCLEAN must be configured with version-specific defaults when processing MS-DIAL 5 exports)

## Examples

```
LipoCLEAN.exe --print MSD4
```

## Evaluation signals

- Generated options.txt file is valid TOML syntax (can be parsed by a TOML parser without errors)
- File contains all required configuration fields documented for the specified MS-DIAL version
- File name is exactly options.txt and is located in the current working directory where the command was invoked
- All template placeholders are present and readable for user customization (e.g., paths to MS-DIAL export files are clearly marked or provided with example syntax)
- No validation errors are reported when the generated options.txt is subsequently used with the LipoCLEAN `--options` argument in a dry-run or help mode

## Limitations

- Models and options files are version-specific to MS-DIAL; a configuration generated with --print MSD4 will not work with MS-DIAL 5 data and vice versa.
- The tool does not validate that specified MS-DIAL export file locations actually exist until runtime during the full analysis step.
- Generated defaults may require significant user customization depending on non-standard analysis parameters or export configurations.
- No changelog is provided in the repository, so differences between default options across LipoCLEAN versions are not documented.

## Evidence

- [readme] Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively.: "Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively."
- [readme] These will create an `options.txt` file that you can edit.: "These will create an `options.txt` file that you can edit."
- [readme] All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file.: "All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file."
- [readme] some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other.: "some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other."
- [readme] Both the options file and the model are specific to a version of MS-DIAL.: "Both the options file and the model are specific to a version of MS-DIAL."
