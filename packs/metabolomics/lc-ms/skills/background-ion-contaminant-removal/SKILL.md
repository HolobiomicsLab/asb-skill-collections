---
name: background-ion-contaminant-removal
description: Use when you have a feature table from LC-MS data alongside blank (solvent-only) sample runs, and you want to remove features whose intensity in study samples is not substantially higher than their intensity in blanks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ThermoRawFileParser
  - Python
  - PCPFM (Python-Centric Pipeline for Metabolomics)
  - Asari
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# background-ion-contaminant-removal

## Summary

Remove features from metabolomics feature tables that are likely background contamination or instrumental artifacts by filtering against blank sample intensities using an intensity ratio threshold. This quality control step eliminates low-abundance features present in blank samples before annotation and downstream statistical analysis.

## When to use

Apply this skill when you have a feature table from LC-MS data alongside blank (solvent-only) sample runs, and you want to remove features whose intensity in study samples is not substantially higher than their intensity in blanks. This is especially important before annotation and statistical analysis to avoid wasting computational resources on contaminants or instrumental noise.

## When NOT to use

- Input data lacks blank sample runs or blank sample metadata is unavailable or unreliable
- Feature table is already heavily pre-filtered or blank masking has already been applied
- Study design does not include dedicated blank samples or your blanks are not representative of instrument background for your analytes

## Inputs

- Feature table (TSV or equivalent tabular format with feature abundances across samples)
- Sample metadata CSV file with 'sample_type' or equivalent field distinguishing blank and unknown samples
- Feature intensity values (raw or normalized counts/areas)

## Outputs

- Filtered feature table (same format as input, with low-ratio features removed)
- Feature mapping or log indicating which features were retained vs. removed
- Preserved metadata and feature annotations

## How to apply

Load the input feature table and sample metadata, then use the sample_type field or equivalent metadata column to identify which samples are blanks (designated by blank_value) and which are study samples (designated by sample_value). For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values. Compute the intensity ratio (unknown/blank) for each feature and compare against the configurable blank_intensity_ratio parameter (default threshold of 3). Retain only features where the median/mean intensity in unknown samples exceeds the median/mean blank intensity by at least the specified ratio multiplier. Save the filtered feature table with a new moniker and preserve associated metadata and feature annotations.

## Related tools

- **PCPFM (Python-Centric Pipeline for Metabolomics)** (End-to-end LC-MS preprocessing pipeline that wraps and orchestrates blank_masking as a quality control step) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Python** (Core implementation language for blank_masking command and feature intensity ratio computation)
- **Asari** (Upstream tool that generates the feature table and feature annotations that serve as input to blank masking) — https://github.com/shuzhao-li-lab/asari

## Evaluation signals

- Feature count decreases after blank masking relative to input (number of removed features is logged or reported)
- All retained features have blank_intensity_ratio ≥ the configured threshold (e.g., ≥ 3 by default)
- Metadata rows and feature annotations remain intact and consistent with filtered feature table
- Samples designated as blanks in metadata are correctly identified and used for ratio calculation
- Output feature table schema matches input schema (same columns, feature IDs preserved for retained features)

## Limitations

- Blank masking assumes blank samples are representative of instrument background and contamination; if blanks are improperly prepared or handled, the filter may remove real signals or retain contaminants
- The default intensity ratio threshold (3) may be too stringent or permissive depending on instrument type, ionization method, and analyte class; users should validate the threshold for their specific protocol
- Features with very low absolute intensity in both blanks and samples may fall below detection limits and produce unreliable ratio estimates; the workflow excludes zero values but does not explicitly handle near-zero noise floors
- The skill only addresses background contamination; it does not correct for batch effects, instrumental drift, or systematic biases that require normalization or batch correction in separate steps

## Evidence

- [other] The blank_masking command removes features by comparing feature intensity in study samples (designated by sample_value) to intensity in blanks (designated by blank_value) using a configurable blank_intensity_ratio parameter; features whose intensity in unknown samples is not at least the specified ratio times more than blank samples are dropped.: "The blank_masking command removes features by comparing feature intensity in study samples (designated by sample_value) to intensity in blanks (designated by blank_value) using a configurable"
- [other] For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values. 3. Compute the intensity ratio (unknown/blank) for each feature and compare against the blank_intensity_ratio threshold (default 3).: "For each feature, calculate the median or mean intensity across blank samples and across unknown samples, excluding zero values. Compute the intensity ratio (unknown/blank) for each feature and"
- [other] Load the input feature table and sample metadata using the specified table moniker and identify blank and unknown samples based on the query field (e.g., 'sample_type').: "Load the input feature table and sample metadata using the specified table moniker and identify blank and unknown samples based on the query field (e.g., 'sample_type')."
- [intro] perform quality control: "perform quality control"
- [readme] Outputs are intended to be immediately usable for downstream analysis (e.g. MetaboAnalyst or common tools in R, Python etc.). This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM: "feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM"
