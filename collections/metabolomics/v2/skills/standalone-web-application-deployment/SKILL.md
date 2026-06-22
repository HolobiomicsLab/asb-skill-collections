---
name: standalone-web-application-deployment
description: Use when you have cloned the GNPS_MASST codebase and need to instantiate a domain-specific MASST variant (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, or foodMASST) to accept individual MS/MS spectra as input queries and perform searches against the corresponding curated reference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - microbeMASST
  - metadataMASST
  - GNPS_MASST
  - GNPS libraries
  - MZmine
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
---

# standalone-web-application-deployment

## Summary

Deploy domain-specific MASST standalone web applications that accept single mass spectra as input and perform searches against curated, domain-specific reference databases. This skill enables researchers to set up and validate spectral search infrastructure for microbe, plant, tissue, microbiome, or food metabolomics queries.

## When to use

Use this skill when you have cloned the GNPS_MASST codebase and need to instantiate a domain-specific MASST variant (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, or foodMASST) to accept individual MS/MS spectra as input queries and perform searches against the corresponding curated reference library indexed in that domain.

## When NOT to use

- Input spectra are already in a pre-computed similarity matrix or feature table format; deploy only if you need to execute new single-spectrum searches.
- You need to batch-process multiple spectra simultaneously; use the batch search workflow via jobs.py and the Fast Search API instead of the single-spectrum standalone web application.
- The target domain (microbe, plant, tissue, microbiome, food) is not covered by the available domainMASSTs; this skill applies only to those five domains currently under development.

## Inputs

- GNPS_MASST repository (source code)
- Domain-specific MASST repository (e.g., robinschmid/microbe_masst)
- Single MS/MS spectra in .mgf format or USI identifiers
- Domain-specific reference database index (microbe, plant, tissue, microbiome, or food lineage data)

## Outputs

- Deployed standalone web application instance accessible via web endpoint
- Interactive HTML tree files for domain-specific search results (e.g., _microbe.html)
- JSON files representing search result trees
- Aggregated _matches.tsv file with matched scans and metadata
- _library.tsv file with GNPS library matches for Level 2 annotation
- _datasets.tsv file with unique sample counts per indexed dataset
- Domain-specific _count_domain.tsv files with match counts per MASST

## How to apply

Clone both the GNPS_MASST repository (which contains the standalone web application framework) and the domain-specific implementation (e.g., robinschmid/microbe_masst for microbeMASST). Extract and configure the codebase to ensure spectral search indexing and domain-specific reference library integration are active. Deploy the standalone application to a web server or local environment to accept single-spectrum input queries. Configure search parameters such as minimum cosine score and m/z tolerance according to your analysis requirements. Validate that search outputs are correctly formatted and can be aggregated and visualized downstream using metadataMASST for cross-domain comparisons.

## Related tools

- **GNPS_MASST** (Provides the core standalone web application framework and spectral search indexing code for all domain-specific MASST deployments) — https://github.com/mwang87/GNPS_MASST
- **microbeMASST** (Domain-specific MASST implementation for microbial metabolomics; contains reference database configuration and taxonomic lineage data for 8 kingdoms, 20 phyla, 48 classes, 124 orders, 278 families, 561 genera, 1379 species, and 542 strains) — https://github.com/robinschmid/microbe_masst
- **metadataMASST** (Aggregates and visualizes search outputs across multiple domain-specific MASSTs for cross-domain comparative analysis)
- **GNPS libraries** (Reference spectral library integrated into the deployment to enable Level 2 annotation of matches) — https://library.gnps2.org/
- **MZmine** (Generates .mgf input files that can be searched against deployed standalone web applications) — https://github.com/mzmine/mzmine

## Evaluation signals

- Deployed web application responds to single-spectrum HTTP requests without error and returns search results within expected timeout
- Search result JSON structure matches the defined schema with interactive HTML tree visualization rendering without browser errors
- Output files (_matches.tsv, _library.tsv, _datasets.tsv, _count_domain.tsv) are generated and contain non-empty rows with expected column structure and metadata integrity
- Cosine similarity scores for matched spectra fall within the configured range (e.g., minimum cosine score threshold is respected in output filtering)
- Aggregated outputs can be successfully parsed and visualized by metadataMASST without data loss or format incompatibility

## Limitations

- The Fast Search API underlying batch searches may produce incomplete results on first run; multiple sequential re-runs with skip_existing=True are necessary to capture all possible matches across indexed data.
- Deployment requires Python 3.10 specifically; incompatible Python versions will cause execution failures.
- Standalone web applications accept only one spectrum at a time; batch processing of multiple spectra requires the separate jobs.py workflow and Fast Search API.
- Coverage is limited to five domains (microbe, plant, tissue, microbiome, food); other biological domains or specialized metabolite classes are not supported.
- Search results include all indexed spectra in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN, not only curated domain-specific samples; filtering by domain may be required downstream.

## Evidence

- [other] microbeMASST is implemented as a standalone web application that accepts individual mass spectra as input and performs searches against a microbe-specific reference database: "microbeMASST is implemented as a standalone web application that accepts individual mass spectra as input and performs searches against a microbe-specific reference database"
- [other] Clone the GNPS_MASST repository and domain-specific implementation, extract and configure codebase, deploy to accept single-spectrum input, and validate search outputs: "1. Clone the GNPS_MASST repository from https://github.com/mwang87/GNPS_MASST and the microbeMASST-specific implementation from github.com/robinschmid/microbe_masst. 2. Extract and configure the"
- [readme] The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST: "The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
- [readme] Aggregated search outputs can be generated and visualized using metadataMASST: "Aggregated search outputs can be generated and visualized using metadataMASST"
- [readme] Domain-specific MASSTs currently under development in the Dorrestein Lab include microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST: "This includes microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST"
- [readme] Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against current indexed data and generate multiple outputs for all listed domainMASSTs simultaneously: "Running [jobs.py](https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py) allows users to leverage the [Fast Search API](https://fasst.gnps2.org/fastsearch/) and execute a batch search"
- [readme] Check and adjust parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks: "Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks based on your research question"
- [readme] Make sure to run jobs.py a couple of times until no new output is generated, with skip_existing=True, because some entries may fail on the first run: "Make sure to run [jobs.py](https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py) **_a couple of times_**, until no new output is generated by having the option: `skip_existing=True`."
- [readme] Please make sure to use Python 3.10: "Please make user to use **_Python 3.10_**"
