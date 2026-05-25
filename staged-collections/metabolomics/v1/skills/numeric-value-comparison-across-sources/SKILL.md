---
name: numeric-value-comparison-across-sources
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to cross-validate reported summary statistics against structured data artifacts for verifying reproducibility and detecting transcription or calculation errors.
when_to_use_negative:
- The artifact does not exist or is inaccessible at the cited location (e.g., Zenodo link is dead or requires authentication).
- The article reports aggregate statistics without citing a specific artifact or supplementary table as the source (comparison cannot be grounded).
- The artifact field names or structure are ambiguous or not aligned with the article's reported metrics (e.g., article reports 'spectra removed' but artifact has only 'spectra filtered' without definition).
edam_operation: http://edamontology.org/operation_3436
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3372
tools:
- name: matchms
  role: pipeline execution and metadata cleaning that produces the summary statistics being validated
  repo: https://github.com/MassBank/matchms
- name: Python
  role: script language for parsing artifacts, extracting values, and performing numeric comparisons
- name: Zenodo
  role: repository host for supplementary tables, processing reports, and data artifacts cited in the article
  repo: https://zenodo.org/
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
    - outputs/article_878_full_2026-05-10_v5/skills/numeric-value-comparison-across-sources/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/numeric-value-comparison-across-sources/skill.md
    merged_at: '2026-05-25T07:04:57.434251+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/numeric-value-comparison-across-sources@sha256:1f3a1848e78f6b19da4811b27585c90e56be19717820178567625d6fa78c7a4a
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# numeric-value-comparison-across-sources

## Summary

Cross-validate reported summary statistics (e.g., input counts, removal counts, repair counts, retention counts) from a scientific article against structured data artifacts (e.g., processing reports, supplementary tables) to verify reproducibility and detect transcription or calculation errors.

## When to use

When an article reports aggregate numeric counts or statistics (e.g., 'X spectra removed, Y spectra repaired, Z spectra retained from W input spectra') and you have access to a structured artifact (processing report, supplementary table, or data release on Zenodo) that should contain the underlying values, use this skill to validate field-by-field agreement and document any discrepancies.

## When NOT to use

- The artifact does not exist or is inaccessible at the cited location (e.g., Zenodo link is dead or requires authentication).
- The article reports aggregate statistics without citing a specific artifact or supplementary table as the source (comparison cannot be grounded).
- The artifact field names or structure are ambiguous or not aligned with the article's reported metrics (e.g., article reports 'spectra removed' but artifact has only 'spectra filtered' without definition).

## Inputs

- article text containing reported summary statistics (counts, percentages, or aggregate measures)
- structured artifact or supplementary table in tabular format (CSV, TSV, Excel, JSON, or YAML)
- repository metadata or DOI pointing to the data release location

## Outputs

- structured validation report listing field names, article-reported values, artifact values, match/mismatch status, and absolute/relative differences
- summary statement confirming reproducibility or flagging unresolved discrepancies

## How to apply

Retrieve the artifact (e.g., Supplementary Table S1 or processing report) from the cited repository (e.g., Zenodo DOI 10.5281/zenodo.10160791). Parse the table or report to extract the key numeric fields (e.g., total input spectra, spectra removed, spectra repaired, spectra retained). Validate that the extracted fields are numeric and non-null. Compare each extracted value against the corresponding article-reported value using exact equality. Document the comparison results in a structured validation report, noting which fields match, which diverge, and by how much (absolute and relative difference). The skill is correctly applied when all reported values match the artifact values within expected precision, or when divergences are explained by documented post-processing or filtering steps not captured in the artifact timestamp.

## Related tools

- **matchms** (pipeline execution and metadata cleaning that produces the summary statistics being validated) — https://github.com/MassBank/matchms
- **Python** (script language for parsing artifacts, extracting values, and performing numeric comparisons)
- **Zenodo** (repository host for supplementary tables, processing reports, and data artifacts cited in the article) — https://zenodo.org/

## Evaluation signals

- All article-reported numeric values (input spectra count, spectra removed, spectra repaired, spectra retained) match the corresponding values in the artifact to exact precision (0% relative difference).
- Field presence and data type validation: all expected numeric fields are present in the artifact and are numeric (not null, not text).
- Sum consistency check: 'spectra removed' + 'spectra repaired' + 'spectra retained' equals or is reconcilable with 'input spectra' (or a documented intermediate count).
- Percentage-based findings (e.g., '27.6% of spectra could not be derived') can be recomputed from the artifact counts and match the article values within rounding tolerance (±0.1%).
- No unexplained divergences beyond rounding error (< 1 count difference on counts > 100) or documented post-processing steps not reflected in the artifact timestamp.

## Limitations

- Artifacts may be versioned or post-processed after article publication; timestamp metadata on the artifact release is essential to confirm it reflects the same pipeline run reported in the article.
- Percentage or ratio calculations in the article may round differently than reconstruction from raw counts; agreement must allow for expected rounding tolerance.
- Some fields (e.g., 'spectra repaired') may be derived indirectly from other counts (e.g., 'removed without repair' vs. 'removed after repair'), requiring careful field mapping to avoid false negatives.
- Zenodo or supplementary repositories may have rate limits, access restrictions, or removal; validation depends on artifact availability at the time of check.

## Evidence

- [abstract] article_reported_counts: "Before cleaning, the GNPS library contained 500,569 spectra...The final cleaned GNPS public mass spectral library contains 448.485 curated mass spectra"
- [abstract] repair_function_impact: "a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084"
- [abstract] artifact_location: "Examples of these YAML files can be found on Zenodo [5]"
- [abstract] pipeline_execution_context: "Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min"
