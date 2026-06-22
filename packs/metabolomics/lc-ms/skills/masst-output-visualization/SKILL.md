---
name: masst-output-visualization
description: Use when you have completed one or more domain-specific MASST searches (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) and have aggregated search outputs (matches.tsv, library.tsv, datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3379
  tools:
  - metadataMASST
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - jobs.py
  - GNPS_MASST
  - Fast Search API
  techniques:
  - LC-MS
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

# Reconstruct aggregated search output visualization with metadataMASST

## Summary

metadataMASST consolidates and visualizes aggregated mass spectrometry search results from domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) into cross-domain interpretable outputs. Use this skill when you have completed batch or single-spectrum searches across multiple domain-specific MASSTs and need to synthesize, rank, and visualize hits and metadata to identify domain overlap and score distributions.

## When to use

You have completed one or more domain-specific MASST searches (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) and have aggregated search outputs (matches.tsv, library.tsv, datasets.tsv, or domain-specific JSON/HTML trees) that need to be merged, ranked by cosine score, and visualized to reveal which domains and taxa match your query spectrum and how hits are distributed across them.

## When NOT to use

- You have only single-domain MASST results and no cross-domain comparison is needed; use domain-specific MASST tools directly instead.
- Your input is a single spectrum or USI and you have not yet run batch searches; use the individual domain-specific MASST web apps first.
- Your data is not mass spectrometry spectra (e.g., genomic or proteomic) or does not originate from GNPS/MassIVE, Metabolomics Workbench, Metabolights, or NORMAN; metadataMASST is designed for MS/MS spectral data aggregated from these sources.

## Inputs

- Aggregated domain-MASST search outputs (matches.tsv, library.tsv, datasets.tsv)
- Domain-specific JSON and HTML tree files (_microbe.json, _plant.json, etc.)
- _count_domain.tsv files with per-domain hit counts
- USI (Universal Spectrum Identifier) or .mgf batch search results

## Outputs

- Interactive HTML tree visualizations for each domain (_microbe.html, _plant.html, etc.)
- Merged JSON tree representations with score rankings and metadata
- Consolidated hit distribution visualizations across all queried domains
- Domain overlap and cross-domain match summaries in structured formats

## How to apply

Load all aggregated domain-MASST search outputs (typically from batch runs via jobs.py) into metadataMASST as input. metadataMASST parses and consolidates the hit lists, cosine scores, and NCBI taxonomy metadata from each domain source. The tool then generates interactive HTML tree visualizations (e.g., _domain.html files) and accompanying JSON representations that encode hit distribution, score rankings, and domain-specific overlap. Export the merged results in structured formats (HTML trees, JSON) with embedded or linked visualizations to enable cross-domain comparison and taxonomic interpretation. Verify that hits are deduplicated across domains and that score thresholds (default minimum cosine score applied during the upstream batch search) are consistently applied.

## Related tools

- **metadataMASST** (Primary visualization and aggregation tool for merging and visualizing cross-domain search outputs; generates HTML tree visualizations and JSON representations of hits, scores, and taxonomy metadata) — https://masst.gnps2.org/metadatamasst/
- **microbeMASST** (Domain-specific search tool for microbial spectra; produces aggregated outputs (matches.tsv, library.tsv, JSON, HTML) that feed into metadataMASST) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific search tool for plant spectra; produces domain-specific hits and taxonomy metadata fed to metadataMASST) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific search tool for tissue spectra; contributes domain hits to metadataMASST aggregation) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific search tool for microbiome spectra; provides domain-specific matches merged by metadataMASST) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific search tool for food spectra; contributes domain hits and metadata to metadataMASST visualization) — https://masst.gnps2.org/foodmasst2/
- **jobs.py** (Batch execution script that runs multiple spectra against all domain-specific MASSTs via Fast Search API; generates the aggregated outputs (matches.tsv, library.tsv, datasets.tsv, JSON, HTML) that are input to metadataMASST) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py
- **GNPS_MASST** (Parent codebase containing standalone web application code for all domain-specific MASSTs and metadataMASST) — https://github.com/mwang87/GNPS_MASST
- **Fast Search API** (Backend API used by jobs.py to execute batch searches of multiple spectra against indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN) — https://fasst.gnps2.org/fastsearch/

## Evaluation signals

- All aggregated domain-MASST outputs (matches.tsv, library.tsv, datasets.tsv, _count_domain.tsv files) are successfully parsed without missing or malformed entries.
- Interactive HTML tree visualizations are generated for each queried domain with interactive tree structure, cosine score ordering, and embedded NCBI taxonomy or domain metadata.
- JSON representations of merged results validate against expected schema and contain deduplicated hits across domains with no duplicate cosine scores for the same spectrum match.
- Hit counts and score distributions in the visualization match the source _count_domain.tsv and matches.tsv file statistics; domain overlap (spectra matching multiple domains) is correctly identified and displayed.
- Level 2 metabolomics annotations from library.tsv are embedded in the visualization output; export formats are structured (JSON, TSV, HTML) and linked or embedded visualizations load without errors.

## Limitations

- metadataMASST requires upstream batch execution via jobs.py to generate aggregated outputs; single-spectrum searches must be run through domain-specific MASST tools first.
- Fast Search API failures during batch runs may result in incomplete matches for some spectra; the README recommends running jobs.py multiple times with skip_existing=True to catch missed matches.
- Visualization quality and interpretability depend on the parameter tuning (minimum cosine score, m/z tolerance, minimum matching peaks) set during the upstream batch search; suboptimal thresholds may produce over- or under-represented domain overlaps.
- Domain-specific MASSTs currently cover only NCBI taxonomy curated for microbes (8 kingdoms, 1379 species) and plants (1 kingdom, 3712 species); other organisms or samples not in curated domain databases will appear only in the unfiltered matches.tsv, not in domain-specific visualizations.
- Python 3.10 is required to execute jobs.py; compatibility with other Python versions is not guaranteed.

## Evidence

- [other] metadataMASST takes aggregated search outputs from domain-specific MASSTs (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST) and generates visualized aggregated results: "metadataMASST takes aggregated search outputs from domain-specific MASSTs (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST) and generates visualized aggregated results as its"
- [readme] Aggregated search outputs can be generated and visualized using metadataMASST: "Aggregated search outputs can be generated and visualized using metadataMASST"
- [other] Process and consolidate search results using metadataMASST to merge hits, scores, and metadata across domain sources: "Process and consolidate search results using metadataMASST to merge hits, scores, and metadata across domain sources"
- [other] Generate visualization(s) of aggregated results (e.g., hit distribution, score rankings, domain overlap) to enable interpretation of cross-domain matches: "Generate visualization(s) of aggregated results (e.g., hit distribution, score rankings, domain overlap) to enable interpretation of cross-domain matches"
- [readme] A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html: "A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html (e.g., _microbe.html)"
- [readme] Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN: "Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN"
- [readme] A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum: "A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed"
- [readme] Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks: "Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks based on your research question"
