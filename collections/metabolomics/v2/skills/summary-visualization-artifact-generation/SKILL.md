---
name: summary-visualization-artifact-generation
description: Use when you have completed batch spectral searches against multiple domain-specific MASST tools (via Fast Search API or individual domain searches) and need to combine and visualize the aggregated match results in a format compatible with metadataMASST web interface or downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
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
  - GNPS libraries
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
  - build: coll_microbemasst
    doi: 10.1038/s41564-023-01575-9
    title: microbemasst
  dedup_kept_from: coll_microbemasst
schema_version: 0.2.0
---

# summary-visualization-artifact-generation

## Summary

Generate interactive HTML trees, JSON structures, and TSV summary tables from aggregated multi-domain MASST search outputs to enable unified visualization and interpretation of spectrum matches across domain-specific databases. This skill consolidates fragmented search results from microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST into publication-ready artifacts.

## When to use

You have completed batch spectral searches against multiple domain-specific MASST tools (via Fast Search API or individual domain searches) and need to combine and visualize the aggregated match results in a format compatible with metadataMASST web interface or downstream analysis. Specifically, when you have search output files containing spectrum identifiers, cosine similarity scores, and metadata from one or more domain sources that must be merged into a unified summary.

## When NOT to use

- Your search results are from a single domain-specific MASST tool only and do not require cross-domain aggregation or unified visualization.
- Input data are already in a finalized visualization format (e.g., already rendered HTML or published figures).
- You need real-time interactive queries rather than batch-processed summary artifacts—use the standalone web apps directly instead.

## Inputs

- Search output JSON files from one or more domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST)
- MS/MS spectrum search results containing spectrum identifiers, cosine similarity scores, and metadata
- .mgf files or Universal Spectrum Identifiers (USIs) from prior batch searches
- GNPS Fast Search API response objects

## Outputs

- Interactive HTML tree files for each domain (_microbe.html, _plant.html, _tissue.html, _microbiome.html, _food.html)
- JSON tree structures for domain-specific results (_microbe.json, _plant.json, etc.)
- _matches.tsv: consolidated table of all matched scans across domains with spectrum identifiers and scores
- _library.tsv: matched spectra from GNPS libraries with MSI Level 2 annotation support
- _datasets.tsv: count of unique samples matching the query spectrum per indexed dataset
- _count_domain.tsv files: match counts and metadata for each domain-specific MASST

## How to apply

Load search output files from one or more domain-specific MASST runs (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) into a batch processing pipeline. Parse and normalize each result set to extract spectrum identifiers, match scores (typically cosine similarity), and domain-specific metadata fields. Aggregate results by merging records across domain sources into a unified tabular structure, then generate three categories of output artifacts: (1) interactive HTML tree visualizations for each domain (ending in _domain.html), (2) corresponding JSON tree structures (_domain.json), and (3) consolidated TSV tables (_matches.tsv containing all matched scans, _library.tsv with GNPS library identifiers for Level 2 annotation, _datasets.tsv with per-dataset match counts, and _count_domain.tsv for domain-specific match information). Validate aggregated outputs for completeness and consistency—ensure no records are lost during merge and that metadata fields are preserved across all domains. Use minimum cosine score, m/z tolerance, and minimum matching peaks thresholds as filtering parameters during aggregation, tuned to your research question.

## Related tools

- **metadataMASST** (Web interface for visualization and querying of aggregated cross-domain MASST search outputs) — https://masst.gnps2.org/metadatamasst/
- **GNPS_MASST** (Repository containing code for standalone web applications enabling single-spectrum searches; parent codebase for domain-specific tools) — https://github.com/mwang87/GNPS_MASST
- **Fast Search API** (Backend API used in jobs.py batch processing to execute rapid searches across indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN) — https://fasst.gnps2.org/fastsearch/
- **jobs.py** (Batch processing script that orchestrates searches across multiple domainMASSTs and generates all summary visualization artifacts) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py
- **microbeMASST** (Domain-specific MASST tool for microbial metabolomics; provides input search outputs for aggregation) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific MASST tool for plant metabolomics; provides input search outputs for aggregation) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific MASST tool for tissue metabolomics; provides input search outputs for aggregation) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific MASST tool for microbiome metabolomics; provides input search outputs for aggregation) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific MASST tool for food metabolomics; provides input search outputs for aggregation) — https://masst.gnps2.org/foodmasst2/
- **GNPS libraries** (Reference spectral library used to generate _library.tsv output with Level 2 metabolomics identifications) — https://library.gnps2.org/

## Examples

```
python code/jobs.py  # After adding entries to files list as ("input.mgf", "output/prefix") and setting minimum cosine score, mz tolerance, and minimum matching peaks parameters
```

## Evaluation signals

- All HTML tree files are generated for each requested domain and are interactive and renderable in a web browser without errors.
- Corresponding JSON files match the structure and content of HTML trees and are valid JSON that parses without schema errors.
- The _matches.tsv file contains all spectrum identifiers and cosine similarity scores from input searches with no duplicate rows and no data loss relative to input sources.
- The _library.tsv file contains matches to GNPS library spectra with accurate MSI Level 2 annotation identifiers.
- The _count_domain.tsv files show match counts that sum correctly to the total number of matches in _matches.tsv; no domain is missing or over-counted.
- Cross-validation: spot-check several spectra by manually verifying their matches and metadata fields are consistent across the TSV tables and HTML visualizations.

## Limitations

- Batch processing via jobs.py may experience transient failures with the Fast Search API; the README explicitly recommends running jobs.py multiple times with skip_existing=True until no new outputs are generated to ensure complete coverage.
- The skill requires Python 3.10 specifically; incompatible Python versions may cause runtime errors during artifact generation.
- Input can be .mgf files (from MZmine or GNPS molecular networking), or USIs provided via .csv or .tsv; other formats are not described as supported and will fail.
- Aggregation assumes consistent metadata schema across domain-specific MASST outputs; heterogeneous or malformed input metadata may lead to incomplete or inconsistent summary tables.
- The generated visualizations and tables represent matches against currently indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN; offline or custom reference databases are not described as supported.

## Evidence

- [readme] Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN and generate multiple outputs for all listed domainMASSTs simultaneously.: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench,"
- [readme] A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html; JSON files, _matches.tsv, _library.tsv, _datasets.tsv, and _count_domain.tsv files will be generated.: "A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html (e.g., _microbe.html)"
- [readme] _matches.tsv contains all the scans found to match your searched spectrum across indexed data, including samples not part of curated domain-specific MASSTs.: "A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed."
- [readme] _library.tsv enables Level 2 annotation according the Metabolomics Standards Initiative from GNPS library matches.: "A _library.tsv file will be generated. This contains a list of spectra from the GNPS libraries found to match your spectrum of interest. This enables a Level 2 annotation according the Metabolomics"
- [intro] metadataMASST accepts aggregated search outputs from one or more domain-specific MASST runs and produces visualizable summary artifacts.: "Aggregated search outputs can be generated and visualized using metadataMASST"
- [readme] Multiple domain-specific MASST tools ingest results which can be combined; users should run jobs.py multiple times until no new output is generated due to transient API failures.: "Make sure to run jobs.py **_a couple of times_**, until no new output is generated by having the option: `skip_existing=True`. Due to the Fast Search API some of the entries will fail."
- [readme] Input formats include .mgf files from MZmine or GNPS molecular networking, or Universal Spectrum Identifiers (USIs) provided via .csv or .tsv file.: "You can run either a single .mgf file generated via MZmine, from the molecular networking in GNPS workflow, or a list of USIs provided either via a .csv or .tsv file."
