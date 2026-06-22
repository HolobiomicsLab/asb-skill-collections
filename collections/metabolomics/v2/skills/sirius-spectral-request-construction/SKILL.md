---
name: sirius-spectral-request-construction
description: Use when when you have processed LC-MS/MS data with precursor m/z, ionization mode, collision energy (if available), and fragment peak lists (m/z and intensity pairs), and need to query CSI:FingerID for molecular fingerprint predictions as part of an automated metabolite identification workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - CSI:FingerID
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
- SIRIUS is a java-based software framework for the analysis of LC-MS/MS data
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

# Construct and submit CSI:FingerID web-service requests from parsed mass spectra

## Summary

Format parsed LC-MS/MS spectra into valid CSI:FingerID web service request payloads conforming to the SIRIUS API specification, then submit via HTTP POST to obtain predicted molecular fingerprint predictions. This skill bridges raw spectrum data and the SIRIUS integrated analysis framework.

## When to use

When you have processed LC-MS/MS data with precursor m/z, ionization mode, collision energy (if available), and fragment peak lists (m/z and intensity pairs), and need to query CSI:FingerID for molecular fingerprint predictions as part of an automated metabolite identification workflow.

## When NOT to use

- Input spectrum data has not been preprocessed or validated (missing precursor m/z or fragment peaks)
- User account lacks academic credentials or does not have active license for non-academic use via Bright Giant GmbH
- The goal is structure generation de novo rather than fingerprint-based library matching (use MSNovelist instead)

## Inputs

- Parsed mass spectrum with precursor m/z (float)
- Ionization mode (positive or negative, enum)
- Fragment peak list (array of m/z and intensity pairs)
- Collision energy (optional, numeric or null)
- SIRIUS API credentials (user account token)

## Outputs

- Molecular fingerprint prediction (binary or probability vector)
- Confidence or scoring metrics (numeric)
- Structured fingerprint output (JSON or CSV format)

## How to apply

Prepare spectrum metadata including precursor m/z, ionization mode (positive or negative), and collision energy if available. Construct a valid CSI:FingerID request payload conforming to the SIRIUS API specification, encoding the fragment peak list as m/z and intensity pairs. Submit the payload as an HTTP POST request to the CSI:FingerID endpoint via the SIRIUS web service gateway. Parse the returned JSON response to extract the predicted molecular fingerprint representation and associated confidence or scoring metrics. Save the fingerprint output in structured format (JSON or CSV) for downstream analysis such as library matching or structural classification via CANOPUS.

## Related tools

- **SIRIUS** (Java-based framework that integrates CSI:FingerID web service dispatch, provides API specification, and manages HTTP communication with the web service gateway) — https://github.com/sirius-ms/sirius
- **CSI:FingerID** (Web service component that receives spectrum query requests and returns predicted molecular fingerprints with confidence metrics) — https://www.csi-fingerid.uni-jena.de/v3.0/api/
- **CANOPUS** (Downstream classifier that receives CSI:FingerID fingerprint predictions and assigns systematic chemical classifications) — https://github.com/sirius-ms/sirius

## Evaluation signals

- HTTP POST request returns status 200 and valid JSON response (not 4xx or 5xx error)
- Returned JSON contains 'fingerprint' and 'score' or 'confidence' fields matching the SIRIUS API schema
- Fingerprint vector dimensions match the expected size for the ionization mode (positive or negative predictor)
- Scored fingerprints can be matched against training structures via the public training structures API endpoints
- Output can be serialized to CSV or JSON without schema validation errors and consumed by downstream CANOPUS classifier

## Limitations

- CSI:FingerID web services are restricted to academic research and education use only; non-academic users must obtain licenses from Bright Giant GmbH
- Fingerprint predictions are probabilistic and depend on training data coverage; confidence scores do not guarantee structural correctness
- Request submission requires active user account and internet connectivity to the Böcker group web service gateway
- Collision energy is optional but when unavailable may reduce fingerprint prediction confidence

## Evidence

- [other] Prepare spectrum metadata (precursor m/z, ionization mode, collision energy if available) and fragment peak list (m/z and intensity pairs): "Prepare spectrum metadata (precursor m/z, ionization mode, collision energy if available) and fragment peak list (m/z and intensity pairs)."
- [other] Construct a valid CSI:FingerID web service request payload conforming to the SIRIUS API specification: "Construct a valid CSI:FingerID web service request payload conforming to the SIRIUS API specification."
- [other] Submit the HTTP POST request to the CSI:FingerID endpoint via the SIRIUS web service gateway: "Submit the HTTP POST request to the CSI:FingerID endpoint via the SIRIUS web service gateway."
- [other] Parse the JSON response to extract the predicted molecular fingerprint representation and associated confidence or scoring metrics: "Parse the JSON response to extract the predicted molecular fingerprint representation and associated confidence or scoring metrics."
- [readme] SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only: "The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only"
- [readme] both the graphical user interface and the command line version of SIRIUS seamlessly integrate the CSI:FingerID, CANOPUS and MSNovelist web services: "both the graphical user interface and the command line version of SIRIUS seamlessly integrate the CSI:FingerID, CANOPUS and MSNovelist web services."
