# Evaluation Strategy

## Direct Checks

- Verify that https://pairedomicsdata.bioinformatics.nl/api/projects (or equivalent endpoint) is accessible and returns HTTP 200
- Verify that the retrieved response is valid JSON (parseable without syntax errors)
- Verify that each project document in the response array contains the required top-level keys present in app/public/schema.json (file_format_is check: robust to schema version updates)
- Verify that the JSON Schema definition exists at app/public/schema.json in the iomega/paired-data-form repository
- For a sample of ≥5 randomly selected project documents, validate each against the published schema using a JSON Schema validator (e.g., ajv or jsonschema); output: pass/fail per document
- Verify that all project documents conform to the schema with no validation errors (no canonical answer for sample size; expert review may recommend full census)

## Expert Review

- Assess whether the sample size (if sampling is used) is adequate for detecting schema drift or widespread malformation
- Verify that the schema definition itself is syntactically correct and complete (e.g., all referenced definitions are present)
- Assess whether any observed validation failures indicate a genuine platform issue or expected variability in optional fields
