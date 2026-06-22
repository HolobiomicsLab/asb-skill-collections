---
name: filter-criteria-composition-and-validation
description: Use when you are preparing to reuse public tandem MS data from MassIVE via ReDU and need to partition files by sample metadata (e.g., organism, tissue type, extraction method, ionization source, pre-MS separation) into groups for co-analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - MassIVE
  - ReDU
  - GNPS
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-020-0916-7
  all_source_dois:
  - 10.1038/s41592-020-0916-7
  - 10.1186/2047-217x-2-16
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# filter-criteria-composition-and-validation

## Summary

Systematically compose and validate sample-information filter criteria to partition public mass spectrometry files into cohorts suitable for downstream analysis (molecular networking or library search). This skill ensures that user-defined metadata filters correctly identify and group files while respecting workflow-specific file-count thresholds.

## When to use

You are preparing to reuse public tandem MS data from MassIVE via ReDU and need to partition files by sample metadata (e.g., organism, tissue type, extraction method, ionization source, pre-MS separation) into groups for co-analysis. Use this skill when the repository contains heterogeneous datasets and you must enforce group-size limits (≤3000 files for molecular networking; ≤5000 files for library search) before downstream analysis.

## When NOT to use

- Input metadata file has not passed ReDU validation; use the drag-and-drop validator before composing filters.
- You are filtering on continuous numeric fields (e.g., retention time, m/z) rather than categorical metadata; ReDU File Selector is designed for sample-information categories.
- Downstream workflow is not molecular networking or library search, or workflow-specific file-count thresholds are not applicable to your use case.

## Inputs

- gnps_metadata.tsv (validated ReDU sample-information metadata from MassIVE accession)
- MassIVE accession ID
- User-specified or predefined sample-information attributes (e.g., organism, tissue type, extraction method, ionization source, pre-MS separation)
- Workflow type (molecular networking or library search)

## Outputs

- Grouping manifest (TSV or JSON) listing group ID, selected filter criteria, constituent MassIVE file identifiers, file count, and recommended downstream workflow
- Validated file cohorts partitioned by sample-information criteria
- File-count confirmation for each group relative to workflow threshold

## How to apply

Load the validated ReDU sample-information metadata (gnps_metadata.tsv) from the MassIVE accession and parse all unique sample-information categories and their values across rows. Compose filter criteria by selecting one or more sample-information attributes (e.g., 'organism=Piper' AND 'tissue=leaf'). Apply these filters within the ReDU File Selector using orange buttons for category selection and attribute filtering (red boxes in Attribute Filters Panel). For each filtered subset, count the associated MS/MS files and verify the count does not exceed the workflow-appropriate threshold: reject or subdivide any group exceeding 3000 files for molecular networking or 5000 files for library search. Validation occurs via the drag-and-drop validator and confirmed by checking that file counts in the Selection Summary Panel match expected group assignments.

## Related tools

- **ReDU** (Web interface for composing and applying sample-information filters to partition public MS/MS files by metadata; File Selector displays orange buttons for category selection and red-boxed Attribute Filters Panel for filter application.) — https://github.com/mwang87/ReDU-MS2-GNPS
- **MassIVE** (Public data repository hosting raw and processed MS/MS data; ReDU retrieves sample-information metadata (gnps_metadata.tsv) and file identifiers from MassIVE accessions.)
- **GNPS** (Spectral library search and molecular networking workflows that consume the filtered file cohorts downstream; workflow type determines file-count threshold (3000 for networking; 5000 for search).) — https://github.com/CCMS-UCSD/GNPSDocumentation

## Evaluation signals

- Validation status is 'pass' when gnps_metadata.tsv is processed by the drag-and-drop validator with no schema or field errors.
- File-count for each group does not exceed 3000 (molecular networking) or 5000 (library search) as confirmed in the Selection Summary Panel.
- Grouping manifest lists all constituent MassIVE file identifiers and their counts match the counts shown in ReDU File Selector for each group (G1–G6).
- Applied filter criteria (sample-information attributes and their values) appear as red boxes in Attribute Filters Panel and are human-readable in the manifest.
- Each group is assigned a recommended downstream workflow (molecular networking or library search) based on file count relative to threshold.

## Limitations

- ReDU File Selector supports filtering on categorical sample-information metadata only; continuous fields (e.g., m/z, retention time) require alternative query mechanisms.
- The same chemical can have multiple GNPS annotations due to slight variation in MS/MS spectra, which may affect downstream enrichment analysis but does not impact filter-criteria composition.
- Manual completion of the ReDU sample-information template introduces the risk of inconsistent or missing category values; missing or malformed entries will reduce effective file coverage in filtered cohorts.

## Evidence

- [other] Parse and inventory all unique sample-information categories and their values across all rows (e.g., extraction method, ionization source, organism, tissue type, pre-MS separation).: "Parse and inventory all unique sample-information categories and their values across all rows (e.g., extraction method, ionization source, organism, tissue type, pre-MS separation)."
- [abstract] The orange buttons in the center of the screen correspond to Sample Information categories: "The orange buttons in the center of the screen correspond to Sample Information categories"
- [abstract] If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel (upper-right corner) of the page: "If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel (upper-right corner) of the page"
- [other] The recommended limits are 3000 files for molecular networking and 5000 files for library search.: "The recommended limits are 3000 files for molecular networking and 5000 files for library search."
- [other] Assemble and export a grouping manifest (TSV or JSON) listing each group ID, selected filter criteria, constituent MassIVE file identifiers, file count, and recommended downstream workflow (molecular networking or library search).: "Assemble and export a grouping manifest (TSV or JSON) listing each group ID, selected filter criteria, constituent MassIVE file identifiers, file count, and recommended downstream workflow (molecular"
- [methods] Validation of the ReDU sample information template using the drag-and-drop validator: "Validation of the ReDU sample information template using the drag-and-drop validator"
