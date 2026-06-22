---
name: nextflow-workflow-orchestration
description: Use when when you need to coordinate multiple bioinformatics tools (quality control, alignment, quantification, normalization, batch correction) across diverse compute environments (HPC, cloud, local) while ensuring reproducibility and parameter traceability.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3320
  tools:
  - limma
  - sva
  - ggplot2
  - ComplexHeatmap
  - Nextflow
  - nf-core/modules
  - nf-core/configs
  - Docker
  - Singularity
  - Salmon
  - edgeR
  - sva / ComBat
  - FastQC / trimgalore
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger, limma, sva'
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap'
- 'R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap'
- The pipeline is built using [Nextflow](https://www.nextflow.io) version 23.04.2.5870
- The pipeline is built using [Nextflow](https://www.nextflow.io) version 23.04.2.5870 (IMPORTANT), a workflow tool to run tasks across multiple compute infrastructures
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_multiomicsintegrator_cq
    doi: 10.1093/bioadv/vbae175
    title: MultiOmicsIntegrator
  dedup_kept_from: coll_multiomicsintegrator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbae175
  all_source_dois:
  - 10.1093/bioadv/vbae175
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nextflow-workflow-orchestration

## Summary

Nextflow DSL2 orchestration enables portable, containerized execution of multi-stage bioinformatics pipelines across heterogeneous compute infrastructures using modular process definitions. This skill involves designing and deploying reproducible workflows that compose tools (edgeR, Salmon, FastQC, etc.) into directed acyclic task graphs, with dynamic parameter injection and container isolation per process.

## When to use

When you need to coordinate multiple bioinformatics tools (quality control, alignment, quantification, normalization, batch correction) across diverse compute environments (HPC, cloud, local) while ensuring reproducibility and parameter traceability. Specifically: when processing RNA-seq from raw FASTQ through differential expression analysis, or when integrating multi-omics data requiring sequential preprocessing and analysis stages with configurable parameters.

## When NOT to use

- Input data is already a fully preprocessed feature table with all QC and normalization complete — use direct statistical analysis instead.
- Workflow requires tight iterative feedback or interactive data exploration — Nextflow is batch-oriented; consider R/Python notebooks for exploratory analysis.
- Your institution has no containerization support (Docker/Singularity unavailable) and cannot install nf-core infrastructure — use traditional shell scripts or workflow alternatives.

## Inputs

- Raw FASTQ files or SRA accessions
- Phenotype/samplesheet metadata file
- Reference genome/index (optional, depends on alignment tool)
- Configuration file (params.yml, nextflow.config, institutional profile)
- Count matrix (Salmon output, for preprocessing subworkflows)

## Outputs

- Standardized RData and text-format count matrices
- Normalized and batch-corrected expression matrices
- Quality control reports (FastQC, complexity heatmaps)
- Differential expression results with statistical annotations
- Execution logs and task metadata (.nextflow/logs)
- Provenance and parameter snapshots for reproducibility

## How to apply

Design a Nextflow DSL2 workflow by: (1) decomposing the analysis into discrete processes (e.g., FastQC → trimming → Salmon quantification → preprocessing → differential expression); (2) define each process with explicit input channels, output channels, and container images; (3) chain processes using Nextflow's channel operators to enforce execution dependencies; (4) externalize parameters into YAML or config files (e.g., params_genes.yml specifying filterByExp thresholds, normalization method, batch-correction algorithm); (5) use nf-core/modules where available to standardize module structure and enable tool version pinning; (6) test on small datasets locally, then submit to HPC or cloud via institutional profiles from nf-core/configs. Parameter injection via `-c` flag or profile selection ensures environment-specific resource allocation (executor type, singularity/docker scope, memory/CPU constraints) without modifying the workflow definition.

## Related tools

- **Nextflow** (Core workflow orchestration engine; defines process execution, channel management, and task scheduling across compute infrastructures) — https://www.nextflow.io
- **nf-core/modules** (Modular, standardized Nextflow process library; provides vetted implementations of bioinformatics tools (edgeR, limma, Salmon, FastQC) for reuse across pipelines) — https://github.com/nf-core/modules
- **nf-core/configs** (Institution-specific configuration profiles; enable parameter and executor customization (e.g., SLURM, SGE, cloud) without modifying workflow definition) — https://github.com/nf-core/configs
- **Docker** (Container runtime for process isolation and reproducibility across heterogeneous compute environments) — https://www.docker.com
- **Singularity** (Alternative container runtime, preferred on HPC clusters where Docker is unavailable) — https://sylabs.io
- **Salmon** (Quantifies transcript abundance from FASTQ; output count matrices feed into preprocessing subworkflow)
- **edgeR** (Filtering and normalization of count matrices; implements filterByExp and calcNorm operations in preprocessing)
- **limma** (Batch effect correction and statistical analysis; applies quantile normalization in preprocessing subworkflow)
- **sva / ComBat** (Batch effect removal methods; configurable in params_genes.yml for combat, sva, comsva, svacom strategies)
- **FastQC / trimgalore** (Quality control and adapter trimming stages in RNA-seq preprocessing pipeline)

## Examples

```
nextflow run github.com/ASAGlab/MOI -profile slurm -c params_genes.yml --reads 'data/*_R{1,2}.fastq.gz' --samplesheet metadata.csv
```

## Evaluation signals

- Workflow completes without execution errors; all process outputs match expected schema (RData, text matrix formats for count data; FastQC HTML reports)
- Parameter traceability: nextflow.log and .nextflow/logs directory record all injected parameters (filterByExp threshold, normalization method, batch column name) matching the config file
- Container isolation verified: each process runs in its declared Singularity/Docker image; no host-level tool dependencies required
- Reproducibility test: re-running workflow with identical config and inputs produces bit-identical outputs (or near-identical if RNG-seeded)
- Batch effect correction applied: preprocessed count matrix shows reduced variance across known batch groups (e.g., via PCA or heatmap visual inspection); batch column from samplesheet correctly specified in preprocessing process parameters

## Limitations

- Nextflow DSL2 requires Nextflow version ≥21.10.3; institutional HPC may have older version — requires IT coordination to upgrade
- Container registry access may be restricted on air-gapped networks; offline download via nf-core download tool is recommended but requires pre-staging
- Parameter configuration syntax is case-sensitive and Groovy-based; typos in params.yml or profiles can silently fail or use defaults, necessitating explicit validation steps
- Batch effect correction methods (ComBat, SVA, CoMSVA) assume batch is known and recorded in samplesheet; unknown or mislabeled batches will produce misleading corrections
- Workflow is optimized for linear, DAG-structured pipelines; complex conditional branching or interactive feedback loops may require custom process design

## Evidence

- [readme] The pipeline is built using Nextflow version 23.04.2.5870 (IMPORTANT), a workflow tool to run tasks across multiple compute infrastructures: "The pipeline is built using [Nextflow](https://www.nextflow.io) version 23.04.2.5870 (IMPORTANT), a workflow tool to run tasks across multiple compute infrastructures"
- [readme] It uses Docker/Singularity containers making installation trivial and results highly reproducible. The Nextflow DSL2 implementation of this pipeline uses one container per process: "It uses Docker/Singularity containers making installation trivial and results highly reproducible. The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline"
- [other] The preprocess_matrix subworkflow supports three configurable preprocessing operations: filtering via filterByExp or cutoff values, normalization using calcNorm or quantile methods, and batch effect correction using combat, sva, comsva, or svacom approaches: "The preprocess_matrix subworkflow supports three configurable preprocessing operations: filtering via filterByExp or cutoff values, normalization using calcNorm or quantile methods, and batch effect"
- [other] Apply filterByExp filtering using edgeR to retain features meeting minimum expression thresholds as specified in params_genes.yml. Apply quantile normalization to the filtered count matrix using the limma package. Apply batch-effect correction using ComBat or SVA (as configured in params_genes.yml): "Apply filterByExp filtering using edgeR to retain features meeting minimum expression thresholds as specified in params_genes.yml. Apply quantile normalization to the filtered count matrix using the"
- [readme] these processes have been submitted to and installed from nf-core/modules in order to make them available to all nf-core pipelines, and to everyone within the Nextflow community: "these processes have been submitted to and installed from [nf-core/modules](https://github.com/nf-core/modules) in order to make them available to all nf-core pipelines"
- [readme] The Nextflow [`-c`](https://www.nextflow.io/docs/latest/config.html) parameter can be used with nf-core pipelines in order to load custom config files: "The Nextflow [`-c`](https://www.nextflow.io/docs/latest/config.html) parameter can be used with nf-core pipelines in order to load custom config files that you have available locally"
- [readme] if you or other people within your organisation are likely to be running nf-core pipelines regularly it may be a good idea to use/create a custom config file that defines some generic settings unique to the computing environment within your organisation. This is where nf-core/configs comes in. No need to write a custom config, simply run `nextflow run <nf-core pipeline> -profile <hpc_name>`: "if you or other people within your organisation are likely to be running nf-core pipelines regularly it may be a good idea to use/create a custom config file that defines some generic settings unique"
