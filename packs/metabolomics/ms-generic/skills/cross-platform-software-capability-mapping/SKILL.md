---
name: cross-platform-software-capability-mapping
description: Use when you are designing a new tool for FT-ICR MS analysis (or similar high-resolution mass spectrometry domain) and need to understand which analytical and visualization features are already implemented in competing or complementary tools (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - MetaboDirect
  - UltraMassExplorer
  - FREDA
  - MetaboAnalyst
  - DropMS
  - i-van Krevelen
  - vegan
  - SYNCSA
  - pmartR
  - KEGGREST
  - py4cytoscape
  - UltraMassExplorer (UME)
  - CoreMS
  - vegan (R package)
  - SYNCSA (R package)
  - pmartR (R package)
  - py4cytoscape (Python module)
  - KEGGREST (R package)
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)
- web-based applications such as UltraMassExplorer (UME)
- web-based applications such as UltraMassExplorer (UME) [27], FREDA [28]
- web-based applications such as UltraMassExplorer (UME) [27], FREDA [28], MetaboAnalyst [29]
- web-based applications such as UltraMassExplorer (UME) [27], FREDA [28], MetaboAnalyst [29], and DropMS [30]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Cross-Platform Software Capability Mapping

## Summary

Systematically catalog and compare analytical features across multiple software tools designed for a shared analytical domain (e.g., FT-ICR MS data analysis) to identify capability gaps, redundancies, and unique strengths. This skill produces a structured feature-comparison matrix that guides tool selection and highlights innovation opportunities.

## When to use

You are designing a new tool for FT-ICR MS analysis (or similar high-resolution mass spectrometry domain) and need to understand which analytical and visualization features are already implemented in competing or complementary tools (e.g., MetaboAnalyst, UltraMassExplorer, FREDA, DropMS, i-van Krevelen, CoreMS, Formularity) to position your tool's unique capabilities and avoid redundant implementation.

## When NOT to use

- You are performing a one-time analysis on a single tool and do not need to benchmark against competitors.
- The analytical domain is highly specialized with only one or two tools available; comparison provides limited insight.
- You lack access to tool source code or documentation; feature inference becomes unreliable without code inspection.

## Inputs

- Published articles and methods sections describing each comparison tool
- GitHub repository README files and source code structure
- Dependency declarations (R package imports, Python requirements.txt or setup.py)
- Official tool documentation and supplementary tables
- Repository function signatures and command-line argument definitions

## Outputs

- Structured feature-comparison table (rows: tools; columns: analytical features) with binary or categorical entries
- Capability gap analysis identifying features missing from the new tool
- Unique feature inventory highlighting differentiation opportunities
- Implementation roadmap informed by feature priority and domain relevance

## How to apply

