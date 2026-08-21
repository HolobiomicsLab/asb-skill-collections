---
name: github-release-metadata-comparison
description: Use when you have reproduced a release artifact locally (e.g., via Semantic
  Release or a build tool) and need to verify it matches the official GitHub release
  record.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Semantic Release
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c07078
  title: qc4metabolomics
evidence_spans:
- Semantic Release
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qc4metabolomics
    doi: 10.1021/acs.analchem.4c07078
    title: qc4metabolomics
  dedup_kept_from: coll_qc4metabolomics
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c07078
  all_source_dois:
  - 10.1021/acs.analchem.4c07078
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# github-release-metadata-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate that a locally reproduced software release artifact matches the reference metadata (version number, file contents, checksums) published on GitHub. This skill ensures reproducibility and integrity of versioned releases in scientific software workflows.

## When to use

You have reproduced a release artifact locally (e.g., via Semantic Release or a build tool) and need to verify it matches the official GitHub release record. Apply this skill when you must confirm that version numbers, generated files, and cryptographic checksums are identical to the reference, especially in contexts requiring artifact provenance and release integrity for downstream users or CI/CD pipelines.

## When NOT to use

- The reference GitHub release does not exist or is inaccessible.
- You are validating a pre-release or draft release not formally published on GitHub.
- The local build environment differs fundamentally (e.g., different OS, compiler, or dependency versions) and you have not documented or justified the expected differences.

## Inputs

- git repository at a specific version tag (e.g., v1.0.0)
- reference GitHub release record (version, date, file list, checksums)
- Semantic Release or equivalent build configuration

## Outputs

- validation report (pass/fail for version, files, checksums)
- detailed diff or checksum comparison log
- artifact integrity confirmation

## How to apply

Retrieve the reference GitHub release record (including version tag, release date, and published artifacts). Generate or build the same release locally using the same toolchain and configuration (e.g., Semantic Release with pinned version). Compare the locally produced artifacts against the GitHub release by checking: (1) version string matches the git tag and release metadata; (2) file names, sizes, and contents are byte-for-byte identical; (3) checksums (SHA256 or MD5) for each artifact match. Use diff tools or checksum utilities to automate the comparison. If any mismatch is found, investigate configuration drift, dependency versions, or timestamp variations that may account for the discrepancy.

## Related tools

- **Semantic Release** (generates versioned artifacts and release metadata; configured to produce the same output as the reference release)

## Evaluation signals

- Version number in locally generated artifact matches the git tag and GitHub release version string exactly.
- All file names, sizes (in bytes), and modification timestamps match the reference release (or timestamps are expected to differ and are excluded from comparison).
- Checksums (SHA256 or MD5) for each artifact produced locally are byte-identical to those published on GitHub.
- Release notes or metadata generated locally match the published GitHub release notes verbatim (or expected template differences are documented).
- No extraneous files appear in the local build that are absent from the GitHub release, and vice versa.

## Limitations

- Timestamp differences in archives (e.g., .zip or .tar.gz) may cause checksum mismatches even if content is identical; use content-aware comparison (e.g., tar without timestamps or zip without date metadata) if needed.
- Non-deterministic build outputs (e.g., embedded build IDs, randomized content) may prevent byte-identical reproduction; document and exclude such fields from comparison.
- The skill does not detect functional correctness of the release—only that local and reference artifacts are identical; separate testing is required to validate functionality.

## Evidence

- [other] Execute Semantic Release with appropriate configuration to generate versioned artifacts and release notes.: "Execute Semantic Release with appropriate configuration to generate versioned artifacts and release notes."
- [other] Validate the generated release artifacts and metadata against the reference GitHub release record dated 2025-07-29 to confirm version number, file contents, and checksums match.: "Validate the generated release artifacts and metadata against the reference GitHub release record dated 2025-07-29 to confirm version number, file contents, and checksums match."
