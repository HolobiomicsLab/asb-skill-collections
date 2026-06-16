# SciTask Card: Reproduce the feature-comparison table of MetaboDirect versus MetaboAnalyst, PyKrev, ftmsRanalysis, and UME

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T08:03:26.683093+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/pkg_metabodirect`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `information-extraction`, `benchmark-evaluation`
- GitHub: `Coayala/MetaboDirect`
- Quality: Score 2/5 — Coherent: false, placeholder, 7 grounding failures

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `microbiome-metabolomics`, `environmental-metabolomics`, `untargeted-metabolomics`
- Techniques: `direct-infusion-ms`, `high-resolution-ms`, `feature-detection`, `metabolite-identification`, `multivariate-statistics`, `molecular-networking`

## Research Question
Which analytical and visualization features are implemented in MetaboDirect, and how do its capabilities compare to other available FT-ICR MS software tools across key dimensions such as data filtering, statistical analysis, and transformation network generation?

## Connected Finding
MetaboDirect performs all analyses offered by other available software for FT-ICR MS data except raw spectra processing and molecular formula assignment, including Van Krevelen diagrams, molecular composition plots, thermodynamic indices, chemodiversity indices, pairwise comparisons, PERMANOVA, NMDS, PCA, and transformation network construction with customization.

## Task Description
Verify the presence or absence of analytical features (data filtering, normalization methods, visualization types, statistical tests, transformation network analysis) across five FT-ICR MS analysis tools by inspecting the MetaboDirect codebase and documentation, then reconstruct the binary comparison table reported in the paper.

## Inputs
- MetaboDirect GitHub repository code and documentation
- MetaboDirect ReadTheDocs webpage with full pipeline documentation
- Published documentation or repositories for UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, and i-van Krevelen

## Expected Outputs
- Structured comparison table (CSV or TSV format) with rows for each of five tools and columns for analytical features, with binary ✔/✖ entries indicating presence or absence of each feature

## Expected Output File

- `tool_feature_comparison.csv`

## Landmark Outputs

- `metabodirect_features.txt`
- `ume_freda_metaboanalyst_dropms_ivankrevel_docs_parsed.txt`
- `feature_matrix_raw.csv`
- `tool_feature_comparison.csv`

## Tools
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

## Skills
- software-feature-inventory-and-comparison
- code-repository-analysis
- ft-icr-ms-analysis-tool-evaluation
- analytical-pipeline-feature-documentation
- cross-platform-software-capability-mapping

## Workflow Description
1. Clone the MetaboDirect GitHub repository and review the main pipeline code structure, function signatures, and command-line argument definitions to identify which analytical features are implemented. 2. Parse the ReadTheDocs documentation and supplementary tables (referenced in methods) to extract the complete list of supported normalization methods, filtering parameters, indices calculated, and statistical tests. 3. For each of the five comparison tools (UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, i-van Krevelen), consult their published documentation or repository READMEs to determine feature support for: m/z filtering, isotopic filtering, formula error filtering, compound class assignment, peak normalization (max, minmax, mean, median, total sum, zscore), Van Krevelen diagrams, thermodynamic indices (NOSC, GFE, AImod, DBE), PERMANOVA analysis, NMDS ordination, PCA analysis, chemodiversity metrics (Shannon, Gini-Simpson, Chao1, Rao's), and transformation networks. 4. Cross-reference MetaboDirect source code for the vegan, SYNCSA, pmartR, KEGGREST, and py4cytoscape dependencies to confirm implementation of each feature. 5. Construct a structured comparison table with binary (✔/✖) entries matching the paper's reported format, with rows as tools and columns as analytical features.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `metabodirect.pdf` | main_article | True |

## Missing Information
- No explicit Table 1 comparison table is present in the provided document text; the paper structure mentions features but does not show the actual binary matrix comparing five tools across analytical features.
- The exact list of analytical features included in the original Table 1 comparison is not explicitly enumerated in the provided text; features mentioned across methods section (filtering, normalization, Van Krevelen, PERMANOVA, NMDS, PCA, transformation networks) must be inferred.
- Documentation and feature availability for comparison tools (CoreMS, ftmsRanalysis, MetaboAnalyst, UltraMassExplorer, FREDA, DropMS) is cited via references and links but the specific feature sets are not detailed in the provided discussion section.
- Whether MetaboDirect supports chemodiversity analysis (mentioned in abstract) and which specific diversity metrics (Chao1, Gini-Simpson, Shannon, Rao's quadratic entropy) are supported must be confirmed from codebase inspection.

## Domain Knowledge
- FT-ICR MS data analysis pipelines typically include filtering (m/z, isotopic, formula error, sample prevalence), normalization, molecular property calculations (NOSC, GFE, AImod, DBE), visualization (Van Krevelen diagrams), and statistical/multivariate ordination methods (PERMANOVA, NMDS, PCA).
- Normalization methods in metabolomics include max, minmax, mean, median, total sum, and zscore; more complex methods like PQN require reference spectrum selection which may not be available for exploratory analysis of complex samples.
- Chemodiversity metrics adapted from ecology (Shannon, Gini-Simpson, Chao1, Rao's quadratic entropy) quantify both abundance-based and functional-trait-based diversity in metabolite composition across samples.
- Mass difference network analysis identifies putative biochemical transformations by comparing m/z differences between detected peaks against a reference biochemical transformation key with ≤1 ppm error tolerance.
- MetaboDirect uniquely generates transformation networks ab initio and requires only a single command line execution, whereas existing tools represent compromises between user-friendliness (web-based GUIs) and customizability (R/Python programming-required tools).

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Which analytical and visualization features are implemented in MetaboDirect, and how do its capabilities compare to other available FT-ICR MS software tools across key dimensions such as data filtering, statistical analysis, and transformation network generation?: 'Despite the broad availability of software packages for the analysis of FT-ICR MS data, they often incur in a compromise between flexibility/customizability and user-friendliness that we aim to'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] MetaboDirect performs all analyses offered by other available software for FT-ICR MS data except raw spectra processing and molecular formula assignment, including Van Krevelen diagrams, molecular composition plots, thermodynamic indices, chemodiversity indices, pairwise comparisons, PERMANOVA, NMDS, PCA, and transformation network construction with customization.: 'As observed in Table 1, MetaboDirect can perform all the analyses offered by the other available software for FT‑ICR MS data, except for "raw spectra processing" and "molecular formula assignment"'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] MetaboDirect GitHub repository code and documentation: 'available to install through the Python Package Index (https:// pypi. org/ proje ct/ metab odire ct/)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] MetaboDirect ReadTheDocs webpage with full pipeline documentation: 'The full documentation for the pipeline can be found on its ReadTheDocs webpage: https:// metab odire ct. readt hedocs. io'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] Published documentation or repositories for UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, and i-van Krevelen: 'web-based applications such as UltraMassExplorer (UME) [27], FREDA [28], MetaboAnalyst [29], and DropMS [30]'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Structured comparison table (CSV or TSV format) with rows for each of five tools and columns for analytical features, with binary ✔/✖ entries indicating presence or absence of each feature: 'The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1): (i) data pre-processing, (ii) data diagnostics, (iii) data exploration, (iv) chemodiversity analysis, (v) statistical'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] MetaboDirect: 'The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] UltraMassExplorer: 'web-based applications such as UltraMassExplorer (UME)'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] FREDA: 'web-based applications such as UltraMassExplorer (UME) [27], FREDA [28]'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] MetaboAnalyst: 'web-based applications such as UltraMassExplorer (UME) [27], FREDA [28], MetaboAnalyst [29]'
- `ev_011` from `agent2_synthesis` (agent2_traced): [intro] DropMS: 'web-based applications such as UltraMassExplorer (UME) [27], FREDA [28], MetaboAnalyst [29], and DropMS [30]'
- `ev_012` from `agent2_synthesis` (agent2_traced): [intro] i-van Krevelen: 'visualization tools i-van Krevelen [31]'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] vegan: 'diversity metrics using functions from the R packages vegan [63]'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] SYNCSA: 'diversity metrics using functions from the R packages vegan [63] and SYNCSA [64]'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] pmartR: 'uses a modified "spans_procedure" function from the R package pmartR [51]'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] KEGGREST: 'query the KEGG database [59] using the R package KEGGREST [60]'
- `ev_017` from `agent2_synthesis` (agent2_traced): [methods] py4cytoscape: 'It requires the Python dependencies NumPy [40], pandas [41, 42], seaborn [43], py4cytoscape, and matplotlib [44]'
- `ev_018` from `agent2_synthesis` (agent2_traced): [other] No explicit Table 1 comparison table is present in the provided document text; the paper structure mentions features but does not show the actual binary matrix comparing five tools across analytical features.: 'The online version contains supplementary material available at https:// doi. org/ 10. 1186/ s40168‑ 023‑ 01476‑3.'
- `ev_019` from `agent2_synthesis` (agent2_traced): [methods] The exact list of analytical features included in the original Table 1 comparison is not explicitly enumerated in the provided text; features mentioned across methods section (filtering, normalization, Van Krevelen, PERMANOVA, NMDS, PCA, transformation networks) must be inferred.: 'MetaboDirect pipeline consists of six main steps for the analysis of FT-ICR MS data'
- `ev_020` from `agent2_synthesis` (agent2_traced): [intro] Documentation and feature availability for comparison tools (CoreMS, ftmsRanalysis, MetaboAnalyst, UltraMassExplorer, FREDA, DropMS) is cited via references and links but the specific feature sets are not detailed in the provided discussion section.: 'open-source software such as Formularity [24], most recently CoreMS [25], which provides a comprehensive software framework, or web-based applications such as UltraMassExplorer (UME) [27], FREDA'
- `ev_021` from `agent2_synthesis` (agent2_traced): [other] Whether MetaboDirect supports chemodiversity analysis (mentioned in abstract) and which specific diversity metrics (Chao1, Gini-Simpson, Shannon, Rao's quadratic entropy) are supported must be confirmed from codebase inspection.: 'fully automated pipeline capable of easily generating all the figures, plots, and analysis that are commonly used by the scientific community to visualize, analyze, and interpret FT-ICR MS data sets'

## Evaluation Strategy
### Direct Checks
- file_exists: https://github.com/Coayala/MetaboDirect repository is accessible and contains source code
- file_format_is: MetaboDirect GitHub repository contains Python source files (.py) in expected structure
- contains_substring: MetaboDirect codebase documentation mentions 'Van Krevelen' diagram generation capability
- contains_substring: MetaboDirect codebase documentation mentions 'PERMANOVA' statistical analysis
- contains_substring: MetaboDirect codebase documentation mentions 'NMDS' ordination capability
- contains_substring: MetaboDirect codebase documentation mentions 'normalization' or 'normalize' for peak intensity normalization
- contains_substring: MetaboDirect codebase documentation mentions 'transformation network' or 'mass difference network' construction
- contains_substring: CoreMS GitHub repository (https://github.com/EMSL-Computing/CoreMS) documentation mentions 'Van Krevelen'
- contains_substring: ftmsRanalysis (ftmsRanalysis R package) documentation mentions 'PERMANOVA' capability
- contains_substring: MetaboAnalyst web interface or documentation mentions 'PCA' analysis capability
- file_exists: MetaboDirect User Guide (https://metabodirect.readthedocs.io) is accessible
- contains_substring: MetaboDirect User Guide mentions supported analytical features with binary presence/absence indicators
- output_matches_reference: reconstructed feature comparison table matches structure and binary (✔/✖) notation of original paper Table 1 — robust to cell ordering but exact on tool names and feature names

### Expert Review
- Verify that the five tools in the reconstructed table match the canonical comparison tools intended by the paper (MetaboDirect, CoreMS, ftmsRanalysis, MetaboAnalyst, UltraMassExplorer) based on context of introduction section
- Verify that the set of analytical features (filtering, normalization, Van Krevelen diagrams, PERMANOVA, NMDS, PCA, transformation networks, chemodiversity) selected for comparison are the most salient and representative features discussed in the paper
- Verify that binary ✔/✖ assignments for each tool-feature pair are consistent with explicit statements in tool documentation and the paper's characterization of each tool's capabilities
- Verify that the comparison table reflects documented limitations (e.g., whether web-based tools restrict customization, whether R-based tools require coding competence) mentioned in the introduction

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Inspect MetaboDirect codebase (Python/R) and ReadTheDocs documentation to enumerate all implemented analytical features across six pipeline steps.
2. Systematically extract feature specifications from source code: filtering thresholds (m/z, isotopic, formula error ≤0.5 ppm, sample prevalence), normalization methods (max, minmax, mean, median, total sum, zscore), molecular indices (NOSC, GFE, AImod, DBE), statistical tests (PERMANOVA, NMDS, PCA), chemodiversity metrics (Shannon, Gini-Simpson, Chao1, Rao's), and transformation network construction.
3. Query published documentation for UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, and i-van Krevelen to determine which features each tool supports.
4. Cross-reference MetaboDirect dependencies (vegan, SYNCSA, pmartR, KEGGREST, py4cytoscape) to confirm implementation of statistical and network visualization features.
5. Construct binary comparison table with tools as rows and features as columns, marking ✔ for present and ✖ for absent.
6. Validation: Comparison table matches the binary feature matrix reported in the paper's tool comparison figure/table, with all six MetaboDirect pipeline steps and all cited comparison tools represented.

## Workflow Ports

**Inputs:**

- `metabodirect_repo` — MetaboDirect GitHub repository and code
- `comparison_tools_docs` — Published documentation for comparison tools

**Outputs:**

- `feature_comparison_table` — Binary feature comparison table across five tools

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (7):
  - finding: evidence_span not found in section 'intro' (value='MetaboDirect performs all analyses offered by other availabl', span='As observed in Table 1, MetaboDirect can perform all the ana')
  - tools[8]: evidence_span not found in section 'methods' (value='pmartR', span='uses a modified "spans_procedure" function from the R packag')
  - missing_information[1]: evidence_span not found in section 'methods' (value='The exact list of analytical features included in the origin', span='MetaboDirect pipeline consists of six main steps for the ana')
  - missing_information[2]: evidence_span not found in section 'intro' (value='Documentation and feature availability for comparison tools ', span='open-source software such as Formularity [24], most recently')
  - missing_information[3]: evidence_span not found in section 'other' (value='Whether MetaboDirect supports chemodiversity analysis (menti', span='fully automated pipeline capable of easily generating all th')
  - SEMANTIC GAP: research_question asks 'how do its capabilities compare' but finding only states what MetaboDirect can do relative to absence of two features; no comparative analysis of key dimensions (filtering, statistical analysis, transformation network generation) is provided
  - SEMANTIC GAP: finding asserts specific features (Van Krevelen, PERMANOVA, NMDS, PCA, transformation networks, thermodynamic indices, chemodiversity indices) but these are not substantiated by the cited evidence span 'Table 1'
- Notes: This task card has severe structural problems. The core finding references 'Table 1' as evidence, but Table 1 is not provided in the source material, making the finding completely ungroundable. The research question asks for comparative feature analysis ('how do capabilities compare...across key dimensions'), but the finding merely enumerates MetaboDirect features without comparative context. Multiple placeholder language issues exist ('the data', 'the paper', 'five comparison tools' without clear enumeration). The tools list mixes comparison tools (UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, i-van Krevelen) with implementation dependencies (vegan, SYNCSA, pmartR, KEGGREST, py4cytoscape), creating confusion about scope. The missing_information section itself admits the feature list is inferred rather than extracted, yet the finding presents these inferences as established facts. The task is reproduction-class but lacks the reference artifact (Table 1) needed for validation. The task would require access to the original paper's Table 1 and external documentation not provided here; as currently framed, it cannot be assessed for quality without that material.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
