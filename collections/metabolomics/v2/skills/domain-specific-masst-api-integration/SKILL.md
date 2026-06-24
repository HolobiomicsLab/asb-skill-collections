---
name: domain-specific-masst-api-integration
description: Use when your research involves searching MS/MS spectra against multiple
  curated taxonomic or domain-specific databases (microbial, plant, tissue, microbiome,
  or food origin) and you need to aggregate, compare, and visualize matching results
  across all domains in a single interface.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - GNPS_MASST
  - metadataMASST
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - Fast Search API
  - MZmine
  techniques:
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1038/s41538-022-00137-3
  title: foodMASST
evidence_spans:
- The code for the different standalone web applications, which allow users to search
  one spectrum at a time, can be found in GNPS_MASST
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

# domain-specific-masst-api-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrating API endpoints from domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) into a unified aggregation layer to route heterogeneous MS/MS search results into metadataMASST for combined visualization and analysis. This skill enables batch processing of multiple spectra against all domain-specific MASSTs simultaneously rather than searching one spectrum at a time.

## When to use

Your research involves searching MS/MS spectra against multiple curated taxonomic or domain-specific databases (microbial, plant, tissue, microbiome, or food origin) and you need to aggregate, compare, and visualize matching results across all domains in a single interface. Specifically, when you have a collection of .mgf files or USI lists from molecular networking or MZmine and want to identify the distribution and overlap of spectral matches across multiple biological domains simultaneously.

## When NOT to use

- Your input spectra are already annotated at MSI Level 1 (exact mass library match with retention time); batch integration adds redundancy without new discriminatory value.
- You require single-domain searching (e.g., only microbeMASST); use the standalone web application directly rather than implementing API integration overhead.
- Your spectra originate from non-standard sample types not covered by the five current domainMASSTs (microbe, plant, tissue, microbiome, food) and you lack domain-specific reference libraries to add.

## Inputs

- MS/MS spectrum files (.mgf format generated via MZmine or GNPS molecular networking)
- Universal Spectrum Identifiers (USI) lists (.csv or .tsv format)
- Search parameter configuration (cosine score threshold, m/z tolerance, minimum peaks)
- Domain-specific MASST API endpoint specifications and authentication credentials

## Outputs

- Interactive HTML tree files for each domain-specific MASST (_domain.html files, e.g., _microbe.html, _plant.html)
- JSON tree metadata files (_domain.json) for programmatic consumption
- _matches.tsv: all matching scans across indexed data (GNPS/MassIVE, Metabolomics Workbench, Metabolights, NORMAN)
- _library.tsv: matched spectra from GNPS libraries (Level 2 annotation MSI compliance)
- _datasets.tsv: count of unique samples matching per indexed dataset
- _count_domain.tsv files: per-domain match statistics and summary metrics

## How to apply

Clone the GNPS_MASST base repository and examine the metadataMASST module structure to understand input schemas and output rendering logic. For each domain-specific MASST (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST), identify and document the Fast Search API endpoint signatures and expected input/output formats. Route search results from each domain into a unified aggregation layer by normalizing heterogeneous output structures (e.g., cosine scores, matched peak counts, dataset provenance) into a common data model. Implement aggregation logic to combine results from all domains, then develop visualization components (interactive HTML trees, TSV summary tables, JSON metadata files) to display aggregated matches. Test end-to-end by submitting test queries to verify that metadataMASST correctly combines and renders results across all integrated domain sources. Set search parameters (minimum cosine score, m/z tolerance, minimum matching peaks) consistent with your research question before batch execution.

## Related tools

- **GNPS_MASST** (Base framework providing standalone web application code and unified API infrastructure for all domain-specific MASST tools) — https://github.com/mwang87/GNPS_MASST
- **metadataMASST** (Aggregation and visualization layer that combines search results from all domain-specific MASSTs and renders interactive outputs)
- **microbeMASST** (Domain-specific search tool providing taxonomically-informed spectral matching for microbial metabolites; one input source to aggregation pipeline) — https://github.com/robinschmid/microbe_masst
- **plantMASST** (Domain-specific search tool for plant-derived metabolites; routed to aggregation layer for combined output)
- **tissueMASST** (Domain-specific search tool for tissue-derived metabolites; integrated into aggregation pipeline)
- **microbiomeMASST** (Domain-specific search tool for microbiome-associated metabolites; input to unified aggregation)
- **foodMASST** (Domain-specific search tool for food-derived metabolites; one of five domains aggregated by metadataMASST)
- **Fast Search API** (Backend API for executing batch spectral searches against GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN indexed data)
- **MZmine** (Upstream tool for generating .mgf files suitable as input to batch MASST searches) — https://github.com/mzmine/mzmine

## Examples

```
python jobs.py  # After editing jobs.py to add entries as ("input_directory/input_file", "output_directory/output_prefix") and setting cosine_score_min=0.7, mz_tolerance=0.1, min_matching_peaks=6
```

## Evaluation signals

- All domain-specific MASST endpoints are successfully invoked without timeouts or authentication failures; HTTP status codes return 200 for each domain query.
- Output HTML tree files (_microbe.html, _plant.html, etc.) render interactively in browser with hierarchical taxonomy and match counts; verify that leaf nodes display cosine scores and dataset provenance.
- Aggregated _matches.tsv contains rows from all five domains (verify unique domain identifiers in output); no duplicate rows for identical spectrum–reference pairs across domains.
- JSON files (_domain.json) parse without schema errors and contain normalized keys matching the metadataMASST input schema (e.g., 'cosine_score', 'sample_id', 'domain_source').
- Row counts in _count_domain.tsv files sum correctly to total match count in _matches.tsv; spot-check 3–5 domain-specific counts by manual query to verify consistency.

## Limitations

- API integration requires Python 3.10; older or newer versions may encounter dependency conflicts with the Fast Search API client.
- Fast Search API calls may fail transiently; batch runs must be executed multiple times with `skip_existing=True` until no new outputs are generated; single-pass execution may miss matches.
- Output files generated reflect only currently indexed datasets (GNPS/MassIVE, Metabolomics Workbench, Metabolights, NORMAN); spectra in private repositories or not yet deposited in public repositories will not appear in aggregated results.
- metadataMASST aggregation performs normalization but does not resolve conflicts or re-rank results across domains; domain-specific matches with identical m/z and retention time may appear duplicated if scoring schemes differ between domains.

## Evidence

- [other] metadataMASST enables generation and visualization of aggregated search outputs across domain-specific MASST searches: "Aggregated search outputs can be generated and visualized using metadataMASST"
- [readme] Batch search integrates all five domain MASSTs simultaneously via Fast Search API: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench,"
- [other] Aggregation normalizes heterogeneous domain outputs into unified data structures: "Implement aggregation logic to combine heterogeneous search outputs from all domain sources into a single normalized data structure"
- [readme] Specific output files generated per domain and in aggregate: "A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html (e.g., _microbe.html)"
- [readme] Domain-specific MASST tools are under active development for five biological domains: "the different domain-specific MASSTs currently under development in the Dorrestein Lab at UC San Diego. This includes microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST"
- [readme] Python 3.10 is required for batch execution: "Please make user to use Python 3.10"
- [readme] Batch runs may require multiple passes due to transient API failures: "Make sure to run jobs.py _a couple of times_, until no new output is generated by having the option: `skip_existing=True`. Due to the Fast Search API some of the entries will fail"
