---
name: metabolomics-ora-methodology
description: Use when you have a metabolomics dataset and want to perform pathway
  enrichment analysis using ORA, but need to first understand its behavior, limitations,
  and correct application through reproducible simulation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Jupyter
  - cwieder/metabolomics-ORA
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009105
  title: ORA
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ora
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  dedup_kept_from: coll_ora
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

# metabolomics-ora-methodology

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Reproduce and validate Over-representation Analysis (ORA) simulations in metabolomics to understand pitfalls and apply best practices for pathway enrichment. This skill involves executing Python-based simulations in a Jupyter notebook to regenerate results demonstrating how ORA performs under different experimental conditions and parameter choices.

## When to use

You have a metabolomics dataset and want to perform pathway enrichment analysis using ORA, but need to first understand its behavior, limitations, and correct application through reproducible simulation. Specifically, when you need to validate whether ORA is appropriate for your study design, assess sensitivity to background set composition, or benchmark against alternative enrichment methods.

## When NOT to use

- You have already selected and validated a different pathway enrichment method (e.g., GSEA, FELLA) and do not need to compare approaches.
- Your metabolomics data lacks a defined reference pathway database or metabolite annotation resource required for ORA.
- You are performing real-time production analysis and cannot tolerate the computational time or dependency overhead of notebook-based simulation.

## Inputs

- Python 3.8 environment with dependencies (numpy, pandas, scipy, matplotlib, jupyter)
- cwieder/metabolomics-ORA repository code
- reproducible_simulations.ipynb Jupyter notebook

## Outputs

- Simulation figures and tables demonstrating ORA performance under varying conditions
- Validated results matching those reported in the publication (DOI:10.1371/journal.pcbi.1009105)
- Executable notebook with parameterizable simulation code for custom scenarios

## How to apply

Clone the cwieder/metabolomics-ORA repository and set up a Python 3.8 environment with dependencies. Launch Jupyter and open src/reproducible_simulations.ipynb, then execute all cells sequentially to regenerate simulation outputs. The notebook contains parameterized simulations that demonstrate ORA behavior across different metabolite set sizes, background metabolite frequencies, and sample compositions. Review the generated figures and tables to identify which pitfalls (e.g., bias from unequal metabolite detection rates, sensitivity to background set definition) are relevant to your experimental design. Use these insights to decide whether ORA is suitable and, if so, which best practices to implement (e.g., appropriate background set selection, multiple-testing correction thresholds).

## Related tools

- **Python** (Language for implementing ORA simulation logic and statistical computations)
- **Jupyter** (Interactive notebook environment for executing and documenting reproducible simulation workflows)
- **cwieder/metabolomics-ORA** (Repository containing reference implementation of ORA simulations with best practices documentation) — https://github.com/cwieder/metabolomics-ORA.git

## Examples

```
git clone https://github.com/cwieder/metabolomics-ORA.git && cd metabolomics-ORA && jupyter notebook src/reproducible_simulations.ipynb
```

## Evaluation signals

- Generated figures and numerical tables in the executed notebook match exactly those reported in the publication (DOI:10.1371/journal.pcbi.1009105).
- All notebook cells execute without errors on Python 3.8 with specified dependencies on standard hardware (tested on MacOS).
- Simulation outputs demonstrate expected ORA behavior patterns documented in the article (e.g., sensitivity to background set composition, bias under unequal detection rates).
- Code is executable and reproducible by independent users following the documented workflow steps without manual parameter adjustment.
- The notebook runs to completion in reasonable time (< 1 hour on standard hardware) and produces both tabular and graphical outputs.

## Limitations

- Simulations are tested and validated only on Python 3.8; compatibility with other Python versions is not documented.
- Results are specific to the metabolomics domain and pathway definitions used in the study; transfer to other omics data types (genomics, proteomics) requires separate validation.
- No changelog is provided, limiting ability to track changes or understand version-specific behavior.
- Simulations demonstrate ORA pitfalls but do not include integrated comparison to alternative enrichment methods (GSEA, FELLA, etc.) in a single unified workflow.

## Evidence

- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [intro] This repository contains the code to run the simulations presented in the study: "This repository contains the code to run the simulations presented in the study"
- [intro] Pathway analysis in metabolomics: Pitfalls and best practice for the use of Over-representation Analysis: "Pathway analysis in metabolomics: Pitfalls and best practice for the use of Over-representation Analysis"
- [intro] code tested using Python 3.8 on MacOS with standard hardware: "code tested using Python 3.8 on MacOS with standard hardware"
- [other] Execute all cells in the notebook sequentially to regenerate simulation outputs: "Execute all cells in the notebook sequentially to regenerate simulation outputs"
