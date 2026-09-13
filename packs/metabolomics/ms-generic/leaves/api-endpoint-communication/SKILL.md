---
name: api-endpoint-communication
description: Use when you have fingerprint or spectrum data that requires compound-class
  annotation but prefer not to run SIRIUS locally, or need to integrate predictions
  into an automated analysis pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3172
  tools:
  - CANOPUS
  - SIRIUS
  - CSI:FingerID
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# api-endpoint-communication

## Summary

Submit mass spectrometry data (fingerprints or spectra) to remote SIRIUS web service endpoints and retrieve structured compound-class predictions with confidence scores. This skill enables programmatic access to CANOPUS and related predictors without local installation.

## When to use

You have fingerprint or spectrum data that requires compound-class annotation but prefer not to run SIRIUS locally, or need to integrate predictions into an automated analysis pipeline. Use this when you have valid academic credentials and institutional email, or have obtained a commercial license.

## When NOT to use

- You are a non-academic user without a commercial license from Bright Giant GmbH — the Böcker group web services are restricted to academic research and education.
- Your input data is not in the format accepted by the SIRIUS web service endpoint (e.g., incompatible fingerprint encoding or spectrum file type).
- You require real-time processing with latency guarantees — web service calls may be subject to queue delays or rate limits.

## Inputs

- fingerprint data (format specified by SIRIUS web service)
- mass spectrum (format specified by SIRIUS web service)
- web service endpoint URL
- authentication credentials (academic institutional email or commercial license)

## Outputs

- structured JSON or tabular compound-class annotation
- predicted compound class labels
- confidence scores or probability estimates per class
- structured result object with required metadata fields

## How to apply

Prepare fingerprint or spectrum data in the format accepted by the target CANOPUS web service endpoint (consult SIRIUS documentation for format specifications). Construct an HTTP request to the appropriate SIRIUS web service API hosted by the Böcker group, authenticating with your academic account or commercial credentials. Submit the query asynchronously or synchronously depending on endpoint design. Retrieve the response, which will contain a structured JSON or tabular result with predicted compound classes, probability scores, and confidence metrics. Parse and validate the result to ensure required fields (compound class, confidence/probability) are present and confidence is above your acceptance threshold before downstream interpretation.

## Related tools

- **SIRIUS** (Framework providing CANOPUS web service endpoint and handling fingerprint/spectrum submission, result retrieval, and parsing) — https://github.com/sirius-ms/sirius
- **CANOPUS** (Remote web service component for compound-class prediction from fingerprints or spectra; returns structured annotations with confidence scores) — https://bio.informatik.uni-jena.de/software/canopus/
- **CSI:FingerID** (Complementary SIRIUS web service for structure identification; may be chained with CANOPUS for comprehensive annotation) — https://www.csi-fingerid.uni-jena.de/

## Evaluation signals

- HTTP response status is 200 (success) or other expected code; no network or authentication errors.
- Parsed result contains all required fields: compound class, probability/confidence score, and metadata.
- Confidence score is within expected numeric range (e.g., 0–1 or 0–100%) and matches the prediction quality for known standards.
- Result JSON or table structure matches the documented schema for the SIRIUS web service version used.
- Compound class labels match the ClassyFire or CANOPUS taxonomy used by the Böcker group endpoint.

## Limitations

- Web services are restricted to academic research and education use only; non-academic users must obtain a commercial license from Bright Giant GmbH.
- Network latency, service availability, and rate limits may affect throughput and suitability for real-time or high-volume pipelines.
- Prediction confidence and accuracy depend on the training data and models underlying CANOPUS; edge cases or novel structural features may receive low confidence.
- API endpoint format, authentication method, and response schema may change between SIRIUS versions; consult the documentation for the deployed version.

## Evidence

- [other] CANOPUS is offered as a web service component within the SIRIUS framework for academic research and education use, enabling remote submission of queries for compound-class annotation.: "CANOPUS is offered as a web service component within the SIRIUS framework for academic research and education use, enabling remote submission of queries for compound-class annotation."
- [other] Submit the query to the CANOPUS web service hosted by the Böcker group using the appropriate API or HTTP endpoint.: "Submit the query to the CANOPUS web service hosted by the Böcker group using the appropriate API or HTTP endpoint."
- [other] Retrieve the structured JSON or tabular response containing predicted compound classes and confidence scores.: "Retrieve the structured JSON or tabular response containing predicted compound classes and confidence scores."
- [readme] The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only.: "The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only."
- [readme] Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services. Results are retrieved from the web service and can be displayed in the SIRIUS graphical user interface.: "Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services. Results are retrieved from the web service."
