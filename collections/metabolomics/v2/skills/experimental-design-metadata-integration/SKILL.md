---
name: experimental-design-metadata-integration
description: Use when when you have LC-MS raw data and need to process it through a feature detection and quantification pipeline in KNIME, but lack a structured mapping between sample identifiers, experimental conditions, and the raw LC-MS runs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - KNIME Analytics Platform
  - OpenMS
  - ili app
derived_from:
- doi: 10.1038/nprot.2017.122
  title: 3D molecular cartography (Optimus / 'ili)
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_3d_molecular_cartography_optimus_ili_cq
    doi: 10.1038/nprot.2017.122
    title: 3D molecular cartography (Optimus / 'ili)
  dedup_kept_from: coll_3d_molecular_cartography_optimus_ili_cq
schema_version: 0.2.0
---

# experimental-design-metadata-integration

## Summary

Integration of experimental design metadata with LC-MS feature tables in KNIME to enable structured, traceable analysis of untargeted metabolomics datasets. This skill ensures that sample annotations, run order, and quality control information are properly linked to detected features for downstream filtering, normalization, and spatial mapping.

## When to use

When you have LC-MS raw data and need to process it through a feature detection and quantification pipeline in KNIME, but lack a structured mapping between sample identifiers, experimental conditions, and the raw LC-MS runs. Apply this skill if your analysis requires selective exclusion of blank/control runs, reproducibility filtering across pooled QC or replicate samples, or normalized intensity export stratified by experimental group.

## When NOT to use

- Your experimental design metadata is incomplete or inconsistent with actual LC-MS run identifiers — reconcile naming and validate cardinality first.
- You are performing targeted (not untargeted) metabolomics with a predefined m/z and RT ion list — Optimus is optimized for untargeted feature discovery.
- Your LC-MS data is already processed and quality-controlled by an external pipeline and you only need visualization or downstream statistical modeling — use Optimus's export-only workflow branches instead.

## Inputs

- Experimental design file (CSV with sample identifiers, LC-MS run assignments, and metadata columns)
- LC-MS feature table (output from feature detection; m/z, retention time, and quantification intensity matrix)
- Stub input file (KNIME-specific template for workflow initialization)

## Outputs

- Annotated feature table with sample metadata and filtering flags
- Normalized intensity matrix stratified by experimental group and QC/sample type
- Exclusion summary report (features removed by blank/control, rarity, MS/MS, QC reproducibility, or RT boundary filters)
- Spatial feature maps compatible with ili app (JSON or proprietary format)

## How to apply

Load the experimental design file (typically CSV format with sample identifiers, run mappings, and metadata columns) alongside the LC-MS feature table into KNIME file reader nodes. The experimental design file should contain columns linking sample names to their corresponding LC-MS runs and any relevant categorical or continuous metadata (e.g., sample type, treatment group, internal standard concentration). Use KNIME's join/merge nodes to associate feature quantification results with this metadata. This enables conditional filtering steps: for instance, mark features as 'excluded' if they appear only in blank/control runs (step 4 in workflow), or flag features lacking MS/MS data (step 6), or remove low-reproducibility features detected in fewer than a user-defined threshold of runs (step 5). The experimental design file also drives normalization selection (step 11), allowing you to specify which internal standards or QC pooled samples to use as normalizing factors. Validate that the merged feature table preserves row cardinality and that all sample-run mappings are non-null before proceeding to visualization and spatial mapping export.

## Related tools

- **KNIME Analytics Platform** (Workflow orchestration engine for loading experimental design files, joining with feature tables, and executing conditional filtering and normalization logic) — https://www.knime.org
- **OpenMS** (LC-MS feature detection and quantification algorithms integrated into the Optimus workflow; produces the feature table that will be linked to experimental design metadata) — http://www.openms.de
- **ili app** (Web application for interactive visualization of spatial feature maps output by Optimus after experimental design metadata has been used to filter and normalize features) — https://github.com/ili-toolbox/ili

## Evaluation signals

- All rows in the merged feature table have non-null experimental design metadata; no unmatched sample IDs or LC-MS runs remain.
- Feature count decreases predictably after each optional filtering step (blank/control exclusion, rarity filter, MS/MS flag, QC reproducibility, RT boundary); report row counts before and after each step.
- Normalized intensity distributions show expected behavior: intensities scale consistently within QC pooled samples or internal standard-normalized groups, with lower variance across replicates than across distinct experimental conditions.
- Spatial feature maps (ili JSON exports) contain the correct sample type, condition, and normalized intensity metadata for each feature, verifiable by spot-checking a few high-intensity features against the original experimental design file.
- No features are removed or duplicated during the join operation; total feature count is preserved until explicit filtering steps are applied.

## Limitations

- Experimental design file must be provided manually in CSV format with correct column names and sample identifiers matching LC-MS run labels; KNIME will not automatically infer or correct mismatches.
- Reproducibility filtering (step 8) and QC-based normalization (step 11) require replicates or pooled QC samples to be explicitly marked in the experimental design metadata; their absence will disable or degrade these optional steps.
- Minimum RAM requirement of 2 GB is insufficient for datasets with ~100 or more LC-MS runs; temporary file accumulation can exhaust storage if workflow is re-executed iteratively without manual cleanup.
- Putative molecular annotation (step 10) relies on m/z-RT matching to an externally provided molecule list (CSV or GNPS export); MS/MS validation is not performed in Optimus and must be done downstream.
- Direct-infusion MS data is supported but is not spatially mapped; spatial mapping applies only to imaging mass spectrometry or spatially resolved LC-MS workflows where sample coordinates are defined in the experimental design metadata.

## Evidence

- [readme] Experimental design metadata integration enables selective filtering: "Optimus is a workflow for LC-MS-based untargeted metabolomics. It can be used for feature detection, quantification, filtering (e.g. removing background features), annotation, normalization and,"
- [other] Experimental design file and stub input are required inputs: "The Optimus workflow requires an experimental design file and a stub input file as inputs to process LC-MS feature tables for analysis and spatial mapping."
- [readme] Blank/control and QC reproducibility filtering depend on experimental design metadata: "(*Optional*) Exclusion of features that came from blank/control runs. ... (*Optional*) Exclusion of features that are not reproducible in pooled quality control (QC) runs."
- [readme] Normalization methods select based on experimental design strategy: "(*Optional*) Normalization of intensities of detected features. Currently, several normalization methods are available, based on: total ion current (TIC) of each run; internal standards present in"
- [other] Workflow loading and execution requires proper input file configuration: "Load the experimental design file and LC-MS feature table into KNIME using the file reader nodes. 2. Execute the Optimus workflow nodes in sequence to perform feature analysis and spatial mapping as"
