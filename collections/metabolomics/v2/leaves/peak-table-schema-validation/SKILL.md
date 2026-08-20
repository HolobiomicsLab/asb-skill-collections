---
name: peak-table-schema-validation
description: Use when after converting peak-picker output (from MZmine, XCMS, MS-DIAL,
  or Compound Discoverer) into LipidMatch-compatible format. Use this skill when you
  need to verify that the converted file will be successfully read by LipidMatch before
  proceeding to lipid identification;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3197
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3370
  tools:
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - LipidMatch
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- LipidMatch can be used with various peak picking software (for example MZmine, XCMS,
  MS-DIAL, and Compound Discoverer)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-017-1744-3
  all_source_dois:
  - 10.1186/s12859-017-1744-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-table-schema-validation

## Summary

Validate that peak-picking output files conform to the LipidMatch input schema before ingestion, ensuring all required columns (m/z, retention time, intensity) are present, correctly named, and properly typed. This prevents silent failures and data loss during the format handoff between external peak-picking software and the lipid identification pipeline.

## When to use

After converting peak-picker output (from MZmine, XCMS, MS-DIAL, or Compound Discoverer) into LipidMatch-compatible format. Use this skill when you need to verify that the converted file will be successfully read by LipidMatch before proceeding to lipid identification; it is especially important when batch-converting multiple peak tables or when integrating peak-picking output from new instruments or experimental protocols.

## When NOT to use

- Input is already a validated LipidMatch feature table from a previous successful run — skip directly to identification.
- You are performing initial exploratory peak-picking and do not yet need to integrate with LipidMatch.
- The peak-picking software has its own built-in output validation and you trust its schema — though manual spot-checks are still recommended for new instrument/protocol combinations.

## Inputs

- peak table or feature list file from peak-picking software (MZmine, XCMS, MS-DIAL, or Compound Discoverer native export format)
- converted peak table file in proposed LipidMatch-compatible format
- LipidMatch input schema specification (column names, data types, required fields)

## Outputs

- validation report (pass/fail with specific column, row, and data-type errors identified)
- validated peak table file ready for LipidMatch ingestion

## How to apply

Load the converted peak table file and inspect its structure against the LipidMatch input schema. Verify row count (non-empty feature list), column headers (presence and spelling of m/z, retention time, intensity columns), and data types (numeric values in m/z and intensity columns, real-valued retention times). Check for missing values, out-of-range values (e.g., negative m/z or intensity), and correct decimal formatting. If the file is CSV or tab-delimited, validate delimiter consistency and quote handling. Compare the file structure to a known-good LipidMatch input file from the repository batch workflow. If validation passes, the file is ready for LipidMatch analysis; if it fails, return to the conversion script and correct the mapping of peak-picker output columns to LipidMatch requirements.

## Related tools

- **LipidMatch** (Target software into which the validated peak table is ingested for lipid identification via m/z matching against in-silico fragmentation libraries) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak-picking software producing feature lists that must be validated and converted to LipidMatch input format)
- **XCMS** (Peak-picking software producing feature lists that must be validated and converted to LipidMatch input format)
- **MS-DIAL** (Peak-picking software producing feature lists that must be validated and converted to LipidMatch input format)
- **Compound Discoverer** (Peak-picking software producing feature lists that must be validated and converted to LipidMatch input format)

## Evaluation signals

- Row count matches expected number of features detected by peak-picker (no rows lost or duplicated during conversion).
- Column headers exactly match LipidMatch requirements: m/z, retention time, intensity (or schema-specified aliases); no extra or missing columns that would cause parser errors.
- All m/z and intensity values are numeric and positive; retention time values are non-negative real numbers in expected units (minutes or seconds).
- No missing or NaN values in required columns; missing values in optional columns are handled consistently (empty string vs. 0 vs. explicit null marker).
- File can be successfully parsed by LipidMatch reader without encoding, delimiter, or quote-escaping errors; spot-check a sample of 5–10 rows manually against raw peak-picker output to confirm accurate column mapping.

## Limitations

- LipidMatch does not currently support Waters files; peak tables from Waters instruments must be exported in a neutral format (CSV, TSV) before validation.
- Schema validation does not check semantic correctness (e.g., whether m/z values are physically plausible for the instrument used, or whether retention times are monotonically increasing). Instrument-specific range checks (e.g., Q-Exactive m/z range ~50–2000) require additional domain knowledge.
- Validation is format-agnostic and does not verify consistency with the experimental protocol or acquisition parameters (e.g., whether feature intensity is in raw counts, normalized, or log-transformed); such checks require knowledge of the peak-picker configuration.

## Evidence

- [other] Validate the converted file structure against LipidMatch input schema (row count, column headers, data types) to confirm successful format translation.: "Validate the converted file structure against LipidMatch input schema (row count, column headers, data types) to confirm successful format translation."
- [readme] LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer): "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
- [other] ensuring all required columns (m/z, retention time, intensity) are mapped correctly: "ensuring all required columns (m/z, retention time, intensity) are mapped correctly"
- [readme] a batch file for lipidomics with MZmine processing: "a batch file for lipidomics with MZmine processing"
- [readme] The software does not currently support Waters files: "The software does not currently support Waters files"
