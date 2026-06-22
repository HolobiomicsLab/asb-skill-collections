---
name: search-result-visualization-across-domains
description: Use when you have executed batch searches of MS/MS spectra against multiple domain-specific MASST indices and need to synthesize results across domains (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0224
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - metadataMASST
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - Fast Search API
  - GNPS_MASST
derived_from:
- doi: 10.1038/s41538-022-00137-3
  title: foodMASST
evidence_spans:
- Aggregated search outputs can be generated and visualized using metadataMASST
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_foodmasst_2_cq
    doi: 10.1038/s41538-022-00137-3
    title: foodMASST
  dedup_kept_from: coll_foodmasst_2_cq
schema_version: 0.2.0
---

# search-result-visualization-across-domains

## Summary

Aggregate and visualize mass spectrometry search results from multiple domain-specific MASST tools into unified, interactive outputs. This skill enables cross-domain metabolomics discovery by combining heterogeneous search outputs (from microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) through normalized data structures and interactive visualizations.

## When to use

Use this skill when you have executed batch searches of MS/MS spectra against multiple domain-specific MASST indices and need to synthesize results across domains (e.g., comparing microbial vs. plant metabolite matches for the same query spectrum, or displaying matches distributed across tissue types and food sources simultaneously) into a single coherent view for interpretation or publication.

## When NOT to use

- Input contains only single-domain results (e.g., only microbeMASST matches); use individual domain viewers instead
- Query spectra have not yet been searched against the domain-specific MASST indices; execute batch search first
- Analysis goal is domain-specific hypothesis testing rather than cross-domain discovery; individual domain tools may be more appropriate

## Inputs

- MS/MS spectra in .mgf format (from MZmine or GNPS molecular networking)
- Universal Spectrum Identifiers (USIs) in .csv or .tsv format
- Domain-specific MASST search outputs in JSON and TSV format (one per domain: microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST)
- GNPS library matches in TSV format
- Per-domain match counts and dataset summaries

## Outputs

- Interactive HTML tree files aggregating results across all domains
- Unified JSON representation of aggregated search results
- _matches.tsv: consolidated matches across all domain-specific MASSTs with metadata
- _library.tsv: deduplicated GNPS library matches enabling Level 2 MSI annotation
- _datasets.tsv: counts of unique samples matching query per indexed dataset
- _count_domain.tsv files: domain-specific match count summaries

## How to apply

Execute batch searches via the Fast Search API against all indexed domain-specific MASST data to generate domain-specific JSON and TSV outputs. Route each domain's search results (matches, library annotations, dataset counts) into a unified aggregation layer that normalizes heterogeneous output schemas into a common data structure. Implement visualization components—interactive HTML trees, tabular summaries, and count matrices—that render the combined results, preserving domain-specific context while enabling cross-domain comparison. Validate end-to-end by confirming that all domain results are present, no matches are dropped during aggregation, and interactive elements (e.g., tree expansion, filtering) operate correctly across the full combined dataset.

## Related tools

- **metadataMASST** (Primary aggregation and visualization engine for cross-domain search results; generates interactive HTML trees and unified JSON outputs from heterogeneous domain-specific MASST results) — https://github.com/mwang87/GNPS_MASST
- **microbeMASST** (Domain-specific search tool generating matches against curated microbial metabolome data; contributes one set of domain-specific results to aggregation) — https://github.com/robinschmid/microbe_masst
- **plantMASST** (Domain-specific search tool generating matches against curated plant metabolome data; contributes one set of domain-specific results to aggregation) — https://github.com/mwang87/GNPS_MASST
- **tissueMASST** (Domain-specific search tool generating matches against curated tissue metabolome data; contributes one set of domain-specific results to aggregation) — https://github.com/mwang87/GNPS_MASST
- **microbiomeMASST** (Domain-specific search tool generating matches against curated microbiome metabolome data; contributes one set of domain-specific results to aggregation) — https://github.com/mwang87/GNPS_MASST
- **foodMASST** (Domain-specific search tool generating matches against curated food metabolome data; contributes one set of domain-specific results to aggregation) — https://github.com/mwang87/GNPS_MASST
- **Fast Search API** (Backend service for batch searching multiple MS/MS spectra against indexed GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN data across all domain MASSTs) — https://fasst.gnps2.org/fastsearch/
- **GNPS_MASST** (Base framework containing standalone web application code for individual domain-specific MASST tools; provides foundation for metadataMASST aggregation) — https://github.com/mwang87/GNPS_MASST

## Examples

```
python code/jobs.py  # After populating jobs.py with entries: ("spectra.mgf", "results/batch1") with skip_existing=True; metadataMASST then generates results/batch1_microbe.html, results/batch1_plant.html, ..., results/batch1_matches.tsv, results/batch1_library.tsv, results/batch1_datasets.tsv
```

## Evaluation signals

- All queried spectra produce cross-domain result sets in metadataMASST output with non-empty aggregated JSON and HTML trees
- Aggregated _matches.tsv contains entries from all domain-specific MASSTs without duplication or loss; row counts match sum of per-domain matches
- Interactive HTML trees render without JavaScript errors and allow expansion/collapse of domain-specific result nodes
- Library-level annotations in _library.tsv are deduplicated and MSI Level 2 compliant (matched against GNPS libraries)
- _count_domain.tsv files show consistent totals when summed across domains and match individual domain search reports

## Limitations

- Some Fast Search API requests may fail on first execution; re-runs with skip_existing=True are required to capture all possible matches across all domains
- Requires Python 3.10 to run batch search pipeline; compatibility with other Python versions not validated
- Visualization performance may degrade with very large numbers of matches (>10,000) across multiple domains; pagination or filtering strategies may be needed
- Results reflect only currently indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN; older or private datasets are not included

## Evidence

- [other] Aggregation layer integration and output normalization: "Aggregated search outputs can be generated and visualized using metadataMASST"
- [readme] Batch search methodology: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench,"
- [readme] Interactive visualization output formats: "A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html (e.g., _microbe.html)"
- [readme] Consolidated matching results output: "A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed. This includes also samples that are"
- [other] Domain-specific result aggregation rationale: "metadataMASST enables generation and visualization of aggregated search outputs across domain-specific MASST searches, distinguishing it from standalone tools that search one spectrum at a time"
