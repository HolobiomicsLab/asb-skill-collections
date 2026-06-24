---
name: memory-mapped-file-selection-strategy
description: Use when initializing a Dataset object in NMRFx and must decide which
  storage backend to use for in-memory or memory-mapped file access.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - NMRFx
  techniques:
  - NMR
  license_tier: restricted
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

# memory-mapped-file-selection-strategy

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A decision-tree method for selecting the optimal storage backend implementation (SubMatrixFile, BigMappedMatrixFile, MappedSubMatrixFile, or MappedMatrixFile) for Dataset.createDataFile() based on cache flags, dataset size, and block layout. This skill optimizes memory efficiency and access patterns for large NMR datasets in NMRFx.

## When to use

Apply this skill when initializing a Dataset object in NMRFx and must decide which storage backend to use for in-memory or memory-mapped file access. Key trigger: you have parsed dataset metadata (cache-file flag, total point count, block layout configuration) and need to route file creation to the appropriate implementation to balance memory footprint against access performance for datasets that may exceed available heap space.

## When NOT to use

- Input dataset is already loaded in memory and does not require file-backed storage
- Dataset size is small (total bytes < Integer.MAX_VALUE / 2) and single-block layout is confirmed — simpler file I/O methods may be more appropriate
- Processing context is not Windows and cache-file flag is irrelevant to your use case

## Inputs

- dataset metadata object (cache-file flag, total point count, block layout configuration)
- dataset size in bytes
- processing context (Windows vs. other platforms)

## Outputs

- DatasetStorageInterface implementation instance (one of: SubMatrixFile, BigMappedMatrixFile, MappedSubMatrixFile, MappedMatrixFile)
- selection decision with documented rationale

## How to apply

Extract three parameters from dataset metadata: (1) cache-file flag status; (2) total dataset size in bytes; (3) block layout structure (single-block vs. multi-block/tiled). Apply the selection logic in sequence: First, if cache-file flag is enabled and the processing context is Windows, select SubMatrixFile for platform-specific optimized caching. Second, compute total-points × bytes-per-point; if this exceeds Integer.MAX_VALUE / 2 (~1 GB), select BigMappedMatrixFile to enable memory-mapped access for datasets too large for heap allocation. Third, if the block layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile to exploit efficient tiled access patterns. Finally, default to MappedMatrixFile for single-block layouts. Document the selection decision and rationale in code comments, noting the performance trade-offs between MappedSubMatrixFile (efficient for multi-block) and MappedMatrixFile (simpler but potentially slower for tiled datasets).

## Related tools

- **NMRFx** (Framework providing Dataset class, DatasetStorageInterface implementations (SubMatrixFile, BigMappedMatrixFile, MappedSubMatrixFile, MappedMatrixFile), and createDataFile() factory method) — https://github.com/nanalysis/nmrfx

## Evaluation signals

- Verify that the selected storage backend matches the decision tree: SubMatrixFile only when cache-file flag is true on Windows; BigMappedMatrixFile when dataset size exceeds Integer.MAX_VALUE / 2; MappedSubMatrixFile when block count > 1; MappedMatrixFile as fallback.
- Confirm that the chosen implementation is instantiated and returned by Dataset.createDataFile() without throwing an exception.
- Validate that memory usage remains within expected bounds: memory-mapped implementations should not allocate the full dataset into heap, while single-block MappedMatrixFile should handle typical single-block layouts efficiently.
- Check that code comments document the selection rationale and note performance trade-offs between MappedSubMatrixFile and MappedMatrixFile for the specific layout type.
- For multi-block datasets, verify that MappedSubMatrixFile is chosen and that tiled access patterns perform better than single-mapped-file access in profiling benchmarks.

## Limitations

- Selection logic is tied to Integer.MAX_VALUE / 2 threshold; datasets near this boundary may exhibit unpredictable performance transitions.
- Windows-specific optimization for SubMatrixFile assumes platform-specific caching benefits; actual performance gain is platform-dependent and may not materialize on all Windows configurations.
- Multi-block detection relies on block layout metadata; if metadata is corrupt or missing, fallback to MappedMatrixFile may not be optimal.
- No adaptive re-selection once a backend is instantiated; if dataset properties change at runtime, the initially selected backend may become suboptimal.

## Evidence

- [other] Parse the dataset metadata to extract cache-file flag, total number of points, and block layout configuration.: "Parse the dataset metadata to extract cache-file flag, total number of points, and block layout configuration."
- [other] Implement conditional logic to select SubMatrixFile if cache file is enabled (Windows processing context).: "Implement conditional logic to select SubMatrixFile if cache file is enabled (Windows processing context)."
- [other] Otherwise, if total points converted to bytes exceeds Integer.MAX_VALUE / 2, select BigMappedMatrixFile for memory-mapped access to large datasets.: "Otherwise, if total points converted to bytes exceeds Integer.MAX_VALUE / 2, select BigMappedMatrixFile for memory-mapped access to large datasets."
- [other] If layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile for efficient tiled access.: "If layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile for efficient tiled access."
- [other] Document selection criteria and add comments addressing the performance trade-offs between MappedSubMatrixFile and MappedMatrixFile for single-block cases.: "Document selection criteria and add comments addressing the performance trade-offs between MappedSubMatrixFile and MappedMatrixFile for single-block cases."
