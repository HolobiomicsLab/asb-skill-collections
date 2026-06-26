---
name: cloud-compatible-file-output
description: Use when after feature clustering and drift correction (Gravity and Blueshift
  outputs) are complete and you need to produce a final, validated feature table ready
  for storage, archival, or downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - bmxp
  - Python
  - Formation
  - Blueshift
  - Gravity
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cloud-compatible-file-output

## Summary

Format and finalize metabolomics feature tables using the Formation module to generate cloud-compatible output files that meet standardized schema and quality-control criteria. This ensures downstream interoperability and reproducibility across the BMXP pipeline.

## When to use

Apply this skill after feature clustering and drift correction (Gravity and Blueshift outputs) are complete and you need to produce a final, validated feature table ready for storage, archival, or downstream analysis. Trigger when you have a processed feature table that must conform to BMXP's shared schema (Feature Metadata, Injection Metadata, Sample Metadata, and Feature Abundances pivot tables) and pass QC checks before release.

## When NOT to use

- Input is raw LCMS data (.raw or .mzml files) — use Chroma first to read and convert to feature format.
- Feature table has not yet undergone drift correction and redundancy clustering — use Blueshift and Gravity before Formation.
- You need to align multiple datasets from different LCMS methods — use Eclipse before clustering and formation.

## Inputs

- Processed feature table from Blueshift or Gravity (pivot table of Feature x Injection abundances)
- Feature Metadata table (bmxp.FMDATA) with Compound_ID, RT, MZ, Intensity, Method, Annotation_ID, Adduct, Metabolite columns
- Injection Metadata table (bmxp.IMDATA) with injection_id, broad_id, program_id, injection_type, QCRole columns
- Sample Metadata table (bmxp.SMDATA) with broad_id and arbitrary metadata columns

## Outputs

- Formatted feature table adhering to BMXP shared schema with standardized column headers and naming conventions
- QC report documenting pass/fail status for feature integrity, missing-value thresholds, and metadata completeness checks
- Cloud-compatible output file(s) suitable for archival, storage, and downstream analysis

## How to apply

Load the processed feature table (output from Blueshift or Gravity) into Formation in the appropriate LCMS data format. Apply Formation-specific formatting rules to standardize feature annotations, metadata structure, and column naming conventions according to the BMXP shared schema (e.g., Compound_ID, RT, MZ, injection_id, broad_id). Execute quality-control checks on feature integrity, missing-value thresholds, and metadata completeness. Generate a formatted output file and a QC report documenting pass/fail status for each check. Validate that the output meets Formation acceptance criteria before finalizing and deploying to cloud storage.

## Related tools

- **bmxp** (Python package providing the Formation module and shared schema for metabolomics pipeline standardization) — https://github.com/broadinstitute/bmxp
- **Formation** (Standalone BMXP module that performs formatting, standardization, and final QC on processed LCMS feature data) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/formation/readme.md
- **Blueshift** (Upstream module providing drift-corrected feature table as input to Formation) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/blueshift/readme.md
- **Gravity** (Upstream module providing clustered redundant features as input to Formation) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md
- **Python** (Programming language used to implement Formation and all BMXP modules)

## Evaluation signals

- All feature metadata columns (Compound_ID, RT, MZ, Intensity, Method, Annotation_ID, Adduct, Metabolite, Non_Quant) are present and populated according to BMXP.FMDATA schema.
- All injection metadata columns (injection_id, broad_id, program_id, injection_type, QCRole) are present and populated according to BMXP.IMDATA schema.
- Feature x Injection abundance pivot table uses Compound_ID as row index and injection_id as column index with no missing values above the specified threshold.
- QC report shows pass status for feature integrity checks, missing-value thresholds, and metadata completeness for all records.
- Output file conforms to cloud-compatible format (e.g., parquet, HDF5, or CSV) and is free of encoding errors, special characters in column headers, or schema violations.

## Limitations

- Formation is a standalone module and requires upstream preprocessing by Blueshift and Gravity; it cannot recover from errors introduced in earlier pipeline stages.
- The shared schema and column naming conventions are global and must be configured consistently across all BMXP modules before running Formation; schema mismatches will cause validation failures.
- Formation does not perform feature annotation or metabolite identification — only formatting and validation of metadata supplied by upstream modules or external sources.

## Evidence

- [other] Formation is a standalone module in the BMXP pipeline that performs formatting and final quality control on processed LCMS feature data.: "Formation is a standalone module in the BMXP pipeline that performs formatting and final quality control on processed LCMS feature data."
- [other] Apply Formation-specific formatting rules to standardize feature annotations, metadata structure, and column naming conventions.: "Apply Formation-specific formatting rules to standardize feature annotations, metadata structure, and column naming conventions."
- [other] Execute quality control checks on feature integrity, missing-value thresholds, and metadata completeness.: "Execute quality control checks on feature integrity, missing-value thresholds, and metadata completeness."
- [readme] Each tool is meant to be a standalone module that performs a step in our processing pipeline. They are written in Python and C, and designed to be perfomant and cloud-compatible.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline. They are written in Python and C, and designed to be perfomant and cloud-compatible."
- [readme] All BMXP modules use a shared schema and file formats with our prefered columns headers.: "All BMXP modules use a shared schema and file formats with our prefered columns headers."
- [other] Load the processed feature table (output from Blueshift or Gravity) in the appropriate metabolomics data format.: "Load the processed feature table (output from Blueshift or Gravity) in the appropriate metabolomics data format."
