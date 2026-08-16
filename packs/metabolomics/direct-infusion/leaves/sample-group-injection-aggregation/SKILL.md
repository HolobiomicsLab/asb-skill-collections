---
name: sample-group-injection-aggregation
description: Use when when you have picked and annotated MS1 features from replicate injections of the same sample and need to produce a unified feature matrix indexed by sample (not injection).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - SmartPeak
  - SmartPeakGUI
  - SmartPeakCLI
  - OpenMS
  - pyOpenMS
  - BFAIR
  techniques:
  - direct-infusion-MS
derived_from:
- doi: 10.1021/acs.analchem.0c03421
  title: SmartPeak
evidence_spans:
- SmartPeak automates targeted and quantitative metabolomics data processing
- SmartPeak GUI provides functionality to facilitate users to get up and running as quickly as possible
- SmartPeak CLI provides an equivalent of SmartPeak GUI application, however with a possibility to run in headless mode
- SmartPeak CLI provides an equivalent of SmartPeak GUI application
- The software is based on the OpenMS toolkit
- The software is based on the OpenMS toolkit.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smartpeak_cq
    doi: 10.1021/acs.analchem.0c03421
    title: SmartPeak
  dedup_kept_from: coll_smartpeak_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03421
  all_source_dois:
  - 10.1021/acs.analchem.0c03421
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-group-injection-aggregation

## Summary

Consolidate multiple injections of the same sample and merge features across sample groups defined in the sequence file to enable group-level statistical analysis and comparative metabolomics. This skill is essential in high-throughput untargeted metabolomics workflows where replicate injections must be unified before group-wise comparisons.

## When to use

When you have picked and annotated MS1 features from replicate injections of the same sample and need to produce a unified feature matrix indexed by sample (not injection). Use this skill after background filtering, adduct merging, and feature annotation are complete—particularly in FIA-MS FullScan Unknowns or semi-targeted workflows where the sequence file defines sample groupings and you plan to perform downstream group comparisons or statistical tests.

## When NOT to use

- Input is already a sample-level feature table (no injection replicates to merge).
- You need to preserve injection-level variance for QC trend analysis or time-series monitoring across a sample batch.
- Sample groupings in the sequence file are malformed, missing, or do not reflect the biological design (validate sequence metadata first).

## Inputs

- picked and annotated MS1 feature list (mzTab or feature table format with intensity values per injection)
- sequence file (.csv) with sample identifiers, group assignments, and injection replicates
- feature annotation results (e.g., from SEARCH_ACCURATE_MASS and MERGE_FEATURES)

## Outputs

- sample-level feature matrix (rows = samples, columns = m/z × RT features, values = aggregated intensities)
- group-annotated feature table with sample-group metadata preserved
- feature list with sample-level quality metrics (e.g., coefficient of variation across replicates)

## How to apply

After filtering features by blank signal intensity and merging adducts of the same compound, apply MERGE_INJECTIONS to consolidate all injections belonging to the same sample into a single row, typically by summing or averaging feature intensities across replicates. Then apply STORE_FEATURES_SAMPLE_GROUP to merge features across the sample groups (e.g., case vs. control cohorts) specified in the sequence file metadata. The rationale is to reduce the injection dimension while preserving sample-level biological variability; grouping enforces consistent handling of the sample structure defined in the input sequence configuration, ensuring that downstream statistical tests operate on the intended sample-group contrasts rather than on individual injections.

## Related tools

- **SmartPeak** (orchestrates the full workflow including MERGE_INJECTIONS and STORE_FEATURES_SAMPLE_GROUP steps) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakGUI** (provides interactive configuration and monitoring of injection/sample merging and group storage operations) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (enables command-line execution of injection and group merging workflows without GUI) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (provides underlying feature merging and intensity aggregation algorithms)
- **BFAIR** (post-processing and statistical analysis of aggregated sample-group features) — https://github.com/AutoFlowResearch/BFAIR

## Evaluation signals

- Verify that the number of rows in the output feature table equals the number of unique samples (not injections) in the sequence file.
- Check that sample-level feature intensities are non-negative and within expected range (e.g., no NaN or negative values after aggregation).
- Confirm that group assignments are correctly propagated: all samples in a group should share the same group label in the output metadata.
- Compute coefficient of variation (CV) for aggregated intensities across replicate injections; high CV (>50%) may indicate injection-level variability worth investigating.
- Validate that the number of features per sample is consistent after merging (no unexpected loss or gain of features due to missing values or aggregation errors).

## Limitations

- Injection merging assumes all replicates of a sample use the same or compatible MS parameters; mismatched acquisition settings may produce misleading aggregate intensities.
- If the sequence file lacks explicit group labels or sample metadata, STORE_FEATURES_SAMPLE_GROUP may fail or create uninformative groupings; preprocessing and validation of the sequence file is mandatory.
- Aggregation (e.g., sum or mean) of intensities across injections can mask outlier injections or instrumental drift; no robust outlier detection is described in the workflow.
- The workflow does not explicitly handle unbalanced designs (e.g., differing numbers of replicates per sample or missing injections); such cases may require manual sequence file curation or post-hoc filtering.

## Evidence

- [methods] Merge injections belonging to the same sample using MERGE_INJECTIONS: "Merge injections belonging to the same sample using MERGE_INJECTIONS."
- [methods] Merge features across sample groups specified in the sequence file using STORE_FEATURES_SAMPLE_GROUP: "Merge features across sample groups specified in the sequence file using STORE_FEATURES_SAMPLE_GROUP."
- [intro] SmartPeak automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting: "The workflow automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting."
- [readme] The collection of examples is located at src/example/data directory of the SmartPeak source code. The directory contains examples of different kinds of data in .mzML format and their corresponding configuration files.: "The collection of examples is located at ``src/example/data`` directory of the SmartPeak source code."
