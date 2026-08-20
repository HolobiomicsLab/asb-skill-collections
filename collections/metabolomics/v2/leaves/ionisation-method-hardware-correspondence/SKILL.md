---
name: ionisation-method-hardware-correspondence
description: Use when when evaluating whether a mass spectrometry analysis platform
  (such as mzmine) has comprehensive module support across multiple ionisation and
  separation techniques (LC, GC, IMS, MALDI MS imaging), or when planning a multi-technique
  MS study and needing to confirm that all intended.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mzmine
  techniques:
  - LC-MS
  - GC-MS
  - ion-mobility-MS
  license_tier: open
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

# ionisation-method-hardware-correspondence

## Summary

Verify that a mass spectrometry data processing software or workflow provides module coverage across all supported ionisation techniques (LC, GC, IMS, MS Imaging) and MS instrument types. This skill ensures completeness of the analytical pipeline by mapping each separation/ionisation method to its corresponding processing modules.

## When to use

When evaluating whether a mass spectrometry analysis platform (such as mzmine) has comprehensive module support across multiple ionisation and separation techniques (LC, GC, IMS, MALDI MS imaging), or when planning a multi-technique MS study and needing to confirm that all intended ionisation methods have corresponding processing infrastructure in the chosen software.

## When NOT to use

- Single-technique workflows where only one ionisation method (e.g., LC-MS only) is planned—the full multi-technique correspondence check adds overhead without benefit.
- When evaluating data processing steps already performed by upstream instruments or vendor software—this skill applies to comprehensive software platforms, not individual hardware-specific processors.

## Inputs

- Software repository codebase (source code structure)
- Module documentation or README files
- Declared hardware/instrument support list

## Outputs

- Module inventory list with categorisation by function
- Coverage matrix mapping ionisation types to modules
- Structured coverage verification report
- Module-to-technique correspondence documentation

## How to apply

Access the software repository (e.g., github.com/mzmine/mzmine) and retrieve the complete list of processing modules from codebase structure or documentation. Categorise each module by its primary function (import, preprocessing, alignment, identification, visualisation). Cross-reference module source code and documentation to identify which separation/ionisation types (LC, GC, IMS, MS Imaging) each module explicitly supports. Build a coverage matrix mapping separation/ionisation types to modules. Verify that every supported type (LC, GC, IMS, MS imaging) is covered by at least one module in the workflow. Document findings in a structured report showing the module inventory and coverage verification. The rationale is that complete coverage ensures users of all supported ionisation techniques can execute end-to-end analytical workflows without tool switching.

## Related tools

- **mzmine** (Target platform for module coverage assessment; provides the complete set of MS data analysis modules to be inventoried and cross-referenced against supported ionisation techniques) — https://github.com/mzmine/mzmine

## Evaluation signals

- Coverage matrix is complete: every declared ionisation type (LC, GC, IMS, MS imaging, MALDI) maps to at least one processing module in each major workflow stage (import, preprocessing, alignment, identification, visualisation).
- Module source code or documentation explicitly lists supported ionisation types as attributes or in method signatures.
- No gaps are present in the ionisation-technique-to-module mapping; if a technique is declared as supported by the software overall, all required processing functions are available for it.
- The structured report is reproducible: another evaluator using the same repository state and categorisation logic produces the same module inventory and coverage matrix.
- Cross-reference verification confirms that modules documented for a given ionisation type have been tested or used successfully with that technique (e.g., by examining test data, example workflows, or issue tracker references).

## Limitations

- Coverage matrix reflects only declared module support; modules may not be equally mature or well-tested across all ionisation types, and this skill does not assess algorithm quality or experimental validation.
- The skill requires access to current repository codebase or comprehensive documentation; changes to module structure or removal of undocumented modules may invalidate prior inventories.
- Module interdependencies and workflow composition are not explicitly verified—the skill checks that individual modules exist for each ionisation type but does not guarantee that modules can be combined into a coherent end-to-end workflow for all combinations of techniques.
- New ionisation technologies or instrument types emerging after the software snapshot may not be represented in the coverage matrix.

## Evidence

- [other] mzmine is designed with a complete set of modules covering the entire MS data analysis workflow and supports liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments.: "mzmine is designed with a complete set of modules covering the entire MS data analysis workflow and supports liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS"
- [other] Categorise each module by its primary function (e.g., import, preprocessing, alignment, identification, visualisation). Cross-reference module documentation or source code to identify which separation/ionisation types each module supports (LC, GC, IMS, MS Imaging). Build a coverage matrix mapping separation/ionisation types to modules.: "Categorise each module by its primary function (e.g., import, preprocessing, alignment, identification, visualisation). Cross-reference module documentation or source code to identify which"
- [intro] provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow: "provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow"
