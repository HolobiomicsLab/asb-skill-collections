---
name: compound-class-annotation-parsing
description: Use when after submitting a fingerprint or spectrum query to the CANOPUS
  web service and receiving a structured response.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0153
  tools:
  - CANOPUS
  - SIRIUS
  techniques:
  - LC-MS
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

# compound-class-annotation-parsing

## Summary

Parse and validate structured compound-class annotation results returned by CANOPUS web service queries, extracting predicted compound classes and confidence scores into a standardized tabular or JSON format. This skill ensures annotation completeness and conformance before downstream structural or metabolomic interpretation.

## When to use

Apply this skill after submitting a fingerprint or spectrum query to the CANOPUS web service and receiving a structured response. Use it when you need to validate that the response contains all required fields (compound class, probability/confidence), standardize the format for downstream analysis, and ensure the annotation result is ready for integration into a metabolite identification workflow.

## When NOT to use

- Input is raw MS/MS spectra or fingerprints not yet submitted to CANOPUS—submit to the web service first.
- You need structural candidate ranking or de novo structure generation—use CSI:FingerID or MSNovelist instead.
- Annotation results are already integrated into a SIRIUS GUI session—the GUI handles parsing internally.

## Inputs

- CANOPUS web service JSON or tabular response
- structured annotation result containing compound-class predictions

## Outputs

- parsed and validated compound-class annotation table (CSV/TSV/JSON)
- standardized records with compound class and confidence score fields
- validation report (records passed, failed, or incomplete)

## How to apply

Retrieve the structured JSON or tabular response from the CANOPUS web service endpoint. Parse the response to extract predicted compound classes and their associated confidence scores or probabilities. Validate that all required fields (compound class, probability/confidence) are present in each annotation record. Check that confidence scores fall within the expected range (typically 0–1 or 0–100%). Convert the parsed data into a standardized format (e.g., CSV, TSV, or JSON) suitable for storage or downstream analysis. Log any malformed or incomplete records for review.

## Related tools

- **CANOPUS** (web service that generates the structured compound-class annotation result to be parsed and validated) — https://bio.informatik.uni-jena.de/software/canopus/
- **SIRIUS** (Java-based framework that seamlessly integrates the CANOPUS web service and handles result retrieval and display) — https://github.com/sirius-ms/sirius

## Evaluation signals

- All returned records contain non-empty compound-class field.
- All confidence/probability scores are numeric and fall within valid range (0–1 or 0–100%).
- Parsed output schema matches expected structure: compound class, confidence score, and optional metadata (e.g., query ID, timestamp).
- No truncation, encoding errors, or malformed JSON/CSV in parsed output.
- Validation report accurately counts and categorizes passed and failed records with descriptive error messages for any malformed entries.

## Limitations

- CANOPUS web service is available for academic research and education use only; non-academic users require licenses from Bright Giant GmbH.
- Confidence scores reflect model predictions and should not be interpreted as ground truth; low-confidence predictions may require manual review or additional validation.
- Parsing assumes CANOPUS returns consistent JSON/tabular schema; changes in API response format may require script updates.
- This skill validates structure only; it does not assess biological relevance, consistency with reference databases, or cross-validation with other tools (CSI:FingerID, ZODIAC).

## Evidence

- [other] retrieve and parse the annotation result: "Retrieve the structured JSON or tabular response containing predicted compound classes and confidence scores. Parse and validate the annotation result to ensure required fields (compound class,"
- [readme] CANOPUS web service integration in SIRIUS: "Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services. Results are retrieved from the web service and can be displayed in the"
- [readme] academic-only restriction: "The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only."
- [readme] SIRIUS integration of CANOPUS: "SIRIUS integrates a collection of our tools, including CSI:FingerID (with COSMIC), ZODIAC, CANOPUS."
