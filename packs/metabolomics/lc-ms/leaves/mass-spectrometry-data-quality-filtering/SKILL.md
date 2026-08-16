---
name: mass-spectrometry-data-quality-filtering
description: Use when you have generated a complete feature table from mzML files (e.g., Asari 'full' feature table) and need to curate it for downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Asari
  - Python
  - PCPFM (PythonCentricPipelineForMetabolomics)
  - metDataModel
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- pcpfm asari -i ./my_experiment
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

# Mass Spectrometry Data Quality Filtering

## Summary

Filter LC-MS feature tables to remove low-quality features and background contamination before downstream statistical analysis. This skill removes features present in fewer than a specified percentile of samples and optionally masks blank contamination, yielding curated feature tables suitable for metabolite annotation and biomarker discovery.

## When to use

Apply this skill when you have generated a complete feature table from mzML files (e.g., Asari 'full' feature table) and need to curate it for downstream analysis. Use it when you want to distinguish a 'preferred' filtered table from the comprehensive 'full' table, when you need to remove background ions and contaminants detected in blank samples, or when you want to drop undesired samples (QC, blanks) that are not targets for statistical inference.

## When NOT to use

- Input is already a 'preferred' feature table curated by Asari—re-filtering risks over-aggressive removal of true signals.
- Your study design requires retention of all features for subsequent statistical imputation or machine-learning preprocessing—quality filtering may remove informative rare features.
- You have not yet performed mass-to-charge calibration or feature grouping—filter only after feature table generation is complete.

## Inputs

- Full feature table (TSV or JSON) from Asari processing
- Blank sample intensities or blank-labeled feature matrix subset
- Sample metadata CSV with 'Sample Type' field identifying blanks, QC, and study samples
- Feature retention percentile threshold (e.g., 10%, 20%)

## Outputs

- Preferred (quality-filtered) feature table (TSV)
- Blank-masked feature table (optional; TSV)
- Updated experiment object with 'preferred' and/or custom moniker registrations
- QC report documenting number of features and samples pre/post filtering

## How to apply

Asari generates both 'full' (complete features) and 'preferred' (quality-filtered) feature table monikers by default; the preferred table applies feature retention filters based on sample prevalence thresholds. To apply manual filtering: (1) load the full feature table and blank sample data; (2) optionally perform blank masking by identifying features with signal intensity in blanks comparable to or exceeding signal in study samples, flagging these as likely contaminants; (3) drop features present in fewer than a configured percentile of study samples (e.g., retain only features in ≥10% of samples); (4) remove QC and blank samples themselves from the table if they are not required for downstream analysis; (5) register the filtered table with an appropriate moniker (e.g., 'preferred') and store it in the asari_results directory. The rationale is that rare features are often technical noise or instrument artifacts, while ubiquitous blank contamination obscures true metabolic signal.

## Related tools

- **Asari** (Generates 'full' and 'preferred' feature tables; preferred moniker incorporates default quality filtering) — https://github.com/shuzhao-li/asari
- **PCPFM (PythonCentricPipelineForMetabolomics)** (Orchestrates mzML-to-feature-table workflow and provides interface to apply filtering steps and register filtered tables with experiment metadata) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **metDataModel** (Defines common data model for representing filtered feature tables and experiment objects with standardized moniker registration) — https://github.com/shuzhao-li-lab/metDataModel

## Examples

```
pcpfm filter --input asari_results/full_Feature_table.tsv --blank_samples blanks.csv --retention_percentile 10 --output feature_tables/preferred_filtered.tsv --register_moniker preferred
```

## Evaluation signals

- Filtered table has fewer features than full table; row count reduction is proportional to percentile threshold and blank/QC prevalence.
- Blank-masked features show zero or near-zero intensity in study samples but elevated intensity in blank samples, confirming contaminant identification.
- Feature retention rate matches configured percentile cutoff (e.g., if threshold is 10%, ≤90% of features are dropped).
- Sample counts match expected study design after QC/blank removal (e.g., if 10 blanks + 50 study samples input, output has 50 rows).
- Filtered table is successfully registered in experiment object with moniker 'preferred' or custom label, and is accessible for downstream normalization and annotation steps.

## Limitations

- Feature retention percentile thresholds are heuristic; no statistical consensus exists on optimal cutoffs—practitioners must validate against known metabolites or orthogonal data.
- Blank masking requires representative blank samples; if blanks are non-informative or contaminated, masking may fail or remove true signals.
- The pipeline currently lacks built-in support for internal spike-in standards for QC-based filtering; this feature is marked 'TO BE IMPLEMENTED' and must be applied externally.
- GC-MS and other data types beyond LC-MS are under development; filtering pipeline is currently validated only for LC-MS(-MS) mzML inputs.
- Over-aggressive filtering can remove rare true metabolites; practitioners should cross-validate filtered features against authentic standards or public spectral databases (HMDB, MoNA) before downstream analysis.

## Evidence

- [other] Asari generates 'full' feature table containing all detected features and a 'preferred' feature table with quality-filtered features: "Asari outputs a full feature table containing all detected features and a preferred feature table with quality-filtered features, both stored in the asari_results directory."
- [intro] Features present in fewer than a specified percent of samples are dropped during filtering: "features present in fewer than this percent of samples are dropped"
- [intro] Blank masking removes features likely due to background ions and contaminants: "Blank masking to remove features likely due to background ions and contaminants"
- [intro] QC and blank samples can be dropped from feature tables for downstream analysis: "Drop undesired samples such as QC samples and blanks"
- [readme] Filtered tables are optionally blank masked, normalized, batch corrected, annotated or otherwise curated: "optionally blank masked, normalized, batch corrected, annotated or otherwise curated"
- [other] Filtered feature tables are integrated into experiment object with monikers for downstream processing: "Register both feature tables in the experiment object with monikers 'full' and 'preferred' respectively, making them accessible for subsequent normalization, annotation, and quality control steps."
