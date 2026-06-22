---
name: isf-feature-table-export
description: Use when after completing Part 4 (Identification of ISF Features) in the ISFrag workflow, when you have an ISFrag analysis results object containing identified ISF features and need to save them as a portable, tabular file for external analysis, reporting, or integration with other metabolomics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3751
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - ISFrag
  - R
  - RStudio
derived_from:
- doi: 10.1021/acs.analchem.1c01644
  title: ISFrag
evidence_spans:
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table.
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table
- To install ISFrag package R version 4.0.0 or above is required
- we recommend using RStudio to complete the installation and usage of ISFrag
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isfrag_cq
    doi: 10.1021/acs.analchem.1c01644
    title: ISFrag
  dedup_kept_from: coll_isfrag_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c01644
  all_source_dois:
  - 10.1021/acs.analchem.1c01644
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct the ISF Result Feature Table export

## Summary

Export identified in-source fragment (ISF) features from ISFrag analysis results into a structured tabular result file (CSV or TSV format). This skill formats and serializes ISF annotations, parent–fragment relationships, and confidence scores for downstream interpretation and data sharing.

## When to use

After completing Part 4 (Identification of ISF Features) in the ISFrag workflow, when you have an ISFrag analysis results object containing identified ISF features and need to save them as a portable, tabular file for external analysis, reporting, or integration with other metabolomics workflows.

## When NOT to use

- ISF feature identification has not yet been completed (Part 4 results are not available).
- You need hierarchical or tree-structured output of ISF relationships (use Part 5.2 Export ISF Relationship Tree instead).
- The ISFrag analysis results object is empty or contains no identified ISF features.

## Inputs

- ISFrag analysis results object containing identified ISF features (from Part 4)
- Output directory path (string)

## Outputs

- ISF Result Feature Table file (CSV or TSV format)
- Structured tabular data with columns: feature identifiers, ISF annotations, parent–fragment relationships, confidence scores

## How to apply

Load the ISFrag analysis results object from Part 4 containing the identified ISF features. Use ISFrag's Part 5.1 export function to automatically format the identified ISF features into a tabular structure with columns for feature identifiers, ISF annotations, parent–fragment relationship links, and confidence scores. Select a standard output format (CSV or TSV) and execute the export function, which will write the formatted feature table to disk. Verify that all expected columns are present and that row counts match the number of identified ISF features in the results object.

## Related tools

- **ISFrag** (R package that provides the export function (Part 5.1) to serialize identified ISF features into tabular result files) — https://github.com/HuanLab/ISFrag.git
- **R** (Programming language runtime (version 4.0.0 or above required) in which ISFrag executes and writes output files)
- **RStudio** (Recommended IDE for executing ISFrag export functions and inspecting the resulting feature table file)

## Evaluation signals

- Output file (CSV or TSV) is created at the specified directory path and is readable and parseable.
- The exported table contains all expected columns: feature identifiers, ISF annotations, parent–fragment relationships, and confidence scores.
- Row count in the output file matches the number of identified ISF features in the input results object.
- All feature identifiers, annotation values, and confidence scores are non-null and match their corresponding entries in the results object.
- The tabular format is consistent (no jagged rows, proper delimiters) and compatible with downstream tools (R, Python, spreadsheet applications).

## Limitations

- Export function is only available after ISF feature identification (Part 4) has been completed; incomplete or failed prior analyses will result in empty or erroneous exports.
- Only CSV and TSV formats are supported; other formats require manual file conversion or custom scripts.
- The export does not include raw MS2 spectra or full metadata; it is a summary table of annotations and relationships only.

## Evidence

- [intro] ISFrag provides a Part 5.1 export function to output ISF Result Feature Table from identified ISF features as a structured result file.: "ISFrag provides a Part 5.1 export function to output ISF Result Feature Table from identified ISF features as a structured result file."
- [intro] Format the identified ISF features into a tabular result structure with appropriate columns (feature identifiers, ISF annotations, parent–fragment relationships, confidence scores).: "Format the identified ISF features into a tabular result structure with appropriate columns (feature identifiers, ISF annotations, parent–fragment relationships, confidence scores)."
- [intro] Export the formatted result feature table to a standard file format (CSV or TSV) using ISFrag's export functionality.: "Export the formatted result feature table to a standard file format (CSV or TSV) using ISFrag's export functionality."
- [readme] Part 5: Results Export: "[Part 5: Results Export] - [5.1 Export ISF Result Feature Table]"
