---
name: ft-icr-ms-analysis-tool-evaluation
description: Use when you are evaluating or selecting FT-ICR MS software for a specific metabolomics workflow and need to assess which tools support your required analytical dimensions (e.g., Van Krevelen diagrams, PERMANOVA, thermodynamic indices, chemodiversity metrics, transformation networks).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ft-icr-ms-analysis-tool-evaluation

## Summary

Systematic evaluation and comparison of feature coverage across FT-ICR MS analysis software tools to assess which analytical and visualization capabilities are implemented in candidate pipelines relative to peer tools. This skill helps researchers select or benchmark software based on concrete feature support for data filtering, statistical analysis, molecular visualization, and transformation network construction.

## When to use

You are evaluating or selecting FT-ICR MS software for a specific metabolomics workflow and need to assess which tools support your required analytical dimensions (e.g., Van Krevelen diagrams, PERMANOVA, thermodynamic indices, chemodiversity metrics, transformation networks). Use this skill when comparing a candidate tool (like MetaboDirect) against established alternatives (UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, i-van Krevelen) to determine feature parity or unique capabilities.

## When NOT to use

- Your input is already a pre-existing published comparison table or benchmark study — extract findings directly rather than re-evaluating.
- You are conducting feature validation or benchmark performance testing (runtime, memory, accuracy on gold-standard data) rather than capability inventory — use performance profiling or validation benchmarking skills instead.
- The tool is designed for raw spectra processing (e.g., peak-picking, deconvolution, mass calibration) rather than post-formula-assignment analysis — MetaboDirect explicitly does not provide raw spectra preprocessing and accepts only peak abundance tables with assigned molecular formulas.

## Inputs

- FT-ICR MS analysis software source code (GitHub repository or local clone)
- Software documentation (ReadTheDocs, published methods, repository README)
- List of comparison tools and their feature inventories
- Dependency specifications (setup.py, requirements.txt, R DESCRIPTION files)

## Outputs

- Feature-comparison matrix (rows = tools, columns = analytical features; entries = binary ✔/✖)
- Categorized feature list (filtering, normalization, visualization, statistics, transformation networks)
- Summary of unique or rare features per tool
- Assessment of user-friendliness vs. flexibility tradeoffs

## How to apply

