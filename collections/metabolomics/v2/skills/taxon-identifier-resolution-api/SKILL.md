---
name: taxon-identifier-resolution-api
description: Use when you have a metadata table with raw, non-standardized taxonomy
  strings (e.g. misspellings, deprecated nomenclature, or aliases) in separate species,
  genus, and family columns, and you need to standardize them before performing taxon-dependent
  scoring (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0625
  tools:
  - Open Tree of Life
  - INVENTA
  - Lotus Database
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- The taxonomy should be cleaned to uptoday recognized names, you can use the Open
  Tree of Life
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fmolb.2022.1028334
  all_source_dois:
  - 10.3389/fmolb.2022.1028334
  - 10.1038/s41467-021-23953-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Taxon identifier resolution via Open Tree of Life API

## Summary

Normalize raw taxonomy strings (species, genus, family) to currently recognized taxonomic names and their Open Tree of Life identifiers (OTOL_ID) for downstream integration into metabolomics literature and chemical class calculations. This ensures consistent cross-referencing with external taxonomic databases and enables accurate Literature Component scoring.

## When to use

You have a metadata table with raw, non-standardized taxonomy strings (e.g. misspellings, deprecated nomenclature, or aliases) in separate species, genus, and family columns, and you need to standardize them before performing taxon-dependent scoring (e.g. Literature Component calculation) or cross-referencing with the Lotus Database (which uses NPClassifyre ontology). This is mandatory before running INVENTA if you plan to use the Literature Component or Class Component.

## When NOT to use

- Taxonomy strings are already validated and current in the input (e.g. already curated against a recent taxonomic reference).
- You do not plan to use Literature Component or Class Component scoring; if only Feature Component is needed, raw taxonomy may be acceptable.
- The Open Tree of Life API is unavailable or your network cannot reach the service.

## Inputs

- Metadata table (TSV format) with ATTRIBUTE_Species, ATTRIBUTE_Genus, ATTRIBUTE_Family columns
- Raw taxonomy strings (species, genus, and family names in free text)

## Outputs

- Cleaned metadata TSV with resolved taxonomy names
- OTOL_ID columns for species, genus, and family ranks
- Mapping table linking original names to resolved names and OTOL_IDs

## How to apply

Load the metadata table in TSV format and extract the three columns designated as species_column, genus_column, and family_column. For each unique taxon name in each rank, query the Open Tree of Life API to retrieve the current accepted name and corresponding OTOL_ID. Build a mapping table linking original names to resolved names and OTOL_IDs for all three ranks. Replace the original taxonomy strings in the metadata table with the resolved names and append new OTOL_ID columns for each rank. The resolved names ensure consistency with currently recognized nomenclature, and the OTOL_IDs enable linking to external resources. Output a cleaned metadata TSV with standardized taxonomy and OTOL_ID fields, suitable for LC and CC calculations.

## Related tools

- **Open Tree of Life** (Provides API queries to retrieve accepted taxon names and OTOL_IDs for normalization) — https://opentree.readthedocs.io/en/latest/readme.html
- **INVENTA** (Consumes cleaned metadata with resolved taxonomy for Literature Component and Class Component calculations) — https://github.com/luigiquiros/inventa
- **Lotus Database** (Target database for cross-referencing; uses NPClassifyre ontology and requires standardized taxonomy)

## Evaluation signals

- All rows in the resolved taxonomy columns match currently accepted names as confirmed by Open Tree of Life.
- OTOL_ID columns are populated with valid identifiers for ≥95% of resolved taxa; any unresolved names are flagged or logged.
- Mapping table shows no duplicate resolved names (i.e., multiple original names map to the same accepted name as expected for synonyms).
- Cleaned metadata schema matches GNPS format with MANDATORY headers (ATTRIBUTE_Species, ATTRIBUTE_Organe) present; no syntax errors in TSV.
- Literature Component and Class Component calculations downstream do not fail due to missing or malformed taxonomy fields.

## Limitations

- Open Tree of Life may not recognize very recent species descriptions or highly specialized nomenclature; unresolvable names should be manually reviewed or excluded.
- API query rate limits or network latency may slow processing for large metadata tables with many unique taxa.
- Taxonomy standardization does not resolve environmental or sampling ambiguities (e.g. plants identified only to family level); quality of input taxonomy strings directly affects output quality.
- OTOL_ID linking is current as of the Open Tree of Life release date; downstream tools using different or older taxonomic references may not align perfectly.

## Evidence

- [other] For each unique taxon name in each taxonomic rank, query the Open Tree of Life API to retrieve the current accepted name and taxon Open Tree of Life identifier (OTOL_ID).: "For each unique taxon name in each taxonomic rank, query the Open Tree of Life API to retrieve the current accepted name and taxon Open Tree of Life identifier (OTOL_ID)."
- [other] The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life to do so.: "The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life to do so (https://opentree.readthedocs.io/en/latest/readme.html)."
- [other] Taxonomy normalization is performed using the Open Tree of Life reference to convert sample taxonomy strings to currently recognized names, producing a cleaned taxonomy table required for Literature Component calculations.: "Taxonomy normalization is performed using the Open Tree of Life reference to convert sample taxonomy strings to currently recognized names, producing a cleaned taxonomy table required for Literature"
- [other] Replace the original taxonomy strings in the metadata table with resolved names and append OTOL_ID columns for each rank.: "Replace the original taxonomy strings in the metadata table with resolved names and append OTOL_ID columns for each rank."
- [other] given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary: "given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary"
