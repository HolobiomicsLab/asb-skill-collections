---
name: pipeline-end-to-end-execution-and-validation
description: Use when you have a published computational pipeline with deposited code and validation data, and you need to verify that the pipeline can be executed end-to-end to reproduce reported validation metrics (annotation accuracy, coverage, or equivalent performance benchmarks).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3697
  tools:
  - HassounLab/BAM
  - PROXIMAL2
  - GNN-SOM
  - BAM
derived_from:
- doi: 10.1021/acs.analchem.4c01565
  title: bam
evidence_spans:
- HassounLab/BAM
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bam
    doi: 10.1021/acs.analchem.4c01565
    title: bam
  dedup_kept_from: coll_bam
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01565
  all_source_dois:
  - 10.1021/acs.analchem.4c01565
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pipeline-end-to-end-execution-and-validation

## Summary

Execute a complete bioinformatics pipeline (BAM) on a validation dataset and compare predicted outputs against reference annotations to assess reproduction of reported metrics. This skill validates that a computational method produces expected results when applied to the same data used in the original study.

## When to use

You have a published computational pipeline with deposited code and validation data, and you need to verify that the pipeline can be executed end-to-end to reproduce reported validation metrics (annotation accuracy, coverage, or equivalent performance benchmarks). This is the appropriate skill when assessing computational reproducibility of a method or when setting up a baseline implementation before applying the pipeline to new data.

## When NOT to use

- The pipeline code is not available or cannot be compiled/executed in your computational environment (missing dependencies or incompatible OS).
- You do not have access to the original validation dataset or reference annotations; without ground truth, you cannot assess metric reproducibility.
- Your goal is to apply the pipeline to a novel metabolomics dataset rather than validate reproducibility of reported results; in that case, focus on configuring inputs and interpreting outputs rather than comparison to a reference.

## Inputs

- Pipeline repository code (HassounLab/BAM codebase)
- Validation dataset: CSV file of queries with identifier, mass, anchor SMILES, and known ground-truth structures
- Reaction dataset: metabolites_list (CSV with structure SMILES), reaction_list (CSV with id, formula, EC columns)
- Conda environment specifications for PROXIMAL2 and GNN-SOM dependencies

## Outputs

- Ranked molecular structure candidates for each query suspect
- Validation metrics report: annotation accuracy (e.g., percentage correct structures in top-1, top-5 rankings), coverage (percentage of queries with predictions)
- Performance benchmarks (runtime, memory usage if applicable)
- Log files documenting pipeline execution and any errors

## How to apply

Clone or obtain the pipeline repository (HassounLab/BAM) and verify the codebase is intact and dependencies are configured. Retrieve the deposited validation dataset comprising input data (untargeted metabolomics profiles) and reference annotations (ground-truth molecular structures). Configure the pipeline with the parameters documented in the original study (biotransformation rules source—KEGG or RetroRules; molecular networking settings; reaction datasets). Execute the pipeline end-to-end by invoking the main entry point (runBAM.sh) with default or specified configuration variables. Compute validation metrics by comparing pipeline predictions (structure candidates and rankings) against reference annotations, measuring annotation accuracy (correct structures ranked in top-N) and coverage (fraction of queries with any candidate). Generate a metrics report documenting achieved performance; discrepancies from reported values may indicate missing dependencies (e.g., PROXIMAL2, GNN-SOM), configuration drift, or incomplete data.

## Related tools

- **PROXIMAL2** (Dependency for biotransformation operator generation and metabolite pathway prediction) — https://github.com/HassounLab/PROXIMAL2
- **GNN-SOM** (Dependency for site-of-metabolism prediction to rank biotransformation candidates) — https://github.com/HassounLab/GNN-SOM
- **BAM** (Primary pipeline implementing biotransformation-based annotation method for molecular structure discovery) — https://github.com/HassounLab/BAM

## Examples

```
sh runBAM.sh
```

## Evaluation signals

- Pipeline executes without errors when runBAM.sh is invoked with default configuration and provided validation data.
- Predicted structure candidates are output in the specified WRITE_DIRECTORY with consistent format (e.g., ranked list per query).
- Annotation accuracy and coverage metrics computed against reference annotations match or are very close to (within 1–2 percentage points of) reported values in the article.
- All output files are generated (operators cache, final reaction pairs, ranked candidates) and are non-empty.
- Runtime and memory usage are reasonable and documented; extremely slow execution or out-of-memory errors may indicate misconfiguration.

## Limitations

- The pipeline requires two external conda environments (proximal2 and som) to be pre-installed and correctly named; misconfiguration of these dependencies is a common source of failure.
- The validation dataset is tied to a specific reaction source (KEGG or RetroRules); switching reaction datasets requires manual reconfiguration of four variables in runBAM.sh and re-execution, which may be error-prone.
- No changelog is available in the repository, so tracking changes between versions or understanding what was modified is difficult.
- The method is designed for untargeted metabolomics and global molecular networks; applicability to other spectral library sources or targeted assays is not discussed.

## Evidence

- [other] Does the BAM pipeline, when executed end-to-end on the deposited validation dataset, reproduce the reported validation metrics for molecular structure discovery from untargeted metabolomics data?: "Does the BAM pipeline, when executed end-to-end on the deposited validation dataset, reproduce the reported validation metrics"
- [other] Execute the BAM pipeline end-to-end on the validation data to generate structure annotations. Compute validation metrics (annotation accuracy, coverage) by comparing pipeline predictions against reference annotations.: "Execute the BAM pipeline end-to-end on the validation data to generate structure annotations. Compute validation metrics (annotation accuracy, coverage) by comparing pipeline predictions against"
- [readme] This repository contains code to implement the biotransformation-based annotation method (BAM), as well as the data used to validate BAM.: "This repository contains code to implement the biotransformation-based annotation method (**BAM**), as well as the data used to validate BAM"
- [readme] BAM uses previous tools, PROXIMAL2 and GNN-SOM. To use BAM, these tools need to be downloaded and included under the BAM-main directory. Also, both conda environments need to be created as described in those repositories and named proximal2 and som respectively.: "BAM uses previous tools, PROXIMAL2 and GNN-SOM. To use BAM, these tools need to be downloaded and included under the "BAM-main" directory. Also, both conda environments need to be created"
- [readme] Once the code and conda environments are structured as specified in the Installation and Requirements section above, run the runBAM.sh file as it is to run the algorithm with the files as described here.: "run the runBAM.sh file as it is to run the algorithm with the files as described here"
