# Workflow Challenge: `coll_ms2query_workflow`


> MS2Query is a tool for reliable and fast MS/MS spectral-based analogue search. This repository documents the software's installation, usage, and contribution guidelines.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MS2Query provides functionality for MS/MS spectral-based analogue search and library matching. The repository contains installation instructions, command-line usage documentation, and guidelines for integrating MS2Query into other tools, creating custom spectral libraries, and training new models. The project uses a GitHub Actions continuous integration workflow that triggers on pull requests and integrates with Sonarcloud for quality assurance.

## Research questions

- How is the MS2Query search workflow architecturally split into separate processing branches for true library matches versus analogue search?
- How does the refactored Library Matching Module read spectral library data from a SQLite database and return candidate matches for query spectra?
- How does the scoring module compute average InChIKey score and neighbourhood score for candidate matches in MS2Query?
- What spectrum pre-processing functions are defined and applied to raw query spectra before library matching in MS2Query?
- How does the MS2Query GitHub Actions continuous-integration workflow integrate build/test execution with Sonarcloud static analysis to produce automated quality reports and passing CI status badges?

## Methods overview

Access the MS2Query repository and retrieve PR #72 metadata, commit history, and code diffs. Identify the top-level orchestrator or workflow entry point and trace the control flow that decides between library-match and analogue-search branches. Document decision criteria, parameter dependencies, and data routing for each branch. Map intermediate scoring, filtering, and result-merging logic that connect the two branches. Validation: cross-verify the documented architecture against the actual codebase implementation to confirm all routing logic and decision nodes are accurately represented. Load spectral library from SQLite database and index by precursor m/z for fast range queries. Parse input query spectra and extract precursor mass and fragment peaks. Filter library entries by precursor mass tolerance window around each query precursor. Compute spectral similarity scores (e.g., cosine similarity, dot product) for filtered candidates. Rank candidates by similarity score and return structured output with library identifiers and scores. Validation: candidate matches are returned with correct library entry identifiers and ranked in descending order of match score; database query executes without errors and matches expected test cases in PR #65 test suite. Load candidate match records from upstream library-matching module, retaining match IDs and InChIKey annotations. Compute average InChIKey score per candidate by aggregating structural similarity across InChIKey layers. Compute neighbourhood score per candidate by evaluating spectral feature-space density and proximity of similar matches. Merge both scores into a single standardized candidate record structure with ID, InChIKey score, and neighbourhood score fields. Validate: Unit tests confirm score ranges are within expected bounds (e.g. 0–1 or 0–100), record structure matches specification, and output file is machine-readable CSV or JSON. Define spectral normalisation algorithm signature accepting raw m/z-intensity pairs and output parameters (e.g., TIC normalisation, L2 normalisation) Define spectral filtering algorithm signature accepting intensity threshold and minimum peak count parameters Implement normalisation function to rescale intensities while preserving relative abundance ratios Implement filtering function to remove peaks below noise threshold and handle edge cases Chain normalisation and filtering functions into a single pre-processing pipeline function Write unit tests validating normalisation output sums to expected value and filtering removes correct peaks Validation: cleaned spectra pass format validation (numeric m/z and intensity fields present), test suite passes with 100% coverage of pre-processing functions, and intensity distributions reflect expected normalisation Create a GitHub Actions workflow YAML file that specifies trigger events (push and pull requests) and job configuration for the ms2query repository. Define a Python test job matrix that executes `python setup.py test` to validate the existing test suite passes on each workflow trigger. Integrate Sonarcloud analysis action into the workflow to perform static code scanning and generate code quality metrics. Commit and push the workflow file to a feature branch in the ms2query repository to activate CI/CD automation. Execute the workflow via a test commit or pull request to validate job execution, generate the CI status badge, and retrieve the Sonarcloud quality report. Validation: Confirm CI status badge displays in repository README, workflow YAML file is valid and registered in GitHub Actions, and Sonarcloud report contains code coverage and quality gate metrics.

