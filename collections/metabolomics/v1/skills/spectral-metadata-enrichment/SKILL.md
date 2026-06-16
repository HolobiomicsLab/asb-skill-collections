---
name: spectral-metadata-enrichment
description: Use when you have a .msp spectral library file with sparse or incomplete metadata (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
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
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
- 'fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer
schema_version: 0.2.0
---

# spectral-metadata-enrichment

## Summary

Enriches mass spectra records in .msp files by asynchronously querying external chemical databases (CIR, CTS, PubChem, IDSM, BridgeDb) to add missing metadata fields such as SMILES, InChI, CAS numbers, and chemical formulas. This skill is essential when working with incomplete spectral libraries that lack standardized chemical identifiers needed for downstream annotation and analysis.

## When to use

You have a .msp spectral library file with sparse or incomplete metadata (e.g., only compound names or InChI strings), and you need to populate missing chemical identifiers (SMILES, InChI, CAS numbers, IUPAC names, chemical formulas) by cross-referencing multiple authoritative chemical databases. Apply this skill when per-attribute fill-rate analysis shows significant gaps (e.g., <50% coverage on critical fields) that external services can cost-effectively resolve.

## When NOT to use

- Your .msp file already has >90% coverage on the target metadata fields you need—metadata enrichment will add minimal value and consume API quota.
- Your spectral library contains proprietary or confidential compound names that must not be transmitted to external web services for privacy or IP reasons.
- You require real-time or sub-second latency annotations; the asynchronous HTTP-based approach introduces network I/O and service availability dependencies that can introduce multi-second delays per spectrum.

## Inputs

- .msp spectral library file (text format with metadata key–value pairs)
- source attribute name (e.g., 'name', 'inchi')
- target metadata fields (e.g., 'smiles', 'inchikey', 'cas_number', 'formula')
- list of converter service names (subset of: CIR, CTS, PubChem, IDSM, BridgeDb, RDKit)

## Outputs

- enriched .msp file with additional metadata fields populated
- per-attribute fill-rate statistics (count of non-null values before and after annotation)
- structured Logger records tracking conversion success/failure per metadata field
- summary table with initial fill rate, final fill rate, and absolute gain per attribute

## How to apply

Load the .msp file into the MSMetaEnhancer Application class and register the desired converter services (CIR, CTS, PubChem, IDSM, BridgeDb, and optionally RDKit) via ConverterBuilder. Define conversion jobs as tuples specifying source attribute (e.g., 'name'), target attribute (e.g., 'inchi'), and service name. Invoke the asynchronous annotate_spectra() method, which dispatches HTTP requests to each service's API endpoint via the WebConverter base class query_the_service() method. Parse service-specific API responses using parse_response() to extract structured metadata. Aggregate enriched fields back into spectra records and save the annotated output to a new .msp file. Monitor fill-rate statistics via the Logger component to validate coverage gains before and after annotation.

## Related tools

- **CIR** (Web service for name-to-structure and structure-to-identifier conversion (e.g., InChI ↔ SMILES)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Chemical Translation Service for compound identifier and structure lookup) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Public chemical database queried for standardized SMILES, InChI, and CAS numbers) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Chemical structure and metadata repository for name-to-structure and formula derivation) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Cross-database identifier mapping service for chemical entities) — https://bridgedb.github.io/
- **RDKit** (Computational chemistry library for local structure-based metadata derivation (no network call))
- **MSMetaEnhancer** (Orchestration framework providing Application class, asynchronous annotation pipeline, and Logger for coverage metrics) — https://github.com/RECETOX/MSMetaEnhancer

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

- Fill-rate statistics show measurable increase in non-null counts for target metadata fields (e.g., SMILES fill rate rises from 30% to 85% post-annotation).
- Logger records confirm successful API responses and correct parse_response() extraction for queried services (zero or minimal parse errors).
- Spot-check enriched records for semantic correctness: SMILES strings are valid (parseable by RDKit), InChI strings start with 'InChI=1S/', CAS numbers match expected format (e.g., XXXXX-XX-X).
- No records are lost or duplicated during annotation; output .msp file contains same spectrum count and spectral data (m/z, intensity arrays) as input.
- Asynchronous execution completes in expected time; no timeout or service-unavailability errors exceed an acceptable threshold (e.g., <5% of jobs fail due to transient network issues).

## Limitations

- External service availability and response time variability: annotation speed and success depend on uptime and query load of CIR, CTS, PubChem, IDSM, and BridgeDb APIs, which may introduce multi-second delays or partial failures.
- Metadata accuracy is bounded by source quality: if an external service returns incorrect or outdated identifiers (e.g., wrong SMILES for a given compound name due to ambiguous nomenclature), the enriched .msp file will propagate those errors.
- Service-specific response parsing: each converter has its own parse_response() implementation, and response schema changes or undocumented variations in API outputs can break enrichment for that service.
- API rate limiting and quota exhaustion: large-scale annotation (thousands of spectra) may hit per-IP or per-key rate limits, causing job failures or requiring retry logic with exponential backoff.
- No explicit conflict resolution when multiple services return different values for the same field; the pipeline aggregates results but does not rank or vote on conflicting identifiers.

## Evidence

- [readme] MSMetaEnhancer is a tool used for `.msp` files annotation. It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb.: "MSMetaEnhancer is a tool used for `.msp` files annotation. It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb."
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
- [other] For each job, the WebConverter base class calls `query_the_service` to make HTTP requests to the target API endpoint.: "For each job, the WebConverter base class calls `query_the_service` to make HTTP requests to the target API endpoint."
- [other] Parse API responses using service-specific `parse_response` methods to extract SMILES, InChI, CAS and other metadata fields.: "Parse API responses using service-specific `parse_response` methods to extract SMILES, InChI, CAS and other metadata fields."
- [other] Parse Logger records to compute fill-rate statistics (count of non-null values per metadata attribute before and after annotation).: "Parse Logger records to compute fill-rate statistics (count of non-null values per metadata attribute before and after annotation)."
