---
name: chemical-identifier-mapping
description: Use when you have .msp spectral library files with compound names but lack standardized chemical identifiers (SMILES, InChI, InChI Key, CAS number, IUPAC names, or molecular formulas).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0219
  - http://edamontology.org/topic_3697
  tools:
  - MSMetaEnhancer
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - RDKit
  - pytest
  - openNAU
  - HMDB
  - MassBank
  - METLIN
  - patRoon
  - screenSuspects
  - BioTransformer
  - PubChemLite
  - MetFrag
  - R
  - Docker
  - tima
  - LOTUS
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
- doi: 10.21147/j.issn.1000-9604.2023.05.11
  title: ''
- doi: 10.1186/s13321-020-00477-w
  title: ''
- doi: 10.3389/fpls.2019.01329
  title: ''
evidence_spans:
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
- 'fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb'
- An open-source analysis software for untargeted metabolism data (openNAU) was constructed
- The `generateTPs` function is used to obtain TPs for a particular set of parents.
- componTP <- generateComponents(algorithm = "tp",
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  - build: coll_opennau_cq
    doi: 10.21147/j.issn.1000-9604.2023.05.11
    title: OpenNAU
  - build: coll_patroon_cq
    doi: 10.1186/s13321-020-00477-w
    title: patRoon
  - build: coll_tima_cq
    doi: 10.3389/fpls.2019.01329
    title: tima
  dedup_kept_from: coll_msmetaenhancer
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.04494
  all_source_dois:
  - 10.21105/joss.04494
  - 10.21147/j.issn.1000-9604.2023.05.11
  - 10.1186/s13321-020-00477-w
  - 10.3389/fpls.2019.01329
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-identifier-mapping

## Summary

Enriches mass spectra records (.msp files) by querying external chemical databases to retrieve standardized molecular identifiers (SMILES, InChI, CAS numbers) for compound names. This skill automates metadata annotation across heterogeneous web services using asynchronous dispatch, reducing manual curation effort.

## When to use

Apply this skill when you have .msp spectral library files with compound names but lack standardized chemical identifiers (SMILES, InChI, InChI Key, CAS number, IUPAC names, or molecular formulas). Use it before downstream cheminformatics workflows that require canonical molecular representations or when integrating spectra across databases with inconsistent metadata.

## When NOT to use

- Input spectra already contain complete canonical identifiers (SMILES, InChI, InChI Key) from a trusted source—re-annotation adds no new information.
- Compound names are ambiguous, proprietary, or highly specialized (e.g., complex natural product mixtures); external services cannot reliably resolve them.
- Network access to external services is unavailable or rate-limited; asynchronous dispatch will timeout or fail.

## Inputs

- .msp spectral library file (with at minimum compound names or InChI strings)
- list of (source_attribute, target_attribute, service) job tuples specifying desired conversions

## Outputs

- annotated .msp file with enriched metadata fields (SMILES, InChI, InChI Key, CAS number, IUPAC name, molecular formula)
- structured metadata dictionary attached to each spectra record

## How to apply

Load the .msp file into MSMetaEnhancer's Application class and register converter services (CIR, CTS, PubChem, IDSM, BridgeDb, or RDKit). Define conversion jobs as (source_attribute, target_attribute, service) tuples—e.g., ('name', 'inchi', 'IDSM') maps compound names to InChI strings. Invoke the asynchronous `annotate_spectra()` method, which dispatches HTTP requests to each service's API endpoint. For each response, service-specific `parse_response()` methods extract the requested metadata fields. Aggregate enriched metadata back into spectra records and save to an output .msp file. Choose services based on metadata availability: IDSM and CTS excel at InChI/formula derivation; PubChem and CIR handle SMILES and CAS lookups; BridgeDb supports cross-database identifier mapping.

## Related tools

- **MSMetaEnhancer** (Core orchestrator: loads .msp files, registers converter services, dispatches asynchronous annotation jobs, aggregates results, and exports annotated spectra) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Web service for InChI ↔ SMILES conversion and CAS number lookup) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Web service for compound name → InChI, formula, InChI Key, and IUPAC name conversion) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Web service for name → SMILES, InChI, InChI Key, CAS number, and formula lookup; supports isomeric and canonical SMILES) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Web service for InChI → formula, InChI Key, IUPAC name, and canonical SMILES conversion) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Web service for cross-database chemical identifier mapping and normalization) — https://bridgedb.github.io/
- **RDKit** (Local compute converter for SMILES validation, InChI generation, and descriptor calculation without network calls)
- **pytest** (Test framework for validating converter implementations and ensuring backward compatibility)

## Examples

```
import asyncio; from MSMetaEnhancer import Application; from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb; from MSMetaEnhancer.libs.converters.compute import RDKit; from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder; ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit]); app = Application(); app.load_data('sample.msp', file_format='msp'); app.curate_metadata(); jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ('inchi', 'inchikey', 'IDSM')]; asyncio.run(app.annotate_spectra(['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit'], jobs)); app.save_data('sample_out.msp', file_format='msp')
```

## Evaluation signals

- All spectra records in output .msp contain the requested metadata fields (SMILES, InChI, etc.); no records have null or empty values for successfully queried attributes.
- Metadata consistency check: SMILES and InChI strings for the same compound are chemically equivalent (e.g., via RDKit canonicalization).
- Service coverage: verify that each job successfully queried the specified service by checking HTTP response codes and log entries; failed queries are logged and documented.
- No data loss: output .msp file contains all original spectra and metadata; new fields are additive (no overwrites of existing values unless explicitly configured).
- Asynchronous correctness: verify that concurrent requests to multiple services complete without race conditions or duplicated records (via pytest test suite).

## Limitations

- External service availability: annotation depends on uptime and responsiveness of CIR, CTS, PubChem, IDSM, and BridgeDb; network latency or rate-limiting can slow or block enrichment.
- Name ambiguity and resolution: compound names may map to multiple structures across services; conflicts are not automatically resolved; manual curation may be required for disambiguation.
- Incomplete coverage: not all services provide all metadata types (e.g., CAS numbers are sparse in PubChem); job design must account for service-specific capabilities.
- No validation of chemical correctness: tool returns whatever the external service provides; incorrect or outdated records in source databases are propagated without warning.
- Metadata curation prerequisite: the `curate_metadata()` step (e.g., fixing malformed CAS numbers) is recommended but optional; poor input quality degrades matching success.

## Evidence

- [intro] MSMetaEnhancer enriches .msp files by adding SMILES, InChI, and CAS number metadata retrieved from five external services: "MSMetaEnhancer enriches .msp files by adding SMILES, InChI, and CAS number metadata retrieved from five external services: CIR, CTS, PubChem, IDSM, and BridgeDb."
- [readme] Asynchronous implementation allows optimal fetching speed: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
- [intro] Workflow involves specifying conversion jobs and invoking annotate_spectra method: "Configure conversion jobs specifying source attributes (e.g., compound name), target attributes (e.g., SMILES, InChI, CAS), and converter services (CIR, CTS, PubChem, IDSM, BridgeDb). 3. Invoke the"
- [intro] Service-specific response parsing extracts metadata: "Parse API responses using service-specific `parse_response` methods to extract SMILES, InChI, CAS and other metadata fields."
- [readme] Example Python usage defining jobs as tuples: "jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ('inchi', 'inchikey', 'IDSM'), ('inchi', 'iupac_name', 'IDSM'), ('inchi', 'canonical_smiles', 'IDSM')]"
- [intro] Metadata aggregation and output generation: "Aggregate enriched metadata back into the spectra records. 7. Save the annotated spectra to an output .msp file."
