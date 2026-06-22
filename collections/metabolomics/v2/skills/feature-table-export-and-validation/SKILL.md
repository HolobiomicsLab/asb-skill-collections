---
name: feature-table-export-and-validation
description: Use when after executing an MZmine batch processing workflow on raw metabolomics data (mzML/mzXML format), when you need to convert the in-memory feature detection and alignment results into a shareable, schema-compliant tabular format suitable for downstream statistical analysis, figure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MZmine
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1101/2024.05.13.593988v1
  title: plantMASST
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_plantmasst_2_cq
    doi: 10.1101/2024.05.13.593988v1
    title: plantMASST
  dedup_kept_from: coll_plantmasst_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.05.13.593988v1
  all_source_dois:
  - 10.1101/2024.05.13.593988v1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-table-export-and-validation

## Summary

Export processed metabolomics feature tables from MZmine in standardized formats (CSV, mzTab) and validate output dimensions and content against repository documentation or expected schema. This skill ensures that feature detection, alignment, and normalization workflows produce compliant, reproducible tabular outputs.

## When to use

After executing an MZmine batch processing workflow on raw metabolomics data (mzML/mzXML format), when you need to convert the in-memory feature detection and alignment results into a shareable, schema-compliant tabular format suitable for downstream statistical analysis, figure generation, or archival in a computational biology repository.

## When NOT to use

- Input is already a validated, repository-archived feature table (skip to downstream analysis).
- Raw mass spectrometry data has not yet been loaded into MZmine or batch processing has not completed.
- The analysis goal does not require standardized tabular output (e.g., only internal MZmine visualizations are needed).

## Inputs

- MZmine batch processing configuration file
- Raw metabolomics data in mzML or mzXML format
- MZmine feature detection and alignment result object (in-memory)

## Outputs

- Processed feature table in CSV format
- Processed feature table in mzTab format
- Validation report (schema conformance, row/column counts, data type checks)

## How to apply

Within MZmine, configure the export step of the batch processing workflow to output the aligned feature table in CSV or mzTab format, specifying output columns (feature ID, m/z, retention time, peak area, sample intensities) according to the repository's documented schema. After export, programmatically validate the output by checking (1) table dimensions match expected row counts (features) and column counts (samples plus metadata), (2) numeric columns contain valid intensities or peak areas within physically plausible ranges, (3) feature annotations (m/z, RT) are present and non-null, and (4) the file parses correctly in the target analysis environment (Python/R). Compare the exported table structure against any reference schemas or prior outputs documented in the repository to detect format regressions or missing columns.

## Related tools

- **MZmine** (Execute batch feature detection, alignment, and normalization; configure and invoke export step to produce feature tables in CSV or mzTab format.) — github.com/helenamrusso/plantmasst

## Evaluation signals

- Output file parses without error in Python (pandas.read_csv) or R (read.csv) and matches declared schema (column names, data types, row count).
- Feature table dimensions (row count ≥ expected number of detected features, column count = samples + metadata columns) are consistent with batch processing inputs and repository documentation.
- Numeric columns (intensities, peak areas, m/z, retention time) contain non-negative values within physically plausible ranges for the instrument and sample type; no unexpected NaN or Inf values.
- Feature identifiers are unique and non-null; metadata columns (sample names, feature IDs) match the input sample list and expected naming conventions from the repository.
- File format (CSV delimiter, header row, encoding) matches the target downstream tool requirements (e.g., statistical software or figure generation notebooks).

## Limitations

- Export format and field availability depend on MZmine version and batch configuration; older or custom configurations may omit columns required by repository documentation.
- CSV export may lose precision for very large intensity values or require special handling for scientific notation; mzTab is recommended for higher-fidelity archival.
- Validation schema is repository-specific; portable validation across different metabolomics projects requires explicit schema mapping or format standardization.
- No changelog or version tracking documented for the plantMASST repository, so historical format changes are not tracked; practitioners must manually verify compatibility with prior outputs.

## Evidence

- [other] Execute the MZmine batch workflow to perform feature detection, alignment, and normalization as specified in the input configuration.: "Execute the MZmine batch workflow to perform feature detection, alignment, and normalization as specified in the input configuration."
- [other] Export the processed feature table in a standardized tabular format (CSV or mzTab).: "Export the processed feature table in a standardized tabular format (CSV or mzTab)."
- [other] Validate the output feature table dimensions and content against repository documentation or expected schema.: "Validate the output feature table dimensions and content against repository documentation or expected schema."
- [readme] It is organized around the main tables used in the study, the notebooks that generate figure panels, the MZmine inputs used for metabolomics processing, and the supplementary HTML outputs produced from the analyses used as use cases.: "It is organized around the main tables used in the study, the notebooks that generate figure panels, the MZmine inputs used for metabolomics processing, and the supplementary HTML outputs produced"
- [readme] MZmine/: input files and batch files for the metabolomics datasets used in as use cases in this project.: "MZmine/: input files and batch files for the metabolomics datasets used in as use cases in this project."
