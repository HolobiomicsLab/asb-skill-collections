---
name: software-feature-inventory-and-comparison
description: Use when you need to assess whether a newly developed FT-ICR MS pipeline
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
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
  - LC-MS
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis
  (e.g., chemodiversity analysis, multivariate statistics)
- web-based applications such as UltraMassExplorer (UME)
- web-based applications such as UltraMassExplorer (UME) [27], FREDA [28]
- web-based applications such as UltraMassExplorer (UME) [27], FREDA [28], MetaboAnalyst
  [29]
- web-based applications such as UltraMassExplorer (UME) [27], FREDA [28], MetaboAnalyst
  [29], and DropMS [30]
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

# software-feature-inventory-and-comparison

## Summary

Systematically document and compare analytical capabilities across multiple software tools for FT-ICR MS data analysis, producing a structured feature matrix that identifies which implementations support each analytical method, visualization type, and data transformation. This skill is essential when evaluating tool suitability for a specific research question or when positioning a new tool within the existing ecosystem.

## When to use

You need to assess whether a newly developed FT-ICR MS pipeline (e.g. MetaboDirect) implements all analytical features available in competing tools (UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, i-van Krevelen), or when selecting between tools for a study requiring specific analyses such as Van Krevelen diagrams, thermodynamic indices (NOSC, GFE, AImod, DBE), PERMANOVA, NMDS, PCA, or transformation network generation.

## When NOT to use

- The input tools use incompatible data formats or operate on different types of mass spectrometry instruments (e.g., mixing FT-ICR MS with GC-MS or LC-MS tools designed for different molecular weight ranges or compound classes).
- Comparison tools are closed-source or proprietary with no accessible documentation, source code, or published methods; feature parity cannot be reliably determined.
- Your research question requires runtime performance comparison (speed, memory usage, scalability) rather than feature availability; use computational benchmarking instead of feature inventory.

## Inputs

- GitHub repository or source code directory for target software (e.g., Coayala/MetaboDirect)
- ReadTheDocs or published documentation pages for target and comparison tools
- Published methods sections or supplementary tables describing feature availability
- Software dependency declarations (setup.py, requirements.txt, DESCRIPTION, environment.yml)

## Outputs

- Structured feature-comparison table (matrix format: rows=tools, columns=analytical features, cells=binary ✔/✖)
- Annotated feature list with implementation source (code location, dependency, or documentation reference)
- Capability gap summary identifying features implemented in target but not in comparators (and vice versa)

## How to apply

