# Evaluation Strategy

## Direct Checks

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

## Expert Review

- Verify that the five tools in the reconstructed table match the canonical comparison tools intended by the paper (MetaboDirect, CoreMS, ftmsRanalysis, MetaboAnalyst, UltraMassExplorer) based on context of introduction section
- Verify that the set of analytical features (filtering, normalization, Van Krevelen diagrams, PERMANOVA, NMDS, PCA, transformation networks, chemodiversity) selected for comparison are the most salient and representative features discussed in the paper
- Verify that binary ✔/✖ assignments for each tool-feature pair are consistent with explicit statements in tool documentation and the paper's characterization of each tool's capabilities
- Verify that the comparison table reflects documented limitations (e.g., whether web-based tools restrict customization, whether R-based tools require coding competence) mentioned in the introduction
