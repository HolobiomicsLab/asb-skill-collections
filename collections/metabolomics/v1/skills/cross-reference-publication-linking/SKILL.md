---
name: cross-reference-publication-linking
description: Use when when cataloging a suite of related bioinformatics tools or web applications (particularly in domains like metabolomics, microbiology, or systems biology) and you need to establish the authoritative peer-reviewed or preprint publication for each tool, verify publication URLs are live, and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0089
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - metadataMASST
  - GNPS_MASST
  - robinschmid/microbe_masst
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_microbemasst
    doi: 10.1038/s41564-023-01575-9
    title: microbemasst
  dedup_kept_from: coll_microbemasst
schema_version: 0.2.0
---

# cross-reference-publication-linking

## Summary

Extract and validate peer-reviewed or preprint publications associated with domain-specific bioinformatics tools from repository documentation, then verify accessibility and linkage integrity. This skill ensures that scientific tools are properly attributed to their originating research and that publication metadata is current and retrievable.

## When to use

When cataloging a suite of related bioinformatics tools or web applications (particularly in domains like metabolomics, microbiology, or systems biology) and you need to establish the authoritative peer-reviewed or preprint publication for each tool, verify publication URLs are live, and document the publication status (peer-reviewed vs. preprint) to support reproducibility claims and proper citation.

## When NOT to use

- When tools are documented only in peer-reviewed methods papers without a separate code repository README — use the methods paper as the primary source instead.
- When publication metadata is intentionally withheld (e.g., embargo period); defer cross-referencing until embargo lifts.
- When validating tool functionality or benchmark performance — this skill only validates publication metadata linkage, not scientific correctness or computational results.

## Inputs

- Repository README file (markdown or text format)
- Tool/application enumeration list with documented publication metadata
- Publication URLs or DOI identifiers

## Outputs

- Structured inventory file (CSV or JSON) with tool name, publication title, venue, URL, DOI, and verification status
- HTTP response code validation report (200/30x = accessible; 404+ = dead link)
- Publication metadata record (title, authors, year, journal/preprint server, peer-review status)

## How to apply

Retrieve the README or primary documentation file from the source repository and systematically parse sections listing tools or applications. For each tool, extract the associated publication link (DOI, URL, or both) and publication venue. Cross-validate each URL by performing a HEAD or GET request to confirm HTTP 200 or 30x response codes. Record the publication status (e.g., 'Nature Microbiology' = peer-reviewed; 'bioRxiv' = preprint). Compile results into a structured inventory (CSV or JSON) with columns for tool name, publication title, publication venue, publication URL, publication DOI (if available), peer-review status, and verification timestamp. Flag any 404 or unreachable links, and note cases where a tool is listed but no publication is documented.

## Related tools

- **microbeMASST** (Domain-specific mass spectrometry search tool for microbial metabolomics; primary example in the source card) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific mass spectrometry search tool for plant metabolomics; example in publication inventory) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific mass spectrometry search tool for tissue metabolomics; example in publication inventory) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific mass spectrometry search tool for microbiome metabolomics; example in publication inventory) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific mass spectrometry search tool for food metabolomics; example in publication inventory) — https://masst.gnps2.org/foodmasst2/
- **metadataMASST** (Aggregation and visualization tool for outputs from domain-specific MASSTs; example in publication inventory) — https://masst.gnps2.org/metadatamasst/
- **GNPS_MASST** (Source code repository containing implementation of all standalone MASST web applications) — https://github.com/mwang87/GNPS_MASST
- **robinschmid/microbe_masst** (Secondary repository containing batch search utilities and lineage data for microbeMASST and plantMASST) — https://github.com/robinschmid/microbe_masst

## Evaluation signals

- All tools enumerated in the README have at least one associated publication link in the 'Publications associated with the search tools' section; no tools listed without metadata.
- Each publication URL resolves to HTTP 200 or 30x response (redirect accepted); no 404, 403, or timeout responses.
- Publication venues are correctly classified as peer-reviewed (Nature Microbiology, npj Science of Food) or preprint (bioRxiv) based on the domain of the URL.
- Inventory file schema is complete and consistent: every row has non-empty tool name, publication URL, and verification status; DOI or title columns are populated where available in the source.
- Timestamps on verification are recent (within 30 days) and include HTTP response code and round-trip time for transparency; no stale or undated entries.

## Limitations

- Publication metadata in the README may become outdated if a preprint (bioRxiv) is later published in a peer-reviewed venue; periodic re-verification is recommended.
- Some publications may move, be retracted, or have access restrictions (paywall, institutional login) that prevent full-text access even if the URL is technically reachable; HTTP validation only confirms server response, not content integrity.
- The README does not list DOI identifiers for all publications, only URLs; if DOI is required for citation metadata, additional lookup (e.g., via Crossref API) may be necessary.
- Preprint servers (bioRxiv) may update abstracts or metadata after initial indexing; URL stability is generally good but version anchoring (e.g., 'v1.abstract') in the README should be preserved to avoid drift.

## Evidence

- [readme] Standalone Web Apps: 1. microbeMASST 2. plantMASST 3. tissueMASST 4. microbiomeMASST 5. foodMASST 6. metadataMASST: "Standalone Web Apps:
1. [microbeMASST](https://masst.gnps2.org/microbemasst/)
2. [plantMASST](https://masst.gnps2.org/plantmasst/)"
- [readme] Publications associated with the search tools are enumerated with links and venues: "Publications associated with the search tools:
1. [microbeMASST - Nature Microbiology](https://www.nature.com/articles/s41564-023-01575-9)"
- [readme] The README documents six domain-specific MASST applications each with live URLs and associated publications: "This repository contains the code and data for the different domain-specific MASSTs currently under development in the Dorrestein Lab at UC San Diego. This includes microbeMASST, plantMASST,"
- [other] Extracting and validating URLs from repository README against a structured inventory: "Compile extracted data into a structured inventory file (CSV or JSON) with columns for application name, live URL, publication DOI/link, and verification status."
- [readme] Preprint and peer-reviewed publications are both documented in the publication list: "2. [plantMASST - bioRxiv](https://www.biorxiv.org/content/10.1101/2024.05.13.593988v1)
5. [foodMASST - npj Science of Food](https://www.nature.com/articles/s41538-022-00137-3)"
