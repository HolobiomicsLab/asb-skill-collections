---
name: machine-learning-model-application-to-lipidomics
description: Use when you have MS-DIAL lipid identifications from an Orbitrap or TOF
  mass spectrometer and need to remove spurious or low-confidence assignments before
  downstream metabolomics analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - LipoCLEAN
  - MS-DIAL
  - Docker
  - Conda
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
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

# machine-learning-model-application-to-lipidomics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply pre-trained machine learning models to filter low-confidence lipid identifications from MS-DIAL output, improving annotation quality by removing incorrect lipid assignments. LipoCLEAN uses instrument-specific models (Orbitrap or TOF) trained on manually curated MS/MS spectra to score and retain only high-confidence identifications.

## When to use

You have MS-DIAL lipid identifications from an Orbitrap or TOF mass spectrometer and need to remove spurious or low-confidence assignments before downstream metabolomics analysis. This is particularly valuable when you cannot manually validate thousands of identifications or when working with new datasets from the same instrument family as the training data.

## When NOT to use

- Input lipid identifications are from an instrument family or vendor not represented in the training data (e.g., TimsTOF or Bruker systems); the authors note limited generalization across TOF vendors.
- MS-DIAL identifications were already produced with blank filtering enabled or using non-standard export settings; the model expects the specific msp format and column structure.
- You need to train a custom model on your own curated data rather than use the pre-trained weights; this requires preparing labeled datasets and modifying LipoCLEAN's model training pipeline.

## Inputs

- MS-DIAL alignment export file in msp format (m/z matrix, no blank filtering)
- TOML-formatted configuration file specifying MS-DIAL export location and output directory

## Outputs

- Filtered lipid identification table (tab-delimited) with machine learning quality scores
- QC plots (in example_output/QC/) showing confidence distributions and retention time alignment
- Log file (LipoCLEAN.log) documenting run parameters and model application details

## How to apply

First, export your MS-DIAL alignment results in msp format using the m/z matrix option without blank filtering, following MS-DIAL's export settings. Generate a TOML configuration file using the `--print MSD4` or `--print MSD5` command to match your MS-DIAL version, then edit it to specify the path to your MS-DIAL export file(s). Run LipoCLEAN with the configured TOML file: the tool applies the appropriate pre-trained model (QE_Pro_model for Orbitrap systems; TOF_model for time-of-flight instruments) to score each lipid identification. The model leverages spectral features, retention time, and ion intensity patterns learned from 742–1125 manually annotated standards per instrument type. Validate filtering quality by examining the QC plots in `example_output/QC/` and the log file; these show model confidence distributions and retention time alignment success.

## Related tools

- **MS-DIAL** (Generates lipid identification alignments and exports spectra in msp format for LipoCLEAN filtering)
- **LipoCLEAN** (Command-line tool that applies machine learning models to score and filter MS-DIAL lipid identifications) — https://github.com/stavis1/LipoCLEAN
- **Docker** (Container runtime for executing LipoCLEAN without local dependency installation)
- **Conda** (Environment manager for installing LipoCLEAN and its Python dependencies)

## Examples

```
python -m lipoCLEAN --options example_analysis_options.txt
```

## Evaluation signals

- Presence of QC plots in example_output/QC/ folder; plots should show model confidence score distributions and successful retention time alignment across input files.
- Log file (LipoCLEAN.log) contains no errors and reports the correct number of input identifications and the count of retained (filtered) identifications.
- Output identification table retains expected column structure (including m/z data) and contains only identifications with model confidence scores above the implied threshold.
- For known-valid standards or positive controls in the input, verify they are retained in the output; for known-invalid identifications, verify they are removed.
- Model application is specific to MS-DIAL version (4 vs. 5) as evidenced by TOML configuration; verify correct options file was used (MSD4 vs. MSD5) matching your MS-DIAL export.

## Limitations

- Models are specific to MS-DIAL version; a model trained on MS-DIAL 4 data will not work correctly with MS-DIAL 5 exports due to column renames and scaling differences. Users must select the correct version-specific model and TOML template.
- Generalization across instrument families is limited. The QE_Pro_model is expected to work across Orbitrap systems, but the TOF_model has been tested only on TripleTOF 6600; TimsTOF and other vendor TOF platforms should be validated on a subset of results before trusting full-scale filtering.
- Tool requires MS-DIAL exports generated with specific settings (m/z matrix option, msp format, no blank filtering). Non-standard exports will cause model inference to fail or produce unreliable scores.
- Retention time correction is performed per-input-file, so datasets from different chromatography methods or instrument configurations should be processed as separate files to avoid alignment artifacts.
- No changelog is provided, limiting users' ability to track model version changes or bug fixes across releases.

## Evidence

- [readme] All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file.: "All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file."
- [readme] Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively.: "Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively."
- [intro] LipoCLEAN uses machine learning to filter lipid identifications from MS-DIAL output: "A machine learning based quality filter for lipid identifications from MS-DIAL"
- [readme] We expect that the QE_Pro_model will work for all Orbitrap systems. We do not have the data necessary to know how well the TOF model will generalize to all TOF instruments so if you are working with e.g. TimsTOF data it would be a good idea to do an initial validation of the output.: "We expect that the QE_Pro_model will work for all Orbitrap systems. We do not have the data necessary to know how well the TOF model will generalize to all TOF instruments so if you are working with"
- [readme] Some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other.: "Some columns were renamed and scaled differently between the two versions so a model trained on one version's data will not work with the other."
- [readme] The results will be in a folder named `example_output/` the `example_output/QC/` folder contains several plots to assess the quality of the results.: "The results will be in a folder named `example_output/` the `example_output/QC/` folder contains several plots to assess the quality of the results."
- [readme] Select 'm/z matrix' to be exported (deselect any other exports you do not want to generate): "Select 'm/z matrix' to be exported (deselect any other exports you do not want to generate)"
- [readme] Make sure blank filtering is NOT selected: "Make sure blank filtering is NOT selected"
- [readme] The retention time correction is run on a per-input-file basis.: "The retention time correction is run on a per-input-file basis."
