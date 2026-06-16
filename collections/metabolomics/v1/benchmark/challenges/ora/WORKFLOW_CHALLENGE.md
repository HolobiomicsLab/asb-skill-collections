# Workflow Challenge: `coll_ora_workflow`


> This repository provides reproducible Python code in a Jupyter notebook for simulating and analyzing Over-representation Analysis (ORA) in metabolomics pathway analysis, enabling users to examine how metabolite detection coverage affects ORA statistical outcomes.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

The study presents a Jupyter notebook-based implementation (src/reproducible_simulations.ipynb) containing Python code tested on Python 3.8 with standard hardware that enables reproduction of reported ORA simulation results and analysis of how metabolite detection coverage impacts ORA p-value distributions. The code implements the background-set selection mechanism for ORA pathway analysis in metabolomics and allows users to adapt the simulations for application to their own data.

## Research questions

- Can the Python simulation code in the reproducible_simulations.ipynb notebook be executed to regenerate the results demonstrating pitfalls and best practices for Over-representation Analysis in metabolomics?
- How does the fraction of metabolites detected (coverage) relative to the pathway database affect the distribution of ORA p-values and false-positive rates in metabolomics pathway analysis?
- How is the background set of metabolites constructed for Over-representation Analysis (ORA) in metabolomics, given an experimental detection list and a metabolomics pathway database?

## Methods overview

Clone the cwieder/metabolomics-ORA repository to obtain the reproducible simulation notebook and dependencies. Install Python 3.8 and all required packages specified in the repository environment configuration. Execute the Jupyter notebook src/reproducible_simulations.ipynb cell-by-cell to run ORA simulations. Collect all generated figures and tables demonstrating ORA pitfalls and best-practice recommendations. Validation: regenerated outputs match figures and tables published in DOI:10.1371/journal.pcbi.1009105. Clone the metabolomics-ORA repository containing the simulation framework and pathway database. Execute the Jupyter notebook simulation workflow, varying the fraction of detected metabolites across coverage levels (e.g., 10–100%). For each coverage level, run ORA on simulated metabolite sets and collect p-value distributions and false-positive counts at p < 0.05 threshold. Aggregate simulation results into a summary statistics table containing coverage percentage, ORA p-value summary statistics (mean, median, quartiles), and false-positive rate with confidence intervals. Generate line plots of false-positive rate versus coverage and distribution plots (boxplots or violin plots) of p-values across coverage levels. Validation: confirm that false-positive rate tracks expected behavior with coverage (increasing or decreasing according to the pathway composition), and verify that p-value distributions show systematic shift with coverage level. Load the metabolomics pathway database and map metabolites to pathway annotations. Load the experimental detection list of metabolites identified in the study. Construct the background set by selecting all metabolites in the database that are NOT in the experimental detection list. Apply any study-specific filtering rules (e.g., minimum pathway coverage, metabolite measurement feasibility). Compute background-set statistics: total size, per-pathway counts, and overlap validation. Validation: confirm background set size, pathway coverage distribution, and absence of detection-list metabolites; verify no pathway is empty after background construction.

**Domain:** metabolomics

**Techniques:** pathway-analysis, enrichment-analysis, statistical-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The study presents code to run simulations in a Jupyter notebook. _[grounded: tool_jupyter_notebook]_
- **(finding)** Users can adapt the code in the notebook to perform simulations on their own data.
- **(finding)** All code has been tested using Python 3.8 on MacOS version 11.2.3. _[grounded: tool_python38]_
- **(finding)** Code testing was performed with 16GB RAM standard hardware.
- **(finding)** The article addresses pitfalls and best practice for the use of Over-representation Analysis in pathway analysis. _[grounded: ORA_method]_
- **(finding)** The research is conducted by authors from the Department of Metabolism, Digestion, and Reproduction at Imperial College London.
- **(finding)** The research involves collaboration with INRA, Toulouse University, INP, UMR 1331, Toxalim Research Centre in Food Toxicology.
- **(finding)** The repository can be cloned from GitHub at the URL github.com/cwieder/metabolomics-ORA.git.

