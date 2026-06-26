---
name: over-representation-analysis-workflow
description: Use when when you need to reproduce published ORA simulation results,
  validate pathway enrichment findings from a metabolomics study, or examine pitfalls
  and practices in Over-representation Analysis methodology.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Jupyter
  - metabolomics-ORA
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1009105
  title: ORA
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ora_cq
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  dedup_kept_from: coll_ora_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009105
  all_source_dois:
  - 10.1371/journal.pcbi.1009105
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# over-representation-analysis-workflow

## Summary

Execute a complete Over-representation Analysis (ORA) simulation workflow in a Jupyter notebook to reproduce pathway enrichment results and validate ORA methodology in metabolomics. This skill involves cloning a versioned repository, configuring the Python environment, running sequential notebook cells, and collecting validated output artifacts.

## When to use

When you need to reproduce published ORA simulation results, validate pathway enrichment findings from a metabolomics study, or examine pitfalls and best practices in Over-representation Analysis methodology. Use this skill specifically when a study provides a reproducible Jupyter notebook containing executable ORA code and you have access to a local development environment.

## When NOT to use

- Your Python version is not 3.8 or compatible with the declared environment; dependency conflicts will prevent notebook execution and invalidate results.
- You require interactive parameter tuning or custom ORA configurations beyond what the fixed notebook cells provide; this workflow is designed for exact reproduction, not modification.
- The metabolomics study did not publish its ORA code in a Jupyter notebook or repository; you have only the paper's written methods and cannot access executable source.

## Inputs

- metabolomics-ORA GitHub repository (cwieder/metabolomics-ORA)
- Python 3.8 interpreter with pip or conda
- Jupyter notebook environment

## Outputs

- Generated simulation plots (publication-quality figures)
- CSV tables with pathway enrichment statistics
- Simulation logs documenting execution state
- Intermediate data artifacts from sequential cell execution

## How to apply

Clone the metabolomics-ORA repository from GitHub, establish a Python 3.8 environment with all declared dependencies installed, launch Jupyter, and sequentially execute all cells in src/reproducible_simulations.ipynb. The notebook generates intermediate and final simulation artifacts (plots, CSV tables, logs) that directly correspond to pathway analysis results reported in the study. Validate correctness by comparing output file schemas, checking that CSV tables contain expected columns and row counts, confirming plots render without errors, and verifying that numerical results align with published figures and tables. The workflow tests reproducibility at the code execution level, not just theoretical validity.

## Related tools

- **Python** (Execution engine for ORA simulation code; version 3.8 required)
- **Jupyter** (Interactive notebook interface for executing sequential ORA simulation cells and generating inline outputs)
- **metabolomics-ORA** (Source repository containing reproducible simulation code within src/reproducible_simulations.ipynb) — https://github.com/cwieder/metabolomics-ORA

## Examples

```
git clone https://github.com/cwieder/metabolomics-ORA.git && cd metabolomics-ORA && python -m venv env && source env/bin/activate && pip install -r requirements.txt && jupyter notebook src/reproducible_simulations.ipynb
```

## Evaluation signals

- All notebook cells execute without errors and complete in reasonable time (<5 min typical for simulations)
- Output CSV files contain expected column headers (e.g., pathway ID, p-value, adjusted p-value) and non-zero row counts matching published result tables
- Generated plots (e.g., ROC curves, enrichment distributions) render without missing data or axis labels and visually match figures in the published article
- Numerical results (p-values, effect sizes, pathway rankings) in CSV outputs are identical or within floating-point precision to printed results in the paper
- No warnings or deprecated function calls appear in execution logs; dependencies resolve cleanly on first install

## Limitations

- Reproducibility is limited to Python 3.8; newer Python versions may introduce breaking changes in upstream dependencies not declared in the repository.
- The fixed notebook workflow does not support parameter exploration or methodological variants; to test alternative ORA configurations you must modify and re-execute cells, which falls outside this skill's scope.
- No changelog is provided in the repository, so it is unclear whether the notebook has been updated since initial publication or if historical versions are archived elsewhere.
- The workflow validates code execution and artifact generation but does not validate the statistical soundness or biological validity of the ORA findings themselves; see the article for methodological critique.

## Evidence

- [intro] This repository contains the code to run the simulations presented in the study.: "This repository contains the code to run the simulations presented in the study."
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [intro] Python 3.8 on MacOS (v11.2.3) and Jupyter notebook src/reproducible_simulations.ipynb: "Python 3.8 on MacOS (v11.2.3)"
- [other] 1. Clone the metabolomics-ORA repository from github:cwieder/metabolomics-ORA. 2. Set up Python 3.8 environment and install required dependencies specified in the repository. 3. Launch Jupyter and open src/reproducible_simulations.ipynb. 4. Execute all cells sequentially to run the ORA simulations, generating intermediate and final result artifacts.: "1. Clone the metabolomics-ORA repository from github:cwieder/metabolomics-ORA. 2. Set up Python 3.8 environment and install required dependencies specified in the repository. 3. Launch Jupyter and"
- [other] Collect and validate all output files (plots, CSV tables, simulation logs) produced by the notebook execution.: "Collect and validate all output files (plots, CSV tables, simulation logs) produced by the notebook execution."
