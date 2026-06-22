---
name: structured-result-validation
description: Use when after retrieving a JSON or tabular response from a web service endpoint (such as CANOPUS), validate the result before parsing or integrating it into your analysis pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - CANOPUS
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

# structured-result-validation

## Summary

Validate that structured annotation results from web service queries (e.g., CANOPUS compound-class predictions) contain required fields and conform to expected schemas before downstream analysis. This skill ensures data integrity and prevents propagation of malformed or incomplete predictions.

## When to use

After retrieving a JSON or tabular response from a web service endpoint (such as CANOPUS), validate the result before parsing or integrating it into your analysis pipeline. Apply this skill whenever you need to confirm that compound-class predictions include both a predicted class label and an associated confidence or probability score, and before using those predictions for further interpretation or filtering.

## When NOT to use

- Input is already a pre-filtered database of curated compound structures with no missing annotations.
- You are working only with molecular formula predictions (not compound class predictions).
- The downstream tool does not require confidence scores (though best practice is to retain them).

## Inputs

- JSON response object from CANOPUS web service
- tabular result file (TSV/CSV) with compound-class predictions and scores
- fingerprint or spectrum query submission result

## Outputs

- validated annotation result with confirmed compound class and probability/confidence fields
- validation report (pass/fail per record)
- cleaned or filtered annotation dataset ready for downstream analysis

## How to apply

Parse the structured response (JSON or tabular format) returned from the web service and check for presence of mandatory fields: compound class label and probability/confidence score. Verify data types (e.g., score is numeric and in valid range such as 0–1 or 0–100) and that no critical fields are null or missing. If validation fails, log the malformed record and either reject it or flag it for manual review; do not pass incomplete annotations downstream. The rationale is that CANOPUS predictions are only actionable if confidence is quantified alongside the class assignment, allowing users to filter by reliability threshold and avoid false positives in subsequent compound identification or pathway analysis steps.

## Related tools

- **CANOPUS** (web service that accepts fingerprint or spectrum queries and returns structured compound-class annotation results to be validated) — https://github.com/sirius-ms/sirius
- **SIRIUS** (Java-based framework that integrates and submits queries to CANOPUS web service; result validation is applied before displaying annotations in GUI or CLI) — https://github.com/sirius-ms/sirius

## Evaluation signals

- All retrieved records contain non-null compound class and probability/confidence fields.
- Confidence scores are numeric and within expected range (e.g., 0–1 or 0–100 depending on CANOPUS output format).
- No records with missing or malformed fields propagate past validation step.
- Validation report documents number of input records, number passing, and reasons for any rejections.
- Downstream analysis tools can successfully parse and use the validated annotations without schema errors.

## Limitations

- Validation logic assumes fixed schema (compound class + probability); custom or legacy versions of CANOPUS may use different field names or formats.
- Validation does not assess biological plausibility or accuracy of predictions—only structural completeness; confidence threshold tuning remains user-dependent.
- No built-in mechanism to recover or impute missing confidence scores; records missing this field are rejected entirely.

## Evidence

- [other] Parse and validate the annotation result to ensure required fields (compound class, probability/confidence) are present.: "Parse and validate the annotation result to ensure required fields (compound class, probability/confidence) are present."
- [other] Retrieve the structured JSON or tabular response containing predicted compound classes and confidence scores.: "Retrieve the structured JSON or tabular response containing predicted compound classes and confidence scores."
- [other] CANOPUS is offered as a web service component within the SIRIUS framework for academic research and education use, enabling remote submission of queries for compound-class annotation.: "CANOPUS is offered as a web service component within the SIRIUS framework for academic research and education use, enabling remote submission of queries for compound-class annotation."
- [readme] Both the graphical user interface and the command line version of SIRIUS seamlessly integrate the CSI:FingerID, CANOPUS and MSNovelist web services.: "Both the graphical user interface and the command line version of SIRIUS seamlessly integrate the CSI:FingerID, CANOPUS and MSNovelist web services."
