---
name: spectral-fingerprint-web-service-query
description: Use when you have a high-resolution LC-MS/MS spectrum or pre-computed molecular fingerprint from a small-molecule sample and need to retrieve a systematic structural classification (compound class and subclass) with confidence estimates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0593
  tools:
  - CANOPUS
  - SIRIUS
  - CSI:FingerID
  - ClassyFire
derived_from:
- doi: 10.1038/s41587-021-01045-9
  title: cosmic
evidence_spans:
- The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  dedup_kept_from: coll_cosmic
schema_version: 0.2.0
---

# spectral-fingerprint-web-service-query

## Summary

Query the CANOPUS web service with a prepared fingerprint or mass spectrum to retrieve structured compound-class predictions with confidence scores. This skill enables remote submission of LC-MS/MS fragmentation data or pre-computed fingerprints to the Böcker group's hosted SIRIUS infrastructure for systematic metabolite classification.

## When to use

You have a high-resolution LC-MS/MS spectrum or pre-computed molecular fingerprint from a small-molecule sample and need to retrieve a systematic structural classification (compound class and subclass) with confidence estimates. Use this skill when your goal is to assign the unknown compound to a taxonomic class rather than identify a specific structure or retrieve candidate molecules from a database.

## When NOT to use

- Your input is a low-resolution or singly-charged MS spectrum without isotope-pattern information; CANOPUS relies on high-resolution fragmentation data or validated fingerprints for accurate class prediction.
- You require a specific chemical name, InChI, or SMILES for the compound; CANOPUS returns taxonomic classes, not individual structure identities — use CSI:FingerID web service instead for structure-database matching.
- Your samples are for commercial or non-academic use without a license from Bright Giant GmbH; SIRIUS web services are restricted to academic research and education only.

## Inputs

- High-resolution LC-MS/MS spectrum with fragment masses and intensities
- Molecular formula annotation (for MS/MS data)
- Pre-computed molecular fingerprint (CSI:FingerID or ECFP-like format)
- Authenticated SIRIUS web service user account

## Outputs

- Structured compound-class annotation (JSON or tabular)
- ClassyFire taxonomy hierarchy (class, subclass, direct parent, etc.)
- Confidence scores / probability estimates for each predicted class

## How to apply

Prepare your fingerprint or spectrum data in the format accepted by the CANOPUS web service endpoint (typically JSON with fragment ions, intensities, and molecular formula for MS/MS data, or a pre-computed fingerprint vector). Submit the query to the CANOPUS web service hosted by the Böcker group using the appropriate HTTP API endpoint with your authenticated user credentials (institutional email for academic access). Retrieve and parse the structured JSON response containing predicted compound classes (e.g., ClassyFire taxonomy), subclasses, and confidence scores (probabilities). Validate the response by checking that required fields (compound class, confidence/probability scores) are present and non-null; discard predictions with confidence below your domain-specific threshold (no universal threshold is stated; domain knowledge or prior benchmarking on similar samples should guide cutoff selection). Store the result alongside your original spectrum/fingerprint record for downstream use (structure database queries, biological interpretation, or comparative analysis).

## Related tools

- **SIRIUS** (Java framework that integrates CANOPUS and other web services; provides GUI and CLI for submitting queries and retrieving results) — https://github.com/sirius-ms/sirius
- **CSI:FingerID** (Complementary web service within SIRIUS ecosystem; generates molecular fingerprints that can be used as input to CANOPUS, or retrieves candidate structures from metabolite databases) — https://github.com/sirius-ms/sirius
- **ClassyFire** (Provides the compound taxonomy and classification scheme used by CANOPUS for annotating predicted classes)

## Evaluation signals

- HTTP response status is 200 OK and response body is valid JSON with non-null 'class' and 'confidence' (or 'probability') fields.
- Predicted compound classes match the expected taxonomic hierarchy (e.g., compound class → direct parent → subclass) with no missing levels.
- Confidence scores are numeric values in the range [0, 1] or [0, 100] and are consistent with known or negative-control samples (e.g., known standards score > 0.7; blanks or out-of-scope compounds score < 0.3).
- Response retrieval time is < 30 seconds for typical 10–100 fragment-ion spectra (confirms web service availability and network connectivity).
- Parsed annotation result can be serialized back to JSON/CSV without loss of information, and linked to the original spectrum via unique identifier (confirming data integrity and traceability).

## Limitations

- CANOPUS web services are restricted to academic research and education use only; non-academic users require a commercial license from Bright Giant GmbH.
- Classification accuracy depends on the quality of the input spectrum or fingerprint; low-resolution data, heavy background noise, or spectra from atypical ionization modes may yield low-confidence predictions.
- CANOPUS returns compound classes, not individual chemical structures; for unknown compounds not represented in training databases, class predictions may be coarse or uninformative.
- No publicly available changelog was found for CANOPUS version updates, making it difficult to track changes in model accuracy, supported classes, or API breaking changes between releases.

## Evidence

- [other] CANOPUS is offered as a web service component within the SIRIUS framework for academic research and education use, enabling remote submission of queries for compound-class annotation.: "CANOPUS is offered as a web service component within the SIRIUS framework for academic research and education use, enabling remote submission of queries for compound-class annotation."
- [other] Prepare fingerprint or spectrum data in the format accepted by the CANOPUS web service endpoint. Submit the query to the CANOPUS web service hosted by the Böcker group using the appropriate API or HTTP endpoint. Retrieve the structured JSON or tabular response containing predicted compound classes and confidence scores.: "Prepare fingerprint or spectrum data in the format accepted by the CANOPUS web service endpoint. Submit the query to the CANOPUS web service hosted by the Böcker group using the appropriate API or"
- [readme] The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only: "The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only"
- [readme] Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services. Results are retrieved from the web service and can be displayed in the SIRIUS graphical user interface.: "Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services. Results are retrieved from the web service and can be displayed in the"
- [readme] For non-academic users, the Bright Giant GmbH provides licenses and all related services: "For non-academic users, the Bright Giant GmbH provides licenses and all related services"
