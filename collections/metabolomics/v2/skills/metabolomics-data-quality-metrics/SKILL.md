---
name: metabolomics-data-quality-metrics
description: Use when you have a Sciex Multiquant (≥v3.0.3) txt export containing QCpool sample measurements at multiple timepoints within a sequence, and you need to flag compounds with high technical variability or signal degradation before proceeding to statistical analysis or interpretation of.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - QComics
  - Sciex Multiquant
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c03660
  title: QComics
evidence_spans:
- The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qcomics
    doi: 10.1021/acs.analchem.3c03660
    title: QComics
  dedup_kept_from: coll_qcomics
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c03660
  all_source_dois:
  - 10.1021/acs.analchem.3c03660
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-quality-metrics

## Summary

Compute coefficient of variation (CV) and signal-trend metrics from QCpool (quality control pool) samples injected at regular intervals during liquid chromatography–mass spectrometry (LC-MS) sequences to rapidly assess technical reproducibility and instrumental drift in metabolomics or lipidomics studies. This skill enables detection of compounds with poor quality metrics before downstream analysis.

## When to use

Apply this skill when you have a Sciex Multiquant (≥v3.0.3) txt export containing QCpool sample measurements at multiple timepoints within a sequence, and you need to flag compounds with high technical variability or signal degradation before proceeding to statistical analysis or interpretation of metabolomics/lipidomics data.

## When NOT to use

- Input data are not from Sciex Multiquant or are in a format other than txt export — use vendor-specific quality control tools or reformatting steps first.
- QCpool samples were not injected at regular intervals during the sequence — CV and trend metrics require time-series structure to detect drift.
- The analysis goal is compound identification or metabolite annotation rather than quality control assessment — use orthogonal tools (MS/MS matching, retention time prediction, etc.) instead.

## Inputs

- Sciex Multiquant txt export file containing QCpool sample measurements
- QCpool positional table with compound identifiers and signal intensities per injection

## Outputs

- Per-compound coefficient of variation (CV) summary
- Signal-trend metrics (slope, drift, stability index) per compound across injection sequence
- Quality overview report (table and/or figure) flagging compounds with acceptable vs. poor quality metrics

## How to apply

Load the QCpool positional table exported from Sciex Multiquant txt format and parse compound identifiers with their signal intensities across sequential injections. For each compound, calculate the coefficient of variation (CV) as the standard deviation divided by mean intensity across all QCpool measurements to quantify technical reproducibility. Assess signal-trend metrics such as linear slope, drift, or stability index across the injection sequence to detect instrumental signal degradation or systematic bias. Aggregate per-compound CV and trend results into a summary table, flagging compounds with CV exceeding acceptable thresholds (article does not specify a numerical cutoff but implies compounds are categorized as 'acceptable vs. poor quality metrics') and those showing significant slope or drift. Generate a quality overview report in tabular and/or visual format suitable for rapid qualitative assessment before releasing the study dataset for downstream analysis.

## Related tools

- **Sciex Multiquant** (Instrument data processing software that analyzes QCpool samples and exports compound signal intensities in txt format for quality assessment)
- **QComics** (R/Python package that ingests Sciex Multiquant txt exports, computes per-compound CV and signal-trend metrics, and generates quality overview visualizations and summaries) — https://github.com/ricoderks/QComics

## Evaluation signals

- CV values are computed for every compound across all QCpool injections and fall within expected ranges (typically 0–100% for biological or instrumental samples).
- Signal-trend metrics (slope, drift indices) are calculated for each compound and flagged when they exceed acceptable thresholds (article does not specify numerical thresholds but expects compounds to be ranked or categorized as acceptable vs. poor).
- Quality overview report clearly separates compounds into 'acceptable' and 'poor quality' categories, enabling rapid visual inspection for compounds with systematic problems (e.g., CV > threshold or significant drift).
- Output table/figure is suitable for inclusion in study methods or supplementary materials to document QC performance.
- All QCpool injections in the input sequence are represented in CV and trend calculations (no missing timepoints should be silently excluded).

## Limitations

- Sciex Multiquant software version must be ≥v3.0.3; earlier versions may produce incompatible txt export formats.
- Quality assessment relies on QCpool samples injected at regular intervals; irregular or sparse QCpool sampling reduces the sensitivity of trend detection and CV estimation.
- No numerical CV or drift thresholds are specified in the source material; users must define acceptable cutoffs based on their own study design, instrument platform, and metabolite class (e.g., lipids may have different CVs than primary metabolites).
- No changelog is available for the QComics package, limiting traceability of algorithm changes or bug fixes across versions.

## Evidence

- [intro] The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
- [intro] QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to txt format: "QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [intro] a pooled sample (QCpool) needs to measured in regular intervals during one or more sequences: "a pooled sample (QCpool) needs to measured in regular intervals during one or more sequences"
- [other] Calculate per-compound coefficient of variation (CV) as a measure of technical reproducibility and assess signal-trend metrics (slope, drift, stability index) across injection sequence: "Calculate per-compound coefficient of variation (CV) as a measure of technical reproducibility. 4. Assess signal-trend metrics (e.g., slope, drift, or stability index) across the injection sequence"
- [other] Aggregate CV and trend results into a summary table or visualization highlighting compounds with acceptable vs. poor quality metrics: "Aggregate CV and trend results into a summary table or visualization highlighting compounds with acceptable vs. poor quality metrics"
