---
name: multi-batch-experimental-design-understanding
description: Use when your metabolomics experiment includes samples acquired across multiple instrument runs, different preparation dates, or distinct sample cohorts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ThermoRawFileParser
  - pycombat
  - Python
  - PCPFM (Python-Centric Pipeline for Metabolomics)
  - Asari
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- Batch correction is performed using pycombat.
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

# multi-batch-experimental-design-understanding

## Summary

Recognize and document batch structure in multi-batch LC-MS metabolomics experiments to enable proper batch effect detection and correction. Understanding batch metadata (acquisition timing, instrument configuration, sample preparation cohorts) is prerequisite to applying batch-aware normalization and validation.

## When to use

Your metabolomics experiment includes samples acquired across multiple instrument runs, different preparation dates, or distinct sample cohorts. Batch information must be recorded in the sample metadata (a 'Batch' field or equivalent) before normalization, quality control, or statistical analysis. Use this skill when you observe systematic intensity or m/z drift across sample groups, or when your experimental design explicitly includes multiple acquisition batches.

## When NOT to use

- All samples were acquired in a single instrument run with no systematic acquisition timing or preparation differences—batch correction is unnecessary.
- Batch labels cannot be reliably assigned or documented from available metadata.
- Samples are already fully batch-corrected and you are only performing final statistical analysis without re-validation.

## Inputs

- raw LC-MS acquisition files (.raw or .mzML)
- sample metadata CSV with at minimum: sample names, file paths, and batch labels
- feature table (pre- or post-imputation) with sample and feature counts

## Outputs

- annotated sample metadata CSV with batch field populated
- batch effect assessment report (inter-batch variance before/after correction)
- batch-corrected feature table (optional, downstream product)

## How to apply

Extract batch labels from instrument metadata, sample acquisition logs, or experiment design and add them as a dedicated field in your sample metadata CSV (e.g., 'Batch' column with values like 'batch_1', 'batch_2'). Document the biological or technical rationale for batch assignment—whether batches represent distinct instrument runs, preparation dates, or sample cohorts. This metadata is then passed to downstream correction tools (e.g., the pcpfm pipeline's --by_batch parameter to pycombat) during data normalization. The batch field enables calculation of inter-batch variance metrics (median intensity variance across shared features grouped by batch) to quantify batch effects before and after correction, validating that batch correction does not artificially remove true biological signal.

## Related tools

- **pycombat** (Applies empirical Bayes batch correction to feature tables using batch labels supplied via the by_batch parameter)
- **PCPFM (Python-Centric Pipeline for Metabolomics)** (Orchestrates the complete metabolomics workflow including batch metadata handling, feature table construction, and batch correction via the pcpfm batch_correct command) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Asari** (Processes mzML data to feature tables; outputs are then subject to batch-aware normalization and correction downstream)
- **Python** (Used to load metadata, calculate inter-batch variance statistics, and validate batch effect attenuation)

## Evaluation signals

- Batch field is present in sample metadata CSV and contains consistent, non-null values for all samples (no missing batch assignments).
- After pycombat correction with the --by_batch parameter, the output feature table retains identical sample count and feature count as the input (structural integrity check).
- Median inter-batch intensity variance for high-intensity features is demonstrably lower in the corrected table than in the uncorrected table, confirming batch effect attenuation.
- Sample and feature dimensions are verified post-correction (e.g., row and column counts match input and output tables).
- Batch labels correspond to documented acquisition or preparation cohorts, with no systematic confounding of batch with phenotype (e.g., all cases in batch_1 and all controls in batch_2 would confound biological signal with batch effect).

## Limitations

- If batch is confounded with phenotype or treatment (e.g., all case samples in one batch, all controls in another), batch correction may remove true biological signal.
- Batch correction assumes shared features across batches; features present in only one batch cannot be corrected.
- The article notes ongoing development of support for GC-MS and other data types; current batch workflows are optimized for LC-MS metabolomics.
- Manual curation of batch metadata is still recommended for full flexibility, especially in large studies where automated preprocessing may introduce batch assignment errors.

## Evidence

- [other] Batch correction using pycombat is applied to multi-batch interpolated feature tables via the by_batch flag, and the corrected table should retain identical sample and feature dimensions while systematically reducing inter-batch intensity variance for shared features.: "Batch correction using pycombat is applied to multi-batch interpolated feature tables via the by_batch flag, and the corrected table should retain identical sample and feature dimensions while"
- [readme] It is typical that the sequence file contains sufficient information for metadata. However, some instruments do not allow all values for all fields in a sequence file. This step is therefore to prepare metadata from the sequence file.: "It is typical that the sequence file contains sufficient information for metadata. However, some instruments do not allow all values for all fields in a sequence file"
- [readme] As a basic recommmendation, you should include a field for sample type (e.g., 'Type') with strings for each type of sample (i.e., standards are marked 'STD', blanks are 'BLANK', etc.) and a 'Batch' field if your samples were collected in multiple: "you should include a field for sample type (e.g., 'Type') with strings for each type of sample (i.e., standards are marked 'STD', blanks are 'BLANK', etc.) and a 'Batch' field if your samples were"
- [other] Calculate median inter-batch variance for a subset of high-intensity features in both uncorrected and corrected tables using sample grouping by the batch field.: "Calculate median inter-batch variance for a subset of high-intensity features in both uncorrected and corrected tables using sample grouping by the batch field"
- [other] Confirm that corrected table median inter-batch variance is lower than uncorrected median inter-batch variance, demonstrating successful batch effect attenuation.: "Confirm that corrected table median inter-batch variance is lower than uncorrected median inter-batch variance, demonstrating successful batch effect attenuation"
