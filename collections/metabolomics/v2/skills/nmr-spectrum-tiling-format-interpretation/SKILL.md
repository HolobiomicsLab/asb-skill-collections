---
name: nmr-spectrum-tiling-format-interpretation
description: 'Use when when loading or creating an NMR spectral dataset (Dataset.createDataFile)
  and the system must decide between multiple storage backends (SubMatrixFile, BigMappedMatrixFile,
  MappedSubMatrixFile, MappedMatrixFile). Triggers include: (1) dataset metadata specifies
  a cache-file flag;'
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

# nmr-spectrum-tiling-format-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpret and select appropriate storage backends for NMR spectral datasets based on tiling layout, cache configuration, and memory constraints. This skill ensures efficient memory-mapped file access by matching dataset characteristics to the optimal DatasetStorageInterface implementation.

## When to use

When loading or creating an NMR spectral dataset (Dataset.createDataFile) and the system must decide between multiple storage backends (SubMatrixFile, BigMappedMatrixFile, MappedSubMatrixFile, MappedMatrixFile). Triggers include: (1) dataset metadata specifies a cache-file flag; (2) total spectral points, when converted to bytes, exceed Integer.MAX_VALUE / 2; (3) block layout defines multiple sub-matrices (tiled access pattern); or (4) single-block monolithic layout is detected.

## When NOT to use

- Dataset is already loaded in memory or pre-cached; storage backend selection applies only to new file creation or loading from disk.
- NMR data is already in a non-spectral format (e.g., processed peak lists, metabolite concentrations); this skill targets raw or processed time-domain/frequency-domain spectral matrices.
- Block layout and total point count metadata are unavailable or unreliable; the selection logic depends on accurate metadata parsing.

## Inputs

- Dataset metadata object (cache-file flag, total point count, block layout configuration)
- Spectral point count (integer, may be very large)
- Block layout descriptor (e.g., number of blocks, dimensions per block)
- Platform context (e.g., Windows, Linux/Unix)

## Outputs

- Selected DatasetStorageInterface implementation class (SubMatrixFile | BigMappedMatrixFile | MappedSubMatrixFile | MappedMatrixFile)
- Rationale documentation (selection decision tree with criteria met)
- File handle or memory-mapped buffer reference to the chosen backend

## How to apply

Parse dataset metadata to extract the cache-file flag, total number of spectral points, and block layout configuration. Apply conditional selection logic in this order: (1) If cache-file flag is enabled in a Windows processing context, select SubMatrixFile for platform-optimized access. (2) If total points × bytes-per-point ≥ Integer.MAX_VALUE / 2, select BigMappedMatrixFile to enable memory-mapped access for large datasets and avoid heap overflow. (3) If block layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile for efficient tiled access with per-block memory mapping. (4) Otherwise, for single-block layouts, select MappedMatrixFile as the default fallback. Document selection criteria and performance trade-offs, especially between MappedSubMatrixFile and MappedMatrixFile for boundary cases near the single/multi-block threshold.

## Related tools

- **NMRFx** (NMR processing and analysis platform providing Dataset class, DatasetStorageInterface implementations, and file I/O backends for spectral data) — https://github.com/nanalysis/nmrfx

## Evaluation signals

- Verify that the selected storage backend matches the decision tree output: check that SubMatrixFile is chosen only when cache-file flag is true on Windows; BigMappedMatrixFile is chosen when point count × bytes ≥ Integer.MAX_VALUE / 2; MappedSubMatrixFile is chosen for multi-block layouts; MappedMatrixFile is chosen for single-block.
- Confirm that memory-mapped file descriptors or buffer handles are successfully created for the chosen backend without heap overflow or out-of-memory exceptions.
- Validate that spectral data can be read/written through the selected backend with correct data alignment and block-wise access patterns (especially for MappedSubMatrixFile with tiled layouts).
- Check that the selection rationale documentation accurately reflects which criteria were evaluated and which threshold (if any) was crossed to trigger the backend choice.
- Monitor read/write performance metrics: MappedSubMatrixFile should show efficient per-block page faults for multi-block datasets; BigMappedMatrixFile should handle datasets exceeding 2 GB without memory errors.

## Limitations

- Selection logic assumes Integer.MAX_VALUE / 2 as the heap-safety threshold; actual JVM heap configuration may differ, requiring platform-specific tuning.
- Performance trade-offs between MappedSubMatrixFile and MappedMatrixFile for single-block layouts are mentioned but not quantified; empirical benchmarking may be needed for boundary cases.
- Windows-specific optimization (SubMatrixFile cache) assumes platform detection is reliable; cross-platform testing is required to validate platform context accuracy.
- Block layout metadata must be complete and accurate; malformed or missing layout descriptors will cause incorrect backend selection.

## Evidence

- [other] Implement conditional logic to select SubMatrixFile if cache file is enabled (Windows processing context). Otherwise, if total points converted to bytes exceeds Integer.MAX_VALUE / 2, select BigMappedMatrixFile for memory-mapped access to large datasets.: "Implement conditional logic to select SubMatrixFile if cache file is enabled (Windows processing context). Otherwise, if total points converted to bytes exceeds Integer.MAX_VALUE / 2, select"
- [other] If layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile for efficient tiled access. Fallback to MappedMatrixFile for single-block layouts.: "If layout defines multiple blocks (sub-matrix case), select MappedSubMatrixFile for efficient tiled access. Fallback to MappedMatrixFile for single-block layouts."
- [other] Document selection criteria and add comments addressing the performance trade-offs between MappedSubMatrixFile and MappedMatrixFile for single-block cases.: "Document selection criteria and add comments addressing the performance trade-offs between MappedSubMatrixFile and MappedMatrixFile for single-block cases."
