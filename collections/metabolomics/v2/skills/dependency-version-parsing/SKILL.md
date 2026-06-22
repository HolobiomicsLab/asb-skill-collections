---
name: dependency-version-parsing
description: 'Use when before launching a multi-tool computational workflow (e.g., QCxMS2 mass spectra calculations) that depends on external programs with version-sensitive APIs or features. Apply this skill when: (1) the workflow has explicit minimum version requirements for one or more dependencies;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - QCxMS2
  - xtb
  - molbar
  - geodesic_interpolate
  - CREST
  - orca
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
---

# dependency-version-parsing

## Summary

Validate that required external program dependencies are installed with minimum version thresholds before computational workflow execution. This skill locates executables in system PATH, queries their version strings, parses version numbers, compares against specified minima, and generates a structured validation report.

## When to use

Before launching a multi-tool computational workflow (e.g., QCxMS2 mass spectra calculations) that depends on external programs with version-sensitive APIs or features. Apply this skill when: (1) the workflow has explicit minimum version requirements for one or more dependencies; (2) those dependencies are not package-managed or containerized; (3) users have manual responsibility for installation and sourcing; (4) version mismatches would cause silent failures or incorrect results rather than clear error messages.

## When NOT to use

- Dependencies are already containerized (Docker, Singularity, Conda environment) — use container-native version inspection instead.
- Workflow uses a package manager (conda, modules, environment manager) that guarantees version compatibility — delegate to package manager lock file validation.
- Version differences are backwards-compatible within a wide range and workflow is agnostic to version — apply lighter version-warning instead of hard gate.

## Inputs

- system PATH environment variable
- list of required external program names with version thresholds (e.g., [{'name': 'xtb', 'min_version': '6.7.1', 'operator': '>'}, {'name': 'CREST', 'min_version': '3.0.2', 'operator': '>='}])
- optional: known installation directories or shell sourcing scripts

## Outputs

- structured validation report (CSV or JSON) with columns: [program_name, min_required_version, found_version, version_check_operator, pass_fail_status, absolute_path_to_executable]
- exit code (0 = all hard requirements passed, non-zero = at least one hard requirement failed)
- human-readable summary log (stdout/stderr)

## How to apply

For each required dependency, execute a three-stage validation pipeline: (1) Locate the executable by querying system PATH using platform-appropriate tools ('which' on Unix, 'where' on Windows); (2) Invoke the executable with a version-reporting flag (commonly --version or -V), capture and parse stdout to extract the semantic version string (e.g., '6.8.0' from 'xtb version 6.8.0'); (3) Parse the extracted version into comparable components (major.minor.patch) and compare each component numerically against the minimum threshold (e.g., xtb > 6.7.1 means reject 6.7.1 and earlier, accept 6.7.2 and later). Record pass/fail outcome and the located version for each dependency. Aggregate results into a structured report (CSV or JSON) listing each dependency name, minimum required version, found version (or 'NOT FOUND'), and pass/fail status. The report becomes the gate: proceed to workflow execution only if all hard requirements pass; optional dependencies (e.g., geodesic_interpolate) may pass if executable is present even if version check fails.

## Related tools

- **QCxMS2** (workflow orchestrator requiring validated external dependencies before execution) — https://github.com/grimme-lab/QCxMS2
- **xtb** (external quantum mechanical method backend with strict minimum version > 6.7.1) — https://github.com/grimme-lab/xtb
- **CREST** (conformer sampling tool dependency with minimum version >= 3.0.2) — https://github.com/crest-lab/crest
- **molbar** (fragmentation tool dependency with minimum version >= 1.1.3) — https://git.rwth-aachen.de/bannwarthlab/molbar
- **orca** (external electronic structure backend with minimum version >= 6.0.0)
- **geodesic_interpolate** (optional trajectory interpolation tool; version check skipped if version unavailable) — https://github.com/virtualzx-nad/geodesic-interpolate

## Examples

```
#!/bin/bash
for prog in xtb CREST molbar orca; do
  if cmd=$(which $prog 2>/dev/null); then
    ver=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
    echo "$prog: found=$ver cmd=$cmd"
  else
    echo "$prog: NOT FOUND"
  fi
done
```

## Evaluation signals

- All five required executables (xtb, CREST, molbar, orca, geodesic_interpolate) are successfully located in PATH or known installation directories.
- Version strings are extracted and parsed without errors; each version compares as a valid semantic version (major.minor.patch or major.minor).
- For xtb, located version is > 6.7.1 (e.g., 6.8.0 passes, 6.7.1 or 6.7.0 fails); for CREST, located version is >= 3.0.2; for molbar, >= 1.1.3; for orca, >= 6.0.0.
- Validation report is generated in valid CSV or JSON format, machine-parseable, with no null or ambiguous values in critical columns.
- Final exit code is 0 if and only if all five hard requirements pass; any failed requirement results in non-zero exit code and clear error message identifying the failed dependency and its found version.

## Limitations

- Version extraction assumes standard --version or -V flags and GNU/POSIX output format; non-standard or proprietary version reporters may fail silently or produce unparseable output.
- Comparison logic is numeric and assumes semantic versioning (major.minor.patch); pre-release or build-metadata suffixes (e.g., '6.8.0-rc1', '6.8.0+build123') may cause parsing failures unless explicitly normalized.
- Locating executables relies on PATH; executables installed in non-standard locations without explicit full path or shell aliases will not be found.
- geodesic_interpolate version check is non-blocking (optional); workflow may proceed even if version is not queryable, potentially masking incompatibilities at runtime.
- No detection of dynamic library version mismatches (e.g., incompatible GLIBC, OpenBLAS, or MKL versions linked to an executable) — only reports executable presence and self-reported version.

## Evidence

- [readme] For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2: xtb (version > 6.7.1), CREST (version >= 3.0.2), molbar (version >= 1.1.3), orca (version >= 6.0.0), geodesic_interpolate: "For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2"
- [other] QCxMS2 requires users to manually ensure installation and sourcing of five external programs with minimum version thresholds: xtb (version > 6.7.1), CREST (version >= 3.0.2), molbar (version >= 1.1.3), orca (version >= 6.0.0), and geodesic_interpolate: "QCxMS2 requires users to manually ensure installation and sourcing of five external programs with minimum version thresholds"
- [other] Query the system PATH and attempt to locate each required executable: xtb, CREST, molbar, orca, and geodesic_interpolate using standard command-line tools (e.g., 'which' on Unix or 'where' on Windows). For each located executable, invoke version-reporting flags (typically --version or -V) and parse the output to extract the version string.: "For each located executable, invoke version-reporting flags (typically --version or -V) and parse the output to extract the version string"
- [other] Compare extracted versions against the minimum thresholds: xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0; for geodesic_interpolate, confirm presence without version check if version output is unavailable.: "Compare extracted versions against the minimum thresholds: xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0"
- [other] Record pass/fail outcome for each dependency and generate a structured validation report (CSV or JSON) summarizing all results with explicit version numbers found and minimum requirements.: "Record pass/fail outcome for each dependency and generate a structured validation report (CSV or JSON)"
