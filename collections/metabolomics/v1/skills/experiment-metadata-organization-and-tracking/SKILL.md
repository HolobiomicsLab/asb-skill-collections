---
name: experiment-metadata-organization-and-tracking
description: Use when before initiating raw file conversion or feature extraction, when you have a heterogeneous collection of raw LC-MS files (.raw or .mzML) and sample information scattered across instrument logs, sequence files, or spreadsheets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - ThermoRawFileParser
  - Asari
  - khipu
  - pcpfm assemble
  - pcpfm preprocess
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
- convert Thermo .raw to mzML (ThermoRawFileParser)
- process mzML data to feature tables (Asari)
- pre-annotation to group featues to empirical compounds (khipu)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
---

# experiment-metadata-organization-and-tracking

## Summary

Structured assembly of LC-MS metabolomics experiments by organizing raw acquisition files, sample metadata (names, types, batch identifiers, file paths), and instrument parameters into a centralized JSON state object that tracks provenance and enables reproducible, batch-aware processing. This foundation precedes all downstream quality control, normalization, and annotation steps.

## When to use

Before initiating raw file conversion or feature extraction, when you have a heterogeneous collection of raw LC-MS files (.raw or .mzML) and sample information scattered across instrument logs, sequence files, or spreadsheets. Use this skill to consolidate metadata into a single source of truth that documents sample types (blank, QC, unknown), batch membership, file paths, and ionization mode, so that later QC and normalization steps can be batch-aware and traceable.

## When NOT to use

- Metadata is already integrated into a processed feature table or experiment object from a prior run — use `pcpfm` state recovery instead.
- You lack sample type information (blank vs. sample vs. QC) — metadata assembly requires these distinctions to enable later blank masking and QC filtering.
- Files are in unsupported formats (e.g., raw Thermo .raw files on a non-Windows system without ThermoRawFileParser installed) — file format validation will fail during assembly.

## Inputs

- CSV sequence/metadata file (columns: sample name, file path, sample type, optionally batch identifier)
- Raw LC-MS acquisition files (.raw or .mzML)
- Target experiment directory path

## Outputs

- experiment.json (persistent state object with sample inventory, metadata, ionization mode, file paths)
- Experiment directory structure (raw_acquisitions/, converted_acquisitions/, feature_tables/, results/, annotations/)
- Validated sample-to-file mapping

## How to apply

Create a CSV metadata file with minimally required fields: sample name, file path, and sample type (e.g., 'Blank', 'QC', 'Unknown'). Optionally add a batch identifier field if samples were acquired in separate instrument runs. Use the `pcpfm assemble` command with this CSV and a target experiment directory path; the command will validate file accessibility, infer ionization mode from file headers, and construct a persistent JSON experiment state object that tracks all samples, their metadata attributes, and processing history. If your sequence file uses non-standard field names or paths are relative, run `pcpfm preprocess` first to normalize field names and resolve paths before assembly. The resulting experiment.json acts as the single source of truth for all downstream operations: blank masking compares sample-to-blank pairs defined in metadata, sample dropping filters by type or QAQC results stored in the state, and batch correction later uses the batch field to apply within- and between-batch normalization independently.

## Related tools

- **pcpfm assemble** (Command to validate and ingest CSV metadata, resolve file paths, infer ionization mode, and create experiment state JSON) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **pcpfm preprocess** (Utility to normalize sequence file field names and resolve relative paths before assembly) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **ThermoRawFileParser** (Extracts metadata (ionization mode, instrument parameters) from Thermo .raw file headers during assembly validation)

## Examples

```
pcpfm assemble --metadata samples.csv --experiment_dir ./my_experiment
```

## Evaluation signals

- experiment.json is created and is valid JSON; all sample records are present with non-null metadata fields (name, file path, sample type, batch if provided).
- File path resolution succeeds for all rows: `pcpfm` should report zero file-not-found errors during assembly.
- Ionization mode is inferred and consistent within the experiment (or explicitly specified per sample if heterogeneous); verify in experiment.json or via `pcpfm list` command.
- Downstream operations (e.g., `pcpfm blank_masking`) correctly identify and pair samples to blanks using the assembled metadata without requiring manual re-entry of sample names or types.
- Sample dropping (`pcpfm drop_samples`) successfully filters by metadata field (e.g., type='QC') with no off-by-one errors or missing samples.

## Limitations

- Sample names must match their corresponding mzML file names exactly (or be resolvable via the file path field); mismatches can cause downstream feature extraction to fail. This issue was fixed as of 2024-02-28 per the README.
- Metadata is limited to fields present in the input CSV; additional attributes (e.g., phenotype, treatment group) not anticipated at assembly time cannot be added retroactively without re-running assembly or manually editing experiment.json (which is not recommended).
- Ionization mode inference relies on instrument headers and may be ambiguous for mixed-mode acquisitions; users should validate inferred mode and override if necessary.
- Batch identifiers must be manually assigned in the metadata CSV; no automated batch detection from acquisition timestamps or instrument logs is performed.

## Evidence

- [other] Assemble experiment using pcpfm assemble with CSV metadata file (sample names, file paths, sample types, batch identifiers) to create an experiment directory and JSON state object.: "Assemble experiment using pcpfm assemble with CSV metadata file (sample names, file paths, sample types, batch identifiers) to create an experiment directory and JSON state object."
- [readme] an appropriately formattted sequence file / sample metadata file along with mzML files. You can work with .raw files but support is limited.: "You will need an appropriately formattted sequence file / sample metadata file along with mzML files."
- [readme] Inputs should include a set of raw files (.raw or .mzML) and a csv file for metadata (minimal sample names and file path).: "Inputs should include a set of raw files (.raw or .mzML) and a csv file for metadata (minimal sample names and file path)."
- [readme] It is typical that the sequence file contains sufficient information for metadata. However, some instruments do not allow all values for all fields in a sequence file. This step is therefore to prepare metadata from the sequence file.: "It is typical that the sequence file contains sufficient information for metadata. However, some instruments do not allow all values for all fields in a sequence file."
- [readme] Note that to replicate the presented results you will need to run the `download extras` command.: "Note that to replicate the presented results you will need to run the `download extras` command."
- [readme] Note that annotation sources including the HMDB, while free for public non-commercial use, is not redistributed in this package.: "Note that annotation sources including the HMDB, while free for public non-commercial use, is not redistributed in this package."
- [other] blank masking by comparing sample to blank intensities with configurable intensity ratios: "blank masking by comparing sample to blank intensities with configurable intensity ratios"
- [other] sample dropping by metadata field or QAQC results: "sample dropping by metadata field or QAQC results"
- [readme] Note that this is for documentation but also because the manuscript is under review. Notably there was an issue regarding sample names that do not match their mzML file names. This has been fixed as of 2/28/24.: "Notably there was an issue regarding sample names that do not match their mzML file names. This has been fixed as of 2/28/24."
