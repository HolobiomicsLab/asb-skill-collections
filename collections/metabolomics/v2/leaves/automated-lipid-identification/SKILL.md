---
name: automated-lipid-identification
description: Use when you have high-resolution tandem mass spectrometry (MS2) data
  in .ms2 format and need to systematically identify and annotate lipid A molecular
  structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - Python
  - git
  - MSConvert (ProteoWizard)
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c00520
  title: LipidA-IDER
evidence_spans:
- $ python LipidAIDER_GUI.py
- 'Step 0: Install git (if you have not done so before)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipida_ider_cq
    doi: 10.1021/acs.analchem.5c00520
    title: LipidA-IDER
  dedup_kept_from: coll_lipida_ider_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00520
  all_source_dois:
  - 10.1021/acs.analchem.5c00520
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# automated-lipid-identification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

LipidA-IDER is an automated structure annotation tool that identifies lipid A from high-resolution tandem mass spectrometry (MS2) data at systems-level scale. Use this skill to rapidly annotate and structurally characterize lipid A molecules from MS2 spectra without manual intervention.

## When to use

You have high-resolution tandem mass spectrometry (MS2) data in .ms2 format and need to systematically identify and annotate lipid A molecular structures. This skill is appropriate when you lack prior lipid A structural annotations and want to apply uniform, automated structure-matching criteria across large MS2 datasets.

## When NOT to use

- Your input mass spectrometry data is in a format other than .ms2 (e.g., raw vendor format, mzML, or NetCDF) without prior conversion via MSConvert.
- You are running the tool on macOS or Linux — LipidA-IDER has only been tested on Windows; use on other platforms has not been validated.
- Your data contains lipid classes other than lipid A, or you need simultaneous annotation of multiple diverse lipid classes.

## Inputs

- .ms2 format mass spectrometry data files (peak-picked MS2 spectra)
- LipidAIDER_AnalysisParam.csv (parameter configuration file)
- LipidAIDER_BatchAnalysisFiles.csv (batch metadata file, optional for CLI mode)

## Outputs

- Annotated lipid A structure assignments and identifications
- Batch output files in Logger/<YYYYMMDD_HHMMSS>/Batch Output subdirectory

## How to apply

First, ensure your mass spectrometry data is in .ms2 format (convert using MSConvert with Peak Picking [CWT algorithm] and MS Levels 2 if needed). Install Python and git, then clone the LipidA-IDER repository. Open a terminal in the LipidA-IDER directory and either (1) launch the GUI via `python LipidAIDER_GUI.py`, select your .ms2 file(s) and default or custom parameter settings, then click 'Run Analysis'; or (2) use CLI mode by editing the batch and parameter CSV files, then invoke `python LIPIDAIDER_main.py` or `python LIPIDAIDER_main.py -m <PATH_TO_MS2_FILE>`. The tool will generate annotated lipid A structure outputs in a timestamped Logger subdirectory. Verify outputs contain expected annotation fields and compare against known lipid A reference spectra to confirm structural assignments.

## Related tools

- **Python** (Runtime environment for executing the LipidA-IDER GUI and CLI scripts)
- **git** (Version control and repository cloning to obtain the LipidA-IDER codebase) — https://github.com/git-guides/install-git
- **MSConvert (ProteoWizard)** (Preprocessing tool to convert raw mass spectrometry data to .ms2 format with peak picking (CWT algorithm, MS Levels 2)) — https://proteowizard.sourceforge.io/download.html

## Examples

```
$ python LIPIDAIDER_main.py -m /path/to/demo_input_files/sample.ms2
```

## Evaluation signals

- Output files are successfully written to the timestamped Logger/<YYYYMMDD_HHMMSS>/Batch Output directory with no error messages or incomplete annotation records.
- Annotated lipid A structures can be parsed and contain expected fields (e.g., structure identifiers, fragment ion assignments, scoring metrics).
- Annotation results for demo input files match documented expected outputs (compare against expected lipid A reference standards).
- CLI invocations complete without Python runtime errors; GUI mode displays 'selected files' confirmation before and 'Run Analysis' completion status after execution.
- Parameter settings from LipidAIDER_AnalysisParam.csv are correctly applied to the analysis (verify by inspecting output metadata or log files).

## Limitations

- LipidA-IDER has only been tested on Windows; use on macOS and Linux has not been tested and may fail or produce unreliable results.
- Tool currently accepts only .ms2 format input; other mass spectrometry data formats require conversion via MSConvert, adding preprocessing overhead.
- No changelog is publicly available, limiting users' ability to track feature additions, bug fixes, or breaking changes across versions.
- Default parameter settings are optimized for lipid A; use on data with different sample origins or instrumental configurations may require parameter tuning via the CSV configuration file.

## Evidence

- [readme] LipidA-IDER is an automated structure annotation tool for systems-level scale identification of lipid A from high resolution tandem mass spectrometry (MS2) data.: "LipidA-IDER is an automated structure annotation tool for systems-level scale identification of lipid A from high resolution tandem mass spectrometry (MS2) data"
- [readme] Input file format and conversion requirement for .ms2: "LipidAIDER currently accepts data in .ms2 format. To convert to .ms2, use MSConvert (ProteoWizard)"
- [readme] Platform limitation and testing scope: "As of current, LipidA-IDER has only been tested on Windows. Use of LipidA-IDER on MacOS and Linux has *not* been tested."
- [readme] Demo files availability for users without initial data: "In the event that you do not have initial .ms2 data, we have provided the some demo input files for your use here: [\Source\demo_input_files]"
- [readme] Output location specification: "Upon completion of the analysis. the generated output will be found in the '\Logger\<YYYYMMDD_HHMMSS>\Batch Output' subfolder."
- [readme] Parameter configuration workflow: "If you would like to modify parameters to better suit your data, you may do so by changing the relevant setting values in the csv file found in [\Settings\LipidAIDER_AnalysisParam.csv]"
