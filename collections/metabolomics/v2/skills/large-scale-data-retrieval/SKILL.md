---
name: large-scale-data-retrieval
description: Use when you have a query mass spectrum (or a metabolite reference spectrum from public data) and need to search it against a large-scale spectral repository (≥billions of spectra, e.g., GNPS library) where execution time and resource efficiency are critical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - GNPS
  - MASST+
  - Spectrum USI (Spectrum Unique Spectrum Identifier)
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41587-023-01985-4
  title: MASST
evidence_spans:
- MASST+ is publicly available as a web service on GNPS
- Like MASST, MASST+ is publicly available as a web service on GNPS.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_masst_3_cq
    doi: 10.1038/s41587-023-01985-4
    title: MASST
  dedup_kept_from: coll_masst_3_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-023-01985-4
  all_source_dois:
  - 10.1038/s41587-023-01985-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# large-scale-data-retrieval

## Summary

Query and retrieve results from billion-scale mass spectrometry spectral databases using MASST+, enabling metabolomics searches across collections infeasible with prior tools. This skill is essential when the research question requires comprehensive spectral matching against globally-aggregated reference libraries without computational bottlenecks.

## When to use

Apply this skill when you have a query mass spectrum (or a metabolite reference spectrum from public data) and need to search it against a large-scale spectral repository (≥billions of spectra, e.g., GNPS library) where execution time and resource efficiency are critical. Use it when prior tools like MASST are too slow or have failed to complete searches due to database scale.

## When NOT to use

- Your spectral database contains <100 million spectra; MASST (original tool) is sufficient and does not require the billion-scale optimization.
- You have only a few isolated spectra to match and search latency is not a constraint; simpler batch search tools may be more practical.
- Your query spectra are not mass spectrometry data or are in a format incompatible with MASST+ ingestion (e.g., unprocessed raw instrument files without MS/MS fragmentation).

## Inputs

- Query mass spectrum (MS/MS data in .mgf or USI format)
- Mass tolerance parameter (in ppm or Da)
- Spectral similarity scoring threshold
- Connection parameters to billion-scale spectral database (GNPS or local indexed repository)

## Outputs

- Ranked list of spectral hits with similarity scores
- Query execution time and resource consumption log
- Search completion status report
- Result count summary

## How to apply

Prepare a query mass spectrum or select a representative metabolite spectrum from public metabolomics data. Configure MASST+ with connection parameters to the target billion-scale spectral database (e.g., via GNPS or a locally indexed repository). Submit the query using the MASST+ search interface, specifying standard mass tolerance and spectral similarity scoring parameters (e.g., cosine similarity). Monitor query execution time and resource consumption during the search. Retrieve ranked results scored by spectral similarity, validate that hits are returned, and record search completion status, elapsed time, and total result count in a summary report to confirm the billion-scale query completed successfully.

## Related tools

- **MASST+** (Primary search engine for fast, error-tolerant querying of billion-scale metabolomics mass spectrometry databases; reduces search time by two orders of magnitude over MASST) — https://github.com/mohimanilab/MASSTplus
- **GNPS** (Public web service hosting MASST+ and providing access to large-scale spectral library and molecular networking infrastructure)
- **Spectrum USI (Spectrum Unique Spectrum Identifier)** (Standardized identifier format for unambiguously specifying and retrieving individual query spectra from public repositories) — https://github.com/mwang87/MetabolomicsSpectrumResolver

## Evaluation signals

- Query execution completes within reasonable time and returns non-empty hit list ranked by spectral similarity score (confirming billion-scale database was queried).
- Elapsed time is significantly faster than sequential database scans; log records <1% of the theoretical time required by the original MASST tool.
- Resource consumption (memory, CPU) remains bounded and proportional to query spectrum complexity, not database size.
- Retrieved hit spectra have precursor m/z within specified mass tolerance of query spectrum and match chemical identity of expected metabolite (spot-check validation).
- Search completion status is 'success' and result count matches expected order of magnitude for a broad or narrow chemical class query.

## Limitations

- MASST+ indexing and database connection setup require prior configuration; initial deployment to a new spectral repository may be time-intensive.
- Search accuracy depends on data quality and completeness of the indexed spectral library; sparse or poorly annotated regions of chemical space may yield few or unreliable hits.
- Error tolerance (handling of mass calibration drift, instrument artifacts) is designed for typical metabolomics workflows; atypical MS/MS fragmentation patterns or heavily modified spectra may not retrieve expected matches.

## Evidence

- [other] MASST+ is capable of querying against databases of billions of mass spectra, whereas this capability was not feasible with MASST.: "MASST+ is capable of querying against databases of billions of mass spectra, whereas this capability was not feasible with MASST"
- [readme] MASST+ provides fast and error tolerant search of metabolomics mass spectrometry data while reducing the search time by two orders of magnitude.: "MASST+ provides fast and error tolerant search of metabolomics mass spectrometry data while reducing the search time by two orders of magnitude"
- [readme] If you know the spectrum USI of a spectrum you want to search with MASST+, you can enter it directly at https://masst.ucsd.edu/masstplus/.: "If you know the spectrum USI of a spectrum you want to search with MASST+, you can enter it directly"
- [readme] It is capable of querying against databases of billions of mass spectra, which was not feasible with MASST.: "It is capable of querying against databases of billions of mass spectra, which was not feasible with MASST"
