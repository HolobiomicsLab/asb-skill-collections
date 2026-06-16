---
name: lipid-identification-quality-filtering
description: Use when you have MS-DIAL lipid identification results (alignment exports in msp/txt format) and need to distinguish correct from incorrect lipid IDs before downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipoclean
    doi: 10.1021/acs.analchem.4c04040
    title: lipoclean
  dedup_kept_from: coll_lipoclean
schema_version: 0.2.0
---

# lipid-identification-quality-filtering

## Summary

Apply machine learning-based quality filtering to lipid identifications exported from MS-DIAL to remove incorrect identifications and improve annotation reliability. This skill uses LipoCLEAN to score and filter lipid hits based on instrument-specific models trained on manually curated MS-DIAL datasets.

## When to use

You have MS-DIAL lipid identification results (alignment exports in msp/txt format) and need to distinguish correct from incorrect lipid IDs before downstream analysis. Apply this skill when you lack manual curation resources or when you want to systematically filter MS-DIAL output using learned patterns from instrument families (Orbitrap, TOF).

## When NOT to use

- Your MS-DIAL export used non-standard settings (e.g., blank filtering enabled, export format other than msp, or columns manually removed) — LipoCLEAN expects column structure specific to the MS-DIAL version.
- You are working with an instrument family not in the training set (e.g., a novel TOF variant) without prior validation — the tool's generalization limits are acknowledged for non-Orbitrap and non-standard-TOF instruments.
- Your data has already been manually curated or filtered by other means — applying LipoCLEAN will re-score identifications and may introduce inconsistency with existing curation.

## Inputs

- MS-DIAL alignment result export (msp/txt format with m/z matrix)
- TOML-formatted options file specifying MS-DIAL version (4 or 5), export file path, and output directory

## Outputs

- Filtered lipid identification table (tab-delimited txt format)
- Quality control plots and assessment visualizations (in QC/ subdirectory)
- LipoCLEAN.log file containing execution details and filtering statistics

## How to apply

First, export your MS-DIAL alignment results using the specified export settings: select 'Alignment result', choose m/z matrix export format (msp), and ensure blank filtering is NOT selected. Second, generate or prepare a TOML-formatted options file specifying the MS-DIAL export file location and output directory; use `--print MSD4` or `--print MSD5` to obtain a version-appropriate template. Third, invoke LipoCLEAN with the options file via your chosen installation method (executable, Conda, or Docker). Fourth, inspect the output folder for filtered lipid identifications and QC plots in `example_output/QC/` to assess confidence in the filtering results. The tool applies an instrument-specific trained model (QE_Pro_model for Orbitrap systems, TOF_model for time-of-flight) that has learned patterns of correct vs. incorrect identifications; validation is critical if using instruments outside the training set (e.g., TimsTOF).

## Related tools

- **LipoCLEAN** (Command-line tool that applies machine learning models to score and filter MS-DIAL lipid identifications) — https://github.com/stavis1/LipoCLEAN
- **MS-DIAL** (Metabolomics software that produces the lipid identification alignment results that LipoCLEAN filters)

## Examples

```
LipoCLEAN.exe --print MSD4 > options.txt && LipoCLEAN.exe --options options.txt
```

## Evaluation signals

- Output folder contains `example_output/` with filtered lipid table and QC/ subdirectory plots
- LipoCLEAN.log file completes without critical errors (warnings like 'No module named brainpy._c.composition' are expected and non-fatal)
- QC plots (e.g., model score distributions, retention time alignment plots) show expected patterns consistent with the training instrument type
- Filtered lipid identifications have reduced total count compared to input (indicating filtering has removed low-confidence hits) and retain expected high-confidence identifications
- TOML options file specifies MS-DIAL version (4 or 5) matching the export data; mismatch will cause incorrect column mapping or model failure

## Limitations

- LipoCLEAN models are MS-DIAL version-specific: a model trained on MS-DIAL 4 data will not work with MS-DIAL 5 exports due to column renames and scaling differences. Separate options files and models must be used for each version.
- Generalization to untested instrument types is limited. The QE_Pro_model is expected to work for all Orbitrap systems, but TOF model generalization to non-standard TOF instruments (e.g., TimsTOF) is unvalidated and requires manual validation of results.
- MS-DIAL export settings must match the specifications in the README (m/z matrix format, msp export, blank filtering disabled, label column positioned left of MS/MS spectrum column for training data). Non-standard exports will have incompatible column structure.
- Training data span specific organisms and instrument/source combinations (Canis familiaris, Aspergillus fumigatus, Laccaria bicolor, Rattus norvegicus); performance on novel organisms is not characterized.
- No changelog is provided, limiting understanding of version differences and potential breaking changes between releases.

## Evidence

- [readme] LipoCLEAN is a command line tool that applies machine learning to filter lipid identifications from MS-DIAL output: "LipoCLEAN is a command line tool. Usage instructions can be obtained using the `--help` flag. All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML"
- [readme] Default TOML options files are available for MS-DIAL 4 and 5 via command-line arguments: "Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively."
- [readme] MS-DIAL export must use specific settings including m/z matrix format and msp export with blank filtering disabled: "Select 'Alignment result' in the dropdown menu. Select 'm/z matrix' to be exported (deselect any other exports you do not want to generate). Make sure blank filtering is NOT selected. 'Export format'"
- [readme] LipoCLEAN provides QC plots and filtering statistics in output folder: "The results will be in a folder named `example_output/` the `example_output/QC/` folder contains several plots to assess the quality of the results."
- [readme] Models are instrument-family specific with known generalization limits: "We expect that the QE_Pro_model will work for all Orbitrap systems. We do not have the data necessary to know how well the TOF model will generalize to all TOF instruments so if you are working with"
- [readme] MS-DIAL 4 and 5 are not interchangeable due to column structure differences: "Our tool supports both MS-DIAL 4 and 5. However, some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other."
