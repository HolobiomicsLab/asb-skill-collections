# SciTask Card: Reproduce the CI workflow by running the pytest test suite via Hatch

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T17:50:38.861186+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_scanpy/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `benchmark-evaluation`, `data-processing`
- DOI: `10.1186/s13059-017-1382-0`
- GitHub: `scverse/scanpy`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `transcriptomics`
- Subdomains: `rna-seq`, `differential-expression`
- Techniques: `dimensionality-reduction`, `clustering`, `batch-correction`, `normalization`, `statistical-analysis`

## Research Question
Does the Scanpy test suite execute without failures when invoked via the Hatch environment using the standard test command?

## Connected Finding
Scanpy uses pytest for testing and provides a Hatch environment configuration to execute the test suite via the `hatch test` command.

## Task Description
Execute the Scanpy pytest test suite using the Hatch environment to verify all tests pass with zero non-skipped failures, confirming the codebase meets the CI passing state.

## Inputs
- Scanpy repository source code (scverse/scanpy cloned locally)
- hatch.toml configuration file with predefined test environment

## Expected Outputs
- Test execution report with exit code 0 and zero non-skipped test failures
- Console output log from pytest showing all test results and summary statistics

## Artifact References

### Inputs

- `Scanpy repository source code (scverse/scanpy cloned locally)` → **github** `scverse/scanpy` (score 0.2857)

## Landmark Outputs

- `pytest_run.log`
- `test_summary.txt`
- `failed_tests_report.txt`

## Tools
- Scanpy
- pytest
- Hatch
- git
- matplotlib

## Skills
- git-repository-cloning-and-fork-management
- hatch-environment-configuration-and-activation
- pytest-test-suite-execution-and-result-interpretation
- test-failure-diagnosis-and-logging-analysis
- matplotlib-plot-reference-image-comparison
- ci-pipeline-reproducibility-verification

## Workflow Description
1. Fork and clone the scverse/scanpy repository to a local machine using git. 2. Create a development environment using Hatch by running `hatch test` from the repository root, which automatically creates the predefined Hatch environment specified in hatch.toml. 3. Execute the full pytest test suite via `hatch test`, which runs all tests in the scanpy/tests directory with the configured pytest settings. 4. Verify the test run completes with exit code 0 and reports zero non-skipped test failures. 5. (Optional) Run a subset of tests using `-k` patterns or specific test files (e.g., `hatch test test_plotting.py`) for faster iteration during development. 6. Check that any custom matplotlib plot reference images match expected outputs via the image_comparer fixture.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/NKG7.png` | figure | False |
| `figures/Scanpy_Logo.svg` | figure | False |
| `figures/Scanpy_Logo_BrightFG.svg` | figure | False |
| `figures/Scanpy_Logo_RGB.png` | figure | False |
| `figures/cell_types.png` | figure | False |
| `figures/ci_plot-view_attachment-tab.png` | figure | False |
| `figures/ci_plot-view_select-test.png` | figure | False |
| `figures/ci_plot-view_tests-tab.png` | figure | False |
| `figures/expected.png` | figure | False |
| `figures/filter_genes_dispersion.png` | figure | False |
| `figures/louvain.png` | figure | False |
| `figures/paga_paul15.png` | figure | False |
| `figures/paga_planaria.png` | figure | False |
| `figures/spatial-basic-analysis.png` | figure | False |
| `figures/stacked_violin_dotplot_matrixplot.png` | figure | False |
| `figures/timeseries.png` | figure | False |
| `figures/tissue_hires_image.png` | figure | False |
| `figures/tissue_lowres_image.png` | figure | False |
| `figures/tsne_1.3M.png` | figure | False |
| `figures/violin.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found documenting test suite status, recent test modifications, or known failing tests

