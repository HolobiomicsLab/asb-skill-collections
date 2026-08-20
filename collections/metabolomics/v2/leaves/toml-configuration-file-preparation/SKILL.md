---
name: toml-configuration-file-preparation
description: Use when you have exported lipid identifications from MS-DIAL (version
  4 or 5) and need to run LipoCLEAN quality filtering on that output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - LipoCLEAN
  - MS-DIAL
  techniques:
  - ion-mobility-MS
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

# TOML Configuration File Preparation for LipoCLEAN

## Summary

Prepare a TOML-formatted options file to configure LipoCLEAN's machine learning lipid filter with MS-DIAL export locations and version-specific parameters. This is a prerequisite step that translates MS-DIAL dataset locations and tool settings into a structured configuration consumable by the LipoCLEAN command-line interface.

## When to use

You have exported lipid identifications from MS-DIAL (version 4 or 5) and need to run LipoCLEAN quality filtering on that output. The TOML configuration file specifies which MS-DIAL export files to analyze and which pre-trained model (QE_Pro_model or TOF_model) to apply, making it necessary before any LipoCLEAN execution.

## When NOT to use

- MS-DIAL exports already include blank filtering enabled — regenerate exports with blank filtering deselected before configuring TOML
- You are using a custom-trained model not listed in the provided instrument/model table — prepare training data first rather than configuring for inference
- Input data is already pre-filtered or has been processed by a different lipid identification tool — TOML preparation is specific to MS-DIAL outputs

## Inputs

- MS-DIAL alignment result export (msp or .txt format from m/z matrix export)
- MS-DIAL version identifier (4 or 5)
- Target output directory path

## Outputs

- TOML-formatted options.txt configuration file
- Validated file path references and model selection metadata

## How to apply

Generate a default TOML template by running `LipoCLEAN --print MSD4` or `--print MSD5` (depending on your MS-DIAL version) to create an options.txt file. Open the generated file and edit it to specify the directory path(s) containing your MS-DIAL export files (typically .txt files starting with 'Mz' from the m/z matrix export). Ensure the blank filtering setting is NOT enabled in MS-DIAL exports beforehand. If using a non-standard instrument family (e.g., TimsTOF instead of Orbitrap), validate the model choice in the TOML against your instrument type, as models are instrument-family-specific. Save the edited TOML file and verify it is readable by attempting a test invocation with the `--help` flag to confirm syntax acceptance.

## Related tools

- **LipoCLEAN** (Machine learning lipid identification quality filter that consumes the TOML configuration to filter MS-DIAL identifications) — https://github.com/stavis1/LipoCLEAN
- **MS-DIAL** (Metabolomics data analysis platform whose lipid identification output is configured and referenced in the TOML file)

## Examples

```
LipoCLEAN.exe --print MSD4 > options.txt && [edit options.txt to add path to MS-DIAL export] && LipoCLEAN.exe --options options.txt
```

## Evaluation signals

- TOML file is syntactically valid and parseable by the TOML parser (no parsing errors when LipoCLEAN reads it)
- Specified MS-DIAL export file paths exist and contain .txt files with column headers matching MS-DIAL 4 or 5 format (version-specific column names match the selected model)
- Selected model (QE_Pro_model for Orbitrap instruments, TOF_model for time-of-flight) is appropriate for declared instrument type
- Output directory path is writable and LipoCLEAN successfully generates example_output/ folder and QC plots when invoked with the configuration
- If using a non-Orbitrap or non-standard-TOF instrument, validation plots in example_output/QC/ show reasonable lipid retention time and m/z distributions without systematic biases

## Limitations

- Models are instrument-family-specific and have not been validated on all TOF variants (e.g., TimsTOF) — use at-risk on instruments outside the training dataset instrument families (Q-Exactive, LTQ Velos Pro, TripleTOF 6600)
- Column names and scaling differ between MS-DIAL versions 4 and 5; a TOML configuration and model trained on one version will not work correctly with the other version
- Blank filtering must be disabled in MS-DIAL exports before LipoCLEAN configuration — the tool does not post-hoc apply blank filtering if it was included in the export
- The TOML file does not support per-input-file retention time correction parameters — correction is applied on a per-file basis but cannot be customized at configuration time

## Evidence

- [readme] All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file.: "All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file."
- [readme] Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively.: "Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively."
- [readme] Make sure blank filtering is NOT selected: "Make sure blank filtering is NOT selected"
- [readme] Our tests have shown that a model will likely generalize to a family of instruments but that this has limits. We expect that the QE_Pro_model will work for all Orbitrap systems.: "Our tests have shown that a model will likely generalize to a family of instruments but that this has limits. We expect that the QE_Pro_model will work for all Orbitrap systems."
- [readme] Some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other.: "Some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other."
