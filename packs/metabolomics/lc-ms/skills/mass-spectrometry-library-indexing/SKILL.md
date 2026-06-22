---
name: mass-spectrometry-library-indexing
description: Use when you have a large MS/MS experiment (mzML format) requiring lipid annotation and need to match experimental spectra against >10 million theoretical lipid fragments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - XCMS
  - CAMERA
  - RaMS
  - LipidIN Expeditious Querying (EQ) Module
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

# mass-spectrometry-library-indexing

## Summary

Build and query an indexed, hierarchical in-memory data structure of lipid fragmentation spectra to enable rapid spectral matching against massive libraries (>100M entries) at scale. This skill accelerates MS/MS lipid annotation by organizing theoretical and experimental spectra by chain composition and double-bond topology, then performing millions to billions of cosine-similarity or mass-error-tolerant fragment comparisons per second.

## When to use

You have a large MS/MS experiment (mzML format) requiring lipid annotation and need to match experimental spectra against >10 million theoretical lipid fragments. You are bottlenecked by spectral library query latency or have computational constraints (single machine, time-critical workflows). LipidIN's hierarchical indexing is particularly suited when your lipid space is combinatorially large (all chain compositions and double-bond isomers for a lipid class) but topologically structured.

## When NOT to use

- Your lipid library is small (<1 million entries) or unstructured: simpler in-memory lookup or database indexing (SQLite, PostgreSQL) will suffice with lower implementation overhead.
- Your MS/MS spectra are low-resolution or heavily noisy: hierarchical indexing assumes structured fragmentation patterns; polished, high-resolution spectra are required for accurate matching.
- You need real-time annotation in a streaming pipeline with very low latency (<10 ms per spectrum): the current implementation targets batch processing on standard CPUs.

## Inputs

- mzML file (raw mass spectrometry data in centroid or profile mode)
- hierarchical lipid fragmentation library (168.6 million entries, organized by chain composition and double-bond location; available as pos_ALL.rda or neg_ALL.rda)
- MS/MS spectral intensity matrix (after RaMS preprocessing, .rda format)
- ionization mode (ESI: 'p' for positive, 'n1' for [M+COOH]−, 'n2' for [M+CH3COO]−)

## Outputs

- ranked list of spectral matches (matched lipid ID, fragment m/z, cosine similarity or mass error scores)
- annotation table (CSV format with lipid annotation, precursor m/z, retention time, match score)
- query throughput metrics (queries/second, wall-clock execution time)

## How to apply

First, load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid spectral similarity lookup. Preprocess experimental MS/MS spectra from mzML files using RaMS and apply MS2 intensity filtering (MS2_filter parameter, typically 0.10–0.15× max intensity) to reduce noise. Implement spectral querying logic using cosine similarity or mass-error-tolerant fragment matching with MS1 and MS2 m/z tolerances (typically ppm1=5 ppm, ppm2=10 ppm for high-resolution instruments). Execute the expeditious querying (EQ) module as a C++-accelerated secondary matching pass against the hierarchical library, recording wall-clock time and query throughput. Validate that the system achieves approximately 70 billion queries in under 1 second on standardized benchmarks (13th Gen Intel Core i7-13700F, 64 GB RAM, Windows 11) before deploying to production annotation workflows.

## Related tools

- **XCMS** (Peak alignment, matching, and preprocessing of mass spectrometry data for metabolite profiling before spectral library querying)
- **CAMERA** (Compound spectra extraction and annotation of LC/MS datasets to group related peaks before library matching)
- **RaMS** (Fast in-memory parsing and preprocessing of mzML files with optional multithreading, converting raw spectra to .rda format for EQ module input)
- **LipidIN Expeditious Querying (EQ) Module** (C++-accelerated secondary spectral matching against the hierarchical lipid fragmentation library using cosine similarity or mass-error-tolerant fragment matching) — https://github.com/LinShuhaiLAB/LipidIN
- **Rcpp** (Interface between R preprocessing and C++ query engine for performance-critical matching loops)

