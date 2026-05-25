---
name: artifact-provenance-tracing-to-repository
description: Retrieve and validate processing artifacts (e.g., supplementary tables, cleaned spectral libraries, YAML configuration files) from public repositories (Zenodo, GitHub) to verify that reported statistics and processing parameters match the actual outputs claimed in a published article. This skill ensures reproducibility by grounding published findings in auditable, versioned artifacts.
when_to_use_negative:
- The article does not cite a public repository or makes no quantitative claims about pipeline outputs that can be verified against an artifact.
- The repository deposit is embargoed, access-restricted, or no longer available.
- The article describes only experimental raw data (e.g., mass spectra files) without reporting processing statistics that can be cross-checked against a summary table or report.
edam_operation: http://edamontology.org/operation_3895
edam_topics:
- http://edamontology.org/topic_0081
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: produces the cleaned spectral library and processing report artifacts deposited in the repository
  repo: https://github.com/matchms/matchms
- name: Zenodo
  role: public repository hosting the cleaned GNPS library, processing report (Supplementary Table S1), scripts, and YAML filter configuration used in the pipeline
  repo: https://zenodo.org/record/10160791
- name: Python
  role: language for parsing, validating, and comparing extracted artifact fields against reported values
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
    - outputs/article_878_full_2026-05-10_v5/skills/artifact-provenance-tracing-to-repository/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/artifact-provenance-tracing-to-repository/skill.md
    merged_at: '2026-05-25T07:15:30.865897+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/artifact-provenance-tracing-to-repository@sha256:0b5c44af72134f61a4460042cb7d55b9baca7165ec5d3ef9c6ecfc91553bb37f
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# artifact-provenance-tracing-to-repository

## Summary

Retrieve and validate processing artifacts (e.g., supplementary tables, cleaned spectral libraries, YAML configuration files) from public repositories (Zenodo, GitHub) to verify that reported statistics and processing parameters match the actual outputs claimed in a published article. This skill ensures reproducibility by grounding published findings in auditable, versioned artifacts.

## When to use

When a published article reports quantitative results of a data processing pipeline (e.g., 'removed 31,758 spectra, repaired 52,084, retained 448,485') and cites a public repository deposit, use this skill to retrieve the processing report or output artifact and cross-check numeric fields, metadata structure, and configuration details against the article's claims to verify the pipeline run was executed as described.

## When NOT to use

- The article does not cite a public repository or makes no quantitative claims about pipeline outputs that can be verified against an artifact.
- The repository deposit is embargoed, access-restricted, or no longer available.
- The article describes only experimental raw data (e.g., mass spectra files) without reporting processing statistics that can be cross-checked against a summary table or report.

## Inputs

- article text with repository citations and numeric claims
- repository accession identifier (DOI, GitHub URL, or Zenodo deposit ID)
- expected numeric or categorical field names from article methods/results

## Outputs

- parsed processing report or artifact (e.g., structured table, YAML config)
- field-by-field validation report (matching/mismatching values)
- boolean confirmation of reproducibility (all fields match or not)

## How to apply

First, identify the repository and accession number cited in the article (e.g., Zenodo DOI 10.5281/zenodo.10160791). Retrieve the processing report or supplementary artifact (e.g., Supplementary Table S1) from that repository. Parse the artifact using the appropriate parser (e.g., CSV/TSV for tabular data, YAML for configuration files, Python/matchms for serialized objects). Extract key numeric fields documented in the article—in this case, total input spectra count, number removed, number repaired, and number retained. Validate data types (numeric fields should be integers) and field presence against the expected schema. Compare extracted values row-by-row or field-by-field against the quantitative claims in the article text. Document discrepancies or confirmations in a structured validation report, flagging any mismatches that would indicate either a transcription error or a divergence between the reported and actual pipeline execution.

## Related tools

- **matchms** (produces the cleaned spectral library and processing report artifacts deposited in the repository) — https://github.com/matchms/matchms
- **Zenodo** (public repository hosting the cleaned GNPS library, processing report (Supplementary Table S1), scripts, and YAML filter configuration used in the pipeline) — https://zenodo.org/record/10160791
- **Python** (language for parsing, validating, and comparing extracted artifact fields against reported values)

## Evaluation signals

- All numeric fields in the parsed artifact (input count, removed count, repaired count, retained count) match the values reported in the article text within zero tolerance (e.g., 500,569 input spectra, 31,758 removed, 52,084 repaired, 448,485 retained).
- The artifact schema is complete and matches the expected fields documented in the article methods (e.g., 'total input spectra count', 'number of spectra removed', etc.).
- Data types are correct: numeric fields parse as integers, not strings or missing values.
- The repository deposit includes a YAML configuration file or supplementary table that lists all filters and parameters used, allowing independent verification that the settings match the pipeline description.
- No rows or fields in the artifact are truncated, corrupted, or redacted; the artifact is complete and machine-parseable.

## Limitations

- If the article reports only aggregate statistics without a detailed breakdown table, the artifact may not support granular field-level validation.
- Repositories may lack version pinning for tool versions (e.g., matchms 0.26.4) used to generate the artifact, making it difficult to reproduce the exact output if the tool is updated.
- The skill does not verify the correctness of the underlying pipeline logic or filter parameters—it only confirms that reported numbers match the stored artifact; wrong chemical annotations consistent with the measured mass will go unnoticed in the current pipeline.
- If the repository has since been updated or corrected, the artifact version retrieved may not match the version used during the original article's analysis, leading to apparent discrepancies that reflect post-publication fixes rather than original errors.

## Evidence

- [other] Processing report artifact and validation workflow: "The cleaned library, the scripts and YAML file with the filters and settings can be found on Zenodo [5]"
- [abstract] Quantitative claims to verify against artifact: "Before cleaning, the GNPS library contained 500,569 spectra. The final cleaned GNPS public mass spectral library contains 448.485 curated mass spectra"
- [abstract] Repair statistics enabling granular validation: "combined the newly introduced repair functions repaired the metadata of 52,084"
- [abstract] Processing time and scale context: "Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min"
- [discussion] Limitation: pipeline cannot catch semantically plausible but incorrect annotations: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline"
