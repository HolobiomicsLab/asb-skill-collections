---
name: pre-analytical-delay-stratification
description: Use when when you have NMR metabolite measurements paired with documented
  pre-centrifugation and post-centrifugation delay times, and need to assess how processing
  delays affect metabolic parameter stability within a plasma or serum sample cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - PRIMA-Panel
  techniques:
  - NMR
  license_tier: restricted
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

# pre-analytical-delay-stratification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interactive stratification and visualization of NMR metabolic parameters by processing delay intervals (pre- and post-centrifugation) to assess stability and identify minor/major metabolite changes across time-points. Used in quality control workflows for peripheral blood sample metabolomics studies.

## When to use

When you have NMR metabolite measurements paired with documented pre-centrifugation and post-centrifugation delay times, and need to assess how processing delays affect metabolic parameter stability within a plasma or serum sample cohort. Specifically when generating quality control performance reports stratified by SPREC-classified delay intervals.

## When NOT to use

- Metabolite data lacks accompanying pre- or post-centrifugation delay metadata — the skill requires both delay timing and metabolite measurements linked by sample identifier.
- Input metabolites are already aggregated or normalized by delay — the skill is designed for raw or minimally processed measurements where delay effects are still observable.
- Study uses only a single fixed processing delay with no variation across samples — no stratification or delay-dependent variation to explore.

## Inputs

- NMR metabolite measurement table (numeric values per metabolite, per sample)
- Pre-analytical metadata table with pre-centrifugation delay times (minutes)
- Pre-analytical metadata table with post-centrifugation delay times (minutes)
- Sample type annotations (plasma or serum)
- Cohort or group labels

## Outputs

- Interactive visualizations stratified by processing delay bins (scatter, line, box, lollipop plots)
- Performance report table with metabolite changes (minor and major) per delay interval
- .HTML formatted performance report
- .csv export of stratified summary table with descriptive statistics (mean, SD, correlation coefficients)

## How to apply

Load the metabolite dataset and pre-analytical metadata (processing delay times, sample type, cohort) into the PRIMA-Panel interface. Parse and validate that metabolite measurements and delay variables are present and properly formatted. Separate the data by pre-centrifugation and post-centrifugation delay phases using the Data tab (visualized as scatter plots, line plots, box plots, or SPREC-sorted lollipop plots). Use the Performance Reports 'Single' tab to set slider ranges for pre- and post-centrifugation time windows, generating a stratified table that highlights minor and major metabolite changes (defined by adjustable % thresholds and color coding) within each delay bin. Filter and subset by sample type (plasma vs. serum) and cohort through the interactive interface. Export the stratified performance table as .HTML report or .csv for downstream validation and reporting.

## Related tools

- **PRIMA-Panel** (Interactive data exploration and performance reporting interface for visualizing and stratifying metabolic parameters by processing delay intervals) — https://github.com/funkam/PRIMA

## Evaluation signals

- Stratified tables correctly separate metabolites by pre-centrifugation and post-centrifugation delay bins with no missing or misaligned samples.
- Minor and major change thresholds (% values) are consistently applied across all metabolites within a given delay window and align with user-specified color coding rules.
- Exported .csv and .HTML reports contain matching summary statistics (mean, SD, correlation) and are parseable by downstream tools.
- Interactive filtering by sample type and cohort returns only the expected subset of rows; unfiltered data matches input row count.
- Visualizations (plots and lollipop diagrams) show monotonic or expected trends in metabolite values across increasing delay durations, with no out-of-range or invalid numeric values.

## Limitations

- The tool is designed for peripheral blood (plasma/serum) samples only; applicability to other sample types (urine, CSF, tissues) is not documented.
- Performance depends on valid SPREC classification of delay time-points; misclassified or non-standard delay intervals may produce uninformative stratification.
- Minor and major change thresholds are user-adjustable but not validated against biological reference ranges; threshold selection requires domain expertise.
- The README does not specify limits on cohort size, number of metabolites, or data table dimensions; performance scaling for large-scale studies is undocumented.

## Evidence

- [readme] Finding: PRIMA-Panel as interactive data exploration tool: "The panel functions as a data expoloration tool. It allows to investigate the these effects interactively"
- [readme] Finding: PRIMA-Panel investigates processing delays on metabolic parameters: "The PRIMA-Panel is a tool to investigate the effect of processing delays on metabolic parameters in samples of peripheral blood (plasma / serum)"
- [readme] Workflow: Data tab stratifies by SPREC and delay phase: "The Data tab shows different ways of highlighting the different stability time-points in minutes. The time-points are sorted according to their SPREC classification. In addition, there is an"
- [readme] Workflow: Performance Reports tab generates stratified tables with adjustable thresholds: "The 'Single' tab allows the user to set a pre-centrifugation time and a post-centrifugation using a Slider. A table is then generated that higlights a minor and a major change for each metabolite in"
- [readme] Output: Exportable performance reports in HTML and CSV formats: "The table can be downloaded as a .HTML report or the table directly as .csv (or other formats)"
