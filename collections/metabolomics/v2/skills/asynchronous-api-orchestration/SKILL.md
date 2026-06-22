---
name: asynchronous-api-orchestration
description: Use when you have a batch of mass spectra records in .msp format that lack standardized metadata fields (SMILES, InChI, CAS numbers, molecular formula, IUPAC names) and need to populate them by querying multiple independent web APIs in parallel.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MSMetaEnhancer
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - RDKit
  - asyncio
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
- 'fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer
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

# asynchronous-api-orchestration

## Summary

Coordinate multiple concurrent HTTP requests to heterogeneous web services (CIR, CTS, PubChem, IDSM, BridgeDb) to enrich mass spectra metadata in .msp files. This skill enables optimal fetching speed by dispatching conversion jobs asynchronously rather than sequentially.

## When to use

You have a batch of mass spectra records in .msp format that lack standardized metadata fields (SMILES, InChI, CAS numbers, molecular formula, IUPAC names) and need to populate them by querying multiple independent web APIs in parallel. Use this skill when sequential API calls would be prohibitively slow and when the target services support independent, stateless queries keyed on existing compound identifiers (e.g., compound name, InChI string).

## When NOT to use

- Input .msp file lacks any source attribute (e.g., compound name, InChI) that can be used to query external services—the APIs require at least one anchor field to initiate lookup.
- Target metadata fields are already present in ≥95% of records; annotation overhead outweighs marginal gain in coverage.
- External web services (CIR, CTS, PubChem, IDSM, BridgeDb) are currently unavailable or have strict rate limits incompatible with your batch size and timeout constraints.

## Inputs

- .msp mass spectra library file (NIST format) containing compound records with at least one source attribute (e.g., compound name or InChI)
- List of conversion job tuples: [(source_attr, target_attr, service), ...]
- List of service names to register: ['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit']

## Outputs

- Enriched .msp file with added metadata fields (SMILES, InChI, CAS number, molecular formula, IUPAC name, inchikey)
- Logger records capturing per-attribute conversion success/failure counts and fill-rate statistics
- Summary table with rows for each metadata field and columns for initial fill rate, final fill rate, and absolute gain

## How to apply

Register all target converter services (e.g., CTS, CIR, IDSM, PubChem, BridgeDb, RDKit) with the ConverterBuilder. Define a list of conversion jobs as tuples specifying (source_attribute, target_attribute, service_name)—for example, ('name', 'inchi', 'IDSM') to convert compound name to InChI. Invoke the Application.annotate_spectra() coroutine with the services list and jobs list; this dispatches all jobs asynchronously via asyncio. Each WebConverter subclass implements query_the_service() to make the HTTP request and parse_response() to extract the returned metadata. Aggregate results back into the spectra records and save to output .msp. Verify correctness by inspecting the Logger component's per-attribute fill-rate statistics before and after annotation.

## Related tools

- **MSMetaEnhancer** (Orchestrator application class that loads .msp files, dispatches async annotation jobs, and aggregates enriched metadata back into spectra records.) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Web service queried for SMILES-to-InChI and name-to-structure conversions.) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Web service queried for chemical structure conversions and standardized identifiers.) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Web service queried for compound metadata including SMILES, InChI, CAS numbers, and molecular properties.) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Web service queried for InChI-to-formula, InChI-to-inchikey, and InChI-to-IUPAC-name conversions.) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Web service queried for compound identifier mappings and database cross-references.) — https://bridgedb.github.io/
- **RDKit** (Local computational converter (non-web) used for chemistry informatics operations like SMILES validation and property computation.)
- **asyncio** (Python standard library used to dispatch and coordinate concurrent coroutines for parallel API queries.)

## Examples

```
import asyncio
from MSMetaEnhancer import Application
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder

ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
app = Application()
app.load_data('sample.msp', file_format='msp')
jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM')]
asyncio.run(app.annotate_spectra(['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit'], jobs))
app.save_data('sample_out.msp', file_format='msp')
```

## Evaluation signals

- Per-attribute fill-rate statistics computed by Logger show measurable gain (increase in non-null counts for SMILES, InChI, CAS, formula, IUPAC name fields) compared to baseline .msp file before annotation.
- Output .msp file contains no validation errors when re-parsed by MSMetaEnhancer Application class.
- Asynchronous execution time is significantly lower (wall-clock) than sequential execution would be; spot-check by comparing runtime logs.
- Randomly sample 10–20 enriched records and manually verify that returned SMILES, InChI, and CAS numbers are chemically consistent with the compound name (e.g., correct molecular weight, expected functional groups).
- All jobs in the job list complete with a final status (success or failure) recorded in Logger; no jobs hang or time out indefinitely.

## Limitations

- External web services (CIR, CTS, PubChem, IDSM, BridgeDb) are third-party and subject to downtime, rate limiting, and API changes; annotation may fail silently or incompletely if services are unavailable.
- Quality and coverage of returned metadata vary by service; some services may not recognize ambiguous or non-standardized compound names, leading to null or partial results.
- Asynchronous processing requires careful error handling to distinguish between service errors, malformed queries, and timeout events; the current implementation's resilience to these conditions is not detailed in the article.
- The annotation pipeline assumes source attributes (e.g., compound name) are present and reasonably clean; highly noisy or incomplete source data will degrade conversion success rates.

## Evidence

- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb"
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed"
- [other] Invoke the asynchronous `annotate_spectra` method with the defined jobs to dispatch metadata enrichment requests to web services.: "Invoke the asynchronous `annotate_spectra` method with the defined jobs to dispatch metadata enrichment requests to web services"
- [other] For each job, the WebConverter base class calls `query_the_service` to make HTTP requests to the target API endpoint.: "For each job, the WebConverter base class calls `query_the_service` to make HTTP requests to the target API endpoint"
- [other] Parse API responses using service-specific `parse_response` methods to extract SMILES, InChI, CAS and other metadata fields.: "Parse API responses using service-specific `parse_response` methods to extract SMILES, InChI, CAS and other metadata fields"
- [other] Parse Logger records to compute fill-rate statistics (count of non-null values per metadata attribute before and after annotation).: "Parse Logger records to compute fill-rate statistics (count of non-null values per metadata attribute before and after annotation)"
