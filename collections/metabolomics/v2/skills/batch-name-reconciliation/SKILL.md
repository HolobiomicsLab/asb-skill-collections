---
name: batch-name-reconciliation
description: Use when when you have a metadata table with taxonomic annotations (species, genus, family columns) that may contain outdated, misspelled, or non-canonical taxon names, and you need to integrate these samples into a natural products analysis pipeline that requires standardized taxonomy (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3678
  - http://edamontology.org/topic_0637
  tools:
  - Open Tree of Life
  - INVENTA
  - Lotus Database
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

# batch-name-reconciliation

## Summary

Reconcile taxonomic names in bulk against a reference ontology (Open Tree of Life) to normalize species, genus, and family strings to currently accepted names and identifiers. This enables standardized cross-referencing with literature databases and downstream chemical annotation pipelines.

## When to use

When you have a metadata table with taxonomic annotations (species, genus, family columns) that may contain outdated, misspelled, or non-canonical taxon names, and you need to integrate these samples into a natural products analysis pipeline that requires standardized taxonomy (e.g., for Literature Component scoring in INVENTA or comparison against the Lotus Database). Use this skill before any downstream literature-based or taxonomy-aware chemical annotation steps.

## When NOT to use

- Taxonomy is already verified against Open Tree of Life and OTOL_IDs are already present in the metadata.
- Analysis does not require integration with literature databases or taxonomy-aware chemical scoring (e.g., pure spectral networking without Literature Component).
- Taxonomic resolution is not available in Open Tree of Life (e.g., very new or environmental isolate names).

## Inputs

- metadata table in TSV format with ATTRIBUTE_Species, ATTRIBUTE_Genus, and ATTRIBUTE_Family columns
- list or set of unique taxon names per rank to be reconciled

## Outputs

- cleaned metadata TSV table with resolved species, genus, and family names
- appended OTOL_ID columns for species, genus, and family ranks
- mapping table linking original names to resolved names and OTOL_IDs

## How to apply

Load the metadata table (TSV format) and extract the three columns designated as species_column, genus_column, and family_column. For each unique taxon name within each taxonomic rank, query the Open Tree of Life API to retrieve the current accepted name and the corresponding Open Tree of Life identifier (OTOL_ID). Construct a mapping table that links original names to resolved names and OTOL_IDs for all three ranks. Replace the original taxonomy strings in the metadata table with the resolved names and append new OTOL_ID columns for each rank. The output is a cleaned metadata TSV table with standardized taxonomy and OTOL_ID fields, ready for use in Literature Component calculations and cross-referencing with the Lotus Database (which uses the NPClassifyre ontology).

## Related tools

- **Open Tree of Life** (API reference for querying and retrieving current accepted taxon names and OTOL_IDs for reconciliation) — https://opentree.readthedocs.io/en/latest/readme.html
- **INVENTA** (Downstream pipeline that consumes cleaned taxonomy to compute Literature Component scores) — https://github.com/luigiquiros/inventa
- **Lotus Database** (Reference database for natural product compounds indexed by standardized taxonomy and NPClassifyre ontology)

## Evaluation signals

- All unique taxon names per rank are present in the output mapping table with 1:1 correspondence to resolved names.
- Every row in the cleaned metadata table has a corresponding OTOL_ID value (no null/missing OTOL_IDs for successfully reconciled taxa).
- Resolved names match currently accepted taxonomic nomenclature as verified against Open Tree of Life (spot-check against online OTOL browser or API).
- No duplicate or conflicting mappings for the same original taxon name (i.e., the mapping is deterministic).
- Cleaned metadata can be successfully loaded and parsed by downstream components (e.g., INVENTA's Literature Component calculation) without schema errors.

## Limitations

- Taxa not present in the Open Tree of Life reference (e.g., very recently described species, non-binomial environmental isolates) cannot be reconciled and will result in null or unmapped entries.
- Ambiguous or misspelled names may not be resolved; manual curation or fuzzy matching may be required for such cases.
- The API query rate or response latency may become a bottleneck for very large taxonomic datasets (thousands of unique taxa).
- Taxonomy is updated regularly in Open Tree of Life; reconciliation performed at different time points may yield slightly different OTOL_IDs if the reference taxonomy is revised.

## Evidence

- [other] For each unique taxon name in each taxonomic rank, query the Open Tree of Life API to retrieve the current accepted name and taxon Open Tree of Life identifier (OTOL_ID).: "For each unique taxon name in each taxonomic rank, query the Open Tree of Life API to retrieve the current accepted name and taxon Open Tree of Life identifier (OTOL_ID)."
- [other] The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life to do so.: "The species should be cleaned to up-to-day recognized names, you can use the Open Tree of Life to do so."
- [other] Taxonomy normalization is performed using the Open Tree of Life reference to convert sample taxonomy strings to currently recognized names, producing a cleaned taxonomy table required for Literature Component calculations.: "Taxonomy normalization is performed using the Open Tree of Life reference to convert sample taxonomy strings to currently recognized names, producing a cleaned taxonomy table required for Literature"
- [other] Replace the original taxonomy strings in the metadata table with resolved names and append OTOL_ID columns for each rank.: "Replace the original taxonomy strings in the metadata table with resolved names and append OTOL_ID columns for each rank."
- [other] given that the Lotus Dabase uses the NPClassifyre ontology and Sirius uses the Classifyre ontology, performing this step is absolutley necesary: "given that the Lotus Database uses the NPClassifyre ontology, performing this step is absolutely necessary for cross-referencing"