First, identify the target analytical domain and the candidate comparison tools from published literature and repository registries. For each tool, extract its feature set by consulting (1) published documentation and methods sections, (2) GitHub repository README and source code structure (especially function signatures and command-line arguments), and (3) dependency declarations (e.g., R libraries like vegan, SYNCSA, pmartR; Python modules like py4cytoscape) which often indicate feature implementation. Organize features into logically grouped columns such as data filtering (m/z range, isotopic presence, formula error threshold), normalization methods (max, minmax, mean, median, total sum, z-score), statistical tests (PERMANOVA, NMDS, PCA), derived indices (NOSC, GFE, AImod, DBE, chemodiversity metrics: Shannon, Gini-Simpson, Chao1, Rao's), and visualization types (Van Krevelen diagrams, molecular composition plots, transformation networks). Build a binary or feature-level comparison table with tools as rows and features as columns. Cross-reference implementation details by inspecting actual source code for dependency usage (e.g., confirm vegan is used for PERMANOVA if claimed). Document any tools that lack certain capabilities to highlight niches for new tool development.

## Related tools

- **MetaboDirect** (Reference tool being positioned; implements Van Krevelen diagrams, PERMANOVA, NMDS, PCA, chemodiversity analysis, and transformation networks for FT-ICR MS) — https://github.com/Coayala/MetaboDirect
- **MetaboAnalyst** (Comparison tool for feature capability assessment)
- **UltraMassExplorer (UME)** (Comparison tool (web-based) for feature capability assessment)
- **FREDA** (Comparison tool (web-based) for feature capability assessment)
- **DropMS** (Comparison tool (web-based) for feature capability assessment)
- **i-van Krevelen** (Comparison tool (visualization-focused) for feature capability assessment)
- **CoreMS** (Comparison tool providing comprehensive software framework for FT-ICR MS)
- **vegan (R package)** (Dependency indicator for PERMANOVA and NMDS ordination implementation)
- **SYNCSA (R package)** (Dependency indicator for phylogenetic-community analysis features)
- **pmartR (R package)** (Dependency indicator for normalization method implementation)
- **py4cytoscape (Python module)** (Dependency indicator for transformation network visualization via Cytoscape)
- **KEGGREST (R package)** (Dependency indicator for KEGG database integration and pathway mapping)

## Evaluation signals

- Feature-comparison table is complete and consistent: every tool-feature cell is populated (✔/✖ or category); rows represent all identified tools; columns represent all identified features in the domain.
- Source verification: each claimed feature is traceable to published documentation, README, or source code inspection; dependency declarations match claimed features (e.g., if PERMANOVA is claimed, vegan or equivalent dependency appears in package imports).
- Coverage of feature groups: the table includes at least the following logical columns relevant to FT-ICR MS analysis: data filtering (m/z, isotopic, formula error, sample presence), peak normalization methods, compound class assignment, statistical tests (PERMANOVA, NMDS, PCA), chemodiversity indices (Shannon, Gini-Simpson, Chao1, Rao's), thermodynamic indices (NOSC, GFE, AImod, DBE), and visualization types (Van Krevelen, molecular composition, transformation networks).
- Gap identification is actionable: comparison reveals at least one feature implemented by some tools but absent from the reference tool, and at least one unique feature implemented only by the reference tool.
- No false positives: claimed features are not inferred from tool names alone; each entry is grounded in explicit code or documentation evidence.

## Limitations

- MetaboDirect does not provide raw spectra data preprocessing; feature comparison assumes molecular formula assignment has already been performed upstream, limiting scope for tools that include preprocessing pipelines.
- Web-based GUI tools (MetaboAnalyst, UME, FREDA, DropMS) are often restrictive and do not allow full customization; their documented capabilities may not reflect all underlying algorithms or parameter tuning options available in source code.
- Documentation currency and completeness vary across tools; older tools or those without active maintenance may have outdated or incomplete feature descriptions, requiring source code inspection that may be time-consuming or unavailable.
- Feature detection from dependencies (e.g., vegan → PERMANOVA) is probabilistic; a tool may import a package but not use all its functions, or may implement similar functionality without importing the canonical package.

## Evidence

- [other] Which analytical and visualization features are implemented in MetaboDirect, and how do its capabilities compare to other available FT-ICR MS software tools: "Which analytical and visualization features are implemented in MetaboDirect, and how do its capabilities compare to other available FT-ICR MS software tools across key dimensions such as data"
- [other] MetaboDirect performs all analyses offered by other available software for FT-ICR MS data except raw spectra processing: "MetaboDirect performs all analyses offered by other available software for FT-ICR MS data except raw spectra processing and molecular formula assignment, including Van Krevelen diagrams, molecular"
- [other] For each of the five comparison tools, consult their published documentation or repository READMEs to determine feature support: "For each of the five comparison tools (UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, i-van Krevelen), consult their published documentation or repository READMEs to determine feature support for:"
- [other] Cross-reference MetaboDirect source code for the vegan, SYNCSA, pmartR, KEGGREST, and py4cytoscape dependencies: "Cross-reference MetaboDirect source code for the vegan, SYNCSA, pmartR, KEGGREST, and py4cytoscape dependencies to confirm implementation of each feature"
- [other] Construct a structured comparison table with binary entries matching the paper's reported format: "Construct a structured comparison table with binary (✔/✖) entries matching the paper's reported format, with rows as tools and columns as analytical features"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: argparse, numpy, pandas, seaborn, more-itertools, py4cytoscape,"
- [methods] MetaboDirect does not provide raw spectra data preprocessing: "MetaboDirect does not provide raw spectra data preprocessing"
- [intro] they often incur in a compromise between flexibility/customizability and user-friendliness: "they often incur in a compromise between flexi­bility/customizability and user-friendliness that we aim to address with MetaboDirect"
