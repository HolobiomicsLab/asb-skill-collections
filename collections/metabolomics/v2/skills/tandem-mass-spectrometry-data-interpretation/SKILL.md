---
name: tandem-mass-spectrometry-data-interpretation
description: Use when you have high-resolution MS2 data (.ms2 format) from tandem mass spectrometry analysis of lipid A-containing samples and need to perform automated structure annotation and identification at systems scale.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3929
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0153
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

# tandem-mass-spectrometry-data-interpretation

## Summary

Automated structure annotation of lipid A from high-resolution tandem mass spectrometry (MS2) data using LipidA-IDER, an open-source tool that identifies and classifies lipid A molecular species at systems scale. This skill enables conversion of raw MS2 spectral data into annotated lipid structure outputs.

## When to use

You have high-resolution MS2 data (.ms2 format) from tandem mass spectrometry analysis of lipid A-containing samples and need to perform automated structure annotation and identification at systems scale. You lack established lipid A reference libraries or wish to standardize annotation across large sample batches. You want to avoid manual peak assignment and structural hypothesis generation.

## When NOT to use

- Input data is in formats other than .ms2 (e.g., raw vendor formats, mzML, NetCDF) without prior conversion
- Running on MacOS or Linux systems, as LipidA-IDER has only been tested and validated on Windows
- Data consists of MS1 spectra only or does not include tandem MS2 fragmentation data

## Inputs

- .ms2 format mass spectrometry data files
- LipidAIDER_AnalysisParam.csv configuration file (optional custom parameters)
- LipidAIDER_BatchAnalysisFiles.csv batch definition file (for CLI mode)

## Outputs

- Annotated lipid A structure assignments
- Batch output files in Logger/<YYYYMMDD_HHMMSS>/Batch Output directory
- Per-spectrum annotation records with lipid A molecular identities

## How to apply

First, prepare input data by converting raw mass spectrometry files to .ms2 format using MSConvert (ProteoWizard) with peak picking (CWT algorithm) and MS level 2 filtering. Clone the LipidA-IDER repository and install Python dependencies. Configure analysis parameters in the LipidAIDER_AnalysisParam.csv settings file to match your data characteristics (e.g., m/z accuracy, fragment ion thresholds). Execute LipidA-IDER via either the GUI ($ python LipidAIDER_GUI.py) for interactive file selection and parameter adjustment, or CLI ($ python LIPIDAIDER_main.py -m <PATH_TO_MS2_FILE>) for batch processing. Monitor the Logger directory for timestamped output folders containing annotated lipid structures. Verify output completeness by checking that all input .ms2 records generated corresponding structure annotations.

## Related tools

- **MSConvert (ProteoWizard)** (Converts raw mass spectrometry data to .ms2 format with peak picking and MS level 2 filtering) — https://proteowizard.sourceforge.io/download.html
- **Python** (Runtime environment for executing LipidA-IDER GUI and CLI interfaces)
- **git** (Version control tool for cloning the LipidA-IDER repository)

## Examples

```
$ python LIPIDAIDER_main.py -m /path/to/sample.ms2
```

## Evaluation signals

- Output directory exists in Logger with correctly formatted YYYYMMDD_HHMMSS timestamp
- Batch Output folder contains annotation records for all input .ms2 files without truncation or errors
- Annotated lipid A structures include defined molecular identities with m/z values and fragment ion assignments consistent with input spectra
- Parameter values in settings file align with expected MS data characteristics (e.g., instrument resolution, ion mode)
- No error logs or warnings in stdout/stderr indicating failed spectrum processing or missing required input files

## Limitations

- LipidA-IDER has only been tested on Windows; use on MacOS and Linux has not been tested and is unsupported
- Accepts only .ms2 format input; conversion from other formats (raw vendor data, mzML) is required beforehand
- Output quality and annotation accuracy depend on proper configuration of analysis parameters in LipidAIDER_AnalysisParam.csv; misaligned parameters may produce spurious or incomplete annotations
- Tool is optimized for lipid A structures specifically; applicability to other lipid classes or modified lipid A species is not documented

## Evidence

- [readme] LipidA-IDER is an automated structure annotation tool for systems-level scale identification of lipid A from high resolution tandem mass spectrometry (MS2) data: "LipidA-IDER is an automated structure annotation tool for systems-level scale identification of lipid A from high resolution tandem mass spectrometry (MS2) data"
- [readme] As of current, LipidA-IDER has only been tested on Windows. Use of LipidA-IDER on MacOS and Linux has *not* been tested.: "As of current, LipidA-IDER has only been tested on Windows. Use of LipidA-IDER on MacOS and Linux has *not* been tested."
- [readme] LipidAIDER currently accepts data in .ms2 format. To convert to .ms2, use MSConvert (ProteoWizard) (download from: https://proteowizard.sourceforge.io/download.html) Settings: Output format: .ms2, Filters: Peak Picking, Algorithm: CWT, MS Levels: 2: "LipidAIDER currently accepts data in .ms2 format. To convert to .ms2, use MSConvert (ProteoWizard) Settings: Output format: .ms2, Filters: Peak Picking, Algorithm: CWT, MS Levels: 2"
- [readme] Upon completion of the analysis. the generated output will be found in the '\Logger\<YYYYMMDD_HHMMSS>\Batch Output' subfolder.: "Upon completion of the analysis. the generated output will be found in the '\Logger\<YYYYMMDD_HHMMSS>\Batch Output' subfolder."
- [readme] In the event that you do not have initial .ms2 data, we have provided the some demo input files for your use here: [\Source\demo_input_files]: "In the event that you do not have initial .ms2 data, we have provided the some demo input files for your use"
