---
name: mass-spectrometry-query-formulation
description: Use when you have a high-resolution LC-MS/MS experiment with a measured [M+H]+ or [M-H]− ion mass and optionally a parent ion fragmentation spectrum (peak list with m/z and intensity pairs), and you seek to generate candidate molecular structures for an unknown metabolite that may not be in.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MSNovelist
  - SIRIUS
  techniques:
  - LC-MS
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

# mass-spectrometry-query-formulation

## Summary

Construct a properly formatted query payload for submission to the MSNovelist web service, containing molecular ion mass and optional tandem mass spectrometry fragmentation data. This skill bridges LC-MS/MS experiment output and de-novo structure generation by encoding spectral inputs into the REST API contract expected by SIRIUS.

## When to use

You have a high-resolution LC-MS/MS experiment with a measured [M+H]+ or [M-H]− ion mass and optionally a parent ion fragmentation spectrum (peak list with m/z and intensity pairs), and you seek to generate candidate molecular structures for an unknown metabolite that may not be in existing spectral libraries. The query must be constructed before submitting to MSNovelist via the SIRIUS web service endpoint.

## When NOT to use

- The input is an already-retrieved set of candidate structures from a previous MSNovelist query—reformulation is not needed.
- You have only a low-resolution or nominal mass measurement (integer m/z); MSNovelist exploits high-mass accuracy, so nominal-mass queries will suffer reduced ranking power.
- Your analysis goal is to search an existing spectral database for known compounds rather than generate de-novo unknown structures.

## Inputs

- Molecular ion mass (m/z value, typically [M+H]+ or [M-H]−, high-resolution accurate mass)
- Tandem mass spectrum (optional): peak list with m/z and relative intensity values
- Ionization mode (positive or negative)
- Optionally: instrument metadata (resolution, mass accuracy tolerance)

## Outputs

- JSON-formatted query payload conforming to MSNovelist REST API schema
- HTTP POST request body ready for submission to SIRIUS web service endpoint

## How to apply

Prepare a JSON payload containing the molecular ion mass (accurate to at least four decimal places for high-resolution instruments) and, if available, the fragmentation spectrum data (m/z and intensity pairs). The payload format must match the MSNovelist REST API specification as integrated into SIRIUS. If fragmentation data is provided, include it as a peak list within the query structure; otherwise, submit mass-only queries for initial candidate generation. Encode the payload using UTF-8 and submit via HTTP POST to the SIRIUS MSNovelist endpoint. The web service will accept the query and return a JSON response containing ranked candidate structures, so the query formulation step determines the quality and scope of downstream structure predictions.

## Related tools

- **SIRIUS** (Framework host and REST API endpoint provider for MSNovelist web service; processes the formatted query payload and returns structure candidates) — https://github.com/sirius-ms/sirius
- **MSNovelist** (De-novo structure generation engine that consumes the query payload (molecular ion mass and fragmentation spectrum) and outputs ranked candidate structures)

## Evaluation signals

- JSON payload validates against the MSNovelist API schema (no parse errors when submitted to SIRIUS endpoint)
- Molecular ion mass is included with sufficient decimal precision (≥4 decimal places for high-resolution MS)
- If fragmentation spectrum is included, peak list contains both m/z and intensity fields with numeric values
- HTTP POST submission returns a 200 OK response with a JSON response body containing a 'candidates' or 'structures' array
- Returned candidate structures are ranked by score and include SMILES or InChI representations

## Limitations

- MSNovelist web service is restricted to academic research and education use only; non-academic users must obtain a commercial license from Bright Giant GmbH.
- Query formulation with only mass (no fragmentation spectrum) produces broader candidate sets with lower discrimination; inclusion of tandem MS data significantly improves ranking.
- The web service response quality depends on the chemical space covered by the training data; novel or highly unusual structural classes may receive lower-confidence rankings.
- User authentication via institutional email is required; non-standard academic domains may require manual validation before web service access is granted.

## Evidence

- [other] Prepare query payload containing molecular ion mass and optional fragmentation spectrum data: "Prepare query payload containing molecular ion mass and optional fragmentation spectrum data in the format accepted by the MSNovelist REST API endpoint."
- [readme] MSNovelist web service endpoint in SIRIUS framework: "Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services."
- [other] Web service returns JSON with ranked structures: "Retrieve JSON-formatted response containing ranked candidate structures and associated scores."
- [readme] Academic-only usage restriction: "The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only."
- [readme] SIRIUS integration with MSNovelist: "SIRIUS integrates a collection of our tools, including CSI:FingerID (with COSMIC), ZODIAC, CANOPUS. In particular, both the graphical user interface and the command line version of SIRIUS seamlessly"
