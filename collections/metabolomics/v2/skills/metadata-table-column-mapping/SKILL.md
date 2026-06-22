---
name: metadata-table-column-mapping
description: Use when you have a GNPS-format TSV metadata table with mandatory columns (ATTRIBUTE_Species, ATTRIBUTE_Organe, and optional genus/family columns) and need to prepare cleaned, standardized taxonomy strings for integration into the Literature Component or cross-referencing with external reference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3407
  tools:
  - Open Tree of Life
  - Inventa
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- The taxonomy should be cleaned to uptoday recognized names, you can use the Open Tree of Life
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_inventa_cq
    doi: 10.3389/fmolb.2022.1028334
    title: Inventa
  dedup_kept_from: coll_inventa_cq
schema_version: 0.2.0
---

# metadata-table-column-mapping

## Summary

Map and extract taxonomic and sample annotation columns from a TSV metadata table (GNPS format) to enable downstream calculations of novelty scores and Literature Component metrics. This skill bridges raw sample metadata to structured feature-taxon associations required by metabolomics prioritization workflows.

## When to use

Apply this skill when you have a GNPS-format TSV metadata table with mandatory columns (ATTRIBUTE_Species, ATTRIBUTE_Organe, and optional genus/family columns) and need to prepare cleaned, standardized taxonomy strings for integration into the Literature Component or cross-referencing with external reference databases like Lotus or Open Tree of Life. Required when the input metadata uses inconsistent or unrecognized taxonomic nomenclature that must be resolved before scoring.

## When NOT to use

- Metadata is already validated against a stable, internally curated taxonomic reference and does not require reconciliation with external nomenclature standards.
- Input table lacks mandatory ATTRIBUTE_Species or ATTRIBUTE_Organe columns; column mapping cannot proceed without identifying taxon columns.
- Downstream analysis does not require Literature Component scoring or cross-reference integration with Lotus Database; column standardization alone may not justify the overhead.

## Inputs

- TSV metadata table in GNPS format with ATTRIBUTE_Species, ATTRIBUTE_Organe columns (and optionally genus, family columns)
- Open Tree of Life API endpoint (or local reference dataset)

## Outputs

- Cleaned metadata TSV table with resolved taxonomic names
- OTOL_ID columns (one per taxonomic rank: species, genus, family)
- Mapping table linking original taxon names to resolved names and OTOL_IDs

## How to apply

Load the TSV metadata table and identify the three key taxonomic rank columns specified as species_column, genus_column, and family_column according to the GNPS metadata standard. For each unique taxon name in each rank, query the Open Tree of Life API to retrieve the currently accepted taxonomic name and Open Tree of Life identifier (OTOL_ID). Create a mapping table linking original names to resolved names and OTOL_IDs for all three ranks. Replace original taxonomy strings in the metadata table with resolved names and append OTOL_ID columns for each rank. Validate that all taxon strings have been successfully mapped; unresolved entries should be flagged for manual review or secondary lookup. The resulting cleaned metadata TSV table becomes the authoritative input for subsequent Literature Component calculations and enables cross-referencing with the Lotus Database, which uses the NPClassifyre ontology.

## Related tools

- **Open Tree of Life** (Provides API for querying current accepted taxonomic names and OTOL_IDs to resolve and normalize sample taxonomy strings against a community-curated reference) — https://opentree.readthedocs.io/en/latest/readme.html
- **Inventa** (Consumes cleaned metadata table with resolved ATTRIBUTE_Species column to calculate Literature Component and other novelty metrics) — https://github.com/luigiquiros/inventa

## Evaluation signals

- All unique taxon strings in species_column, genus_column, and family_column have corresponding entries in the mapping table with non-null OTOL_IDs.
- Resolved taxonomy names match current nomenclature standards from Open Tree of Life API (no deprecated or misspelled names remain).
- The cleaned metadata TSV table has three new columns (one per rank) containing OTOL_IDs with no missing values for mapped taxa.
- Row count and sample identifiers are preserved between input and output metadata tables; no samples are dropped during mapping.
- Downstream Literature Component calculations using the cleaned metadata produce valid scores (e.g., LC values between 0 and 1) without errors or missing taxon lookups.

## Limitations

- Open Tree of Life API may not have entries for rare, newly described, or colloquial species names; unresolved taxa require manual curation or alternative reference databases.
- Taxonomy normalization is independent of spectral or chemical data and does not validate whether the mapped taxon is appropriate for the sample's actual chemical content.
- Mapping fidelity depends on input string quality (spelling, capitalization, nomenclatural authority); severely malformed or transliterated taxon strings may fail to resolve.
- Open Tree of Life uses its own taxonomic backbone; results may differ from other reference systems (NCBI, GBIF) and may not align with Lotus Database nomenclature without additional harmonization.

## Evidence

- [other] Load the metadata table (TSV format) and extract the three columns specified as species_column, genus_column, and family_column.: "Load the metadata table (TSV format) and extract the three columns specified as species_column, genus_column, and family_column."
- [other] For each unique taxon name in each taxonomic rank, query the Open Tree of Life API to retrieve the current accepted name and taxon Open Tree of Life identifier (OTOL_ID).: "For each unique taxon name in each taxonomic rank, query the Open Tree of Life API to retrieve the current accepted name and taxon Open Tree of Life identifier (OTOL_ID)."
- [other] Replace the original taxonomy strings in the metadata table with resolved names and append OTOL_ID columns for each rank.: "Replace the original taxonomy strings in the metadata table with resolved names and append OTOL_ID columns for each rank."
- [other] The standard format from GNPS is preferred: metadata_filename: it uses the GNPS format: "The standard format from GNPS is preferred: metadata_filename: it uses the GNPS format"
- [readme] The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life to do so: "The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life to do so"
- [readme] ATTRIBUTE_Species : The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life: "ATTRIBUTE_Species : The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life"
- [other] suitable for use in subsequent LC calculations and cross-referencing with the Lotus Database (which uses NPClassifyre ontology): "suitable for use in subsequent LC calculations and cross-referencing with the Lotus Database (which uses NPClassifyre ontology)"
