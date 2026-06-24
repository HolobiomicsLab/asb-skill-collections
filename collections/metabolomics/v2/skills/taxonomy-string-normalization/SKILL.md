---
name: taxonomy-string-normalization
description: Use when when preparing a metadata table (TSV format with species, genus,
  and family columns) for natural product metabolomics analysis where the Literature
  Component score must query known compounds by taxon.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0637
  tools:
  - Open Tree of Life
  - Open Tree of Life API
  - INVENTA
  - Lotus Database
  techniques:
  - LC-MS
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

# Taxonomy String Normalization

## Summary

Normalize sample taxonomy strings (species, genus, family) to currently recognized taxonomic names using the Open Tree of Life reference API, producing a cleaned metadata table with resolved names and OTOL identifiers for downstream Literature Component calculations and cross-referencing with the Lotus Database.

## When to use

When preparing a metadata table (TSV format with species, genus, and family columns) for natural product metabolomics analysis where the Literature Component score must query known compounds by taxon. Use this skill if taxonomy names are non-standard, obsolete, or unrecognized by the Open Tree of Life, which is required before calculating taxon-based novelty metrics in the INVENTA prioritization workflow.

## When NOT to use

- Taxonomy names are already confirmed as currently recognized by Open Tree of Life (e.g., recently validated against OTOL in another pipeline step)
- The analysis does not require the Literature Component or taxon-based novelty scoring; in such cases, taxonomy normalization overhead is not justified
- Input metadata lacks explicit species, genus, or family columns or uses a non-standard taxonomy schema incompatible with Open Tree of Life queries

## Inputs

- metadata table (TSV format) with mandatory ATTRIBUTE_Species, ATTRIBUTE_Genus, ATTRIBUTE_Family columns in GNPS format
- species, genus, and family taxonomy strings (non-normalized, potentially obsolete or non-standard names)

## Outputs

- cleaned metadata TSV table with standardized taxonomy names
- OTOL_ID columns appended for species, genus, and family ranks
- mapping table linking original names to resolved names and OTOL_IDs

## How to apply

Extract the three taxonomy columns (species_column, genus_column, family_column) from your GNPS-format metadata table. For each unique taxon name at each rank, query the Open Tree of Life API to retrieve the current accepted name and corresponding Open Tree of Life identifier (OTOL_ID). Build a mapping table linking original names to resolved names and OTOL_IDs for all three ranks. Replace the original taxonomy strings in the metadata table with these resolved names and append new columns with OTOL_ID values for each rank. The cleaned metadata TSV must conform to GNPS format requirements (mandatory ATTRIBUTE_Species header with cleaned names) before being passed to INVENTA's Literature Component calculation, which depends on accurate taxon matching to Lotus Database records that use the NPClassifyre ontology.

## Related tools

- **Open Tree of Life API** (Query service for retrieving current accepted taxonomic names and OTOL identifiers for normalization) — https://opentree.readthedocs.io/en/latest/readme.html
- **INVENTA** (Downstream tool that consumes the cleaned metadata with normalized taxonomy to calculate Literature Component (LC) and prioritize natural extracts by novelty potential) — https://github.com/luigiquiros/inventa
- **Lotus Database** (Reference database with NPClassifyre ontology-indexed compound records queryable by normalized taxon names for Literature Component scoring)

## Evaluation signals

- All unique taxon names in original metadata are present in the mapping table with corresponding OTOL_IDs and resolved names
- Resolved taxonomy names conform to Open Tree of Life accepted nomenclature (validate by spot-checking against OTOL API directly)
- No null or empty OTOL_ID values in the final cleaned metadata table for any of the three ranks (species, genus, family)
- Cleaned metadata TSV maintains GNPS format compliance with mandatory ATTRIBUTE_Species header and no introduction of malformed or truncated rows
- Literature Component calculation on cleaned metadata produces non-zero LC scores for all samples, confirming successful taxon-to-Lotus Database linkage

## Limitations

- Open Tree of Life API may not have entries for all taxa, especially rare, newly described, or colloquial species names; such unmapped taxa will fail to retrieve OTOL_IDs and must be handled via manual curation or exclusion
- Normalization is one-directional and does not back-propagate corrections to the original quantification or feature tables; correcting taxonomy does not alter underlying MS2 spectral data or feature annotations
- The skill assumes taxonomy columns are correctly labeled and internally consistent (e.g., species name matches its genus and family); garbage input will produce garbage output regardless of OTOL API success
- Batch querying the Open Tree of Life API may encounter rate limits or network failures; large-scale projects may require asynchronous or local OTOL data mirroring

## Evidence

- [other] Taxonomy normalization is performed using the Open Tree of Life reference to convert sample taxonomy strings to currently recognized names, producing a cleaned taxonomy table required for Literature Component calculations.: "Taxonomy normalization is performed using the Open Tree of Life reference to convert sample taxonomy strings to currently recognized names"
- [other] For each unique taxon name in each taxonomic rank, query the Open Tree of Life API to retrieve the current accepted name and taxon Open Tree of Life identifier (OTOL_ID).: "For each unique taxon name in each taxonomic rank, query the Open Tree of Life API to retrieve the current accepted name and taxon Open Tree of Life identifier (OTOL_ID)"
- [other] Replace the original taxonomy strings in the metadata table with resolved names and append OTOL_ID columns for each rank.: "Replace the original taxonomy strings in the metadata table with resolved names and append OTOL_ID columns for each rank"
- [readme] The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life to do so (https://opentree.readthedocs.io/en/latest/readme.html).: "The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life to do so"
- [other] The Literature Component (LC) is a score based on the number of compounds reported in the literature for the taxon of a given extract. It is independent of the spectral data.: "The Literature Component (LC) is a score based on the number of compounds reported in the literature for the taxon of a given extract"
- [other] given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary: "given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary"
