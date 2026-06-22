---
name: signal-trend-assessment-across-injections
description: Use when you have QCpool (pooled quality control) samples measured at regular intervals across one or more LC-MS/MS sequences and need to detect whether instrument performance degrades, drifts, or destabilizes during the analytical run.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - QComics
  - Sciex Multiquant
  techniques:
  - LC-MS
  - tandem-MS
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

# signal-trend-assessment-across-injections

## Summary

Assess instrumental drift and signal degradation in metabolomics/lipidomics quality control by computing trend metrics (slope, drift, stability index) across sequential QCpool injection data. This skill detects temporal instability in mass spectrometry signal that may compromise study reproducibility.

## When to use

Apply this skill when you have QCpool (pooled quality control) samples measured at regular intervals across one or more LC-MS/MS sequences and need to detect whether instrument performance degrades, drifts, or destabilizes during the analytical run. Use it as part of post-acquisition quality review before committing metabolomics or lipidomics data to downstream analysis.

## When NOT to use

- Input is already a quality-filtered feature table or normalized metabolite abundance matrix — signal trend assessment targets raw instrumental signals, not processed abundances.
- QCpool samples were not measured at regular intervals throughout the sequence — trend assessment requires evenly-spaced or well-documented temporal distribution to detect drift reliably.
- Data source is not Sciex Multiquant output or an equivalent instrument-specific export with parsed signal intensities — this skill depends on machine-readable, injection-ordered intensity data.

## Inputs

- Sciex Multiquant txt export containing QCpool positional table
- Parsed compound identifiers (names or mass-to-charge ratios)
- Signal intensities (peak areas or heights) from sequential QCpool injections
- Injection sequence metadata (sample order, injection number, timestamp if available)

## Outputs

- Trend metric summary table (per-compound slope, drift, stability index values)
- Quality assessment flags (acceptable vs. poor trend metrics per compound)
- Visualization of signal intensity across injection sequence (e.g., scatter plot with trend line per compound)
- Quality overview report highlighting compounds with instrumental drift or signal degradation

## How to apply

Load parsed QCpool positional data (compound identifiers and signal intensities) from Sciex Multiquant txt export in sequential injection order. For each compound, fit a trend model (linear regression for slope/drift detection or rolling-window stability index) across the injection sequence to quantify signal change over time. Calculate metrics such as slope magnitude (% change per injection), absolute drift from expected baseline, or coefficient of variation across moving windows to characterize stability. Aggregate results into a summary table flagging compounds with significant drift (e.g., slope exceeding predefined threshold) or poor stability (high rolling CV). Use these flagged compounds to assess whether instrumental conditions remained acceptable throughout the sequence; compounds with acceptable metrics indicate robust technical reproducibility, while widespread drift suggests need for instrument maintenance or sequence re-analysis.

## Related tools

- **QComics** (Primary tool for computing and aggregating signal-trend metrics (slope, drift, stability index) and generating quality overview visualizations from QCpool injection data.) — https://github.com/ricoderks/QComics
- **Sciex Multiquant** (Upstream software (version > v3.0.3) that analyzes QCpool samples and exports positional data in txt format; required input source for trend assessment.)

## Evaluation signals

- Trend metrics (slope, drift, stability index) are computed for all compounds in the QCpool table and reported in summary output with numeric precision.
- Per-compound trend values are accompanied by quality flags ('acceptable' vs. 'poor') that align with predefined thresholds or literature-standard reproducibility cutoffs (e.g., drift within expected instrument variation).
- Visualization (e.g., time-series plot with fitted trend line) shows signal intensity trajectory for a representative subset of compounds; visual trend agreement should match reported slope/drift values.
- Aggregate statistics (e.g., percentage of compounds with acceptable trend metrics) are presented to enable rapid assessment of overall sequence quality.
- Edge cases (missing injections, zero or near-zero intensities, outlier spikes) are either handled transparently (e.g., documented in report) or flagged for manual review.

## Limitations

- Trend assessment depends on regular injection intervals; sparse or irregular QCpool sampling may yield unreliable drift estimates.
- Slope and drift metrics assume linear or quasi-linear signal decay/increase; non-linear instrumental behavior or sudden instrument failures may not be detected by simple linear regression.
- The skill operates on raw signal intensities; if Sciex Multiquant applies normalization or background subtraction within txt export, trend metrics will reflect post-processed, not true raw, signals.
- Optimal thresholds for flagging 'poor' trend metrics are context-dependent (instrument type, method robustness, regulatory requirements) and not universally defined in the source material.

## Evidence

- [other] Assess signal-trend metrics (e.g., slope, drift, or stability index) across the injection sequence to detect instrumental drift or signal degradation.: "Assess signal-trend metrics (e.g., slope, drift, or stability index) across the injection sequence to detect instrumental drift or signal degradation."
- [intro] a pooled sample (QCpool) needs to measured in regular intervals during one or more sequences: "a pooled sample (QCpool) needs to measured in regular intervals during one or more sequences"
- [intro] QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format: "QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [intro] The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
- [other] Parse compound identifiers and signal intensities across sequential QCpool injections.: "Parse compound identifiers and signal intensities across sequential QCpool injections."
