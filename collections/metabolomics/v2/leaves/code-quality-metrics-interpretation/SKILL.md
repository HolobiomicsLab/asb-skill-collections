---
name: code-quality-metrics-interpretation
description: Use when after a GitHub Actions CI workflow has executed static analysis
  (e.g., via Sonarcloud) and generated a quality report.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - MS2Query
  - Sonarcloud
  - GitHub Actions
  - MS2Query CI_build.yml
  license_tier: open
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# code-quality-metrics-interpretation

## Summary

Interpret and evaluate automated code quality metrics (coverage, technical debt, quality gates) produced by continuous integration pipelines to determine code health and identify refactoring priorities. This skill enables maintainers to set meaningful quality thresholds and assess whether a codebase meets reliability standards before merging.

## When to use

After a GitHub Actions CI workflow has executed static analysis (e.g., via Sonarcloud) and generated a quality report. Use this skill when you need to decide whether a pull request meets minimum quality standards, track code health trends over releases, or identify technical debt hotspots that should be addressed before feature release.

## When NOT to use

- Input is a binary pass/fail gate status with no underlying metric details—this skill requires actionable metric values (coverage %, debt estimate, violation counts), not just a gate result.
- The codebase has no established quality baseline or thresholds—you must first define organizational standards before interpreting metrics meaningfully.
- Static analysis is disabled or Sonarcloud is not integrated into the CI pipeline—this skill depends on automated quality report generation.

## Inputs

- Sonarcloud static analysis report (JSON or web-accessible dashboard)
- GitHub Actions workflow execution log
- Pull request diff (to correlate coverage changes with code additions)
- Project quality gate policy (if configured)

## Outputs

- Interpreted quality metrics summary (coverage %, technical debt, gate status)
- Merge/no-merge recommendation based on quality thresholds
- List of prioritized code quality issues (security, duplication, debt)
- Updated quality baseline for tracking project health over time

## How to apply

Retrieve the Sonarcloud quality report output from the completed GitHub Actions workflow, which includes code coverage percentage, technical debt (in days), and quality gate pass/fail status. Examine coverage metrics to ensure new code paths are tested; cross-reference technical debt estimates with your project's maintenance capacity and release timeline. Use quality gates (binary pass/fail rules on coverage, duplicated lines, security vulnerabilities) as automated decision criteria—a failing gate typically blocks merge until violations are resolved. Document the thresholds your team has chosen (e.g., minimum coverage, maximum debt) so interpretation is consistent across pull requests. Use the ms2query_model_prediction score analogy from MS2Query: similar to filtering matches by confidence (e.g., score > 0.7 for reliability), set quality score thresholds that balance false positives against actionable feedback.

## Related tools

- **Sonarcloud** (Generates static analysis report with code coverage, technical debt, security vulnerabilities, and quality gates for CI-integrated code review)
- **GitHub Actions** (Orchestrates CI workflow that triggers Sonarcloud analysis and surfaces quality report results in pull request context) — https://github.com/iomega/ms2query
- **MS2Query CI_build.yml** (Example GitHub Actions workflow configuration demonstrating integration of build/test execution with Sonarcloud static analysis) — https://github.com/iomega/ms2query

## Evaluation signals

- Sonarcloud quality gate transitions from FAIL to PASS after code changes, indicating threshold-driven interpretation was applied correctly.
- Code coverage percentage increases or maintains expected baseline (e.g., ≥ 80%) for pull request without regressing overall project coverage.
- Technical debt estimate (in days) is documented and tracked; debt trend is compared against project release timeline to confirm feasibility of merge.
- Security vulnerabilities and code duplication counts are reviewed and cross-referenced; high-severity findings are explicitly addressed in merge decision.
- Interpretation is reproducible: team members following the same quality threshold policy reach the same pass/fail recommendation for identical metrics.

## Limitations

- Sonarcloud metrics reflect static analysis heuristics and may produce false positives (e.g., complex but correct code flagged as high debt). Manual review of flagged code is often necessary to avoid rejecting valid contributions.
- Code coverage percentage does not guarantee test quality; high coverage of low-quality tests (e.g., tests that do not validate behavior) can mask bugs. Use coverage as one signal, not the sole criterion.
- Technical debt estimates are relative and project-dependent. A debt value is only meaningful if the team has calibrated what 'debt per day' means in their codebase; raw numbers are not comparable across projects.
- Quality gates are typically binary (pass/fail) and may not reflect nuanced trade-offs; a single failing gate blocks merge even if other metrics are strong. Thresholds must be tuned to avoid overly strict or permissive gates.

## Evidence

- [other] MS2Query uses a GitHub Actions workflow (CI_build.yml) that triggers on pull requests and integrates with Sonarcloud, producing a GitHub Workflow Status badge that reflects the combined outcome of build, test, and static analysis checks.: "integrates with Sonarcloud, producing a GitHub Workflow Status badge that reflects the combined outcome of build, test, and static analysis checks"
- [other] Retrieve and document the Sonarcloud quality report output showing code coverage, technical debt, and quality gates status.: "Retrieve and document the Sonarcloud quality report output showing code coverage, technical debt, and quality gates status"
- [readme] This column contains a score, which indicates the likelihood that the found match is a good match. This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good match/analogue.: "This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good match"
- [readme] To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be discarded.: "To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution"
- [readme] MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10: "MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10"
