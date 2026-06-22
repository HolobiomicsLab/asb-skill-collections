---
name: installation-requirement-validation
description: Use when before attempting to run QCxMS2 for the first time, after updating any external dependencies (xtb, CREST, molbar, orca, geodesic_interpolate), or when troubleshooting unexplained calculation failures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0003
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

# installation-requirement-validation

## Summary

Systematically verify that all required external programs are installed with their minimum specified versions before executing QCxMS2 calculations. This skill prevents runtime failures by validating the dependency chain early in the setup process.

## When to use

Before attempting to run QCxMS2 for the first time, after updating any external dependencies (xtb, CREST, molbar, orca, geodesic_interpolate), or when troubleshooting unexplained calculation failures. Apply this skill when you have a new computing environment or suspect that a required tool is missing or outdated.

## When NOT to use

- Input systems where executables are already bundled or virtualized (e.g., Docker containers with pre-installed dependencies); use this skill only if the host environment requires independent verification.
- Automated CI/CD pipelines that already embed version checks in their build configuration; this skill is for manual setup or troubleshooting, not for replacing existing automated checks.
- Environments where xtb is technically optional because tblite is integrated; refer to CREST documentation—some functionalities like QCG still require xtb.

## Inputs

- System PATH environment variable
- Installed executable names: qcxms2, xtb, crest, molbar, orca, geodesic_interpolate
- Target minimum version thresholds (documented in QCxMS2 README)

## Outputs

- Structured validation report (CSV or JSON) summarizing pass/fail status per dependency
- Explicit version numbers discovered for each executable
- Boolean flag indicating whether all dependencies meet minimum requirements

## How to apply

Locate each required executable in the system PATH using command-line tools (e.g., 'which' on Unix or 'where' on Windows). For each found executable, invoke its version-reporting flag (typically --version or -V) and parse the output to extract the version string. Compare extracted versions against the documented minimum thresholds: xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0; for geodesic_interpolate, confirm presence without enforcing a version check if version output is unavailable. Record pass/fail status for each dependency and generate a structured validation report (CSV or JSON) that lists all discovered versions alongside the minimum requirements. Stop installation of QCxMS2 and halt calculation startup if any dependency fails validation.

## Related tools

- **xtb** (Semiempirical quantum mechanical calculator; required version > 6.7.1 for QCxMS2 calculations) — https://github.com/grimme-lab/xtb
- **CREST** (Conformer-rotamer ensemble sampling tool for automated exploration of molecular chemical space; required version ≥ 3.0.2 for QCxMS2 conformer generation) — https://github.com/crest-lab/crest
- **molbar** (Molecular fragmentation tool for mass spectrum prediction; required version ≥ 1.1.3 for QCxMS2 fragmentation workflows) — https://git.rwth-aachen.de/bannwarthlab/molbar
- **orca** (General-purpose quantum chemistry package for high-level calculations; required version ≥ 6.0.0 for QCxMS2 quantum mechanical refinement) — https://orcaforum.kofo.mpg.de
- **geodesic_interpolate** (Optional tool for interpolating molecular structures along reaction pathways; presence required but version check may be skipped if unavailable) — https://github.com/virtualzx-nad/geodesic-interpolate
- **QCxMS2** (Main program requiring all validated dependencies before launch) — https://github.com/grimme-lab/QCxMS2

## Examples

```
for dep in xtb crest molbar orca geodesic_interpolate; do echo "Checking $dep:"; which $dep && $dep --version 2>&1 | head -1; done > qcxms2_deps.txt
```

## Evaluation signals

- All five required executables (xtb, CREST, molbar, orca, geodesic_interpolate) are locatable via PATH search without error.
- Each executable's --version or -V flag returns a parseable version string; non-zero exit code indicates validation failure.
- Extracted version numbers exactly match or exceed documented thresholds: xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0.
- Validation report is machine-readable (valid CSV or JSON) and contains at least six columns/fields: tool name, required version, found version, comparison operator, pass/fail status, timestamp.
- A passing validation report allows QCxMS2 to proceed; a failing report (any single dependency below threshold) triggers an informative error message and halts execution.

## Limitations

- Version extraction depends on consistent --version or -V output format; non-standard or missing version flags will cause parsing failures. Geodesic_interpolate lacks documented version reporting, so its validation is presence-only.
- PATH-based executable lookup assumes standard system conventions (Unix 'which' or Windows 'where'); non-standard installations in obscure directories may evade detection even if installed.
- No changelog is available in the QCxMS2 repository, so historical version requirements or breaking changes between releases cannot be tracked for retrospective validation.
- Validation occurs only at setup time; if a dependency is uninstalled or downgraded after QCxMS2 starts, no runtime re-validation occurs—users must manually re-run this skill.

## Evidence

- [readme] For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2: "For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2"
- [readme] xtb > 6.7.1, CREST ≥ 3.0.2, molbar ≥ 1.1.3, orca ≥ 6.0.0: "**xtb** (version > 6.7.1 - bleeding edge version)
**CREST** (version >= 3.0.2)
**molbar** (version >= 1.1.3)
**orca** (version >= 6.0.0)"
- [other] Query the system PATH and attempt to locate each required executable using standard command-line tools (e.g., 'which' on Unix or 'where' on Windows): "Query the system PATH and attempt to locate each required executable: xtb, CREST, molbar, orca, and geodesic_interpolate using standard command-line tools (e.g., 'which' on Unix or 'where' on Windows)"
- [other] For each located executable, invoke version-reporting flags and parse the output to extract the version string: "For each located executable, invoke version-reporting flags (typically --version or -V) and parse the output to extract the version string"
- [other] Record pass/fail outcome for each dependency and generate a structured validation report: "Record pass/fail outcome for each dependency and generate a structured validation report (CSV or JSON) summarizing all results with explicit version numbers found and minimum requirements"
- [readme] While xtb is technically not needed for the primary runtypes of CREST thanks to tblite integration, some functionalities like QCG still require it: "While `xtb` is technically not needed for the primary runtypes of CREST versions >3.0 thanks to an integration of [`tblite`](https://github.com/tblite/tblite), some functionalities, like QCG, still"
