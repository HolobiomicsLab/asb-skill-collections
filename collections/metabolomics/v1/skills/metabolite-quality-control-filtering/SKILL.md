---
name: metabolite-quality-control-filtering
description: Use when after feature extraction (Asari) has produced a full feature table from mzML data, but before normalization and annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - ThermoRawFileParser
  - Asari
  - khipu
  - PCPFM (Python-Centric Pipeline for Metabolomics)
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

# metabolite-quality-control-filtering

## Summary

Remove low-quality, rare, or contaminated metabolite features from LC-MS feature tables using blank masking, sample dropping, and missing-value retention thresholds. This skill ensures downstream statistical analysis operates on high-confidence, frequently observed metabolites.

## When to use

Apply this skill after feature extraction (Asari) has produced a full feature table from mzML data, but before normalization and annotation. Use it when your dataset contains blank samples (to identify and remove contaminants), QC/control samples marked in metadata, or when you observe that many features appear sporadically across samples. Trigger: raw feature table contains both sample and blank acquisitions, or metadata includes 'sample_type' field with 'QC', 'Blank', or 'Unknown' labels.

## When NOT to use

- Input is already a curated feature table from a prior analysis (applying QC filtering twice risks over-filtering and loss of biological signal).
- Dataset contains no blank samples or control replicates (blank masking and sample dropping steps become ineffective).
- Sample metadata does not include sample type or batch fields (filtering logic cannot distinguish blanks from unknowns).

## Inputs

- feature table (TSV format) from Asari extraction with m/z, retention time, and intensity columns
- sample metadata CSV with sample names, file paths, sample types (Blank/QC/Unknown), and batch identifiers
- experiment JSON state object containing QAQC results and sample annotations

## Outputs

- blank-masked feature table (contaminated features removed)
- sample-dropped feature table (control and failed-QC samples removed)
- filtered feature table (infrequent features below retention percentile removed)
- final QC-ready feature table with high-confidence metabolites

## How to apply

Execute three sequential filtering steps on the feature table. First, run blank masking by comparing feature intensities in sample to blank samples using a configurable intensity-ratio threshold (default 3×); remove features where blank intensity exceeds sample intensity, applying this separately if multiple blank types exist. Second, drop unwanted samples (blanks, QC replicates, failed QC) by matching metadata fields (e.g., sample_type=='Blank') or by QAQC filter criteria recorded in the experiment JSON state. Third, filter out infrequent features using a feature-retention percentile threshold (default 50%); this removes sparse features that appear in fewer than the cutoff percentage of samples. These steps are applied in sequence because blank masking eliminates contaminant signals before sample dropping removes control samples, and missing-value filtering ensures the final table contains only metabolites observed consistently.

## Related tools

- **Asari** (Upstream feature extraction that produces the initial full feature table subjected to QC filtering) — https://github.com/shuzhao-li/asari
- **PCPFM (Python-Centric Pipeline for Metabolomics)** (Orchestrates blank_masking, drop_samples, and drop_missing_features commands in sequence with configurable thresholds) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Python** (Implementation language for QC filtering logic and CLI commands)

## Examples

```
pcpfm blank_masking --experiment_dir ./my_experiment --blank_type Blank --intensity_ratio 3.0 && pcpfm drop_samples --experiment_dir ./my_experiment --metadata_field sample_type --metadata_value Blank && pcpfm drop_missing_features --experiment_dir ./my_experiment --feature_percentile 50
```

## Evaluation signals

- Blank-masked table has fewer features than input table; verify by row count and confirm removed features have blank intensity ≥ sample intensity × 3.
- Sample-dropped table lacks all rows matching sample_type=='Blank' or sample_type=='QC' in metadata; inspect experiment.json for 'dropped_samples' list.
- Final filtered table retains only features appearing in ≥50% of samples (or configured percentile); check feature presence distribution before and after using pandas value_counts() on non-zero intensity columns.
- No NaN or inf values appear in remaining feature intensities; validate with pandas.isna().sum() == 0 and pandas.isinf().sum() == 0.
- Sample counts in final table match expected unknowns (total samples minus blanks minus failed QC); cross-check against metadata row count.

## Limitations

- Blank masking assumes blank samples are representative of contamination across the experiment; if blanks are collected under different conditions than samples, intensity ratios may not reflect true contaminant levels.
- Feature-retention percentile (default 50%) is arbitrary; setting too high removes genuine rare metabolites; too low retains uninformative sparse features. Optimization requires biological validation or pilot QC inspection.
- The pipeline requires properly formatted metadata with consistent sample_type values; malformed or missing sample_type entries will cause sample dropping to fail silently or incorrectly.
- Batch correction is optional and applied post-QC; if batch effects are strong, they may inflate apparent feature variance before filtering, potentially altering which features pass the retention threshold.

## Evidence

- [other] blank masking by comparing sample to blank intensities with configurable intensity ratios: "blank masking by comparing sample to blank intensities with configurable intensity ratios"
- [other] sample dropping by metadata field or QAQC results: "sample dropping by metadata field or QAQC results"
- [other] Remove infrequent features via pcpfm drop_missing_features using feature-retention percentile threshold (default 50%) to discard rare features: "Remove infrequent features via pcpfm drop_missing_features using feature-retention percentile threshold (default 50%) to discard rare features"
- [other] Perform blank masking using pcpfm blank_masking with intensity-ratio threshold (default 3×) to remove features where blank intensity exceeds sample intensity: "Perform blank masking using pcpfm blank_masking with intensity-ratio threshold (default 3×) to remove features where blank intensity exceeds sample intensity"
- [other] Drop unwanted samples (QC, blanks) via pcpfm drop_samples by metadata field match, sample name, or QAQC filter criteria: "Drop unwanted samples (QC, blanks) via pcpfm drop_samples by metadata field match, sample name, or QAQC filter criteria"
- [readme] This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM: "This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM"
