---
name: controlled-vocabulary-term-mapping
description: Use when you have collected or inherited sample-information metadata
  from multiple sources (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0219
  tools:
  - MassIVE
  - ReDU
  - ReDU File Selector
  - ReDU sample-information validator (drag-and-drop)
  - GNPS
  techniques:
  - LC-MS
  license_tier: restricted
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

# Controlled-Vocabulary Term Mapping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Map free-text or heterogeneous sample-information metadata fields to standardized controlled vocabulary terms to enable interoperable filtering, querying, and aggregation across public mass spectrometry repositories. This skill ensures that diverse researcher annotations (e.g., organism names, tissue types, extraction methods) are reconciled to canonical terms, enabling downstream cohort assembly and comparative analysis.

## When to use

You have collected or inherited sample-information metadata from multiple sources (e.g., different research groups uploading to MassIVE) with inconsistent or synonymous terminology for the same biological or chemical attributes (organism, tissue, extraction method, ionization source, pre-MS separation technique). You need to construct cohorts for re-analysis (e.g., molecular networking or library search) by filtering on these attributes, but cannot reliably group files unless terms are normalized. The ReDU File Selector and Chemical Explorer depend on validated, standardized sample-information categories to populate orange filter buttons and red attribute filters.

## When NOT to use

- Metadata is already validated and uses only canonical controlled-vocabulary terms from a single, authoritative source (e.g., a closed ReDU drop-down menu). Applying term mapping will introduce no-op redundancy.
- You are performing a one-time single-dataset analysis and do not need to merge or compare data across cohorts defined by sample-information attributes. Ad-hoc filtering on raw values may suffice.
- The sample-information metadata is incomplete or too sparse (e.g., >50% of target fields are null or 'unknown'). Term mapping cannot disambiguate missing data; data quality remediation must occur first.

## Inputs

- ReDU sample-information metadata TSV (gnps_metadata.tsv) loaded from MassIVE accession with raw, heterogeneous values in one or more sample-information fields
- Reference controlled vocabulary or ontology (e.g., NCBI Taxonomy, UBERON anatomy, Plant Ontology, or locally maintained ReDU drop-down lists)
- Inventory of unique values for a target metadata field (e.g., parsed from column 'organism' across all rows)

## Outputs

- Normalized ReDU sample-information metadata TSV with canonical controlled-vocabulary terms replacing or supplementing raw values
- Term-mapping manifest or lookup table documenting the bijection between raw values and canonical terms (e.g., CSV or JSON)
- Validation report confirming that remapped metadata passes ReDU schema checks and file counts match MassIVE records
- Updated File Selector UI with deduplicated orange filter buttons and red attribute filter boxes reflecting the normalized vocabulary

## How to apply

First, inventory all unique values across a sample-information metadata field (e.g., 'organism') by parsing the validated ReDU sample-information TSV (gnps_metadata.tsv). Second, identify synonyms, spelling variants, and informal aliases (e.g., 'mouse', 'Mus musculus', 'M. musculus', 'rodent') using domain knowledge or a reference ontology (e.g., NCBI Taxonomy, Plant Ontology). Third, assign each unique value to a single canonical controlled-vocabulary term, documenting the mapping rule (exact match, synonym resolution, or hierarchical generalization). Fourth, apply the mapping uniformly across all rows in the metadata file, replacing or augmenting the original value. Fifth, validate the remapped metadata using the ReDU drag-and-drop validator to ensure schema compliance and file counts reconcile with MassIVE records. Sixth, verify that orange filter buttons and red attribute filter boxes in the File Selector now display consistent, non-redundant category values, enabling reproducible user-driven cohort assembly.

## Related tools

- **ReDU File Selector** (User-facing interface for filtering public MS/MS files by sample-information categories; displays orange buttons for categories and red boxes for applied attribute filters; depends on normalized controlled-vocabulary terms to avoid UI redundancy and enable cohort assignment to G1–G6 groups) — https://github.com/mwang87/ReDU-MS2-GNPS
- **ReDU sample-information validator (drag-and-drop)** (Validates remapped sample-information TSV against ReDU schema; confirms file counts reconcile with MassIVE records; signals successful term normalization) — https://github.com/mwang87/ReDU-MS2-GNPS
- **MassIVE** (Public repository for mass spectrometry data; stores raw MS/MS files and associates them with validated sample-information metadata; term-mapped metadata must correctly link files to MassIVE accession records)
- **GNPS** (Downstream workflow platform; receives grouped, term-normalized cohorts from ReDU File Selector and executes spectral library search or molecular networking; benefits from canonical terminology to avoid duplicate or fragmented analysis tasks) — https://github.com/CCMS-UCSD/GNPSDocumentation

## Evaluation signals

- All unique values in a target sample-information field map to exactly one canonical controlled-vocabulary term; no value is unmapped or maps to multiple terms.
- The ReDU sample-information validator reports zero schema violations and file counts in the remapped metadata match the number of MS/MS files recorded in the corresponding MassIVE accession.
- Orange filter buttons and red attribute filter boxes in the ReDU File Selector UI display deduplicated category values (no duplicate or near-duplicate terms); each button corresponds to a single canonical term.
- Users can reproducibly select and assign files to cohort groups (G1–G6) using the normalized filters, and file counts in the Selection Summary Panel remain stable across repeated filter-and-group operations.
- A term-mapping manifest is auditable: for each raw value, the manifest documents the canonical term, the mapping rule (e.g., 'synonym of', 'exact match', 'hierarchical parent'), and the source vocabulary (e.g., 'NCBI Taxonomy v2024-01').

## Limitations

- Term mapping is most effective when the target controlled vocabulary is comprehensive and well-maintained. If the reference ontology is incomplete or becomes stale, some raw values may remain unmapped or map incorrectly.
- Manual term mapping (without automated synonym resolution or fuzzy matching) is labor-intensive and error-prone, especially for large, heterogeneous datasets. Errors in the mapping manifest can propagate through downstream cohort assembly and analysis.
- The ReDU File Selector enforces recommended file-count limits (3000 files for molecular networking, 5000 for library search). Even after term normalization, a single cohort may exceed these thresholds, requiring further subdivision by additional sample-information attributes or manual partitioning.
- Some sample-information fields (e.g., 'organism', 'tissue type') have well-established, publicly maintained ontologies (NCBI Taxonomy, UBERON), while others (e.g., 'pre-MS separation technique', 'extraction protocol details') may lack canonical vocabularies, necessitating ReDU-specific drop-down lists or domain expertise.
- Term mapping is irreversible without preserving the original raw values. Researchers using term-mapped data may lose granularity or context if the mapping rule was overly broad (e.g., collapsing multiple strains into a single species term).

## Evidence

- [other] Parse and inventory all unique sample-information categories and their values across all rows (e.g., extraction method, ionization source, organism, tissue type, pre-MS separation).: "Parse and inventory all unique sample-information categories and their values across all rows (e.g., extraction method, ionization source, organism, tissue type, pre-MS separation)"
- [other] Apply user-specified or predefined filters on one or more sample-information attributes to partition the file list into logical subsets.: "Apply user-specified or predefined filters on one or more sample-information attributes to partition the file list into logical subsets"
- [abstract] The orange buttons in the center of the screen correspond to Sample Information categories. If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel (upper-right corner) of the page.: "The orange buttons in the center of the screen correspond to Sample Information categories. If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel"
- [methods] Fill in sample information using drop-downs when applicable. When complete, **delete all extra rows** of the template. Download from Google Sheets as a tab separated text file using **'File-Download as' and selecting 'Tab-seperated values...'**. Validation of the ReDU sample information template using the drag-and-drop validator.: "Fill in sample information using drop-downs when applicable. Validation of the ReDU sample information template using the drag-and-drop validator"
- [readme] ReDU is a community-minded approach to find and reuse public data containing tandem MS data at the repository scale. Our aim is to empower researchers to put their data in the context of public data as well as explore questions using public data at the repository scale.: "ReDU is a community-minded approach to find and reuse public data containing tandem MS data at the repository scale"
