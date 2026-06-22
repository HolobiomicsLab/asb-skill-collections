---
name: api-response-error-handling
description: Use when when building asynchronous metadata enrichment workflows that call multiple external APIs (CIR, CTS, PubChem, IDSM, BridgeDb) to annotate mass spectra .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MSMetaEnhancer
  - Python
  - pytest
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- '**MSMetaEnhancer** is a tool used for `.msp` files annotation'
- '`MSMetaEnhancer/libs/converters/web/` named after your service'
- 'MSMetaEnhancer: A Python package for mass spectra metadata annotation'
- Create a new Python file in `MSMetaEnhancer/libs/converters/web/`
- make sure the existing tests still work by running ``pytest``
- 'fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer_cq
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.04494
  all_source_dois:
  - 10.21105/joss.04494
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# API Response Error Handling

## Summary

Implement robust error handling in metadata annotation pipelines to gracefully manage API failures, rate limits, and malformed responses from distributed chemical databases. This skill ensures data quality and pipeline resilience when fetching SMILES, InChI, CAS numbers, and other structural annotations from external web services.

## When to use

When building asynchronous metadata enrichment workflows that call multiple external APIs (CIR, CTS, PubChem, IDSM, BridgeDb) to annotate mass spectra .msp files, and you need to prevent a single API failure or rate limit from halting the entire annotation process or corrupting output files.

## When NOT to use

- Input is a static, pre-validated metadata table with no external API dependencies.
- The workflow requires real-time synchronous responses and cannot tolerate queuing or retry delays.
- All annotation services are guaranteed to have 100% uptime and zero rate limiting (rare in practice).

## Inputs

- .msp mass spectra files with partial metadata (e.g., compound names, CAS numbers)
- API endpoint specifications and rate limit documentation for each service
- Job configurations defining input-to-output attribute mappings (e.g., 'name' → 'inchi' via IDSM)

## Outputs

- Annotated .msp files with successfully fetched metadata
- Structured error logs recording failed API calls (service, query, HTTP status, error type, timestamp)
- Validation report distinguishing successful, rate-limited, and malformed responses

## How to apply

Implement error handling at two levels: (1) service-level handlers that catch API timeouts, HTTP errors, and malformed JSON responses, returning empty dictionaries rather than propagating exceptions; (2) pipeline-level handlers that log error details (service name, query input, HTTP status, error message) and allow the annotation process to continue with remaining services. Use throttling mechanisms to respect API rate limits by implementing delays between requests or queue-based request scheduling. Validate response structure before parsing (check for expected fields, type consistency) and implement fallback logic where applicable (e.g., try CTS if CIR fails for a given query). Record all error events in structured logs alongside successful conversions to enable downstream validation auditing.

## Related tools

- **MSMetaEnhancer** (Asynchronous metadata annotation framework that executes error-prone API calls; error handling must integrate into its Job and Converter architecture) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Chemical structure service queried for SMILES and InChI conversion; subject to timeouts and rate limits) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Metabolomics standards database API; requires rate-limit-aware querying) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Large public chemical database API with strict rate limits and variable response formats) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Elixir chemical structure service; API responses must be parsed robustly) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Cross-database identifier mapping service; subject to network and parsing errors) — https://bridgedb.github.io/
- **pytest** (Unit testing framework for validating error handlers against synthetic API failures and rate-limit scenarios)
- **Python** (Primary implementation language for async error handling and logging infrastructure)

## Examples

```
# Implement error handler in converter:
class RobustConverter:
    def parse_response(self, response):
        try:
            data = response.json()
            if not data or 'error' in data:
                return {}
            return self.validate_fields(data)
        except (ValueError, KeyError, requests.Timeout):
            return {}

# Use in job loop with rate limiting:
import asyncio
for job in jobs:
    try:
        result = await service.convert(job['input'])
        validation_log.write(f"{job},result={result},status=ok")
    except Exception as e:
        validation_log.write(f"{job},error={e},status=failed")
        await asyncio.sleep(5)  # throttle before retry
```

## Evaluation signals

- Structured error logs contain all failed API calls with service name, HTTP status, and query input; log completeness validates error capture.
- Annotation pipeline continues processing remaining spectra and services after encountering an API error; absence of unhandled exceptions in stderr confirms graceful degradation.
- Output .msp file contains only validated metadata from successful responses; no malformed or partially-parsed values reach the file.
- Rate-limit errors are logged and throttling delays are applied; subsequent retries succeed within documented API quota windows.
- Unit tests using pytest cover at least: HTTP 4xx/5xx errors, timeout exceptions, malformed JSON responses, and empty/null fields in valid JSON; all error cases return empty dictionaries rather than raising exceptions.

## Limitations

- If all services are unavailable or heavily rate-limited, metadata enrichment will degrade to only locally-computable attributes (e.g., RDKit-based calculations).
- Logging all error details can produce large log files for high-throughput annotations; log rotation and archival policies must be established.
- Some APIs return HTTP 200 with error messages embedded in JSON bodies (e.g., 'not found' or 'invalid query'); these require application-level parsing and are not caught by status code checks alone.
- Retry logic with exponential backoff can delay annotation completion; timeout thresholds must balance resilience against user wait times.

## Evidence

- [other] Always handle API errors gracefully and return empty dictionaries when data is not available: "Always handle API errors gracefully and return empty dictionaries when data is not available"
- [other] Respect API rate limits using throttling mechanisms: "Respect API rate limits using throttling mechanisms"
- [other] Implement robust response parsing that handles various response formats: "Implement robust response parsing that handles various response formats"
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
- [other] MSMetaEnhancer implements attribute validation tracked in logs to check fetched annotation values before they are written back to spectra, ensuring data quality during the metadata enrichment process.: "MSMetaEnhancer implements attribute validation tracked in logs to check fetched annotation values before they are written back to spectra, ensuring data quality during the metadata enrichment process."
- [other] Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured validation report file.: "Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured validation report file."
