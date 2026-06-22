---
name: repository-metadata-extraction
description: Use when when you need to inventory a collection of related web applications or tools distributed across multiple repositories, discover their live deployment URLs, trace their associated publications, and verify accessibility and metadata completeness.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3071
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - metadataMASST
  - GNPS_MASST
  - microbe_masst
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
- doi: 10.1101/2024.05.13.593988v1
  title: ''
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
- Aggregated search outputs can be generated and visualized using metadataMASST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma
    doi: 10.5702/massspectrometry.S0033
    title: magma
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# repository-metadata-extraction

## Summary

Extract and validate domain-specific tool URLs, associated publications, and metadata from repository README files and source code repositories. This skill systematically discovers live web application endpoints, peer-reviewed or preprint publication links, and taxonomic/data coverage information from structured repository documentation.

## When to use

When you need to inventory a collection of related web applications or tools distributed across multiple repositories, discover their live deployment URLs, trace their associated publications, and verify accessibility and metadata completeness. This is particularly valuable when a README lists multiple domain-specific or variant tools (e.g., microbeMASST, plantMASST, tissueMASST) and you need comprehensive, validated links for end-user or citation purposes.

## When NOT to use

- Input repository README is missing or inaccessible—cannot extract metadata without source documentation.
- Tools listed in README are outdated or deprecated—verification will fail; use historical archives (Internet Archive) if currency cannot be assumed.
- Publication links are incomplete or missing from README—extraction will produce null fields; do not invent DOIs or URLs.

## Inputs

- Repository README file (Markdown or plaintext)
- GitHub repository URL or Zenodo deposit URL
- Publication reference section or bibtex file from repository

## Outputs

- Structured inventory (CSV or JSON) with tool name, live URL, publication DOI, publication title, journal/platform, verification status
- Accessibility validation report (HTTP status codes, timestamp)
- Taxonomic or data coverage table (if applicable, e.g., lineage tables)

## How to apply

Begin by cloning or retrieving the primary repository (e.g., via Zenodo DOI or GitHub URL). Locate and parse the README file for explicit listings of standalone web applications, typically found in a section such as 'Standalone Web Apps' or 'Tools Available'. For each tool listed, extract the live URL (e.g., https://masst.gnps2.org/microbemasst/). Cross-reference each tool entry with associated publication links in a dedicated 'Publications' or 'How to cite' section, recording DOI, journal, and publication status (peer-reviewed vs. preprint). Validate accessibility by performing HTTP HEAD or GET requests to confirm each URL responds with a 2xx status code. For tools with lineage or taxonomic coverage metadata (e.g., tables documenting Kingdom, Phylum, Class, etc.), extract and structure this information. Compile results into a structured CSV or JSON inventory with columns for tool name, live URL, publication DOI/link, publication title, journal/preprint platform, and verification timestamp.

## Related tools

- **GNPS_MASST** (Source repository containing code for all domain-specific standalone web applications and batch search infrastructure) — https://github.com/mwang87/GNPS_MASST
- **microbe_masst** (Domain-specific repository containing batch search scripts (jobs.py) and lineage metadata tables for microbeMASST and plantMASST) — https://github.com/robinschmid/microbe_masst
- **microbeMASST** (Deployed web application endpoint for microbial metabolomics search) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Deployed web application endpoint for plant metabolomics search) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Deployed web application endpoint for tissue metabolomics search) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Deployed web application endpoint for microbiome metabolomics search) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Deployed web application endpoint for food metabolomics search) — https://masst.gnps2.org/foodmasst2/
- **metadataMASST** (Deployed web application for generating and visualizing aggregated search outputs) — https://masst.gnps2.org/metadatamasst/

## Examples

```
curl -I https://masst.gnps2.org/microbemasst/ && python -c "import csv; csv.DictWriter(open('masst_inventory.csv','w'), fieldnames=['tool','url','publication_doi','journal']).writeheader(); csv.DictWriter(open('masst_inventory.csv','a'), fieldnames=['tool','url','publication_doi','journal']).writerows([{'tool':'microbeMASST','url':'https://masst.gnps2.org/microbemasst/','publication_doi':'s41564-023-01575-9','journal':'Nature Microbiology'}])"
```

## Evaluation signals

- All listed tool URLs are accessible and return HTTP 200 status; verify via curl -I or requests library
- Each tool name in the inventory matches the corresponding README entry exactly (case-sensitive); no typos or aliases introduced
- Publication DOIs are valid and resolvable via crossref.org or doi.org; publication titles match official records
- Taxonomic or data coverage metadata extracted matches the source table structure (e.g., Kingdom, Phylum, Class columns preserved with correct counts)
- Inventory is complete: no tool listed in README is missing from the output; verify via row count comparison

## Limitations

- Zenodo deposits or GitHub repositories may be archived or deleted after publication; periodic re-validation is necessary to maintain link viability.
- Publication links embedded in README may reference preprints (bioRxiv, medRxiv) that later transition to peer-reviewed journals; extraction captures the link as documented, not the final published version.
- Some tools may have multiple versions or staging deployments (dev, staging, production); README may not clearly distinguish deployment environments; HTTP redirects should be followed and final endpoint recorded.
- Batch search scripts (jobs.py) require specific Python version (3.10 per README) and may fail or succeed inconsistently with the Fast Search API; this skill extracts metadata only, not executable validation.

## Evidence

- [readme] This repository contains the code and data for the different domain-specific MASSTs currently under development in the Dorrestein Lab at UC San Diego. This includes microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST.: "This repository contains the code and data for the different domain-specific MASSTs currently under development"
- [readme] Standalone Web Apps: 1. [microbeMASST](https://masst.gnps2.org/microbemasst/) 2. [plantMASST](https://masst.gnps2.org/plantmasst/) 3. [tissueMASST](https://masst.gnps2.org/tissuemasst/) 4. [microbiomeMASST](https://masst.gnps2.org/microbiomemasst/) 5. [foodMASST](https://masst.gnps2.org/foodmasst2/) 6. [metadataMASST](https://masst.gnps2.org/metadatamasst/): "Standalone Web Apps: 1. [microbeMASST](https://masst.gnps2.org/microbemasst/) ... 6. [metadataMASST](https://masst.gnps2.org/metadatamasst/)"
- [readme] Publications associated with the search tools: 1. [microbeMASST - Nature Microbiology](https://www.nature.com/articles/s41564-023-01575-9) 2. [plantMASST - bioRxiv](https://www.biorxiv.org/content/10.1101/2024.05.13.593988v1): "Publications associated with the search tools: 1. [microbeMASST - Nature Microbiology](https://www.nature.com/articles/s41564-023-01575-9)"
- [readme] Within the folder lineages you can find the complete lineage information of each NCBI taxonomy IDs used in microbeMASST and plantMASST.: "Within the folder lineages you can find the complete lineage information of each NCBI taxonomy IDs"
- [readme] The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in [GNPS_MASST](https://github.com/mwang87/GNPS_MASST): "The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