## Steps

### Step `task_001`
- Title: Reproduce the ORA simulation results reported in the study
- Task kind: `reproduction`
- Task: Execute the reproducible_simulations.ipynb Jupyter notebook from the cwieder/metabolomics-ORA GitHub repository using Python 3.8 to regenerate simulation outputs (figures and tables) that demonstrate pitfalls and best-practice recommendations for Over-representation Analysis (ORA) in metabolomics.
- Inputs:
  - cwieder/metabolomics-ORA GitHub repository (https://github.com/cwieder/metabolomics-ORA.git)
  - Python 3.8 runtime environment
- Expected outputs:
  - Simulation figures and tables demonstrating ORA pitfalls and best practices in metabolomics
- Tools: Python, Jupyter
- Landmark output files: src/reproducible_simulations.ipynb, simulation_figures/*.png, simulation_tables/*.csv

### Step `task_002`
- Depends on: `task_001`
- Title: Analyze the effect of metabolomics-specific coverage bias on ORA p-value distributions
- Task kind: `analysis`
- Task: Re-run the ORA simulation framework to quantify how metabolite detection coverage (fraction of pathway database detected) affects ORA p-value distributions and false-positive rates. Generate a summary statistics table and visualization of coverage-dependent FPR trends.
- Inputs:
  - metabolomics-ORA repository (github:cwieder/metabolomics-ORA)
  - Jupyter notebook with simulation code and pathway database
- Expected outputs:
  - Summary statistics table (CSV or TSV) with coverage levels, ORA p-value statistics, and false-positive rates
  - Figure(s) showing false-positive rate and ORA p-value distribution as a function of metabolite detection coverage
- Tools: Python, Jupyter
- Landmark output files: simulation_results_raw.pkl, coverage_stats_table.csv, fpr_vs_coverage.png, pvalue_distribution_boxplots.png
- Primary expected artifact: `coverage_fpr_summary.csv`

### Step `task_003`
- Title: Reconstruct the background-set selection component of the ORA pipeline
- Task kind: `component_reconstruction`
- Task: Implement the background-set construction procedure for Over-representation Analysis (ORA) in metabolomics given an experimental detection list and a metabolomics pathway database. Produce a background set and verify its size and composition match the expected statistical properties.
- Inputs:
  - Metabolomics pathway database (e.g., KEGG, Reactome, or custom database with metabolite-to-pathway mappings)
  - Experimental detection list: set of metabolites detected in the study
- Expected outputs:
  - Background set: structured list of metabolites forming the statistical background for ORA
  - Background-set statistics: JSON or CSV report with total count, per-pathway counts, and composition metrics
- Tools: Python, Jupyter
- Landmark output files: background_set_raw.json, background_set_stats.csv
- Primary expected artifact: `background_set_stats.csv`

## Final expected outputs

- `Summary statistics table (CSV or TSV) with coverage levels, ORA p-value statistics, and false-positive rates` (type: file, tolerance: hash)
- `Figure(s) showing false-positive rate and ORA p-value distribution as a function of metabolite detection coverage` (type: file, tolerance: hash)
- `Background set: structured list of metabolites forming the statistical background for ORA` (type: file, tolerance: hash)
- `Background-set statistics: JSON or CSV report with total count, per-pathway counts, and composition metrics` (type: file, tolerance: hash)

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
  "workflow_id": "coll_ora_workflow",
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
    "Summary statistics table (CSV or TSV) with coverage levels, ORA p-value statistics, and false-positive rates": "<locator>",
    "Figure(s) showing false-positive rate and ORA p-value distribution as a function of metabolite detection coverage": "<locator>",
    "Background set: structured list of metabolites forming the statistical background for ORA": "<locator>",
    "Background-set statistics: JSON or CSV report with total count, per-pathway counts, and composition metrics": "<locator>"
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
