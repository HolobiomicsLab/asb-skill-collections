---
name: mass-spectrometry-data-column-mapping
description: Use when you have generated a peak table or feature list from MZmine, XCMS, MS-DIAL, or Compound Discoverer in its native export format and need to ingest it into LipidMatch for lipid identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - LipidMatch
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)
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
---

# mass-spectrometry-data-column-mapping

## Summary

Convert peak-picking output from external mass spectrometry software (MZmine, XCMS, MS-DIAL, Compound Discoverer) into LipidMatch-compatible input format by mapping required columns (m/z, retention time, intensity) and validating schema compliance. This skill bridges the file-format handoff between heterogeneous peak-picker tools and a downstream lipidomics annotation pipeline.

## When to use

You have generated a peak table or feature list from MZmine, XCMS, MS-DIAL, or Compound Discoverer in its native export format and need to ingest it into LipidMatch for lipid identification. The source peak-picker output has columns that do not directly align with LipidMatch's required input schema (e.g., different column names, missing retention time, or non-standard m/z precision).

## When NOT to use

- Input peak table is already in LipidMatch format (column names, data types, and schema already match) — skip directly to LipidMatch annotation.
- Peak-picking software output is from Waters instruments, as LipidMatch does not currently support Waters files.
- Peak table is incomplete or missing critical columns (m/z, retention time, or intensity) that cannot be recovered or imputed from the source file.

## Inputs

- Peak table or feature list file from MZmine, XCMS, MS-DIAL, or Compound Discoverer (native format: .csv, .txt, or proprietary export)
- LipidMatch batch file or conversion script from GarrettLab-UF/LipidMatch repository

## Outputs

- LipidMatch-compatible input file with mapped columns (m/z, retention time, intensity) in correct format and data types
- Validation report confirming schema compliance (row count, column headers, data types)

## How to apply

Obtain the peak table output file from your selected peak-picking software in its native export format (e.g., MZmine .csv, XCMS feature table, MS-DIAL .txt). Locate the LipidMatch batch file and conversion scripts from the GarrettLab-UF/LipidMatch GitHub repository. Execute the batch file or conversion script to transform the peak-picker output, ensuring all required columns (m/z, retention time, intensity) are mapped to the correct LipidMatch field names and data types. Validate the converted file structure by confirming row count preservation, expected column headers, and numeric data types match LipidMatch input schema. Spot-check a sample of m/z and retention time values in the converted file against the original peak-picker output to confirm no truncation or precision loss occurred during conversion.

## Related tools

- **LipidMatch** (Target annotation tool; consumes the converted peak table to perform lipid identification via in-silico fragmentation matching) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Upstream peak-picking and feature detection; generates the native peak table to be converted)
- **XCMS** (Alternative peak-picking and feature detection software; generates feature table for conversion)
- **MS-DIAL** (Alternative peak-picking and feature detection software; generates feature table for conversion)
- **Compound Discoverer** (Alternative peak-picking and feature detection software; generates feature table for conversion)

## Evaluation signals

- Row count in converted file matches original peak-picker output (no rows lost or duplicated during conversion).
- Column headers in converted file exactly match LipidMatch schema (m/z, retention time, intensity, and any additional expected fields).
- Numeric data types are preserved: m/z and intensity as decimal/float; retention time as numeric (seconds or minutes, consistently formatted).
- Spot-checked m/z values in converted file match source peak-picker file within machine precision (no truncation to <4 decimal places).
- File structure passes LipidMatch input validation (parser accepts file without schema or type errors when loaded into LipidMatch).

## Limitations

- Conversion script assumes peak-picker column naming conventions; non-standard or renamed columns in source file may cause mapping failures.
- No automatic handling of missing or null values in critical columns (m/z, retention time, intensity); source peak-picker output must be complete.
- Different peak-picker software may export retention time in different units (seconds vs. minutes); conversion script may require manual unit adjustment or parameter configuration.
- Waters instrument files are not supported by LipidMatch, making column mapping from Waters-specific peak-pickers impossible.
- No changelog available to track breaking changes in LipidMatch input schema across software versions; schema validation must be performed with the specific LipidMatch version in use.

## Evidence

- [other] Obtain the peak table or feature list output file from the selected peak-picking software (MZmine, XCMS, MS-DIAL, or Compound Discoverer) in its native export format.: "Obtain the peak table or feature list output file from the selected peak-picking software (MZmine, XCMS, MS-DIAL, or Compound Discoverer) in its native export format."
- [other] Execute the batch file or conversion script to transform the peak-picker output into the LipidMatch-compatible input format, ensuring all required columns (m/z, retention time, intensity) are mapped correctly.: "Execute the batch file or conversion script to transform the peak-picker output into the LipidMatch-compatible input format, ensuring all required columns (m/z, retention time, intensity) are mapped"
- [other] Validate the converted file structure against LipidMatch input schema (row count, column headers, data types) to confirm successful format translation.: "Validate the converted file structure against LipidMatch input schema (row count, column headers, data types) to confirm successful format translation."
- [readme] LipidMatch is modular, allowing it to fit in various workflows you may have in your lab. For example LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer): "LipidMatch is modular, allowing it to fit in various workflows you may have in your lab. For example LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and"
- [readme] The link at the bottom of this page contains a manual, lipid libraries in .csv format, a batch file for lipidomics with MZmine processing, and LipidMatch software/scripts.: "The link at the bottom of this page contains a manual, lipid libraries in .csv format, a batch file for lipidomics with MZmine processing, and LipidMatch software/scripts."
- [readme] The software does not currently support Waters files.: "The software does not currently support Waters files."
