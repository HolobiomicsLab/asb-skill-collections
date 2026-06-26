---
name: ms-dial-version-compatibility
description: Use when you are preparing to run LipoCLEAN on MS-DIAL output and need
  to create or update a configuration file, or you have switched between MS-DIAL 4
  and MS-DIAL 5 data and need to verify that your options file and trained model are
  compatible with the current version's column naming and scaling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - LipoCLEAN
  - MS-DIAL
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Generate and validate MS-DIAL version-specific configuration files

## Summary

Generate default TOML-formatted options files for MS-DIAL 4 or MS-DIAL 5 via the LipoCLEAN `--print` argument, then validate that the configuration matches the target MS-DIAL version's column schema and scaling conventions before running lipid quality filtering. This skill ensures model and configuration compatibility, since models trained on one MS-DIAL version will not work with the other.

## When to use

You are preparing to run LipoCLEAN on MS-DIAL output and need to create or update a configuration file, or you have switched between MS-DIAL 4 and MS-DIAL 5 data and need to verify that your options file and trained model are compatible with the current version's column naming and scaling.

## When NOT to use

- Your input MS-DIAL export was generated with a version other than the one you specify in the --print argument; regenerate the export first.
- You already have a manually edited and validated options.txt; only regenerate if you are switching MS-DIAL versions or need to reset to defaults.
- You are not using LipoCLEAN for lipid quality filtering; this skill is specific to LipoCLEAN's configuration workflow.

## Inputs

- MS-DIAL version identifier (4 or 5)
- Target output directory path
- Existing options.txt file (optional, for comparison)

## Outputs

- TOML-formatted options.txt configuration file
- Validated mapping between MS-DIAL version and model/column schema

## How to apply

Execute `LipoCLEAN --print MSD4` or `LipoCLEAN --print MSD5` (via executable, Conda, or Docker) to generate a version-specific options.txt file. Open the generated file and confirm it contains TOML-formatted keys appropriate for your target MS-DIAL version. Before running inference, verify that (1) the model file specified in the options matches the version (e.g., QE_Pro_model or TOF_model), (2) all column names and scaling factors in the config match MS-DIAL's output schema for that version, and (3) the MS-DIAL export used as input was generated with the same version. If upgrading from MS-DIAL 4 to 5 or vice versa, regenerate the options file rather than reusing the old one, since column names and scaling differ between versions.

## Related tools

- **LipoCLEAN** (Command-line tool that generates version-specific default configuration files via --print MSD4 or --print MSD5 arguments and applies machine learning-based quality filtering to MS-DIAL lipid identifications) — https://github.com/stavis1/LipoCLEAN
- **MS-DIAL** (Upstream mass spectrometry data analysis software whose output (alignment results exported as msp format) serves as input to LipoCLEAN; LipoCLEAN requires version-matched configuration and models)

## Examples

```
python -m lipoCLEAN --print MSD5
```

## Evaluation signals

- The generated options.txt file exists and is readable as valid TOML syntax with no parse errors
- All required configuration keys for the specified MS-DIAL version (MSD4 or MSD5) are present in the options file
- The model name in the options file matches the version (e.g., QE_Pro_model or TOF_model for the target instrument family)
- When used with MS-DIAL export data from the same version, LipoCLEAN runs without column-name mismatch errors or scaling warnings
- Regenerating the options file for the opposite version (e.g., MSD5 after using MSD4) produces a file with different column definitions or scaling factors, confirming version-specific content

## Limitations

- Models trained on MS-DIAL 4 data will not work with MS-DIAL 5 input and vice versa; separate model and configuration files are required for each version.
- Column names and scaling factors differ between MS-DIAL versions; manually created or edited options files from a different version will cause inference errors.
- The tool supports only MS-DIAL versions 4 and 5; no option generation is available for other versions.
- The --print argument generates a template; users must still edit paths and parameters (e.g., input file location) before running inference.

## Evidence

- [intro] Configuration is provided via TOML formatted text files with default options available for MS-DIAL versions 4 and 5: "all options are given to the tool in a TOML formatted text file. Default options files for MS-DIAL 4 and 5 can be obtained"
- [readme] Default options files are generated using version-specific command-line arguments: "Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively. These will create an `options.txt` file that you can edit."
- [readme] Models and configurations are version-specific and incompatible across MS-DIAL versions: "some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other. Both the options file and the model are specific to a"
- [readme] Separate default options files must be obtained for each MS-DIAL version before running inference: "We provide separate default options files for each version that can be obtained with the `--print MSD4` and `--print MSD5` command line arguments, respectively."
- [readme] Generated options.txt file serves as editable configuration template: "If you want a default version of the options file run `LipoCLEAN.exe --print MSD4`. To use the tool on other data edit the `options.txt` file."
