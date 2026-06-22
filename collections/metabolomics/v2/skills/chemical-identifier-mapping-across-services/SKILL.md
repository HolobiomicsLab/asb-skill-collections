---
name: chemical-identifier-mapping-across-services
description: Use when when you have .msp files with sparse or incomplete chemical metadata (e.g., only compound names) and need to populate missing identifiers (SMILES, InChI, InChI keys, CAS numbers, IUPAC names, formulas) by querying multiple external chemical databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
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

# chemical-identifier-mapping-across-services

## Summary

Asynchronously map chemical identifiers (compound name, InChI, SMILES, CAS number) across multiple heterogeneous web services (CIR, CTS, PubChem, IDSM, BridgeDb) to enrich mass spectra .msp files with standardized metadata. This skill leverages concurrent API calls and rate-limiting to optimize retrieval speed while respecting external service constraints.

## When to use

When you have .msp files with sparse or incomplete chemical metadata (e.g., only compound names) and need to populate missing identifiers (SMILES, InChI, InChI keys, CAS numbers, IUPAC names, formulas) by querying multiple external chemical databases. Use this skill when the input spectra lack standardized chemical descriptors required for downstream spectral matching, annotation, or cross-database linking.

## When NOT to use

- Input .msp file already contains complete, validated chemical metadata from a single authoritative source (e.g., pre-curated NIST library).
- Target chemical identifiers are not available in any of the five supported external services (CIR, CTS, PubChem, IDSM, BridgeDb) — synchronous manual curation or alternative specialist databases may be necessary.
- Network connectivity is unreliable or external services are offline; asynchronous batching will not mitigate API unavailability.

## Inputs

- .msp file (mass spectra records with compound identifiers)
- Spectra or DataFrame data class instances (parsed spectrum records)
- List of converter names (e.g., ['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit'])
- List of Job tuples: (source_attribute, target_attribute, converter_name)

## Outputs

- .msp file with enriched metadata fields (SMILES, InChI, InChI keys, CAS numbers, IUPAC names, formulas)
- Spectrum records with merged response dictionaries from each converter
- Error logs documenting skipped or malformed responses

## How to apply

Load the input .msp file using MSMetaEnhancer's Spectra or DataFrame data class to extract spectrum records and identifiers. Initialize the ConverterBuilder to instantiate all available web converters (CIR, CTS, PubChem, IDSM, BridgeDb) and compute converters (RDKit) in a single aiohttp session. Construct conversion Job tuples specifying source_attribute → target_attribute → converter_name mappings (e.g., compound_name → SMILES via PubChem). Execute all jobs asynchronously using the Converter dispatcher, which dynamically invokes the matched converter's method and applies Throttler rate-limiting to respect API quotas. Parse and merge response dictionaries from each converter into the spectrum record, applying error handling to gracefully skip missing or malformed responses. Write the enriched spectra back to .msp format, preserving the original structure and adding new metadata fields.

## Related tools

- **MSMetaEnhancer** (Primary framework orchestrating asynchronous conversion jobs, managing Spectra/DataFrame loading, and coordinating converter registration and dispatch.) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Web converter for structure-based identifier conversion (e.g., InChI → SMILES).) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Web converter for chemical identifier transformations (compound name → SMILES, InChI, etc.).) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Web converter for comprehensive chemical metadata retrieval (SMILES, InChI, CAS numbers, formulas, IUPAC names).) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Web converter for InChI-based chemical transformations (InChI → formula, InChI key, IUPAC name).) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Web converter for cross-database chemical identifier mapping.) — https://bridgedb.github.io/
- **RDKit** (Compute converter for local, structure-based identifier derivations (e.g., SMILES → InChI key).)
- **pytest** (Testing framework used to validate converter integration and API response parsing.)

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

- All spectrum records in the output .msp file contain newly populated metadata fields (SMILES, InChI, CAS numbers, etc.) that were missing in the input.
- No spectrum record is lost or truncated; input and output .msp files have matching spectrum counts and original fields are preserved.
- Error handling gracefully skipped malformed or unavailable responses without crashing; error logs document which spectra/converters failed and why.
- Asynchronous execution completed faster than sequential calls would have; concurrent HTTP requests to multiple services were dispatched in parallel batches.
- Rate-limiting thresholds were respected; no HTTP 429 (Too Many Requests) errors were encountered and throttler logs show delays applied between API calls to each service.

## Limitations

- External service availability and response quality are not guaranteed; if CIR, CTS, PubChem, IDSM, or BridgeDb are offline or return empty responses, enrichment will be incomplete for those pathways.
- API rate limits vary by service and may be exceeded during large batch runs; the Throttler mitigates but does not eliminate rate-limit failures, and users must monitor retry behavior.
- Chemical identifier ambiguity: a single compound name may map to multiple distinct structures across services (e.g., isomers, salts, stereoisomers); users must curate metadata post-annotation or validate using spectral similarity.
- Asynchronous implementation adds complexity to error debugging; failures from concurrent converters are harder to isolate and reproduce than synchronous execution.
- Response parsing assumes standardized formats from each service; custom or deprecated API response schemas may cause parsing failures or silent data loss.

## Evidence

- [readme] MSMetaEnhancer uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
- [other] Initialize converters and execute jobs asynchronously with rate-limiting.: "Initialize the ConverterBuilder to instantiate all available web converters (CIR, CTS, PubChem, IDSM, BridgeDb) and compute converters (RDKit) from the registry in a single aiohttp session. Execute"
- [readme] Metadata enrichment includes SMILES, InChI, and CAS numbers from multiple external services.: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](...), [CTS](...), [PubChem](...), [IDSM](...), and [BridgeDb](...)"
- [other] Error handling for malformed responses during metadata merging.: "Parse and merge response dictionaries from each converter into the spectrum record, applying error handling to gracefully skip missing or malformed responses."
- [other] Job tuple structure specifies source, target, and converter for each transformation.: "construct conversion Job tuples (source_attribute → target_attribute → converter_name) specifying the desired metadata transformations (e.g., compound_name → SMILES via PubChem)"
