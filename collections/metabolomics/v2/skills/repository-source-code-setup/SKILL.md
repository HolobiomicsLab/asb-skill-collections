---
name: repository-source-code-setup
description: Use when you need to validate that a published software tool (e.g., MassQL) executes correctly in your environment, reproduce published results, or contribute to development.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3365
  tools:
  - MassQL
  - GitHub Actions (test-unit.yml workflow)
  - pytest (inferred from test suite structure)
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1038/s41592-025-02785-1
  title: MassQL
evidence_spans:
- The Mass Spec Query Language (MassQL) is a domain specific language meant to be a succinct way to express a query in a mass spectrometry centric fashion.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massql
    doi: 10.1038/s41592-025-02785-1
    title: MassQL
  dedup_kept_from: coll_massql
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02785-1
  all_source_dois:
  - 10.1038/s41592-025-02785-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# repository-source-code-setup

## Summary

Clone a scientific software repository and install its runtime dependencies and test fixtures to prepare the codebase for execution or testing. This skill ensures a reproducible local environment matching the project's configuration before running workflows, unit tests, or analyses.

## When to use

You need to validate that a published software tool (e.g., MassQL) executes correctly in your environment, reproduce published results, or contribute to development. Apply this skill when you have a GitHub repository URL and want to verify the unit test suite or run the tool end-to-end on your own machine.

## When NOT to use

- The tool is already installed in your environment (e.g., via pip install massql) and you do not need to reproduce or develop against the source repository.
- You only need to use the tool as a published package, not inspect or modify its source code.
- The repository is private or inaccessible to you; instead, rely on pre-built Docker images or containerized distributions.

## Inputs

- GitHub repository URL or clone path (string)
- Repository README or configuration files (text/markdown)
- Requirements files (requirements.txt, setup.py, environment.yml, or equivalent)

## Outputs

- Cloned local repository directory with all source code
- Installed Python package with dependencies available in the environment
- Fetched test fixtures and data files (if required by the test suite)
- Test execution report (pass/fail status, test counts, error logs)
- Verification that the tool CLI or API is callable

## How to apply

First, clone the repository from GitHub (e.g., mwang87/MassQueryLanguage) to a local directory. Next, examine the repository structure and README to identify runtime and test dependencies—these may be specified in requirements files (e.g., requirements.txt, requirements_test.txt) or in documentation. Install the core package and its dependencies using the recommended package manager (pip for Python). If the project includes a test suite, fetch additional test fixtures or data (e.g., via scripts like get_data.sh) that are not bundled with the git repo. Verify installation by checking that the tool's API or CLI is available (e.g., `from massql import msql_engine` or `massql --help`). Finally, run the test suite (e.g., via a CI workflow definition like test-unit.yml) to confirm that the installation succeeded and the codebase is functional.

## Related tools

- **MassQL** (Reference implementation of a domain-specific query language for mass spectrometry data; the tool being installed and tested) — https://github.com/mwang87/MassQueryLanguage
- **GitHub Actions (test-unit.yml workflow)** (CI workflow definition that specifies how to execute the unit test suite; consulted to understand the test execution steps) — https://github.com/mwang87/MassQueryLanguage
- **pytest (inferred from test suite structure)** (Test runner implied by the presence of a test suite; typically specified in requirements_test.txt)

## Examples

```
cd /tmp && git clone https://github.com/mwang87/MassQueryLanguage.git && cd MassQueryLanguage && pip install -r requirements_test.txt && cd tests && sh ./get_data.sh && cd .. && python -m pytest tests/
```

## Evaluation signals

- Repository successfully clones without authentication errors and contains the expected directory structure (Language Grammar, Reference Implementation, CLI, workflows).
- All core and test dependencies install without errors or unresolved version conflicts; `pip show massql` or `from massql import msql_engine` confirms the package is available.
- Test fixtures are fetched completely (e.g., `cd tests && sh ./get_data.sh` completes without errors); data files are present in the test directory.
- Unit test suite executes and the test-unit.yml CI badge shows a passing status (green check); test output reports zero failures or expected/acceptable failure counts.
- The command-line tool is callable (e.g., `massql test.mzML "QUERY scaninfo(MS2DATA)" --output_file results.tsv` produces output without import or command-not-found errors).

## Limitations

- Test fixtures and large data files may not be bundled with the git repository; they must be fetched separately via scripts (e.g., get_data.sh), which may require network access or authentication.
- Python version compatibility may vary; the README states the package is tested on Python 3.9 but compatibility with other versions is uncertain.
- CI workflows (test-unit.yml, test-package.yml) are defined for GitHub Actions; execution locally requires a compatible test runner setup, not automatic replication of the CI environment.

## Evidence

- [other] Clone the MassQL repository, install dependencies, execute unit tests, collect results: "1. Clone the MassQL repository (mwang87/MassQueryLanguage) from GitHub. 2. Install dependencies and runtime environment as specified in the repository configuration. 3. Execute the unit test suite"
- [readme] Test fixtures are not bundled and must be fetched separately: "To run tests, you'll need to first fetch some fixtures that are not bundled with the git repo: `cd tests && sh ./get_data.sh`"
- [readme] Test suite requires additional dependencies specified in a separate requirements file: "You will also want to install the extra requirements for the test suite: `pip install -r requirements_test.txt`"
- [readme] Python 3.9 is the tested version; other versions are uncertain: "We currently test massql in python 3.9, but are figuring out other versions if they work or not."
- [readme] Basic Python API invocation after installation: "from massql import msql_engine
results_df = msql_engine.process_query(input_query, input_filename)"
