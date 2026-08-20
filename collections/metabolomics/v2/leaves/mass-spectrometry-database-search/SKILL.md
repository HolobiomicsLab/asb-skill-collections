---
name: mass-spectrometry-database-search
description: Use when you have an unknown mass spectrum (or a representative metabolite
  spectrum from public data) and need to identify it by comparing it against a large
  reference library—particularly when the database contains billions of spectra and
  earlier tools like MASST are too slow or resource-intensive.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - GNPS
  - MASST+
  - GNPS Molecular Networking
  techniques:
  - LC-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-database-search

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Query an unknown mass spectrum against billion-scale spectral databases to identify metabolites and related compounds through spectral similarity matching. This skill enables fast, error-tolerant search of metabolomics MS data at scales previously infeasible with earlier tools.

## When to use

You have an unknown mass spectrum (or a representative metabolite spectrum from public data) and need to identify it by comparing it against a large reference library—particularly when the database contains billions of spectra and earlier tools like MASST are too slow or resource-intensive.

## When NOT to use

- Your query spectrum is already confidently annotated and does not require identification verification.
- You are searching against a small, local spectral database (< millions of spectra) where MASST or simpler similarity tools are adequate.

## Inputs

- Query mass spectrum (USI format or GNPS library spectrum)
- Spectral database connection parameters (database URL or local indexed repository path)
- Mass tolerance threshold (ppm or m/z units)
- Scoring parameters (e.g., dot-product similarity cutoff)

## Outputs

- Ranked list of spectral hits (sorted by spectral similarity score)
- Metabolite identifications with confidence scores
- Search execution metadata (elapsed time, result count, resource consumption)

## How to apply

Prepare or select a query mass spectrum (in USI format or from the GNPS library) and configure MASST+ with connection parameters to the target spectral database (e.g., GNPS or a local indexed repository). Submit the query via the MASST+ web interface or integrated workflow (e.g., from a molecular networking job) using standard mass tolerance and scoring parameters. MASST+ will execute the search—reducing search time by two orders of magnitude compared to MASST—and rank results by spectral similarity score (dot-product). Monitor query execution time and resource consumption, then retrieve and validate that results are returned with ranked hits. Record completion status, elapsed time, and result count in a summary report.

## Related tools

- **MASST+** (Primary search engine: executes billion-scale spectral similarity queries and ranks hits by dot-product score) — https://github.com/mohimanilab/MASSTplus
- **GNPS** (Host platform and reference library: provides web service interface to MASST+, manages molecular networking integration, and serves as the default spectral database backend) — https://proteomics3.ucsd.edu/ProteoSAFe/
- **GNPS Molecular Networking** (Upstream workflow context: generates clusters and network edges that can be queried via MASST+ for spectral matching at scale)

## Evaluation signals

- Query execution completes without timeout or resource exhaustion, regardless of database size (billions of spectra).
- Returned hits are ranked by spectral similarity score (dot-product), with highest-scoring metabolites appearing first.
- Result count and elapsed time are logged and comparable to the two-order-of-magnitude speedup claimed (e.g., seconds to minutes rather than hours).
- Metabolite identifications returned include valid GNPS spectrum IDs, library accessions (MSV, filename, scan), and precursor mass / retention time metadata.
- Search results remain consistent when the same query is resubmitted against the same database snapshot.

## Limitations

- Search accuracy is limited by spectral resolution and quality of the reference database; noisy or low-abundance query spectra may return false positives or false negatives.
- Error tolerance and mass tolerance thresholds directly affect both recall and precision; overly lenient parameters may yield spurious matches.
- Integration with molecular networking (via Advanced MASST) requires a completed GNPS networking job; on-the-fly searches require either a USI or a pre-indexed local database.
- Very-large-scale databases (billions of spectra) require indexed storage and sufficient computational resources; raw, unindexed databases may still be prohibitively slow.

## Evidence

- [other] MASST+ is capable of querying against databases of billions of mass spectra, whereas this capability was not feasible with MASST.: "MASST+ is capable of querying against databases of billions of mass spectra, which was not feasible with MASST"
- [readme] MASST+ provides fast and error tolerant search of metabolomics mass spectrometry data while reducing the search time by two orders of magnitude.: "MASST+ provides fast and error tolerant search of metabolomics mass spectrometry data while reducing the search time by two orders of magnitude"
- [other] Results are returned ranked by spectral similarity score.: "Retrieve and validate that results are returned (hits ranked by spectral similarity score)"
- [readme] MASST+ can be integrated with molecular networking workflows to search clusters.: "When the job has completed, click 'View All Clusters With IDs'. This will open a new tab, where you can click 'Advanced MASST' and then 'MASST+ Search'"
- [other] Query submission uses standard mass tolerance and scoring parameters.: "Submit the query using MASST+ search interface with standard mass tolerance and scoring parameters"
