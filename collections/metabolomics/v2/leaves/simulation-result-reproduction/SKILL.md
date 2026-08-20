---
name: simulation-result-reproduction
description: Use when when you have access to a study's source repository containing
  executable simulation code in a Jupyter notebook, and you need to validate that
  the reported ORA results can be regenerated from the provided Python implementation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3678
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Jupyter
  - metabolomics-ORA repository
  license_tier: open
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

# simulation-result-reproduction

## Summary

Execute a published Jupyter notebook containing Over-representation Analysis (ORA) simulations to regenerate pathway analysis results and validate computational reproducibility. This skill verifies that simulation code runs end-to-end and produces the intermediate and final artifacts reported in the study.

## When to use

When you have access to a study's source repository containing executable simulation code in a Jupyter notebook, and you need to validate that the reported ORA results can be regenerated from the provided Python implementation. Use this skill to verify reproducibility before adapting or extending the simulation methodology.

## When NOT to use

- When the repository contains only raw data but no executable notebook — use data processing or analysis setup skills instead.
- When Python dependencies cannot be installed or environment setup fails — first troubleshoot environment compatibility.
- When the study provides only final results figures without intermediate code artifacts — you cannot validate intermediate computational steps.

## Inputs

- Jupyter notebook file (src/reproducible_simulations.ipynb)
- Python 3.8 environment with installed dependencies
- Repository source code (metabolomics-ORA)

## Outputs

- CSV tables containing simulation results
- PNG/PDF plots and figures
- Simulation logs and execution artifacts
- Numerical result data matching study findings

## How to apply

Clone the source repository (github:cwieder/metabolomics-ORA) to a local environment. Install Python 3.8 and all dependencies specified in the repository's requirements or setup documentation. Launch Jupyter and open the reproducible_simulations.ipynb notebook. Execute all cells sequentially from top to bottom, monitoring for runtime errors or incomplete execution. Collect all output artifacts (plots, CSV tables, simulation logs, intermediate result files) produced by cell execution. Cross-validate the generated artifacts against the figures, tables, and numerical results reported in the study's main text and supplementary materials to confirm quantitative and visual consistency.

## Related tools

- **Python** (Execution runtime for simulation code and numerical computation)
- **Jupyter** (Interactive notebook environment for running and validating sequential simulation cells)
- **metabolomics-ORA repository** (Source repository containing the reproducible_simulations.ipynb notebook and all simulation code) — https://github.com/cwieder/metabolomics-ORA

## Examples

```
jupyter notebook src/reproducible_simulations.ipynb
```

## Evaluation signals

- All notebook cells execute without runtime errors or unhandled exceptions
- Output files are generated with expected naming conventions and non-zero file sizes
- Numerical values in generated CSV tables match (within floating-point tolerance) the results reported in the study's figures and tables
- Plot dimensions, axis labels, and visual elements in generated plots correspond to published study figures
- Simulation logs or execution traces indicate completion of all major computational steps described in the notebook comments or study methods

## Limitations

- Reproducibility depends on exact Python 3.8 version and compatible dependency versions — environment drift may cause failures
- No changelog is available in the repository to document changes to the notebook between study publication and current state
- Results are reproducible only on systems compatible with the study's original runtime environment (noted as macOS v11.2.3 in the paper)

## Evidence

- [intro] This repository contains the code to run the simulations presented in the study.: "This repository contains the code to run the simulations presented in the study."
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [intro] Python 3.8 on MacOS (v11.2.3): "Python 3.8 on MacOS (v11.2.3)"
- [intro] Jupyter notebook **src/reproducible_simulations.ipynb**: "Jupyter notebook **src/reproducible_simulations.ipynb**"
- [other] Execute all cells sequentially to run the ORA simulations, generating intermediate and final result artifacts.: "Execute all cells sequentially to run the ORA simulations, generating intermediate and final result artifacts."
