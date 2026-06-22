---
name: batch-script-execution-and-automation
description: Use when you have generated a peak table or feature list output file from an external peak-picking tool (MZmine, XCMS, MS-DIAL, or Compound Discoverer) in its native export format and need to ingest it into LipidMatch for lipid identification without manual column remapping or format conversion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# batch-script-execution-and-automation

## Summary

Execute batch files and conversion scripts to transform peak-picking software output into LipidMatch-compatible input format, automating the file-format handoff between external peak-picking tools (MZmine, XCMS, MS-DIAL, Compound Discoverer) and the LipidMatch analysis pipeline.

## When to use

You have generated a peak table or feature list output file from an external peak-picking tool (MZmine, XCMS, MS-DIAL, or Compound Discoverer) in its native export format and need to ingest it into LipidMatch for lipid identification without manual column remapping or format conversion.

## When NOT to use

- Input is already in LipidMatch-native format or has been previously converted
- Using Waters mass spectrometry instruments or file formats, which LipidMatch does not currently support
- Peak-picking output is from a tool not in the supported list (MZmine, XCMS, MS-DIAL, Compound Discoverer)

## Inputs

- peak table or feature list output file from MZmine, XCMS, MS-DIAL, or Compound Discoverer in native export format

## Outputs

- LipidMatch-compatible input file with mapped columns (m/z, retention time, intensity)

## How to apply

Obtain the peak table output file from your chosen peak-picking software in its native export format. Retrieve the LipidMatch batch file and associated conversion scripts from the GarrettLab-UF/LipidMatch GitHub repository. Execute the batch file or conversion script against your peak-picker output file, which will automatically transform the data into LipidMatch-compatible format while mapping all required columns (m/z, retention time, intensity). After execution, validate the converted file structure against the LipidMatch input schema by checking row count, column headers, and data types to confirm successful format translation before proceeding to lipid identification.

## Related tools

- **LipidMatch** (downstream analysis pipeline that accepts the converted peak-picking output for lipid identification via in-silico fragment matching) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (upstream peak-picking tool generating feature lists that serve as input to the batch conversion process)
- **XCMS** (upstream peak-picking tool generating feature lists that serve as input to the batch conversion process)
- **MS-DIAL** (upstream peak-picking tool generating feature lists that serve as input to the batch conversion process)
- **Compound Discoverer** (upstream peak-picking tool generating feature lists that serve as input to the batch conversion process)

## Evaluation signals

- Converted file row count matches the original peak table (no data loss during transformation)
- All required columns (m/z, retention time, intensity) are present with correct headers in the output file
- Data types of numeric columns (m/z, intensity values) are correctly preserved as numeric, not text
- No NULL or missing values appear in mandatory columns after conversion
- Converted file successfully loads into LipidMatch without schema validation errors on subsequent ingestion

## Limitations

- LipidMatch does not currently support Waters instrument file formats
- Conversion scripts are tool-specific; output from peak-picking tools outside the supported list (MZmine, XCMS, MS-DIAL, Compound Discoverer) may require custom adaptation
- Column mapping assumes standard export formats from peak-picking tools; non-standard or custom exports may fail without modification to conversion scripts

## Evidence

- [other] a batch file for MZmine processing is provided in the repository to facilitate this file-format handoff: "a batch file for MZmine processing is provided in the repository to facilitate this file-format handoff"
- [other] Execute the batch file or conversion script to transform the peak-picker output into the LipidMatch-compatible input format, ensuring all required columns (m/z, retention time, intensity) are mapped correctly.: "Execute the batch file or conversion script to transform the peak-picker output into the LipidMatch-compatible input format, ensuring all required columns (m/z, retention time, intensity) are mapped"
- [other] Validate the converted file structure against LipidMatch input schema (row count, column headers, data types) to confirm successful format translation: "Validate the converted file structure against LipidMatch input schema (row count, column headers, data types) to confirm successful format translation"
- [readme] a batch file for lipidomics with MZmine processing, and LipidMatch software/scripts: "a batch file for lipidomics with MZmine processing, and LipidMatch software/scripts"
- [readme] The software does not currently support Waters files: "The software does not currently support Waters files"
