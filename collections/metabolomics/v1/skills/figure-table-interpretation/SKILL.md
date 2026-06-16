---
name: figure-table-interpretation
description: Use when you need to verify claims about algorithm performance, data processing correctness, or workflow outcomes in a scientific article or software repository. Use it when source documents contain figures, tables, or visualization badges (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3575
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - OpenMS
  - KNIME
  - Python
  - GitHub
  - pyOpenMS
  - nextflow
  - Galaxy
  - TOPPAS
  - MZmine 2
  - mzmine2
  - MZmine
  - mzmine (current)
  - SIRIUS
  - CSI:FingerID
  - CANOPUS
  - MSNovelist
  - ZODIAC
derived_from:
- doi: 10.1074/mcp.M113.031278
  title: featurefindermetab
- doi: 10.1186/1471-2105-11-395
  title: ''
- doi: 10.1038/s41592-019-0344-8
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bindiscover
    doi: 10.1186/s13321-023-00734-8
    title: bindiscover
  - build: coll_featurefindermetab
    doi: 10.1074/mcp.M113.031278
    title: featurefindermetab
  - build: coll_mzmine2
    doi: 10.1186/1471-2105-11-395
    title: mzmine2
  - build: coll_sirius
    doi: 10.1038/s41592-019-0344-8
    title: sirius
  dedup_kept_from: coll_featurefindermetab
schema_version: 0.2.0
---

# figure_table_interpretation

## Summary

Systematically extract, validate, and synthesize quantitative findings from figures and tables in scientific literature and repository documentation to assess data quality, workflow correctness, and algorithmic performance. This skill supports reproducibility assessment and method validation in mass spectrometry and bioinformatics pipelines.

## When to use

Apply this skill when you need to verify claims about algorithm performance, data processing correctness, or workflow outcomes in a scientific article or software repository. Use it when source documents contain figures, tables, or visualization badges (e.g., analytics plots, test results, quantitative metrics) that encode evidence about tool behavior, coverage, or robustness across platforms and data types.

## When NOT to use

- Input contains only narrative description with no quantitative tables, figures, or metrics to extract
- Task requires inferring numerical values not explicitly stated in any figure, table, or badge
- Source material is a software announcement or marketing document without empirical performance data

## Inputs

- scientific article text with embedded figures and tables
- repository README and documentation files
- build/test status badges and analytics widgets
- version compatibility matrices
- quantitative performance metrics (e.g., accuracy, sensitivity, specificity ranges)

## Outputs

- extracted quantitative findings with source attribution
- inventory of supported input formats, platforms, and versions
- list of missing signals or undocumented gaps
- assessment of consistency between narrative claims and tabular evidence
- validation report indicating correctness and applicability of methods

## How to apply

First, identify all tabular or visual evidence in the article and README (e.g., performance tables, analytics badges, build/test status widgets, version compatibility matrices). Extract numeric values, categorical outcomes, and metric ranges (e.g., platform support, test coverage). Cross-reference claims made in narrative sections (methods, results, discussion) against these extracted values to detect consistency or gaps. For missing signals (e.g., no changelog found, no strong finding sentence detected heuristically), document the absence and its implications for reproducibility. Use the extracted data to construct a complete picture of workflow applicability: identify which input formats (mzML, mzXML, etc.), platforms (Windows, macOS, Linux), and tool versions are supported, and which edge cases or severity levels are documented (e.g., 'severity is usually assigned by maintainers and used internally to indicate if a bug is a blocker for a new release'). Report findings that align with or contradict stated capabilities.

## Related tools

- **OpenMS** (reference LC-MS data management and analysis platform; provides TOPP tools, visualization (TOPPView), quantification workflows (label-free, SILAC, iTRAQ, TMT, SRM, SWATH), de novo and database search, and adapter integration for workflow engines) — https://github.com/OpenMS/OpenMS
- **pyOpenMS** (Python bindings to OpenMS C++ API for rapid algorithm development and integration with Python-based workflows)
- **KNIME** (workflow integration engine supporting OpenMS TOPP tools via CTD (common tool description) parameter scheme)
- **nextflow** (workflow engine supporting integration of OpenMS TOPPTools)
- **Galaxy** (workflow engine supporting integration of OpenMS TOPPTools)
- **TOPPAS** (OpenMS-native workflow engine for TOPPTools composition and execution)

## Evaluation signals

- Extracted quantitative metrics (e.g., number of TOPP tools, platform support counts) match or contradict stated feature claims in narrative sections
- All supported input formats (mzML, mzXML, mzIdentXML, pepXML, mzTab) and output formats are enumerated and traceable to method or documentation sections
- Missing signals (e.g., absent changelog, no heuristically detected strong finding) are explicitly flagged with rationale for why absence matters
- Cross-platform support (Windows 10/11, macOS, Linux) is verified via build badges or explicit version/compatibility tables
- Quantification protocol coverage (label-free, SILAC, iTRAQ, TMT, SRM, SWATH) is confirmed against tool inventory or workflow examples

## Limitations

- Heuristic finding detection may fail to identify strong claims in non-standard narrative formats; manual review required for edge cases
- Analytics badges and status widgets may be outdated if they reference static snapshots; check timestamps or git history for recency
- Severity assignments and internal prioritization schemes (e.g., 'blocker' status for bug fixes) may not be documented in public repositories, limiting reproducibility assessment
- Missing signals (e.g., no changelog) indicate documentation gaps but do not prove absence of underlying functionality; requires inspection of git history or issue tracker

## Evidence

- [other] No changelog found: "_No changelog found._"
- [other] Finding confidence is determined by expert review: "The finding should be confirmed by expert review; no strong finding sentence was detected heuristically."
- [other] Severity classification is internal to OpenMS maintainers: "The severity is usually assigned by OpenMS maintainers and used internally to e.g. indicate if a bug is a blocker for a new release."
- [readme] Core C++ library and Python bindings; support for standard MS formats: "Core C++ library under three-clause BSD licence using modern C++23
Python bindings to the C++ API through pyOpenMS
Major community file formats supported (mzML, mzXML, mzIdentXML, pepXML, mzTab, etc.)"
- [readme] OpenMS supports diverse quantification protocols and workflow engines: "OpenMS offers analyses for various quantitation protocols, including label-free quantitation, SILAC, iTRAQ, TMT, SRM, SWATH, etc.
It supports easy integration of OpenMS built tools into workflow"
- [readme] Cross-platform availability: "Support for all major platforms (Windows [10, 11], macOS and Linux)"
- [readme] TOPP tool inventory and analysis scope: "Over 150+ individual analysis tools (TOPP Tools), covering most MS and LC-MS data processing and mining tasks"
