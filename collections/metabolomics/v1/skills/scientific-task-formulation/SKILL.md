---
name: scientific-task-formulation
description: Use when you are starting a new mass spectrometry analysis task or feature request where the problem scope is unclear, the tool chain (e.g., OpenMS + Python + KNIME integration) is not yet selected, or acceptance criteria (code quality, test coverage, documentation) have not been established.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3572
  tools:
  - OpenMS
  - KNIME
  - Python
  - GitHub
  - TOPPTools
  - pyOpenMS
  - TOPPView
  - GNPS (Global Natural Products Social Molecular Networking)
  - ISDB-LOTUS
  - Sirius 6
  - MatchMS
  - MZmine
  - MZmine 2
  - mzmine2
  - mzmine (current)
  - npanalyst
  - forward_train.py
  - forward_evaluate_pipeline.py
  - analysis_pipeline.py
  - Conda / Mamba
  - SIRIUS
  - CSI:FingerID
  - CANOPUS
  - MSNovelist
  - ZODIAC
derived_from:
- doi: 10.1074/mcp.M113.031278
  title: featurefindermetab
- doi: 10.1289/EHP7722
  title: ''
- doi: 10.1002/cmtd.202400088
  title: ''
- doi: 10.1186/1471-2105-11-395
  title: ''
- doi: 10.1021/acscentsci.1c01108
  title: ''
- doi: 10.1021/acs.analchem.2c02093
  title: ''
- doi: 10.1021/acs.analchem.5c03730
  title: ''
- doi: 10.1038/s41592-019-0344-8
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_13c_spacem
    doi: 10.1038/s42255-024-01118-4
    title: 13C-SpaceM
  - build: coll_bindiscover
    doi: 10.1186/s13321-023-00734-8
    title: bindiscover
  - build: coll_featurefindermetab
    doi: 10.1074/mcp.M113.031278
    title: featurefindermetab
  - build: coll_hexpmetdb
    doi: 10.1289/EHP7722
    title: HExpMetDB
  - build: coll_ms2decide
    doi: 10.1002/cmtd.202400088
    title: ms2decide
  - build: coll_mzmine2
    doi: 10.1186/1471-2105-11-395
    title: mzmine2
  - build: coll_np_analyst
    doi: 10.1021/acscentsci.1c01108
    title: NP Analyst
  - build: coll_rassp
    doi: 10.1021/acs.analchem.2c02093
    title: rassp
  - build: coll_rtmsecho
    doi: 10.1021/acs.analchem.5c03730
    title: rtmsecho
  - build: coll_sirius
    doi: 10.1038/s41592-019-0344-8
    title: sirius
  dedup_kept_from: coll_featurefindermetab
schema_version: 0.2.0
---

# scientific_task_formulation

## Summary

Formulate a well-scoped research question and methodological workflow for mass spectrometry data analysis by defining clear objectives, selecting appropriate tools (e.g., OpenMS, KNIME), and establishing acceptance criteria (unit tests, functional tests, documentation) before implementation.

## When to use

You are starting a new mass spectrometry analysis task or feature request where the problem scope is unclear, the tool chain (e.g., OpenMS + Python + KNIME integration) is not yet selected, or acceptance criteria (code quality, test coverage, documentation) have not been established. Particularly relevant when contributing new analysis algorithms or workflows to a large scientific software project.

## When NOT to use

- The task scope is already fully defined and validated (e.g., existing algorithm with clear parameters and test suite)
- You are implementing a routine analysis on data with a known, proven workflow (no novel methodology formulation needed)
- The input data or output expectations are so ambiguous that formulation itself cannot proceed without external domain expertise or stakeholder input

## Inputs

- Research question or analysis objective (text)
- Input data format specification (e.g., mzML, mzXML, mzIdentXML)
- Available computational resources and target platforms (Windows/macOS/Linux)

## Outputs

- Formulated task specification document
- Selected tool and library components (OpenMS, Python, KNIME, etc.)
- Workflow step sequence (ordered list)
- Acceptance criteria checklist (unit tests, functional tests, documentation, coding conventions, Python bindings if applicable)

