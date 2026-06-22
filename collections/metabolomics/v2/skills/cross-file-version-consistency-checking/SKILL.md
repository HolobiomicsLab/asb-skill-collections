---
name: cross-file-version-consistency-checking
description: Use when before initiating a release branch workflow for a multi-module Maven project, particularly when the repository contains multiple pom.xml files at different directory levels and a release branch naming convention (e.g., 'release/X.Y.Z') is planned.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics: []
  tools:
  - NMRFx
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

# cross-file-version-consistency-checking

## Summary

Validates that all version strings across distributed configuration files (pom.xml, build metadata) in a software repository are synchronized, preventing release branch creation with conflicting versions. This is essential for multi-module projects where version drift can cause build failures or deployment inconsistencies.

## When to use

Before initiating a release branch workflow for a multi-module Maven project, particularly when the repository contains multiple pom.xml files at different directory levels and a release branch naming convention (e.g., 'release/X.Y.Z') is planned. Use this skill when preparing to verify that all version tags are aligned prior to cutting a release.

## When NOT to use

- When the project uses a single pom.xml or centralizes version management in a parent POM that is already validated.
- When release branches are created ad-hoc without version synchronization as a project requirement.
- When the repository is not a Maven-based project or does not use pom.xml for version declaration.

## Inputs

- Git repository directory (NMRFx or similar multi-module Maven project)
- pom.xml file collection (distributed across repository tree)
- Branch context (typically master or main branch)

## Outputs

- Version consistency validation report
- Indexed list of pom.xml files with extracted versions
- Pass/fail status for release readiness
- File path and version mismatch log (if conflicts detected)

## How to apply

Clone or access the target repository and ensure the master branch (or appropriate base branch) is checked out. Scan the entire repository tree to locate all pom.xml files, then systematically extract the <version> tag value from each file. Compare all extracted version strings for exact matches; record any file paths and differing values where mismatches occur. Generate a structured validation report that lists each pom.xml file checked, its extracted version, and an overall pass/fail status. The skill succeeds when all versions match exactly and the report confirms synchronization; if verification passes, document that the release branch can be safely created without version conflicts.

## Related tools

- **NMRFx** (Target software repository for version consistency validation; source of pom.xml files to be scanned and compared) — github.com/nanalysis/nmrfx

## Evaluation signals

- All pom.xml files in the repository tree are discovered and included in the report.
- Version strings extracted from each <version> tag are identical across all files (exact string match, including patch and qualifier segments).
- Pass/fail status clearly indicates whether versions are synchronized or lists specific mismatches with file paths and differing values.
- Release branch naming convention (e.g., 'release/X.Y.Z') is validated as safe to apply only when pass status is confirmed.
- No pom.xml files are skipped or omitted from the verification.

## Limitations

- Requires manual or scripted scanning of the repository tree; does not automatically detect nested or non-standard pom.xml locations.
- Does not verify consistency with external version sources (e.g., Maven Central, artifact repositories).
- Cannot detect version mismatches introduced in uncommitted local changes; operates on the checked-out branch state only.
- Does not validate semantic version format (e.g., SemVer compliance) — only exact string matching.

## Evidence

- [other] Scan all pom.xml files in the repository tree and extract version strings from each <version> tag.: "Scan all pom.xml files in the repository tree and extract version strings from each <version> tag."
- [other] Verify that all extracted versions match exactly; flag any mismatches with file paths and differing values.: "Verify that all extracted versions match exactly; flag any mismatches with file paths and differing values."
- [other] Generate a validation report listing all pom files checked, their versions, and an overall pass/fail status indicating whether all versions are synchronized.: "Generate a validation report listing all pom files checked, their versions, and an overall pass/fail status indicating whether all versions are synchronized."
- [other] If verification passes, document that the release branch naming convention (prefixed 'release/X.Y.Z') can be safely applied without version conflicts.: "If verification passes, document that the release branch naming convention (prefixed 'release/X.Y.Z') can be safely applied without version conflicts."
