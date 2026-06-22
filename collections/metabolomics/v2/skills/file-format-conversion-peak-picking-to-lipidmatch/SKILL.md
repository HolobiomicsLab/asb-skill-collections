---
name: file-format-conversion-peak-picking-to-lipidmatch
description: Use when you have generated a peak table or feature list from MZmine, XCMS, MS-DIAL, or Compound Discoverer and need to ingest it into LipidMatch for lipid identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-017-1744-3
  all_source_dois:
  - 10.1186/s12859-017-1744-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-format-conversion-peak-picking-to-lipidmatch

## Summary

Convert peak-picking output from external tools (MZmine, XCMS, MS-DIAL, Compound Discoverer) into LipidMatch-compatible input format by mapping required columns (m/z, retention time, intensity) and validating schema compliance. This skill bridges the gap between modular peak detection workflows and LipidMatch's lipid identification pipeline.

## When to use

You have generated a peak table or feature list from MZmine, XCMS, MS-DIAL, or Compound Discoverer and need to ingest it into LipidMatch for lipid identification. The peak-picking output is in the native export format of the upstream tool and has not yet been converted to LipidMatch's input schema.

## When NOT to use

- Your input is already a feature table in LipidMatch format or from another tool already compatible with LipidMatch.
- Your peak-picking software is Waters, which is not currently supported by LipidMatch.
- You are working with Waters UHPLC-HRMS/MS data, as LipidMatch does not currently support Waters files.

## Inputs

- Peak table from MZmine (native export format)
- Feature list from XCMS (native export format)
- Peak/feature table from MS-DIAL (native export format)
- Peak table from Compound Discoverer (native export format)

## Outputs

- LipidMatch-compatible input file with mapped m/z, retention time, and intensity columns
- Validated feature table ready for lipid identification

## How to apply

Obtain the peak table output file in its native export format from your chosen peak-picking software. Retrieve the LipidMatch batch file and conversion scripts from the GarrettLab-UF/LipidMatch GitHub repository. Execute the batch file or conversion script to transform the peak-picker output, ensuring m/z, retention time, and intensity columns are correctly mapped. Validate the converted file structure against LipidMatch's input schema by checking row count, column headers, and data types match expected values. Confirm the file is ready for downstream lipid identification matching against the in-silico fragmentation library.

## Related tools

- **MZmine** (Source peak-picking tool; generates peak tables in native format for conversion)
- **XCMS** (Source peak-picking tool; generates feature lists in native format for conversion)
- **MS-DIAL** (Source peak-picking tool; generates peak tables in native format for conversion)
- **Compound Discoverer** (Source peak-picking tool; generates peak tables in native format for conversion)
- **LipidMatch** (Target tool accepting converted peak-picking output for lipid identification) — https://github.com/GarrettLab-UF/LipidMatch

## Evaluation signals

- Converted file contains all required columns: m/z, retention time, and intensity with no missing values in critical rows.
- Column headers match LipidMatch's expected input schema exactly (case-sensitive and proper order).
- Data types are correct: m/z and retention time as numeric (float), intensity as numeric, row count matches original peak table.
- File can be successfully loaded into LipidMatch without parser errors or schema validation failures.
- Spot-check: sample of converted rows shows accurate mapping from original peak-picker columns (e.g., m/z values are unchanged, retention times preserved).

## Limitations

- Waters UHPLC-HRMS/MS files are not currently supported by LipidMatch, so conversion from Waters-based peak-picking tools will fail.
- Conversion accuracy depends on correct identification and mapping of column names from each peak-picker's native format; non-standard column naming in the source file may require manual adjustment.
- The batch file and conversion scripts are specifically designed for the tools listed (MZmine, XCMS, MS-DIAL, Compound Discoverer); conversion from other peak-picking software may require custom script modification.

## Evidence

- [other] Locate the LipidMatch batch file and conversion scripts from the GarrettLab-UF/LipidMatch GitHub repository.: "Locate the LipidMatch batch file and conversion scripts from the GarrettLab-UF/LipidMatch GitHub repository."
- [other] Execute the batch file or conversion script to transform the peak-picker output into the LipidMatch-compatible input format, ensuring all required columns (m/z, retention time, intensity) are mapped correctly.: "Execute the batch file or conversion script to transform the peak-picker output into the LipidMatch-compatible input format, ensuring all required columns (m/z, retention time, intensity) are mapped"
- [other] Validate the converted file structure against LipidMatch input schema (row count, column headers, data types) to confirm successful format translation.: "Validate the converted file structure against LipidMatch input schema (row count, column headers, data types) to confirm successful format translation."
- [readme] LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer): "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
- [readme] The software does not currently support Waters files: "The software does not currently support Waters files"
- [readme] a batch file for lipidomics with MZmine processing: "a batch file for lipidomics with MZmine processing"
