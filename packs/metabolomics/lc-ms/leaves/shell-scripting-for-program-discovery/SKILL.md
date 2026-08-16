---
name: shell-scripting-for-program-discovery
description: Use when a scientific application (such as QCxMS2) requires multiple external programs with specific version constraints and you need to programmatically verify their presence and compatibility before executing calculations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3363
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - QCxMS2
  - xtb
  - molbar
  - geodesic_interpolate
  - CREST
  - orca
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/jasms.5c00234
  title: QCxMS2
evidence_spans:
- Program package for the quantum mechanical calculation of EI mass spectra using automated reaction network exploration
- '**xtb** (version > 6.7.1 - bleeding edge version)'
- '**molbar** (version >= 1.1.3)'
- '**geodesic_interpolate** (version'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qcxms2_cq
    doi: 10.1021/jasms.5c00234
    title: QCxMS2
  dedup_kept_from: coll_qcxms2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00234
  all_source_dois:
  - 10.1021/jasms.5c00234
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# shell-scripting-for-program-discovery

## Summary

Construct and execute shell scripts to locate external program executables in the system PATH and validate their installed versions against minimum thresholds. This skill ensures that prerequisite dependencies (xtb, CREST, molbar, orca, geodesic_interpolate) meet version requirements before a computational workflow like QCxMS2 can proceed.

## When to use

Apply this skill when a scientific application (such as QCxMS2) requires multiple external programs with specific version constraints and you need to programmatically verify their presence and compatibility before executing calculations. Use it as a pre-flight validation step in automated computational pipelines to prevent downstream failures due to missing or incompatible dependencies.

## When NOT to use

- When external programs are statically linked or bundled within the main application binary—program discovery is unnecessary if all dependencies are self-contained.
- When the computational workflow has no external dependencies or runs in a containerized environment where all versions are pre-validated and immutable.
- When version checking is irrelevant to the analysis—e.g., when only the executable path is needed and compatibility is not a concern.

## Inputs

- List of required external program names (e.g., xtb, CREST, molbar, orca, geodesic_interpolate)
- Minimum version thresholds for each program (e.g., xtb > 6.7.1, CREST ≥ 3.0.2)
- System PATH environment variable
- Shell execution environment (bash, zsh, sh)

## Outputs

- Structured validation report (JSON or CSV) documenting each dependency's validation status
- Explicit version strings extracted from each located executable
- Pass/fail outcome per dependency
- Boolean flag indicating whether all dependencies are satisfied (suitable for conditional workflow entry)

## How to apply

Query the system PATH using command-line tools (e.g., 'which' on Unix/Linux or 'where' on Windows) to locate each required executable. For each found program, invoke its version-reporting flag (typically --version or -V) and parse the output to extract the semantic version string. Compare extracted versions against documented minimum thresholds using string comparison or semantic versioning logic: xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0; for tools without available version output (e.g., geodesic_interpolate), confirm executable presence only. Aggregate results into a structured validation report (CSV or JSON format) that records pass/fail status, found version, and minimum requirement for each dependency. Halt execution or warn the user if any dependency fails validation.

## Related tools

- **xtb** (External dependency for semiempirical tight-binding calculations in QCxMS2; requires version > 6.7.1) — https://github.com/grimme-lab/xtb
- **CREST** (External dependency for conformer/rotamer ensemble sampling in QCxMS2; requires version ≥ 3.0.2) — https://github.com/crest-lab/crest
- **molbar** (External dependency for molecular bar calculations in QCxMS2; requires version ≥ 1.1.3) — https://git.rwth-aachen.de/bannwarthlab/molbar
- **orca** (External dependency for quantum mechanical calculations in QCxMS2; requires version ≥ 6.0.0)
- **geodesic_interpolate** (Optional external dependency for geodesic path interpolation in QCxMS2; version check skipped if unavailable) — https://github.com/virtualzx-nad/geodesic-interpolate
- **QCxMS2** (Scientific application requiring validation of all listed external dependencies before execution) — https://github.com/grimme-lab/QCxMS2

## Examples

```
which xtb && xtb --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' && which crest && crest --version | head -1
```

## Evaluation signals

- All required executables are successfully located in the system PATH; the output report contains non-empty paths for each.
- Version strings extracted from --version or -V output parse correctly and are semantically comparable (e.g., 6.8.0 > 6.7.1).
- Validation logic correctly identifies passing dependencies (versions meeting or exceeding thresholds) and failing ones (below minimum).
- The structured output report (JSON or CSV) contains all required fields: program name, found version, minimum required version, and pass/fail status.
- If any dependency fails validation, the script halts or returns a non-zero exit code, preventing downstream execution of QCxMS2 calculations.

## Limitations

- Version-reporting flags and output formats vary across programs; some programs may not support --version or -V, requiring manual specification of version-query syntax or skipping version checks (as with geodesic_interpolate).
- The approach assumes programs are on the system PATH; statically linked or non-standard installation paths require explicit PATH modification or path hints.
- Semantic version parsing must handle variability in version string formats (e.g., '6.7.1', 'v6.7.1', '6.7.1-rc1'); simple string comparison may fail for complex version schemes.
- Cross-platform differences (e.g., 'which' vs. 'where') require separate script implementations or wrapper logic for portability.
- The QCxMS2 documentation notes that users must manually ensure installation and sourcing of external programs; the script cannot resolve missing programs, only report their status.

## Evidence

- [other] For each located executable, invoke version-reporting flags (typically --version or -V) and parse the output to extract the version string.: "For each located executable, invoke version-reporting flags (typically --version or -V) and parse the output to extract the version string."
- [other] Compare extracted versions against the minimum thresholds: xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0: "Compare extracted versions against the minimum thresholds: xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0"
- [readme] For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2: "For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2"
- [other] Query the system PATH and attempt to locate each required executable: xtb, CREST, molbar, orca, and geodesic_interpolate using standard command-line tools (e.g., 'which' on Unix or 'where' on Windows).: "Query the system PATH and attempt to locate each required executable: xtb, CREST, molbar, orca, and geodesic_interpolate using standard command-line tools (e.g., 'which' on Unix or 'where' on"
- [other] Record pass/fail outcome for each dependency and generate a structured validation report (CSV or JSON) summarizing all results with explicit version numbers found and minimum requirements.: "Record pass/fail outcome for each dependency and generate a structured validation report (CSV or JSON) summarizing all results with explicit version numbers found and minimum requirements."
