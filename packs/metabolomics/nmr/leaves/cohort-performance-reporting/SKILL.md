---
name: cohort-performance-reporting
description: Use when you have NMR metabolite measurements from peripheral blood samples
  (plasma/serum) paired with processing delay metadata (pre-centrifugation and post-centrifugation
  times) and need to benchmark metabolic parameter stability across delay windows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2945
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - PRIMA-Panel
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c04938
  title: PRIMA-Panel
evidence_spans:
- Pre-Analytical Investigator for NMR-based Metabolomics (PRIMA-Panel)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_prima_panel_cq
    doi: 10.1021/acs.analchem.4c04938
    title: PRIMA-Panel
  dedup_kept_from: coll_prima_panel_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c04938
  all_source_dois:
  - 10.1021/acs.analchem.4c04938
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cohort-performance-reporting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate stratified performance reports for metabolite cohorts under varying pre-analytical conditions (processing delays, sample type, centrifugation timing). This skill quantifies metabolic parameter stability across delay bins or continuous timepoints, flagging minor and major deviations to support pre-analytical method validation.

## When to use

You have NMR metabolite measurements from peripheral blood samples (plasma/serum) paired with processing delay metadata (pre-centrifugation and post-centrifugation times) and need to benchmark metabolic parameter stability across delay windows. Use this skill when you must communicate which metabolites are robust to processing delays and which show clinically or analytically significant drift—typically to validate sample handling protocols or set acceptable processing windows for a cohort.

## When NOT to use

- Input metabolite data lack paired processing delay or SPREC timing metadata—the skill requires explicit delay annotations to stratify and evaluate.
- Data are already processed into a feature/stability matrix or aggregated by delay window; the skill is designed for raw metabolite measurements paired with individual-level timing variables.
- The research question is purely exploratory (e.g., 'show me all correlations') rather than validation-focused; the skill is optimized for threshold-driven performance assessment.

## Inputs

- Metabolite measurements (NMR intensity or concentration values) from a cohort of plasma/serum samples
- Pre-analytical metadata table: pre-centrifugation delay (minutes), post-centrifugation delay (minutes), sample type (plasma vs. serum), cohort identifier
- SPREC classification codes (or equivalent delay timepoints in minutes)

## Outputs

- Tabular performance report (HTML and/or CSV) stratified by processing delay bin or continuous delay values
- Summary statistics table per metabolite per delay stratum (mean, SD, correlation coefficients)
- Annotated metabolite table flagging minor and major changes per delay window
- Interactive visualizations (scatter, line, or lollipop plots) linking delay duration to metabolic parameter values

## How to apply

Load the metabolite dataset and pre-analytical metadata (SPREC-classified processing delay times, sample type, cohort identifiers) into the PRIMA-Panel interface. Parse and validate that metabolite measurements and delay variables are properly formatted and aligned. Stratify the cohort by pre-centrifugation and post-centrifugation delay bins (or use continuous delay sliders); for each stratum, compute descriptive statistics (mean, SD, correlation) and flag metabolites showing minor or major changes relative to a reference state (baseline or shortest delay). Configure color thresholds (e.g., % change cutoffs) to highlight clinically or analytically significant deviations. Export the tabular report as HTML (for visual inspection) or CSV (for downstream analysis), enabling stakeholders to identify which metabolites and delay ranges are within acceptable limits.

## Related tools

- **PRIMA-Panel** (Interactive data exploration and performance report generation interface for visualizing metabolic parameter drift across processing delays and exporting stratified summary tables with configurable color-coded thresholds) — https://github.com/funkam/PRIMA

## Evaluation signals

- Exported performance report includes all metabolites from the input dataset, stratified by pre- and post-centrifugation delay bins, with no missing values or dropped samples (except where explicitly filtered by user).
- Descriptive statistics (mean, SD, correlation) are correctly computed for each metabolite within each delay stratum and match spot-checks against the raw input.
- Color-coded flags (minor and major change indicators) are consistently applied: metabolites crossing the user-specified % threshold are flagged; those within threshold remain unmarked.
- HTML report renders correctly with interactive filtering/sorting; CSV export is machine-readable and preserves all stratification dimensions (delay bin, sample type, cohort).
- Visualizations (scatter/line/lollipop plots) accurately represent the relationship between delay duration and individual metabolic parameter values across the cohort without outlier distortion or misaligned axes.

## Limitations

- The skill assumes delay metadata are accurately recorded and linked to metabolite samples; misalignment between timing records and measurements will produce misleading correlation and stability estimates.
- Performance thresholds (% change cutoffs for minor/major flags) are user-configurable and subjective; the skill does not prescribe clinically or analytically validated cutoffs—users must select thresholds based on their specific metabolite, instrument, and use case.
- The tool stratifies by delay bins or sliders but does not automatically detect or correct for non-linear delay effects, batch effects, or confounders (e.g., sample storage temperature, light exposure); users must interpret results in context.
- Reports are generated per cohort upload; comparison across independent cohorts or meta-analysis across multiple studies is manual and not integrated into the PRIMA-Panel interface.

## Evidence

- [readme] Tool function and core use case: "The PRIMA-Panel is a tool to investigate the effect of processing delays on metabolic parameters in samples of peripheral blood (plasma / serum)."
- [readme] Interactive data exploration capability: "The panel functions as a data expoloration tool. It allows to investigate the these effects interactively."
- [readme] Performance report generation and stratification: "The 'Single' tab allows the user to set a pre-centrifugation time and a post-centrifugation using a Slider. A table is then generated that higlights a minor and a major change for each metabolite in"
- [readme] Export capability and formats: "The table can be downloaded as a .HTML report or the table directly as .csv (or other formats)."
- [other] Workflow input validation and data organization: "Parse and validate the input data structure to ensure metabolite measurements and delay variables are present and properly formatted."
- [readme] Cohort metadata and pre-analytical information upload: "PRIMA-Panel allows the creation of so called performance reports for sample cohorts. Here a data table with pre-analytical information can be uploaded"
- [readme] SPREC-based delay classification: "The time-points are sorted according to their SPREC classification. In addition, there is an alternative way of presenting the date in form of lollipop plots."
