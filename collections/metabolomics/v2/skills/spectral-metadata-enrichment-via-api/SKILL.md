---
name: spectral-metadata-enrichment-via-api
description: Use when you have .msp spectrum files with minimal metadata (e.g., only compound name and mass) and need to augment them with chemical structure descriptors, identifiers, and properties from external databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3696
  edam_topics:
  - http://edamontology.org/topic_0218
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-metadata-enrichment-via-api

## Summary

Enrich mass spectra in .msp files with computed and fetched metadata (SMILES, InChI, CAS number, formula, IUPAC name) by dispatching asynchronous conversion jobs across multiple external web services and local chemical informatics libraries. This skill is essential when raw spectral records lack structural and chemical annotations needed for compound identification and comparative analysis.

## When to use

Apply this skill when you have .msp spectrum files with minimal metadata (e.g., only compound name and mass) and need to augment them with chemical structure descriptors, identifiers, and properties from external databases. Use it specifically when spectrum records require transformations like name→SMILES, InChI→formula, or inchi→inchikey to enable downstream spectral matching, library curation, or chemical mining.

## When NOT to use

- Spectra are already fully annotated with target metadata (SMILES, InChI, CAS); re-enrichment will redundantly query external APIs and consume rate limits.
- Input is not .msp format or does not contain parseable compound identifiers (name, mass, precursor m/z); converter jobs cannot be constructed.
- Network connectivity or external service availability is severely degraded; asynchronous job batching will timeout or accumulate errors without meaningful enrichment.
- Spectra are proprietary or confidentiality-sensitive and cannot be transmitted to third-party web services (CIR, CTS, PubChem, IDSM, BridgeDb) for conversion.

## Inputs

- .msp file with spectrum records and minimal metadata (compound name, mass, precursor m/z)
- list of source attributes (e.g., 'name', 'inchi', 'cas_number')
- list of target attributes to compute (e.g., 'smiles', 'formula', 'inchikey')
- list of converter service names ('CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit')

## Outputs

- enriched .msp file with added metadata columns (SMILES, InChI, InChIKey, CAS number, formula, IUPAC name, canonical_smiles, isomeric_smiles)
- annotation report (implicit) listing successful and failed job conversions per spectrum

## How to apply

Load the .msp file using MSMetaEnhancer's Spectra or DataFrame data class to parse spectrum records and extract identifiers (compound name, mass). Register all desired converters (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) with ConverterBuilder in a single aiohttp session to initialize web and compute backends. Construct conversion Job tuples specifying source_attribute→target_attribute→converter_name transformations (e.g., 'name'→'inchi'→'IDSM'). Execute all jobs asynchronously via the Converter dispatcher, which dynamically invokes the matched converter's method and applies Throttler rate-limiting to respect API request limits. Parse and merge response dictionaries into each spectrum record, applying error handling to gracefully skip missing or malformed responses. Finally, write enriched spectra back to .msp format, preserving original structure and adding new metadata fields.

## Related tools

- **MSMetaEnhancer** (orchestrates asynchronous annotation pipeline, provides Spectra/DataFrame parsers, Converter dispatcher, and .msp I/O) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (web converter for chemical structure lookups and transformations (InChI↔SMILES)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (web converter for chemical translation and conversion (name→structure identifiers)) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (web converter for compound lookups, structure queries, and metadata retrieval (SMILES, InChI, CAS, formula)) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (web converter for chemical structure translation (name→InChI, InChI→formula, InChI→inchikey, InChI→IUPAC name)) — https://idsm.elixir-czech.cz/
- **BridgeDb** (web converter for cross-database identifier mapping) — https://bridgedb.github.io/
- **RDKit** (compute converter for local chemical informatics (SMILES→InChI, structure validation, descriptor generation))

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
jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ('inchi', 'inchikey', 'IDSM')]
asyncio.run(app.annotate_spectra(['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit'], jobs))
app.save_data('sample_out.msp', file_format='msp')
```

## Evaluation signals

- Output .msp file contains all requested target metadata fields (SMILES, InChI, formula, etc.) populated for ≥95% of input spectra (tolerance for unresoluble compounds).
- Verify asynchronous execution via logs: all conversion jobs complete without hanging; Throttler honors API rate limits (no HTTP 429 errors observed).
- Spot-check 5–10 enriched spectrum records: values are chemically consistent (e.g., InChI and SMILES represent the same structure; formula matches InChI composition).
- Error handling: malformed or missing responses from external services are skipped gracefully without halting the pipeline; failed jobs are logged and downstream spectra continue enrichment.
- Original spectrum fields (precursor m/z, MS/MS peaks, retention time) are preserved unchanged in output .msp; only new metadata columns are appended.

## Limitations

- Conversion success depends on external service availability and query timeouts; if services are unavailable or slow, enrichment jobs fail silently for those spectra.
- API rate limits imposed by external web services (CIR, CTS, PubChem, IDSM, BridgeDb) may cause throttling; large-scale enrichment (>10k spectra) may require staggered batch processing.
- Compound name ambiguity: identical compound names can resolve to different structures across services or may not resolve at all if the name is non-standard or proprietary.
- RDKit local converter requires exact SMILES or InChI input; if upstream web converters produce invalid structures, RDKit-dependent downstream jobs fail.
- Spectra with incomplete or incorrect precursor mass or compound name cannot be reliably enriched; garbage input yields garbage or missing output.

## Evidence

- [other] Load the input .msp file using MSMetaEnhancer's Spectra or DataFrame data class to parse spectrum records and extract identifiers (compound name, mass).: "Load the input .msp file using MSMetaEnhancer's Spectra or DataFrame data class to parse spectrum records and extract identifiers (compound name, mass)."
- [other] Initialize the ConverterBuilder to instantiate all available web converters (CIR, CTS, PubChem, IDSM, BridgeDb) and compute converters (RDKit) from the registry in a single aiohttp session.: "Initialize the ConverterBuilder to instantiate all available web converters (CIR, CTS, PubChem, IDSM, BridgeDb) and compute converters (RDKit) from the registry in a single aiohttp session."
- [other] Execute all jobs asynchronously using the Converter dispatcher, which dynamically invokes the matched converter's method and applies Throttler rate-limiting to respect API limits.: "Execute all jobs asynchronously using the Converter dispatcher, which dynamically invokes the matched converter's method and applies Throttler rate-limiting to respect API limits."
- [other] Parse and merge response dictionaries from each converter into the spectrum record, applying error handling to gracefully skip missing or malformed responses.: "Parse and merge response dictionaries from each converter into the spectrum record, applying error handling to gracefully skip missing or malformed responses."
- [intro] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](...), [CTS](...), [PubChem](...), [IDSM](...), and [BridgeDb](...).: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services"
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
