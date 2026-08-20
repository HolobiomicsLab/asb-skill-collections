---
name: url-validation-and-accessibility-verification
description: Use when when compiling or maintaining a catalog of web-accessible scientific
  tools (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3071
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - metadataMASST
  - GNPS_MASST
  license_tier: open
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# URL Validation and Accessibility Verification

## Summary

Systematically verify that documented live URLs for scientific web applications are syntactically valid and respond correctly to HTTP requests. This skill ensures resource inventory accuracy and discoverability in scientific repositories.

## When to use

When compiling or maintaining a catalog of web-accessible scientific tools (e.g., standalone web applications, databases, dashboards) extracted from repository documentation, and you need to confirm that documented URLs are live, accessible, and return expected HTTP status codes before publishing or ingesting them into downstream systems.

## When NOT to use

- Input URLs are already validated and stored in a live database or CI/CD pipeline with automated health checks.
- The task is to validate HTML structure or semantic content of a webpage (not just HTTP accessibility).
- URLs are behind authentication or rate-limiting that requires credentials or API keys not provided in the context.

## Inputs

- Repository README file or structured metadata document listing tool names and their documented live URLs
- List of URLs as plain text, CSV, or JSON (e.g., domain-specific MASST tool URLs)
- Optional: expected HTTP status codes or redirect patterns per tool

## Outputs

- Structured inventory file (CSV or JSON) with columns: application name, documented URL, resolved URL, HTTP status code, verification timestamp, accessibility status (PASS/FAIL/REDIRECT)
- Log or report of inaccessible or invalid URLs requiring manual intervention
- Summary statistics (e.g., % of verified URLs, count of redirects or errors)

## How to apply

For each URL extracted from repository documentation (e.g., README, publication metadata), perform the following validation steps: (1) Check syntactic validity of the URL (scheme, domain, path structure conform to RFC 3986). (2) Attempt an HTTP HEAD or GET request to each URL with a timeout threshold (e.g., 10 seconds) to confirm server availability. (3) Record the HTTP status code returned (expect 200 or 3xx redirects for valid resources). (4) If a redirect is encountered, follow and validate the final destination URL. (5) Document verification timestamp, status code, and any error messages in a structured inventory (CSV or JSON) with columns for tool name, documented URL, final resolved URL (if redirected), HTTP status, and verification status. (6) Flag any non-2xx responses or timeouts as requiring manual review before publication.

## Related tools

- **microbeMASST** (Live web application URL to be validated (example: https://masst.gnps2.org/microbemasst/))
- **plantMASST** (Live web application URL to be validated (example: https://masst.gnps2.org/plantmasst/))
- **tissueMASST** (Live web application URL to be validated (example: https://masst.gnps2.org/tissuemasst/))
- **microbiomeMASST** (Live web application URL to be validated (example: https://masst.gnps2.org/microbiomemasst/))
- **foodMASST** (Live web application URL to be validated (example: https://masst.gnps2.org/foodmasst2/))
- **metadataMASST** (Live web application URL to be validated (example: https://masst.gnps2.org/metadatamasst/))
- **GNPS_MASST** (Source repository containing code and documentation for domain-specific MASST applications) — https://github.com/mwang87/GNPS_MASST

## Examples

```
python -c "import requests; urls = ['https://masst.gnps2.org/microbemasst/', 'https://masst.gnps2.org/plantmasst/']; results = [(url, requests.head(url, timeout=10).status_code) for url in urls]; print(results)"
```

## Evaluation signals

- All documented URLs conform to valid URL syntax (RFC 3986 compliant domain, scheme, and path).
- Each URL returns HTTP status 200 OK or expected 3xx redirect status within timeout threshold (e.g., ≤10 seconds).
- Redirects are followed to their final destination and the final URL is also responsive.
- Inventory file contains complete and consistent entries for all tool names mentioned in the source README.
- No URLs are duplicated or have conflicting status codes across verification runs (consistency check).

## Limitations

- URLs may be behind rate-limiting, authentication, or CORS policies that prevent automated validation without credentials.
- Transient network failures or temporary server downtime may produce false negatives; multiple retry attempts may be necessary.
- Some URLs may redirect through multiple hops or employ caching, making verification timestamps ephemeral.
- Validation does not confirm semantic correctness of page content, only HTTP-level accessibility.

## Evidence

- [other] Verify that each URL is accessible and responds correctly: "Validate that each URL is accessible and responds correctly."
- [other] Structured inventory with tool name, live URL, publication, and verification status: "Compile extracted data into a structured inventory file (CSV or JSON) with columns for application name, live URL, publication DOI/link, and verification status."
- [readme] Six documented domain-specific MASST web applications with live URLs: "Standalone Web Apps:
1. [microbeMASST](https://masst.gnps2.org/microbemasst/)
2. [plantMASST](https://masst.gnps2.org/plantmasst/)
3. [tissueMASST](https://masst.gnps2.org/tissuemasst/)
4."
- [readme] Publication metadata linked to each domain-specific MASST tool: "Publications associated with the search tools:
1. [microbeMASST - Nature Microbiology](https://www.nature.com/articles/s41564-023-01575-9)
2. [plantMASST - bioRxiv]"
