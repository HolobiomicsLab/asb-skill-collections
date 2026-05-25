---
name: tabular-data-parsing-and-structure-verification
description: Parse and validate the structure of tabular processing reports (e.g., Supplementary Table S1 from matchms library cleaning pipelines) by extracting numeric fields, verifying data types and field presence, and comparing extracted values against published statistics to confirm pipeline execution fidelity.
when_to_use_negative:
- The input is already a validated schema or has been previously verified by the data producer.
- The table documents intermediate filtering steps rather than aggregate final counts (use this skill only when validating summary statistics, not per-spectrum metadata).
- Reference statistics are unavailable or the article does not report concrete numeric counts for comparison.
edam_operation: http://edamontology.org/operation_2409
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: metadata cleaning and library filtering pipeline that produces the processing report to be parsed and verified
  repo: https://github.com/matchms/matchms
- name: Python (pandas)
  role: tabular data parsing and numeric extraction from CSV/Excel processing reports
- name: RDKit
  role: structure comparison and validation (referenced for resolving SMILES/InChI/InChIKey conflicts in repair operations)
provenance:
  source_task_ids:
  - task_007
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/tabular-data-parsing-and-structure-verification/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/tabular-data-parsing-and-structure-verification/skill.md
    merged_at: '2026-05-25T07:15:30.849071+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/tabular-data-parsing-and-structure-verification@sha256:00c8bba8ceb4f7e80b099912a9e9419c72eeb998b6c8cb38f07fd2216e7a1d90
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# tabular-data-parsing-and-structure-verification

## Summary

Parse and validate the structure of tabular processing reports (e.g., Supplementary Table S1 from matchms library cleaning pipelines) by extracting numeric fields, verifying data types and field presence, and comparing extracted values against published statistics to confirm pipeline execution fidelity.

## When to use

When you have a tabular artifact (CSV, Excel, or TSV) documenting the results of a metadata cleaning or filtering pipeline—specifically when you need to verify that reported summary statistics (e.g., 'input 500,569 spectra', 'removed 31,758', 'repaired 52,084', 'retained 448,485') match the actual counts in the table. This is essential for reproducibility validation of library cleaning workflows where intermediate and final counts are critical audit points.

## When NOT to use

- The input is already a validated schema or has been previously verified by the data producer.
- The table documents intermediate filtering steps rather than aggregate final counts (use this skill only when validating summary statistics, not per-spectrum metadata).
- Reference statistics are unavailable or the article does not report concrete numeric counts for comparison.

## Inputs

- Tabular processing report artifact (CSV, TSV, or Excel format)
- Reference statistics from article (numeric counts: input, removed, repaired, retained)

## Outputs

- Structured validation report (JSON or CSV) with field-by-field comparison results
- Pass/fail verdict for each field with absolute and relative differences
- Log of any missing or malformed fields

## How to apply

Load the tabular file using Python (e.g., pandas) and parse all rows and columns, ensuring headers are correctly identified. Validate that required numeric fields (total input, removed count, repaired count, retained count) are present and can be cast to integers without loss of precision. Extract the numeric values for each field, documenting any missing or malformed entries. Compare extracted counts field-by-field against the article-reported reference values using exact equality or a small tolerance (e.g., ±1 for rounding). If discrepancies exist, flag the field name, extracted value, expected value, and absolute difference in a structured validation report. This confirms that the processing report faithfully represents the pipeline's execution on the input dataset.

## Related tools

- **matchms** (metadata cleaning and library filtering pipeline that produces the processing report to be parsed and verified) — https://github.com/matchms/matchms
- **Python (pandas)** (tabular data parsing and numeric extraction from CSV/Excel processing reports)
- **RDKit** (structure comparison and validation (referenced for resolving SMILES/InChI/InChIKey conflicts in repair operations))

## Evaluation signals

- All required fields (input, removed, repaired, retained) are present in the parsed table with no null or missing values.
- Extracted numeric values are exact integers with no rounding errors or type coercion failures.
- Field-by-field comparison shows zero absolute difference between extracted and reference values (or difference within documented tolerance).
- Audit invariant: input count = removed + repaired + retained (or closely approximates it).
- Validation report is generated and human-readable, with each field's status (pass/fail) clearly annotated.

## Limitations

- The skill assumes the reference statistics in the article are correct; it does not validate the correctness of the pipeline itself, only fidelity to reported counts.
- It cannot detect wrong chemical annotations that are consistent with measured mass, as noted in the article's discussion—plausibility checks comparing metadata and measured fragments are not yet implemented.
- The skill does not validate per-spectrum metadata fields (e.g., ionmode, precursor m/z, adduct); it only aggregates counts at the table level.
- If the processing report uses non-standard column names or numeric formats (e.g., scientific notation, thousands separators), parsing may fail or require preprocessing.

## Evidence

- [abstract] input_spectra_count_validation: "Before cleaning, the GNPS library contained 500,569 spectra...The final cleaned GNPS public mass spectral library contains 448.485 curated mass spectra"
- [abstract] repair_and_removal_counts_validation: "In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084"
- [other] reproducibility_via_supplementary_table: "Examples of these YAML files can be found on Zenodo [5]"
- [abstract] pipeline_execution_on_gnps_library: "Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min"
