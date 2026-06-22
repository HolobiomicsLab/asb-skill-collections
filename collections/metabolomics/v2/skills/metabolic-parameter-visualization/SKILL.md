---
name: metabolic-parameter-visualization
description: Use when when you have paired NMR metabolite measurements and corresponding processing metadata (pre-centrifugation delay, post-centrifugation delay, sample type, cohort) for a blood sample cohort and need to determine which metabolites remain stable across the expected or observed delay range, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - PRIMA-Panel
  - QC-Tool
  techniques:
  - NMR
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

# metabolic-parameter-visualization

## Summary

Create interactive visualizations of metabolic parameter stability across processing delay timepoints in peripheral blood samples (plasma/serum) to identify which metabolites are sensitive to pre- and post-centrifugation delays. This skill enables rapid, exploratory assessment of pre-analytical effects on NMR-measured metabolites through dynamic filtering and stratified performance reporting.

## When to use

When you have paired NMR metabolite measurements and corresponding processing metadata (pre-centrifugation delay, post-centrifugation delay, sample type, cohort) for a blood sample cohort and need to determine which metabolites remain stable across the expected or observed delay range, or to communicate stability profiles to stakeholders via interactive exploration rather than static tables.

## When NOT to use

- Input lacks pre-analytical metadata (processing delay times, sample type, cohort information) — visualization cannot map metabolite variation to delay sources without these dimensions.
- Metabolite data are already quality-controlled and delay effects have been removed — this skill is designed to detect and visualize delay sensitivity, not to validate already-corrected data.
- Sample cohort size is < 5 per delay bin — stratified visualization and performance statistics become unreliable with sparse groups.

## Inputs

- NMR metabolite measurement matrix (numeric, one row per sample, one column per metabolite)
- Pre-analytical metadata table (sample ID, pre-centrifugation delay in minutes, post-centrifugation delay in minutes, SPREC classification, sample type [plasma/serum], cohort identifier)
- Processing timestamp pairs (date+time of collection, centrifugation, and aliquoting for delay calculation)

## Outputs

- Interactive scatter/line/box/lollipop plot panel stratified by pre- and post-centrifugation delay phase
- Performance report table (.csv or .HTML) with metabolite-level minor and major change flags per delay bin
- Filtered dataset subsets (by sample type, cohort, or delay range) exported as .csv
- Summary statistics table (mean, standard deviation, correlation coefficient per metabolite × delay stratum)

## How to apply

Load the metabolite dataset alongside pre-analytical metadata (processing delay times in minutes, SPREC classification, sample type designation [plasma vs. serum], and cohort labels) into PRIMA-Panel. Parse and validate that metabolite measurements and delay variables are present and properly formatted. Create multi-panel visualizations (scatter plots, line plots, box plots, or lollipop plots) stratified by pre- and post-centrifugation delay phases, with metabolite parameter values on the y-axis and delay duration on the x-axis. Use the 'Single' tab to set slider-controlled delay thresholds and generate performance tables that flag minor and major changes (configurable % thresholds) for each metabolite within the specified timeframe. Dynamically filter by sample type, cohort, or delay range through the interactive interface. Export tables as .csv or .HTML and visualizations for downstream reporting.

## Related tools

- **PRIMA-Panel** (Primary interactive Shiny application for loading metabolite data, rendering delay-stratified visualizations (scatter, line, box, lollipop plots), filtering by sample type/cohort/delay range, and generating configurable performance reports with minor/major change thresholds.) — https://github.com/funkam/PRIMA
- **QC-Tool** (Related quality control repository containing PRIMA-Panel logo and supporting assets; used for visualization branding and supplementary QC workflows.) — https://github.com/funkam/QC-Tool

## Evaluation signals

- Visualizations render without missing data or axis label errors; metabolite measurements and delay values appear on correct axes with appropriate scales.
- Performance report table contains one row per metabolite and flags minor/major changes for each metabolite within the user-specified pre- and post-centrifugation delay range; flagged changes align with configured % thresholds (e.g., if threshold is 10%, flagged metabolites show ≥10% change between min and max delay).
- Filtering by sample type (plasma vs. serum), cohort, or delay range reduces the rendered plot and table to only the selected subset without data loss or duplication.
- Descriptive statistics (mean, SD, correlation coefficient) computed per delay bin or continuous delay value match manual calculation on the filtered dataset (spot-check at least one metabolite × delay stratum).
- Exported .csv table retains all columns (metabolite name, change flag, statistics) and .HTML report renders without formatting errors in a web browser.

## Limitations

- PRIMA-Panel currently separates pre- and post-centrifugation delays into two distinct tabs; combined interaction effects between both delay phases are not directly visualized in a single panel.
- Minor and major change thresholds are user-configurable but must be set manually per analysis session; no built-in statistical significance test (e.g., t-test or mixed model) is applied to determine whether observed changes exceed biological noise.
- Tool requires manual timestamp calculation (date+time differences) via the 'Tools' tab before uploading delay metadata; no automated extraction from raw LIMS or instrument data.
- Performance scaling and responsiveness for cohorts >10,000 samples not explicitly documented; very large datasets may cause UI lag in the interactive interface.
- Visualizations and reports are exploratory; they do not provide formal recommendations for which metabolites should be excluded or delay thresholds that define acceptable pre-analytical windows.

## Evidence

- [intro] Interactive data exploration and processing delay stratification: "The panel functions as a data expoloration tool. It allows to investigate the these effects interactively"
- [intro] Processing delay effect quantification on metabolic parameters in blood samples: "a tool to investigate the effect of processing delays on metabolic parameters in samples of peripheral blood (plasma / serum)"
- [intro] Performance report generation with pre-analytical stratification: "PRIMA-Panel allows the creation of so called performance reports for sample cohorts. Here a data table with pre-analytical information can be uploaded"
- [readme] Dual-phase delay visualization (pre- and post-centrifugation): "The data is split according the two different delays (pre- and post-centrifugation"
- [readme] Configurable change thresholds and export formats: "A table is then generated that higlights a minor and a major change for each metabolite in that given timeframe. The colors, as well as the % threshholds, can be adjusted. The table can be downloaded"
