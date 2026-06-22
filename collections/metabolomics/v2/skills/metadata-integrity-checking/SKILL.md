---
name: metadata-integrity-checking
description: Use when after processing LCMS feature data through Blueshift or Gravity but before finalizing results.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - bmxp
  - Python
  - Formation
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf290/8128335
  all_source_dois:
  - 10.1093/bioinformatics/btaf290/8128335
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metadata-integrity-checking

## Summary

Validate that metabolomics feature, injection, and sample metadata conform to BMXP schema requirements and completeness thresholds before downstream analysis. This skill ensures data integrity and reproducibility across the metabolomics processing pipeline.

## When to use

After processing LCMS feature data through Blueshift or Gravity but before finalizing results. Apply this skill when you have formatted feature tables with associated injection and sample metadata and need to verify that all required columns are present, index fields are correct, metadata completeness meets threshold, and field values conform to expected types and allowed categories (e.g., injection_type ∈ {'sample', 'prefa', 'prefb', 'blank', 'other-', 'not_used-'}).

## When NOT to use

- Input is raw LCMS instrument output (.raw or .mzML files) — use Chroma first to read and convert to feature tables.
- Data has not yet been processed through feature clustering (Gravity) or drift correction (Blueshift) — apply those modules before integrity checking.
- Metadata is unstructured or does not conform to BMXP schema — standardize column names and index fields first via Formation formatting rules.

## Inputs

- Feature metadata table (bmxp.FMDATA) with Compound_ID index
- Feature abundances pivot table (Compound_ID × injection_id)
- Injection metadata table (bmxp.IMDATA) with injection_id index
- Sample metadata table (bmxp.SMDATA) with broad_id index

## Outputs

- Formatted feature metadata table (validated schema compliance)
- QC report documenting pass/fail status for each metadata check
- Acceptance/rejection determination for downstream pipeline entry

## How to apply

Load the feature metadata (bmxp.FMDATA), injection metadata (bmxp.IMDATA), and sample metadata (bmxp.SMDATA) tables alongside the feature abundance pivot table. Verify that index fields match schema defaults (Compound_ID, injection_id, broad_id respectively) or have been consistently remapped via bmxp schema configuration. Check that all mandatory columns are present and non-null at configured thresholds (e.g., RT, MZ, Intensity in feature metadata; injection_type, broad_id in injection metadata). Validate field type consistency and allowed-value constraints (e.g., injection_type must match allowed strings). Execute Formation QC checks which document pass/fail status for feature integrity, missing-value thresholds, and metadata completeness, then generate a QC report that gates acceptance before finalization.

## Related tools

- **Formation** (Performs metadata formatting and QC checks; generates formatted output and QC report) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/formation/readme.md
- **bmxp** (Core package providing shared schema definitions (FMDATA, IMDATA, SMDATA) and schema remapping utilities) — https://github.com/broadinstitute/bmxp

## Examples

```
import bmxp
from bmxp.formation import QualityControl
qc = QualityControl(feature_metadata=fmdata, abundances=feature_table, injection_metadata=imdata, sample_metadata=smdata)
report = qc.validate()
if report['pass']:
    formatted_output = qc.format_output()
```

## Evaluation signals

- All required columns from BMXP schema are present in each metadata table (Feature_Specific, Annotation, Injection_Specific, Sample_Specific); index fields match configured schema.
- Feature metadata index (Compound_ID) matches all column headers in feature abundance pivot table; injection metadata index (injection_id) matches all column names in pivot table.
- Injection_type values are exactly one of: 'sample', 'prefa', 'prefb', 'blank', 'other-', 'not_used-'; no unexpected categories or nulls.
- Missing-value counts for critical fields (RT, MZ, Intensity, broad_id, injection_type) are below configured thresholds; QC report shows 'pass' for completeness checks.
- All numeric fields (RT, MZ, Intensity) have valid numeric types; categorical fields match allowed vocabularies; metadata dimensions are mutually consistent (injection_id count matches feature table columns; broad_id count matches sample metadata rows).

## Limitations

- Schema remapping must be applied globally to the bmxp module before running Formation; inconsistent schema configuration across modules will cause silent misalignment.
- Formation performs QC checks but does not automatically repair metadata; failed checks require manual intervention or re-processing upstream.
- The shared schema assumes a specific dimensional structure (Feature × Injection abundance pivot, with separate Injection and Sample metadata); datasets with missing or orthogonal metadata dimensions cannot be validated.
- No cross-validation against external reference databases or metabolite standards is performed by Formation; annotation correctness depends on upstream tools (e.g., Eclipse alignment, Gravity clustering).

## Evidence

- [other] Formation is a standalone module in the BMXP pipeline that performs formatting and final quality control on processed LCMS feature data.: "Formation is a standalone module in the BMXP pipeline that performs formatting and final quality control on processed LCMS feature data."
- [other] Apply Formation-specific formatting rules to standardize feature annotations, metadata structure, and column naming conventions; execute quality control checks on feature integrity, missing-value thresholds, and metadata completeness.: "Apply Formation-specific formatting rules to standardize feature annotations, metadata structure, and column naming conventions. 3. Execute quality control checks on feature integrity, missing-value"
- [readme] All BMXP modules use a shared schema and file formats with preferred column headers for Feature Metadata, Injection Metadata, Sample Metadata, and Feature Abundances.: "All BMXP modules use a shared schema and file formats with our prefered columns headers."
- [readme] Schema can be customized globally so that all packages use the same terminology by modifying dictionary objects in the module directly prior to running code.: "These can be changed globally so that all packages will use the same terminology. To update the schema, modify the dictionary objects in the module directly prior to running code."
- [readme] Injection_type field includes allowed values: sample, prefa, prefb, blank, other-, not_used-.: "injection_type - Type of injection ("sample", "prefa", "prefb", "blank", "other-", "not_used-")"
