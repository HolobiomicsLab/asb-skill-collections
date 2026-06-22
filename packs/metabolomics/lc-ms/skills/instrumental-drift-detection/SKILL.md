---
name: instrumental-drift-detection
description: Use when you have a time-series of repeated QCpool (pooled quality control) injections measured at regular intervals during one or more LC-MS/MS sequences, exported from Sciex Multiquant software (v3.0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# instrumental-drift-detection

## Summary

Detect and quantify instrumental signal drift or degradation across sequential metabolomics/lipidomics QC injections by computing trend metrics (slope, drift index, stability) from pooled sample intensities. This skill enables rapid assessment of whether instrument performance remained stable throughout an analytical sequence, flagging compounds or time windows where signal loss or systematic bias would compromise data quality.

## When to use

Apply this skill when you have a time-series of repeated QCpool (pooled quality control) injections measured at regular intervals during one or more LC-MS/MS sequences, exported from Sciex Multiquant software (v3.0.3+) in txt format, and you need to assess whether signal intensity for individual compounds remained stable or showed degradation/drift over the sequence duration. Particularly useful before proceeding to statistical analysis or metabolite quantification, to rule out instrumental artifacts as confounders.

## When NOT to use

- Input is already a feature table or normalized abundance matrix rather than raw QCpool injection-level intensities.
- QCpool samples were not analyzed with Sciex Multiquant (v3.0.3+) or exported data is not in txt format; workflow is instrument-software-specific.
- Metabolomics/lipidomics study has no pooled QC samples or QCpool measurements were taken only at the start/end of sequences rather than at regular intervals throughout.

## Inputs

- QCpool positional table (Sciex Multiquant txt export with compound identifiers and signal intensities per sequential injection)
- Injection sequence metadata (injection order, timestamp, or sequence block assignment)

## Outputs

- Per-compound trend metrics table (slope, drift index, stability index, percent signal change)
- Quality overview summary (pass/fail or severity classification by compound)
- Visualization of instrumental drift (e.g., intensity vs. injection order plot, heatmap of trend severity)
- Quality assessment report suitable for rapid review before downstream analysis

## How to apply

Load the parsed QCpool positional table (compound identifiers and signal intensities per injection). For each compound, extract the vector of intensities across sequential injection order. Compute per-compound trend metrics: linear regression slope (to detect monotonic drift), rolling coefficient of variation or stability index (to detect local degradation), and/or absolute percent change from first to last injection. Flag compounds where slope magnitude exceeds a study-specific threshold (commonly ±10–20% of mean intensity over the sequence) or where stability index falls below acceptable bounds. Aggregate these per-compound trend results alongside CV values into a summary table and visualization (e.g., scatter plot of slope vs. CV, or heatmap of trend severity by compound and sequence window). This enables rapid visual and statistical triage of which compounds or time periods show acceptable vs. poor instrument stability.

## Related tools

- **Sciex Multiquant** (Instrument software that analyzes QCpool samples and exports compound identifiers and signal intensities in txt format, which serves as input to drift detection.)
- **QComics** (R/Python package that ingests parsed QCpool positional data and computes coefficient of variation, signal-trend metrics, and quality overview summaries including instrumental drift assessment.) — https://github.com/ricoderks/QComics

## Evaluation signals

- Per-compound trend metrics (slope, drift index) are computed without errors and reported with consistent sign conventions and units (e.g., percent change per injection or per unit time).
- Compounds flagged as showing unacceptable drift are visually confirmed in intensity-vs.-injection-order plots to show monotonic or systematic degradation consistent with the computed slope/trend metric.
- Summary statistics (mean and SD of slopes, fraction of compounds exceeding drift threshold) are reproducible when the same QCpool table is re-analyzed, indicating computational stability.
- Comparison of drift metrics before vs. after instrument maintenance/calibration shows expected reduction in drift magnitude, confirming the metric's sensitivity to actual instrumental state changes.
- Compounds with high CV also tend to have high drift index (or vice versa), suggesting internal consistency between reproducibility and stability assessments; discordance warrants investigation of outlier injections or instrumental events.

## Limitations

- Drift detection assumes QCpool injections are evenly spaced in time and that temporal order reflects instrumental state; irregular or clustered QCpool sampling may confound trend estimates.
- Sciex Multiquant software-specific (v3.0.3+); workflows using other instrument platforms (e.g., Orbitrap, Bruker) or export formats (mzML, netCDF) require adapted parsing and may not directly apply QComics outputs.
- Threshold for flagging unacceptable drift is study- and compound-dependent; no universal cutoff is provided. Practitioner must establish context-specific bounds based on instrumental specifications, analytical method, and downstream statistical power requirements.
- Drift detection is blind to the chemical or biological reason for signal change; instrumental drift, ionization suppression from matrix effects, and degradation of authentic standards are not discriminable from trend metrics alone.
- No changelog found in QComics repository, limiting visibility into bug fixes, parameter defaults, or breaking changes across versions.

## Evidence

- [intro] a pooled sample (QCpool) needs to measured in regular intervals during one or more sequences: "a pooled sample (QCpool) needs to measured in regular intervals during one or more sequences"
- [intro] QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format: "QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [other] Assess signal-trend metrics (e.g., slope, drift, or stability index) across the injection sequence to detect instrumental drift or signal degradation.: "Assess signal-trend metrics (e.g., slope, drift, or stability index) across the injection sequence to detect instrumental drift or signal degradation."
- [intro] The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
- [other] Parse compound identifiers and signal intensities across sequential QCpool injections.: "Parse compound identifiers and signal intensities across sequential QCpool injections."
