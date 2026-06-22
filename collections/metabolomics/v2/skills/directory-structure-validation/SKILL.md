---
name: directory-structure-validation
description: Use when after editing core R scripts in the Core-Match repository and before running LipidMatch-4.2 analysis, to verify that developer modifications have been correctly distributed across the Flow version (LipidMatch_Distribution) and Modular version (FluoroMatch_Modular) directory trees.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - LipidMatch
  - FluoroMatch
derived_from:
- doi: 10.1007/s00216-021-03392-7
  title: FluoroMatch 2.0
evidence_spans:
- put Modular.r into two directories
- 'put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution`'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fluoromatch_2_0_cq
    doi: 10.1007/s00216-021-03392-7
    title: FluoroMatch 2.0
  dedup_kept_from: coll_fluoromatch_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-021-03392-7
  all_source_dois:
  - 10.1007/s00216-021-03392-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# directory-structure-validation

## Summary

Validates that edited script files (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R) are placed into the correct target directories within LipidMatch-4.2 distribution to ensure developer changes integrate properly into both Flow and Modular analysis versions.

## When to use

Apply this skill after editing core R scripts in the Core-Match repository and before running LipidMatch-4.2 analysis, to verify that developer modifications have been correctly distributed across the Flow version (LipidMatch_Distribution) and Modular version (FluoroMatch_Modular) directory trees.

## When NOT to use

- When using pre-compiled binary distributions where script files cannot be edited or replaced
- When script files are being downloaded directly from innovativeomics.com/software (use official binary distribution instead)
- When working with a cloned Core-Match repository alone without an installed LipidMatch-4.2 distribution

## Inputs

- edited R script files (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R)
- LipidMatch-4.2 distribution directory structure (downloaded from InnovativeOmics)
- README or methods specification file documenting target paths

## Outputs

- manifest file mapping source files to target paths (CSV or JSON format)
- validated directory tree or layout document
- confirmation that all script files are placed in correct locations

## How to apply

First, identify the four edited script files (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R) from your source submission package. Next, create a manifest file (CSV or JSON) that maps each source file to its required target path(s): Modular.r must be placed in both `LipidMatch-4.2\Flow\LipidMatch_Distribution` and `LipidMatch-4.2\FluoroMatch_Modular` to replace existing code; genEIC.r, MS1Spectragen.r, and Stats.R must all be placed into `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`. Then, verify that each target directory exists within your downloaded LipidMatch-4.2 distribution (typically downloaded from innovativeomics.com/software). Finally, generate a directory tree or layout document showing the final file placement structure to confirm all files are in their specified locations before executing analysis workflows.

## Related tools

- **LipidMatch** (target software distribution into which edited scripts must be integrated) — https://github.com/InnovativeOmics/Core-Match
- **FluoroMatch** (alternative analysis version of LipidMatch requiring Modular.r placement for integration) — https://github.com/InnovativeOmics/Core-Match
- **R** (runtime environment for executing edited script files (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R))

## Evaluation signals

- All four script files (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R) are present in their specified target directories
- Modular.r exists in both `LipidMatch-4.2\Flow\LipidMatch_Distribution` AND `LipidMatch-4.2\FluoroMatch_Modular` directories
- genEIC.r, MS1Spectragen.r, and Stats.R all exist in `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`
- Manifest file entries match actual file locations verified via directory listing or tree output
- No orphaned script files remain in intermediate or incorrect directories

## Limitations

- Validation assumes target directories already exist within the LipidMatch-4.2 distribution; missing parent directories will prevent proper file placement
- Windows and Unix path separators differ (backslash vs. forward slash); cross-platform deployment requires path normalization
- No changelog is available to document which versions of scripts are compatible with which LipidMatch-4.2 releases; version mismatches may cause runtime errors
- The skill validates structural placement only; it does not verify script syntax, dependencies, or functional correctness

## Evidence

- [readme] Modular.r must replace existing code in both directories: "put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution` `LipidMatch-4.2\FluoroMatch_Modular`"
- [readme] Other edited scripts go into the Scripts subdirectory: "Place any edited script files (genEIC.r, MS1Spectragen.r, Stats.R) into: `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`"
- [readme] Developers edit scripts on GitHub and must integrate into downloaded distributions: "**Developers can edit the main algorithms here on github** as a team. Then the code needs to be integrated by placing the edited code in the correct directory from the downloaded distribution"
- [readme] Users download the distribution from the official website: "For LipidMatch, FluoroMatch, and PolyMatch **users should directly download from innovativeomics.com/software** for the latest stable release."
- [readme] Installation is prerequisite to integration: "Install FluoroMatch or LipidMatch from InnovativeOmics.com"
