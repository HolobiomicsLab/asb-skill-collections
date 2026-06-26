---
name: analytical-pipeline-feature-documentation
description: Use when you are evaluating a new or existing data analysis pipeline
  (e.g., MetaboDirect) and need to produce a transparent, evidence-based feature matrix
  showing which analyses it supports—particularly when the pipeline is positioned
  as an alternative to or improvement over established tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
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
  techniques:
  - mass-spectrometry
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

# analytical-pipeline-feature-documentation

## Summary

Document and cross-validate the analytical and visualization features implemented in a bioinformatics pipeline by extracting capabilities from source code, official documentation, and dependency declarations, then comparing against peer software. This skill ensures comprehensive, reusable feature inventories and enables informed tool selection for FT-ICR MS analysis.

## When to use

You are evaluating a new or existing data analysis pipeline (e.g., MetaboDirect) and need to produce a transparent, evidence-based feature matrix showing which analyses it supports—particularly when the pipeline is positioned as an alternative to or improvement over established tools. This is essential before publication, when users need to know whether the tool handles their specific analytical needs (e.g., Van Krevelen diagrams, PERMANOVA, transformation networks), and when claiming novel capabilities.

## When NOT to use

- The pipeline has not yet been published or released; feature claims are speculative or in development.
- The pipeline is purely a wrapper around existing, well-documented packages and adds no novel analyses; documenting the wrapped packages separately is sufficient.
- You are evaluating a closed-source or commercial tool with no accessible source code or public feature disclosure.

## Inputs

- GitHub repository source code (Python, R, or mixed)
- setup.py or requirements.txt / environment.yml (dependency manifest)
- ReadTheDocs or project documentation (methods section)
- Published supplementary tables or SI describing features
- Peer-tool documentation (GitHub READMEs, published papers)

## Outputs

- Feature comparison table (binary or categorical matrix: tools × analytical features)
- Annotated feature inventory for the primary pipeline (with code references)
- Evidence citation map (feature → source location: code file, doc section, dependency module)

## How to apply

First, clone the source repository and inspect the main pipeline code structure, function signatures, and command-line argument definitions to enumerate which analytical features are actually implemented. Next, extract the complete feature list from ReadTheDocs documentation, supplementary materials, and dependency declarations (inspect setup.py or requirements files for key libraries like vegan, SYNCSA, pmartR, KEGGREST, py4cytoscape). Third, consult published documentation or repository READMEs for 3–5 peer tools, recording feature support for each analysis type (e.g., m/z filtering, isotopic filtering, formula error filtering, compound class assignment, peak normalization methods, statistical tests, indices, ordination, transformation networks). Fourth, cross-reference the source pipeline code against its declared dependencies to confirm each feature is genuinely invoked, not merely imported. Finally, construct a structured comparison table with binary (✔/✖) or categorical entries matching published format, with rows as tools and columns as analytical features, and cite the evidence source (code location, documentation section, dependency module) for each claim.

## Related tools

- **vegan** (R library providing PERMANOVA, NMDS, and multivariate statistics (invoked by MetaboDirect for ordination and statistical analysis))
- **SYNCSA** (R library for multivariate analysis; referenced as MetaboDirect dependency)
- **pmartR** (R library for normalization method testing and peak intensity normalization options)
- **KEGGREST** (R library for querying KEGG database to map molecular formulas to biochemical pathways)
- **py4cytoscape** (Python library enabling programmatic Cytoscape control for transformation network visualization)
- **UltraMassExplorer** (Web-based comparison tool for FT-ICR MS analysis; used as peer benchmark for feature matrix)
- **MetaboAnalyst** (Web-based comparison tool for metabolomics analysis; used as peer benchmark)
- **i-van Krevelen** (Specialized visualization tool for Van Krevelen diagrams; feature to compare against MetaboDirect)

## Examples

```
metabodirect -h
```

## Evaluation signals

- Feature matrix rows and columns are mutually exclusive, exhaustive, and use consistent terminology across all tools; no entry is ambiguous or duplicated.
- Each ✔ entry in the matrix is backed by a specific code reference (file path and function name) or documentation section; spot-check 3–5 claims by reviewing the actual invocation in source code.
- All declared dependencies in setup.py/requirements.txt correspond to at least one analytical feature; no orphaned imports.
- Peer-tool features are sourced from published documentation or official repositories, not inferred; any uncertainty is marked or footnoted.
- The matrix accurately reflects MetaboDirect's limitation: raw spectra preprocessing is NOT implemented (pipeline accepts post-assignment peak abundance and molecular formula data only).

## Limitations

- MetaboDirect does not provide raw spectra data preprocessing; the pipeline accepts peak abundance and assigned molecular formula data produced after initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique.
- Web-based peer tools (UltraMassExplorer, MetaboAnalyst, FREDA, DropMS) may have undocumented features or updates not reflected in published documentation; comparison is a snapshot in time.
- Feature parity does not imply identical algorithmic implementations or parameter flexibility; a ✔ for 'PCA' in two tools does not guarantee identical preprocessing or output interpretation.
- The comparison assumes all peer tools accept the same input format (peak abundance + assigned formula); tools requiring raw spectra or different formula assignment are not directly comparable.

## Evidence

- [other] Clone the MetaboDirect GitHub repository and review the main pipeline code structure, function signatures, and command-line argument definitions to identify which analytical features are implemented.: "Clone the MetaboDirect GitHub repository and review the main pipeline code structure, function signatures, and command-line argument definitions to identify which analytical features are implemented."
- [other] For each of the five comparison tools (UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, i-van Krevelen), consult their published documentation or repository READMEs to determine feature support for: m/z filtering, isotopic filtering, formula error filtering, compound class assignment, peak normalization (max, minmax, mean, median, total sum, zscore), Van Krevelen diagrams, thermodynamic indices (NOSC, GFE, AImod, DBE), PERMANOVA analysis, NMDS ordination, PCA analysis, chemodiversity metrics (Shannon, Gini-Simpson, Chao1, Rao's), and transformation networks.: "For each of the five comparison tools (UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, i-van Krevelen), consult their published documentation or repository READMEs"
- [other] Cross-reference MetaboDirect source code for the vegan, SYNCSA, pmartR, KEGGREST, and py4cytoscape dependencies to confirm implementation of each feature.: "Cross-reference MetaboDirect source code for the vegan, SYNCSA, pmartR, KEGGREST, and py4cytoscape dependencies to confirm implementation of each feature."
- [other] MetaboDirect performs all analyses offered by other available software for FT-ICR MS data except raw spectra processing and molecular formula assignment, including Van Krevelen diagrams, molecular composition plots, thermodynamic indices, chemodiversity indices, pairwise comparisons, PERMANOVA, NMDS, PCA, and transformation network construction with customization.: "MetaboDirect performs all analyses offered by other available software for FT-ICR MS data except raw spectra processing and molecular formula assignment"
- [intro] The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: argparse, numpy, pandas, seaborn, more-itertools, py4cytoscape, statsmodels; vegan, ggnewscale, ggpubr, KEGGREST, factoextra, UpSetR, pmartR, SYNCSA, ggvenn, ggrepel.: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules"
