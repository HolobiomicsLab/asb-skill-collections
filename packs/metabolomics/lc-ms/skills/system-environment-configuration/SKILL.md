---
name: system-environment-configuration
description: Use when you need to execute a complex computational chemistry workflow (QCxMS2) that depends on multiple external semiempirical and ab initio quantum chemistry packages.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0176
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# system-environment-configuration

## Summary

Verify and validate that all required external dependencies are installed with minimum specified versions before executing a multi-tool computational workflow. This skill ensures that QCxMS2 can locate and invoke five external programs (xtb, CREST, molbar, orca, geodesic_interpolate) at runtime by systematically checking their presence, extracting version strings, and comparing against documented thresholds.

## When to use

Apply this skill when you need to execute a complex computational chemistry workflow (QCxMS2) that depends on multiple external semiempirical and ab initio quantum chemistry packages. Trigger this skill before attempting any mass spectra calculations or conformer ensemble sampling, especially in new environments (fresh cluster login, new workstation, containerized deployment) where external tool availability is uncertain.

## When NOT to use

- If dependencies are already embedded or statically linked into a monolithic QCxMS2 binary; version checking is unnecessary for self-contained distributions.
- When running QCxMS2 inside a containerized environment (Docker, Singularity) where the container image provider has guaranteed pre-installation and versioning; defer to container metadata.
- If the computational task only uses a subset of QCxMS2 features that do not require all five external programs (e.g., some analyses may not invoke ORCA or geodesic_interpolate); validate only the actually required subset.

## Inputs

- System PATH environment variable (string)
- Installed executable locations for xtb, CREST, molbar, orca, geodesic_interpolate
- Minimum version thresholds specification (JSON or config file with tool names and semantic version constraints)

## Outputs

- Structured validation report (CSV or JSON) documenting each dependency's name, detected version, minimum requirement, and pass/fail status
- Boolean exit code or validation state (all-pass vs. any-fail)
- Human-readable summary of missing or out-of-date dependencies suitable for user error messages

## How to apply

Construct a systematic dependency validation workflow: (1) Query the system PATH using platform-native tools ('which' on Unix/Linux/macOS, 'where' on Windows) to locate each required executable (xtb, CREST, molbar, orca, geodesic_interpolate). (2) For each located executable, invoke its version-reporting flag (typically --version or -V) and parse the output to extract the semantic version string. (3) Compare extracted versions against documented minimum thresholds: xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0; for geodesic_interpolate (optional), confirm presence without strict version enforcement if version output is unavailable. (4) Aggregate pass/fail outcomes for each dependency and generate a structured validation report (CSV or JSON format) that lists each tool's name, found version, minimum requirement, and pass/fail status. (5) Only proceed with QCxMS2 calculations if all mandatory dependencies (xtb, CREST, molbar, orca) pass validation; optional tools like geodesic_interpolate may be flagged as warnings.

## Related tools

- **xtb** (Semiempirical extended tight-binding quantum mechanical calculations for structure optimization and frequency analysis; QCxMS2 requires version > 6.7.1 (bleeding edge)) — https://github.com/grimme-lab/xtb
- **CREST** (Conformer-rotamer ensemble sampling tool for automated molecular structure exploration; QCxMS2 requires version ≥ 3.0.2) — https://github.com/crest-lab/crest
- **molbar** (Molecular barrier calculation and potential energy surface analysis; QCxMS2 requires version ≥ 1.1.3) — https://git.rwth-aachen.de/bannwarthlab/molbar
- **orca** (Ab initio quantum chemistry engine for high-level electronic structure calculations; QCxMS2 requires version ≥ 6.0.0) — https://orcaforum.kofo.mpg.de
- **geodesic_interpolate** (Optional tool for geometric interpolation and reaction pathway refinement (version 1.0.0); no strict version threshold enforced) — https://github.com/virtualzx-nad/geodesic-interpolate

## Evaluation signals

- All mandatory dependencies (xtb, CREST, molbar, orca) report detected versions that satisfy minimum thresholds; validation report shows pass status for each.
- Validation report is generated in valid JSON or CSV format with no malformed entries, and can be parsed by downstream workflow orchestrators.
- When a dependency is missing or below minimum version, the validation report clearly flags it with the tool name, detected version (or 'not found'), and minimum requirement, enabling targeted user remediation.
- QCxMS2 executable successfully invokes at least one downstream dependency (e.g., `xtb --version` returns version string matching detected version in validation report), confirming that PATH sourcing and version extraction logic are correct.
- Validation completes without timeout or hanging, even when searching PATH across network-mounted file systems or slow cluster storage.

## Limitations

- Version detection relies on tools reporting versions via standard flags (--version or -V); non-standard or undocumented version reporting formats will cause extraction to fail silently or report 'unknown version'.
- The skill assumes tools are invoked via standalone executables in the system PATH; tools installed as Python packages, conda environments, or module-managed software may not be detected by standard 'which' or 'where' queries.
- Semantic version parsing assumes standard MAJOR.MINOR.PATCH format (e.g., '6.7.1'); custom version strings (e.g., alpha/beta tags, commit hashes, build metadata) may fail comparison logic and require manual intervention.
- Minimum version thresholds are fixed at skill definition time (xtb > 6.7.1, etc.); if upstream tool releases introduce breaking changes or security patches, thresholds must be manually updated and re-validated.
- The skill does not verify tool functionality (e.g., whether xtb can actually run) or library compatibility (e.g., whether ORCA's MPI build matches the user's HPC environment); it only checks presence and version strings.

## Evidence

- [readme] For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2: "For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2"
- [other] QCxMS2 requires users to manually ensure installation and sourcing of five external programs with minimum version thresholds: xtb (version > 6.7.1), CREST (version >= 3.0.2), molbar (version >= 1.1.3), orca (version >= 6.0.0), and geodesic_interpolate, prior to executing any QCxMS2 calculations.: "QCxMS2 requires users to manually ensure installation and sourcing of five external programs with minimum version thresholds: xtb (version > 6.7.1), CREST (version >= 3.0.2), molbar (version >="
- [other] For each located executable, invoke version-reporting flags (typically --version or -V) and parse the output to extract the version string. Compare extracted versions against the minimum thresholds: "For each located executable, invoke version-reporting flags (typically --version or -V) and parse the output to extract the version string. Compare extracted versions against the minimum thresholds"
- [other] Query the system PATH and attempt to locate each required executable: xtb, CREST, molbar, orca, and geodesic_interpolate using standard command-line tools (e.g., 'which' on Unix or 'where' on Windows).: "Query the system PATH and attempt to locate each required executable: xtb, CREST, molbar, orca, and geodesic_interpolate using standard command-line tools (e.g., 'which' on Unix or 'where' on Windows)"
- [other] Record pass/fail outcome for each dependency and generate a structured validation report (CSV or JSON) summarizing all results with explicit version numbers found and minimum requirements.: "Record pass/fail outcome for each dependency and generate a structured validation report (CSV or JSON) summarizing all results with explicit version numbers found and minimum requirements"
