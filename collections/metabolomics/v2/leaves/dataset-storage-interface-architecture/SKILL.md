---
name: dataset-storage-interface-architecture
description: Use when you have NMR dataset metadata (cache-file flag, total point
  count, block layout configuration) and need to select an appropriate storage backend
  that balances memory efficiency, access patterns, and platform-specific constraints.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - NMRFx
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s42004-025-01812-8
  title: NMRFx
evidence_spans:
- github.com__nanalysis__nmrfx
- github.com/nanalysis/nmrfx
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmrfx_cq
    doi: 10.1038/s42004-025-01812-8
    title: NMRFx
  dedup_kept_from: coll_nmrfx_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42004-025-01812-8
  all_source_dois:
  - 10.1038/s42004-025-01812-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dataset-storage-interface-architecture

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A conditional selection strategy for choosing among multiple storage backend implementations (SubMatrixFile, BigMappedMatrixFile, MappedSubMatrixFile, MappedMatrixFile) based on dataset metadata, memory constraints, and block layout configuration. This skill optimizes memory-mapped file access and cache performance for large NMR datasets.

## When to use

Apply this skill when you have NMR dataset metadata (cache-file flag, total point count, block layout configuration) and need to select an appropriate storage backend that balances memory efficiency, access patterns, and platform-specific constraints. Use it specifically when dataset size exceeds available heap memory or when multi-block (tiled) layouts are present.

## When NOT to use

- Dataset size is small enough to fit entirely in heap memory and single-block layout applies — use direct in-memory storage instead
- Storage backend is externally mandated by downstream API contract or immutable configuration

## Inputs

- Dataset metadata object (containing cache-file flag, total point count, block layout configuration)
- System platform identifier (Windows vs. other)
- Memory availability constraints

## Outputs

- Selected DatasetStorageInterface implementation class (SubMatrixFile, BigMappedMatrixFile, MappedSubMatrixFile, or MappedMatrixFile)
- Selection justification and performance rationale

## How to apply

First, parse the dataset metadata to extract the cache-file flag, total number of points, and block layout configuration. Then apply conditional logic in sequence: (1) if cache file is enabled in a Windows processing context, select SubMatrixFile; (2) if total points converted to bytes exceeds Integer.MAX_VALUE / 2, select BigMappedMatrixFile to enable memory-mapped access; (3) if layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile for efficient tiled access; (4) otherwise, fallback to MappedMatrixFile for single-block layouts. Document the selection criteria and rationale, especially the performance trade-offs between MappedSubMatrixFile and MappedMatrixFile for borderline single-block cases.

## Related tools

- **NMRFx** (NMR data processing and visualization platform in which Dataset.createDataFile() storage-backend selection logic is embedded) — https://github.com/nanalysis/nmrfx

## Evaluation signals

- Verify that selected storage class matches the decision tree: SubMatrixFile only when cache flag + Windows, BigMappedMatrixFile only when byte count > Integer.MAX_VALUE / 2, MappedSubMatrixFile only when multiple blocks are present, MappedMatrixFile as fallback
- Confirm that memory-mapped implementations (BigMappedMatrixFile, MappedSubMatrixFile, MappedMatrixFile) are chosen for datasets exceeding heap limits
- Check that single-block layouts never select MappedSubMatrixFile (confirm block count == 1 before fallback decision)
- Validate that platform-specific path (SubMatrixFile for Windows cache mode) is taken only when both conditions hold
- Review generated documentation comments address stated performance trade-offs, especially rationale for MappedSubMatrixFile vs. MappedMatrixFile boundary

## Limitations

- Selection logic depends on accurate metadata parsing; malformed or incomplete cache-file flag, point count, or block layout will trigger fallback (MappedMatrixFile) regardless of actual dataset size
- Integer.MAX_VALUE / 2 threshold is architecture-dependent; 32-bit systems may require different thresholds than 64-bit platforms
- Windows-specific SubMatrixFile path assumes cache file is pre-allocated and accessible; failure to stage cache file will degrade performance
- No dynamic re-selection once DatasetStorageInterface is instantiated; suboptimal choice (e.g., MappedMatrixFile for a multi-block layout) persists for the dataset's lifetime

## Evidence

- [other] Parse the dataset metadata to extract cache-file flag, total number of points, and block layout configuration.: "Parse the dataset metadata to extract cache-file flag, total number of points, and block layout configuration."
- [other] Implement conditional logic to select SubMatrixFile if cache file is enabled (Windows processing context).: "Implement conditional logic to select SubMatrixFile if cache file is enabled (Windows processing context)."
- [other] If total points converted to bytes exceeds Integer.MAX_VALUE / 2, select BigMappedMatrixFile for memory-mapped access to large datasets.: "If total points converted to bytes exceeds Integer.MAX_VALUE / 2, select BigMappedMatrixFile for memory-mapped access to large datasets."
- [other] If layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile for efficient tiled access.: "If layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile for efficient tiled access."
- [other] Fallback to MappedMatrixFile for single-block layouts.: "Fallback to MappedMatrixFile for single-block layouts."
