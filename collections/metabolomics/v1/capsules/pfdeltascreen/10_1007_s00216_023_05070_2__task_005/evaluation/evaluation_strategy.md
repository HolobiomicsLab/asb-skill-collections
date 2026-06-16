# Evaluation Strategy

## Direct Checks

- verify file exists at github:JonZwe__PFAScreen containing pipeline input stage code
- verify pipeline accepts CSV or TSV artifact as optional custom feature list input
- verify custom feature list input does not trigger pyOpenMS feature detection when supplied
- script_runs: execute pipeline with custom CSV feature list artifact and verify no errors or fallback to automated detection
- verify downstream MD/C filter reads and processes custom feature list records without modification to filter logic
- verify downstream KMD filter reads and processes custom feature list records without modification to filter logic
- verify downstream MS2 fragment filter reads and processes custom feature list records without modification to filter logic
- verify output of prioritization filters applied to custom feature data matches expected schema (any of: feature ID, m/z, retention time, prioritization score, filter pass/fail labels)
- expert_review: parameter-sensitive — confirm that MD/C, KMD, and MS2 thresholds are applied identically whether features originate from pyOpenMS detection or custom CSV supply

## Expert Review

- Review whether custom feature list format specification (column names, data types, required vs. optional fields) is documented or inferred from code
- Assess whether edge cases (missing m/z, missing MS2 data, malformed rows) are handled gracefully and do not silently corrupt downstream filter logic
- Evaluate whether any pyOpenMS-specific metadata (e.g. feature quality scores, detection confidence) is required or optional when using custom feature input
- Judge whether the prioritization filters produce chemically and statistically defensible PFAS rankings when applied to externally supplied feature data
