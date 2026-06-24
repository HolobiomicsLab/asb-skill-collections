---
name: metabolomics-data-formatting
description: Use when after running feature clustering (Gravity) or drift correction
  (Blueshift) on LCMS data, when you have a processed feature table and need to standardize
  its structure, validate metadata completeness, enforce missing-value thresholds,
  and generate a QC report documenting pass/fail status.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - bmxp
  - Python
  - Gravity
  - Blueshift
  - Formation
  - Python (pandas, NumPy, SciPy)
  - MetENP
  - pandas / NumPy
  - KEGGREST / KEGGgraph
  - dplyr / tidyr
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btaf290/8128335
  title: Eclipse
- doi: 10.1101/2020.11.20.391912
  title: ''
evidence_spans:
- pip install bmxp
- They are written in Python and C
- MetENP
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eclipse_cq
    doi: 10.1093/bioinformatics/btaf290/8128335
    title: Eclipse
  - build: coll_metenp_cq
    doi: 10.1101/2020.11.20.391912
    title: MetENP
  dedup_kept_from: coll_eclipse_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf290/8128335
  all_source_dois:
  - 10.1093/bioinformatics/btaf290/8128335
  - 10.1101/2020.11.20.391912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-formatting

## Summary

Format and quality-control processed LCMS metabolomics feature tables to conform to a shared schema with standardized column headers, metadata structure, and integrity checks. Formation is a standalone BMXP module that executes this final pipeline step before data release or downstream analysis.

## When to use

After running feature clustering (Gravity) or drift correction (Blueshift) on LCMS data, when you have a processed feature table and need to standardize its structure, validate metadata completeness, enforce missing-value thresholds, and generate a QC report documenting pass/fail status before sharing or analyzing the data.

## When NOT to use

- Input is raw .raw or .mzML files — use Chroma to read instrument files first
- Data has not yet been aligned across datasets — run Eclipse before Formation
- Feature redundancy has not been resolved — run Gravity to cluster correlated features before formatting

## Inputs

- Processed feature table from Gravity or Blueshift (feature metadata + feature abundances)
- Injection metadata table with injection_id index
- Sample metadata table with broad_id index

## Outputs

- Formatted feature metadata table (bmxp.FMDATA schema)
- Formatted feature abundances pivot table (Compound_ID × injection_id)
- Formatted injection metadata table (bmxp.IMDATA schema)
- Formatted sample metadata table (bmxp.SMDATA schema)
- Formation QC report with pass/fail status for each check

## How to apply

Load the processed feature table (output from Blueshift or Gravity) in the appropriate metabolomics data format. Apply Formation-specific formatting rules to standardize feature annotations, metadata structure, and column naming conventions to match the shared BMXP schema (Compound_ID, RT, MZ, Intensity, Method, and annotation fields for features; injection_id, broad_id, injection_type, batches for injections; broad_id and arbitrary metadata columns for samples). Execute Formation's quality control checks on feature integrity (e.g., RT and MZ validity), missing-value thresholds across the feature abundance pivot table, and metadata completeness (all required columns present and non-null). Generate both a formatted output file and a detailed QC report documenting pass/fail status for each check. Validate that the output meets Formation acceptance criteria (schema compliance, QC pass flags) before finalizing for downstream use.

## Related tools

- **bmxp** (Python package containing Formation module and shared schema definitions) — https://github.com/broadinstitute/bmxp
- **Gravity** (Upstream module that clusters redundant LCMS features; output is input to Formation) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md
- **Blueshift** (Upstream module that performs drift correction; output is input to Formation) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/blueshift/readme.md
- **Formation** (Standalone BMXP module that applies formatting rules and QC checks) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/formation/readme.md

## Evaluation signals

- All feature metadata columns match bmxp.FMDATA schema (Compound_ID, RT, MZ, Intensity, Method, Annotation_ID, Adduct, Metabolite, etc.)
- All injection metadata columns match bmxp.IMDATA schema (injection_id, broad_id, injection_type, batches, etc.)
- All sample metadata columns match bmxp.SMDATA schema (broad_id as index, with arbitrary biospecimen metadata)
- Feature abundance table is a valid pivot table with shape (n_features, n_injections) indexed by Compound_ID × injection_id with no unexpected nulls
- QC report shows pass status for feature integrity, missing-value thresholds, and metadata completeness checks

## Limitations

- Formation requires input data to already be processed through upstream modules (Chroma, Eclipse, Gravity, Blueshift); it does not handle raw instrument files or unaligned datasets
- The shared schema column headers can be customized globally before runtime but must be consistent across all modules used in the pipeline
- Formation does not perform feature annotation or metabolite identification; annotation fields (Annotation_ID, Metabolite) are expected to be populated upstream or externally
- QC checks are based on predefined thresholds for missing values and metadata completeness; highly non-standard datasets may fail checks without custom configuration

## Evidence

- [other] Formation is a standalone module in the BMXP pipeline that performs formatting and final quality control on processed LCMS feature data.: "Formation is a standalone module in the BMXP pipeline that performs formatting and final quality control on processed LCMS feature data."
- [other] Load the processed feature table (output from Blueshift or Gravity) in the appropriate metabolomics data format. Apply Formation-specific formatting rules to standardize feature annotations, metadata structure, and column naming conventions.: "Load the processed feature table (output from Blueshift or Gravity) in the appropriate metabolomics data format. Apply Formation-specific formatting rules to standardize feature annotations, metadata"
- [other] Execute quality control checks on feature integrity, missing-value thresholds, and metadata completeness. Generate a formatted output file and a QC report documenting pass/fail status for each check.: "Execute quality control checks on feature integrity, missing-value thresholds, and metadata completeness. Generate a formatted output file and a QC report documenting pass/fail status for each check."
- [readme] All BMXP modules use a shared schema and file formats with our prefered columns headers. These files are (along with their labels): Feature Metadata `bmxp.FMDATA` - Describes the feature. Index default is `Compound_ID`: "All BMXP modules use a shared schema and file formats with our prefered columns headers. These files are (along with their labels): Feature Metadata `bmxp.FMDATA` - Describes the feature. Index"
- [readme] Feature Abundances - Pivot table of Feature x Injection (`Compound_ID` x `injection_id`) containing the abundances.: "Feature Abundances - Pivot table of Feature x Injection (`Compound_ID` x `injection_id`) containing the abundances."
- [readme] Each tool is meant to be a standalone module that performs a step in our processing pipeline. They are written in Python and C, and designed to be perfomant and cloud-compatible.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline. They are written in Python and C, and designed to be perfomant and cloud-compatible."
