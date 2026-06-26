---
name: conditional-allocation-design-patterns
description: 'Use when when designing a dataset storage layer that must handle variable
  dataset sizes, block layouts, and platform-specific constraints (e.g., Windows vs.
  non-Windows). Specifically: (1) you have parsed dataset metadata including cache-file
  flags, total point counts, and block configuration;'
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

# conditional-allocation-design-patterns

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A design pattern for selecting among multiple storage-backend implementations (e.g., SubMatrixFile, BigMappedMatrixFile, MappedSubMatrixFile, MappedMatrixFile) based on dataset metadata and memory constraints. This skill applies conditional logic to choose the optimal file-storage strategy for NMR spectroscopic datasets, balancing memory efficiency, access patterns, and I/O performance.

## When to use

When designing a dataset storage layer that must handle variable dataset sizes, block layouts, and platform-specific constraints (e.g., Windows vs. non-Windows). Specifically: (1) you have parsed dataset metadata including cache-file flags, total point counts, and block configuration; (2) you need to decide which DatasetStorageInterface implementation to instantiate; and (3) you must trade off between memory-mapped access, tiled/sub-matrix access, and fallback linear access based on dataset footprint and layout topology.

## When NOT to use

- When dataset storage backend is already instantiated or frozen by upstream configuration; this skill applies only at allocation/instantiation time.
- When the dataset is memory-resident or uses a non-file-based storage abstraction (e.g., in-memory columnar or distributed cache); conditional file-backend selection is not applicable.
- When platform-specific optimizations (e.g., Windows cache-file handling) are not supported or relevant to your deployment environment.

## Inputs

- Dataset metadata object (cache-file flag, total point count, block layout configuration)
- Platform identifier (Windows vs. non-Windows)
- DatasetStorageInterface implementation registry or factory

## Outputs

- Selected DatasetStorageInterface implementation instance (SubMatrixFile, BigMappedMatrixFile, MappedSubMatrixFile, or MappedMatrixFile)
- Selection rationale documentation (comments on criteria and trade-offs)

## How to apply

Parse dataset metadata to extract three key attributes: cache-file flag, total number of points (convertible to bytes), and block layout configuration (single vs. multiple blocks). Apply a cascading conditional selection: (1) If cache-file flag is enabled and platform is Windows, select SubMatrixFile for Windows-optimized processing. (2) Else if total points converted to bytes exceeds Integer.MAX_VALUE / 2, select BigMappedMatrixFile to enable memory-mapped access to large datasets without heap overflow. (3) Else if layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile for efficient tiled block-level access. (4) Otherwise, for single-block layouts, select MappedMatrixFile as the default. Document each selection criterion and include comments on performance trade-offs—particularly between MappedSubMatrixFile (finer-grained block access) and MappedMatrixFile (simpler linear memory mapping)—to guide future maintenance and optimization.

## Related tools

- **NMRFx** (Host framework providing Dataset.createDataFile() API and DatasetStorageInterface implementations for NMR data; this skill encapsulates the selection logic within NMRFx's storage-backend initialization.) — https://github.com/nanalysis/nmrfx

## Evaluation signals

- Verify correct implementation type is instantiated: inspect the class name of the returned object and confirm it matches the expected selection rule (e.g., BigMappedMatrixFile if byte-size exceeds Integer.MAX_VALUE / 2).
- Confirm metadata parsing is accurate: validate that cache-file flag, total points, and block layout count are correctly extracted before decision logic is applied.
- Check that selection decision is deterministic and reproducible: re-run allocation with identical metadata and confirm the same implementation is selected.
- Verify performance characteristics match expectation: for multi-block layouts, confirm MappedSubMatrixFile is selected and that block-level access is efficient; for single-block, confirm MappedMatrixFile is the fallback.
- Validate that platform-specific logic is respected: on Windows with cache-file enabled, confirm SubMatrixFile is selected; on other platforms or with cache-file disabled, confirm it is not.

## Limitations

- The Integer.MAX_VALUE / 2 threshold is a heuristic based on heap size assumptions and may not be optimal for all JVM configurations or platform memory layouts; tuning may be required for specific deployments.
- Selection does not account for runtime I/O patterns (sequential vs. random access); a dataset that fits the BigMappedMatrixFile threshold but is accessed sequentially may benefit from a different backend.
- Windows-specific SubMatrixFile selection is conditional on both the cache-file flag and platform detection; misconfiguration of either can lead to suboptimal backend choice.
- The workflow assumes block layout metadata is complete and accurately reflects the true data organization; corrupted or incomplete metadata will lead to incorrect allocation decisions.

## Evidence

- [other] Parse the dataset metadata to extract cache-file flag, total number of points, and block layout configuration.: "Parse the dataset metadata to extract cache-file flag, total number of points, and block layout configuration."
- [other] Select SubMatrixFile if cache file is enabled (Windows processing context).: "Implement conditional logic to select SubMatrixFile if cache file is enabled (Windows processing context)."
- [other] If total points converted to bytes exceeds Integer.MAX_VALUE / 2, select BigMappedMatrixFile for memory-mapped access to large datasets.: "Otherwise, if total points converted to bytes exceeds Integer.MAX_VALUE / 2, select BigMappedMatrixFile for memory-mapped access to large datasets."
- [other] If layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile for efficient tiled access.: "If layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile for efficient tiled access."
- [other] Document selection criteria and add comments addressing the performance trade-offs between MappedSubMatrixFile and MappedMatrixFile for single-block cases.: "Document selection criteria and add comments addressing the performance trade-offs between MappedSubMatrixFile and MappedMatrixFile for single-block cases."
