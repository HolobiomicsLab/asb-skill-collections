---
name: metabolic-ion-peak-filtering
description: Use when you have a raw or extracted peak feature table (CSV or tabular format) containing mass-to-charge ratios, retention times, and intensity values across multiple samples from different experimental groups, and you need to identify which peaks show statistically significant differential.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - metaQC
  - openNAU
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolic-ion-peak-filtering

## Summary

Apply quality control filtering to extracted mass spectrometry peak features to identify differential metabolic ion peaks between experimental groups. This skill removes low-abundance or noisy peaks using signal-to-noise thresholds and feature prevalence criteria, then flags peaks with significant differential intensity patterns.

## When to use

You have a raw or extracted peak feature table (CSV or tabular format) containing mass-to-charge ratios, retention times, and intensity values across multiple samples from different experimental groups, and you need to identify which peaks show statistically significant differential abundance or intensity between conditions while filtering out instrument noise and low-confidence features.

## When NOT to use

- Input is raw mass spectrometry data (mzML, NetCDF, or vendor format) rather than an already-extracted peak feature table — use peak extraction first.
- You only have a single experimental group or sample — differential identification requires at least two groups for comparison.
- Peaks have already been validated and annotated to known metabolites — this skill is for screening and filtering, not post-identification QC.

## Inputs

- peak feature table (CSV or tabular format)
- mass-to-charge ratios (m/z)
- retention times
- intensity values across all samples
- experimental group assignments

## Outputs

- QC-filtered peak feature table
- annotations indicating which QC filters were applied per peak
- candidate differential metabolic ion peaks
- peak-level filter status indicators

## How to apply

Load the peak feature table with m/z ratios, retention times, and intensity values across all samples. Apply quality control filters to remove peaks below signal-to-noise thresholds and those failing feature prevalence criteria (e.g., present in too few samples or too low intensity). Use statistical comparison between experimental groups—such as fold-change thresholds or p-value cutoffs—to identify peaks with significant differential intensity patterns. Retain only peaks that pass all QC criteria and annotate the output table to document which filters were applied and which peaks survive. Export the filtered feature table with peak-level filter pass/fail indicators for downstream metabolite identification.

## Related tools

- **metaQC** (Quality control module within openNAU for filtering extracted peak features using signal-to-noise and prevalence thresholds) — https://github.com/zjuRong/openNAU
- **openNAU** (Complete analysis platform integrating raw mass data extraction and quality control filtering for identification of differential metabolic ion peaks) — https://github.com/zjuRong/openNAU

## Evaluation signals

- Output table row count is less than or equal to input (no peaks are added, only removed or retained).
- Each row in the output table has a corresponding QC filter annotation indicating which thresholds were applied.
- Peaks retained in the output show documented signal-to-noise ratios above the specified threshold.
- Differential peaks exhibit statistically significant intensity differences (fold-change or p-value) between experimental groups.
- All filtered-out peaks can be traced to a specific QC criterion (e.g., low prevalence, below SNR threshold, non-significant fold-change).

## Limitations

- QC thresholds (signal-to-noise, feature prevalence, fold-change, p-value cutoffs) must be set appropriately for the specific metabolomics platform and biological context — inappropriate thresholds may remove true features or retain noise.
- Statistical power for differential identification depends on sample size and biological variability; small or highly variable sample sets may yield unstable results.
- The skill assumes intensity values are comparable across samples; if raw data require normalization, that step must precede QC filtering.

## Evidence

- [readme] The software includes extraction of raw mass data and quality control for the identification of differential metabolic ion peaks.: "extraction of raw mass data and quality control for the identification of differential metabolic ion peaks"
- [other] Apply quality control filters to remove low-abundance or noisy peaks according to signal-to-noise thresholds and feature prevalence criteria.: "Apply quality control filters to remove low-abundance or noisy peaks according to signal-to-noise thresholds and feature prevalence criteria"
- [other] Identify peaks with significant differential intensity patterns between experimental groups using statistical comparison (e.g., fold-change or p-value thresholds).: "Identify peaks with significant differential intensity patterns between experimental groups using statistical comparison (e.g., fold-change or p-value thresholds)"
- [other] Load the extracted peak feature table (CSV or tabular format) containing mass-to-charge ratios, retention times, and intensity values across all samples.: "Load the extracted peak feature table (CSV or tabular format) containing mass-to-charge ratios, retention times, and intensity values across all samples"
- [other] Export the QC-filtered feature table with annotations indicating which QC filters were applied and which peaks survive for downstream identification.: "Export the QC-filtered feature table with annotations indicating which QC filters were applied and which peaks survive for downstream identification"
