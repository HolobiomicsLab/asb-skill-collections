---
name: semantic-versioning-validation
description: Use when when you need to confirm that a generated or retrieved release
  artifact from a version control system (e.g., git tag v1.0.0) produces byte-for-byte
  or functionally equivalent outputs to the official release published on a platform
  (e.g., GitHub Releases) on a specific date.
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

# semantic-versioning-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate that a software release artifact (versioned binary, source archive, or metadata) matches its published semantic version tag and reference release record. This skill ensures reproducibility and integrity of versioned deliverables in scientific software projects.

## When to use

When you need to confirm that a generated or retrieved release artifact from a version control system (e.g., git tag v1.0.0) produces byte-for-byte or functionally equivalent outputs to the official release published on a platform (e.g., GitHub Releases) on a specific date. Use this skill when rebuilding historical releases, validating CI/CD pipelines, or auditing software provenance in a scientific workflow.

## When NOT to use

- Input repository lacks version control tags or semantic versioning metadata.
- Reference release record is unavailable, unsigned, or from an untrusted source.
- The target release predates the adoption of automated versioning tools in the project.

## Inputs

- git repository at a specific semantic version tag (e.g., v1.0.0)
- reference release record (e.g., GitHub Release metadata with version, files, checksums, and publication date)
- versioning tool configuration (e.g., Semantic Release config file)

## Outputs

- generated release artifacts (versioned binaries, source archives, or compiled packages)
- generated release metadata (version string, release notes, file manifest)
- validation report comparing generated artifacts to reference (matching/discrepant files, checksums, metadata)

## How to apply

Retrieve the software repository at the target git tag (e.g., v1.0.0). Execute the versioning and artifact generation tool (e.g., Semantic Release) with the configuration present at that tag to produce the release artifacts and metadata (version number, release notes, file contents). Compare the generated artifacts systematically against the reference release record (published version number, files, and checksums) to confirm alignment. Validate that the version number, file manifests, and cryptographic checksums (e.g., SHA256) all match the reference. Document any discrepancies in artifact content, metadata timestamps, or configuration that would indicate a failure to reproduce.

## Related tools

- **Semantic Release** (Generate versioned release artifacts and metadata from a git repository at a specified semantic version tag)

## Evaluation signals

- Generated version number string matches the reference release version (e.g., '1.0.0').
- Cryptographic checksums (SHA256, MD5) of generated files match those in the reference release record.
- File manifests (file names, sizes, and directory structure) are identical between generated and reference artifacts.
- Release metadata (release notes, timestamps, commit references) are consistent between generated and reference.
- Tool execution completed without errors and produced a complete artifact bundle.

## Limitations

- Reproducibility depends on availability of exact toolchain versions and dependencies present at the time of original release.
- Checksums may diverge if build environment, timestamps, or non-deterministic elements (compression, ordering) differ between original and reproduction.
- Reference release records on platforms like GitHub may be edited post-publication, making historical comparison unreliable.
- This skill validates structural/content integrity only; it does not verify functional correctness or algorithmic validity of the software.

## Evidence

- [other] Execute Semantic Release with appropriate configuration to generate versioned artifacts and release notes.: "Execute Semantic Release with appropriate configuration to generate versioned artifacts and release notes."
- [other] Validate the generated release artifacts and metadata against the reference GitHub release record dated 2025-07-29 to confirm version number, file contents, and checksums match.: "Validate the generated release artifacts and metadata against the reference GitHub release record dated 2025-07-29 to confirm version number, file contents, and checksums match."