**Domain:** metabolomics

**Techniques:** analog-search, cosine-similarity-scoring, database-annotation, metabolite-identification, spectral-library-matching, tandem-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MS2Query is a tool for reliable and fast MS/MS spectral-based analogue search. _[grounded: ms2query_system]_
- **(finding)** MS2Query can be built into other tools. _[grounded: ms2query_system]_
- **(finding)** MS2Query allows users to create their own library without training new models. _[grounded: ms2query_system]_
- **(finding)** MS2Query supports training new models. _[grounded: ms2query_system]_
- **(finding)** Contributors should announce their plans to the rest of the community before starting work on code base changes.
- **(finding)** Contributors should wait until consensus is reached about their idea being a good idea before proceeding.
- **(finding)** Contributors must run existing tests by executing python setup.py test.
- **(finding)** Contributors should update the CHANGELOG.md file with changes.
- **(finding)** Creating a new release of MS2Query requires write permission on the repository. _[grounded: ms2query_system]_
- **(finding)** The version number should be changed in __version__.py for a new release.
- **(finding)** Library parts were moved to Sqlite in pull request 56. _[grounded: ms2query_system]_
- **(finding)** Spectrum processing functions were defined in pull request 61. _[grounded: ms2query_system]_
- **(finding)** The CI workflow was extended and Sonarcloud was added in pull request 62. _[grounded: ms2query_system]_
- **(finding)** Average inchikey score and neighbourhood score were implemented in pull request 78. _[grounded: ms2query_system]_
- **(finding)** The Streamlit web app was removed in pull request 83. _[grounded: ms2query_system]_
- **(finding)** Library matching was refactored in pull request 65. _[grounded: ms2query_system]_
- **(finding)** The workflow was split into true matches and analog search in pull request 72. _[grounded: ms2query_system]_
- **(finding)** Library files creation was refactored in pull request 74. _[grounded: ms2query_system]_
- **(finding)** MS2Query version 0.1.0 was released on 2021-01-01. _[grounded: ms2query_system]_
- **(finding)** The first MS2Query prototype sketched the basic workflow and a Streamlit web app. _[grounded: ms2query_system]_

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- write permission on the repository required to create release

## Steps

### Step `task_001`
- Title: Reconstruct the MS2Query Search Workflow split into true-match and analogue-search branches
- Task kind: `component_reconstruction`
- Task: Document the architectural split of the MS2Query workflow introduced in PR #72 that bifurcates the search logic into two distinct branches: true library matching and analogue search. Produce a control-flow diagram or specification file describing the top-level orchestration logic, decision points, and routing between these branches.
- Inputs:
  - MS2Query repository at https://github.com/iomega/ms2query, specifically PR #72 and associated commit history
- Expected outputs:
  - Control-flow specification or architectural diagram documenting the two-branch orchestration logic (library-match vs. analogue-search), decision criteria, and routing for MS2Query workflow as introduced in PR #72
- Tools: GitHub, MS2Query, Python
- Landmark output files: pr72_commit_list.txt, branch_decision_logic.py, workflow_routing_diagram.svg
- Primary expected artifact: `workflow_architecture_pr72.md`

### Step `task_002`
- Title: Reconstruct the Library Matching Module backed by SQLite storage
- Task kind: `component_reconstruction`
- Task: Implement the refactored Library Matching Module that queries a SQLite spectral library database and returns ranked candidate matches for input query spectra. Output a structured list of candidate library entries with their identifiers and match scores.
- Inputs:
  - SQLite spectral library database file
  - Query MS/MS spectra (m/z and intensity pairs)
- Expected outputs:
  - Structured candidate match list with library entry identifiers and match scores
