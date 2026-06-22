---
name: spectral-search-result-aggregation
description: Use when when you have executed batch searches of MS/MS spectra against multiple domain-specific MASST indices and need to consolidate results across domains (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - metadataMASST
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - Fast Search API
  - jobs.py
  techniques:
  - MS-imaging
  - tandem-MS
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
evidence_spans:
- Aggregated search outputs can be generated and visualized using metadataMASST
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_microbemasst_cq
    doi: 10.1038/s41564-023-01575-9
    title: microbemasst
  dedup_kept_from: coll_microbemasst_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41564-023-01575-9
  all_source_dois:
  - 10.1038/s41564-023-01575-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-search-result-aggregation

## Summary

Aggregate and consolidate mass spectrometry spectral search results from multiple domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) into unified, cross-domain visualizations using metadataMASST. This skill enables interpretation of matches across biological domains by merging hits, scores, and metadata while generating interactive trees and summary statistics.

## When to use

When you have executed batch searches of MS/MS spectra against multiple domain-specific MASST indices and need to consolidate results across domains (e.g., microbe, plant, tissue, microbiome, food) to understand cross-domain metabolite distributions, identify domain overlap, or rank matches by aggregate score across curated taxonomic spaces.

## When NOT to use

- Input spectra are already annotated with compound identity at high confidence (Level 1 MSI standard); use this skill for discovery and cross-validation, not confirmation.
- You need single-domain, taxonomy-focused results only; use domain-specific MASST tools directly without aggregation.
- You require real-time, single-spectrum interactive search; use standalone web applications (masst.gnps2.org) instead of batch jobs.py.

## Inputs

- MS/MS spectra in .mgf format (e.g., from MZmine or GNPS molecular networking)
- Universal Spectrum Identifier (USI) lists in .csv or .tsv format
- Single spectrum query

## Outputs

- Interactive HTML tree files per domain (_microbe.html, _plant.html, _tissue.html, _microbiome.html, _food.html)
- JSON tree files per domain (_microbe.json, etc.)
- _matches.tsv: all indexed scans matching the queried spectrum(a)
- _library.tsv: GNPS library spectra matches (Level 2 annotation compatible)
- _datasets.tsv: unique sample counts per indexed dataset
- _count_domain.tsv files: per-domain match counts and domain-specific statistics

## How to apply

Execute batch spectral search using the Fast Search API (via jobs.py) against all indexed domainMASSTs simultaneously, specifying search parameters including minimum cosine score, m/z tolerance, and minimum matching peaks thresholds. metadataMASST then processes the aggregated domain-specific outputs by merging hits and scores across sources, consolidating metadata, and generating domain-separated interactive HTML tree visualizations (e.g., _microbe.html, _plant.html) alongside JSON exports and domain-specific count TSV files. Re-run the batch job iteratively (with skip_existing=True) to catch transient API failures and recover all possible matches. Validate aggregation by cross-referencing the _matches.tsv (all indexed scans), _library.tsv (GNPS library matches for Level 2 annotation), and _datasets.tsv (unique sample counts per indexed dataset) outputs against your input spectrum counts and expected domain coverage.

## Related tools

- **metadataMASST** (Consolidates aggregated search outputs from domain-specific MASSTs, merges hits/scores/metadata across domains, and generates cross-domain visualizations) — https://github.com/mwang87/GNPS_MASST
- **microbeMASST** (Domain-specific MASST tool providing curated microbial spectral database indexed by NCBI taxonomy; contributes to aggregated results) — https://github.com/robinschmid/microbe_masst
- **plantMASST** (Domain-specific MASST tool providing plant spectral database indexed by NCBI taxonomy; contributes to aggregated results) — https://github.com/robinschmid/microbe_masst
- **tissueMASST** (Domain-specific MASST tool for tissue metabolomes; contributes to aggregated results) — https://github.com/robinschmid/microbe_masst
- **microbiomeMASST** (Domain-specific MASST tool for microbiome samples; contributes to aggregated results) — https://github.com/robinschmid/microbe_masst
- **foodMASST** (Domain-specific MASST tool for food metabolomes; contributes to aggregated results) — https://github.com/robinschmid/microbe_masst
- **Fast Search API** (Backend API enabling batch search of multiple spectra against all indexed domainMASST data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN) — https://fasst.gnps2.org/fastsearch/
- **jobs.py** (Python script (Python 3.10 required) orchestrating batch spectral search across all domainMASSTs and generating aggregated outputs) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py

## Examples

```
python jobs.py  # After adding ("input.mgf", "output_prefix") to files list and setting cosine_score_threshold=0.6, mz_tolerance=0.1, min_matching_peaks=5
```

## Evaluation signals

- All input spectra (.mgf or USI list) are represented in the aggregated _matches.tsv and appear across one or more domain outputs with non-zero match counts
- Domain-specific HTML tree files render without errors and display hierarchical match organization; JSON equivalents are valid, parseable, and match tree structure
- _library.tsv contains matches with spectral library metadata (MSI Level 2 compatible); row count ≥ 0 and ≤ total matches
- _datasets.tsv aggregates unique sample counts correctly: sum of per-dataset counts ≤ total _matches.tsv rows (due to deduplication across domains)
- Re-running jobs.py with skip_existing=True produces no new outputs, confirming all transient API failures have been recovered

## Limitations

- Batch search via Fast Search API may experience transient failures; sequential re-runs (with skip_existing=True) are required to recover all matches, adding latency.
- Aggregation accuracy depends on current indexing of GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN; newly deposited spectra may not be immediately reflected.
- Domain overlap in _count_domain.tsv reflects only currently curated taxonomic lineages (microbeMASST: 561 genera, 1379 species; plantMASST: 1796 genera, 3712 species); uncurated organisms will route to _matches.tsv but not domain-specific trees.
- Cosine score threshold, m/z tolerance, and minimum matching peaks are user-configurable; suboptimal parameter choices may inflate false positives or miss true matches across domains.
- Python 3.10 is required; compatibility with other Python versions is not tested.

## Evidence

- [other] metadataMASST takes aggregated search outputs from domain-specific MASSTs and generates visualized aggregated results as its primary functional operation: "metadataMASST takes aggregated search outputs from domain-specific MASSTs (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST) and generates visualized aggregated results as its"
- [readme] Batch search workflow merges results, scores, and metadata across multiple domain sources: "Running [jobs.py]... allows users to leverage the [Fast Search API]... and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench,"
- [readme] Output structure includes domain-separated trees, comprehensive match list, library annotations, and per-dataset statistics: "A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html (e.g., _microbe.html)... A _matches.tsv file will be generated... A _library.tsv"
- [readme] Iterative re-runs are necessary due to transient API failures: "Make sure to run [jobs.py]... **_a couple of times_**, until no new output is generated by having the option: `skip_existing=True`. Due to the Fast Search API some of the entries will fail."
- [readme] User-configurable search parameters control aggregation sensitivity: "Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks based on your research question."
