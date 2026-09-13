---
name: strain-identifier-mapping-across-genomics-metabolomics
description: Use when when preparing multiomics datasets for NPLinker that combine
  GNPS metabolomics, AntiSMASH genomics, and MIBiG reference data, and you need to
  establish which strain IDs or sample identifiers appear in both genomic and metabolomic
  experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - nplinker
  - Python
  - MIBiG
  - Dynaconf
  - GNPS
  - AntiSMASH
  - BigScape
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
evidence_spans:
- NPLinker is a python framework for data mining microbial natural products
- GNPSDownloader, GNPSExtractor
- Python version ≥3.11
- mibig directory contains the MIBiG metadata
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker_2_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# strain-identifier-mapping-across-genomics-metabolomics

## Summary

Validate and auto-generate strain identifier mappings that link genomic data (AntiSMASH BGCs, BigScape clusters) to metabolomic observations (GNPS molecular networking) within NPLinker's data preparation stage. This ensures consistent strain identity across heterogeneous omics datasets before downstream integration and link computation.

## When to use

When preparing multiomics datasets for NPLinker that combine GNPS metabolomics, AntiSMASH genomics, and MIBiG reference data, and you need to establish which strain IDs or sample identifiers appear in both genomic and metabolomic experiments. Use this skill to reconcile strain nomenclature before data loading and link scoring.

## When NOT to use

- Input GNPS data is already integrated with manually curated strain mappings that do not require validation or regeneration.
- Analysis uses only metabolomics (GNPS) data without genomic linkage or BGC information.
- Strain identity is irrelevant (e.g., single-strain or environment-wide screening without cross-experimental reconciliation).

## Inputs

- nplinker.toml configuration file (Dynaconf format) with root_dir, mode, and GNPS/AntiSMASH/BigScape paths
- GNPS molecular networking data (nodes, edges, metadata)
- AntiSMASH BGC directory containing antiSMASH-output subdirectories with region metadata
- BigScape data (mix_clustering_c*.tsv for v1, data_sqlite.db for v2, or both)
- MIBiG metadata directory
- strain_mappings.json (provided for local mode; auto-generated for PODP mode)
- strains_selected.json (optional, for strain filtering)

## Outputs

- Validated strain_mappings.json with consistent strain identifiers across GNPS, AntiSMASH, and BigScape
- Validated strains_selected.json (if provided)
- Arrangement of all input directories and configuration ready for DatasetLoader consumption
- Configuration error report (if validation fails)

## How to apply

Load the Dynaconf configuration file (nplinker.toml) specifying root_dir, mode (local or PODP), and paths to GNPS, AntiSMASH, and BigScape directories. For PODP mode, auto-generate strain_mappings.json by inferring strain associations from project metadata; for local mode, validate an existing strain_mappings.json against the discovered genomic and metabolomic data. Optionally validate a strains_selected.json file if filtering to a subset. Check that all strain identifiers referenced in GNPS molecular networking nodes have corresponding BGC or sample records in the AntiSMASH/BigScape output. Raise a configuration error if validation fails. Return a validated arrangement of strain mappings ready for DatasetLoader consumption, ensuring that link computation in later stages can correctly pair genomic BGCs with metabolomic features.

## Related tools

- **nplinker** (Orchestrates strain mapping validation and auto-generation as part of DatasetArranger data-preparation stage) — https://github.com/NPLinker/nplinker
- **Dynaconf** (Manages configuration file validation (nplinker.toml) including strain mapping settings and mode (local vs. PODP))
- **GNPS** (Provides metabolomic molecular networking data and strain/sample identifiers for cross-linking with genomic data) — https://gnps.ucsd.edu
- **AntiSMASH** (Provides genomic BGC predictions and strain/genome identifiers for mapping to metabolomic features)
- **BigScape** (Generates BGC clustering (v1 or v2 format) used to organize and reference genomic data in strain mappings)
- **MIBiG** (Reference database of biosynthetic gene clusters used to validate strain and BGC mappings)

## Examples

```
from nplinker import DatasetArranger; arr = DatasetArranger('nplinker.toml'); validated_config = arr.validate_and_arrange(); strain_map = validated_config.get('strain_mappings')
```

## Evaluation signals

- strain_mappings.json validates against schema: all required keys present, no null or duplicate strain IDs, no orphan references to non-existent GNPS nodes or BGC IDs
- Every strain identifier in GNPS molecular networking data has a corresponding entry in strain_mappings.json
- Every AntiSMASH-predicted BGC is traceable to a strain ID in the mapping; BigScape clustering references are consistent across v1 and v2 formats if both present
- strains_selected.json (if provided) contains only strain IDs that exist in validated strain_mappings.json
- No configuration errors raised during Dynaconf validation; PODP metadata JSON (if PODP mode) downloads and parses without errors

## Limitations

- Strain mapping relies on consistent naming conventions across GNPS, AntiSMASH, and provided metadata; inconsistent or missing strain identifiers will cause validation failure.
- PODP mode auto-generation infers strain associations from project metadata; manual curation may be needed for complex multi-strain or complex sample designs.
- BigScape v1 (mix_clustering_c*.tsv) and v2 (data_sqlite.db) formats are both supported but mixing or partial presence can complicate reconciliation.
- MIBiG data is always downloaded and replaced; local modifications are not preserved.

## Evidence

- [other] strain_mappings.json (auto-generate for podp mode; validate for local mode): "Validate strain_mappings.json (auto-generate for podp mode; validate for local mode)"
- [other] antismash directory contains a collection of AntiSMASH BGC data: "antismash directory contains a collection of AntiSMASH BGC data"
- [other] NPLinker requires GNPS molecular networking data as input: "NPLinker requires GNPS molecular networking data as input"
- [other] validated arrangement of all input directories and configuration ready for DatasetLoader consumption: "Return a validated arrangement of all input directories and configuration ready for DatasetLoader consumption."
- [other] NPLinker requires input data preparation including GNPS molecular networking data, antismash directory containing AntiSMASH BGC data, and mibig directory containing MIBiG metadata: "NPLinker requires input data preparation including GNPS molecular networking data, antismash directory containing AntiSMASH BGC data, and mibig directory containing MIBiG metadata"
