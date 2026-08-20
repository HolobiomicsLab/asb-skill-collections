---
name: web-application-documentation-mining
description: Use when you have access to a project README or repository documentation
  (Zenodo deposit, GitHub, or local clone) describing multiple domain-specific web
  applications, and you need to produce a machine-readable inventory of those applications
  with verified live URLs and associated publications for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3346
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3361
  - http://edamontology.org/topic_3520
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - metadataMASST
  - GNPS_MASST
  - jobs.py
  - Fast Search API
  - MZmine
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
- doi: 10.1101/2024.05.13.593988v1
  title: ''
- doi: 10.1101/2025.04.28.651123v1.abstract
  title: ''
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
- Aggregated search outputs can be generated and visualized using metadataMASST
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41564-023-01575-9
  all_source_dois:
  - 10.1038/s41564-023-01575-9
  - 10.1101/2024.05.13.593988v1
  - 10.1101/2025.04.28.651123v1.abstract
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Web Application Documentation Mining

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and validate metadata (URLs, publications, tool descriptions, and parameters) from project README files and repository documentation to create a structured inventory of domain-specific web applications and their capabilities. This skill enables systematic discovery and verification of live deployment URLs, associated peer-reviewed publications, and supported search parameters.

## When to use

You have access to a project README or repository documentation (Zenodo deposit, GitHub, or local clone) describing multiple domain-specific web applications, and you need to produce a machine-readable inventory of those applications with verified live URLs and associated publications for citation, reproducibility tracking, or tool integration into a larger workflow.

## When NOT to use

- The project documentation is outdated or the README explicitly states tools are 'under development' and not yet publicly deployed; prioritize contacting the development team instead.
- Live URLs are not provided in the README and must be reverse-engineered from source code; this exceeds the scope of documentation mining.
- Your goal is to extract source code parameters or algorithm details rather than enumerate deployed tool instances; use code inspection or technical paper review instead.

## Inputs

- Repository README file (Markdown or plaintext)
- Repository source code directory (e.g., GitHub clone or Zenodo deposit archive)
- Project metadata files (CITATION files, setup.py, package.json)

## Outputs

- Structured inventory file (CSV or JSON) with columns: application name, live URL, publication DOI, publication link, supported input formats, taxonomy/lineage coverage, verification status
- HTML summary report of accessible web applications and their associated publications
- Validated URL list with HTTP response codes

## How to apply

Clone or retrieve the target repository from its GitHub or Zenodo source. Locate and parse the README file to identify all documented standalone web applications, extracting the application name, live URL (e.g., https://masst.gnps2.org/microbemasst/), and any associated peer-reviewed or preprint publication links. For batch-search or parameter-driven applications, also extract key parameters (e.g., minimum cosine score, m/z tolerance, minimum matching peaks) and input file formats (.mgf, .csv, .tsv, USI format). Validate that each URL is accessible and responds correctly with HTTP 200. Compile extracted data into a structured inventory (CSV or JSON) with columns for application name, live URL, publication DOI/link, supported input formats, and verification status. Cross-reference lineage or taxonomy coverage tables if present in the documentation.

## Related tools

- **microbeMASST** (Domain-specific web application for microbial metabolomics search; primary example tool documented in README) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific web application for plant metabolomics search; enumerated in README with bioRxiv publication link) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific web application for tissue metabolomics search; documented with preprint publication) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific web application for microbiome metabolomics search; listed with bioRxiv preprint) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific web application for food metabolomics search; documented with npj Science of Food publication) — https://masst.gnps2.org/foodmasst2/
- **metadataMASST** (Web application for aggregating and visualizing search outputs across domain-specific MASSTs) — https://masst.gnps2.org/metadatamasst/
- **GNPS_MASST** (Source code repository containing standalone web application implementations for all domain-specific MASSTs) — https://github.com/mwang87/GNPS_MASST
- **jobs.py** (Batch search script that executes multiple spectra searches against indexed data using Fast Search API with configurable parameters (cosine score, m/z tolerance, minimum matching peaks)) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py
- **Fast Search API** (Backend API service used by batch search workflows to query GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN databases) — https://fasst.gnps2.org/fastsearch/
- **MZmine** (Upstream tool for generating .mgf spectrum files suitable as input to batch search workflows) — https://github.com/mzmine/mzmine

