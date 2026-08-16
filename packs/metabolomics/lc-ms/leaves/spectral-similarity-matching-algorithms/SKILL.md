---
name: spectral-similarity-matching-algorithms
description: Use when when you have experimental MS/MS spectra (from mzML or .rda preprocessed format) and need to annotate them against a reference fragmentation library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - XCMS
  - CAMERA
  - RaMS
  - LipidIN EQ module
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

# spectral-similarity-matching-algorithms

## Summary

High-throughput spectral similarity matching against large fragmentation libraries using mass-error-tolerant fragment matching and cosine similarity to annotate experimental MS/MS spectra. Critical for identifying lipids and other metabolites when working with mass spectrometry datasets.

## When to use

When you have experimental MS/MS spectra (from mzML or .rda preprocessed format) and need to annotate them against a reference fragmentation library. Specifically applicable when processing lipidomics data with MS1 and MS2 measurements, and you require high-throughput matching (millions to billions of queries) against hierarchically organized spectral libraries with defined mass tolerances (e.g., 5–10 ppm).

## When NOT to use

- Input spectra are already pre-identified or de-replicated; use this skill only on raw or minimally processed MS/MS data.
- Library is unstructured or not indexed for rapid lookup; hierarchical organization and in-memory indexing are prerequisites for achieving stated throughput.
- Mass tolerances are incompatible with your instrument calibration or experimental design (e.g., if your ppm error systematically exceeds 10 ppm, matching will fail or produce false positives).

## Inputs

- Preprocessed MS/MS spectral data (.rda format or in-memory array of MS1 m/z, MS2 fragments, and intensities)
- Hierarchical fragmentation library (indexed structure with chain compositions, double-bond locations, and reference spectra)
- MS1 mass tolerance parameter (ppm1, typically 5 ppm)
- MS2 mass tolerance parameter (ppm2, typically 10 ppm)
- MS2 intensity filter threshold (0–1 scale, e.g., 0.10)

## Outputs

- Matched spectrum annotations with library entry identifiers and similarity scores
- CSV-format identification results with ranked candidates
- Query throughput metrics (queries/second, wall-clock execution time)

## How to apply

Load the hierarchical fragmentation library (e.g., 168.6 million lipid entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid lookup. Implement spectral querying logic using cosine similarity or mass-error-tolerant fragment matching to compare experimental MS/MS spectra against library entries, applying MS1 tolerance (ppm1) and MS2 tolerance (ppm2) thresholds. Execute the query engine on preprocessed spectral data, measuring wall-clock time and query throughput (queries/second). Apply MS2 intensity filtering (e.g., MS2_filter=0.10 to remove fragments below 10% of max intensity) before matching. Validate achievement of target throughput (e.g., ~70 billion queries in <1 second for large libraries) and record actual performance metrics to confirm efficiency gains over sequential matching.

## Related tools

- **XCMS** (Upstream MS data processing: peak alignment, matching, and retention-time normalization before spectral similarity matching)
- **CAMERA** (Compound spectra extraction and annotation to support spectral querying workflow)
- **RaMS** (Data preprocessing to convert mzML format to .rda format for input to spectral matching module)
- **LipidIN EQ module** (Core implementation of expeditious querying with cosine similarity and mass-error-tolerant fragment matching) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
source('EQ.r'); EQ(filename='QC_POS1.rda', ppm1=5, ppm2=10, ESI='p')
```

## Evaluation signals

- Query throughput meets or exceeds target (e.g., ~70 billion queries/second for 168.6 million library entries on standardized hardware).
- Wall-clock execution time for a benchmark query set is <1 second (or scales linearly with number of queries).
- Similarity scores for known positive matches fall above a credible cosine similarity threshold (e.g., >0.7); false-positive rates remain low when combined with secondary filtering (LCI module).
- Output CSV contains expected fields (lipid ID, m/z, MS/MS match score, ranked candidates) with no missing or malformed entries.
- Mass error for matched fragments falls within specified tolerances (ppm1 for MS1, ppm2 for MS2) across >95% of matches.

## Limitations

- Throughput depends critically on library indexing and in-memory availability; very large libraries (>1 billion entries) may require distributed or on-disk strategies not detailed here.
- Cosine similarity matching alone produces high false-positive rates; the workflow requires downstream filtering via the LCI module (relative retention time rules) to achieve 5.7% FDR and reduce false annotations.
- Performance metrics (70 billion queries/second) were benchmarked on specific hardware (13th Gen Intel i7-13700F, 64 GB RAM, Windows 11); throughput will vary with system configuration.
- MS2 intensity filtering (MS2_filter parameter) is sensitive to instrumental noise and detector saturation; threshold must be tuned per instrument and sample type to avoid loss of weak but real fragments.
- Library coverage is limited to lipid species with documented fragmentation patterns; novel lipids or heavily modified variants not represented in the 168.6 million entries will fail to match.

## Evidence

- [other] Implement spectral querying logic using cosine similarity or mass-error-tolerant fragment matching to compare experimental MS/MS spectra against library entries.: "Implement spectral querying logic using cosine similarity or mass-error-tolerant fragment matching to compare experimental MS/MS spectra against library entries."
- [other] LipidIN implements an expeditious querying module that performs spectral matching against a 168.6 million lipid fragmentation hierarchical library, achieving throughput of approximately 70 billion spectral queries in less than 1 second.: "LipidIN implements an expeditious querying module that performs spectral matching against a 168.6 million lipid fragmentation hierarchical library, achieving throughput of approximately 70 billion"
- [other] Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid spectral similarity lookup.: "Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid"
- [readme] MS2_filter: a value of 0-1, MS2 fragments with intensity lower than the MS2_filter*max intensity will be deleted: "MS2_filter: a value of 0-1, MS2 fragments with intensity lower than the MS2_filter*max intensity will be deleted"
- [readme] ppm1: MS1 m/z tolerance at parts per million (ppm); ppm2: MS2 m/z tolerance at parts per million (ppm): "ppm1: MS1 m/z tolerance at parts per million (ppm); ppm2: MS2 m/z tolerance at parts per million (ppm)"
