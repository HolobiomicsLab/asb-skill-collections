---
name: metabolite-spectral-matching
description: Use when you have an experimental mass spectrum (or a set of spectra from LC-MS/MS data) and need to identify the underlying metabolite(s) by comparing against known reference spectra in GNPS or a local indexed repository.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - GNPS
  - MASST+
  - GNPS (Global Natural Products Social Molecular Networking)
  - Spectrum USI (Metabolomics Spectrum Resolver)
  techniques:
  - LC-MS
  - NMR
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

# metabolite-spectral-matching

## Summary

Query unknown mass spectra against large-scale reference spectral libraries to identify metabolites by computing spectral similarity scores. This skill enables rapid dereplication and metabolite annotation in metabolomics workflows, particularly when working with billion-scale spectral databases.

## When to use

You have an experimental mass spectrum (or a set of spectra from LC-MS/MS data) and need to identify the underlying metabolite(s) by comparing against known reference spectra in GNPS or a local indexed repository. Use this skill when the scale of your reference library is too large for conventional linear search (e.g., > millions of spectra) or when you need sub-second query latency for high-throughput annotation.

## When NOT to use

- You need de novo structure prediction rather than database matching (spectral matching returns only library identifications)
- Your reference library contains < 10⁶ spectra and standard linear search is sufficient
- Your query spectra are from a completely orthogonal modality (e.g., 1D NMR or IR) not represented in GNPS or your target library

## Inputs

- Query mass spectrum (single spectrum in MGF or USI format, or spectrum USI identifier)
- Mass spectrometry search parameters (mass tolerance in ppm/Da, minimum cosine similarity threshold)
- Reference spectral library connection (GNPS public database or local indexed repository URI)

## Outputs

- Ranked list of spectral hits (with spectrum metadata, precursor m/z, retention time, source library)
- Spectral similarity scores (cosine similarity dot-product, optionally decomposed into shared and shifted peak contributions)
- Search execution metadata (query time, result count, search completion status)

## How to apply

Prepare a query mass spectrum in standard format (e.g., from a GNPS library spectrum or a representative scan from your experiment). Configure MASST+ with appropriate mass tolerance and scoring parameters (typically cosine similarity with fragment m/z matching). Submit the query via the MASST+ web interface or programmatically against the indexed spectral database. Monitor query execution time and retrieve ranked results ordered by spectral similarity score. Validate hits by inspecting the top-ranked matches and checking that their precursor mass and fragmentation pattern align with your query spectrum. Record search metadata (elapsed time, hit count, top match score) to assess search quality and reproducibility.

## Related tools

- **MASST+** (Primary tool for fast, error-tolerant spectral library search at billion-scale. Reduces search latency by two orders of magnitude versus the original MASST and enables queries against databases previously infeasible to search.) — https://github.com/mohimanilab/MASSTplus
- **GNPS (Global Natural Products Social Molecular Networking)** (Hosts the public spectral library and provides web service access to MASST+ searches; also integrates MASST+ results into molecular networking and spectral library browsing workflows.) — https://proteomics3.ucsd.edu/ProteoSAFe/
- **Spectrum USI (Metabolomics Spectrum Resolver)** (Standardized identifier format for locating individual spectra across distributed repositories; used to specify query spectra in MASST+ without manual upload.) — https://github.com/mwang87/MetabolomicsSpectrumResolver

## Evaluation signals

- Query returns results within expected latency (sub-second for single-spectrum queries on billion-scale databases)
- Top-ranked hit(s) have precursor m/z within ±5 ppm of query spectrum and cosine similarity score ≥ 0.7 for confident matches
- Results reproducibly rank spectra by cosine similarity in descending order; re-running the same query yields identical rankings
- Search completion status is reported and query executes without timeout or out-of-memory errors on the target database scale
- When integrated with molecular networking, MASST+ hits propagate correctly to cluster visualization and network edges reflect reported spectral similarity scores

## Limitations

- Spectral matching returns only library identifications; unknown or novel metabolites will not be found if not present in the reference library
- Search quality depends on the completeness and curation of the reference spectral library; poor coverage in certain compound classes or ionization modes will reduce hit rates
- Fragment ion annotation and scoring assume consistent fragmentation behavior; highly similar spectral patterns in different isomers or in-source rearrangements can lead to ambiguous assignments
- Billion-scale search requires pre-indexed databases; ad-hoc searches against custom spectrum collections require local indexing infrastructure

## Evidence

- [readme] MASST+ is capable of querying against databases of billions of mass spectra, which was not feasible with MASST.: "It is capable of querying against databases of billions of mass spectra, which was not feasible with MASST"
- [readme] Two-order-of-magnitude speed improvement over original MASST tool: "reducing the search time by two orders of magnitude"
- [readme] Scoring and ranking mechanism uses spectral similarity dot-product: "product` is the similarity dot-product between the two nodes"
- [readme] Integration with GNPS molecular networking and spectral library browsing: "When the job has completed, click "View All Clusters With IDs". (c) This will open a new tab, where you can click "Advanced MASST" and then "MASST+ Search""
- [readme] Fast and error-tolerant search of metabolomics mass spectrometry data: "MASST+ provides fast and error tolerant search of metabolomics mass spectrometry data"
