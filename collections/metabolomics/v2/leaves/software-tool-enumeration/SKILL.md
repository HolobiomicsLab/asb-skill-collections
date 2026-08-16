---
name: software-tool-enumeration
description: Use when a software package claims to bundle or install a specific number
  of tools (documented or approximate) but the tool names, versions, and sources are
  not enumerated in the primary README or documentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3365
  tools:
  - MetumpX_setup_enUS
  - MetumpX-bin repository
  techniques:
  - mass-spectrometry
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# software-tool-enumeration

## Summary

Systematically enumerate, document, and validate the complete set of bioinformatic tools bundled in a software package by parsing installation scripts, dependency manifests, and repository structure. This skill is essential when a package claims to bundle a large number of tools (e.g., ~89 for metabolomics pipelines) but the README or documentation does not list them explicitly.

## When to use

A software package claims to bundle or install a specific number of tools (documented or approximate) but the tool names, versions, and sources are not enumerated in the primary README or documentation. You need to produce a structured manifest for reproducibility, dependency tracking, or validation purposes.

## When NOT to use

- The package's tool list is already fully enumerated and validated in the README or a manifest file distributed with the package.
- The package does not claim a specific tool count, or the claim is only aspirational and not tied to reproducible installation.
- You need to execute or test the installation yourself; this skill focuses on static manifest extraction, not installation verification.

## Inputs

- GitHub repository URL (or local clone path)
- Installation script(s) (e.g., shell scripts named *setup*, *install*)
- Dependency manifests (e.g., requirements.txt, package lists, apt sources)
- README and documentation files
- Version history or changelog (if available)

## Outputs

- Structured tool manifest (CSV, JSON, or TSV with columns: tool_name, version, installation_method, source_url)
- Tool count validation report (enumerated vs. advertised count)
- Installation method summary (e.g., '42 tools via apt, 30 via pip, 17 from source')
- Missing or incomplete tool entries (if any)

## How to apply

Clone or access the target repository and parse all installation scripts, package dependency files (e.g., package manager manifests, shell scripts), and documented version information to extract tool identifiers, versions, installation methods, and source URLs. Compile extracted entries into a structured format (CSV, JSON, or TSTable) with consistent columns: tool name, version (or version spec), installation method (e.g., apt, pip, from-source), and source repository or URL. Cross-reference the final count against the package's advertised tool count; reconcile any discrepancies by examining changelog or version history files. Validate schema consistency and that all tools are reachable or documented in the package's supported installation environment (e.g., Ubuntu LTS versions listed in the README).

## Related tools

- **MetumpX_setup_enUS** (Primary installation script that orchestrates download and installation of the ~89 bundled tools on Ubuntu systems) — https://github.com/hasaniqbal777/MetumpX-bin
- **MetumpX-bin repository** (Source repository containing all installation logic, dependency files, and package structure to be parsed) — https://github.com/hasaniqbal777/MetumpX-bin

## Examples

```
cd /path/to/MetumpX-bin && grep -r 'apt-get install\|pip install\|wget\|git clone' MetumpX_setup_enUS | sort | uniq > tools_manifest.txt && wc -l tools_manifest.txt
```

## Evaluation signals

- Enumerated tool count matches or is reconciled against the advertised count (~89 tools in MetumpX v2.0, 103 in v2.1); document any delta with rationale.
- All extracted tools have documented source URLs or installation methods that are reachable and valid.
- Manifest schema is consistent across all rows (no missing columns, no formatting inconsistencies).
- Version strings are parseable and consistent with the package manager or source repository conventions (e.g., semver, pinned commit hashes).
- Installation methods are traceable to documented Ubuntu package managers or official repositories (apt, pip, GitHub releases, conda, etc.).

## Limitations

- The MetumpX README does not enumerate individual tool names; the skill output depends entirely on parsing installation scripts, which may use dynamic tool lists or external configuration not visible in the repository.
- Tool versions may not be explicitly pinned in installation scripts, making version tracking incomplete.
- The changelog notes that tool counts changed between versions (50 in v1.0, 89 in v2.0, 103 in v2.1), but no detailed migration or removal log is provided, limiting validation of consistency across versions.
- Windows support is mentioned as virtualization-based (per User Guide), so enumeration may not be complete or consistent across operating systems.

## Evidence

- [readme] MetumpX is a Ubuntu based software package that facilitate easy download and installation of about 89 tools related to standard Untargeted Metabolomics Mass Spectrometry pipeline.: "MetumpX is a Ubuntu based software package that facilitate easy download and installation of about 89 tools"
- [other] Parse the repository structure (installation scripts, dependency files, package manifests) to identify all enumerated tool names, versions, and installation sources.: "Parse the repository structure (installation scripts, dependency files, package manifests) to identify all enumerated tool names, versions, and installation sources."
- [other] Compile the extracted tool list into a structured CSV or JSON manifest with columns for tool name, version (if specified), installation method, and source repository or URL.: "Compile the extracted tool list into a structured CSV or JSON manifest with columns for tool name, version (if specified), installation method, and source repository or URL."
- [readme] Version 2.0: MetumpX initial release, 39 Tools added (Total 89 Tools): "Version 2.0: MetumpX initial release, 39 Tools added (Total 89 Tools)"
- [readme] Version 2.1: 15 Tools added (Total 103 Tools): "Version 2.1: 15 Tools added (Total 103 Tools)"
