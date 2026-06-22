---
name: sample-information-metadata-parsing
description: Use when when you have a validated ReDU sample-information metadata file (gnps_metadata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - MassIVE
  - ReDU
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

# sample-information-metadata-parsing

## Summary

Parse and inventory validated ReDU sample-information metadata (TSV format) to extract unique categories, their values, and associated MS/MS file counts across all rows. This enables systematic filtering and grouping of public mass spectrometry files by sample attributes for downstream cohort assembly.

## When to use

When you have a validated ReDU sample-information metadata file (gnps_metadata.tsv) loaded from a MassIVE accession and need to understand the available filterable dimensions (extraction method, ionization source, organism, tissue type, pre-MS separation) before applying attribute filters to partition files into analysis groups.

## When NOT to use

- Input metadata has not passed ReDU validation; first validate using the drag-and-drop validator.
- Sample-information template contains unfilled rows or malformed entries; clean and delete all extra rows before parsing.
- Metadata is already in a non-tabular or proprietary format not compatible with tab-separated TSV; convert to TSV first.

## Inputs

- ReDU sample-information metadata TSV file (gnps_metadata.tsv) from a MassIVE accession
- Validated metadata (passed ReDU drag-and-drop validator)
- Associated MassIVE file identifier manifest

## Outputs

- Parsed inventory of unique sample-information categories (e.g., extraction method, ionization source, organism, tissue type, pre-MS separation)
- Enumerated value set for each category with occurrence counts
- Cross-reference mapping of category–value pairs to constituent MS/MS file identifiers
- Metadata schema validation report (structure and completeness)

## How to apply

Load the validated ReDU sample-information metadata (gnps_metadata.tsv) from the MassIVE accession into a tabular structure. Parse all rows and systematically inventory unique sample-information categories and their discrete values across the entire cohort. Document the frequency of each category–value pair and cross-reference to the set of MS/MS files annotated with each combination. This parsed inventory serves as the reference layer for subsequent attribute filtering operations in the ReDU File Selector, which applies filters as red boxes in the Attribute Filters Panel to partition files into logical subsets and enforce workflow-appropriate file count thresholds (≤3000 files for molecular networking, ≤5000 for library search).

## Related tools

- **MassIVE** (Public repository hosting raw and processed mass spectrometry data; source of sample-information metadata files via accession identifiers) — https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp
- **ReDU** (Metadata validation and File Selector interface; provides the drag-and-drop validator and attribute filter panel that consume parsed sample-information inventory) — https://github.com/mwang87/ReDU-MS2-GNPS
- **GNPS** (Downstream analysis platform that receives file grouping manifests (TSV/JSON) assembled from parsed metadata for molecular networking or library search workflows) — https://github.com/CCMS-UCSD/GNPSDocumentation

## Evaluation signals

- All rows in the input TSV are parsed without errors; row count and column count match the validated source file.
- Unique sample-information categories are correctly enumerated; each category contains only valid values from the drop-down controlled vocabulary used during metadata entry.
- File identifier cross-reference is complete: every MS/MS file in the MassIVE accession is assigned to at least one category–value pair; no orphaned files.
- Occurrence counts are accurate: sum of file counts across all values within a category equals total file count in the accession.
- Downstream attribute filters in the ReDU File Selector correctly reflect the parsed categories and values; filter options match the inventory.

## Limitations

- Parsing accuracy depends on strict adherence to the ReDU sample-information template schema; non-standard column names or missing required fields will cause parsing failures.
- Sample-information metadata is manually entered by data submitters; incomplete or inconsistent entries (e.g., typos, ambiguous organism names) introduce noise and reduce filtering precision.
- The same chemical compound can have multiple GNPS annotations due to slight variation in MS2 spectra (m/z or abundance), which may complicate downstream grouping and analysis interpretation.
- File count thresholds (3000 for molecular networking, 5000 for library search) are recommended limits; very large cohorts may require subdivision or workflow adjustment.

## Evidence

- [other] Parse and inventory all unique sample-information categories and their values across all rows (e.g., extraction method, ionization source, organism, tissue type, pre-MS separation).: "Parse and inventory all unique sample-information categories and their values across all rows (e.g., extraction method, ionization source, organism, tissue type, pre-MS separation)."
- [other] Load the validated ReDU sample-information metadata (gnps_metadata.tsv) from the MassIVE accession into a tabular structure.: "Load the validated ReDU sample-information metadata (gnps_metadata.tsv) from the MassIVE accession into a tabular structure."
- [other] Apply user-specified or predefined filters on one or more sample-information attributes to partition the file list into logical subsets.: "Apply user-specified or predefined filters on one or more sample-information attributes to partition the file list into logical subsets."
- [methods] Validation of the ReDU sample information template using the drag-and-drop validator: "Validation of the ReDU sample information template using the drag-and-drop validator"
- [abstract] The orange buttons in the center of the screen correspond to Sample Information categories: "The orange buttons in the center of the screen correspond to Sample Information categories"
- [abstract] If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel (upper-right corner) of the page: "If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel (upper-right corner)"
- [abstract] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical"
- [other] count the associated MS/MS files and enforce the workflow-appropriate threshold: reject or subdivide any group exceeding 3000 files for molecular networking or 5000 files for library search.: "count the associated MS/MS files and enforce the workflow-appropriate threshold: reject or subdivide any group exceeding 3000 files for molecular networking or 5000 files for library search."