## Examples

```
python jobs.py --input input_directory/spectra.mgf --output output_directory/results --min_cosine 0.7 --mz_tolerance 0.1 --min_peaks 6
```

## Evaluation signals

- All extracted URLs resolve to live web applications (HTTP 200 response); non-functional URLs are flagged for manual review
- Publication links (DOI, bioRxiv, Nature URLs) are valid and correspond to the stated tool names and release years
- Structured inventory is machine-parseable (valid JSON or well-formed CSV with no missing required fields)
- Taxonomy/lineage coverage tables (if present) are fully extracted and match the stated tool scope (e.g., microbeMASST covers 8 kingdoms, 1379 species; plantMASST covers 3712 species)
- Input format documentation (e.g., '.mgf files generated via MZmine', 'USI format .csv/.tsv', Python 3.10 requirement) is captured in a separate parameters field for batch workflows

## Limitations

- README documentation may be incomplete or outdated; live URLs may move or applications may be retired without README update. Manual verification of accessibility is required.
- Publication links in README may point to preprints (bioRxiv) rather than peer-reviewed versions; you may need to track version progression separately.
- Batch search parameter defaults (minimum cosine score, m/z tolerance, minimum matching peaks) are not always documented in README; extraction may require inspection of source code (e.g., jobs.py) or contact with authors.
- Some tools (e.g., microbiomeMASST) reference incomplete or placeholder publication links; verify URLs before citing.
- Taxonomy lineage tables cover only some tools (microbeMASST and plantMASST documented; tissueMASST, microbiomeMASST, foodMASST coverage not explicitly tabulated in README).

## Evidence

- [readme] This repository contains the code and data for the different domain-specific MASSTs currently under development in the Dorrestein Lab at UC San Diego. This includes microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST.: "This repository contains the code and data for the different domain-specific MASSTs currently under development in the Dorrestein Lab at UC San Diego. This includes microbeMASST, plantMASST,"
- [readme] Standalone Web Apps: 1. [microbeMASST](https://masst.gnps2.org/microbemasst/) 2. [plantMASST](https://masst.gnps2.org/plantmasst/) 3. [tissueMASST](https://masst.gnps2.org/tissuemasst/) 4. [microbiomeMASST](https://masst.gnps2.org/microbiomemasst/) 5. [foodMASST](https://masst.gnps2.org/foodmasst2/) 6. [metadataMASST](https://masst.gnps2.org/metadatamasst/): "Standalone Web Apps: 1. [microbeMASST](https://masst.gnps2.org/microbemasst/) 2. [plantMASST](https://masst.gnps2.org/plantmasst/) 3. [tissueMASST](https://masst.gnps2.org/tissuemasst/)"
- [readme] Publications associated with the search tools: 1. [microbeMASST - Nature Microbiology](https://www.nature.com/articles/s41564-023-01575-9) 2. [plantMASST - bioRxiv](https://www.biorxiv.org/content/10.1101/2024.05.13.593988v1) 3. [tissueMASST - bioRxiv](https://www.biorxiv.org/content/10.1101/2025.04.28.651123v1.abstract) 5. [foodMASST - npj Science of Food](https://www.nature.com/articles/s41538-022-00137-3): "Publications associated with the search tools: 1. [microbeMASST - Nature Microbiology](https://www.nature.com/articles/s41564-023-01575-9)"
- [readme] Running [jobs.py](https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py) allows users to leverage the [Fast Search API](https://fasst.gnps2.org/fastsearch/) and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN and generate multiple outputs for all listed domainMASSTs simultaneously.: "Running [jobs.py] allows users to leverage the [Fast Search API] and execute a batch search of multiple MS/MS spectra against the current indexed data"
- [readme] Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks based on your research question.: "Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks"
- [readme] Within the folder lineages you can find the complete lineage information of each NCBI taxonomy IDs used in microbeMASST and plantMASST. These tools currently cover | microbeMASST | 8 | 20 | 48 | 124 | 278 | 561 | 1379 | 542 |: "Within the folder lineages you can find the complete lineage information of each NCBI taxonomy IDs used in microbeMASST and plantMASST"
