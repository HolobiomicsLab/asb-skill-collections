---
name: web-service-api-integration
description: Use when when you have a parsed mass spectrum (precursor m/z, ionization mode, collision energy, and fragment peak list as m/z–intensity pairs) and need to obtain molecular fingerprint predictions, de-novo candidate structures, or chemical class annotations without maintaining local neural network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2258
  tools:
  - CSI:FingerID
  - MSNovelist
  - SIRIUS
  - CANOPUS
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s41587-021-01045-9
  title: cosmic
evidence_spans:
- The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  dedup_kept_from: coll_cosmic
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-021-01045-9
  all_source_dois:
  - 10.1038/s41587-021-01045-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# web-service-api-integration

## Summary

Construct and submit HTTP POST requests to SIRIUS web service endpoints (CSI:FingerID, MSNovelist, CANOPUS) to dispatch mass spectrometry queries and parse JSON responses into structured molecular predictions. This skill bridges local LC-MS/MS analysis with remote machine-learning-based molecular fingerprint, structure generation, and chemical classification services.

## When to use

When you have a parsed mass spectrum (precursor m/z, ionization mode, collision energy, and fragment peak list as m/z–intensity pairs) and need to obtain molecular fingerprint predictions, de-novo candidate structures, or chemical class annotations without maintaining local neural network models. Use this skill when the SIRIUS graphical or command-line interface is insufficient and you need programmatic control over request payload construction, authentication, and response parsing.

## When NOT to use

- Your institution lacks academic email domain recognition or you cannot obtain a free SIRIUS web service account—commercial users must contact Bright Giant GmbH for licensing.
- You require offline/local inference without network access; use local fingerprint models or structure generators instead.
- Your input spectrum has insufficient fragment ions or very low m/z precursor mass where fingerprint predictors lack training data coverage.

## Inputs

- mass spectrum object with precursor m/z and ionization mode
- fragment peak list (m/z and intensity pairs)
- collision energy (optional but recommended)
- SIRIUS web service API endpoint URL
- user authentication credentials (institutional email for academic access)

## Outputs

- molecular fingerprint prediction (as vector or binary representation with confidence scores)
- de-novo candidate structures (SMILES format with rank and score)
- structured output file (JSON or CSV) with predictions and metadata

## How to apply

First, prepare the spectrum metadata (precursor m/z, ionization mode, collision energy if available) and fragment peak list in the format required by the target SIRIUS web service API specification (REST endpoint accepting JSON). Construct a valid HTTP POST request payload conforming to the service's schema—for CSI:FingerID, include spectrum and metadata; for MSNovelist, include molecular ion mass and optional fragmentation data. Submit the POST request to the appropriate SIRIUS web service gateway endpoint (e.g., CSI:FingerID for fingerprint prediction or MSNovelist for structure generation). Parse the returned JSON response to extract predictions: for CSI:FingerID extract the molecular fingerprint representation and confidence/scoring metrics; for MSNovelist extract ranked candidate structures with SMILES, rank, and score. Serialize the parsed output into a structured format (JSON or CSV) with all relevant fields for downstream analysis or database integration.

## Related tools

- **SIRIUS** (Java-based framework integrating CSI:FingerID, CANOPUS, MSNovelist web services; provides both GUI and CLI for LC-MS/MS analysis and web service dispatch) — https://github.com/sirius-ms/sirius
- **CSI:FingerID** (Web service component for predicting molecular fingerprints from mass spectra using machine learning; integrated into SIRIUS) — https://bio.informatik.uni-jena.de/software/sirius/
- **MSNovelist** (Web service component for de-novo structure generation from mass spectra; accepts molecular ion mass and fragmentation data) — https://bio.informatik.uni-jena.de/software/sirius/
- **CANOPUS** (Web service component for systematic chemical classification using high-resolution fragmentation mass spectra; integrated into SIRIUS) — https://bio.informatik.uni-jena.de/software/sirius/

## Evaluation signals

- HTTP response status code is 200 (OK) and response body is valid JSON conforming to the documented service schema
- Parsed fingerprint prediction contains expected fields (e.g., fingerprint vector, confidence scores) and numeric scores fall within documented range (e.g., 0–1 probability or calibrated uncertainty)
- For MSNovelist: returned structures are valid SMILES strings, rank is an integer ≥ 1, and scores are sorted in descending order
- Output file validates against schema (all required columns present, data types match specification, no missing critical fields)
- Round-trip verification: re-submit the same spectrum payload and confirm identical or near-identical predictions (allowing for minor network/backend variance)

## Limitations

- SIRIUS web services are restricted to academic research and education use only; commercial redistribution is prohibited unless licensed through Bright Giant GmbH.
- Fingerprint and structure prediction quality depend on training data coverage; spectra from rare compound classes or atypical ionization modes may yield lower-confidence predictions.
- Network latency and service availability affect integration time; no guaranteed SLA is documented for the Böcker group's hosted academic services.
- Authentication requires institutional email domain recognition; some organizations may require additional manual validation of academic status.
- The web service payload format and response schema are defined by the SIRIUS API specification and may change between major versions; always validate against current API documentation.

## Evidence

- [other] CSI:FingerID web-service dispatch for molecular fingerprint prediction: "Reconstruct the CSI:FingerID web-service dispatch for molecular fingerprint prediction"
- [other] workflow for CSI:FingerID integration: "1. Prepare spectrum metadata (precursor m/z, ionization mode, collision energy if available) and fragment peak list (m/z and intensity pairs). 2. Construct a valid CSI:FingerID web service request"
- [other] MSNovelist web-service dispatch workflow: "1. Prepare query payload containing molecular ion mass and optional fragmentation spectrum data in the format accepted by the MSNovelist REST API endpoint. 2. Submit HTTP POST request to the"
- [readme] SIRIUS web service access restrictions: "The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only."
- [readme] SIRIUS integration of web services: "Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services. Results are retrieved from the web service and can be displayed in the"
- [readme] commercial licensing for non-academic users: "For non-academic users, the Bright Giant GmbH provides licenses and all related services."