First, clone the target software repository and parse the main pipeline code, function signatures, and command-line argument definitions to extract a list of implemented analytical features; cross-reference the README, ReadTheDocs documentation, and published methods to identify supported normalization methods, filtering parameters, and statistical tests. Second, for each comparison tool, consult published documentation, repository READMEs, and dependency declarations to determine feature support across a predefined feature set (e.g., m/z filtering, isotopic filtering, formula error filtering, compound class assignment, normalization strategies, Van Krevelen diagrams, thermodynamic indices, PERMANOVA, NMDS, PCA, chemodiversity metrics: Shannon, Gini-Simpson, Chao1, Rao's, and transformation networks). Third, trace dependencies (e.g., vegan, SYNCSA, pmartR, KEGGREST, py4cytoscape) in source code to confirm implementation. Finally, construct a binary comparison table with tools as rows and analytical features as columns, using ✔ and ✖ symbols to match published format.

## Related tools

- **MetaboDirect** (target software for feature inventory and capability assessment) — https://github.com/Coayala/MetaboDirect
- **UltraMassExplorer (UME)** (comparison tool for FT-ICR MS analysis features)
- **FREDA** (comparison tool for FT-ICR MS visualization and analysis)
- **MetaboAnalyst** (comparison tool for multivariate analysis and metabolomics workflows)
- **DropMS** (comparison tool for FT-ICR MS data processing)
- **i-van Krevelen** (comparison tool for Van Krevelen diagram visualization)
- **vegan** (R package implementing PERMANOVA, NMDS, and diversity indices in MetaboDirect)
- **SYNCSA** (R package for community ecology analysis used in MetaboDirect)
- **pmartR** (R package for normalization method implementation and testing in MetaboDirect)
- **KEGGREST** (R package for KEGG database querying in MetaboDirect transformation network mapping)
- **py4cytoscape** (Python package for Cytoscape network visualization in MetaboDirect)

## Evaluation signals

- Binary feature matrix is complete and covers all tools and features; no empty cells except where features are explicitly not supported.
- Feature assignments match source code inspection results (e.g., presence of vegan import in setup.py confirms PERMANOVA and NMDS support; presence of pmartR confirms normalization method availability).
- Capability gap summary correctly identifies MetaboDirect's unique features (transformation networks based on mass differences) and limitations (no raw spectra preprocessing) as described in article.
- Features are consistently interpreted across tools (e.g., if 'Van Krevelen diagram' is marked ✔ for one tool, verify all comparison tools use the same or functionally equivalent definition; inconsistent definitions should be flagged).
- Feature coverage for MetaboDirect in final matrix matches the article's stated capabilities: Van Krevelen diagrams, molecular composition plots, thermodynamic indices, chemodiversity indices, pairwise comparisons, PERMANOVA, NMDS, PCA, transformation networks — all marked ✔.

## Limitations

- MetaboDirect does not provide raw spectra data preprocessing; feature inventory should note that input data must have already undergone signal processing and molecular formula assignment before pipeline entry.
- Feature comparison is constrained by documentation quality and accessibility; closed-source tools or those lacking detailed methods sections cannot be reliably included.
- Presence of a dependency (e.g., vegan in R setup) confirms capability availability but does not guarantee end-user-facing feature completeness; some imports may be used for internal testing (e.g., pmartR is listed for normalization tests) rather than in production workflows.
- Feature matrices reflect implemented features as of the article's publication date; tool capabilities evolve over time and comparisons become outdated without periodic re-inventory.

## Evidence

- [other] MetaboDirect performs all analyses offered by other available software for FT-ICR MS data except raw spectra processing and molecular formula assignment, including Van Krevelen diagrams, molecular composition plots, thermodynamic indices, chemodiversity indices, pairwise comparisons, PERMANOVA, NMDS, PCA, and transformation network construction with customization.: "MetaboDirect performs all analyses offered by other available software for FT-ICR MS data except raw spectra processing and molecular formula assignment, including Van Krevelen diagrams, molecular"
- [supplementary] The complete code for the MetaboDirect pipeline is freely available at its GitHub repository: https://github.com/Coayala/MetaboDirect.: "The complete code for the MetaboDirect pipeline is freely available at its GitHub repository: https://github.com/Coayala/MetaboDirect"
- [intro] web-based applications such as UltraMassExplorer (UME), FREDA, MetaboAnalyst, and DropMS: "web-based applications such as UltraMassExplorer (UME), FREDA, MetaboAnalyst, and DropMS"
- [abstract] MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences (mass difference network–based approach): "MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences"
- [methods] MetaboDirect does not provide raw spectra data preprocessing: "MetaboDirect does not provide raw spectra data preprocessing"
- [readme] R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: tidyverse, RColorBrewer, vegan, ggnewscale, ggpubr, KEGGREST, factoextra, UpSetR, pmartR (for normalization tests), SYNCSA: "vegan, ggnewscale, ggpubr, KEGGREST, factoextra, UpSetR, pmartR (for normalization tests), SYNCSA"
- [intro] fully automated pipeline capable of easily generating all the figures, plots, and analysis that are commonly used by the scientific community to visualize, analyze, and interpret FT-ICR MS data sets: "fully automated pipeline capable of easily generating all the figures, plots, and analysis that are commonly used by the scientific community to visualize, analyze, and interpret FT-ICR MS data sets"
