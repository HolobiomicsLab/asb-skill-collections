---
name: spectral-database-query-execution
description: Use when when you have an unknown mass spectrum (query spectrum) and need to search it against a reference database of billions of spectra to find matching or structurally related compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MASST
  - GNPS
  - MASST+
  - CLUSTERING+
  - PAIRING+
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41587-023-01985-4
  title: MASST
evidence_spans:
- MASST+ is an improvement on GNPS Mass Spectrometry Search Tool (MASST)
- MASST+ is an improvement on GNPS Mass Spectrometry Search Tool
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

# spectral-database-query-execution

## Summary

Execute mass spectrometry spectral queries against large reference databases to identify unknown metabolites or retrieve similar spectra. This skill measures query execution time and retrieves ranked results with similarity scores for validation and annotation.

## When to use

When you have an unknown mass spectrum (query spectrum) and need to search it against a reference database of billions of spectra to find matching or structurally related compounds. Apply this skill when baseline search performance is unacceptable (slow wall-clock times) or when the reference database is too large for the original tool to handle efficiently.

## When NOT to use

- Your reference database is small enough for exhaustive search with the original tool — optimization overhead may not justify complexity.
- Your query spectrum is already annotated and you only need structural similarity exploration rather than de novo identification.
- You require full tandem MS/MS fragmentation trees or metafragment analysis; spectral similarity alone may be insufficient.

## Inputs

- Query spectrum (single or batch set)
- Query spectrum USI (Universal Spectrum Identifier)
- Reference mass spectra database (GNPS library or equivalent)
- Search parameters (precursor mass tolerance, fragment ion tolerance, minimum match threshold)
- Database configuration (indexing strategy, division scheme for large databases)

## Outputs

- Ranked list of similar spectra with similarity scores (dot-product, cosine similarity)
- Per-query execution time (wall-clock seconds)
- Aggregate execution time and speedup ratio
- Confidence intervals or run variance for timing statistics
- Network integration data (molecular networking clusters, edges) when integrated with clustering/pairing workflows

## How to apply

Configure both the baseline and optimized search systems (e.g., MASST and MASST+) with identical database and parameter settings. Submit the same query spectrum set to each system and record total wall-clock search time for each. Calculate the speedup ratio (baseline time ÷ optimized time) to quantify performance improvement. Tabulate per-query and aggregate timing statistics with confidence intervals or run variance to account for system variability. Verify that similarity metrics (e.g., cosine dot-product scores) and ranked result ordering remain consistent between systems to ensure functional equivalence despite performance gains.

## Related tools

- **MASST+** (Optimized spectral database search tool that executes queries against billions of mass spectra with two orders of magnitude speedup over baseline MASST) — https://github.com/mohimanilab/MASSTplus
- **MASST** (Baseline GNPS Mass Spectrometry Search Tool; used as performance reference for comparison with MASST+)
- **GNPS** (Global Natural Products Social Molecular Networking platform; hosts MASST+ as a web service and provides the reference spectral library (billions of spectra across 9 precursor mass divisions))
- **CLUSTERING+** (Preprocessing tool that clusters spectra by precursor mass range (9 divisions); output feeds into MASST+ indexing and molecular networking)
- **PAIRING+** (Computes molecular network edges from CLUSTERING+ results; generates node and edge TSV files for network visualization)

## Evaluation signals

- Speedup ratio (MASST time ÷ MASST+ time) equals approximately 100-fold (two orders of magnitude reduction).
- Per-query and aggregate timing statistics include confidence intervals or run variance below acceptable threshold (e.g., <5% coefficient of variation across repeated runs).
- Ranked result lists are identical between baseline and optimized systems (same top-N hits, same cosine similarity scores) — functional equivalence check.
- Search latency for individual queries completes in seconds (not minutes) against billion-scale databases, validating feasibility of billion-spectra querying.
- Network nodes (8M+ clusters) and edges (similarity > threshold) are reproducible across query batches with consistent MSV library and scan provenance tracking.

## Limitations

- Speedup is contingent on identical database configuration and parameter settings; mismatched precursor mass tolerances or fragment ion match thresholds will yield incomparable results.
- Performance gain assumes optimized indexing (e.g., division-based clustering); unindexed or poorly indexed databases may not realize two orders of magnitude improvement.
- Spectral similarity alone (dot-product/cosine score) does not provide chemical structure or ontology validation; manual curation or orthogonal evidence is required for confident compound annotation.
- Error tolerance and match scoring depend on precursor mass range and library composition; results may vary across different subsets of GNPS or alternative metabolomics databases.

## Evidence

- [other] Execute the query set on the baseline MASST system and record total wall-clock search time. Execute the same query set on MASST+ and record total wall-clock search time.: "Execute the query set on the baseline MASST system and record total wall-clock search time. 3. Execute the same query set on MASST+ and record total wall-clock search time."
- [other] Calculate the speedup ratio and verify it equals approximately 100-fold.: "Calculate the speedup ratio (MASST time ÷ MASST+ time) and verify it equals approximately 100-fold."
- [intro] MASST+ reduces search time by two orders of magnitude compared to MASST: "reducing the search time by two orders of magnitude"
- [intro] MASST+ is capable of querying against databases of billions of mass spectra: "It is capable of querying against databases of billions of mass spectra, which was not feasible with MASST"
- [other] Tabulate and report per-query and aggregate timing statistics with confidence intervals or run variance.: "Tabulate and report per-query and aggregate timing statistics with confidence intervals or run variance."
- [readme] GNPS library divided into 9 divisions according to different precursor mass ranges for indexed search.: "We split the GNPS library into 9 divisions according to different precursor mass ranges and executed CLUSTERING+ on each of them."
