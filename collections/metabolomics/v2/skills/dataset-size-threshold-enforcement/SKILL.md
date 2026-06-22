---
name: dataset-size-threshold-enforcement
description: Use when when you have partitioned public MS/MS files from MassIVE using the ReDU File Selector into one or more filtered groups (G1–G6) and need to verify that each group's file count complies with computational constraints before submitting to GNPS molecular networking (3000 file limit) or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MassIVE
  - ReDU
  - ReDU File Selector
  - GNPS
derived_from:
- doi: 10.1038/s41592-020-0916-7
  title: ReDU
- doi: 10.1186/2047-217x-2-16
  title: ''
evidence_spans:
- ReDU only interacts with MassIVE
- data uploaded to MassIVE as a public dataset
- Validation of the ReDU sample information template using the drag-and-drop validator
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_redu_cq
    doi: 10.1038/s41592-020-0916-7
    title: ReDU
  dedup_kept_from: coll_redu_cq
schema_version: 0.2.0
---

# dataset-size-threshold-enforcement

## Summary

Enforce workflow-specific file count limits on filtered MS/MS file cohorts to prevent computational overload and ensure successful execution of downstream molecular networking or library search analyses. This skill partitions large datasets into compliant subsets and documents the rationale for subdivision.

## When to use

When you have partitioned public MS/MS files from MassIVE using the ReDU File Selector into one or more filtered groups (G1–G6) and need to verify that each group's file count complies with computational constraints before submitting to GNPS molecular networking (3000 file limit) or spectral library search (5000 file limit) workflows.

## When NOT to use

- The filtered group already complies with the workflow threshold (no further action needed; proceed directly to workflow submission).
- You are performing exploratory visualization or summary statistics on the file collection without intending to run molecular networking or library search (threshold enforcement is unnecessary for non-computational workflows).
- You do not have access to file counts in the ReDU Selection Summary Panel or cannot verify MassIVE file identifiers (cannot reliably enforce thresholds).

## Inputs

- Filtered MS/MS file list from ReDU File Selector (with sample-information metadata attributes applied)
- File count per group from Selection Summary Panel
- Sample-information attribute categories (organism, tissue type, ionization source, extraction method, pre-MS separation, etc.)

## Outputs

- Grouping manifest (TSV or JSON) listing: group ID, selected filter criteria, constituent MassIVE file identifiers, final file count, and recommended workflow
- Validated file cohorts (each ≤3000 files for molecular networking OR ≤5000 files for library search)
- Subdivision decision log (if original group exceeded threshold)

## How to apply

After applying sample-information attribute filters in the ReDU File Selector and observing the file count in the Selection Summary Panel, compare each group's count against the workflow-appropriate threshold: reject, subdivide, or flag any group exceeding 3000 files for molecular networking or 5000 files for library search. For groups that exceed the threshold, apply additional fine-grained filters (e.g., ionization source, organism, tissue type, extraction method) to partition the cohort into smaller compliant subsets. Document each resulting group's filter criteria, constituent MassIVE file identifiers, final file count, and recommended downstream workflow in a manifest (TSV or JSON format). This prevents computational failure and ensures reproducibility of the cohort assembly.

## Related tools

- **ReDU File Selector** (Filter and group public MS/MS files by sample-information metadata; display file counts per group in Selection Summary Panel) — https://github.com/mwang87/ReDU-MS2-GNPS
- **MassIVE** (Repository storing raw and processed MS/MS data; source of file identifiers and file counts queried by ReDU)
- **GNPS** (Downstream platform for molecular networking (3000 file limit) and spectral library search (5000 file limit) workflows) — https://github.com/CCMS-UCSD/GNPSDocumentation

## Evaluation signals

- Each group's file count in the manifest is ≤3000 for molecular networking or ≤5000 for library search (no group exceeds its target threshold).
- All filter criteria used to subdivide groups are documented and traceable to sample-information categories in the ReDU metadata template.
- MassIVE file identifiers in each group are unique and match the file counts reported in the Selection Summary Panel at the time of grouping.
- The manifest can be re-imported into GNPS batch upload or library search without reporting file-count validation errors.
- If a group was subdivided, the original group count, subdivision criteria, and final subgroup counts are recorded for auditability.

## Limitations

- The 3000 and 5000 file thresholds are recommendations for typical computational resources; clusters or institutions with higher capacity may accommodate larger cohorts, but the skill does not provide guidance on how to determine custom thresholds.
- ReDU File Selector does not automatically enforce thresholds; subdivision and manifest assembly must be performed manually or via scripts external to the ReDU UI.
- If sample-information metadata is incomplete or inconsistent across files (e.g., missing organism field, inconsistent spelling), some filtering criteria may not partition the cohort effectively, potentially failing to achieve compliance on first attempt.

## Evidence

- [other] The recommended limits are 3000 files for molecular networking and 5000 files for library search.: "The recommended limits are 3000 files for molecular networking and 5000 files for library search."
- [other] For each subset, count the associated MS/MS files and enforce the workflow-appropriate threshold: reject or subdivide any group exceeding 3000 files for molecular networking or 5000 files for library search.: "For each subset, count the associated MS/MS files and enforce the workflow-appropriate threshold: reject or subdivide any group exceeding 3000 files for molecular networking or 5000 files for library"
- [other] The orange buttons in the center of the screen correspond to Sample Information categories; If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel (upper-right corner) of the page.: "The orange buttons in the center of the screen correspond to Sample Information categories; If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel (upper-right corner)"
- [other] Assemble and export a grouping manifest (TSV or JSON) listing each group ID, selected filter criteria, constituent MassIVE file identifiers, file count, and recommended downstream workflow.: "Assemble and export a grouping manifest (TSV or JSON) listing each group ID, selected filter criteria, constituent MassIVE file identifiers, file count, and recommended downstream workflow"
- [other] Apply user-specified or predefined filters on one or more sample-information attributes to partition the file list into logical subsets.: "Apply user-specified or predefined filters on one or more sample-information attributes to partition the file list into logical subsets."
