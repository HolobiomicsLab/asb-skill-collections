---
name: ci-pipeline-reproducibility-verification
description: Use when you have cloned a scientific Python project (e.g., scverse/scanpy) and need to verify that your local development environment matches the CI specification before submitting contributions, or when auditing whether the published test suite executes without failures on a fresh checkout.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3365
  tools:
  - git
  - Hatch
  - pytest
  - matplotlib
  - Scanpy
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
- This section of the docs covers our practices for working with git on our codebase
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_scanpy
    doi: 10.1186/s13059-017-1382-0
    title: scanpy
  dedup_kept_from: coll_scanpy
schema_version: 0.2.0
---

# CI Pipeline Reproducibility Verification

## Summary

Verify that a scientific software project's continuous integration (CI) workflow executes reproducibly by running the full test suite locally using the project's declared environment manager (Hatch) and test framework (pytest). This skill ensures that development changes do not break existing functionality and that the test environment is portable across machines.

## When to use

Apply this skill when you have cloned a scientific Python project (e.g., scverse/scanpy) and need to verify that your local development environment matches the CI specification before submitting contributions, or when auditing whether the published test suite executes without failures on a fresh checkout.

## When NOT to use

- The project does not use Hatch or pytest (use the project's native test runner instead).
- You are testing only a subset of functionality and do not need full CI verification (run targeted tests via pytest directly).
- The project is in a broken or untagged development state and the test suite is expected to fail (defer until a stable release or PR milestone).

## Inputs

- Git repository (cloned locally)
- hatch.toml configuration file
- pytest test suite (pytest files in tests/ directory)
- Optional: matplotlib reference images for image comparison fixtures

## Outputs

- Test execution report (exit code and pass/fail/skip counts)
- pytest output log
- Image comparison results (if applicable)
- Confirmation that CI workflow is reproducible locally

## How to apply

Fork and clone the target repository to a local machine using git. Examine the project's hatch.toml configuration file to identify the predefined test environment and pytest settings. Execute the test command `hatch test` from the repository root, which automatically creates the Hatch environment and runs all tests in the designated test directory (e.g., scanpy/tests) with configured pytest parameters. Monitor for exit code 0 and zero non-skipped test failures; any deviation indicates either a missing dependency, platform incompatibility, or a genuine regression. Optionally run a subset of tests using `-k` patterns (e.g., `hatch test -k plotting`) for faster iteration during development. For projects using matplotlib or other image-based testing, verify that custom reference images pass validation via the image_comparer fixture.

## Related tools

- **Hatch** (Environment and dependency management; executes predefined test environments via hatch.toml)
- **pytest** (Test discovery and execution framework; runs test suite with configured settings)
- **git** (Version control for cloning and managing repository checkout)
- **matplotlib** (Reference image generation and comparison for plot validation via image_comparer fixture)
- **Scanpy** (Example scientific software project with reproducible CI workflow via Hatch and pytest) — https://github.com/scverse/scanpy

## Examples

```
hatch test
```

## Evaluation signals

- Exit code 0 from `hatch test` command
- Zero non-skipped test failures reported in pytest output
- All matplotlib reference images pass the image_comparer fixture validation (if present)
- Test execution time and count matches documented expectations or prior CI runs
- No platform-specific or environment-specific errors (e.g., missing optional dependencies should be reported as 'skipped', not 'failed')

## Limitations

- Reproducibility depends on matching Python version and OS architecture; some tests may skip on unsupported platforms.
- Image comparison tests require consistent matplotlib rendering across systems; font rendering or graphics driver differences may cause false failures.
- Large test suites (e.g., Scanpy's full suite) may require significant disk space and compute time; subset testing via `-k` patterns is recommended for rapid iteration.
- Network-dependent tests (e.g., data downloads) may fail in offline environments or due to transient remote service unavailability.

## Evidence

- [other] Does the Scanpy test suite execute without failures when invoked via the Hatch environment using the standard test command?: "Does the Scanpy test suite execute without failures when invoked via the Hatch environment using the standard test command?"
- [other] Scanpy uses pytest for testing and provides a Hatch environment configuration to execute the test suite via the `hatch test` command.: "Scanpy uses pytest for testing and provides a Hatch environment configuration to execute the test suite via the `hatch test` command."
- [other] Fork and clone the scverse/scanpy repository to a local machine using git. Create a development environment using Hatch by running `hatch test` from the repository root, which automatically creates the predefined Hatch environment specified in hatch.toml.: "Fork and clone the scverse/scanpy repository to a local machine using git. Create a development environment using Hatch by running `hatch test` from the repository root, which automatically creates"
- [other] Verify the test run completes with exit code 0 and reports zero non-skipped test failures.: "Verify the test run completes with exit code 0 and reports zero non-skipped test failures."
- [other] Check that any custom matplotlib plot reference images match expected outputs via the image_comparer fixture.: "Check that any custom matplotlib plot reference images match expected outputs via the image_comparer fixture."
- [other] We use pytest to test scanpy. To run the tests, simply run `hatch test`: "We use pytest to test scanpy. To run the tests, simply run `hatch test`"
- [other] Using one of the predefined environments in hatch.toml: "Using one of the predefined environments in hatch.toml"
