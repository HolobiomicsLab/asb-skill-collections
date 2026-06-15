---
name: hatch-environment-configuration-and-activation
description: Use when you have cloned a Python project (e.g., scverse/scanpy) that includes a hatch.toml configuration file and need to set up a consistent development or testing environment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2422
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3372
  tools:
  - Hatch
  - git
  - pytest
  - Scanpy
  - Python
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
- Using one of the predefined environments in hatch.toml is as simple as running `hatch test`
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

# hatch-environment-configuration-and-activation

## Summary

Configure and activate isolated Python development environments using Hatch, a modern environment and dependency manager that reads predefined environment specifications from hatch.toml. This skill enables reproducible testing, linting, and development workflows by automating environment setup and tool invocation without manual virtual environment management.

## When to use

You have cloned a Python project (e.g., scverse/scanpy) that includes a hatch.toml configuration file and need to set up a consistent development or testing environment. Use this skill when you want to avoid manual virtual environment creation and instead rely on declarative, project-level environment definitions that specify Python version, dependencies, and tool configurations.

## When NOT to use

- The project does not include a hatch.toml file; use pip, conda, or Poetry instead.
- You need to manually pin specific dependency versions not declared in hatch.toml; edit the configuration file or use pip install --force-reinstall.
- You are running tests in a containerized or pre-provisioned environment (e.g., Docker, CI/CD); Hatch environment creation may conflict with existing system dependencies.

## Inputs

- hatch.toml configuration file (project root)
- Python source code (local repository directory)
- Test files (pytest suite in scanpy/tests or equivalent)

## Outputs

- Isolated Python environment (cached by Hatch)
- Test execution results (exit code and pytest report)
- Installed dependencies in environment (transitive closure)

## How to apply

Read the hatch.toml file in the repository root to identify available predefined environments (e.g., 'test', 'dev'). Run `hatch test` or `hatch run <environment>:<command>` from the repository root; Hatch automatically creates the specified environment if it does not exist, installs dependencies in isolation, and executes the command. For the Scanpy project, `hatch test` invokes pytest with pre-configured settings to run the full test suite in the scanpy/tests directory. Monitor the command exit code (0 = success, non-zero = failure) and review pytest output to verify zero non-skipped test failures. Hatch caches environments between runs, so subsequent invocations are faster; to force a rebuild, use `hatch env remove <name>` before re-running the command.

## Related tools

- **Hatch** (environment and dependency manager that reads hatch.toml and creates isolated Python environments with specified tools and versions) — https://github.com/pypa/hatch
- **pytest** (test runner executed within the Hatch environment to execute test suite with configured settings) — https://github.com/pytest-dev/pytest
- **Scanpy** (example project providing hatch.toml configuration and test suite invoked via `hatch test`) — https://github.com/scverse/scanpy
- **Python** (language runtime installed and managed by Hatch in the isolated environment)
- **git** (version control system used to clone the repository containing hatch.toml before environment activation)

## Examples

```
hatch test
```

## Evaluation signals

- Hatch environment is created and listed in `hatch env show` output without errors.
- The command `hatch test` completes with exit code 0 and pytest reports zero non-skipped test failures.
- Dependencies declared in hatch.toml (e.g., pytest, matplotlib) are installed in the environment; verify with `hatch run python -c 'import pytest'` producing no ImportError.
- Re-running the same command uses the cached environment (faster execution) rather than recreating it each time.
- Test output includes expected assertion results and no configuration-related warnings (e.g., missing hatch.toml or malformed [tool.hatch.envs.*] sections).

## Limitations

- Hatch environments are isolated per project and Python version; switching between projects requires Hatch to create or activate a different environment, increasing disk usage.
- Custom pytest fixtures (e.g., matplotlib image_comparer) must be defined in conftest.py and available in the test environment; missing fixtures will cause test failures.
- Platform-specific dependencies (e.g., system libraries required by anndata or matplotlib) are not managed by Hatch and must be pre-installed on the host machine.
- Hatch caches environments by name and Python version; if hatch.toml is updated but the environment already exists, Hatch will not automatically reinstall dependencies; use `hatch env remove` to force a rebuild.

## Evidence

- [other] We think the easiest is probably Hatch environments. Using one of the predefined environments in hatch.toml: "We think the easiest is probably Hatch environments. Using one of the predefined environments in hatch.toml"
- [other] We use pytest to test scanpy. To run the tests, simply run `hatch test`: "We use pytest to test scanpy. To run the tests, simply run `hatch test`"
- [other] Create a development environment using Hatch by running `hatch test` from the repository root, which automatically creates the predefined Hatch environment specified in hatch.toml.: "Create a development environment using Hatch by running `hatch test` from the repository root, which automatically creates the predefined Hatch environment specified in hatch.toml."
- [other] Verify the test run completes with exit code 0 and reports zero non-skipped test failures.: "Verify the test run completes with exit code 0 and reports zero non-skipped test failures."
- [other] Execute the full pytest test suite via `hatch test`, which runs all tests in the scanpy/tests directory with the configured pytest settings.: "Execute the full pytest test suite via `hatch test`, which runs all tests in the scanpy/tests directory with the configured pytest settings."
