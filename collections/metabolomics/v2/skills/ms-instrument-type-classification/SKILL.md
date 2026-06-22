---
name: ms-instrument-type-classification
description: Use when when evaluating or designing a mass spectrometry data analysis platform, and you need to verify that every supported separation/ionisation technique (LC, GC, IMS, MS Imaging) is covered by at least one processing module.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - mzmine
  techniques:
  - LC-MS
  - GC-MS
  - ion-mobility-MS
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

# MS Instrument Type Classification

## Summary

Classify mass spectrometry data and workflows by their input separation/ionisation techniques (LC, GC, IMS, MS Imaging) to verify comprehensive software support across all major MS instrument types. This skill ensures that data processing pipelines can handle the full diversity of modern MS workflows.

## When to use

When evaluating or designing a mass spectrometry data analysis platform, and you need to verify that every supported separation/ionisation technique (LC, GC, IMS, MS Imaging) is covered by at least one processing module. Apply this skill when assessing software completeness or when documenting which instrument types a processing pipeline can handle.

## When NOT to use

- When analyzing individual data files or raw spectra—this skill operates at the software architecture level, not on experimental data.
- When you are only concerned with a single separation technique (e.g., LC-MS only) and do not need to assess multi-technique coverage.

## Inputs

- Software repository codebase (GitHub/git URL)
- Module source code and documentation
- Module inventory or architecture documentation

## Outputs

- Module coverage matrix (separation/ionisation type × module)
- Classification report mapping each instrument type to supporting modules
- Completeness verification report

## How to apply

First, access the software repository (e.g., mzmine on GitHub) and extract the complete inventory of processing modules from the codebase structure or module documentation. Next, categorize each module by its primary function (import, preprocessing, alignment, identification, visualization). Then, cross-reference module source code or documentation to identify which separation/ionisation types each module supports—LC (liquid chromatography), GC (gas chromatography), IMS (ion mobility spectrometry), or MS Imaging (e.g., MALDI). Build a coverage matrix mapping separation/ionisation types to modules. Finally, verify that every declared supported type has at least one corresponding module in the workflow architecture, and document the findings in a structured coverage report.

## Related tools

- **mzmine** (Open-source software platform for MS data processing; serves as the target of instrument type classification and the source of module inventory) — https://github.com/mzmine/mzmine

## Evaluation signals

- Coverage matrix is complete: every declared supported technique (LC, GC, IMS, MS Imaging) appears in the matrix with at least one assigned module
- Module-to-technique mappings are verifiable by consulting source code or official documentation (no inferences or guesses)
- Inventory of modules is exhaustive: all processing modules in the codebase are categorized and classified
- Report documents which techniques are supported by which specific module names and versions
- No gaps exist: if a technique is advertised in the software's feature list or README, it must have at least one supporting module in the coverage matrix

## Limitations

- Module support may vary by software version; changelog or release notes may be absent or incomplete, making it difficult to track when support was added or removed.
- Some modules may support multiple techniques but documentation may not be explicit, requiring manual inspection of source code to determine true coverage.
- MS Imaging support (e.g., MALDI) may be less mature or feature-complete than LC/GC support; this skill verifies presence, not feature parity or depth.

## Evidence

- [results] mzmine is designed with a complete set of modules covering the entire MS data analysis workflow and supports liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments.: "Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments"
- [methods] Categorize each module by its primary function and cross-reference documentation to identify which separation/ionisation types each module supports.: "Categorise each module by its primary function (e.g., import, preprocessing, alignment, identification, visualisation). Cross-reference module documentation or source code to identify which"
- [readme] mzmine is described as providing a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow.: "provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow"
