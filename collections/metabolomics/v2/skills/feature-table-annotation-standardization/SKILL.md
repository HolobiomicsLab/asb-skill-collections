---
name: feature-table-annotation-standardization
description: Use when after Blueshift or Gravity processing has produced a feature abundance table with annotations, but before final reporting or integration with sample/injection metadata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - bmxp
  - Python
  - Formation
  - Gravity
  - Blueshift
  - bmxp (Python package)
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

# feature-table-annotation-standardization

## Summary

Standardize feature annotations, metadata structure, and column naming conventions in processed LCMS metabolomics feature tables to ensure consistent schema compliance across the BMXP pipeline. This step prepares formatted output that meets acceptance criteria before final reporting or downstream analysis.

## When to use

After Blueshift or Gravity processing has produced a feature abundance table with annotations, but before final reporting or integration with sample/injection metadata. Apply this skill when feature metadata column headers, annotation labels, or metadata structure do not conform to the BMXP shared schema (e.g., Compound_ID, RT, MZ, Adduct, Metabolite, Annotation_ID fields), or when feature tables from multiple extraction methods or projects must be harmonized to a common labeling convention.

## When NOT to use

- Input feature table is already in a frozen, non-standardized format required by downstream tools (e.g., vendor-proprietary output that cannot be remapped without data loss).
- Feature data has not yet been processed through Blueshift or Gravity—Formation is designed as a terminal formatting and QC module, not a preliminary step.
- Project uses a locked, custom schema incompatible with BMXP shared schema and no schema remapping is feasible.

## Inputs

- Processed feature abundance table (Feature x Injection, output from Blueshift or Gravity)
- Feature metadata with raw annotations (Compound_ID, RT, MZ, Intensity, Method, Annotation_ID, Adduct, Metabolite, Non_Quant)
- Injection metadata (injection_id, broad_id, injection_type, batches)
- Sample metadata (broad_id, program_id, and arbitrary biospecimen columns)

## Outputs

- Formatted feature abundance table with standardized column headers conforming to bmxp.FMDATA and bmxp.IMDATA schema
- QC report documenting pass/fail status for feature integrity, missing-value thresholds, and metadata completeness checks
- Validated output file ready for downstream analysis or reporting

## How to apply

Load the processed feature table (output from Blueshift or Gravity) and the associated feature metadata, injection metadata, and sample metadata in their native formats. Apply Formation-specific formatting rules to map and standardize all feature annotation columns (Compound_ID, Annotation_ID, Adduct, Metabolite, Non_Quant status) and metadata headers to the BMXP shared schema (bmxp.FMDATA, bmxp.IMDATA, bmxp.SMDATA). If using non-standard column names, update the schema dictionary globally in bmxp before running Formation to ensure all downstream modules recognize the terminology. Execute quality control checks on feature integrity (missing values, data type consistency), missing-value thresholds for each feature, and metadata completeness (e.g., all features have RT, MZ, and an Annotation_ID). Generate a formatted output file conforming to the shared schema and a QC report documenting pass/fail status for each check. Validate that output meets Formation acceptance criteria—all required columns present, no nulls in index fields, adduct strings valid, metabolite names populated or explicitly marked as unannotated—before finalizing.

## Related tools

- **Formation** (Standalone BMXP module that executes formatting rules and QC checks on processed feature tables to ensure schema compliance and metadata completeness) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/formation/readme.md
- **Gravity** (Upstream module that clusters redundant LCMS features; output is input to Formation) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md
- **Blueshift** (Upstream module that performs drift correction; output is input to Formation) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/blueshift/readme.md
- **bmxp (Python package)** (Core library providing shared schema dictionaries (bmxp.FMDATA, bmxp.IMDATA, bmxp.SMDATA) and common utilities for all modules including Formation) — https://github.com/broadinstitute/bmxp

## Examples

```
import bmxp
from bmxp.formation import Formation
bmxp.FMDATA['Compound_ID'] = 'Feature_ID'
formatter = Formation(feature_metadata, feature_abundances, injection_metadata, sample_metadata)
formatted_output, qc_report = formatter.execute()
formatter.validate_against_acceptance_criteria(formatted_output)
```

## Evaluation signals

- All feature metadata columns match the BMXP shared schema (Compound_ID, RT, MZ, Intensity, Method, Annotation_ID, Adduct, Metabolite, Non_Quant, Cluster_Num if from Gravity, Batches Skipped if from Blueshift).
- All injection metadata columns present and correctly mapped (injection_id, broad_id, program_id, injection_type, comments, column_number, injection_order, batches, QCRole if from Blueshift).
- No null values in index fields (Compound_ID for features, injection_id for injections, broad_id for samples).
- QC report shows all features pass missing-value thresholds and feature integrity checks; metadata completeness ≥ threshold specified in Formation parameters.
- Formatted output file can be successfully read by downstream BMXP modules (Eclipse, Gravity, Blueshift) without schema-mapping errors when using the same global schema dictionary.

## Limitations

- Formation assumes input data has already been processed through upstream modules (Blueshift, Gravity); raw or incompletely processed feature tables may fail QC checks.
- Custom annotation vocabularies or non-standard adduct formats not recognized by Formation rules may be flagged as validation failures and require manual curation.
- Missing-value thresholds and QC acceptance criteria are configurable but must be pre-specified; Formation does not auto-detect appropriate thresholds for novel data types or extraction methods.
- Schema remapping via global dictionary changes is project-wide; per-module or per-file exceptions are not supported in the current implementation.

## Evidence

- [other] Formation is a standalone module in the BMXP pipeline that performs formatting and final quality control on processed LCMS feature data.: "Formation is a standalone module in the BMXP pipeline that performs formatting and final quality control on processed LCMS feature data."
- [other] Apply Formation-specific formatting rules to standardize feature annotations, metadata structure, and column naming conventions.: "Apply Formation-specific formatting rules to standardize feature annotations, metadata structure, and column naming conventions."
- [other] Execute quality control checks on feature integrity, missing-value thresholds, and metadata completeness.: "Execute quality control checks on feature integrity, missing-value thresholds, and metadata completeness."
- [readme] Each tool is meant to be a standalone module that performs a step in our processing pipeline.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline."
- [readme] All BMXP modules use a shared schema and file formats with our prefered columns headers. These files are (along with their labels): Feature Metadata `bmxp.FMDATA` - Describes the feature. Index default is `Compound_ID`; Injection Metadata `bmxp.IMDATA` - Describes the Injection. Index default is `injection_id`; Sample Metadata `bmxp.SMDATA` - Describes the biospecimen from which the Injection is derived. Index default is `broad_id`.: "All BMXP modules use a shared schema and file formats with our prefered columns headers. These files are (along with their labels): Feature Metadata `bmxp.FMDATA` - Describes the feature. Index"
- [readme] To update the schema, modify the dictionary objects in the module directly prior to running code.: "To update the schema, modify the dictionary objects in the module directly prior to running code."
- [readme] Feature Metadata describes the LCMS feature. This is a mixture of fundamental nontargeted feature information, annotation info, and anything else.: "Feature Metadata describes the LCMS feature. This is a mixture of fundamental nontargeted feature information, annotation info, and anything else."
