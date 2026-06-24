---
name: separation-technique-workflow-alignment
description: Use when when evaluating whether an MS data processing platform (such
  as mzmine) supports the full range of separation/ionization techniques your laboratory
  uses, or when assessing whether gaps exist in the software architecture that would
  require external pre- or post-processing for specific.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mzmine
  techniques:
  - LC-MS
  - GC-MS
  - ion-mobility-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# separation-technique-workflow-alignment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A systematic approach to verify that MS data analysis software provides complete module coverage across all supported separation and ionization techniques (LC, GC, IMS, MS imaging). This skill ensures that every instrument type or data acquisition modality has at least one corresponding processing module in the workflow pipeline.

## When to use

When evaluating whether an MS data processing platform (such as mzmine) supports the full range of separation/ionization techniques your laboratory uses, or when assessing whether gaps exist in the software architecture that would require external pre- or post-processing for specific instrument types.

## When NOT to use

- When the software vendor has not made source code or module documentation publicly available (use vendor contact instead).
- When you are evaluating only a single instrument type or separation technique (use single-technique validation instead).
- When the goal is to optimize performance or parameters for a specific technique rather than assess architectural completeness.

## Inputs

- mzmine repository codebase or source code
- module documentation or API reference
- list of supported MS instruments and separation techniques

## Outputs

- module inventory catalog (categorized by function)
- separation-technique-to-module coverage matrix
- coverage verification report
- gap analysis (if any separation technique lacks module support)

## How to apply

Access the software repository and retrieve the complete list of processing modules from the codebase structure or documentation. Categorize each module by its primary function (import, preprocessing, alignment, identification, visualization). Cross-reference module documentation or source code to identify which separation/ionization types each module explicitly supports (LC, GC, IMS, MS imaging). Build a coverage matrix mapping separation/ionization types to modules. Verify that every supported type (LC, GC, IMS, MS imaging) is covered by at least one module in the workflow. Document the module inventory and coverage verification in a structured report to surface any gaps or incomplete pathways.

## Related tools

- **mzmine** (primary MS data processing platform whose module coverage and separation-technique support is being verified) — https://github.com/mzmine/mzmine

## Evaluation signals

- Coverage matrix is complete: every supported separation technique (LC, GC, IMS, MS imaging) has at least one module mapped to it.
- Module functions are categorized consistently (import, preprocessing, alignment, identification, visualization).
- Cross-reference between module documentation and technique support is bidirectional (each technique appears in module docs; each module references its supported techniques).
- No required workflow step is orphaned (e.g., no technique lacks import, preprocessing, or visualization modules).
- Gap report explicitly lists any technique-module pairs that are absent or under-supported, with justification.

## Limitations

- Coverage matrix reflects only modules explicitly documented; undocumented or implicit support for a technique may be missed.
- Different module versions may have varying technique support; verification should target a specific stable release or development snapshot.
- Some modules may support a technique but with reduced functionality or performance; binary coverage does not measure quality or completeness of support.

## Evidence

- [other] The research question: 'What is the complete set of processing modules provided by mzmine, and does each supported separation/ionisation technique (LC, GC, IMS, MS imaging) have at least one corresponding module in the software architecture?': "What is the complete set of processing modules provided by mzmine, and does each supported separation/ionisation technique (LC, GC, IMS, MS imaging) have at least one corresponding module in the"
- [other] The workflow steps describing the method.: "1. Access the mzmine repository (github.com/mzmine/mzmine) and retrieve the complete list of processing modules from the codebase structure or documentation. 2. Categorise each module by its primary"
- [other] The finding that mzmine provides complete module coverage.: "mzmine is designed with a complete set of modules covering the entire MS data analysis workflow and supports liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS"
- [readme] README confirmation of broad technique support.: "provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow. Support includes liquid chromatography (LC), gas"
