---
name: structured-logging-and-metric-extraction
description: Use when when executing a multi-converter annotation workflow on mass spectra metadata (.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0621
  tools:
  - MSMetaEnhancer
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - ConverterBuilder
  - Logger component
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

# structured-logging-and-metric-extraction

## Summary

Capture and parse structured logs from asynchronous metadata annotation pipelines to compute fill-rate statistics and coverage metrics for enriched .msp files. This skill quantifies annotation success by tracking per-attribute conversion events and computing before/after metadata completeness.

## When to use

When executing a multi-converter annotation workflow on mass spectra metadata (.msp files) and you need to measure the effectiveness of enrichment: how many records gained SMILES, InChI, or CAS number values, what the per-attribute completion rate was before and after annotation, and which converters succeeded or failed.

## When NOT to use

- Your .msp file is already fully annotated (100% fill rate on all target fields); logging will not reveal meaningful enrichment gains.
- You are only interested in raw annotation output, not comparative metrics; structured logging adds overhead without answering a fill-rate question.
- You need real-time annotation feedback rather than post-hoc analysis; Logger component captures events after asynchronous processing completes.

## Inputs

- .msp file (mass spectra metadata format)
- registered Converter objects (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit)
- conversion job specifications (tuple of source_attribute, target_attribute, service_name)

## Outputs

- structured Logger records with per-attribute conversion events
- fill-rate statistics (count of non-null values per attribute)
- summary table with initial fill rate, final fill rate, and absolute gain columns

## How to apply

Initialize all available converters (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) via ConverterBuilder and execute the asynchronous annotate_spectra() method with all supported conversion jobs. Capture structured output from the Logger component during annotation, recording per-attribute conversion success/failure events. Parse Logger records to compute fill-rate statistics by counting non-null values per metadata attribute before and after annotation. Generate a summary table with rows for each metadata field (SMILES, InChI, CAS number) and columns for initial fill rate, final fill rate, and absolute gain in enriched records to quantify the annotation pipeline's impact.

## Related tools

- **MSMetaEnhancer** (Main application framework that manages .msp file loading, converter orchestration, and asynchronous annotation pipeline execution) — https://github.com/RECETOX/MSMetaEnhancer
- **ConverterBuilder** (Registers and initializes all converter instances (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) before annotation) — https://github.com/RECETOX/MSMetaEnhancer
- **Logger component** (Captures structured per-attribute conversion success/failure events during asynchronous annotation processing) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Web service converter for metadata enrichment (InChI → SMILES conversion)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Web service converter for metadata enrichment and reference implementation) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Web service converter for metadata enrichment supporting ISOMERIC_SMILES and CANONICAL_SMILES) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Web service converter for metadata enrichment (name, formula, inchikey, iupac_name)) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Web service converter for metadata enrichment) — https://bridgedb.github.io/
- **RDKit** (Compute-based converter for local SMILES and InChI generation) — https://github.com/RECETOX/MSMetaEnhancer

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
jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'inchikey', 'IDSM')]
asyncio.run(app.annotate_spectra(services, jobs))
# Parse Logger records to compute fill-rate statistics and generate summary table
```

## Evaluation signals

- Logger records contain events for each conversion job; count of success/failure events matches number of conversion jobs attempted
- Fill-rate table shows monotonically non-decreasing final fill rate ≥ initial fill rate for each attribute (no data loss)
- Absolute gain column is non-negative for all attributes; at least one attribute shows gain > 0 for annotation to be considered effective
- Sum of gains across all attributes reflects total metadata records enriched; compare against total spectra count to estimate coverage impact
- Logger output can be parsed and aggregated without errors; structured format (JSON, CSV, or dict) is consistent with Application class expectations

## Limitations

- Logger component only records events; fill-rate gain depends on converter availability and network reliability—if a web service is unavailable, annotation jobs may fail silently or timeout, reducing observed gain.
- Asynchronous processing means timing of events is not guaranteed in strict order; concurrent requests from multiple converters may produce non-deterministic Logger records.
- Fill-rate statistics are computed post-hoc after annotation completes; intermediate or partial enrichment states are not captured.
- CAS number curation (via app.curate_metadata()) may normalize values before annotation, affecting before/after comparison; Logger records enrichment, not curation side effects.

## Evidence

- [other] research question from task_005: "What are the per-attribute fill-rate statistics and annotation coverage metrics produced by MSMetaEnhancer's Logger component when running the full annotation pipeline on a test .msp file?"
- [other] workflow step 4: capture Logger output: "Capture the structured output from the Logger component during annotation, recording per-attribute conversion success/failure events."
- [other] workflow step 5: compute fill-rate statistics: "Parse Logger records to compute fill-rate statistics (count of non-null values per metadata attribute before and after annotation)."
- [other] workflow step 6: generate summary table: "Generate a summary table with rows for each metadata field and columns for initial fill rate, final fill rate, and absolute gain in enriched records."
- [other] finding about metadata enrichment: "MSMetaEnhancer adds metadata including SMILES, InChI, and CAS number to .msp files through asynchronous annotation processing."
- [readme] README: asynchronous implementation: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
- [readme] README: services fetched: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb."
