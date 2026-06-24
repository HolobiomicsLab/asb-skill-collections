---
name: plant-nomenclature-standardization
description: Use when when your metadata table contains species, genus, or family
  names that may be outdated, synonymous, or non-canonical, and you need to integrate
  them with the Literature Component (which requires standardized taxon identifiers)
  or cross-reference with external databases like Lotus Database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0625
  tools:
  - Open Tree of Life
  - Open Tree of Life API
  - Inventa
  - Lotus Database
  license_tier: open
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

# Plant nomenclature standardization

## Summary

Standardize sample taxonomy strings (species, genus, family) to currently recognized names using the Open Tree of Life API, producing a cleaned taxonomy table with resolved names and OTOL identifiers for integration into downstream metabolomics analysis.

## When to use

When your metadata table contains species, genus, or family names that may be outdated, synonymous, or non-canonical, and you need to integrate them with the Literature Component (which requires standardized taxon identifiers) or cross-reference with external databases like Lotus Database (which uses NPClassifyre ontology tied to current taxonomy).

## When NOT to use

- Taxonomy is already validated against a current reference ontology (e.g., NCBI Taxonomy for the current year) with stable IDs.
- Your workflow does not use the Literature Component or Lotus Database cross-reference; taxonomy standardization is unnecessary if you rely only on spectral similarity.
- Sample metadata lacks species, genus, or family information; the skill requires at least one rank to operate meaningfully.

## Inputs

- Metadata table (TSV format) with ATTRIBUTE_Species, genus, and family columns
- Species, genus, and family column name specifications

## Outputs

- Cleaned metadata TSV table with standardized taxonomy names
- OTOL_ID columns appended for species, genus, and family ranks
- Mapping table linking original taxon names to resolved names and OTOL_IDs

## How to apply

Load the metadata table (TSV format) and extract the columns designated as species_column, genus_column, and family_column. For each unique taxon name at each rank, query the Open Tree of Life API to retrieve the current accepted name and corresponding OTOL_ID. Create a bidirectional mapping table linking original names to resolved names and OTOL_IDs for all three ranks. Replace the original taxonomy strings in the metadata with resolved names and append new OTOL_ID columns for each rank. Output a cleaned metadata TSV table suitable for use in subsequent Literature Component calculations and database cross-referencing. Rationale: standardization ensures consistent taxon matching across literature databases and prevents erroneous compound–taxon associations that could bias novelty scoring.

## Related tools

- **Open Tree of Life API** (Query service to retrieve current accepted taxon names and OTOL identifiers for each original species, genus, and family name) — https://opentree.readthedocs.io/en/latest/readme.html
- **Inventa** (Downstream tool that consumes cleaned metadata to calculate Literature Component based on standardized taxon names) — https://github.com/luigiquiros/inventa
- **Lotus Database** (External reference resource using NPClassifyre ontology; standardized taxonomy enables accurate cross-referencing of reported compounds per taxon)

## Evaluation signals

- All rows in original metadata have corresponding entries in the mapping table (100% coverage).
- No null or empty OTOL_ID values in the output cleaned metadata for any taxon rank that was populated in the input.
- Output taxonomy names are recognized as valid current names when spot-checked against the Open Tree of Life web interface.
- Downstream Literature Component calculation completes without taxon lookup errors, confirming identifiers are resolvable.
- Comparison of original vs. cleaned taxonomy reveals expected synonymies (e.g., deprecated species names mapped to accepted names) rather than random or null replacements.

## Limitations

- Open Tree of Life API may not recognize very recently described species or highly localized/vernacular taxon names; query failures require manual curation.
- Ambiguous or misspelled input names (e.g. 'Genus spp.', 'Plantae indet.') may fail resolution or resolve to higher-level taxa, reducing specificity for Literature Component.
- API query rate limits or network outages can interrupt large-scale standardization; no built-in retry logic mentioned in the README.
- The skill assumes the input metadata columns are correctly labeled and formatted; malformed or misaligned columns will propagate errors downstream.

## Evidence

- [other] Taxonomy normalization is performed using the Open Tree of Life reference to convert sample taxonomy strings to currently recognized names, producing a cleaned taxonomy table required for Literature Component calculations.: "Taxonomy normalization is performed using the Open Tree of Life reference to convert sample taxonomy strings to currently recognized names, producing a cleaned taxonomy table required for Literature"
- [other] For each unique taxon name in each taxonomic rank, query the Open Tree of Life API to retrieve the current accepted name and taxon Open Tree of Life identifier (OTOL_ID).: "For each unique taxon name in each taxonomic rank, query the Open Tree of Life API to retrieve the current accepted name and taxon Open Tree of Life identifier (OTOL_ID)."
- [other] Replace the original taxonomy strings in the metadata table with resolved names and append OTOL_ID columns for each rank.: "Replace the original taxonomy strings in the metadata table with resolved names and append OTOL_ID columns for each rank."
- [readme] The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life to do so: "The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life to do so"
- [other] given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary: "given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary"