- Tools: MS2Query, Python, GitHub
- Landmark output files: spectral_library_schema.sql, query_spectra_parsed.csv, precursor_filtered_candidates.csv, ranked_matches.json
- Primary expected artifact: `candidate_matches.json`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct the Scoring Module computing average InChIKey and neighbourhood scores
- Task kind: `component_reconstruction`
- Task: Implement the Scoring Module that computes average InChIKey score and neighbourhood score for candidate matches returned by the library-matching step, and output the scored candidate records.
- Inputs:
  - task_001.expected_outputs[0]: Control-flow specification or architectural diagram documenting the two-branch orchestration logic (library-match vs. analogue-search), decision criteria, and routing for MS2Query workflow as introduced in PR #72
  - Candidate match records from library-matching step
- Expected outputs:
  - Scored candidate matches with average InChIKey score and neighbourhood score fields
  - Test results verifying score computation correctness
- Tools: MS2Query, Python, GitHub
- Landmark output files: candidate_matches_loaded.json, inchikey_scores_intermediate.csv, neighbourhood_scores_intermediate.csv, scoring_tests_passed.log
- Primary expected artifact: `scored_candidates.csv`

### Step `task_004`
- Depends on: `task_002`
- Title: Reconstruct the Spectrum Processing Module defining query-spectrum processing functions
- Task kind: `component_reconstruction`
- Task: Reconstruct the spectrum pre-processing module (PR #61) that defines and applies normalisation, filtering, and related functions to raw query spectra before library matching, producing cleaned spectrum outputs suitable for downstream MS/MS analogue search.
- Inputs:
  - Raw query mass spectra in MS/MS format (e.g., m/z-intensity pairs)
  - MS2Query repository fork with feature branch
- Expected outputs:
  - Cleaned query spectra with normalised intensities and filtered peaks
  - Pre-processing module source code with test suite
  - Updated CHANGELOG.md documenting spectrum processing module changes
- Tools: MS2Query, Python, GitHub
- Landmark output files: spectrum_normalisation.py, spectrum_filtering.py, test_preprocessing_module.py, cleaned_spectra_sample.csv
- Primary expected artifact: `preprocessing_module.py`

### Step `task_005`
- Depends on: `task_004`
- Title: Reconstruct the CI pipeline integrating GitHub Actions and Sonarcloud quality gates
- Task kind: `component_reconstruction`
- Task: Construct and validate a GitHub Actions continuous-integration workflow (PR #62) that integrates automated Python test execution with Sonarcloud static code analysis, producing a passing CI status badge and a Sonarcloud quality report for the ms2query codebase.
- Inputs:
  - ms2query GitHub repository source code and existing test suite
  - GitHub Actions workflow configuration template for CI/CD integration
- Expected outputs:
  - GitHub Actions workflow YAML file defining PR #62 CI/CD pipeline
  - CI status badge displaying workflow pass/fail state in repository README
  - Sonarcloud quality report with code metrics, coverage analysis, and quality gate assessment
- Tools: MS2Query, GitHub, Python, GitHub Actions
- Landmark output files: .github/workflows/ci.yml, test_execution.log, sonarcloud_analysis.json, ci_badge.svg
- Primary expected artifact: `.github/workflows/ci.yml`

## Final expected outputs

- `Scored candidate matches with average InChIKey score and neighbourhood score fields` (type: file, tolerance: hash)
- `Test results verifying score computation correctness` (type: file, tolerance: hash)
- `GitHub Actions workflow YAML file defining PR #62 CI/CD pipeline` (type: file, tolerance: hash)
- `CI status badge displaying workflow pass/fail state in repository README` (type: file, tolerance: hash)
- `Sonarcloud quality report with code metrics, coverage analysis, and quality gate assessment` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** implicit

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_ms2query_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Scored candidate matches with average InChIKey score and neighbourhood score fields": "<locator>",
    "Test results verifying score computation correctness": "<locator>",
    "GitHub Actions workflow YAML file defining PR #62 CI/CD pipeline": "<locator>",
    "CI status badge displaying workflow pass/fail state in repository README": "<locator>",
    "Sonarcloud quality report with code metrics, coverage analysis, and quality gate assessment": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
