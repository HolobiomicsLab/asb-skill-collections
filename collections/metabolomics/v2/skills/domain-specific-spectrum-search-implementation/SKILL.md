---
name: domain-specific-spectrum-search-implementation
description: Use when you have acquired one or more tandem MS/MS spectra and need
  to identify metabolites against a reference library filtered by biological domain
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - microbeMASST
  - metadataMASST
  - GNPS_MASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - Fast Search API
  - MZmine
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41538-022-00137-3
  title: foodMASST
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
- Aggregated search outputs can be generated and visualized using metadataMASST
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

# domain-specific-spectrum-search-implementation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Deploy a standalone web application that enables single-spectrum mass spectrometry searches against a curated, domain-specific reference database (e.g., microbial, plant, or tissue metabolomes). This skill bridges spectral acquisition to taxonomically or ecologically informed metabolite identification by integrating domain-specific indexing and search infrastructure.

## When to use

You have acquired one or more tandem MS/MS spectra and need to identify metabolites against a reference library filtered by biological domain (e.g., you have a microbial sample and want to search only against microbeMASST's curated microbial metabolome, or a plant tissue sample against plantMASST). Use this skill when single-spectrum queries must be run through a web interface or standalone application and you require outputs formatted for downstream taxonomic interpretation or aggregation across multiple domains.

## When NOT to use

- Your spectra have already been pre-searched and annotated against a general (non-domain-specific) library; use domain-specific search only when taxonomic or ecological filtering adds value to your research question.
- You require real-time interactive querying of the entire GNPS/MassIVE database without domain filtering; use the generic MASST or Fast Search API directly instead.
- Your input is already a feature table or abundance matrix rather than raw MS/MS spectra in .mgf or USI format.

## Inputs

- Single or multiple MS/MS spectra (.mgf file format or Universal Spectrum Identifier (USI) list as .csv/.tsv)
- Domain-specific reference library metadata (NCBI taxonomy IDs, strain/species lineage information)
- Search parameters: minimum cosine similarity score, m/z tolerance, minimum matching peaks

## Outputs

- Interactive HTML tree file for domain-specific MASST results (e.g., _microbe.html, _plant.html)
- JSON tree file with hierarchical domain-specific search results
- _matches.tsv: all matching spectra with scores and metadata
- _library.tsv: Level 2 annotations from GNPS library matches
- _datasets.tsv: count of unique samples per indexed dataset
- _count_domain.tsv: match counts per domain-specific MASST

## How to apply

Clone the GNPS_MASST repository (https://github.com/mwang87/GNPS_MASST) to obtain the standalone web application code, then integrate domain-specific reference data and indexing from the corresponding domainMASST implementation (e.g., robinschmid/microbe_masst for microbeMASST). Configure the spectral search indexer to load the curated domain-specific reference library and set search parameters (minimum cosine similarity score, m/z tolerance, minimum matching peaks). Deploy the application to accept single MS/MS spectrum input as .mgf or USI format. Execute the search and validate that output includes annotated matches with cosine scores, taxonomic metadata where applicable, and formatted results compatible with metadataMASST for aggregation and visualization. Repeat searches across multiple spectra as needed and run batch jobs multiple times with skip_existing=True until convergence, as the underlying Fast Search API may encounter transient failures.

## Related tools

- **GNPS_MASST** (source repository containing core standalone web application code for all domain-specific MASSTs) — https://github.com/mwang87/GNPS_MASST
- **microbeMASST** (domain-specific implementation for microbial metabolome searches; deployed web app at masst.gnps2.org/microbemasst/) — https://github.com/robinschmid/microbe_masst
- **plantMASST** (domain-specific implementation for plant metabolome searches; deployed at masst.gnps2.org/plantmasst/)
- **tissueMASST** (domain-specific implementation for tissue metabolome searches; deployed at masst.gnps2.org/tissuemasst/)
- **microbiomeMASST** (domain-specific implementation for microbiome metabolome searches; deployed at masst.gnps2.org/microbiomemasst/)
- **foodMASST** (domain-specific implementation for food metabolome searches; deployed at masst.gnps2.org/foodmasst2/)
- **metadataMASST** (aggregation and visualization tool for outputs from multiple domain-specific MASSTs; deployed at masst.gnps2.org/metadatamasst/)
- **Fast Search API** (backend search infrastructure used for batch queries against indexed GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN data) — https://fasst.gnps2.org/fastsearch/
- **MZmine** (optional upstream tool for generating .mgf spectrum files suitable as input to batch jobs) — https://github.com/mzmine/mzmine

## Examples

```
python jobs.py  # after editing the files list with ('input_spectra.mgf', 'output_prefix') and setting search parameters (min_cosine=0.7, mz_tolerance=0.1, min_matching_peaks=6)
```

## Evaluation signals

- Search outputs are returned in all expected file formats: _domain.html, _domain.json, _matches.tsv, _library.tsv, _datasets.tsv, and _count_domain.tsv.
- Cosine similarity scores in _matches.tsv meet or exceed the configured minimum threshold; matches are sorted by descending score.
- Taxonomic lineage information (kingdom, phylum, class, order, family, genus, species, strain) for microbial or plant matches is correctly populated and indexed according to the domain-specific lineage table.
- Re-running jobs.py with skip_existing=True produces no new output files, indicating convergence and successful retry of transient Fast Search API failures.
- Output matches can be successfully parsed and visualized by metadataMASST without format errors.

## Limitations

- The Fast Search API encounters transient failures; the README recommends running jobs.py multiple times with skip_existing=True until no new output is generated, which increases total execution time.
- Batch searches are limited to spectra available in currently indexed public repositories (GNPS/MassIVE, Metabolomics Workbench, Metabolights, NORMAN); unpublished or private spectra cannot be searched.
- Domain-specific coverage is incomplete: as of the README, microbeMASST covers 8 kingdoms, 20 phyla, 48 classes, 124 orders, 278 families, 561 genera, 1379 species, and 542 strains; plantMASST covers only 1 kingdom, 1 phylum, 11 classes, 81 orders, 319 families, 1796 genera, and 3712 species. Metabolites from uncovered taxa will not be found.
- Python 3.10 is required for batch job execution; compatibility with other Python versions is not documented.
- Single-spectrum web app interface does not support bulk USI uploads; batch USI search requires use of jobs.py script.

## Evidence

- [other] microbeMASST is implemented as a standalone web application that accepts individual mass spectra as input and performs searches against a microbe-specific reference database: "microbeMASST is implemented as a standalone web application that accepts individual mass spectra as input and performs searches against a microbe-specific reference database"
- [other] Clone the GNPS_MASST repository and extract and configure the microbeMASST standalone web application codebase, ensuring spectral search indexing and domain-specific reference library integration.: "Clone the GNPS_MASST repository from https://github.com/mwang87/GNPS_MASST and the microbeMASST-specific implementation from github.com/robinschmid/microbe_masst. Extract and configure the"
- [readme] The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST: "The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
- [readme] Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN and generate multiple outputs for all listed domainMASSTs simultaneously.: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench,"
- [readme] A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed.: "A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed."
- [readme] Aggregated search outputs can be generated and visualized using metadataMASST: "Aggregated search outputs can be generated and visualized using metadataMASST"
- [readme] You can run either a single .mgf file generated via MZmine, from the molecular networking in GNPS workflow, or a list of USIs provided either via a .csv or .tsv file.: "You can run either a single .mgf file generated via MZmine, from the molecular networking in GNPS workflow, or a list of USIs provided either via a .csv or .tsv file."
- [readme] Make sure to run jobs.py a couple of times, until no new output is generated by having the option: skip_existing=True. Due to the Fast Search API some of the entries will fail.: "Make sure to run jobs.py a couple of times, until no new output is generated by having the option: skip_existing=True. Due to the Fast Search API some of the entries will fail."
- [readme] microbeMASST and plantMASST lineage coverage includes taxonomy from kingdom down to strain level: "Within the folder lineages you can find the complete lineage information of each NCBI taxonomy IDs used in microbeMASST and plantMASST."
