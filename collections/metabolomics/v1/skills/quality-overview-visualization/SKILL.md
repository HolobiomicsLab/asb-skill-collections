---
name: quality-overview-visualization
description: Use when you have sequential QCpool (pooled quality control) samples analyzed with Sciex Multiquant (≥v3.0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - QComics
  - Sciex Multiquant
derived_from:
- doi: 10.1021/acs.analchem.3c03660
  title: QComics
evidence_spans:
- The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qcomics
    doi: 10.1021/acs.analchem.3c03660
    title: QComics
  dedup_kept_from: coll_qcomics
schema_version: 0.2.0
---

# quality-overview-visualization

## Summary

Generate a rapid visual and tabular assessment of metabolomics or lipidomics study quality by computing per-compound coefficient of variation (CV) and signal-trend metrics from QCpool injection sequences. This skill enables quick identification of compounds and instrumental phases with acceptable versus poor reproducibility and drift characteristics.

## When to use

Apply this skill when you have sequential QCpool (pooled quality control) samples analyzed with Sciex Multiquant (≥v3.0.3) and exported to txt format, and you need to assess technical reproducibility and instrumental stability across a metabolomics or lipidomics sequence before proceeding to statistical or biological interpretation.

## When NOT to use

- Input QCpool data is not from Sciex Multiquant or has not been exported to txt format with intact positional metadata.
- Study design does not include regular QCpool injections at intervals throughout the analytical sequence.
- Analysis goal is compound identification or quantification—this skill is for quality triage, not metabolite calling or peak integration.

## Inputs

- Sciex Multiquant txt export containing QCpool positional data (compound IDs, signal intensities, injection sequence metadata)

## Outputs

- Quality overview summary table (per-compound CV, trend metrics, quality flags)
- Quality overview visualization (e.g., heatmap, scatter plot, or trend plot highlighting acceptable vs. poor compounds)
- Quality assessment report suitable for rapid study-wide quality review

## How to apply

Load the QCpool positional table from the Sciex Multiquant txt export and parse compound identifiers and signal intensities across sequential QCpool injections. Calculate per-compound coefficient of variation (CV) as a measure of technical reproducibility. Assess signal-trend metrics (e.g., slope, drift, or stability index) across the injection sequence to detect instrumental drift or signal degradation. Aggregate CV and trend results into a summary table or visualization (e.g., heatmap, scatter plot, or trend lines) that highlights compounds with acceptable versus poor quality metrics. The rationale is that regular QCpool measurement throughout sequences captures both within-run instrument drift and compound-specific technical noise; compounds with CV exceeding typical thresholds or trending signals indicate either systematic instrumental problems or genuine analyte instability that should be flagged before downstream analysis.

## Related tools

- **Sciex Multiquant** (Data acquisition and export; processes QCpool samples and exports positional data to txt format for downstream quality assessment)
- **QComics** (Quality overview generation; parses Sciex Multiquant txt exports, computes CV and trend metrics per compound, and produces summary visualizations and reports) — https://github.com/ricoderks/QComics

## Evaluation signals

- CV values are computed and reported for every compound in the QCpool data; missing or NaN values indicate parsing or calculation failure.
- Signal-trend metrics (slope, drift magnitude, or stability index) are present and correctly span the full injection sequence without gaps.
- The summary table includes both per-compound metrics and per-injection or per-phase metadata (e.g., time, sequence position) to enable temporal correlation.
- Visualization clearly distinguishes compounds/phases flagged as 'acceptable' vs. 'poor' quality using distinct visual encoding (color, marker, or annotation).
- Quality thresholds (CV cutoff, drift tolerance, signal degradation threshold) are explicitly reported or configurable; the report documents which compounds exceed them and why.

## Limitations

- QComics requires QCpool data exported from Sciex Multiquant (≥v3.0.3) in txt format; compatibility with other vendor formats or software versions is not documented.
- The skill assumes regular, evenly-spaced QCpool injections throughout the sequence; sparse or irregular QCpool timing may reduce sensitivity to instrumental drift detection.
- CV and trend metrics are univariate per-compound; they do not capture multivariate covariance or batch effects that might affect the entire cohort simultaneously.

## Evidence

- [intro] The goal of the QComics package is to have a quick overview of the quality of a metabolomics or lipidomics study: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
- [intro] QCpool samples need to be analysed with Sciex Multiquant and exported to txt format: "QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [intro] Pooled samples measured at regular intervals to generate quality assessment: "a pooled sample (QCpool) needs to measured in regular intervals during one or more sequences"
- [other] Coefficient of variation and trend-based quality metrics computed from QCpool data: "Calculate per-compound coefficient of variation (CV) as a measure of technical reproducibility. Assess signal-trend metrics (e.g., slope, drift, or stability index) across the injection sequence"
- [other] Quality overview delivered as summary table and visualization for rapid assessment: "Aggregate CV and trend results into a summary table or visualization highlighting compounds with acceptable vs. poor quality metrics. Generate a quality overview report (table and/or figure) suitable"
