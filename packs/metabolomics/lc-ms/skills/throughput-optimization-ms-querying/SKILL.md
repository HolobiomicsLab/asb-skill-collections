---
name: throughput-optimization-ms-querying
description: Use when you have experimental MS/MS spectra that must be matched against a large hierarchical fragmentation library (e.g., 168.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - XCMS
  - CAMERA
  - RaMS
  - LipidIN Expeditious Querying (EQ) Module
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# throughput-optimization-ms-querying

## Summary

Optimize mass spectrometry spectral querying throughput by loading large hierarchical lipid fragmentation libraries into indexed in-memory data structures and implementing mass-error-tolerant fragment matching. This skill is essential when processing high-volume MS/MS datasets and seeking to achieve billion-scale query rates against comprehensive lipid libraries in sub-second timeframes.

## When to use

Apply this skill when you have experimental MS/MS spectra that must be matched against a large hierarchical fragmentation library (e.g., 168.6 million entries) and query latency is a bottleneck—specifically when wall-clock time for annotation must remain under 1 second per spectrum batch, or when throughput targets exceed billions of queries.

## When NOT to use

- Input library is unstructured or not organized by compositional hierarchy (requires pre-indexing preprocessing)
- Spectral data is already fully annotated or you seek only metabolite class summary (not individual lipid identification)
- MS/MS spectra are sparse or low-quality (SNR<5), as matching accuracy will degrade and throughput optimization will not compensate for poor signal

## Inputs

- mzML-format mass spectrometry data files
- hierarchical lipid fragmentation library (168.6 million entries, indexed .rda format)
- preprocessed MS/MS spectra (m/z, intensity pairs) after XCMS/RaMS data preprocessing
- MS1 and MS2 mass tolerance parameters (ppm)

## Outputs

- Annotated spectral match results (CSV format) with lipid identifications and scoring metrics
- Query throughput metrics (queries/second, wall-clock time)
- Primary and secondary matching scores for each spectrum-library entry pair

## How to apply

Load the hierarchical lipid fragmentation library (organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid spectral similarity lookup. Implement spectral matching logic using cosine similarity or mass-error-tolerant fragment matching (with MS1 ppm tolerance typically 5–10 ppm and MS2 tolerance 10 ppm) to compare experimental spectra against library entries. Execute the query engine on standardized benchmark datasets and measure wall-clock time and query throughput (queries/second). The LipidIN expeditious querying (EQ) module achieves ~70 billion spectral queries in <1 second by combining greedy secondary matching algorithms with C++ acceleration for compute-intensive operations, while R and Python handle backend orchestration.

## Related tools

- **XCMS** (Upstream peak alignment, matching, and preprocessing of raw MS data for nonlinear retention-time correction and feature detection prior to spectral querying)
- **CAMERA** (Compound spectra extraction and annotation from LC/MS datasets to group related peaks before library matching)
- **RaMS** (Data preprocessing to convert mzML files into .rda format with multithread support for efficient memory-resident spectral representation)
- **LipidIN Expeditious Querying (EQ) Module** (Core C++-accelerated module executing mass-error-tolerant fragment matching and secondary scoring against indexed library) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
source('./EQ.r'); load('./MS1_MS2_library.rda'); EQ(filename='QC_POS1.rda', ppm1=5, ppm2=10, ESI='p')
```

## Evaluation signals

- Measured query throughput ≥70 billion queries/second on benchmark spectra (wall-clock time <1 second for full batch)
- No missing or truncated match results; all input spectra receive primary and secondary match scores
- Memory footprint remains constant with query volume (indexed structure scales linearly, not quadratically)
- Cosine similarity or fragment match scores for high-confidence hits fall within expected range (e.g., >0.7 for validated lipid matches)
- Downstream LCI module can rerank top candidates without latency degradation, confirming output scores are reproducible and stable across re-evaluation

## Limitations

- Throughput optimization assumes library is pre-indexed; unstructured libraries require manual hierarchical organization and indexing (8–30 min one-time cost)
- Greedy matching algorithms may miss isomeric lipids with near-identical fragmentation patterns; requires downstream Lipid Categories Intelligence (LCI) or relative retention time rules to reduce false positives (5.7% estimated FDR on 8923 lipids)
- C++ acceleration is compute-bound; performance depends on CPU cores and memory bandwidth (benchmarks run on 13th Gen Intel i7-13700F, 64 GB RAM; performance may degrade on resource-constrained systems)
- MS/MS spectra with low SNR or few major fragments may produce ambiguous matches; MS2_filter threshold (0.10× max intensity) should be tuned empirically per instrument and ionization mode
- Requires pre-trained library; custom lipid species or modifications not in the 168.6 million entry library will not be queried

## Evidence

- [other] Implement spectral querying logic using cosine similarity or mass-error-tolerant fragment matching to compare experimental MS/MS spectra against library entries.: "Implement spectral querying logic using cosine similarity or mass-error-tolerant fragment matching to compare experimental MS/MS spectra"
- [intro] LipidIN implements an expeditious querying module that performs spectral matching against a 168.6 million lipid fragmentation hierarchical library, achieving throughput of approximately 70 billion spectral queries in less than 1 second.: "achieves throughput of approximately 70 billion spectral queries in less than 1 second"
- [other] Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid spectral similarity lookup.: "Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure"
- [readme] The system main development languages being R, python and C++. While R, python handles backend processes and C++ accelerates the program.: "The system main development languages being R, python and C++. While R, python handles backend processes and C++ accelerates the program"
- [readme] ppm1: MS1 m/z tolerance at parts per million (ppm); ppm2: MS2 m/z tolerance at parts per million (ppm): "ppm1: MS1 m/z tolerance at parts per million (ppm); ppm2: MS2 m/z tolerance at parts per million (ppm)"
