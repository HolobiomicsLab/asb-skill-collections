---
name: release-versioning-schema-enforcement
description: Use when when preparing a release branch for a Maven-based project (like NMRFx) and you need to verify that all pom.xml files in the repository tree declare identical version strings before applying release branch naming conventions (e.g., 'release/X.Y.Z').
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - NMRFx
  - Git
derived_from:
- doi: 10.1038/s42004-025-01812-8
  title: NMRFx
evidence_spans:
- github.com__nanalysis__nmrfx
- github.com/nanalysis/nmrfx
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmrfx_cq
    doi: 10.1038/s42004-025-01812-8
    title: NMRFx
  dedup_kept_from: coll_nmrfx_cq
schema_version: 0.2.0
---

# release-versioning-schema-enforcement

## Summary

Validates that all pom.xml version declarations across a multi-module Maven project are synchronized before release branch creation. This prevents version conflicts and ensures consistent artifact versioning during the release procedure.

## When to use

When preparing a release branch for a Maven-based project (like NMRFx) and you need to verify that all pom.xml files in the repository tree declare identical version strings before applying release branch naming conventions (e.g., 'release/X.Y.Z').

## When NOT to use

- Repository is not Maven-based (no pom.xml files present).
- Release procedure does not require synchronized versions across multiple modules.
- Version strings are managed by an external build system or continuous integration tool that auto-synchronizes them.

## Inputs

- Maven repository (git clone URL or local directory)
- Branch reference (e.g., 'master')
- pom.xml file tree

## Outputs

- Version validation report (pass/fail status)
- List of pom.xml files with extracted version strings
- Mismatch flagging report (file paths and differing values, if any)
- Release readiness confirmation

## How to apply

Clone or access the target Maven repository and ensure the master branch is checked out. Scan the entire repository tree and extract the <version> tag value from each pom.xml file. Compare all extracted versions for exact matches; record file paths and values for any mismatches. Generate a validation report listing all pom files inspected, their versions, and an overall pass/fail status. Only if all versions match exactly should the release branch naming convention be applied, confirming that no version conflicts will occur during the release process.

## Related tools

- **NMRFx** (Source Maven project whose pom.xml versions are verified for release consistency) — github.com/nanalysis/nmrfx
- **Git** (Version control system to clone repository and verify branch state before scanning)

## Evaluation signals

- All pom.xml files in the repository tree are discovered and scanned.
- Each <version> tag value is extracted and recorded with its file path.
- All extracted versions match exactly (no mismatches detected).
- Validation report explicitly confirms pass/fail status and lists all files inspected.
- If pass status is achieved, release branch naming convention (prefixed 'release/X.Y.Z') can be safely applied without version conflicts.

## Limitations

- Scan requires full repository access and correct branch checkout; partial clones or detached heads may yield incomplete results.
- Only detects structural version mismatches in pom.xml; does not validate that versions are semantically correct or follow project conventions.
- Does not detect version inconsistencies in other build configuration files (gradle, sbt, etc.) if the project is not pure Maven.

## Evidence

- [other] Scan all pom.xml files in the repository tree and extract version strings from each <version> tag.: "Scan all pom.xml files in the repository tree and extract version strings from each <version> tag."
- [other] Verify that all extracted versions match exactly; flag any mismatches with file paths and differing values.: "Verify that all extracted versions match exactly; flag any mismatches with file paths and differing values."
- [other] Generate a validation report listing all pom files checked, their versions, and an overall pass/fail status indicating whether all versions are synchronized.: "Generate a validation report listing all pom files checked, their versions, and an overall pass/fail status indicating whether all versions are synchronized."
- [other] If verification passes, document that the release branch naming convention (prefixed 'release/X.Y.Z') can be safely applied without version conflicts.: "If verification passes, document that the release branch naming convention (prefixed 'release/X.Y.Z') can be safely applied without version conflicts."
