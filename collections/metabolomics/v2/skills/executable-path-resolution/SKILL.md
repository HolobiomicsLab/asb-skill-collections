---
name: executable-path-resolution
description: Use when when preparing to run QCxMS2 or similar multi-tool orchestration software that depends on five or more external programs with strict version floors.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3071
  tools:
  - QCxMS2
  - xtb
  - molbar
  - geodesic_interpolate
  - CREST
  - orca
  techniques:
  - tandem-MS
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

# executable-path-resolution

## Summary

Locates and validates required external executables in the system PATH and verifies their installed versions meet minimum thresholds before a dependent scientific application (QCxMS2) can execute. This skill automates dependency verification to prevent silent failures or version-incompatible runs.

## When to use

When preparing to run QCxMS2 or similar multi-tool orchestration software that depends on five or more external programs with strict version floors. Specifically: before any QCxMS2 mass spectra calculation is attempted, or when setting up a new computational environment where xtb, CREST, molbar, orca, and geodesic_interpolate must all be available and sourced.

## When NOT to use

- The application does not invoke external programs or has no external dependencies with version constraints.
- Executables are already dynamically linked or bundled within a container/virtual environment where PATH resolution is not needed.
- User has already manually verified all dependencies offline and does not require automated validation before each run.

## Inputs

- system PATH environment variable
- executable names: xtb, CREST, molbar, orca, geodesic_interpolate
- minimum version thresholds (hardcoded: xtb >6.7.1, CREST ≥3.0.2, molbar ≥1.1.3, orca ≥6.0.0)

## Outputs

- validation report (CSV or JSON)
- executable location paths (absolute or relative)
- extracted version strings per executable
- pass/fail status per dependency
- structured summary of all results with explicit version numbers and minimum requirements

## How to apply

For each required executable (xtb, CREST, molbar, orca, geodesic_interpolate), query the system PATH using platform-specific lookup tools ('which' on Unix, 'where' on Windows) to locate the binary. Invoke the version-reporting flag (typically --version or -V) on each located executable and parse the output to extract the semantic version string. Compare the extracted version against the minimum thresholds: xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0; for geodesic_interpolate, confirm presence even if version output is unavailable. Record pass/fail for each dependency and generate a structured validation report (CSV or JSON format) with explicit version numbers found, minimum requirements, and pass/fail status. Halt QCxMS2 execution if any dependency fails validation.

## Related tools

- **xtb** (Semiempirical quantum chemistry engine; QCxMS2 invokes xtb for geometry optimizations and electronic structure in mass spectrum calculations) — https://github.com/grimme-lab/xtb
- **CREST** (Conformer ensemble sampler; QCxMS2 uses CREST to generate molecular conformer ensembles for fragmentation analysis) — https://github.com/crest-lab/crest
- **molbar** (Molecular structure manipulation and visualization utility; QCxMS2 requires it for bond breaking and molecular editing in fragmentation workflows) — https://git.rwth-aachen.de/bannwarthlab/molbar
- **orca** (Quantum chemistry package; QCxMS2 invokes orca for high-level ab initio calculations of ionization and fragmentation) — https://orcaforum.kofo.mpg.de
- **geodesic_interpolate** (Reaction pathway interpolation tool (optional); enhances geodesic path generation in molecular geometry space for fragmentation networks) — https://github.com/virtualzx-nad/geodesic-interpolate
- **QCxMS2** (Primary orchestrator; manages the entire workflow and calls this skill to validate external dependencies before mass spectrum calculation) — https://github.com/grimme-lab/QCxMS2

## Examples

```
which xtb && xtb --version && which crest && crest --version && which molbar && molbar --version && which orca && orca --version && which geodesic_interpolate
```

## Evaluation signals

- All five executable locations are successfully resolved and reported with non-empty absolute or relative paths.
- Version strings extracted from each executable match expected semantic versioning format (e.g., '6.7.2', '3.0.2').
- Each extracted version is compared correctly against its minimum threshold; pass signal returned only if xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0.
- Validation report is generated in valid CSV or JSON format with columns/keys: executable_name, path, version_found, minimum_required, status (pass/fail).
- QCxMS2 blocks calculation initiation with an error message if any dependency is missing or fails version check; successful validation allows calculation to proceed.

## Limitations

- Manual installation and sourcing of external programs is required before this skill can succeed; the skill does not install or configure dependencies automatically.
- Version reporting flag (--version or -V) must be supported by the target executable; some tools may use non-standard version output formats, requiring custom parsing.
- geodesic_interpolate lacks a standardized version reporting mechanism, so presence-only validation is performed; version check is skipped for this tool.
- The skill relies on system PATH environment variable; executables in non-standard locations or shadowed by other executables with the same name may yield false positives or negatives.
- No changelog is provided in the QCxMS2 repository, so version compatibility matrices and deprecation timelines are not documented; thresholds may become outdated.

## Evidence

- [other] QCxMS2 requires users to manually ensure installation and sourcing of five external programs with minimum version thresholds: xtb (version > 6.7.1), CREST (version >= 3.0.2), molbar (version >= 1.1.3), orca (version >= 6.0.0), and geodesic_interpolate, prior to executing any QCxMS2 calculations.: "QCxMS2 requires users to manually ensure installation and sourcing of five external programs with minimum version thresholds: xtb (version > 6.7.1), CREST (version >= 3.0.2), molbar (version >="
- [other] Query the system PATH and attempt to locate each required executable: xtb, CREST, molbar, orca, and geodesic_interpolate using standard command-line tools (e.g., 'which' on Unix or 'where' on Windows). For each located executable, invoke version-reporting flags (typically --version or -V) and parse the output to extract the version string.: "Query the system PATH and attempt to locate each required executable: xtb, CREST, molbar, orca, and geodesic_interpolate using standard command-line tools (e.g., 'which' on Unix or 'where' on"
- [other] Compare extracted versions against the minimum thresholds: xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0; for geodesic_interpolate, confirm presence without version check if version output is unavailable.: "Compare extracted versions against the minimum thresholds: xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0; for geodesic_interpolate, confirm presence without version check"
- [other] Record pass/fail outcome for each dependency and generate a structured validation report (CSV or JSON) summarizing all results with explicit version numbers found and minimum requirements.: "Record pass/fail outcome for each dependency and generate a structured validation report (CSV or JSON) summarizing all results with explicit version numbers found and minimum requirements"
- [readme] For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2: "For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2"
