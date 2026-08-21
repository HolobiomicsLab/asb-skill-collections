---
name: maven-pom-version-extraction
description: Use when preparing a software release and you need to verify that all
  Maven modules declare identical version numbers before creating a release branch.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - NMRFx
  license_tier: restricted
  provenance_tier: literature
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42004-025-01812-8
  all_source_dois:
  - 10.1038/s42004-025-01812-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# maven-pom-version-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and validate version strings from all pom.xml files in a Maven-based repository to ensure version synchronization across the project tree. This skill is essential for release preparation workflows where consistent versioning across all modules is a prerequisite for safe branch creation and artifact publishing.

## When to use

Apply this skill when preparing a software release and you need to verify that all Maven modules declare identical version numbers before creating a release branch. Trigger conditions include: (1) initiating a release procedure, (2) auditing a multi-module Maven project for version consistency prior to tagging, or (3) validating that no partial or stale version updates exist in any pom.xml file across the repository tree.

## When NOT to use

- Do not use this skill if the repository is not Maven-based or does not use pom.xml files for version management.
- Do not apply this skill to projects using other build systems (Gradle, npm, Poetry, etc.) without adaptation.
- Do not use as a substitute for automated CI/CD version checks; use only for manual pre-release audits or local verification.

## Inputs

- Maven repository root directory (local or remote clone)
- Target branch name (e.g., 'master', 'main')
- List of pom.xml file paths or search pattern

## Outputs

- Validation report (JSON or plaintext) listing all pom.xml files inspected
- Extracted version strings per module
- Pass/fail status indicating version synchronization
- Mismatch report (if applicable) with file paths and differing version values

## How to apply

Clone or access the target Maven repository and ensure the desired branch (typically master or main) is checked out. Recursively scan the repository tree for all pom.xml files using standard file discovery tools. For each pom.xml, parse the XML structure and extract the <version> tag value. Collect all extracted versions into a set and compare for exact string equality. If all versions match, the verification passes and release branch naming (e.g., 'release/X.Y.Z') can proceed safely. If any version mismatch is detected, flag the differing modules with their file paths and values, preventing branch creation until conflicts are resolved.

## Related tools

- **NMRFx** (Maven-based project whose pom.xml files serve as the source for version extraction and validation) — github.com/nanalysis/nmrfx

## Evaluation signals

- All pom.xml files are identified and scanned without parse errors.
- Each <version> tag is correctly extracted and stored as a string.
- Version strings across all modules are identical (or differences are documented with file paths).
- Pass/fail status is explicitly stated in the validation report.
- Release branch naming convention can be safely applied post-verification (no version conflicts flagged).

## Limitations

- Extraction assumes well-formed XML; malformed pom.xml files may cause parser failures.
- Nested or multi-module projects require recursive discovery; shallow scanning may miss submodules.
- Version strings that differ only in whitespace or XML formatting may not be caught; exact string comparison is required.
- Does not validate semantic versioning (e.g., major.minor.patch format) or version ordering; only checks equality.
- Parent POM inheritance and version property resolution are not addressed; direct <version> tag extraction only.

## Evidence

- [other] Scan all pom.xml files in the repository tree and extract version strings from each <version> tag.: "Scan all pom.xml files in the repository tree and extract version strings from each <version> tag."
- [other] Verify that all extracted versions match exactly; flag any mismatches with file paths and differing values.: "Verify that all extracted versions match exactly; flag any mismatches with file paths and differing values."
- [other] Generate a validation report listing all pom files checked, their versions, and an overall pass/fail status indicating whether all versions are synchronized.: "Generate a validation report listing all pom files checked, their versions, and an overall pass/fail status indicating whether all versions are synchronized."
- [other] If verification passes, document that the release branch naming convention (prefixed 'release/X.Y.Z') can be safely applied without version conflicts.: "If verification passes, document that the release branch naming convention (prefixed 'release/X.Y.Z') can be safely applied without version conflicts."
