---
name: hierarchical-library-data-structure-design
description: Use when when building a reference library for high-throughput spectral matching against experimental MS/MS data, and you need to support millions to billions of queries per second on a standardized dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - XCMS
  - CAMERA
  - RaMS
  - Rcpp
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification.'
- 'CAMERA: an'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidin_cq
    doi: 10.1038/s41467-025-59683-5
    title: LipidIN
  dedup_kept_from: coll_lipidin_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-59683-5
  all_source_dois:
  - 10.1038/s41467-025-59683-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hierarchical-library-data-structure-design

## Summary

Design and index a multi-level hierarchical data structure for a large fragmentation library (e.g., 168.6 million lipid entries) to enable rapid spectral matching queries while organizing entries by biochemical attributes (chain composition, double-bond positions). This skill optimizes in-memory lookup performance for mass spectrometry annotation workflows.

## When to use

When building a reference library for high-throughput spectral matching against experimental MS/MS data, and you need to support millions to billions of queries per second on a standardized dataset. Apply this skill if your annotation bottleneck is library query latency and you have access to structured biochemical metadata (e.g., lipid chain lengths, saturation patterns) that can organize entries hierarchically.

## When NOT to use

- Input is an unstructured or flat list of spectra with no biochemical metadata for hierarchical organization.
- Query workload is small or sporadic (< millions of queries); a simple linear search or small hash table will suffice.
- Target hardware is memory-constrained (< 16 GB RAM); loading the full 168.6 million entry library may not be feasible.

## Inputs

- Fragmentation spectra (theoretical or real MS/MS library entries with m/z, intensity, and retention time metadata)
- Lipid structural metadata (chain composition, double-bond count and position, lipid class or subclass)
- Experimental MS/MS spectra (mzML format peak lists with precursor m/z and fragment m/z values)

## Outputs

- Indexed hierarchical library data structure (e.g., .rda or C++ indexed object in memory)
- Query throughput metrics (queries per second, wall-clock latency, memory footprint)
- Ranked spectral match results with normalized scores (cosine similarity or mass-error-tolerant match scores)

## How to apply

Organize the fragmentation library into a 4-level hierarchy based on biochemical properties: first partition by lipid class and chain composition, then by double-bond locations and stereoisomers, storing metadata for rapid m/z and fragment-pattern lookup. Load the indexed structure into an optimized in-memory data structure (e.g., indexed R data frames or C++ hash tables) that supports cosine-similarity or mass-error-tolerant fragment matching. Implement a query engine in C++ or compiled code to maximize throughput; benchmark wall-clock time and queries-per-second on standardized experimental spectra. Validate that the design achieves target query rates (e.g., ~70 billion queries/second on a 13th-gen Intel i7 with 64 GB RAM) and that matching results normalize and rank correctly by spectral similarity or match score.

## Related tools

- **XCMS** (Mass spectrometry data processing for peak alignment, matching, and identification prior to library querying)
- **CAMERA** (Compound spectra extraction and annotation from LC/MS datasets to prepare query spectra)
- **RaMS** (Data preprocessing to convert mzML format to indexed .rda format for fast library loading)
- **Rcpp** (C++ integration for accelerated query engine implementation and hierarchical indexing)

## Examples

```
load(paste(getwd(),'/MS1_MS2_library.rda',sep='')); source(paste(getwd(),'/EQ.r',sep='')); EQ(filename='QC_POS1.rda', ppm1=5, ppm2=10, ESI='p')
```

## Evaluation signals

- Query throughput meets or exceeds target rate (e.g., ~70 billion queries/second on benchmark dataset).
- Memory footprint is within available RAM; the indexed structure loads and queries without disk I/O delays.
- Spectral match results rank correctly by similarity metric (cosine similarity or mass error tolerance); no inverted or null rankings.
- Wall-clock latency for a standardized spectrum batch (e.g., 100 experimental spectra) is sub-linear with library size.
- Cross-validation: independently rebuild the hierarchy and verify identical match results and query times.

## Limitations

- Library size (168.6 million entries) requires substantial RAM (64 GB observed in benchmarks); scaling to larger organism panels may exceed typical workstation memory.
- Hierarchical organization is optimized for lipid-specific metadata (chain composition, double-bond position); generalization to other compound classes (e.g., peptides, natural products) requires redesign.
- Query performance is sensitive to indexing strategy and hardware (CPU cache, memory bandwidth); performance gains may not transfer to lower-specification machines.
- The 4-level hierarchy assumes a specific lipid nomenclature and taxonomy; changes to lipid class definitions or novel lipid types require library reconstruction.

## Evidence

- [intro] LipidIN implements an expeditious querying module that performs spectral matching against a 168.6 million lipid fragmentation hierarchical library, achieving throughput of approximately 70 billion spectral queries in less than 1 second.: "168.6 million lipid fragmentation hierarchical library, achieving throughput of approximately 70 billion spectral queries in less than 1 second"
- [intro] 168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations: "hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations"
- [other] Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid spectral similarity lookup.: "Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure"
- [readme] The system main development languages being R，python and C++. While R ,python handles backend processes and C++ accelerates the program.: "development languages being R, python and C++. While R, python handles backend processes and C++ accelerates the program"
- [readme] All benchmark tests were performed on a personal computer with 13th Gen Intel® Core™ i7-13700F × 16-Core Processor, 64 GB memory, and installed with Windows11 operation system: "13th Gen Intel® Core™ i7-13700F × 16-Core Processor, 64 GB memory, and installed with Windows11 operation system"
