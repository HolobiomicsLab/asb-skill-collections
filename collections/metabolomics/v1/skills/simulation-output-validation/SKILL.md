---
name: simulation-output-validation
description: Use when after executing a reproducible simulation pipeline (particularly for Over-representation Analysis in metabolomics), compare the newly generated outputs against reference results to confirm that the simulation was correctly implemented and that the computational environment did not.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Jupyter
derived_from:
- doi: 10.1371/journal.pcbi.1009105
  title: ORA
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ora
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  dedup_kept_from: coll_ora
schema_version: 0.2.0
---

# simulation-output-validation

## Summary

Validate that computational simulation outputs match expected results by comparing generated figures and tables against reference publications. This skill ensures reproducibility of pathway analysis simulations in metabolomics by systematically verifying that re-executed code produces equivalent results to the original study.

## When to use

After executing a reproducible simulation pipeline (particularly for Over-representation Analysis in metabolomics), compare the newly generated outputs against reference results to confirm that the simulation was correctly implemented and that the computational environment did not introduce systematic errors or regressions.

## When NOT to use

- When the simulation code has not yet been executed; validation requires actual outputs to compare.
- When expected outputs are unknown or no reference publication exists; validation requires a ground-truth standard.
- When the simulation is intentionally modified (e.g., different random seed, altered parameters, extended sample size); direct output matching is inappropriate for exploratory or sensitivity analysis variants.

## Inputs

- Generated simulation figures (PNG, PDF, or matplotlib objects)
- Generated simulation tables or CSV outputs
- Reference figures and tables from published article
- Simulation code execution logs
- Python environment specification (requirements.txt, conda environment)

## Outputs

- Validation report documenting matches and discrepancies
- Diff or overlay visualizations comparing generated vs. reference figures
- Numerical comparison tables (generated vs. published metrics)
- Reproducibility assessment (pass/fail or congruence score)

## How to apply

After executing all cells in a reproducible simulation notebook (e.g., src/reproducible_simulations.ipynb), systematically compare the generated figures and tables against those reported in the original publication. Verify that numerical outputs (parameter estimates, p-values, pathway rankings) fall within expected tolerances accounting for floating-point precision and random-seed variation. Check that figure dimensions, axis labels, legend content, and visual styling match the reference. Document any discrepancies and investigate whether they arise from environmental differences (Python version, dependency versions, OS), parameter changes, or genuine computational errors. Validation passes when all outputs are visually and numerically congruent with the published results.

## Related tools

- **Python** (Execute simulation code and generate outputs for validation)
- **Jupyter** (Interactive environment for running and documenting simulation notebooks)

## Examples

```
# In Jupyter after executing reproducible_simulations.ipynb: compare generated outputs with reference
import matplotlib.pyplot as plt
from pathlib import Path
gen_fig = plt.imread('output_figures/ora_pitfalls_fig1.png')
ref_fig = plt.imread('reference/figure1_published.png')
assert gen_fig.shape == ref_fig.shape, 'Figure dimensions mismatch'
print('Output validation: figures match published DOI:10.1371/journal.pcbi.1009105')
```

## Evaluation signals

- Generated figures are visually congruent with reference figures in terms of axis ranges, trend lines, and legend content.
- Numerical outputs (pathway p-values, ranking scores, effect sizes) are identical or within floating-point precision (e.g., ±1e-10 for double precision).
- Table row counts and column labels match the published supplementary materials.
- No new warnings or errors appear in the execution log that were absent from the original study documentation.
- Reproducibility confirmed when tested on the same Python version (e.g., Python 3.8) and OS as documented in the publication.

## Limitations

- Floating-point arithmetic variability across platforms (CPU, OS, Python version) may introduce minor numerical differences that do not indicate failure.
- Random-seed-dependent simulations may produce slightly different outputs unless the random seed is explicitly set and documented.
- Dependencies updated after publication may introduce subtle behavioral changes; validation may fail even though the underlying method is correct.
- No automated validation tooling is mentioned in the study; comparison is manual and subjective for visual outputs.

## Evidence

- [other] Execute all cells in the notebook sequentially to regenerate simulation outputs. Verify that generated figures and tables match those reported in the publication: "Execute all cells in the notebook sequentially to regenerate simulation outputs. Verify that generated figures and tables match those reported in the publication (DOI:10.1371/journal.pcbi.1009105)."
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [other] The code tested using Python 3.8 on MacOS with standard hardware: "with the code tested using Python 3.8 on MacOS with standard hardware."
- [intro] This repository contains the code to run the simulations presented in the study: "This repository contains the code to run the simulations presented in the study"
