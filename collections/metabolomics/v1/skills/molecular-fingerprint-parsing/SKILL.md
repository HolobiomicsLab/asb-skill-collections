---
name: molecular-fingerprint-parsing
description: Use when you have received a JSON response from the CSI:FingerID web service endpoint after submitting a fragmentation tree or tandem mass spectrum query, and you need to extract the predicted molecular fingerprint representation and associated scoring metrics for compound identification or CANOPUS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3806
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - CSI:FingerID
  - SIRIUS
  - CANOPUS
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

# molecular-fingerprint-parsing

## Summary

Parse molecular fingerprint predictions returned from the CSI:FingerID web service, extracting predicted fingerprint representations and confidence metrics for downstream structural and chemical classification analysis. This skill bridges the gap between spectrum query submission and fingerprint-based structure annotation.

## When to use

You have received a JSON response from the CSI:FingerID web service endpoint after submitting a fragmentation tree or tandem mass spectrum query, and you need to extract the predicted molecular fingerprint representation and associated scoring metrics for compound identification or CANOPUS chemical classification.

## When NOT to use

- The input is already a pre-computed fingerprint stored in a local database or structure library—use direct lookup instead.
- You are performing de novo structure generation without known fragmentation patterns—use MSNovelist instead.
- The mass spectrum has not yet been processed into a fragmentation tree or does not contain sufficient fragment information to warrant web service submission.

## Inputs

- HTTP JSON response from CSI:FingerID web service
- Spectrum metadata (precursor m/z, ionization mode, collision energy)
- Fragment peak list (m/z and intensity pairs)

## Outputs

- Extracted molecular fingerprint representation (binary or continuous vector)
- Fingerprint confidence or scoring metrics
- Structured fingerprint output (JSON or CSV format)
- Indexed mapping of spectra to fingerprint predictions

## How to apply

Submit a prepared spectrum query (with precursor m/z, ionization mode, collision energy if available, and fragment peak list as m/z–intensity pairs) to the CSI:FingerID web service via the SIRIUS API gateway. Upon receiving the HTTP response payload, parse the JSON structure to locate the fingerprint prediction field and extract both the binary or continuous fingerprint vector and any reported confidence scores or quality metrics. Validate that the fingerprint representation conforms to the expected format (e.g., bit length, encoding scheme) documented in the SIRIUS API specification. Save the extracted fingerprint and metadata in a structured format (JSON or CSV) indexed by the original spectrum identifier for traceability and downstream integration with structure database lookup or CANOPUS classification workflows.

## Related tools

- **CSI:FingerID** (Web service component that accepts spectrum queries and returns predicted molecular fingerprints with confidence metrics) — https://github.com/sirius-ms/sirius
- **SIRIUS** (Java framework that integrates CSI:FingerID and provides the API gateway for dispatching spectrum queries to the fingerprint prediction service) — https://github.com/sirius-ms/sirius
- **CANOPUS** (Downstream tool that consumes molecular fingerprint predictions to assign systematic chemical classifications) — https://github.com/sirius-ms/sirius

## Evaluation signals

- JSON response contains all required fingerprint fields (vector, confidence/score, predictor mode indicator) with no missing or null values.
- Fingerprint vector length matches the documented bit length or dimension for the predictor model (e.g., consistent across all spectra in a batch).
- Confidence or quality scores fall within expected numeric range (e.g., 0–1 for probability, or documented threshold scale) and are not anomalous relative to other predictions in the dataset.
- Extracted fingerprint output files are valid JSON or CSV with consistent schema across all records, indexed by unique spectrum identifiers.
- Round-trip validation: submitted spectrum metadata and fragment peaks are correctly associated with the returned fingerprint in the output file.

## Limitations

- CSI:FingerID web services are restricted to academic research and education use only; commercial users must obtain licenses from Bright Giant GmbH.
- Fingerprint predictions depend on the quality and completeness of the input fragmentation tree and fragment peak annotations; low-quality spectra may yield low-confidence predictions.
- The JSON response schema may differ between CSI:FingerID API versions; parsers must be validated against the SIRIUS API specification version in use.
- No changelog is officially published, making it difficult to track breaking changes in response formats across software updates.

## Evidence

- [other] Parse the JSON response to extract the predicted molecular fingerprint representation and associated confidence or scoring metrics.: "Parse the JSON response to extract the predicted molecular fingerprint representation and associated confidence or scoring metrics."
- [other] Submit the HTTP POST request to the CSI:FingerID endpoint via the SIRIUS web service gateway.: "Submit the HTTP POST request to the CSI:FingerID endpoint via the SIRIUS web service gateway."
- [readme] Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services. Results are retrieved from the web service and can be displayed in the SIRIUS graphical user interface.: "Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services. Results are retrieved from the web service and can be displayed in the"
- [readme] The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only.: "The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only."
