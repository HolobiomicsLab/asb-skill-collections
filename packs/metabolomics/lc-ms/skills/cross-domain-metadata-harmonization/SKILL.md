---
name: cross-domain-metadata-harmonization
description: Use when when you have submitted the same MS/MS spectrum query to multiple domain-specific MASST tools and need to compare matches, combine ranked results, or generate cross-domain summary statistics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - metadataMASST
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - GNPS_MASST
  - Fast Search API
  - jobs.py
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41538-022-00137-3
  all_source_dois:
  - 10.1038/s41538-022-00137-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-domain-metadata-harmonization

## Summary

Aggregates and normalizes heterogeneous mass spectrometry search results from multiple domain-specific MASST tools (microbe, plant, tissue, microbiome, food) into a unified data structure for integrated visualization and comparative analysis. This skill enables unified querying across disparate taxonomic and sample-type domains without manual result consolidation.

## When to use

When you have submitted the same MS/MS spectrum query to multiple domain-specific MASST tools and need to compare matches, combine ranked results, or generate cross-domain summary statistics. Specifically applicable when batch-searching multiple spectra across all domainMASSTs simultaneously using the Fast Search API and requiring harmonized outputs for downstream interpretation.

## When NOT to use

- Searching spectra within a single domain only—use the standalone domain-specific MASST tool directly (e.g., microbeMASST alone) for faster single-domain queries
- When your input spectra are already pre-filtered to a single biological domain and cross-domain comparison adds no interpretive value
- If you require real-time single-spectrum search feedback; batch aggregation via jobs.py is designed for bulk processing and may incur API latency

## Inputs

- MS/MS spectra in .mgf format (from MZmine or GNPS molecular networking)
- Batch lists of Universal Spectrum Identifiers (USIs) in .csv or .tsv format
- JSON search result objects from individual domain-specific MASST API endpoints
- Search parameters (cosine score threshold, m/z tolerance, minimum matching peaks)

## Outputs

- Interactive HTML tree files per domain (_microbe.html, _plant.html, etc.)
- Domain-specific JSON tree objects (_microbe.json, _plant.json, etc.)
- _matches.tsv: unified list of all matching spectra across all indexed databases with domain origin
- _library.tsv: GNPS library matches supporting Level 2 metabolomics annotation
- _datasets.tsv: counts of unique samples per indexed dataset matching the query
- _count_domain.tsv files: match counts and metadata per individual domain MASST
- Aggregated visualization object suitable for metadataMASST web interface

## How to apply

Clone the GNPS_MASST and robinschmid/microbe_masst repositories to access the base framework and metadataMASST component code. Route search results from each domain-specific MASST (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) through a unified aggregation layer by normalizing input schemas—converting heterogeneous API responses into a common data model. Implement aggregation logic that combines results while preserving domain origin metadata (e.g., '_microbe.json', '_plant.json' annotations). Set search parameters consistently across domains: minimum cosine score, m/z tolerance, and minimum matching peaks thresholds. Generate normalized outputs including _matches.tsv (all spectrum matches across indexed databases), _library.tsv (GNPS library matches for Level 2 annotations), _datasets.tsv (unique sample counts per dataset), and domain-specific _count_domain.tsv files. Validate end-to-end by comparing individual domain outputs against the aggregated metadataMASST visualization to ensure no loss or duplication of matches.

## Related tools

- **GNPS_MASST** (Base framework housing all standalone domain-specific MASST web applications and aggregation layer code) — https://github.com/mwang87/GNPS_MASST
- **metadataMASST** (Web application endpoint that visualizes and renders aggregated cross-domain search results) — https://masst.gnps2.org/metadatamasst/
- **microbeMASST** (Domain-specific search tool queried for microbial metabolite matches; results aggregated via this skill) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific search tool queried for plant metabolite matches; results aggregated via this skill) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific search tool queried for tissue metabolite matches; results aggregated via this skill) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific search tool queried for microbiome metabolite matches; results aggregated via this skill) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific search tool queried for food metabolite matches; results aggregated via this skill) — https://masst.gnps2.org/foodmasst2/
- **Fast Search API** (Backend search service invoked by jobs.py for batch querying against indexed GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN databases) — https://fasst.gnps2.org/fastsearch/
- **jobs.py** (Batch orchestration script that coordinates multi-spectrum queries across all domainMASSTs and triggers aggregation workflow) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py

## Examples

```
python jobs.py  # After adding entries to files list as ("input_dir/spectra.mgf", "output_dir/results"), then inspect output_dir/results_matches.tsv, output_dir/results_library.tsv, and output_dir/results_microbe.html for aggregated cross-domain results
```

## Evaluation signals

- Verify that the count of unique spectrum matches in _matches.tsv equals or exceeds the union of individual domain-specific _count_domain.tsv files (no duplicates within a domain, no losses across domains)
- Confirm that all _matches.tsv rows have non-null 'domain_origin' annotations and that each row traces back to at least one valid source domain HTML/JSON file
- Check that Level 2 annotations in _library.tsv correspond to GNPS library entries and that the count of library matches is monotonically consistent when re-running the same batch (idempotency check via skip_existing=True)
- Validate that _datasets.tsv reports sample counts per indexed dataset (GNPS/MassIVE, Metabolomics Workbench, Metabolights, NORMAN) and that the sum of counts across datasets in a domain-specific _count_domain.tsv is non-zero
- Re-run jobs.py multiple times with skip_existing=True and confirm that no new output is generated after the second or third iteration (convergence of Fast Search API results)

## Limitations

- The Fast Search API may fail to return results for some spectrum entries on first execution; sequential re-runs with skip_existing=True are required to achieve complete coverage, and success is not guaranteed for all entries
- Aggregation depends on consistent indexing of all source databases (GNPS/MassIVE, Metabolomics Workbench, Metabolights, NORMAN); if a database is offline or out-of-sync, matches from that source will be missing from _matches.tsv without explicit warning
- Batch search requires Python 3.10; compatibility with other Python versions is not tested and may result in API client failures
- Cross-domain aggregation preserves all matches found in the indexed data, including spectra outside the curated domain-specific MASST lineages; filtering to curated-only results requires post-processing against the lineage TSV files provided in the repository

## Evidence

- [readme] Aggregated search outputs can be generated and visualized using metadataMASST: "Aggregated search outputs can be generated and visualized using metadataMASST"
- [readme] Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN: "Running [jobs.py](https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py) allows users to leverage the [Fast Search API](https://fasst.gnps2.org/fastsearch/) and execute a batch search"
- [other] Implement aggregation logic to combine heterogeneous search outputs from all domain sources into a single normalized data structure: "Implement aggregation logic to combine heterogeneous search outputs from all domain sources into a single normalized data structure"
- [readme] A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed.: "A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed"
- [readme] A _library.tsv file will be generated enabling a Level 2 annotation according the Metabolomics Standards Initiative: "A _library.tsv file will be generated. This contains a list of spectra from the [GNPS libraries](https://library.gnps2.org/) found to match your spectrum of interest. This enables a Level 2"
- [readme] Make sure to run jobs.py a couple of times, until no new output is generated by having the option skip_existing=True. Due to the Fast Search API some of the entries will fail.: "Make sure to run [jobs.py](https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py) **_a couple of times_**, until no new output is generated by having the option: `skip_existing=True`."
- [other] metadataMASST enables generation and visualization of aggregated search outputs across domain-specific MASST searches: "metadataMASST enables generation and visualization of aggregated search outputs across domain-specific MASST searches, distinguishing it from standalone tools that search one spectrum at a time"
