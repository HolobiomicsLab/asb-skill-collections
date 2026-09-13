---
name: metabolite-database-integration
description: Use when you need to construct a reference metabolomics database from
  scratch or when existing public databases (HMDB, MassBank, METLIN) need to be merged
  into a single queryable resource for metabolite annotation in untargeted mass spectrometry
  analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3172
  tools:
  - openNAU
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.21147/j.issn.1000-9604.2023.05.11
  title: OpenNAU
evidence_spans:
- An open-source analysis software for untargeted metabolism data (openNAU) was constructed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_opennau_cq
    doi: 10.21147/j.issn.1000-9604.2023.05.11
    title: OpenNAU
  dedup_kept_from: coll_opennau_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21147/j.issn.1000-9604.2023.05.11
  all_source_dois:
  - 10.21147/j.issn.1000-9604.2023.05.11
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-database-integration

## Summary

Assembles a unified reference metabolomics database by extracting, standardizing, and deduplicating records from multiple public metabolomics databases (HMDB, MassBank, METLIN). This skill produces a consolidated, indexed resource for rapid querying of metabolite identifiers, chemical properties, and mass spectral signatures in untargeted metabolomics workflows.

## When to use

Apply this skill when you need to construct a reference metabolomics database from scratch or when existing public databases (HMDB, MassBank, METLIN) need to be merged into a single queryable resource for metabolite annotation in untargeted mass spectrometry analysis. Use it when redundant records across source databases risk creating duplicate matches during metabolite identification.

## When NOT to use

- You already have a validated, curated reference metabolomics database (e.g., commercial or institution-specific) and do not need to merge public sources.
- Your analysis requires only a small, manually curated subset of metabolites rather than comprehensive database integration.
- You are performing targeted metabolomics where metabolite identities are known in advance and do not require database matching.

## Inputs

- Public metabolomics database records (HMDB, MassBank, METLIN) in their native or downloaded format
- Metabolite identifiers (molecular formula, InChI, InChIKey, mass-to-charge ratio)
- Chemical properties and mass spectral signatures from each source database

## Outputs

- Unified reference metabolomics database (single indexed table or document store)
- Deduplicated metabolite records with consolidated metadata
- Index structures optimized for rapid querying by molecular identifier or mass

## How to apply

First, identify and programmatically access public metabolomics databases (HMDB, MassBank, METLIN) via their APIs or bulk download endpoints, extracting metabolite records with molecular identifiers (InChI, InChIKey), chemical properties, and mass spectral signatures. Standardize field names, data types, and chemical nomenclature across all source databases to ensure consistent schema. Perform deduplication by matching records on molecular formula, InChI, or InChIKey to identify and remove redundant entries. Integrate the deduplicated records into a single indexed reference table with optimized key fields (e.g., InChIKey, mass-to-charge ratio) for rapid querying. Finally, validate completeness and consistency of the merged database by comparing total record counts, verifying key metadata fields are populated, and spot-checking matched records against source databases.

## Related tools

- **openNAU** (Framework for constructing reference metabolomics database and performing untargeted metabolomics analysis including raw mass data extraction and metabolite identification) — https://github.com/zjuRong/openNAU

## Evaluation signals

- Deduplicated record count matches expected total from source databases after accounting for overlaps (within 5–10% variance).
- All indexed fields (InChIKey, molecular formula, mass-to-charge ratio) are non-null across ≥95% of merged records.
- Spot-check: random sample of 50–100 deduplicated records can be traced back to source database entries with matching chemical properties.
- Query performance on indexed fields returns results in <100 ms for typical metabolite mass ranges (50–1000 m/z).
- Metadata field consistency verified: no truncation, encoding errors, or null values in critical fields (chemical name, molecular weight, mass spectral signatures).

## Limitations

- Deduplication relies on exact or fuzzy matching on molecular formula, InChI, or InChIKey; isomeric variants may not be resolved without additional structural validation.
- Public databases (HMDB, MassBank, METLIN) vary in annotation quality, coverage, and update frequency, which may propagate into the integrated database.
- Data standardization across heterogeneous sources is manual or semi-automated and may require domain expertise in chemical nomenclature and data schema design.
- Mass spectral signatures are instrument-dependent; merged records may require additional curation or normalization for consistent use across different MS platforms.

## Evidence

- [intro] Public database sources and merging approach: "Identify and access public metabolomics databases (e.g., HMDB, MassBank, METLIN) referenced in openNAU documentation."
- [intro] Deduplication method: "Perform deduplication by matching records on molecular formula, InChI, or InChIKey to remove redundant entries."
- [intro] Integration and indexing approach: "Integrate deduplicated records into a single reference table with indexed fields for rapid querying."
- [intro] Validation approach: "Validate completeness and consistency of the merged database against source record counts and key metadata fields."
- [readme] Database construction outcome in openNAU: "A reference metabolomics database based on public databases was also constructed."
