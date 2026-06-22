---
name: mass-spectrometry-file-inventory-management
description: Use when you have uploaded MS/MS data to MassIVE with validated sample-information metadata and need to subset public files by sample attributes (organism, tissue type, extraction method, ionization source, pre-MS separation) to create reproducible, manageable cohorts for molecular networking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MassIVE
  - ReDU
  - ReDU File Selector
  - GNPS
  - ReDU metadata validator
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

# mass-spectrometry-file-inventory-management

## Summary

Organize and partition public tandem MS/MS files from MassIVE into logical cohorts by filtering sample-information metadata, enforcing workflow-appropriate file count thresholds, and assembling a manifest for downstream molecular networking or library search analysis. This skill bridges repository-scale data discovery with reproducible reuse by enabling researchers to filter, group, and validate MS/MS file subsets before large-scale analysis.

## When to use

You have uploaded MS/MS data to MassIVE with validated sample-information metadata and need to subset public files by sample attributes (organism, tissue type, extraction method, ionization source, pre-MS separation) to create reproducible, manageable cohorts for molecular networking (≤3000 files) or spectral library search (≤5000 files). Apply this skill when you want to contextualize your own data against public data at repository scale or to compose multiple filtered groups for comparative analysis.

## When NOT to use

- Sample-information metadata is incomplete, unvalidated, or unavailable for the MassIVE accession; the validator must first pass before file inventory can proceed.
- Input file count already conforms to a single workflow requirement (e.g., ≤3000 for molecular networking) and no partitioning or cohort comparison is needed.
- MS/MS data is stored in a private or embargoed MassIVE accession; ReDU requires public data access to enable filtering and grouping.

## Inputs

- MassIVE accession ID
- validated ReDU sample-information metadata TSV (gnps_metadata.tsv) with categories such as organism, tissue type, extraction method, ionization source, pre-MS separation
- list of MS/MS file identifiers associated with the MassIVE accession

## Outputs

- grouping manifest (TSV or JSON format) with columns: group ID, filter criteria, MassIVE file identifiers, file count per group, recommended workflow (molecular networking or library search)
- partitioned file subsets, each with file count verified against workflow thresholds

## How to apply

First, load the validated ReDU sample-information metadata (gnps_metadata.tsv) from the MassIVE accession into a tabular structure and parse all unique sample-information categories and their values across all rows (e.g., extraction method, organism, tissue type). Second, use the ReDU File Selector to apply attribute filters via orange buttons (sample-information categories) and red boxes (attribute filters) to partition the file list into logical subsets. Third, count the MS/MS files in each subset and enforce the workflow-appropriate threshold: reject or subdivide any group exceeding 3000 files for molecular networking or 5000 files for library search. Fourth, assemble and export a grouping manifest (TSV or JSON) listing each group ID, selected filter criteria, constituent MassIVE file identifiers, file count, and recommended downstream workflow. Validate the manifest against the File Selector's Selection Summary Panel to ensure counts and assignments match.

## Related tools

- **ReDU File Selector** (Interactive web interface for filtering and grouping public MS/MS files by sample-information categories and assigning file subsets to group buttons (G1–G6); displays file counts in real time via the Selection Summary Panel) — https://github.com/mwang87/ReDU-MS2-GNPS
- **MassIVE** (Public data repository where MS/MS files and sample-information metadata are uploaded and stored; serves as the source of file inventories and metadata for filtering) — https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp
- **GNPS** (Downstream platform that receives file manifests from ReDU for batch spectral library search and molecular networking workflows; enforces file count limits (3000 for networking, 5000 for library search)) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **ReDU metadata validator** (Drag-and-drop tool for validating the sample-information template before file filtering; ensures metadata completeness and correctness prior to File Selector use) — https://github.com/mwang87/ReDU-MS2-GNPS

## Evaluation signals

- Manifest file count for each group matches the Selection Summary Panel in the ReDU File Selector (no discrepancies).
- All group file counts satisfy the workflow threshold: ≤3000 for molecular networking, ≤5000 for library search; groups exceeding the threshold are either subdivided or flagged as needing rejection.
- Sample-information metadata passes ReDU drag-and-drop validator before filtering begins; no rows have missing or malformed category values.
- Each group ID in the manifest has a complete audit trail: filter criteria, constituent file identifiers, and downstream workflow assignment are all present and internally consistent.
- MassIVE file identifiers in the manifest are resolvable (can be retrieved from the MassIVE accession) and correspond to actual MS/MS files.

## Limitations

- ReDU File Selector is restricted to public MassIVE data; private or embargoed accessions cannot be filtered or grouped.
- File count thresholds (3000 for molecular networking, 5000 for library search) are recommendations and may need adjustment if downstream tools have different scaling constraints or if compute resources are limited.
- Sample-information metadata quality is dependent on manual or automated completion by data contributors; incomplete or inconsistent category values will reduce filtering effectiveness and may result in orphaned or miscategorized files.
- The same chemical can have multiple GNPS annotations due to slight MS2 spectral variation, which may affect downstream library matching and filtering logic if annotation consistency is a criterion.
- Manifest export formats (TSV vs. JSON) must match the downstream workflow system's input requirements; format mismatch can cause import failures or data loss.

## Evidence

- [other] Parse and inventory all unique sample-information categories and their values across all rows (e.g., extraction method, ionization source, organism, tissue type, pre-MS separation).: "Parse and inventory all unique sample-information categories and their values across all rows (e.g., extraction method, ionization source, organism, tissue type, pre-MS separation)."
- [other] The ReDU File Selector allows users to filter files using orange buttons corresponding to sample-information categories, apply attribute filters that appear as red boxes in the Attribute Filters Panel, and assign filtered files to one of six group buttons (G1-G6), with file counts updated in the Selection Summary Panel.: "The ReDU File Selector allows users to filter files using orange buttons corresponding to sample-information categories, apply attribute filters that appear as red boxes in the Attribute Filters"
- [other] The recommended limits are 3000 files for molecular networking and 5000 files for library search.: "The recommended limits are 3000 files for molecular networking and 5000 files for library search."
- [other] For each subset, count the associated MS/MS files and enforce the workflow-appropriate threshold: reject or subdivide any group exceeding 3000 files for molecular networking or 5000 files for library search.: "For each subset, count the associated MS/MS files and enforce the workflow-appropriate threshold: reject or subdivide any group exceeding 3000 files for molecular networking or 5000 files for library"
- [other] Assemble and export a grouping manifest (TSV or JSON) listing each group ID, selected filter criteria, constituent MassIVE file identifiers, file count, and recommended downstream workflow (molecular networking or library search).: "Assemble and export a grouping manifest (TSV or JSON) listing each group ID, selected filter criteria, constituent MassIVE file identifiers, file count, and recommended downstream workflow (molecular"
- [readme] ReDU is a community-minded approach to find and reuse public data containing tandem MS data at the repository scale. ReDU is a launchpad for co- or re-analysis of public data via the Global Natural Product Social Molecular Networking Platform (GNPS).: "ReDU is a community-minded approach to find and reuse public data containing tandem MS data at the repository scale. ReDU is a launchpad for co- or re-analysis of public data via the Global Natural"
- [methods] Validation of the ReDU sample information template using the drag-and-drop validator: "Validation of the ReDU sample information template using the drag-and-drop validator"
- [abstract] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra cause the pattern to match different reference MS2 spectra for the same chemical"
