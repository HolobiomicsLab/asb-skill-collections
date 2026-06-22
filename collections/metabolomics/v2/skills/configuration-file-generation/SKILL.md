---
name: configuration-file-generation
description: Use when you need to set up a LipoCLEAN analysis for MS-DIAL lipid identifications and do not yet have a configuration file, or you are switching between MS-DIAL versions 4 and 5 and need version-specific parameter defaults (e.g., column names and scaling factors that differ between versions).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - LipoCLEAN
  - MS-DIAL
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
  - build: coll_lipoclean
    doi: 10.1021/acs.analchem.4c04040
    title: lipoclean
  dedup_kept_from: coll_lipoclean
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c04040
  all_source_dois:
  - 10.1021/acs.analchem.4c04040
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# configuration-file-generation

## Summary

Generate version-specific default TOML configuration files for LipoCLEAN that define MS-DIAL export locations, quality filtering parameters, and model selection. This skill enables users to obtain a template options file tailored to their MS-DIAL version (4 or 5) that can be subsequently edited for custom analyses.

## When to use

You need to set up a LipoCLEAN analysis for MS-DIAL lipid identifications and do not yet have a configuration file, or you are switching between MS-DIAL versions 4 and 5 and need version-specific parameter defaults (e.g., column names and scaling factors that differ between versions).

## When NOT to use

- You already have a valid, edited options.txt file ready for your analysis—regenerating it will overwrite your customizations.
- Your MS-DIAL export files have already been processed and you only need to rerun LipoCLEAN with the same configuration—use the existing options.txt instead.
- You are working with raw MS data that has not yet been processed by MS-DIAL—MS-DIAL must first generate alignment results and export them in msp format.

## Inputs

- MS-DIAL version identifier (4 or 5)
- Command-line access to LipoCLEAN executable, Python module, or Docker container

## Outputs

- options.txt file in TOML format containing default configuration keys and placeholders for paths and parameters

## How to apply

Execute the LipoCLEAN command-line interface with the `--print MSD4` or `--print MSD5` flag to generate a default options.txt file in TOML format. The flag choice must match your MS-DIAL version, as models and column schemas are version-specific and incompatible across versions. The generated options.txt file contains all required TOML-formatted keys for lipid quality filtering and specifies paths for MS-DIAL export files (which should be in 'msp' format with m/z matrix selected, blank filtering disabled). After generation, open the options.txt file in a text editor and customize parameters such as input/output directories, instrument model selection (e.g., QE_Pro_model or TOF_model based on your mass spectrometer), and any filtering thresholds before running the full LipoCLEAN analysis.

## Related tools

- **LipoCLEAN** (Command-line tool invoked with --print flag to generate default TOML configuration files for specified MS-DIAL versions) — https://github.com/stavis1/LipoCLEAN
- **MS-DIAL** (Upstream tool whose exported alignment results (msp format) are configured in the options.txt file for quality filtering)

## Examples

```
LipoCLEAN.exe --print MSD4
```

## Evaluation signals

- An options.txt file is created in the current working directory or specified output location after executing the --print command.
- The generated options.txt is readable as valid TOML and contains all expected configuration keys (e.g., input paths, model selection, filtering parameters).
- The file structure and column schema references are consistent with the requested MS-DIAL version (e.g., MSD4 vs MSD5 column name mappings).
- When edited with valid file paths and model selection, the options.txt can be passed to LipoCLEAN via `--options options.txt` without syntax or validation errors.
- The options.txt file contains comments or section headers explaining parameter meanings to guide user customization.

## Limitations

- Models and configuration schemas are version-specific; a model trained on MS-DIAL 4 data will not work with MS-DIAL 5 exports due to column renaming and scaling differences, so the correct --print flag (MSD4 or MSD5) must be used.
- The generated options.txt is a template and requires manual editing of file paths and instrument model selection before LipoCLEAN can execute—users must know their MS-DIAL version and instrument type (e.g., Orbitrap vs. TOF).
- The tool does not validate that the edited options.txt points to valid MS-DIAL export files until LipoCLEAN is run with the --options flag, so typos or missing paths will only be caught at execution time.

## Evidence

- [readme] Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively. These will create an `options.txt` file that you can edit.: "Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively. These will create an `options.txt` file that you can edit."
- [readme] All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file.: "All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file."
- [readme] However, some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other. Both the options file and the model are specific to a version of MS-DIAL.: "However, some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other. Both the options file and the model are"
- [readme] If you want a default version of the options file run `LipoCLEAN.exe --print MSD4`.: "If you want a default version of the options file run `LipoCLEAN.exe --print MSD4`."
- [other] Configuration is provided via TOML formatted text files with default options available for MS-DIAL versions 4 and 5: "Configuration is provided via TOML formatted text files with default options available for MS-DIAL versions 4 and 5"
