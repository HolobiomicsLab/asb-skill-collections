---
name: quality-control-threshold-validation
description: Use when after executing Formation formatting on processed feature tables (output from Blueshift or Gravity modules).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - bmxp
  - Python
  - Formation
  - Blueshift
  - Gravity
derived_from:
- doi: 10.1093/bioinformatics/btaf290/8128335
  title: Eclipse
evidence_spans:
- pip install bmxp
- They are written in Python and C
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eclipse_cq
    doi: 10.1093/bioinformatics/btaf290/8128335
    title: Eclipse
  dedup_kept_from: coll_eclipse_cq
schema_version: 0.2.0
---

# quality-control-threshold-validation

## Summary

Quality-control-threshold-validation is the final step in the BMXP metabolomics processing pipeline that validates formatted LCMS feature data against acceptance criteria, checking feature integrity, missing-value thresholds, and metadata completeness before finalizing the dataset. This skill ensures processed metabolomics output meets required data quality standards before downstream analysis or reporting.

## When to use

Apply this skill after executing Formation formatting on processed feature tables (output from Blueshift or Gravity modules). Use it when you have standardized feature annotations, metadata structure, and column naming conventions in place, and you need to certify that the dataset is complete, internally consistent, and ready for publication or downstream analysis. Trigger: you have a formatted feature table with Feature Metadata (bmxp.FMDATA), Injection Metadata (bmxp.IMDATA), and Feature Abundances, and require a QC report documenting pass/fail status for each validation rule.

## When NOT to use

- Input feature table has not yet been processed by Blueshift or Gravity (no intermediate processing output exists).
- Feature data is already in a downstream analysis format (e.g., normalized abundances, fold changes, or statistical test outputs); Formation expects raw/processed feature counts.
- Metadata schema differs materially from BMXP standard (custom Compound_ID, injection_id, or abundance table structure not reconcilable with the shared schema).

## Inputs

- Processed feature table (output from Blueshift or Gravity) in BMXP schema format
- Feature Metadata (bmxp.FMDATA) with Compound_ID index
- Injection Metadata (bmxp.IMDATA) with injection_id index
- Feature Abundances (Compound_ID × injection_id pivot table)
- Formation-specific formatting rules and threshold specifications

## Outputs

- Formatted feature table (standardized annotations, metadata structure, column naming)
- QC report documenting pass/fail status for each validation check
- List of flagged rows/columns and validation violations
- Finalized dataset approved for downstream analysis

## How to apply

Load the processed feature table in BMXP schema format (Feature Metadata indexed by Compound_ID, Injection Metadata indexed by injection_id, and a Feature × Injection abundance pivot table). Execute Formation-specific quality control checks in sequence: (1) validate feature integrity by confirming all Compound_IDs are unique and non-null; (2) assess missing-value thresholds across the feature abundance matrix, rejecting features or injections exceeding predefined sparsity limits; (3) verify metadata completeness by confirming required column headers and non-null values in critical fields (RT, MZ, Intensity, Method, injection_type, broad_id). (4) Cross-validate that injection_ids in the abundance table match those in Injection Metadata, and that Compound_IDs match Feature Metadata. (5) Generate a QC report documenting pass/fail status for each check and the rows/columns that failed. (6) Validate that the formatted output meets Formation acceptance criteria (e.g., no failed critical checks) before finalizing. The rationale is to catch schema violations, data loss, and incompleteness early, preventing downstream pipeline failures or corrupted analysis.

## Related tools

- **bmxp** (Core Python package providing Formation module and shared schema (FMDATA, IMDATA, SMDATA) for QC validation) — https://github.com/broadinstitute/bmxp
- **Formation** (BMXP module that performs formatting and final QC checks on feature tables) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/formation/readme.md
- **Blueshift** (Upstream BMXP module (drift correction) that produces processed feature table input to Formation) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/blueshift/readme.md
- **Gravity** (Upstream BMXP module (feature clustering) that produces processed feature table input to Formation) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md

## Evaluation signals

- All features in the abundance matrix are indexed by valid, unique Compound_IDs that exist in Feature Metadata.
- All injections in the abundance matrix are indexed by valid, unique injection_ids that exist in Injection Metadata with correct injection_type and broad_id assignments.
- Missing-value frequency per feature and per injection does not exceed Formation's configured thresholds (checked against predefined sparsity limits).
- All required Feature Metadata columns (RT, MZ, Intensity, Method, Annotation_ID, Adduct, Metabolite) contain non-null values and pass type/format validation.
- QC report shows zero critical failures (pass status for feature integrity, missing-value threshold, and metadata completeness checks) before output is finalized.

## Limitations

- Formation operates only on data that has already passed upstream processing (Blueshift or Gravity); it cannot recover from data loss or corruption introduced in earlier pipeline stages.
- QC thresholds (missing-value limits, metadata requirements) are fixed at Formation configuration time; ad-hoc threshold adjustments require reconfiguration and rerun.
- Formation validates schema conformance and structural completeness but does not assess biological plausibility, annotation accuracy, or cross-sample consistency (those are pre-pipeline responsibilities).
- The shared BMXP schema assumes standard column labels and index names; custom metabolomics data formats or non-standard injection type vocabularies must be mapped to the schema manually before Formation can validate them.

## Evidence

- [other] Formation is a standalone module in the BMXP pipeline that performs formatting and final quality control on processed LCMS feature data.: "Formation is a standalone module in the BMXP pipeline that performs formatting and final quality control on processed LCMS feature data."
- [other] Apply Formation-specific formatting rules to standardize feature annotations, metadata structure, and column naming conventions; execute quality control checks on feature integrity, missing-value thresholds, and metadata completeness; generate a formatted output file and a QC report documenting pass/fail status for each check.: "Apply Formation-specific formatting rules to standardize feature annotations, metadata structure, and column naming conventions. 3. Execute quality control checks on feature integrity, missing-value"
- [readme] All BMXP modules use a shared schema and file formats with preferred column headers including Feature Metadata (bmxp.FMDATA indexed by Compound_ID), Injection Metadata (bmxp.IMDATA indexed by injection_id), Sample Metadata, and Feature Abundances (pivot table of Feature x Injection).: "All BMXP modules use a shared schema and file formats with our prefered columns headers. These files are (along with their labels): * Feature Metadata `bmxp.FMDATA` - Describes the feature. Index"
- [intro] Formation - Formatting and Final QC is one of the key tools in the BMXP collection designed to be a standalone module that performs a step in the processing pipeline.: "Formation - Formatting and Final QC"
- [readme] Each tool is meant to be a standalone module that performs a step in the processing pipeline and is designed to be performant and cloud-compatible.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline. They are written in Python and C, and designed to be perfomant and cloud-compatible."
