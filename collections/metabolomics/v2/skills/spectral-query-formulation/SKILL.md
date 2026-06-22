---
name: spectral-query-formulation
description: Use when you have a query mass spectrum (or representative metabolite spectrum from public data) and need to identify it by searching against large spectral reference databases (millions to billions of spectra).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - GNPS
  - MASST+
  - MASST
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
---

# spectral-query-formulation

## Summary

Formulate and submit mass spectra queries to billion-scale spectral databases using MASST+, enabling fast identification of unknown metabolites by matching against millions of reference spectra with configurable mass tolerance and scoring parameters. This skill is essential when screening unknown mass spectra against comprehensive metabolomics libraries at scale.

## When to use

You have a query mass spectrum (or representative metabolite spectrum from public data) and need to identify it by searching against large spectral reference databases (millions to billions of spectra). Use this skill when the original MASST tool's search time or database size limitations are prohibitive, or when you require error-tolerant matching with ranking by spectral similarity score.

## When NOT to use

- Query spectrum is poorly fragmented or has very few peaks — MASST+ relies on spectral similarity scoring and may return spurious hits with low-information spectra.
- You require exact chemical structure determination — MASST+ performs spectral matching and cannot definitively assign structure without orthogonal validation (NMR, chemical standards).
- Your database is smaller than ~1 million spectra or latency requirements are <100 ms — overhead of MASST+ indexing may not be justified; simpler database engines may suffice.

## Inputs

- Query mass spectrum (USI identifier, mgf file, or mzML format)
- Mass spectrometry dataset (precursor m/z and fragment peaks with intensities)
- Database connection parameters (GNPS endpoint or local indexed repository path)
- Search parameters (mass tolerance, scoring method)

## Outputs

- Ranked list of spectral matches (by cosine similarity score)
- Hit annotations (metabolite identity, library source, precursor m/z, retention time)
- Query execution metadata (elapsed time, resource consumption, result count)
- Search completion status report

## How to apply

Prepare your query mass spectrum in a standard format (or select a representative spectrum from GNPS library). Configure MASST+ with connection parameters to a billion-scale spectral database (e.g., GNPS or a local indexed repository). Submit the query using the MASST+ search interface, specifying standard mass tolerance (e.g., ±0.1 Da for precursor, ±0.05 Da for fragments) and scoring parameters (typically spectral cosine similarity dot-product). Monitor query execution time and resource consumption. Retrieve results ranked by spectral similarity score. Validate that results are returned with hit annotations (matched metabolite, library source, similarity score) and record search completion status and elapsed time in a summary report.

## Related tools

- **MASST+** (Primary spectral search engine; executes billion-scale queries with two orders of magnitude speed reduction over MASST) — https://github.com/mohimanilab/MASSTplus
- **GNPS** (Provides public spectral database and web service interface for MASST+ queries; hosts reference library and molecular networking integration)
- **MASST** (Legacy spectral search tool; retained for comparison and context on speed/scale improvements)

## Evaluation signals

- Query completes within expected time frame (typically seconds for billion-scale database with MASST+, vs. hours with original MASST)
- Results are ranked by spectral similarity score (cosine dot-product) and include hit annotations with library source and retention time
- Result count is non-zero and includes expected metabolite(s) or known reference compounds if query spectrum is from annotated library
- Spectral similarity scores for top hits are above noise threshold (typically >0.7 cosine similarity for confident matches)
- Search execution logs record resource consumption and confirm database indexing was queried rather than performing full-database scan

## Limitations

- MASST+ is optimized for metabolomics and may not perform well on proteomics or other non-metabolomics mass spectra.
- Query spectrum quality and fragmentation pattern directly affect match confidence; highly similar spectra in the database may produce ambiguous rankings if cosine similarity scores are close.
- Error tolerance (handling of mass calibration drift, shifted peaks) improves recall but may increase false positive matches; validation via orthogonal methods (chemical standards, retention time, isotope patterns) is recommended.
- Database indexing requires substantial upfront computation; adding new spectra to a billion-scale index may incur significant latency.

## Evidence

- [intro] Billion-scale database capability: "It is capable of querying against databases of billions of mass spectra, which was not feasible with MASST"
- [intro] Speed improvement and error tolerance: "MASST+ provides fast and error tolerant search of metabolomics mass spectrometry data while reducing the search time by two orders of magnitude"
- [other] Workflow steps for query submission and result validation: "Submit the query using MASST+ search interface with standard mass tolerance and scoring parameters. Monitor and log query execution time and resource consumption. Retrieve and validate that results"
- [readme] Web service integration and public availability: "Like MASST, MASST+ is publicly available as a web service on GNPS"
- [readme] Integration with molecular networking workflow: "When the job has completed, click "View All Clusters With IDs". This will open a new tab, where you can click "Advanced MASST" and then "MASST+ Search""
