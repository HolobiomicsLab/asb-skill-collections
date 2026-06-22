---
name: spectrum-query-formatting
description: Use when you have parsed LC-MS/MS spectral data (precursor m/z, ionization mode, collision energy, and a list of fragment m/z and intensity pairs) and need to submit it to the CSI:FingerID web service for molecular fingerprint prediction as part of a metabolite identification workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - CSI:FingerID
  - SIRIUS
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
---

# spectrum-query-formatting

## Summary

Prepare and encode mass spectrum metadata and fragment peaks into a valid CSI:FingerID web service request payload conforming to the SIRIUS API specification. This skill bridges raw or parsed LC-MS/MS data and the CSI:FingerID molecular fingerprint prediction service.

## When to use

You have parsed LC-MS/MS spectral data (precursor m/z, ionization mode, collision energy, and a list of fragment m/z and intensity pairs) and need to submit it to the CSI:FingerID web service for molecular fingerprint prediction as part of a metabolite identification workflow.

## When NOT to use

- You are working with low-resolution mass spectra or data lacking accurate precursor m/z values, as CSI:FingerID requires high-resolution MS data for reliable fingerprint prediction.
- You are submitting data for commercial purposes; the README states 'The SIRIUS web services...are for academic research and education use only.'
- You already have a molecular fingerprint prediction from another source and need only to validate or post-process it, rather than generate one de novo.

## Inputs

- Parsed mass spectrum with precursor m/z (accurate mass)
- Ionization mode (positive ion mode or negative ion mode)
- Collision energy (optional)
- Fragment peak list as m/z and intensity pairs
- SIRIUS API specification or valid endpoint documentation

## Outputs

- JSON-formatted CSI:FingerID web service request payload
- HTTP POST request conforming to SIRIUS API specification
- Confirmation of successful payload submission to the endpoint

## How to apply

Extract spectrum metadata including precursor m/z, ionization mode (positive or negative), and collision energy if available. Compile the fragment peak list as m/z and intensity pairs, ensuring peaks meet the service's quality thresholds. Construct the request payload by conforming to the SIRIUS API specification—the README indicates that Fragmentation trees and spectra are 'directly uploaded from SIRIUS to the CSI:FingerID...web services.' Format the payload as JSON per the SIRIUS API contract. Submit the HTTP POST request to the CSI:FingerID endpoint via the SIRIUS web service gateway. Validate that the request accepts the spectrum without schema or encoding errors before proceeding to fingerprint retrieval.

## Related tools

- **SIRIUS** (Web service gateway and framework that integrates CSI:FingerID and manages the HTTP POST dispatch of spectrum queries; also provides the API specification for payload formatting.) — https://github.com/sirius-ms/sirius
- **CSI:FingerID** (Target web service that accepts the formatted spectrum query payload and returns predicted molecular fingerprints with confidence scores.) — https://www.csi-fingerid.uni-jena.de/

## Evaluation signals

- The request payload conforms to the SIRIUS API JSON schema with no validation errors.
- The HTTP POST request is accepted by the CSI:FingerID endpoint (HTTP 200 or 202 response status).
- The response contains a valid molecular fingerprint representation and associated scoring or confidence metrics in the expected JSON structure.
- Precursor m/z, ionization mode, and fragment peaks are correctly encoded and match the input spectrum metadata without loss or corruption.
- The payload can be independently re-submitted and produces consistent fingerprint predictions.

## Limitations

- The skill assumes high-resolution mass spectrometry data; low m/z accuracy will result in unreliable fingerprint predictions.
- Fragment peak lists must be pre-filtered for noise; the service does not perform aggressive denoising and may misinterpret low-intensity artifacts.
- The CSI:FingerID web service is rate-limited and requires valid academic credentials; non-academic users must obtain licenses from Bright Giant GmbH.
- Collision energy metadata is optional but improves prediction confidence; its absence may reduce fingerprint ranking quality.
- The service requires network connectivity and is subject to the availability of the Böcker group's hosting infrastructure.

## Evidence

- [other] Prepare spectrum metadata and construct CSI:FingerID request: "Prepare spectrum metadata (precursor m/z, ionization mode, collision energy if available) and fragment peak list (m/z and intensity pairs). Construct a valid CSI:FingerID web service request payload"
- [other] Submit and parse web service response: "Submit the HTTP POST request to the CSI:FingerID endpoint via the SIRIUS web service gateway. Parse the JSON response to extract the predicted molecular fingerprint representation and associated"
- [readme] SIRIUS integrates and dispatches spectra to CSI:FingerID: "Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services."
- [readme] Academic use only restriction: "The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only."
- [readme] SIRIUS framework for LC-MS/MS analysis: "SIRIUS is a java-based software framework for the analysis of LC-MS/MS data of metabolites and other small molecules of biological interest."
