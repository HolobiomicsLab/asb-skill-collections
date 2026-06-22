---
name: ms-dial-export-file-specification
description: Use when you have MS-DIAL 4 or MS-DIAL 5 alignment results and need to configure LipoCLEAN for quality filtering of lipid identifications. Use this skill at the start of a LipoCLEAN analysis when you need to specify which MS-DIAL export files to analyze and how to locate them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - LipoCLEAN
  - MS-DIAL 4
  - MS-DIAL 5
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.4c04040
  title: lipoclean
evidence_spans:
- LipoCLEAN is a command line tool
- Default options files for MS-DIAL 4 and 5
- a machine learning based quality filter for lipid identifications from MS-DIAL
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-dial-export-file-specification

## Summary

Generate version-specific default TOML-formatted configuration files for LipoCLEAN that specify MS-DIAL export file locations and filtering parameters. This skill bridges MS-DIAL's lipid identification output and LipoCLEAN's machine learning quality filter by establishing the correct export settings and file format expectations.

## When to use

You have MS-DIAL 4 or MS-DIAL 5 alignment results and need to configure LipoCLEAN for quality filtering of lipid identifications. Use this skill at the start of a LipoCLEAN analysis when you need to specify which MS-DIAL export files to analyze and how to locate them.

## When NOT to use

- You are using a different lipid identification tool (not MS-DIAL); LipoCLEAN is specifically designed for MS-DIAL export format.
- Your MS-DIAL export has already been filtered or preprocessed; this skill establishes the initial export specification, not post-hoc correction.
- You do not have write access to the analysis directory; the generated options.txt file must be editable and the working directory must be writable for LipoCLEAN to function.

## Inputs

- MS-DIAL 4 or MS-DIAL 5 alignment results (in-memory or from project file)
- LipoCLEAN executable or module with --print capability

## Outputs

- TOML-formatted options.txt file with version-specific default configuration
- Tab-delimited MS-DIAL export file (.txt, named 'Mz*') containing m/z matrix and lipid identifications

## How to apply

Invoke LipoCLEAN with `--print MSD4` or `--print MSD5` (depending on your MS-DIAL version) to generate a default TOML-formatted `options.txt` file. Review the generated file to confirm all required configuration fields for MS-DIAL export file paths and filtering parameters are present. Before running LipoCLEAN, export alignment results from MS-DIAL using the exact settings specified: select 'Alignment result' export type, enable 'm/z matrix' export, disable blank filtering, and set export format to 'msp'. The resulting .txt file (named starting with 'Mz') contains the tab-delimited data required by LipoCLEAN. Edit the generated `options.txt` to specify the path to your MS-DIAL export file(s), ensuring the file format and column structure match the version-specific schema (MS-DIAL 4 and 5 have different column names and scaling). The TOML syntax and column structure must be valid before passing the options file to the LipoCLEAN execution step.

## Related tools

- **LipoCLEAN** (Command-line tool that generates version-specific default TOML options files via --print argument and executes quality filtering using MS-DIAL export specifications) — https://github.com/stavis1/LipoCLEAN
- **MS-DIAL 4** (Upstream tool providing lipid identification and alignment results; must be configured to export in 'msp' format with m/z matrix enabled)
- **MS-DIAL 5** (Upstream tool providing lipid identification and alignment results with renamed columns and different scaling than MS-DIAL 4; requires version-specific options file)

## Examples

```
LipoCLEAN.exe --print MSD4
```

## Evaluation signals

- Generated options.txt file is valid TOML syntax with no parsing errors
- All required configuration fields (MS-DIAL export file path, filtering parameters) are present and populated in the options.txt
- MS-DIAL export file (.txt, starting with 'Mz') exists at the path specified in options.txt and contains tab-delimited data with expected columns for the specified MS-DIAL version
- The 'label' column (if present for training data) is positioned before (to the left of) the 'MS/MS spectrum' column
- Export was performed with blank filtering disabled, m/z matrix selected, and export format set to 'msp', as confirmed by checking MS-DIAL project export log or re-exporting with correct settings

## Limitations

- Models and options files are specific to MS-DIAL version; a model trained on MS-DIAL 4 will not work with MS-DIAL 5 data due to column name changes and scaling differences.
- The tool expects exactly the export settings specified in the README (m/z matrix, msp format, blank filtering off); deviations in export configuration will cause parsing or accuracy failures.
- LipoCLEAN requires a trained machine learning model for the specific instrument type (QE_Pro_model for Orbitrap systems, TOF_model for time-of-flight); models may not generalize beyond their instrument family without validation.
- On some systems, a warning 'No module named brainpy._c.composition' may appear; this does not indicate an error but may signal missing optional dependencies.

## Evidence

- [readme] Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively.: "Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively."
- [readme] All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file.: "All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file."
- [readme] These will create an `options.txt` file that you can edit.: "These will create an `options.txt` file that you can edit."
- [readme] Select 'm/z matrix' to be exported (deselect any other exports you do not want to generate): "Select 'm/z matrix' to be exported (deselect any other exports you do not want to generate)"
- [readme] Make sure blank filtering is NOT selected. 'Export format' should be 'msp'.: "Make sure blank filtering is NOT selected. 'Export format' should be 'msp'."
- [readme] Our tool supports both MS-DIAL 4 and 5. However, some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other.: "Our tool supports both MS-DIAL 4 and 5. However, some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other."