First, extract the complete feature inventory from the candidate tool by reviewing source code (especially dependencies like vegan, SYNCSA, pmartR, KEGGREST, py4cytoscape), main pipeline code structure, and ReadTheDocs documentation to identify all supported normalization methods, filtering parameters, statistical tests, and indices. Second, for each comparison tool, consult published documentation, repository READMEs, and peer-reviewed methods sections to determine which features each supports. Third, create a structured binary (✔/✖) comparison table with rows as tools and columns as analytical features, organized by functional category: m/z and isotopic filtering, molecular formula quality filters, peak normalization methods (max, minmax, mean, median, total sum, zscore), composition visualization (Van Krevelen, elemental/molecular class plots), thermodynamic indices (NOSC, GFE, AImod, DBE), multivariate statistics (PERMANOVA, NMDS, PCA), chemodiversity metrics (Shannon, Gini-Simpson, Chao1, Rao's), and transformation networks. Cross-reference source code dependencies to confirm each feature's implementation status rather than relying solely on documentation. Finally, validate that the comparison distinguishes between features present in all tools versus unique capabilities; MetaboDirect's automation (single command-line call generating all outputs) and ab initio biochemical transformation network generation are key differentiators.

## Related tools

- **MetaboDirect** (Subject tool being evaluated for feature coverage and automation capability) — https://github.com/Coayala/MetaboDirect
- **UltraMassExplorer (UME)** (Comparison tool — web-based GUI for FT-ICR MS analysis with feature constraints)
- **FREDA** (Comparison tool — web-based FT-ICR MS analysis software)
- **MetaboAnalyst** (Comparison tool — web-based metabolomics analysis platform)
- **DropMS** (Comparison tool — web-based FT-ICR MS data analysis tool)
- **i-van Krevelen** (Comparison tool — interactive visualization tool for Van Krevelen diagrams)
- **vegan** (Dependency for multivariate statistics (NMDS, PERMANOVA) in candidate tool)
- **SYNCSA** (Dependency for chemodiversity analysis and functional diversity metrics)
- **pmartR** (Dependency for normalization method testing and standardization)
- **KEGGREST** (Dependency for biochemical transformation network mapping via KEGG database)
- **py4cytoscape** (Dependency for transformation network visualization and export to Cytoscape)

## Evaluation signals

- Comparison matrix completeness: all candidate tools have entries for every analytical feature category (filtering, normalization, visualization, statistics, transformation networks); no missing cells.
- Source code traceability: each ✔ entry in the matrix is supported by at least one specific function signature, code module, or README statement naming the feature.
- Feature definition consistency: the same feature (e.g., 'PERMANOVA') is defined identically across all rows; no conflation of similar but distinct methods (e.g., PERMANOVA vs. ANOSIM).
- Unique feature validation: MetaboDirect's claimed unique capabilities (ab initio transformation networks, single-command automation generating all outputs in <2 min for 120 samples) are verified against comparison tools' documented feature lists.
- Dependency audit: all Python, R, and Cytoscape dependencies listed in the tool's setup files (setup.py, DESCRIPTION, requirements.txt) are mapped to at least one feature in the matrix.

## Limitations

- MetaboDirect does not provide raw spectra preprocessing (peak-picking, deconvolution, mass calibration), requiring users to pre-process raw FT-ICR MS data with external tools (CoreMS, Formularity) before formula assignment and input to the pipeline.
- Feature inventory relies on documentation and source code inspection; undocumented or deprecated features may be missed, and web-based tools (UME, FREDA, MetaboAnalyst, DropMS) may not have publicly available code for exhaustive inspection.
- Comparison captures feature presence/absence but not usability, customization depth, or parameter flexibility — a binary ✔ for 'PCA' does not reflect whether the tool allows color coding, subset selection, or export of loading plots.
- No evaluation of performance, accuracy, or reproducibility of features across tools — only capability inventory.
- Transformation network generation methodology varies (MetaboDirect uses mass difference network-based approach ab initio; other tools may require KEGG mapping or manual curation) but may be collapsed to single ✔/✖ entry if not carefully distinguished.

## Evidence

- [other] Which analytical and visualization features are implemented in MetaboDirect, and how do its capabilities compare to other available FT-ICR MS software tools across key dimensions such as data filtering, statistical analysis, and transformation network generation?: "Which analytical and visualization features are implemented in MetaboDirect, and how do its capabilities compare to other available FT-ICR MS software tools across key dimensions such as data"
- [other] MetaboDirect performs all analyses offered by other available software for FT-ICR MS data except raw spectra processing and molecular formula assignment, including Van Krevelen diagrams, molecular composition plots, thermodynamic indices, chemodiversity indices, pairwise comparisons, PERMANOVA, NMDS, PCA, and transformation network construction with customization.: "MetaboDirect performs all analyses offered by other available software for FT-ICR MS data except raw spectra processing and molecular formula assignment, including Van Krevelen diagrams, molecular"
- [other] For each of the five comparison tools (UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, i-van Krevelen), consult their published documentation or repository READMEs to determine feature support for: m/z filtering, isotopic filtering, formula error filtering, compound class assignment, peak normalization..., Van Krevelen diagrams, thermodynamic indices (NOSC, GFE, AImod, DBE), PERMANOVA analysis, NMDS ordination, PCA analysis, chemodiversity metrics (Shannon, Gini-Simpson, Chao1, Rao's), and transformation networks.: "For each of the five comparison tools (UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, i-van Krevelen), consult their published documentation or repository READMEs to determine feature support for:"
- [other] Cross-reference MetaboDirect source code for the vegan, SYNCSA, pmartR, KEGGREST, and py4cytoscape dependencies to confirm implementation of each feature.: "Cross-reference MetaboDirect source code for the vegan, SYNCSA, pmartR, KEGGREST, and py4cytoscape dependencies to confirm implementation of each feature."
- [abstract] MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences (mass difference network-based approach): "MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences (mass difference network-based approach)"
- [methods] MetaboDirect does not provide raw spectra data preprocessing: "MetaboDirect does not provide raw spectra data preprocessing"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: vegan, SYNCSA, pmartR (for normalization tests), KEGGREST, py4cytoscape: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: vegan, SYNCSA, pmartR (for normalization tests), KEGGREST,"
- [intro] they often incur in a compromise between flexibility/customizability and user-friendliness that we aim to address with MetaboDirect: "they often incur in a compromise between flexibility/customizability and user-friendliness that we aim to address with MetaboDirect"
- [results] 40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min to generate all the figures, plots, and outputs: "40 samples were processed in less than 1 min whereas 120 samples took as little as 2 min to generate all the figures, plots, and outputs"
