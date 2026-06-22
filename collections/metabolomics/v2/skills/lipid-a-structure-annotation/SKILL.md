---
name: lipid-a-structure-annotation
description: Use when when you have high-resolution tandem mass spectrometry (MS2) data in .ms2 format and need to identify and annotate lipid A structures at scale.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3661
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - git
  - MSConvert (ProteoWizard)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-a-structure-annotation

## Summary

LipidA-IDER is an automated structure annotation tool for systems-level identification of lipid A from high-resolution tandem mass spectrometry (MS2) data. Use this skill to assign lipid A molecular structures to fragmentation patterns in MS2 spectra.

## When to use

When you have high-resolution tandem mass spectrometry (MS2) data in .ms2 format and need to identify and annotate lipid A structures at scale. Suitable for researchers working with lipopolysaccharide components or bacterial lipid extracts where lipid A structural diversity must be characterized.

## When NOT to use

- Input data is not in .ms2 format (first convert using MSConvert with CWT peak-picking and MS level 2 filtering)
- Running on macOS or Linux (tool has only been tested on Windows; use on other platforms is untested)
- You require real-time or interactive visualization of fragmentation trees (CLI mode provides only batch output)

## Inputs

- .ms2 format mass spectrometry data files
- LipidAIDER_AnalysisParam.csv parameter configuration file
- optional: LipidAIDER_BatchAnalysisFiles.csv for batch submission

## Outputs

- annotated lipid A structure identifications
- fragmentation pattern interpretations
- batch output files in Logger/YYYYMMDD_HHMMSS/Batch Output directory

## How to apply

Install the LipidA-IDER repository and set up the Python environment. Prepare input .ms2 files (converted from raw instrument data using MSConvert with peak-picking algorithm CWT and MS level 2 filtering). Configure analysis parameters in LipidAIDER_AnalysisParam.csv according to your MS data characteristics (e.g., mass tolerance, fragmentation thresholds). Execute the annotation via GUI (python LipidAIDER_GUI.py) or CLI (python LIPIDAIDER_main.py) against your prepared .ms2 files or the provided demo_input_files. The tool will generate annotated lipid A structure assignments with fragmentation interpretations in the timestamped output directory (Logger/YYYYMMDD_HHMMSS/Batch Output).

## Related tools

- **MSConvert (ProteoWizard)** (converts raw mass spectrometry instrument data to .ms2 format with peak-picking (CWT algorithm) and MS level 2 filtering required by LipidA-IDER) — https://proteowizard.sourceforge.io/download.html
- **Python** (runtime environment for executing LipidAIDER_GUI.py and LIPIDAIDER_main.py scripts)
- **git** (version control for cloning the LipidA-IDER repository from GitHub) — https://github.com/git-guides/install-git

## Examples

```
$ python LIPIDAIDER_main.py -m /path/to/sample.ms2
```

## Evaluation signals

- Output directory is successfully created with timestamp format YYYYMMDD_HHMMSS and contains Batch Output subfolder
- Generated lipid A structure annotations correspond to known fragmentation patterns in the MS2 spectra
- All input .ms2 files are processed without errors; completion is indicated by output file generation
- Parameter configuration matches data characteristics (e.g., mass tolerance aligns with instrument specifications)
- Annotated structures have consistent mass-to-charge ratios and fragment ion assignments with input spectral peaks

## Limitations

- LipidA-IDER has only been tested on Windows; use on macOS and Linux has not been tested
- Currently accepts .ms2 format data files only; raw instrument data must be pre-converted via MSConvert
- Annotation accuracy depends on quality of input .ms2 file preparation and appropriate parameter tuning for the specific MS instrument and lipid A sample type
- No changelog is available to track tool version changes or improvements

## Evidence

- [readme] LipidA-IDER is an automated structure annotation tool for systems-level scale identification of lipid A from high resolution tandem mass spectrometry (MS2) data: "LipidA-IDER is an automated structure annotation tool for systems-level scale identification of lipid A from high resolution tandem mass spectrometry (MS2) data"
- [readme] Input file format requirement: "LipidAIDER currently accepts data in .ms2 format. To convert to .ms2, use MSConvert (ProteoWizard)"
- [readme] Demo files availability for users without MS2 data: "In the event that you do not have initial .ms2 data, we have provided the some demo input files for your use here: [\Source\demo_input_files]"
- [readme] Output location convention: "Upon completion of the analysis. the generated output will be found in the '\Logger\<YYYYMMDD_HHMMSS>\Batch Output' subfolder."
- [readme] Platform limitation: "As of current, LipidA-IDER has only been tested on Windows. Use of LipidA-IDER on MacOS and Linux has *not* been tested."
- [readme] Parameter configuration requirement: "Users may edit this file to according to the nature of their data. The default settings for Lipid A has been recorded in [\Settings\README.md]"
- [readme] GUI execution command: "$ python LipidAIDER_GUI.py"
