---
name: plasma-serum-sample-comparison
description: Use when you have NMR-based metabolomics measurements from a cohort containing
  both plasma and serum samples with associated processing delay metadata (pre- and
  post-centrifugation times), and you need to determine whether metabolic parameter
  stability differs between the two sample types or to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# plasma-serum-sample-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A method for interactively stratifying NMR metabolomics data by sample type (plasma versus serum) to isolate and compare processing delay effects on metabolic parameters within each matrix. This skill enables matrix-specific stability assessments critical for pre-analytical quality control in peripheral blood metabolomics studies.

## When to use

You have NMR-based metabolomics measurements from a cohort containing both plasma and serum samples with associated processing delay metadata (pre- and post-centrifugation times), and you need to determine whether metabolic parameter stability differs between the two sample types or to generate matrix-specific performance reports for assay validation.

## When NOT to use

- Input dataset contains only a single sample type (plasma only or serum only)—comparison requires both matrices present
- Processing delay metadata or sample type labels are missing or unreliably recorded; filtering and stratification cannot be performed without these variables
- The research question concerns cross-matrix harmonization or batch correction rather than matrix-specific stability assessment

## Inputs

- NMR metabolite measurement table (quantified metabolic parameters across sample cohort)
- Pre-analytical metadata table with columns: sample_type (plasma or serum), pre_centrifugation_delay_minutes, post_centrifugation_delay_minutes, cohort_identifier
- Cohort sample annotations (optional: batch, collection site, storage conditions)

## Outputs

- Matrix-stratified interactive visualizations (scatter, line, and lollipop plots showing metabolite values vs. delay times, grouped by plasma/serum)
- Performance report tables (.csv or .HTML format) with descriptive statistics (mean, SD, correlation) per metabolite, stratified by sample type and delay bins
- Minor and major change annotations per metabolite within each sample type matrix (color-coded by adjustable % threshold)

## How to apply

Load the metabolite dataset alongside pre-analytical metadata (processing delay times, sample type designation, cohort information) into the PRIMA-Panel. Parse and validate that sample type is correctly labeled (plasma vs. serum) and that delay variables (pre-centrifugation and post-centrifugation times in minutes) are present. Use the interactive filtering interface to subset the data by sample type, then generate separate visualizations (scatter plots, line plots, box plots) and performance report tables for each matrix showing the relationship between processing delay duration and individual metabolic parameters. Stratify the descriptive statistics (mean, standard deviation, correlation coefficients) by sample type and delay bins. This separation allows you to assess whether metabolic stability or degree of change differs between matrices—a critical pre-analytical consideration—and to highlight minor and major metabolic changes within each sample type using adjustable color-coding and percentage thresholds. Export matrix-specific tables as .csv or .HTML performance reports for downstream interpretation.

## Related tools

- **PRIMA-Panel** (Interactive data exploration and performance report generation platform for stratifying metabolomics measurements by sample type and processing delay; provides tabular summary, filtering, visualization, and export functionality) — https://github.com/funkam/PRIMA

## Evaluation signals

- Verify that filtering by sample type correctly partitions all records into plasma-only and serum-only subsets with no cross-contamination or missing assignments
- Check that performance report tables contain separate rows or sections for plasma and serum, each with distinct descriptive statistics and delay bin stratifications
- Confirm that visualizations display plasma and serum traces or annotations as visually distinct (e.g., separate facets, colors, or overlaid traces with legend) so matrix-specific trends are discernible
- Validate that exported .csv or .HTML reports include sample type as an explicit column or report section header, allowing downstream filtering by matrix
- Inspect that correlation coefficients and mean/SD values for the same metabolite differ between plasma and serum subsets when genuine pre-analytical differences exist, indicating sensitive stratification

## Limitations

- PRIMA-Panel requires properly formatted and labeled sample type metadata; mislabeled or ambiguous sample type entries will produce unreliable stratification
- The tool does not perform statistical hypothesis tests (e.g., t-tests or ANOVA) to formally compare plasma vs. serum stability; it provides descriptive summaries and visual comparison, leaving formal significance testing to downstream analysis
- Minor and major change thresholds are user-adjustable but subjective; no universal metabolite-specific cutoffs are embedded, so interpretation requires domain expertise and prior knowledge of acceptable metabolic drift by matrix

## Evidence

- [readme] Sample type filtering capability: "Enable dynamic filtering and subsetting of the dataset by sample type (plasma vs. serum), cohort, or delay range through the interactive interface"
- [readme] Matrix-specific performance report generation: "The PRIMA-Panel allows the creation of so called performance reports for sample cohorts. Here a data table with pre-analytical information can be uploaded"
- [readme] Pre- and post-centrifugation delay stratification: "The data is split according the two different delays (pre- and post-centrifugation"
- [readme] Plasma and serum as distinct analytical matrices: "The PRIMA-Panel is a tool to investigate the effect of processing delays on metabolic parameters in samples of peripheral blood (plasma / serum)"
- [readme] Interactive data exploration across sample types: "The panel functions as a data expoloration tool. It allows to investigate the these effects interactively"
