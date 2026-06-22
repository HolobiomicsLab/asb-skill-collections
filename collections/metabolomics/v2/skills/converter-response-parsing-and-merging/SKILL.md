---
name: converter-response-parsing-and-merging
description: Use when after executing asynchronous conversion jobs across multiple external APIs during spectrum metadata enrichment, when you have received response dictionaries from one or more converters and need to integrate them into spectrum records while maintaining data integrity and handling partial or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
  - Throttler
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
---

# converter-response-parsing-and-merging

## Summary

Parse and integrate metadata responses from multiple external web services (CIR, CTS, PubChem, IDSM, BridgeDb) into mass spectrum records while handling malformed or missing data gracefully. This skill ensures that enriched .msp files preserve original structure and correctly merge new metadata fields without data loss or corruption.

## When to use

Apply this skill after executing asynchronous conversion jobs across multiple external APIs during spectrum metadata enrichment, when you have received response dictionaries from one or more converters and need to integrate them into spectrum records while maintaining data integrity and handling partial or failed API responses.

## When NOT to use

- Input spectrum records are already complete and do not require metadata enrichment from external services.
- Converter responses are guaranteed to be error-free and complete (no error handling needed — this skill's value lies in robustness during partial/failed API calls).
- The target .msp file format does not support additional metadata fields or has a rigid schema that cannot accommodate new columns.

## Inputs

- .msp file (parsed spectrum records with original metadata)
- Response dictionaries from converter jobs (one per converter per spectrum)
- Job specifications (source_attribute → target_attribute → converter_name tuples)

## Outputs

- Enriched spectrum records with merged metadata fields
- .msp file with preserved structure and new metadata columns
- Error/skip log (for missing or malformed converter responses)

## How to apply

Iterate over the response dictionaries returned by each converter in the dispatcher. For each response, validate the structure and data types of the returned metadata (e.g., SMILES string, InChI identifier, CAS number). Apply error handling to gracefully skip missing values, null responses, or malformed data that do not conform to expected formats. Merge valid key-value pairs from the response into the corresponding spectrum record, checking for conflicts with existing metadata and deciding whether to overwrite or preserve the original value. Finally, reconstruct the enriched spectrum record with both original and newly merged fields, preserving the .msp file schema (metadata keys, spectrum peak list format, etc.) before writing back to disk.

## Related tools

- **MSMetaEnhancer** (Main application orchestrating converter dispatch and spectrum annotation pipeline; provides the Spectra/DataFrame data classes to load and parse .msp files and the annotate_spectra method to execute jobs) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Web service converter for chemical structure queries (e.g., InChI → SMILES)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Web service converter for chemical identifiers (e.g., InChI → formula)) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Web service converter for compound metadata (e.g., name → SMILES, canonical_smiles, isomeric_smiles)) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Web service converter for chemical structure and name queries (e.g., name → inchi, formula, inchikey, iupac_name)) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Web service converter for database cross-references and identifier mapping) — https://bridgedb.github.io/
- **RDKit** (Compute-based converter for local cheminformatics operations (e.g., SMILES manipulation, structure validation))
- **Throttler** (Rate-limiting mechanism applied during converter execution to respect API rate limits)

## Examples

```
asyncio.run(app.annotate_spectra(services=['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit'], jobs=[('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ('inchi', 'canonical_smiles', 'IDSM')]))
```

## Evaluation signals

- All valid converter responses are successfully merged into spectrum records without loss of data; verify by checking that expected metadata fields (SMILES, InChI, CAS number, etc.) are present in output .msp file.
- Malformed or missing converter responses are gracefully skipped without raising exceptions; verify by confirming the pipeline completes successfully and error logs record skipped fields.
- Original spectrum metadata is preserved and not overwritten by converter responses (unless explicitly intended); verify by spot-checking output records and comparing original and enriched fields side-by-side.
- .msp file schema and peak list structure remain intact after merging; verify by parsing output .msp file with MSMetaEnhancer's Spectra parser and confirming no parse errors or missing peaks.
- Metadata keys in output records follow consistent naming conventions and match the job specification (source_attribute → target_attribute); verify by inspecting a sample of enriched spectra and confirming field names and values align with requested conversions.

## Limitations

- External API failures or timeouts may result in partial or empty responses; graceful error handling skips missing data but may leave spectrum records incompletely enriched.
- Response parsing must handle multiple formats and structures across different converters (CIR, CTS, PubChem, IDSM, BridgeDb each return different JSON/XML schemas); robust parsing logic is required but context-specific and may need extension for new converters.
- Conflicting or redundant metadata from multiple converters (e.g., two SMILES strings from different services) are not automatically reconciled; merging strategy must be defined a priori (e.g., first-come-first-served, merge with priority rank).
- Rate-limiting via Throttler may slow annotation if API limits are strict; trade-off between throughput and compliance with service terms of use.
- Data validation is applied during parsing and merging, but malformed or semantically invalid metadata (e.g., chemically incorrect SMILES) may not be detected and could propagate into output .msp file.

## Evidence

- [other] Parse and merge response dictionaries from each converter into the spectrum record, applying error handling to gracefully skip missing or malformed responses.: "Parse and merge response dictionaries from each converter into the spectrum record, applying error handling to gracefully skip missing or malformed responses."
- [other] Execute all jobs asynchronously using the Converter dispatcher, which dynamically invokes the matched converter's method and applies Throttler rate-limiting to respect API limits.: "Execute all jobs asynchronously using the Converter dispatcher, which dynamically invokes the matched converter's method and applies Throttler rate-limiting to respect API limits."
- [other] Write the enriched spectra back to an .msp file, preserving original structure and adding new metadata fields.: "Write the enriched spectra back to an .msp file, preserving original structure and adding new metadata fields."
- [other] Always handle API errors gracefully and return empty dictionaries when data is not available: "Always handle API errors gracefully and return empty dictionaries when data is not available"
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
