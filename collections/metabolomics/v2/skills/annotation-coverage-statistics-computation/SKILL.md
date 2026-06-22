---
name: annotation-coverage-statistics-computation
description: Use when you have run MSMetaEnhancer's annotate_spectra() method on a .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3500
  edam_topics:
  - http://edamontology.org/topic_0769
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

# annotation-coverage-statistics-computation

## Summary

Compute per-attribute fill-rate statistics and annotation coverage metrics from MSMetaEnhancer's Logger component output, quantifying the enrichment of metadata fields (SMILES, InChI, CAS number) in .msp mass spectrometry files before and after multi-service annotation.

## When to use

You have run MSMetaEnhancer's annotate_spectra() method on a .msp file using multiple converters (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) and need to measure the effectiveness of the annotation pipeline by tracking which metadata attributes were successfully enriched, how many records gained new values, and what proportion of the dataset now has complete metadata coverage.

## When NOT to use

- The .msp file has not yet been processed by annotate_spectra(); you need to run the annotation pipeline first before computing coverage statistics.
- You are interested only in the enriched .msp output file itself, not in quantitative evaluation of annotation effectiveness or metadata completeness.
- The Logger component was not enabled or Logger records were not captured during the annotation run, making fill-rate computation impossible.

## Inputs

- .msp file loaded into Application class
- Logger records from annotate_spectra() execution with all converter services active
- Metadata attribute names (SMILES, InChI, CAS number, formula, InChI key, IUPAC name, canonical_smiles)
- Conversion job specifications (source_field, target_field, service_name tuples)

## Outputs

- Summary table with per-attribute fill-rate statistics (rows=metadata fields, columns=initial fill rate, final fill rate, absolute gain)
- Per-attribute conversion success/failure event counts
- Structured annotation coverage metrics (count of enriched records per metadata field)
- Data frame or CSV with field-wise coverage analysis

## How to apply

After executing the asynchronous annotate_spectra() method with all supported conversion jobs, capture the structured output and failure events from the Logger component for each metadata attribute (SMILES, InChI, CAS number, formula, InChI key, IUPAC name, etc.). Parse Logger records to identify conversion successes and failures, then compute fill-rate statistics: count non-null values per attribute in the original dataset, count non-null values after annotation, and calculate absolute gain (records converted from null to non-null). Generate a summary table with rows for each metadata field and columns for initial fill rate, final fill rate, and absolute gain. This tabular output quantifies the benefit of each converter service and reveals which metadata fields remain sparse despite annotation attempts.

## Related tools

- **MSMetaEnhancer** (Primary tool that executes asynchronous annotation and logs per-attribute conversion events; Logger component produces the structured records parsed to compute coverage statistics) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Chemical converter service that fetches metadata and contributes to per-service fill-rate statistics)
- **CTS** (Chemical converter service that fetches metadata and contributes to per-service fill-rate statistics)
- **PubChem** (Chemical converter service that fetches metadata and contributes to per-service fill-rate statistics)
- **IDSM** (Chemical converter service that fetches metadata and contributes to per-service fill-rate statistics)
- **BridgeDb** (Chemical converter service that fetches metadata and contributes to per-service fill-rate statistics)
- **RDKit** (Local computational converter that derives chemical properties (e.g., SMILES from InChI) and contributes to per-service fill-rate statistics)
- **Python** (Language in which MSMetaEnhancer is implemented and in which Logger record parsing and fill-rate calculations are performed)

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
services = ['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit']
jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM')]
asyncio.run(app.annotate_spectra(services, jobs))
# Parse Logger records to compute fill-rate statistics for each metadata attribute
```

## Evaluation signals

- Initial fill rates for each metadata attribute sum to ≤100% (no record can have >1 value per attribute before annotation)
- Final fill rates for each metadata attribute are ≥ initial fill rates (annotation only adds values, never removes them)
- Absolute gain (final count − initial count) is non-negative for all attributes
- Sum of absolute gains across all attributes equals total number of conversion successes logged by the Logger component
- At least one metadata attribute shows final fill rate >initial fill rate, demonstrating that annotation had a measurable effect

## Limitations

- Fill-rate statistics depend on Logger component being enabled and fully capturing conversion events; if logging is incomplete or disabled, coverage statistics will be underestimated.
- Some converter services (CIR, CTS, PubChem, IDSM, BridgeDb) are web services subject to network failures, rate limiting, or service unavailability, which may cause conversion attempts to fail silently or partially; coverage metrics reflect actual execution, not theoretical optimal coverage.
- Metadata attributes with null or missing input values (e.g., compounds without InChI keys in the original .msp) cannot be converted by downstream services; initial sparsity limits the theoretical maximum achievable fill rate for dependent fields.
- The skill measures only quantitative coverage (fill rates), not quality or correctness of enriched metadata; high fill rates do not guarantee that the fetched SMILES, InChI, or CAS numbers are accurate or match the parent compound.

## Evidence

- [other] MSMetaEnhancer adds metadata including SMILES, InChI, and CAS number to .msp files through asynchronous annotation processing.: "MSMetaEnhancer adds metadata including SMILES, InChI, and CAS number to .msp files through asynchronous annotation processing."
- [other] Capture the structured output from the Logger component during annotation, recording per-attribute conversion success/failure events.: "Capture the structured output from the Logger component during annotation, recording per-attribute conversion success/failure events."
- [other] Parse Logger records to compute fill-rate statistics (count of non-null values per metadata attribute before and after annotation).: "Parse Logger records to compute fill-rate statistics (count of non-null values per metadata attribute before and after annotation)."
- [other] Generate a summary table with rows for each metadata field and columns for initial fill rate, final fill rate, and absolute gain in enriched records.: "Generate a summary table with rows for each metadata field and columns for initial fill rate, final fill rate, and absolute gain in enriched records."
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb"
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
