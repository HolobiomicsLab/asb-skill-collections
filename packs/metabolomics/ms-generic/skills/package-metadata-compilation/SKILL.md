---
name: package-metadata-compilation
description: Use when when a package README or publication claims to install a large, fixed number of tools (e.g., 'approximately 89 tools') but does not enumerate them explicitly.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3173
  tools:
  - MetumpX-bin
  - Shell script parser (manual or automated)
  - Dependency file parser (apt, pip, conda)
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

# package-metadata-compilation

## Summary

Systematically enumerate and structure all dependencies, tools, and versions installed by a software package by parsing repository artifacts (installation scripts, manifests, dependency files). This skill recovers machine-readable metadata when package documentation does not explicitly list all components.

## When to use

When a package README or publication claims to install a large, fixed number of tools (e.g., 'approximately 89 tools') but does not enumerate them explicitly. Use this skill to reconstruct the authoritative tool manifest by inspecting installation scripts, package managers, version pinning files, or dependency declarations in the source repository.

## When NOT to use

- Input package already provides a complete, machine-readable manifest (e.g., a shipped tools.json or SBOM) — use direct parsing instead.
- Package is closed-source or repository is unavailable — this skill requires access to installation artifacts.
- Tool count is not claimed or is described as dynamic/user-configurable — enumeration will be incomplete or misleading.

## Inputs

- GitHub repository URL or local clone path
- Installation scripts (shell, Python, or other formats)
- Dependency declaration files (requirements.txt, environment files, package lists)
- README or documentation stating tool count

## Outputs

- Structured tool manifest (CSV or JSON) with columns: tool name, version, installation method, source URL, installation order
- Count validation report comparing enumerated tools to documented total
- Dependency graph or tree (optional) showing inter-tool relationships

## How to apply

Clone or access the package repository and identify all installation artifacts: shell scripts (e.g., `MetumpX_setup_enUS`), dependency manifests (requirements.txt, package.json, environment.yml, apt lists), and configuration files. Parse these artifacts line-by-line to extract tool names, pinned versions, installation methods (apt, pip, conda, git clone, manual download), and source URLs. Cross-reference extracted tools against the claimed count (e.g., ~89 for MetumpX) to identify any discrepancies. Compile results into a structured format (CSV or JSON) with columns for tool name, version, installation method, source repository/URL, and installation order where applicable. Validate that the enumerated count matches the documented total, noting any version increments across releases.

## Related tools

- **MetumpX-bin** (Source package whose installation manifest and dependencies are enumerated) — https://github.com/hasaniqbal777/MetumpX-bin
- **Shell script parser (manual or automated)** (Extracts tool names, versions, and URLs from installation scripts)
- **Dependency file parser (apt, pip, conda)** (Reads and structures declared dependencies from package manager manifests)

## Examples

```
cd MetumpX-bin && grep -rE '^(apt-get install|pip install|conda install|git clone|wget|curl)' . > tools.log && sort -u tools.log | wc -l
```

## Evaluation signals

- Enumerated tool count matches or explains any deviation from the documented total (e.g., version 2.0 claims 89 tools; v2.1 adds 14 more for 103 total).
- All tool names, versions, and source URLs are traceable to specific lines in installation scripts or dependency files (no inference).
- Structured output (CSV/JSON) is machine-readable and can be validated against a schema (tool name is non-empty string, version matches semantic versioning or 'unknown', source URL is valid URI or 'local').
- No duplicate tool entries in the manifest; if a tool appears in multiple installation paths, it is recorded once with all sources documented.
- Installation method is one of: {apt, pip, conda, git clone, manual download, local binary} and is justified by the source artifact.

## Limitations

- Installation scripts may download tools dynamically based on user choices or system state; static parsing captures only the declared or hardcoded tool set, not runtime selections.
- Version pinning may be implicit (e.g., via commit hash or tag) rather than explicit semantic versioning; version extraction requires repository inspection or build-time resolution.
- Some tools may be transitive dependencies not explicitly listed in primary installation scripts; complete enumeration may require recursive dependency resolution.
- README claims a tool count (e.g., '89 tools', '103 tools' in v2.1) but does not define what constitutes a 'tool' — a library, binary, R package, and plugin may all be conflated under one count.
- Repository may lack a changelog or version history pinning tool additions to specific releases; the relationship between version numbers and tool count is documented in this paper's Revision History but may be incomplete or post-hoc.

## Evidence

- [intro] MetumpX is designed to download and install approximately 89 tools for untargeted metabolomics mass spectrometry pipelines on Ubuntu systems.: "MetumpX is a Ubuntu based software package that facilitate easy download and installation of about 89 tools related to standard Untargeted Metabolomics Mass Spectrometry pipeline."
- [other] The workflow requires parsing repository structure including installation scripts and dependency files.: "Parse the repository structure (installation scripts, dependency files, package manifests) to identify all enumerated tool names, versions, and installation sources."
- [readme] Version 2.0 added 39 tools to the initial 50 (total 89); version 2.1 added 14 more (total 103).: "**Version 1.0** - 50 Tools... **Version 2.0** - 39 Tools added (Total 89 Tools)... **Version 2.1** - 15 Tools added (Total 103 Tools)"
- [other] Output should be compiled into a structured, machine-readable format with tool metadata.: "Compile the extracted tool list into a structured CSV or JSON manifest with columns for tool name, version (if specified), installation method, and source repository or URL."
- [other] Validation requires comparing enumerated count to the documented total.: "Validate that the enumerated count matches the documented ~89 tools."
