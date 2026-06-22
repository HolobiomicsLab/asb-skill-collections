---
name: converter-pipeline-integration-and-execution
description: Use when when you have a .msp mass spectra file with incomplete or missing chemical metadata fields (SMILES, InChI, CAS number, formula, InChIKey, IUPAC name) and need to populate those fields by querying multiple external chemical identifier services and local cheminformatics tools in parallel.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
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
  - ConverterBuilder
  - RDKit
  - Logger
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# converter-pipeline-integration-and-execution

## Summary

Register multiple chemical identifier conversion services (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) into an MSMetaEnhancer Application instance and execute asynchronous batch annotation jobs to enrich .msp mass spectra files with computed or fetched metadata fields (SMILES, InChI, CAS number, formula, InChIKey, IUPAC name).

## When to use

When you have a .msp mass spectra file with incomplete or missing chemical metadata fields (SMILES, InChI, CAS number, formula, InChIKey, IUPAC name) and need to populate those fields by querying multiple external chemical identifier services and local cheminformatics tools in parallel.

## When NOT to use

- Input .msp file already has complete metadata for your analysis goals—skip enrichment to avoid unnecessary API calls and latency.
- Your metadata fields do not map to the conversion jobs supported by available converters (e.g., seeking obscure proprietary chemical identifiers not in CIR, CTS, PubChem, IDSM, BridgeDb, or RDKit).
- You need real-time single-record conversion rather than batch asynchronous enrichment of entire .msp datasets.

## Inputs

- .msp file (mass spectrum metadata file with chemical records)
- list of converter service names (string labels: 'CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit')
- list of conversion job specifications (tuples: source_field, target_field, service)

## Outputs

- enriched .msp file with new metadata fields populated
- Logger records documenting per-job conversion success/failure events
- per-attribute fill-rate statistics (count of non-null values before and after annotation)

## How to apply

First, register all desired converter services (web-based: CTS, CIR, IDSM, PubChem, BridgeDb; and local: RDKit) using the ConverterBuilder.register() method. Then instantiate an Application, load your .msp file via load_data(), and curate metadata to standardize input fields (e.g., CAS numbers). Finally, define a list of conversion jobs as (source_field, target_field, service) tuples—for example, ('inchi', 'formula', 'IDSM') to derive molecular formula from InChI—and invoke asyncio.run(app.annotate_spectra(services, jobs)) to execute all jobs asynchronously, leveraging parallel network requests and local computation for optimal fetching speed. Capture the structured Logger output during execution to track per-job success/failure.

## Related tools

- **MSMetaEnhancer** (Application container that coordinates converter registration, data loading, and asynchronous annotation pipeline orchestration) — https://github.com/RECETOX/MSMetaEnhancer
- **ConverterBuilder** (Factory for registering converter service implementations (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) into the Application) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Chemical Identifier Resolver web service for SMILES, InChI, and structural identifier lookups) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Chemical Translation Service for multi-format identifier conversion) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Public chemical compound database for metadata lookup and identifier mappings) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Cheminformatics service for formula, InChIKey, and IUPAC name derivation from InChI) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Federated identifier mapping service for cross-database chemical record linkage) — https://bridgedb.github.io/
- **RDKit** (Local cheminformatics toolkit for synchronous structural property computation (SMILES, InChI, molecular descriptors))
- **Logger** (Structured logging component capturing per-attribute conversion events and fill-rate statistics) — https://github.com/RECETOX/MSMetaEnhancer

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
app.curate_metadata()
jobs = [('inchi', 'formula', 'IDSM'), ('inchi', 'inchikey', 'IDSM')]
asyncio.run(app.annotate_spectra(['IDSM'], jobs))
app.save_data('sample_out.msp', file_format='msp')
```

## Evaluation signals

- Verify that the enriched .msp file contains non-null values in previously empty metadata fields (SMILES, InChI, CAS, formula, InChIKey, IUPAC name) for a sample of records.
- Compare fill-rate statistics before and after annotation: compute the percentage of non-null records per metadata attribute and confirm absolute gain ≥ 0 for all fields.
- Confirm that Logger records document at least one successful conversion event for each registered service; inspect failure rates to identify unresponsive or mismatched service–job combinations.
- Validate that all output records retain their original spectral data (m/z, intensity pairs) and that no records were dropped during asynchronous processing.
- Spot-check converted identifiers (e.g., retrieve a known compound's SMILES from PubChem and verify it matches the enriched .msp file) to detect malformed or misattributed values.

## Limitations

- External web services (CIR, CTS, PubChem, IDSM, BridgeDb) may be unavailable, rate-limited, or return incomplete results for obscure compounds; fallback to RDKit for local computation when available.
- Asynchronous annotation speed is constrained by network latency and service response times; optimal throughput depends on configuring appropriate concurrency limits and retry policies.
- Conversion accuracy depends on the quality and completeness of input fields (e.g., canonical SMILES or valid InChI are required); garbage-in-garbage-out if source metadata is malformed or ambiguous.
- Different converter services may return conflicting identifiers for the same compound (e.g., isomeric vs. canonical SMILES); the pipeline does not automatically reconcile or rank conflicting results.
- Local RDKit computation requires valid chemical structure representation in the input file; it cannot recover missing or unparseable structures.

## Evidence

- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb"
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed"
- [readme] ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit]): "ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])"
- [readme] specify requested jobs: "jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ('inchi', 'inchikey', 'IDSM'), ('inchi', 'iupac_name', 'IDSM'), ('inchi', 'canonical_smiles', 'IDSM')]"
- [other] Execute the asynchronous annotate_spectra() method with all supported conversion jobs to enrich metadata fields (SMILES, InChI, CAS number, etc.).: "Execute the asynchronous annotate_spectra() method with all supported conversion jobs to enrich metadata fields (SMILES, InChI, CAS number, etc.)"
- [other] Capture the structured output from the Logger component during annotation, recording per-attribute conversion success/failure events.: "Capture the structured output from the Logger component during annotation, recording per-attribute conversion success/failure events"
- [other] Parse Logger records to compute fill-rate statistics (count of non-null values per metadata attribute before and after annotation).: "Parse Logger records to compute fill-rate statistics (count of non-null values per metadata attribute before and after annotation)"
