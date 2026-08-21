---
name: annotation-table-construction
description: Use when when you have access to multiple public metabolomics databases
  and need to build a unified reference table for metabolite annotation in untargeted
  mass spectrometry analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - openNAU
  - MetaQC
  - MARC
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

# annotation-table-construction

## Summary

Construction of a reference metabolomics annotation table by integrating, standardizing, and deduplicating metabolite records from multiple public databases (HMDB, MassBank, METLIN). This skill produces a indexed, validated reference resource for metabolite identification in untargeted metabolomics workflows.

## When to use

When you have access to multiple public metabolomics databases and need to build a unified reference table for metabolite annotation in untargeted mass spectrometry analysis. Apply this skill at the outset of an openNAU analysis pipeline when raw metabolomics ion peaks require matching against known metabolites.

## When NOT to use

- Input metabolite data is already in a single standardized reference database (e.g., already merged HMDB-only records)
- Workflow requires organism-specific or pathway-curated annotations beyond generic metabolite matching
- Your analysis uses only targeted metabolomics with pre-defined metabolite lists rather than untargeted discovery

## Inputs

- Public metabolomics database records (HMDB, MassBank, METLIN)
- Metabolite records with molecular identifiers and mass spectral data
- Chemical properties (molecular formula, InChI, InChIKey, m/z)

## Outputs

- Unified reference metabolomics annotation table
- Indexed reference database with standardized nomenclature
- Deduplicated metabolite records with validated metadata

## How to apply

First, identify and access source databases (HMDB, MassBank, METLIN) documented in openNAU. Extract metabolite records including molecular identifiers, chemical properties, and mass spectral signatures from each source. Standardize field names, data types, and nomenclature across all databases to ensure consistency. Perform deduplication by matching records on molecular formula, InChI, or InChIKey to eliminate redundant entries. Integrate the deduplicated records into a single reference table with indexed fields (e.g., InChIKey, m/z) for rapid querying during peak annotation. Finally, validate completeness and consistency by comparing merged record counts and key metadata fields against source database records to ensure no data loss during integration.

## Related tools

- **openNAU** (Complete analysis platform housing reference database construction, raw mass data extraction, and quality control for metabolomics annotation) — https://github.com/zjuRong/openNAU
- **MetaQC** (Component of openNAU for quality control in metabolomics data processing) — https://github.com/zjuRong/openNAU
- **MARC** (Component of openNAU for metabolite annotation and reference matching) — https://github.com/zjuRong/openNAU

## Evaluation signals

- Merged record count matches or exceeds sum of individual database records minus expected duplicates
- Standardized field names are consistent across all rows; no NULL values in indexed query fields (InChI, InChIKey, molecular formula)
- Deduplication validation: InChIKey matching correctly identifies and removes redundant entries; no duplicate InChIKeys remain in final table
- Indexed fields enable sub-100ms query response for metabolite lookup by m/z (mass accuracy ≤ 5 ppm tolerance per openNAU specification)
- Metadata completeness check: key fields (molecular identifier, chemical properties, mass spectral signature) are present for ≥95% of records

## Limitations

- Deduplication relies on InChI/InChIKey availability; metabolites missing these identifiers may not be deduplicated and may appear as redundant entries
- Integration of heterogeneous databases may introduce inconsistencies in nomenclature or annotation standards that are only partially resolved by standardization
- No explicit handling of isobaric compounds or isomers that share molecular formula or InChI but differ in structure; queries may return false-positive matches
- Public source databases evolve; merged reference tables become stale if source databases are not re-harvested periodically

## Evidence

- [other] Public database sources and deduplication logic: "Identify and access public metabolomics databases (e.g., HMDB, MassBank, METLIN) referenced in openNAU documentation. Extract metabolite records including molecular identifiers, chemical properties,"
- [other] Integration and validation workflow: "Integrate deduplicated records into a single reference table with indexed fields for rapid querying. Validate completeness and consistency of the merged database against source record counts and key"
- [readme] Reference database construction as core openNAU capability: "A reference metabolomics database based on public databases was also constructed."
- [readme] Complete analysis system integration: "Finally, a complete analysis system platform for untargeted metabolomics was established."
