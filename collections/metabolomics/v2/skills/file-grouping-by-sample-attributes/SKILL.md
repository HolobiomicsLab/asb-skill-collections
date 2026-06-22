---
name: file-grouping-by-sample-attributes
description: Use when you have a validated ReDU sample-information metadata table (gnps_metadata.tsv) loaded from a MassIVE accession, and you need to partition public MS/MS files into multiple analysis cohorts by one or more sample attributes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3371
  tools:
  - MassIVE
  - ReDU
  - ReDU File Selector
  - GNPS
  - ReDU metadata validator
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-grouping-by-sample-attributes

## Summary

Partition a collection of public mass spectrometry files from MassIVE into logical cohorts by filtering on validated sample-information metadata (extraction method, ionization source, organism, tissue type, pre-MS separation, etc.), then assign filtered subsets to named groups while enforcing workflow-specific file-count thresholds. This skill enables downstream co-analysis of public tandem MS data via GNPS molecular networking or library search.

## When to use

You have a validated ReDU sample-information metadata table (gnps_metadata.tsv) loaded from a MassIVE accession, and you need to partition public MS/MS files into multiple analysis cohorts by one or more sample attributes. Use this skill when you want to explore how sample type, preparation method, or organism influence spectral patterns, or when you need to prepare file subsets for molecular networking (≤3000 files) or library search (≤5000 files).

## When NOT to use

- Sample-information metadata has not been validated against the ReDU template—proceed to validation first.
- Your analysis goal does not require partitioning by sample attributes (e.g., you are analyzing a single, homogeneous cohort).
- MassIVE file identifiers are not available or the files have not been uploaded to MassIVE/made public.

## Inputs

- validated ReDU sample-information metadata table (gnps_metadata.tsv) from a MassIVE accession
- inventory of unique sample-information categories and their values (extraction method, ionization source, organism, tissue type, pre-MS separation)
- user-specified or predefined filter criteria on one or more sample-information attributes

## Outputs

- partition of MS/MS file list into logical subsets
- grouping manifest (TSV or JSON) with group ID, filter criteria, MassIVE file identifiers, file count, and recommended workflow
- file-count validation report confirming compliance with molecular networking (≤3000) or library search (≤5000) thresholds

## How to apply

Load the validated ReDU sample-information metadata (gnps_metadata.tsv) from the MassIVE accession into a tabular structure and parse all unique sample-information categories and their values across rows. Use the ReDU File Selector to apply filters on one or more attributes: click orange buttons corresponding to sample-information categories, then select attribute values—these will appear as red boxes in the Attribute Filters Panel. For each logical subset, count the associated MS/MS files and enforce the workflow-appropriate threshold: reject or subdivide any group exceeding 3000 files for molecular networking or 5000 files for library search. Assemble and export a grouping manifest (TSV or JSON) listing each group ID, selected filter criteria, constituent MassIVE file identifiers, file count, and recommended downstream workflow.

## Related tools

- **ReDU File Selector** (interactive UI for filtering and grouping MS/MS files by sample-information metadata; displays orange buttons for categories, red boxes for applied filters, and group assignment buttons (G1–G6)) — https://github.com/mwang87/ReDU-MS2-GNPS
- **MassIVE** (public repository for mass spectrometry data; stores raw and processed MS/MS files and provides accession identifiers and file URLs for filtering operations) — https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp
- **GNPS** (backend platform for spectral library matching and molecular networking workflows; receives grouped file cohorts from ReDU for downstream analysis) — https://github.com/CCMS-UCSD/GNPSDocumentation
- **ReDU metadata validator** (drag-and-drop tool to validate sample-information metadata template before file grouping; ensures compliance with ReDU schema) — https://github.com/mwang87/ReDU-MS2-GNPS

## Evaluation signals

- All selected files are present in MassIVE and correspond to the applied filter criteria (spot-check file counts against MassIVE query results).
- File count for each group does not exceed 3000 (molecular networking) or 5000 (library search); groups exceeding threshold are flagged or subdivided.
- Grouping manifest is valid TSV or JSON with complete columns: group ID, filter criteria, MassIVE file IDs, file count, recommended workflow.
- Orange and red filter boxes in the File Selector UI accurately reflect the sample-information categories and values applied.
- Selection Summary Panel reports file counts that match the grouping manifest output.

## Limitations

- Recommended file-count limits (3000 for molecular networking, 5000 for library search) are guidelines; very large groups may still fail or produce incomplete results depending on compute resources.
- The same chemical can have multiple GNPS annotations due to slight variation in MS2 spectra, which may affect downstream chemical-level filtering or enrichment.
- Manual completion of the ReDU sample-information template is required before filtering; incomplete or inconsistent metadata will limit available filter categories.
- File Selector filtering is limited to pre-defined sample-information categories in the ReDU schema; arbitrary or unmapped metadata fields cannot be used as filters.

## Evidence

- [other] The ReDU File Selector allows users to filter files using orange buttons corresponding to sample-information categories, apply attribute filters that appear as red boxes in the Attribute Filters Panel, and assign filtered files to one of six group buttons (G1-G6), with file counts updated in the Selection Summary Panel.: "The ReDU File Selector allows users to filter files using orange buttons corresponding to sample-information categories, apply attribute filters that appear as red boxes in the Attribute Filters"
- [other] Load the validated ReDU sample-information metadata (gnps_metadata.tsv) from the MassIVE accession into a tabular structure. Parse and inventory all unique sample-information categories and their values across all rows (e.g., extraction method, ionization source, organism, tissue type, pre-MS separation).: "Load the validated ReDU sample-information metadata (gnps_metadata.tsv) from the MassIVE accession into a tabular structure. Parse and inventory all unique sample-information categories and their"
- [other] For each subset, count the associated MS/MS files and enforce the workflow-appropriate threshold: reject or subdivide any group exceeding 3000 files for molecular networking or 5000 files for library search.: "For each subset, count the associated MS/MS files and enforce the workflow-appropriate threshold: reject or subdivide any group exceeding 3000 files for molecular networking or 5000 files for library"
- [other] Assemble and export a grouping manifest (TSV or JSON) listing each group ID, selected filter criteria, constituent MassIVE file identifiers, file count, and recommended downstream workflow (molecular networking or library search).: "Assemble and export a grouping manifest (TSV or JSON) listing each group ID, selected filter criteria, constituent MassIVE file identifiers, file count, and recommended downstream workflow (molecular"
- [abstract] The orange buttons in the center of the screen correspond to Sample Information categories. If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel (upper-right corner) of the page.: "The orange buttons in the center of the screen correspond to Sample Information categories. If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel (upper-right corner)"
- [methods] Manual completion of the ReDU sample information template. Fill in sample information using drop-downs when applicable. When complete, delete all extra rows of the template. Download from Google Sheets as a tab separated text file using 'File-Download as' and selecting 'Tab-seperated values...'. Validation of the ReDU sample information template using the drag-and-drop validator.: "Manual completion of the ReDU sample information template...Validation of the ReDU sample information template using the drag-and-drop validator"
