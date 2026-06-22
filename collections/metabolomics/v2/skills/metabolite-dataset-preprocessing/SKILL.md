---
name: metabolite-dataset-preprocessing
description: Use when you have raw NMR metabolomics measurements paired with pre-analytical metadata (e.g., processing delay times, sample type designations [plasma vs. serum], cohort identifiers) and need to investigate how delays affect measured metabolic parameters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - PRIMA-Panel
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

# metabolite-dataset-preprocessing

## Summary

Load, parse, validate, and organize NMR metabolomics datasets together with pre-analytical metadata (processing delays, sample types, cohort information) into a structured, quality-controlled format suitable for interactive exploration and statistical analysis. This skill prepares raw metabolite measurements and delay variables for downstream investigation of pre-analytical effects on metabolic parameter stability.

## When to use

Apply this skill when you have raw NMR metabolomics measurements paired with pre-analytical metadata (e.g., processing delay times, sample type designations [plasma vs. serum], cohort identifiers) and need to investigate how delays affect measured metabolic parameters. The skill is essential before interactive visualization or performance report generation, particularly when input data structure, formatting, or completeness cannot be assumed.

## When NOT to use

- Input data is already a validated, quality-controlled feature table with no missing pre-analytical metadata — skip directly to interactive exploration.
- Processing delay information is unavailable or not recorded in the source data — this skill requires delay variables to function.
- The analysis goal is limited to univariate metabolite statistics and does not require stratification by delay bins or sample type — simpler preprocessing may suffice.

## Inputs

- raw metabolite measurement table (rows: samples; columns: metabolite concentrations)
- pre-analytical metadata table (processing delay times, sample type, cohort, SPREC classification)
- date/time stamps for centrifugation events (optional, used to calculate delay intervals)

## Outputs

- validated, normalized metabolite dataset with integrated pre-analytical metadata
- preprocessed tabular data structure ready for interactive visualization and subsetting
- data quality report documenting validation results and any excluded samples

## How to apply

Load the metabolite dataset and pre-analytical metadata into memory as a unified structure. Parse and validate the input data to verify that metabolite measurements, delay variables (pre- and post-centrifugation times), sample type labels, and cohort identifiers are present and properly formatted. Check for missing values, data type mismatches, and consistency between delay timestamps and recorded SPREC classifications. Organize the validated data into a normalized tabular form (e.g., rows = samples, columns = metabolites + metadata) with delay times split into pre-centrifugation and post-centrifugation bins or continuous values. This preprocessed dataset then becomes the input for interactive filtering, visualization, and performance report generation within the PRIMA-Panel interface.

## Related tools

- **PRIMA-Panel** (interactive data exploration and visualization platform that consumes preprocessed metabolite datasets and enables dynamic filtering/subsetting by delay ranges, sample type, and cohort) — https://github.com/funkam/PRIMA

## Evaluation signals

- All metabolite columns are numeric with no non-convertible values; delay columns (pre- and post-centrifugation times) are present and parseable as numeric or timestamp formats.
- Sample type variable contains only expected categories (plasma, serum) with no orphaned or misspelled entries; cohort identifiers match the metadata schema.
- Row count and column count remain constant or only decrease (due to exclusion of invalid rows); no unexplained data amplification or duplication.
- Delay values fall within biologically plausible ranges (e.g., post-centrifugation delay > 0 minutes, pre-centrifugation delay < 24 hours) as specified by SPREC classification standards.
- Downstream PRIMA-Panel filtering and visualization functions execute without schema errors and correctly stratify data by delay bins, sample type, and cohort.

## Limitations

- Preprocessing assumes metabolite measurements and delay metadata are co-registered by sample ID; misalignment or missing linkage will cause validation failure.
- The skill does not impute missing metabolite or delay values — rows or columns with substantial missingness may need to be excluded prior to preprocessing.
- SPREC classification validation requires external reference data (e.g., standard delay ranges for plasma vs. serum); this skill does not define those standards internally.
- Timestamp-based delay calculation (date+time differences) is only supported via a separate Tools module; direct processing of raw timestamps is not part of the core preprocessing workflow.
- The skill assumes input data are in tabular format (CSV, TSV, or Excel); binary or hierarchical formats (HDF5, netCDF) require conversion before preprocessing.

## Evidence

- [other] workflow_step_1: "Load the metabolite dataset and pre-analytical metadata (processing delay times, sample type, cohort information) into memory."
- [other] workflow_step_2: "Parse and validate the input data structure to ensure metabolite measurements and delay variables are present and properly formatted."
- [intro] preprocessing_purpose: "a tool to investigate the effect of processing delays on metabolic parameters in samples of peripheral blood (plasma / serum)"
- [readme] delay_organization: "The data is split according the two different delays (pre- and post-centrifugation"
- [intro] interactive_readiness: "The panel functions as a data expoloration tool. It allows to investigate the these effects interactively."
