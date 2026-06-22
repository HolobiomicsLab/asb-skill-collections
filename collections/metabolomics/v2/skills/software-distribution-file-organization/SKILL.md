---
name: software-distribution-file-organization
description: Use when you have edited one or more core algorithm scripts (Modular.r, genEIC.r, MS1Spectragen.r, or Stats.R) in a shared developer repository (e.g., Core-Match on GitHub) and need to integrate those changes into an already-installed LipidMatch-4.2 or FluoroMatch distribution on disk.
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
  - Core-Match
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

# software-distribution-file-organization

## Summary

Organize edited algorithm scripts into version-specific directory structures within a downloaded LipidMatch or FluoroMatch distribution to integrate developer changes from a central repository into both Flow and Modular execution modes. This skill ensures that script modifications are placed in the correct target paths so the software framework can load and execute them without breaking either workflow variant.

## When to use

You have edited one or more core algorithm scripts (Modular.r, genEIC.r, MS1Spectragen.r, or Stats.R) in a shared developer repository (e.g., Core-Match on GitHub) and need to integrate those changes into an already-installed LipidMatch-4.2 or FluoroMatch distribution on disk. This skill is necessary before testing or deploying the modified software to ensure the installed version uses your updated code rather than the original distribution defaults.

## When NOT to use

- You are an end-user installing LipidMatch or FluoroMatch for the first time without custom script modifications — use the standard InnovativeOmics.com download instead.
- You have not yet edited or cloned the Core-Match repository; you are only using the pre-built distribution as-is.
- Your edits are to documentation, metadata, or parameters only (not the algorithm scripts themselves) — those changes typically do not require this file reorganization skill.

## Inputs

- Edited script files: Modular.r, genEIC.r, MS1Spectragen.r, Stats.R (from GitHub Core-Match repository or local developer edits)
- Installed LipidMatch-4.2 or FluoroMatch distribution directory (from InnovativeOmics.com download)
- README or methods specification documenting target directory paths

## Outputs

- Organized script files distributed across LipidMatch-4.2 directory structure
- Manifest file (CSV or JSON) mapping source files to target paths
- Directory tree or layout document showing final file placement

## How to apply

First, install the base LipidMatch or FluoroMatch distribution from InnovativeOmics.com. Then identify which scripts you have edited (Modular.r requires special handling; genEIC.r, MS1Spectragen.r, and Stats.R are treated together). For Modular.r, replace the existing file in *both* `LipidMatch-4.2\Flow\LipidMatch_Distribution` *and* `LipidMatch-4.2\FluoroMatch_Modular` to ensure both Flow and Modular versions use your changes. For the other three scripts, place edited copies into `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`. Create a manifest file (CSV or JSON) mapping each source file to its target path(s) to document the distribution layout, then validate that all target directories exist in your installed copy. Finally, generate a directory tree or layout document to confirm the final file placement structure matches the expected configuration.

## Related tools

- **LipidMatch** (Target software distribution into which edited scripts are integrated; requires scripts placed in specific subdirectories within LipidMatch-4.2 directory structure) — https://innovativeomics.com/software
- **FluoroMatch** (Alternative target software distribution; shares Modular.r script with LipidMatch but maintains separate directory (`FluoroMatch_Modular`) requiring independent script placement) — https://innovativeomics.com/software
- **R** (Execution environment for the algorithm scripts being organized and deployed (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R are R language scripts))
- **Core-Match** (Central GitHub repository where developers edit and collaborate on main algorithm implementations before integrating into local distributions) — https://github.com/InnovativeOmics/Core-Match

## Evaluation signals

- All target directories specified in the manifest exist within the installed LipidMatch-4.2 or FluoroMatch distribution and are readable.
- Modular.r is present in both `LipidMatch-4.2\Flow\LipidMatch_Distribution` and `LipidMatch-4.2\FluoroMatch_Modular` with identical content; file timestamps or checksums confirm replacement of originals.
- genEIC.r, MS1Spectragen.r, and Stats.R are placed in `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts` and are readable by the R execution environment.
- Directory tree output shows the expected hierarchy with no missing intermediate directories; manifest file entries match actual file paths on disk.
- Software executes without 'file not found' errors for the edited scripts; if available, comparison of software output before/after reorganization shows expected behavioral differences from the edits.

## Limitations

- This skill assumes you have already downloaded and installed a base LipidMatch or FluoroMatch distribution from InnovativeOmics.com; it does not generate the distribution structure from scratch.
- No automated validation mechanism (e.g., checksum or version lock file) is mentioned in the README to verify that deployed scripts match their source versions, so manual inspection or external version control tracking is required.
- Windows-style path separators (backslash) are used in the README; Unix-like systems may require path translation or symbolic linking; cross-platform compatibility is not explicitly addressed.
- The README does not document a changelog or version tracking system for integrated edits, so comparing the integrated distribution to upstream Core-Match changes must be done manually.

## Evidence

- [readme] Install FluoroMatch or LipidMatch from InnovativeOmics.com; put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution` and `LipidMatch-4.2\FluoroMatch_Modular`: "Install FluoroMatch or LipidMatch from InnovativeOmics.com

If edited, put Modular.r into two directories (replace existing code):

`LipidMatch-4.2\Flow\LipidMatch_Distribution`

`LipidMatch-4.2\Fluor"
- [readme] Place any edited script files (genEIC.r, MS1Spectragen.r, Stats.R) into: `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`: "Place any edited script files (genEIC.r, MS1Spectragen.r, Stats.R) into:

`LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`"
- [readme] Developers can edit the main algorithms here on github as a team. Then the code needs to be integrated by placing the edited code in the correct directory from the downloaded distribution: "**Developers can edit the main algorithms here on github** as a team. Then the code needs to be integrated by placing the edited code in the correct directory from the downloaded distribution"
- [readme] For LipidMatch, FluoroMatch, and PolyMatch users should directly download from innovativeomics.com/software for the latest stable release.: "For LipidMatch, FluoroMatch, and PolyMatch **users should directly download from innovativeomics.com/software** for the latest stable release."
