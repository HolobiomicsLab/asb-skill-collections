# Workflow Challenge: `coll_biosynfoni_workflow`


> Biosynfoni is a biosynformatic molecular fingerprint tool tailored for natural product chemistry and bioinformatic research. The paper describes the package's design and demonstrates its test suite execution through GitHub Actions CI.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This work presents biosynfoni, a molecular fingerprint resource designed specifically for natural product chemistry and bioinformatic research applications. The paper reproduces the biosynfoni Python package installation and test suite execution via a GitHub Actions CI workflow. It further analyzes the fingerprint vector distribution across the Zenodo biosynfoni dataset to characterize fingerprint properties. The biosynformatic molecular fingerprint computation for natural product molecules is described as a mechanism underlying the tool, though separate evaluation of this computation is not reported.

## Research questions

- Does the biosynfoni package install successfully from source and pass its full pytest test suite?
- How does the biosynfoni package compute a molecular fingerprint representation tailored for natural product chemistry and bioinformatic research?
- What are the statistical properties of the biosynfoni fingerprint vectors in the deposited dataset, including bit-frequency distributions, sparsity characteristics, and pairwise similarity patterns?

## Methods overview

Obtain biosynfoni source code from the published repository (GitHub or Zenodo). Install biosynfoni in development mode with development dependencies using pip. Execute the pytest test suite against the tests/ directory. Validation: All pytest tests must pass with exit code 0, confirming package installation and functional correctness. Retrieve biosynfoni source from GitHub or Zenodo deposit. Install package in development mode with all dependencies. Load sample molecular structures from dataset. Invoke biosynfoni fingerprint computation on molecule set. Serialize fingerprints to structured output (CSV or NumPy array with molecule identifiers and bit-vectors). Validation: Verify output file format, row count matches molecule count, and fingerprints are non-empty bit-vectors. Install biosynfoni package from source repository using pip in development mode. Load fingerprint vectors from the Zenodo dataset deposit. Compute bit-frequency distribution across all bit positions. Calculate sparsity (zero-bit proportion) for the dataset. Compute all pairwise Tanimoto similarity coefficients. Summarize statistics (mean, median, std dev) for each metric. Generate histogram and density plots for distributions. Validation: confirm all metrics are computed without missing values and visualizations display expected distributional characteristics.

**Domain:** cheminformatics

**Techniques:** molecular-networking, database-annotation, dereplication

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Biosynfoni is a biosynformatic molecular fingerprint tailored to natural product chemistry and bioinformatic research. _[grounded: biosynfoni_system]_
- **(finding)** The project is available on PyPI. _[grounded: biosynfoni_system]_
- **(finding)** Biosynfoni supports multiple Python versions. _[grounded: biosynfoni_system]_
- **(hypothesis)** The project is licensed under an MIT license.
- **(finding)** The code follows the black code style standard. _[grounded: tool_black]_
- **(finding)** Development installation can be performed by running pip install -e .[dev] from the project root. _[grounded: tool_biosynfoni_pkg]_
- **(finding)** Tests can be run locally using the pytest tests/ command. _[grounded: tool_pytest]_
- **(finding)** Code should be formatted with black before submitting a pull request. _[grounded: tool_black]_
- **(finding)** Tests are run automatically when a pull request is pushed.
- **(finding)** The project source is hosted on GitHub at lucinamay/biosynfoni. _[grounded: biosynfoni_system]_
- **(finding)** Contributions to biosynfoni development are welcomed through issues or pull requests. _[grounded: biosynfoni_system]_

## Steps

### Step `task_001`
- Title: Reproduce the biosynfoni Python package installation and test suite execution
- Task kind: `reproduction`
- Task: Install the biosynfoni package from source in development mode and execute the full pytest test suite to verify package functionality and reproducibility.
- Inputs:
  - biosynfoni source code repository (GitHub: lucinamay/biosynfoni or Zenodo: 10.5281/zenodo.14822624)
- Expected outputs:
  - pytest test execution report showing all tests passed
  - Installed biosynfoni package in development mode with dev dependencies
- Tools: pip, pytest, biosynfoni
- Landmark output files: pip_install.log, pytest_output.txt

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the biosynformatic molecular fingerprint computation for a set of natural product molecules
- Task kind: `component_reconstruction`
- Task: Install the biosynfoni Python package from the Zenodo-deposited source and compute molecular fingerprint representations for a sample dataset. Output fingerprints as a structured file (CSV or NumPy array) encoding substructure bit-vectors.
- Inputs:
  - biosynfoni package source code from GitHub repository (lucinamay/biosynfoni) or Zenodo deposit (10.5281/zenodo.14822624)
  - Sample molecular dataset (SMILES strings, MOL files, or SDF format with molecule identifiers)
- Expected outputs:
  - Fingerprint file in CSV or NumPy format containing molecule identifiers and corresponding substructure bit-vector representations
- Tools: biosynfoni, pip, pytest
- Landmark output files: package_installed.log, molecules_parsed.txt
- Primary expected artifact: `biosynfoni_fingerprints.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Analyze the fingerprint vector distribution across the Zenodo biosynfoni dataset
- Task kind: `analysis`
- Task: Load the deposited biosynfoni dataset from Zenodo and compute summary statistics (bit-frequency per position, sparsity, pairwise Tanimoto similarity distribution) across all fingerprint vectors. Output a summary statistics table and distribution visualizations.
- Inputs:
  - Zenodo biosynfoni fingerprint dataset deposit (DOI: 10.5281/zenodo.14822624)
  - biosynfoni package source code repository
- Expected outputs:
  - Summary statistics table containing bit-frequency per position, sparsity, and pairwise Tanimoto similarity distribution metrics
  - Distribution plots (histogram/density) visualizing bit-frequency, sparsity, and Tanimoto similarity across fingerprint vectors
- Tools: biosynfoni, pip
- Landmark output files: fingerprint_vectors_loaded.pkl, bit_frequency_distribution.csv, sparsity_distribution.csv, tanimoto_similarity_matrix.pkl, summary_statistics.csv, bit_frequency_histogram.png
- Primary expected artifact: `fingerprint_summary_statistics.csv`

## Final expected outputs

- `Fingerprint file in CSV or NumPy format containing molecule identifiers and corresponding substructure bit-vector representations` (type: file, tolerance: hash)
- `Summary statistics table containing bit-frequency per position, sparsity, and pairwise Tanimoto similarity distribution metrics` (type: file, tolerance: hash)
- `Distribution plots (histogram/density) visualizing bit-frequency, sparsity, and Tanimoto similarity across fingerprint vectors` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: open — validity-first.** The deterministic match-rubrics above are demoted to *informational*. The binding evaluator is **SCIENTIFIC_VALIDITY** (below). Any scientifically sound method that addresses the research question is valid, and novel findings or unexplored aspects can score positively — **different is not wrong**.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** concrete

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
  "workflow_id": "coll_biosynfoni_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003"
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
    }
  },
  "final_outputs": {
    "Fingerprint file in CSV or NumPy format containing molecule identifiers and corresponding substructure bit-vector representations": "<locator>",
    "Summary statistics table containing bit-frequency per position, sparsity, and pairwise Tanimoto similarity distribution metrics": "<locator>",
    "Distribution plots (histogram/density) visualizing bit-frequency, sparsity, and Tanimoto similarity across fingerprint vectors": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
