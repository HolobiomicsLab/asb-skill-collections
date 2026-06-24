---
name: quality-control-threshold-optimization
description: Use when when you have extracted a peak feature table (CSV or tabular
  format) with mass-to-charge ratios, retention times, and intensity values across
  multiple samples, and you need to distinguish genuine differential metabolic signals
  from instrumental noise or low-abundance background before.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaQC
  - MARC
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.21147/j.issn.1000-9604.2023.05.11
  title: OpenNAU
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_opennau_cq
    doi: 10.21147/j.issn.1000-9604.2023.05.11
    title: OpenNAU
  dedup_kept_from: coll_opennau_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21147/j.issn.1000-9604.2023.05.11
  all_source_dois:
  - 10.21147/j.issn.1000-9604.2023.05.11
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Quality Control Threshold Optimization

## Summary

A systematic approach to filter extracted mass spectrometry peak features by applying signal-to-noise thresholds and feature prevalence criteria to identify differential metabolic ion peaks suitable for downstream metabolite identification. This skill bridges raw peak extraction and statistical annotation by removing low-abundance or noisy peaks that would confound group-wise comparisons.

## When to use

When you have extracted a peak feature table (CSV or tabular format) with mass-to-charge ratios, retention times, and intensity values across multiple samples, and you need to distinguish genuine differential metabolic signals from instrumental noise or low-abundance background before performing statistical group comparisons or metabolite identification.

## When NOT to use

- Input data is already a curated, vendor-validated metabolite list rather than raw extracted peaks
- Analysis goal is untargeted feature discovery without group-wise comparison (threshold optimization is predicated on differential signal detection)
- Peak table has already undergone aggressive filtering by upstream preprocessing; re-filtering risks removing true signal

## Inputs

- Peak feature table (CSV or tabular format) with mass-to-charge ratios, retention times, and intensity values
- Experimental group assignments for all samples
- Signal-to-noise threshold parameters
- Feature prevalence thresholds (minimum sample detection fraction)

## Outputs

- QC-filtered peak feature table with passing features annotated
- QC filter application log (which thresholds were applied to each feature)
- Differential intensity summary statistics (fold-change and/or p-values for group comparisons)

## How to apply

Load the extracted peak feature table and sequentially apply two classes of quality control filters: (1) abundance and noise filters using signal-to-noise thresholds to remove low-intensity or noisy peaks, and (2) feature prevalence criteria to exclude peaks present in only a small subset of samples. After filtering, identify peaks with significant differential intensity patterns between experimental groups using statistical comparison methods (fold-change or p-value thresholds). Retain only candidate peaks that pass all QC criteria and export the filtered table with annotations documenting which QC filters were applied and which peaks survived. The rationale is that removing noisy, low-abundance, or sporadically detected features reduces false positives in downstream metabolite annotation while preserving genuine differential signals.

## Related tools

- **MetaQC** (Applies quality control filtering to extracted peak features according to signal-to-noise and prevalence thresholds) — https://github.com/zjuRong/openNAU
- **MARC** (Performs downstream metabolite annotation and reference database matching on QC-filtered peaks) — https://github.com/zjuRong/openNAU

## Evaluation signals

- QC-filtered feature table has fewer rows than input (low-abundance and noisy peaks removed)
- Exported feature table includes explicit annotations documenting which QC filters were applied to each peak
- Differential peaks identified show statistically significant fold-change or p-value signals that would be confounded if low-abundance noise were retained
- Signal-to-noise ratio distribution of retained peaks is visibly shifted toward higher quality compared to discarded peaks
- Feature prevalence of retained peaks meets or exceeds the specified threshold in a minimum fraction of samples per group

## Limitations

- Threshold selection (signal-to-noise cutoff, prevalence fraction, fold-change/p-value bounds) is not fully automated and requires expert review or prior knowledge of expected metabolite abundance ranges
- Aggressive thresholds may remove rare or condition-specific metabolites that have genuine biological significance despite low or sporadic detection
- Quality control filtering is most effective when sample replication is adequate; sparse or unbalanced group designs reduce statistical power for differential detection

## Evidence

- [intro] extraction and filtering rationale: "It includes the extraction of raw mass data and quality control for the identification of differential metabolic ion peaks."
- [other] workflow steps for filtering: "Apply quality control filters to remove low-abundance or noisy peaks according to signal-to-noise thresholds and feature prevalence criteria."
- [other] differential detection method: "Identify peaks with significant differential intensity patterns between experimental groups using statistical comparison (e.g., fold-change or p-value thresholds)."
- [other] output documentation requirement: "Export the QC-filtered feature table with annotations indicating which QC filters were applied and which peaks survive for downstream identification."
