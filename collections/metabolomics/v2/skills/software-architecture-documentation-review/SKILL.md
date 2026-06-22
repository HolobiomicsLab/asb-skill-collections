---
name: software-architecture-documentation-review
description: Use when you need to verify the scope and completeness of a software platform's analytical capabilities—particularly when the project claims to support multiple input modalities (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  tools:
  - mzmine
derived_from:
- doi: 10.1038/s41587-023-01690-2
  title: mzmine3
evidence_spans:
- mzmine is an open-source software for mass spectrometry data processing
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzmine3
    doi: 10.1038/s41587-023-01690-2
    title: mzmine3
  dedup_kept_from: coll_mzmine3
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-023-01690-2
  all_source_dois:
  - 10.1038/s41587-023-01690-2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# software-architecture-documentation-review

## Summary

A systematic method to audit the completeness and coverage of a software project's processing modules across supported data types by cross-referencing source code structure, documentation, and module categorization against defined analysis workflows. This skill verifies that every claimed capability (e.g., LC, GC, IMS, MS imaging support) is backed by at least one concrete implementation module.

## When to use

Apply this skill when you need to verify the scope and completeness of a software platform's analytical capabilities—particularly when the project claims to support multiple input modalities (e.g., different chromatography techniques, ionization methods, or imaging modes) and you need to confirm that each claimed support has a corresponding processing module in the actual codebase. Typical triggers include: (1) evaluating software fitness for a multi-technique workflow; (2) documenting module inventory for reproducibility; (3) identifying gaps in coverage before adopting a tool for production use.

## When NOT to use

- Do not use this skill to evaluate the correctness or performance of individual modules—it verifies existence and categorization, not algorithm correctness or output quality.
- Do not use this skill to validate parameter defaults or optimization settings within modules; the skill focuses on coverage of workflow categories, not tuning.
- Do not use this skill as a substitute for reading method papers or validation benchmarks; a module's existence does not guarantee it is scientifically sound or suitable for your specific data.

## Inputs

- GitHub repository codebase (source structure and module listing)
- Project README or technical documentation claiming technique support (LC, GC, IMS, MS imaging, etc.)
- Module-level documentation (docstrings, README.md files in module directories, or wiki pages)

## Outputs

- Coverage matrix: (support claim × module) cross-reference table
- Module inventory: structured list of all processing modules with categorized functions
- Gap analysis report: documented presence or absence of each claimed capability
- Verification summary: boolean assertion that every claimed technique has ≥1 corresponding module

## How to apply

Begin by retrieving the complete list of processing modules from the official repository (e.g., GitHub codebase structure or technical documentation). Categorize each module by its primary function in the MS data analysis workflow (import, preprocessing, alignment, identification, visualization). Next, inspect module documentation or source code to identify which separation/ionization types each module explicitly supports (LC, GC, IMS, MS Imaging). Construct a coverage matrix mapping the claimed technique support (rows) against available modules (columns). For each supported technique listed in the project's README or publication abstract, verify that at least one module in the matrix explicitly claims support for that technique. Document discrepancies or gaps in a structured report; gaps indicate either incomplete documentation, unstable features, or scope misalignment and should prompt clarification with maintainers or investigation of related issues/PRs.

## Related tools

- **mzmine** (Subject of architecture review; provides modular MS data processing pipeline with claimed support for LC, GC, IMS, and MS imaging) — https://github.com/mzmine/mzmine

## Evaluation signals

- Coverage matrix is complete: every row (claimed technique) has at least one non-empty column (supporting module).
- All modules retrieved from the codebase are categorized and assigned to at least one workflow function (import, preprocessing, alignment, identification, visualization, etc.).
- Gap analysis report shows 0 uncovered claimed techniques when cross-referencing the README's 'Support includes …' statement against the module inventory.
- Module evidence is traced to source code or official documentation (e.g., module README, Javadoc/docstring, GitHub issue/PR) rather than inferred.
- The structured report is reproducible: a third party following the same steps on the same repository commit produces an identical module list and coverage matrix.

## Limitations

- Coverage verification is blind to module maturity, stability, or scientific validation; a module may be listed but undocumented, deprecated, or experimental.
- Discrepancies between claimed support (README) and actual implementation (source code) may exist; the skill detects these gaps but does not explain their cause (e.g., unfinished feature, documentation rot).
- Module documentation may be sparse or missing; absence of explicit evidence does not prove absence of support—manual code inspection may be required for conclusive verification.
- The skill does not evaluate whether a module works correctly on real-world data; it only confirms the existence of a processing pathway.

## Evidence

- [readme] mzmine is an open-source software for mass spectrometry data processing. The goals of the project is to provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow.: "provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow"
- [readme] Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments.: "Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments"
- [other] task_001 research question: What is the complete set of processing modules provided by mzmine, and does each supported separation/ionisation technique (LC, GC, IMS, MS imaging) have at least one corresponding module in the software architecture?: "What is the complete set of processing modules provided by mzmine, and does each supported separation/ionisation technique (LC, GC, IMS, MS imaging) have at least one corresponding module in the"
- [other] Categorise each module by its primary function (e.g., import, preprocessing, alignment, identification, visualisation). Cross-reference module documentation or source code to identify which separation/ionisation types each module supports (LC, GC, IMS, MS Imaging). Build a coverage matrix mapping separation/ionisation types to modules.: "Categorise each module by its primary function (e.g., import, preprocessing, alignment, identification, visualisation). Cross-reference module documentation or source code to identify which"
