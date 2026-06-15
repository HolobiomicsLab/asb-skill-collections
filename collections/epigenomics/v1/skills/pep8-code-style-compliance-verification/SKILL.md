---
name: pep8-code-style-compliance-verification
description: Use when developing or reviewing Python code for a scientific package (e.g., cooltools) that targets collaborative development with multiple contributors.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3674
  tools:
  - flake8
  - conda
  - pytest-flake8
  - black
  - autopep8
  - pytest
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans:
- We use [flake8](http://flake8.pycqa.org/en/latest/) to automatically lint the code
- we recommend using [conda](https://docs.conda.io/en/latest/miniconda.html)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cooltools
    doi: 10.1371/journal.pcbi.1012067
    title: cooltools
  dedup_kept_from: coll_cooltools
schema_version: 0.2.0
---

# PEP8 code style compliance verification

## Summary

Automated verification that Python code adheres to PEP 8 style conventions using linting tools (flake8) and optional code formatters (black, autopep8). This skill ensures consistent code style across a scientific Python package, which improves maintainability and code review efficiency.

## When to use

Apply this skill when developing or reviewing Python code for a scientific package (e.g., cooltools) that targets collaborative development with multiple contributors. Use it as part of continuous integration (CI) workflows or before submitting pull requests to enforce uniform style and catch formatting issues automatically rather than during manual code review.

## When NOT to use

- Input is legacy Python code without existing style baseline and refactoring is out of scope—linting will flag numerous violations that may be impractical to fix retroactively without dedicated effort.
- Project uses a custom or non-standard Python style guide incompatible with PEP 8—flake8 enforces PEP 8 conventions and cannot be easily configured to override them.
- Style compliance is not a project priority and code review does not enforce uniform formatting—applying this skill without team buy-in will create friction without benefit.

## Inputs

- Python source files (.py)
- Python package repository with setup.py or pyproject.toml
- Pytest configuration file (pytest.ini or pyproject.toml)

## Outputs

- Flake8 linting report (stdout/log with line-by-line violations or clean status)
- Formatted Python source files (if using black or autopep8 with in-place option)
- CI/CD test pass/fail status based on style compliance

## How to apply

Integrate flake8 linting into your pytest-based testing framework using the pytest-flake8 extension to check code style alongside unit tests. Run flake8 from the repository root to identify style violations against PEP 8 standards. Optionally use black or autopep8 as an automated code formatter to repair formatting issues; black is recommended for deterministic, uncompromising formatting. Execute the linter as part of the standard test suite (e.g., `pytest`) so that style violations fail the build. Configure project-level rules in `pyproject.toml` or setup.cfg to specify which violations to enforce. Evaluate success by confirming zero style warnings in CI logs and that all code diffs show consistent formatting across the codebase.

## Related tools

- **flake8** (Primary linter to detect and report PEP 8 style violations and code smells in Python source files) — http://flake8.pycqa.org/en/latest/
- **pytest-flake8** (Pytest plugin that integrates flake8 linting into the pytest test suite, allowing style checks to run alongside unit tests) — https://docs.pytest.org/en/latest
- **black** (Automated code formatter that enforces deterministic PEP 8-compliant formatting with minimal configuration) — https://github.com/psf/black
- **autopep8** (Automated code formatter that fixes PEP 8 style violations reported by pycodestyle with configurable aggressiveness) — https://github.com/hhatto/autopep8
- **pytest** (Test runner that orchestrates linting and unit test execution in a unified test pipeline) — https://docs.pytest.org/en/latest

## Examples

```
cd /path/to/cooltools && pytest
```

## Evaluation signals

- Flake8 exits with status code 0 and reports zero violations when run on the codebase root.
- CI/CD pipeline (e.g., GitHub Actions) includes a pytest-flake8 job that passes on all commits to main and pull requests.
- Code diffs in pull requests show consistent indentation, line length, whitespace, and naming conventions across all modified files.
- Linting report log is clean (no E* or W* error/warning codes from PEP 8 standard rule set) when inspected post-CI.
- All newly contributed code maintains the style baseline set by black or autopep8 formatting, verifiable through automated formatting pre-commit hooks or CI gates.

## Limitations

- Flake8 enforces PEP 8 conventions and cannot easily adapt to custom style guidelines outside the PEP 8 standard; projects with idiosyncratic style requirements may experience friction.
- Black's opinionated formatting approach (e.g., line length, quote style) may conflict with existing code aesthetics or comments; manual resolution is required for exceptional cases.
- Style linting does not detect logical errors, performance issues, or functional correctness—it is orthogonal to unit testing and type checking and must be combined with other quality gates.
- High volume of pre-existing style violations in legacy codebases can make initial linting adoption costly; remediation may require phased rollout or selective enforcement.

## Evidence

- [other] We use [flake8](http://flake8.pycqa.org/en/latest/) to automatically lint the code and maintain code style: "We use [flake8](http://flake8.pycqa.org/en/latest/) to automatically lint the code and maintain code style"
- [other] pytest testing framework with pytest-cov and pytest-flake8 for coverage and style: "We use [pytest](https://docs.pytest.org/en/latest) as our unit testing framework with the `pytest-cov` extension to check code coverage and `pytest-flake8` to check code style"
- [other] black and autopep8 for code formatting: "You can use a code formatter like [black](https://github.com/psf/black) or [autopep8](https://github.com/hhatto/autopep8)"
- [other] Run pytest to execute tests from repository root: "you can just `cd` to the root of your repository and run `pytest`"
