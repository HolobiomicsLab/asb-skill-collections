---
name: metadata-field-based-sample-stratification
description: Use when you have a feature table and accompanying CSV metadata that
  includes a 'Sample Type' field (or equivalent) with entries such as 'BLANK', 'QC',
  'STD', or 'Unknown'.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PCPFM
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm_cq
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metadata-field-based-sample-stratification

## Summary

Stratify LC-MS metabolomics samples into groups (blanks, QC, unknowns, standards) based on categorical metadata fields to enable targeted quality control, filtering, and downstream curation. This skill is essential for separating samples by experimental role before applying differential processing such as blank masking or batch correction.

## When to use

Apply this skill when you have a feature table and accompanying CSV metadata that includes a 'Sample Type' field (or equivalent) with entries such as 'BLANK', 'QC', 'STD', or 'Unknown'. Use it before blank masking, batch correction, or sample removal operations that require discriminating samples by their experimental role rather than by their intensities or statistical properties.

## When NOT to use

- Metadata does not include a categorical 'Sample Type' or equivalent field — manual annotation is required first.
- All samples are of a single type (e.g., no blanks in the study) — stratification may be unnecessary or will yield empty strata.
- Sample identifiers in metadata do not match sample column names in the feature table — perform identifier reconciliation first.

## Inputs

- CSV metadata file with sample identifiers and categorical fields (e.g., Sample Type, Batch)
- Feature table (TSV or similar) with features in rows and samples in columns, indexed by sample identifier

## Outputs

- Stratified sample lists or indices mapping each sample to its experimental role (blank, QC, standard, unknown)
- Updated experiment.json metadata reference for downstream filters

## How to apply

Parse the experiment metadata CSV file and extract the user-designated query_field (e.g., 'Sample Type'). Identify which metadata values correspond to blanks (blank_value, typically 'BLANK') and which correspond to study samples (sample_value, typically 'Unknown'). Use these designations to partition the feature table into subsets: one containing only blank samples and one containing only study samples. This stratification is then used as input to subsequent filtering steps (e.g., calculating median intensities per stratum for blank masking). The metadata field must be manually curated or preprocessed to ensure consistent string values; the PCPFM pipeline includes an optional preprocessing step (pcpfm preprocess) to standardize metadata before analysis.

## Related tools

- **PCPFM** (orchestrates metadata parsing and stratification within the full LC-MS preprocessing pipeline) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Python** (language used to parse CSV metadata and implement sample stratification logic)

## Examples

```
pcpfm preprocess -s ./Sequence.csv --new_csv_path ./NewSequence.csv --name_field='Name' --path_field='Path' --preprocessing_config ./pcpfm/preprocessing.json
```

## Evaluation signals

- Stratified sample lists are non-empty and partition all samples without overlap (each sample belongs to exactly one stratum).
- Sample identifiers in each stratum match metadata field values as expected (e.g., all 'BLANK' samples grouped together).
- Subsequent filters (blank masking, batch correction) receive the correct subsets and produce consistent results (e.g., median intensity ratios calculated only from the designated blank and sample strata).
- experiment.json is updated with references to the stratification and any new derived tables, enabling full pipeline traceability.

## Limitations

- Relies on manual or semi-automated metadata curation; inconsistent or missing 'Sample Type' values will cause silent failures or incorrect stratification.
- The preprocessing step (pcpfm preprocess) is optional; users working with manually constructed metadata must ensure field consistency.
- If sample names in metadata do not match mzML file names, earlier pipeline stages may fail; this issue was fixed as of 2/28/24 but may recur with non-standard naming conventions.
- No built-in support for hierarchical or multi-level stratification (e.g., by both 'Sample Type' and 'Batch'); user must manually subset or run the skill iteratively.

## Evidence

- [other] Parse the query_field and identify samples matching blank_value and sample_value designations.: "Parse the query_field and identify samples matching blank_value and sample_value designations."
- [readme] It is typical that the sequence file contains sufficient information for metadata. However, some instruments do not allow all values for all fields in a sequence file. This step is therefore to prepare metadata from the sequence file.: "It is typical that the sequence file contains sufficient information for metadata. However, some instruments do not allow all values for all fields in a sequence file."
- [readme] An example of input CSV file: [table with Sample Type, Name, Filepath columns showing Blank, QC, Unknown designations]: "Other fields are supported and can be used during an analysis. As a basic recommendation, you should include a field for sample type (e.g., "Type") with strings for each type of sample (i.e.,"
- [intro] remove samples not needed for downstream analysis namely QC samples, blanks, etc.: "Drop undesired samples such as QC samples and blanks: remove samples not needed for downstream analysis namely QC samples, blanks, etc."
- [readme] there was an issue regarding sample names that do not match their mzML file names. This has been fixed as of 2/28/24.: "there was an issue regarding sample names that do not match their mzML file names. This has been fixed as of 2/28/24."
