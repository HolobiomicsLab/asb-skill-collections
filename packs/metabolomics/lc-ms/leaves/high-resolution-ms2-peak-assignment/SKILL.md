---
name: high-resolution-ms2-peak-assignment
description: Use when you have high-resolution MS2 data in .ms2 format from lipid
  A samples and need to perform automated structure annotation to identify lipid A
  molecular variants and their fragmentation patterns at scale.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - git
  - MSConvert (ProteoWizard)
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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

# high-resolution-ms2-peak-assignment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automated structure annotation of lipid A from high-resolution tandem mass spectrometry (MS2) data by assigning fragment peaks to lipid A structural moieties. This skill is essential when you have MS2 spectra and need to identify and annotate lipid A molecular structures at systems level.

## When to use

Apply this skill when you have high-resolution MS2 data in .ms2 format from lipid A samples and need to perform automated structure annotation to identify lipid A molecular variants and their fragmentation patterns at scale.

## When NOT to use

- Input data is not in .ms2 format — first convert using MSConvert (ProteoWizard) with Peak Picking (CWT algorithm) and MS Level 2 filters
- Your mass spectrometry data is from non-lipid A samples or low-resolution instruments not suitable for structure annotation
- You are running on MacOS or Linux — LipidA-IDER has only been tested on Windows; use on other platforms has not been validated

## Inputs

- .ms2 format mass spectrometry data files
- LipidAIDER_AnalysisParam.csv parameter settings file
- LipidAIDER_BatchAnalysisFiles.csv batch specification (for CLI mode)

## Outputs

- Annotated lipid A structure assignments
- Fragment peak annotations with m/z assignments
- Batch output folder (Logger/<YYYYMMDD_HHMMSS>/Batch Output)

## How to apply

LipidA-IDER performs peak assignment by accepting .ms2 format input files containing high-resolution tandem mass spectrometry data. The tool uses configurable analysis parameters (stored in LipidAIDER_AnalysisParam.csv) to control peak picking, m/z tolerance, and structural annotation thresholds. Users prepare input files and parameter settings, then execute the analysis via either GUI (python LipidAIDER_GUI.py) or CLI (python LIPIDAIDER_main.py). The analysis generates annotated output in a timestamped Logger directory containing structural assignments for detected lipid A species. Success is verified by confirming that annotated lipid A structure outputs are generated and saved to the specified output directory with assigned fragment annotations.

## Related tools

- **Python** (Execution environment for LipidA-IDER GUI and CLI interfaces)
- **git** (Repository cloning tool to obtain LipidA-IDER source code) — https://github.com/Systems-Biology-Of-Lipid-Metabolism-Lab/LipidA-IDER
- **MSConvert (ProteoWizard)** (Data format conversion to .ms2 with peak picking (CWT algorithm, MS Level 2)) — https://proteowizard.sourceforge.io/download.html

## Examples

```
$ python LIPIDAIDER_main.py -m /path/to/demo_input_files/sample.ms2
```

## Evaluation signals

- Output files are generated in the timestamped Logger directory with expected structure (Logger/<YYYYMMDD_HHMMSS>/Batch Output)
- Annotated lipid A structural assignments are present in output with fragment peak m/z values assigned
- No runtime errors or warnings in terminal/CLI output indicating parameter or data format issues
- Output files contain expected number of annotated lipid A species matching input sample count
- Batch Output folder contains dated subdirectory matching analysis run timestamp

## Limitations

- LipidA-IDER has only been tested on Windows; use on MacOS and Linux has not been tested
- Currently accepts only .ms2 format data files; other formats require preprocessing with MSConvert
- Requires .ms2 input files to have been processed with Peak Picking using CWT algorithm at MS Level 2
- Performance and accuracy depend on appropriate parameter tuning in LipidAIDER_AnalysisParam.csv for the specific MS data nature

## Evidence

- [readme] LipidA-IDER is an automated structure annotation tool for systems-level scale identification of lipid A from high resolution tandem mass spectrometry (MS2) data: "LipidA-IDER is an automated structure annotation tool for systems-level scale identification of lipid A from high resolution tandem mass spectrometry (MS2) data"
- [readme] LipidAIDER currently accepts data in .ms2 format. To convert to .ms2, use MSConvert (ProteoWizard) (download from: https://proteowizard.sourceforge.io/download.html) Settings: Output format: .ms2, Filters: Peak Picking, Algorithm: CWT, MS Levels: 2: "LipidAIDER currently accepts data in .ms2 format. To convert to .ms2, use MSConvert (ProteoWizard) Settings: Output format: .ms2, Filters: Peak Picking, Algorithm: CWT, MS Levels: 2"
- [readme] As of current, LipidA-IDER has only been tested on Windows. Use of LipidA-IDER on MacOS and Linux has *not* been tested: "LipidA-IDER has only been tested on Windows. Use of LipidA-IDER on MacOS and Linux has *not* been tested"
- [readme] Upon completion of the analysis. the generated output will be found in the '\Logger\<YYYYMMDD_HHMMSS>\Batch Output' subfolder: "Upon completion of the analysis. the generated output will be found in the '\Logger\<YYYYMMDD_HHMMSS>\Batch Output' subfolder"
- [readme] The default parameters are provided in [\Settings\LipidAIDER_AnalysisParam.csv](/Settings/LipidAIDER_AnalysisParam.csv). Users may edit this file to according to the nature of their data: "Users may edit this file to according to the nature of their data"
