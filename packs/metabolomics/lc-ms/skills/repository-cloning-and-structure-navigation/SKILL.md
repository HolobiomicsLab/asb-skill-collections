---
name: repository-cloning-and-structure-navigation
description: Use when when starting a fresh ENPKG installation, you have a GitHub URL (e.g., https://github.com/enpkg/enpkg_full or https://github.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - ENPKG
  - Git
  - enpkg_full
  - enpkg_workflow
  - enpkg_data_organization
  - enpkg_taxo_enhancer
  - enpkg_mn_isdb_taxo
  - enpkg_sirius_canopus
  - enpkg_meta_analysis
  - enpkg_graph_builder
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acscentsci.3c00800
  title: enpkg
- doi: 10.5281/zenodo.10018590
  title: ''
evidence_spans:
- Welcome to the ENPKG Full Workflow!
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enpkg
    doi: 10.1021/acscentsci.3c00800
    title: enpkg
  dedup_kept_from: coll_enpkg
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.3c00800
  all_source_dois:
  - 10.1021/acscentsci.3c00800
  - 10.5281/zenodo.10018590
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Repository Cloning and Structure Navigation

## Summary

Clone a distributed ENPKG workflow repository from GitHub and navigate its modular structure to identify component repositories, configuration files, and workflow entry points. This is the foundational step for setting up the ENPKG natural products knowledge graph pipeline.

## When to use

When starting a fresh ENPKG installation, you have a GitHub URL (e.g., https://github.com/enpkg/enpkg_full or https://github.com/enpkg/enpkg_workflow) and need to understand the repository's directory layout, locate the main workflow orchestrator script, identify per-sample processing components, and find configuration parameters (especially user.yml and .env template files). Use this skill before attempting dependency installation or workflow execution.

## When NOT to use

- You have already cloned and inspected the repository in a previous session and are only updating dependencies or re-running a cached workflow.
- The workflow is being installed via package manager (conda-forge, pip wheel) rather than from source — dependency resolution should use package metadata, not README repository links.
- You are working with a pre-built Docker image or containerized deployment — the repository structure is immutable and this skill is redundant.

## Inputs

- GitHub repository URL (string, e.g., https://github.com/enpkg/enpkg_full)
- Git client installed locally
- Network access to GitHub

## Outputs

- Local repository directory tree (on disk)
- Identified workflow orchestrator script path
- List of modular component repositories and their URLs
- Configuration file locations (user.yml, .env.example)
- Dependency manifest file paths (pyproject.toml, uv.lock, requirements.txt, or environment.yml)

## How to apply

Begin by cloning the target repository using git clone and navigate to the root directory. Examine the repository structure to identify: (1) workflow orchestrator scripts (e.g., 00_workflow_all.sh in enpkg_full), (2) modular sub-components documented in the README that link to separate repositories (enpkg_data_organization, enpkg_taxo_enhancer, enpkg_mn_isdb_taxo, enpkg_sirius_canopus, enpkg_meta_analysis, enpkg_graph_builder), (3) parameter configuration files (params/user.yml), (4) environment setup files (.env.example), and (5) dependency specifications (uv.lock or pyproject.toml for modern environments, or requirements.txt/environment.yml for conda-based setups). Verify that the cloned repository matches the documented architecture by cross-referencing the README's step descriptions with actual directories and scripts present. This navigation establishes the cognitive map needed for subsequent installation and execution steps.

## Related tools

- **Git** (Version control system used to clone and manage the ENPKG repository from GitHub) — https://github.com/git-guides/install-git
- **enpkg_full** (Main orchestrator repository containing the complete workflow, configuration templates, and unified entry point script (00_workflow_all.sh)) — https://github.com/enpkg/enpkg_full
- **enpkg_workflow** (Metarepository documenting the logical workflow architecture, linking to individual sample processing components) — https://github.com/enpkg/enpkg_workflow
- **enpkg_data_organization** (Step 1 modular component: organizes MZmine output into per-sample folder structure) — https://github.com/enpkg/enpkg_data_organization
- **enpkg_taxo_enhancer** (Step 2 modular component: resolves taxonomy and links to Wikidata) — https://github.com/enpkg/enpkg_taxo_enhancer
- **enpkg_mn_isdb_taxo** (Step 3 modular component: generates molecular networks and performs ISDB annotation with taxonomical reweighting) — https://github.com/enpkg/enpkg_mn_isdb_taxo
- **enpkg_sirius_canopus** (Step 4 modular component: executes SIRIUS/CSI:FingerID/CANOPUS structural annotation) — https://github.com/enpkg/enpkg_sirius_canopus
- **enpkg_meta_analysis** (Step 5 modular component: retrieves NPClassifier taxonomy and Wikidata IDs for annotated compounds; also includes optional ChEMBL integration) — https://github.com/enpkg/enpkg_meta_analysis
- **enpkg_graph_builder** (Step 6 modular component: constructs RDF knowledge graphs from all prior processing outputs) — https://github.com/enpkg/enpkg_graph_builder

## Examples

```
git clone https://github.com/enpkg/enpkg_full.git && cd enpkg_full && ls -la && cat README.md | head -50
```

## Evaluation signals

- Verify the cloned directory contains the expected root files: README.md, .gitignore, and pyproject.toml (or uv.lock) or environment.yml, confirming the clone completed without truncation.
- Confirm the workflow orchestrator script exists and is executable: `ls -la workflow/00_workflow_all.sh` should return a file with execute permissions.
- Check that the README's documented step repositories are either present as git submodules or correctly linked as external URLs, ensuring the modular architecture is intact.
- Verify configuration templates exist: `test -f params/user.yml && test -f .env.example` should return true, indicating configuration scaffolding is in place.
- Cross-reference the repository's README 'Prerequisites' section against the presence of dependency manifests (pyproject.toml or environment.yml) to confirm the stated dependency system (uv, conda, or pip) is properly declared.

## Limitations

- Repository structure may change across versions; clone a specific tagged release (e.g., `git clone --branch v1.0.0`) if reproducibility is critical.
- Modular components are linked as external repositories; cloning enpkg_full does not automatically fetch all sub-components—users must manually clone each or use git submodules if configured.
- The README references a test dataset on Zenodo (https://doi.org/10.5281/zenodo.10018590); this dataset must be downloaded separately and is not included in the repository clone.
- Environment setup requires external tools (Git, Anaconda/Miniconda, or uv) to be pre-installed; cloning alone does not verify these prerequisites.

## Evidence

- [readme] First, clone the repository to your local machine: ```bash
git clone https://github.com/enpkg/enpkg_full.git
```

Navigate to the newly created folder: ```bash
cd enpkg_full
```: "First, clone the repository to your local machine: ```bash
git clone https://github.com/enpkg/enpkg_full.git
``` Navigate to the newly created folder: ```bash
cd enpkg_full
```"
- [readme] The different steps are described below, with the link to the corresponding repository to perform the analysis: "The different steps are described below, with the link to the corresponding repository to perform the analysis"
- [readme] This guide will walk you through the installation, setup, and execution of the ENPKG full workflow.: "This guide will walk you through the installation, setup, and execution of the ENPKG full workflow."
- [readme] You will need to edit the following parameters files: - Parameters at [user.yaml](https://github.com/enpkg/enpkg_full/blob/main/params/user.yml): "You will need to edit the following parameters files: - Parameters at [user.yaml](https://github.com/enpkg/enpkg_full/blob/main/params/user.yml)"
- [readme] Runtime secrets and machine-specific paths (e.g., `PATH_TO_SIRIUS`, `SIRIUS_USERNAME`, `SIRIUS_PASSWORD`) live in a `.env` file that is ignored by git. Configure it as follows: ```bash
cp .env.example .env
```: "Runtime secrets and machine-specific paths (e.g., `PATH_TO_SIRIUS`, `SIRIUS_USERNAME`, `SIRIUS_PASSWORD`) live in a `.env` file that is ignored by git."
- [readme] From the root of the repository, run: ```bash
sh workflow/00_workflow_all.sh
```: "From the root of the repository, run: ```bash
sh workflow/00_workflow_all.sh
```"
