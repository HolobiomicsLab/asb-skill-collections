---
name: git-branch-workflow-validation
description: Use when when preparing to create a release branch in a Maven-based multi-module project (e.g., NMRFx), use this skill to verify that all pom.xml files in the repository tree declare identical version strings. This is a prerequisite for safe release-branch naming (e.g., release/X.Y.
license: CC-BY-4.0
metadata:
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

# git-branch-workflow-validation

## Summary

Validates that a multi-module software project (e.g., NMRFx) maintains synchronized version strings across all pom.xml files before creating a release branch, ensuring version consistency across the entire repository tree.

## When to use

When preparing to create a release branch in a Maven-based multi-module project (e.g., NMRFx), use this skill to verify that all pom.xml files in the repository tree declare identical version strings. This is a prerequisite for safe release-branch naming (e.g., release/X.Y.Z) and prevents version conflicts during artifact build and deployment.

## When NOT to use

- Repository uses a non-Maven build system (e.g., Gradle, SBT, Cargo) where version synchronization is managed differently.
- Target branch is already a release branch; use this skill only on development or master branches before release creation.
- pom.xml files are already known to have intentionally different versions (rare, but may occur in monorepo setups with decoupled module versioning).

## Inputs

- NMRFx repository (cloned or remote URL)
- Master branch checkout state
- pom.xml file tree

## Outputs

- Validation report (pass/fail status)
- List of all pom.xml files with extracted versions
- Mismatch log (if any versions differ)

## How to apply

Clone or access the target repository (e.g., github.com/nanalysis/nmrfx) and ensure the master branch is checked out. Recursively scan the entire repository tree to locate all pom.xml files and extract the version string from each <version> tag. Compare all extracted versions for exact equality and record any file paths with mismatched values. Generate a validation report that lists all pom files checked, their versions, and an overall pass/fail status. Only if verification passes can the release branch naming convention (release/X.Y.Z) be safely applied without version conflicts.

## Related tools

- **NMRFx** (Target software project whose pom.xml files are scanned and validated for version consistency) — github.com/nanalysis/nmrfx

## Evaluation signals

- All pom.xml files in the repository tree are located and enumerated in the report.
- Every extracted <version> tag value is identical across all pom files (or mismatches are explicitly flagged with file paths and differing values).
- Validation report explicitly states pass/fail status; pass indicates safe to proceed with release/X.Y.Z branch naming.
- No version conflicts or overlapping version declarations remain after verification.
- Release branch can be created and checked out without triggering Maven build failures due to version mismatches.

## Limitations

- Skill assumes master branch is the authoritative source; if working from a feature or staging branch, results may not reflect the intended release baseline.
- Does not detect or validate whether version strings follow semantic versioning conventions (X.Y.Z format); only verifies equality.
- If pom.xml files use property references (e.g., ${project.version}) instead of literal version tags, extraction logic must be adapted.
- Multi-repo projects or external dependencies with independent versioning are not covered by this validation.

## Evidence

- [other] Scan all pom.xml files in the repository tree and extract version strings from each <version> tag.: "Scan all pom.xml files in the repository tree and extract version strings from each <version> tag."
- [other] Verify that all extracted versions match exactly; flag any mismatches with file paths and differing values.: "Verify that all extracted versions match exactly; flag any mismatches with file paths and differing values."
- [other] Generate a validation report listing all pom files checked, their versions, and an overall pass/fail status indicating whether all versions are synchronized.: "Generate a validation report listing all pom files checked, their versions, and an overall pass/fail status indicating whether all versions are synchronized."
- [other] If verification passes, document that the release branch naming convention (prefixed 'release/X.Y.Z') can be safely applied without version conflicts.: "If verification passes, document that the release branch naming convention (prefixed 'release/X.Y.Z') can be safely applied without version conflicts."
