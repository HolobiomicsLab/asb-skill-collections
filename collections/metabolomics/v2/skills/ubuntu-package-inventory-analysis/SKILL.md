---
name: ubuntu-package-inventory-analysis
description: Use when when you have a Ubuntu-based software package (e.g., MetumpX) that advertises bundling a specific number of tools (~89) but the individual tool names, versions, installation sources, and installation methods are not enumerated in the README or primary documentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MetumpX
  - Git
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btz765
  title: MetumpX untargeted MS support package
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metumpx_untargeted_ms_support_package_cq
    doi: 10.1093/bioinformatics/btz765
    title: MetumpX untargeted MS support package
  dedup_kept_from: coll_metumpx_untargeted_ms_support_package_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btz765
  all_source_dois:
  - 10.1093/bioinformatics/btz765
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Ubuntu Package Inventory Analysis

## Summary

Systematically enumerate, document, and validate the complete manifest of software tools bundled in an Ubuntu-based installation package by parsing repository structure, dependency files, and installation scripts. This skill is essential when a package claims to bundle a large toolset (e.g., ~89 tools) but the enumerated list is not explicitly published in documentation.

## When to use

When you have a Ubuntu-based software package (e.g., MetumpX) that advertises bundling a specific number of tools (~89) but the individual tool names, versions, installation sources, and installation methods are not enumerated in the README or primary documentation. This skill applies when you need to reconstruct the complete, validated tool manifest for reproducibility, citation, dependency tracking, or validation against the claimed tool count.

## When NOT to use

- The tool list is already fully enumerated and validated in the package README or peer-reviewed publication — use direct reference instead.
- The package is closed-source or the installation scripts are obfuscated — manual reverse-engineering is not feasible.
- The goal is to install or run the package, not to audit or document its contents — use the standard installation workflow instead.

## Inputs

- GitHub repository URL (e.g., hasaniqbal777/MetumpX-bin)
- Installation scripts (e.g., MetumpX_setup_enUS shell script)
- Dependency files and package manifests
- README documentation
- Supplementary docs (e.g., User Guide PDF)
- Revision history / changelog

## Outputs

- Structured tool manifest (CSV or JSON) with columns: tool_name, version, installation_method, source_url, installation_order
- Validation report comparing enumerated tool count to documented count
- Installation dependency graph (if applicable)
- Annotated README or supplementary documentation identifying tool boundaries

## How to apply

Clone or access the package repository from GitHub. Parse the installation scripts (e.g., MetumpX_setup_enUS), dependency manifests, package configuration files, and any embedded tool lists or download sources. Extract each tool's name, version (if specified), installation method (source compilation, package manager, precompiled binary, etc.), and source repository or URL. Compile the extracted data into a structured format (CSV or JSON) with columns for tool name, version, installation method, and source. Validate the final enumerated tool count against the package's documented tool count (e.g., confirm ~89 tools; note version history changes such as v1.0=50 tools, v2.0=89 tools, v2.1=103 tools). Use manual expert review to cross-check the manifest against the package's actual installation behavior and any supplementary documentation (e.g., User Guide PDF).

## Related tools

- **MetumpX** (Ubuntu-based package whose tool inventory is being reconstructed and validated) — https://github.com/hasaniqbal777/MetumpX-bin
- **Git** (Version control system used to clone and access the MetumpX repository for local parsing)

## Examples

```
git clone https://github.com/hasaniqbal777/MetumpX-bin && cd MetumpX-bin && grep -r 'wget\|apt-get\|git clone' MetumpX_setup_enUS | awk '{print $NF}' > tool_manifest.txt
```

## Evaluation signals

- Enumerated tool count matches the package's documented count within the cited version (e.g., v2.0 = 89 tools, v2.1 = 103 tools as stated in Revision History).
- All tools in the manifest have a non-empty name, installation method, and source URL or installation source.
- Installation scripts (e.g., MetumpX_setup_enUS) can be traced to every tool entry; no tools are missing from the script parsing.
- Version numbers (if present) are consistent with the repository release tags and supplementary documentation.
- Manual expert review confirms that the manifest reflects the actual tools downloaded and installed during a test run on Ubuntu.

## Limitations

- The MetumpX README does not enumerate individual tool names or versions — the manifest must be reconstructed from opaque installation scripts, which may fail if scripts are heavily obfuscated or dynamically generated.
- Tool versions and installation sources may change between package releases; the manifest is version-specific and must be regenerated for each release.
- The README does not provide a changelog for individual tools, only package-level version history (v1.0 → v2.0 → v2.1); tool-level dependency and version tracking requires deep parsing of installation scripts.
- Installation dialog boxes (mentioned in README: 'Follow the on-screen dialogue boxes for installation') may allow users to selectively install subsets of tools, meaning the final installed tool count may differ from the documented ~89.

## Evidence

- [readme] MetumpX is a Ubuntu based software package that facilitate easy download and installation of about 89 tools related to standard Untargeted Metabolomics Mass Spectrometry pipeline.: "MetumpX is a Ubuntu based software package that facilitate easy download and installation of about 89 tools related to standard Untargeted Metabolomics Mass Spectrometry pipeline."
- [other] Parse the repository structure (installation scripts, dependency files, package manifests) to identify all enumerated tool names, versions, and installation sources.: "Parse the repository structure (installation scripts, dependency files, package manifests) to identify all enumerated tool names, versions, and installation sources."
- [other] Compile the extracted tool list into a structured CSV or JSON manifest with columns for tool name, version (if specified), installation method, and source repository or URL.: "Compile the extracted tool list into a structured CSV or JSON manifest with columns for tool name, version (if specified), installation method, and source repository or URL."
- [other] Validate that the enumerated count matches the documented ~89 tools.: "Validate that the enumerated count matches the documented ~89 tools."
- [readme] Version 1.0 - 50 Tools; Version 2.0 - 39 Tools added (Total 89 Tools); Version 2.1 - 15 Tools added (Total 103 Tools): "Version 1.0 - 50 Tools; Version 2.0 - 39 Tools added (Total 89 Tools); Version 2.1 - 15 Tools added (Total 103 Tools)"