## How to apply

Begin by formulating a clear research question aligned with your scientific objective (e.g., 'quantify peptides using label-free or SILAC protocols'). Identify the required input data formats (mzML, mzXML, mzIdentXML, etc.) and desired output (quantitation tables, identifications). Select tool components from the OpenMS ecosystem (C++ library, TOPPTools, pyOpenMS Python bindings, KNIME nodes) that cover your workflow. Document the required workflow steps (e.g., spectrum preprocessing, peptide identification, quantitation) and establish acceptance criteria: unit tests and functional tests for correctness, Python bindings if algorithm exposure is needed, and proper documentation (inline code comments, method descriptions). Before opening a pull request, verify adherence to coding conventions and completion of all test and documentation requirements.

## Related tools

- **OpenMS** (Core C++ library providing LC-MS data management, analysis algorithms, and infrastructure for rapid tool development) — https://github.com/OpenMS/OpenMS
- **TOPPTools** (Pre-built ready-to-use analysis tools for proteomics and metabolomics data processing and mining) — https://github.com/OpenMS/OpenMS
- **pyOpenMS** (Python bindings to OpenMS C++ API enabling rapid algorithm development and integration into Python workflows) — https://github.com/OpenMS/OpenMS
- **KNIME** (Workflow engine for integrating and orchestrating OpenMS TOPPTools and analyses)
- **TOPPView** (1D, 2D, and 3D visualization tool for LC-MS data exploration and validation) — https://github.com/OpenMS/OpenMS

## Evaluation signals

- Research question is explicit, measurable, and aligned with supported MS workflows (label-free, SILAC, iTRAQ, TMT, SRM, SWATH, DIA, or targeted protocols)
- Input/output data formats are specified and supported by OpenMS (mzML, mzXML, mzIdentXML, pepXML, mzTab, etc.)
- All workflow steps are documented, each with a designated tool component (OpenMS C++, TOPPTool, pyOpenMS, or KNIME node)
- Acceptance criteria include passing unit tests, functional tests, and adherence to OpenMS coding conventions; Python bindings are documented if algorithm exposure is needed
- Task specification can be traced to a corresponding issue or pull request in https://github.com/OpenMS/OpenMS with evidence of maintainer assignment and severity classification

## Limitations

- The formulation process relies on internal OpenMS maintainer expertise to assign severity and assess blockers; no automated heuristic was detected to validate finding strength in the provided source materials
- No changelog or version compatibility constraints were mentioned in the source material, so long-term maintenance and backward-compatibility implications must be clarified separately
- Task formulation in OpenMS assumes familiarity with mass spectrometry concepts, file formats (mzML, mzXML, etc.), and quantitation protocols; domain expertise is not generated by this skill

## Evidence

- [methods] Before you open the pull request, make sure you adhere to our coding conventions and have unit tests and functional tests as well as proper documentation and Python bindings: "Before you open the pull request, make sure you adhere to [our coding conventions] and have [unit tests and functional tests] as well as [proper documentation] and have Python bindings — nanobind"
- [readme] OpenMS is an open-source software C++ library for LC-MS data management and analyses offering infrastructure for rapid tool development: "OpenMS is an open-source software C++ library for LC-MS data management and analyses. It offers an infrastructure for rapid development of mass spectrometry-related software."
- [readme] OpenMS offers analyses for various quantitation protocols including label-free, SILAC, iTRAQ, TMT, SRM, SWATH: "OpenMS offers analyses for various quantitation protocols, including label-free quantitation, SILAC, iTRAQ, TMT, SRM, SWATH, etc."
- [readme] OpenMS supports easy integration into workflow engines like KNIME via the TOPPTools concept and unified parameter handling: "It supports easy integration of OpenMS built tools into workflow engines like nextflow, KNIME, Galaxy, and TOPPAS via the TOPPTools concept and a unified parameter handling via a 'common tool"
- [other] The severity is usually assigned by OpenMS maintainers and used internally to indicate if a bug is a blocker for a new release: "The severity is usually assigned by OpenMS maintainers and used internally to e.g. indicate if a bug is a blocker for a new release."
