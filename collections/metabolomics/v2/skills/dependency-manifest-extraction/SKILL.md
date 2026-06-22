---
name: dependency-manifest-extraction
description: Use when a bioinformatics package claims to install a large number of tools (e.g., ~89 for untargeted metabolomics pipelines) but the article or main documentation does not enumerate them explicitly.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - MetumpX (installation framework)
  - Manual expert review
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
---

# dependency-manifest-extraction

## Summary

Extract, enumerate, and validate the complete list of software tools and their versions that a bioinformatics package downloads and installs, producing a structured manifest suitable for reproducibility and dependency auditing. This skill surfaces hidden tool inventories from installation scripts and repository structures when they are not explicitly documented.

## When to use

A bioinformatics package claims to install a large number of tools (e.g., ~89 for untargeted metabolomics pipelines) but the article or main documentation does not enumerate them explicitly. You need to reconstruct the tool manifest from installation scripts, package managers, or repository structure to verify the count, identify versions, trace sources, and enable reproducible deployment.

## When NOT to use

- The package already publishes an explicit, version-pinned dependency manifest (e.g., lock file or bill-of-materials) — use that directly instead of reverse-engineering from scripts.
- The package is purely interpreted or web-based with no compiled tool dependencies — extraction workflow targets compiled or containerized bioinformatics stacks.
- Installation scripts are obfuscated, proprietary, or inaccessible — manifest extraction requires parseable source code or dependency declarations.

## Inputs

- GitHub repository clone or directory with installation scripts
- Installation automation files (shell scripts, setup executables, Dockerfiles)
- Dependency declaration files (requirements.txt, environment.yml, apt package lists, .json manifests)
- Revision history or changelog documenting tool additions across releases
- Project README or supplementary documentation with version metadata

## Outputs

- Structured tool manifest (CSV or JSON) with columns: tool_name, version, installation_method, source_repository_or_url
- Enumerated count of tools with validation against claimed total
- Gap report documenting missing version metadata, broken URLs, or count discrepancies
- Installation method classification (source download, package manager, git clone, etc.)

## How to apply

Clone or access the package repository and parse installation automation scripts (e.g., MetumpX_setup_enUS), dependency declaration files (package lists, conda environments, or apt manifests), and version pinning records. Extract tool name, version (if specified), installation method (source URL, package manager, or git repo), and source repository for each entry. Compile findings into a structured manifest (CSV or JSON) with consistent column ordering: tool_name, version, installation_method, source_url. Validate the extracted count against the documented claim (~89 tools) and cross-check version compatibility by inspecting revision history and release notes. Flag any discrepancies between claimed and enumerated tool counts, missing version metadata, or broken source URLs as gaps requiring manual expert review.

## Related tools

- **MetumpX (installation framework)** (Source package containing installation scripts and dependency declarations to be parsed for tool enumeration) — https://github.com/hasaniqbal777/MetumpX-bin
- **Manual expert review** (Validation and gap-filling step to reconcile extracted manifest against source scripts and resolve ambiguous dependency declarations)

## Examples

```
# Clone MetumpX repository
git clone https://github.com/hasaniqbal777/MetumpX-bin
cd MetumpX-bin
# Parse installation script (requires manual reverse-engineering or decompilation)
# strings MetumpX_setup_enUS | grep -E '(tool|package|install)' > candidate_tools.txt
# Then compile extracted names into manifest.json with tool name, version, source_url fields
```

## Evaluation signals

- Extracted tool count matches or closely approximates the documented claim (e.g., ~89 for MetumpX) with documented reasons for any variance (e.g., platform-specific subsets).
- All enumerated tools have associated installation method and source URL traceable to repository content or package manager catalogs.
- Version metadata is populated for all tools (or justified absence documented, e.g., 'latest' or 'system package').
- Manifest structure is machine-readable (valid CSV/JSON schema) with no missing required columns.
- Manual spot-check of 5–10 randomly selected tools confirms that source URLs are accessible and installation method is verifiable against actual scripts.

## Limitations

- MetumpX README does not enumerate individual tool names or versions in the main documentation; extraction requires parsing binary installation script (MetumpX_setup_enUS) which may be difficult to reverse-engineer without source.
- Revision history indicates tool count changed across versions (50 → 89 → 103 tools) but does not name which tools were added or removed; gaps in changlog limit traceability.
- Installation script uses on-screen dialogue boxes, making automated parsing of tool selections and conditional dependencies challenging.
- Platform specificity: MetumpX is Ubuntu-only; extracted manifest may not reflect platform-specific tool subsets for other operating systems or virtualization environments.
- No changelog or version pinning file found in available documentation; tool versions may float or be implicit in package manager metadata.

## Evidence

- [readme] MetumpX is a Ubuntu based software package that facilitate easy download and installation of about 89 tools related to standard Untargeted Metabolomics Mass Spectrometry pipeline.: "MetumpX is a Ubuntu based software package that facilitate easy download and installation of about 89 tools related to standard Untargeted Metabolomics Mass Spectrometry pipeline."
- [other] Parse the repository structure (installation scripts, dependency files, package manifests) to identify all enumerated tool names, versions, and installation sources.: "Parse the repository structure (installation scripts, dependency files, package manifests) to identify all enumerated tool names, versions, and installation sources."
- [other] Compile the extracted tool list into a structured CSV or JSON manifest with columns for tool name, version (if specified), installation method, and source repository or URL.: "Compile the extracted tool list into a structured CSV or JSON manifest with columns for tool name, version (if specified), installation method, and source repository or URL."
- [readme] Version 2.0 - MetumpX initial release - 39 Tools added (Total 89 Tools) - Pipeline Correction - Bug fixes: "Version 2.0 - MetumpX initial release - 39 Tools added (Total 89 Tools)"