## Examples

```
source(paste(getwd(),'/EQ.r',sep='')); EQ(filename='QC_POS1.rda', ppm1=5, ppm2=10, ESI='p')
```

## Evaluation signals

- Query throughput reaches ≥70 billion spectral queries in <1 second on standardized benchmark hardware (Intel Core i7-13700F, 64 GB RAM); actual measured time is recorded and compared to baseline.
- Matched lipid annotations show >94% accuracy (≤5.7% estimated false discovery rate) when validated against independent standards or orthogonal methods (e.g., retention time rules via LCI module).
- Memory footprint remains stable (~20–40 GB for full 168.6M entry library) and does not grow with the number of queries; no heap fragmentation or cache-miss spikes observed during sustained matching.
- Matched fragment m/z values fall within specified tolerance windows (ppm1 for MS1, ppm2 for MS2); all matches fail fast if any fragment violates the mass-error bound.
- Recall (coverage) improves by ≥20% after wide-spectrum fingerprint regeneration (WMYn module); unmatched spectra in the input set are reduced by the predicted yield.

## Limitations

- Library must be pre-indexed and loaded into memory; indexing time is not included in query throughput benchmarks. Data format conversion (mzML → .rda) takes ~2 minutes per sample, creating a warm-up cost.
- Accuracy depends on the completeness and quality of the underlying lipid fragmentation library; isomers with identical or near-identical MS/MS spectra may not be resolved by spectral matching alone (downstream LCI module required).
- Performance is optimized for modern CPUs (13th Gen Intel Core i7 or equivalent); older processors or embedded systems may not achieve 70 billion queries/second. Multithreading requires careful file locking in multi-task environments (fixed in LipidIN v4.0+, August 30, 2024).
- The module assumes high-resolution MS/MS data; low-resolution, unit-mass or nominal-mass spectra may have insufficient fragment-level detail for reliable cosine similarity calculations.
- ESI ionization mode must be explicitly specified and match the acquisition mode; mismatched ion mode (e.g., querying negative-mode data with positive-mode library) produces spurious high-scoring matches.

## Evidence

- [other] LipidIN implements an expeditious querying module that performs spectral matching against a 168.6 million lipid fragmentation hierarchical library, achieving throughput of approximately 70 billion spectral queries in less than 1 second.: "expeditious querying module that performs spectral matching against a 168.6 million lipid fragmentation hierarchical library, achieving throughput of approximately 70 billion spectral queries in less"
- [other] Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid spectral similarity lookup.: "Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid"
- [other] Implement spectral querying logic using cosine similarity or mass-error-tolerant fragment matching to compare experimental MS/MS spectra against library entries.: "spectral querying logic using cosine similarity or mass-error-tolerant fragment matching to compare experimental MS/MS spectra against library entries"
- [readme] All benchmark tests were performed on a personal computer with 13th Gen Intel® Core™ i7-13700F × 16- Core Processor, 64 GB memory, and installed with Windows11 operation system: "13th Gen Intel® Core™ i7-13700F × 16- Core Processor, 64 GB memory, and installed with Windows11 operation system"
- [readme] Resolved the prolonged processing time issue in the EQ module and fixed the accidental file deletion problem in the LCI module when running multiple files simultaneously.: "Resolved the prolonged processing time issue in the EQ module; Fixed the accidental file deletion problem in the LCI module when running multiple files simultaneously"
- [readme] data format conversion process for the LCI module takes approximately 2 minutes.: "data format conversion process for the LCI module takes approximately 2 minutes"
- [readme] MS2_filter: a value of 0-1, MS2 fragments with intensity lower than the MS2_filter*max intensity will be deleted: "MS2_filter: a value of 0-1, MS2 fragments with intensity lower than the MS2_filter*max intensity will be deleted"
