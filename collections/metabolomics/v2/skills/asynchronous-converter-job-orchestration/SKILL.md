---
name: asynchronous-converter-job-orchestration
description: Use when you have mass spectrum records in .msp format lacking computed
  chemical metadata (SMILES, InChI, CAS numbers, formulas, IUPAC names) and want to
  fetch these properties from multiple heterogeneous web services without blocking
  on individual API calls.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0630
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - MSMetaEnhancer
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - RDKit
  - Python
  - pytest
  - aiohttp
  license_tier: open
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- '**MSMetaEnhancer** is a tool used for `.msp` files annotation'
- '`MSMetaEnhancer/libs/converters/web/` named after your service'
- 'fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation)'
- __all__ = ['IDSM', 'CTS', 'CIR', 'PubChem', 'BridgeDb', 'MyService']
- '[CTS](https://cts.fiehnlab.ucdavis.edu/)'
- '[PubChem](https://pubchem.ncbi.nlm.nih.gov/)'
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

# asynchronous-converter-job-orchestration

## Summary

Orchestrate multiple asynchronous metadata conversion jobs across distributed web services to enrich mass spectra in .msp files with chemical identifiers and properties. This skill uses async/await patterns with rate-limiting and error handling to maximize throughput when calling external APIs (CIR, CTS, PubChem, IDSM, BridgeDb) in parallel.

## When to use

Use this skill when you have mass spectrum records in .msp format lacking computed chemical metadata (SMILES, InChI, CAS numbers, formulas, IUPAC names) and want to fetch these properties from multiple heterogeneous web services without blocking on individual API calls. Apply it especially when the number of spectra or diversity of conversion targets justifies the overhead of async session setup.

## When NOT to use

- Input spectra already possess complete metadata for your analysis; async orchestration adds unnecessary latency.
- You require strict deterministic ordering or sequential validation of converter outputs; async execution order is non-deterministic.
- API rate limits are extremely tight or service is flaky; concurrent requests may trigger throttling errors faster than sequential calls.

## Inputs

- .msp file (parsed into Spectra or DataFrame data class with spectrum records containing at least compound name and mass)
- list of Job tuples: (source_attribute, target_attribute, converter_name)
- list of converter names to register and use (e.g., ['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit'])

## Outputs

- .msp file with enriched metadata fields (SMILES, InChI, CAS number, formula, IUPAC name, inchikey, etc.)
- spectrum records with merged response dictionaries from each converter
- error log or gracefully-handled empty dictionaries for failed conversions

## How to apply

First, construct a list of conversion Job tuples, each specifying (source_attribute → target_attribute → converter_name), e.g. ('name', 'inchi', 'IDSM'). Register all converters (CTS, CIR, IDSM, PubChem, BridgeDb, RDKit) with the ConverterBuilder in a single aiohttp session to pool connections. Then invoke the Converter dispatcher asynchronously (via asyncio.run) to execute all jobs in parallel; the dispatcher dynamically matches each Job to the registered converter's method and applies the Throttler to enforce API rate limits. Collect response dictionaries from each converter, merge them into each spectrum record, and apply graceful error handling to skip missing or malformed responses. Finally, validate that enriched metadata fields are present and non-null before persisting the enriched spectra back to .msp format.

## Related tools

- **MSMetaEnhancer** (orchestration framework; provides Application class, Spectra/DataFrame parsers, ConverterBuilder registry, and async annotate_spectra method) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (web converter for chemical structure queries and InChI/SMILES transformations) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (web converter for chemical compound identification and metadata lookup) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (web converter for canonical/isomeric SMILES, InChI, CAS number, formula retrieval) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (web converter for InChI-based lookups: formula, InChIKey, IUPAC name, canonical SMILES) — https://idsm.elixir-czech.cz/
- **BridgeDb** (web converter for cross-database identifier mapping and metadata federation) — https://bridgedb.github.io/
- **RDKit** (compute converter for local, synchronous cheminformatics transformations (e.g., SMILES → InChI))
- **aiohttp** (async HTTP client for managing pooled connections across parallel API requests)
- **pytest** (framework for regression and unit testing of converter outputs and job dispatch logic)

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
jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ('inchi', 'canonical_smiles', 'IDSM')]
asyncio.run(app.annotate_spectra(['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit'], jobs))
app.save_data('sample_out.msp', file_format='msp')
```

## Evaluation signals

- All Job tuples completed without blocking the event loop; no synchronous or serial delays in logs.
- Response dictionaries from all queried converters are present in enriched spectrum records; check that target_attribute keys exist and contain non-null, non-empty values.
- API rate-limit errors do not occur; Throttler successfully enforced pauses between requests without triggering 429 / 503 responses.
- Error handling gracefully captured and logged malformed or unavailable conversions (e.g., empty dicts returned); no unhandled exceptions propagated to outer asyncio loop.
- .msp output file schema is preserved (original fields intact, new metadata fields appended); parsed .msp can be re-imported by MSMetaEnhancer without validation errors.

## Limitations

- Async orchestration is bottlenecked by the slowest converter; one unresponsive web service delays all parallel jobs if not isolated with individual timeouts.
- External web services (CIR, CTS, PubChem, IDSM, BridgeDb) are not guaranteed to have 100% coverage for all compound names or identifiers; missing or incorrect responses must be handled gracefully.
- Rate limiting via Throttler is reactive (applied post-hoc); if API quotas are exhausted mid-run, jobs may still fail; preemptive quota checking is not implemented.
- Asynchronous implementation adds complexity and potential for subtle concurrency bugs (e.g., shared mutable state, race conditions in response merging); requires careful testing and review.
- Each converter's response format is heterogeneous; robust response parsing logic must handle service-specific quirks (e.g., ISOMERIC_SMILES vs CANONICAL_SMILES in PubChem).

## Evidence

- [readme] MSMetaEnhancer uses asynchronous implementation of annotation process allowing for optimal fetching speed: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
- [other] Execute all jobs asynchronously using the Converter dispatcher with Throttler rate-limiting: "Execute all jobs asynchronously using the Converter dispatcher, which dynamically invokes the matched converter's method and applies Throttler rate-limiting to respect API limits."
- [other] Initialize ConverterBuilder to instantiate all available web converters in a single aiohttp session: "Initialize the ConverterBuilder to instantiate all available web converters (CIR, CTS, PubChem, IDSM, BridgeDb) and compute converters (RDKit) from the registry in a single aiohttp session."
- [other] Construct conversion Job tuples specifying source to target attribute mappings via converter: "For each spectrum, construct conversion Job tuples (source_attribute → target_attribute → converter_name) specifying the desired metadata transformations (e.g., compound_name → SMILES via PubChem)."
- [other] Parse and merge response dictionaries with error handling to gracefully skip malformed responses: "Parse and merge response dictionaries from each converter into the spectrum record, applying error handling to gracefully skip missing or malformed responses."
- [readme] Metadata includes SMILES, InChI, and CAS number fetched from multiple services: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](...), [CTS](...), [PubChem](...), [IDSM](...), and [BridgeDb](...)."
- [readme] Python usage pattern for invoking async annotation with asyncio.run: "asyncio.run(app.annotate_spectra(services, jobs))"