## Domain Knowledge
- Scanpy's test suite includes both computational tests and visual plot comparison tests; plot tests use the image_comparer fixture which compares generated plots against expected.png reference images stored in scanpy/tests/_images directories.
- The Hatch environment manager automatically handles Python version selection, dependency installation, and isolation; running `hatch test` creates the environment on demand and does not require manual venv activation.
- Pytest exit code 0 indicates all tests passed; a non-zero exit code indicates at least one test failure, and the term 'non-skipped failures' excludes tests marked with pytest.skip decorators, which are expected and do not cause failure.
- The CI badge reported as passing indicates that the main branch successfully runs this test suite in a GitHub Actions or Azure Pipelines environment; local reproduction requires matching the Python version, dependencies, and environment variables used in the CI configuration.
- Pre-commit hooks configured in the repository perform code style checks using Ruff; these may run automatically on git commit if installed locally and could block test execution if style violations are detected, requiring fixes before tests are invoked.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: pytest, Hatch, Test execution report with exit code 0 and zero non-skipped test failures, Console output log from pytest showing all test results and summary statistics.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does the Scanpy test suite execute without failures when invoked via the Hatch environment using the standard test command?: 'We use pytest to test scanpy. To run the tests, simply run `hatch test`'
- `ev_002` from `agent2_synthesis` (agent2_traced): [other] Scanpy uses pytest for testing and provides a Hatch environment configuration to execute the test suite via the `hatch test` command.: 'We use pytest to test scanpy. To run the tests, simply run `hatch test`'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Scanpy repository source code (scverse/scanpy cloned locally): 'Fork the Scanpy repository to your own GitHub account'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] hatch.toml configuration file with predefined test environment: 'Using one of the predefined environments in hatch.toml is as simple as running `hatch test`'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Test execution report with exit code 0 and zero non-skipped test failures: 'We use pytest to test scanpy. To run the tests, simply run `hatch test`'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Console output log from pytest showing all test results and summary statistics: 'To run the tests, simply run `hatch test`'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] pytest: 'We use pytest to test scanpy. To run the tests, simply run `hatch test`'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] Hatch: 'Using one of the predefined environments in hatch.toml is as simple as running `hatch test`'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] git: 'This section of the docs covers our practices for working with git on our codebase'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] matplotlib: 'matplotlib.testing.setup tries to establish a consistent environment for creating plots'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found documenting test suite status, recent test modifications, or known failing tests: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file 'hatch.toml' exists in the repository root
- verify file 'pyproject.toml' exists in the repository root
- script_runs: execute 'hatch run hatch-test' in the scanpy repository directory and confirm exit code is 0
- script_runs: execute 'hatch test' in the scanpy repository directory and confirm exit code is 0
- output_matches_reference: verify that test execution log contains no non-skipped test failures (robust to test count and parameter changes)

### Expert Review
- Verify that the Hatch environment configuration in hatch.toml correctly specifies the test environment and pytest invocation
- Confirm that all declared test dependencies in the Hatch configuration are correctly resolved and available

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Clone the scverse/scanpy repository locally and navigate to the repository root directory.
2. Create and activate the Hatch test environment by invoking `hatch test`, which reads hatch.toml and installs dependencies.
3. Execute the full pytest test suite, which reads pytest configuration and runs all test modules in scanpy/tests with matplotlib plot comparison setup active.
4. Capture and parse the test execution output to confirm exit code is 0 and no non-skipped test failures are reported.
5. Validation: confirm test run exits with code 0 and the summary line reports zero failed tests, matching the CI badge passing state reported by the repository.
6. References: source article (DOI: 10.1186/s13059-017-1382-0)

## Workflow Ports

**Inputs:**

- `scanpy_repo` — Scanpy repository source code
- `hatch_config` — hatch.toml configuration file

**Outputs:**

- `test_report` — Pytest test execution report with exit code and failure count
- `test_log` — Console output from test run showing test results summary

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:scverse__scanpy`
- **Synthesized at:** 2026-06-15T17:57:56+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
