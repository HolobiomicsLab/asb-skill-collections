# Workflow Challenge: `coll_bam_workflow`


> BAM is a biotransformation-based annotation method for molecular structure discovery from untargeted metabolomics data. This repository provides the implementation code and validation dataset to reproduce reported results.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This repository contains the implementation of BAM (biotransformation-based annotation method), a computational approach for molecular structure discovery from untargeted metabolomics data that integrates biotransformation rules and global molecular networking. The repository includes both the BAM codebase and the validation dataset used to assess the method's performance, enabling reproduction of the reported validation results.

## Research questions

- Does the BAM pipeline, when executed end-to-end on the deposited validation dataset, reproduce the reported validation metrics for molecular structure discovery from untargeted metabolomics data?
- How does the BAM method apply biotransformation rules to generate candidate molecular structures from input molecules?
- How does the global molecular networking component of BAM operate on candidate transformed structures to generate a molecular network file and annotation table?

## Methods overview

Obtain the HassounLab/BAM repository and validation dataset (metabolomics data + reference annotations). Configure and initialize the BAM pipeline with biotransformation rules and molecular networking parameters. Execute the BAM pipeline end-to-end to generate structure annotations for validation data. Compute annotation accuracy (percentage of correct predictions) and coverage (percentage of features with assignments) against reference. Validation: Reported validation metrics (annotation accuracy and coverage) must match or closely approximate the paper's published benchmarks for the validation dataset. Load and validate input SMILES using RDKit chemistry library. Access and parse biotransformation rules from the BAM codebase. Apply each rule to every input structure, generating candidate products. Deduplicate and track parent–product relationships with rule metadata. Serialize results as structured JSON/CSV output file. Validation: Verify that all input structures have been processed, no invalid SMILES are output, and parent–product links are traceable. Load candidate structures from biotransformation rules and MS/MS spectral features. Compute pairwise spectral similarity scores across all features using cosine similarity or analogous metric. Apply spectral similarity threshold to filter network edges and retain high-confidence spectral matches. Detect molecular families via graph clustering or community detection on the filtered network. Integrate candidate structures with network nodes and assign feature-to-structure annotations based on mass and spectral consistency. Validation: Confirm molecular network file is properly formatted and parseable; verify annotation table contains all MS features with at least one candidate structure assignment and cluster membership; assess annotation coverage (% of features with predicted structures) and network statistics (number of nodes, edges, clusters) match expected scale.

**Domain:** metabolomics

**Techniques:** molecular-networking, metabolite-identification, network-annotation-propagation, database-annotation, high-resolution-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** This repository contains code to implement the biotransformation-based annotation method (BAM).
- **(finding)** The repository contains data used to validate BAM. _[grounded: dataset_validation_data]_
- **(finding)** BAM uses biotransformation rules and global molecular networking for molecular structure discovery. _[grounded: comp_biotransformation_rules]_

## Steps

### Step `task_001`
- Title: Reproduce BAM Validation Results Using the BAM Codebase and Validation Dataset
- Task kind: `reproduction`
- Task: Execute the BAM (biotransformation-based annotation method) pipeline end-to-end on a deposited validation dataset using the HassounLab/BAM repository codebase, and reproduce reported validation metrics including annotation accuracy and coverage.
- Inputs:
  - HassounLab/BAM repository codebase
  - Deposited validation metabolomics dataset with reference annotations
- Expected outputs:
  - Annotation predictions (structures assigned by BAM pipeline)
  - Validation metrics (annotation accuracy, coverage scores)
  - Performance report comparing BAM predictions to reference annotations
- Tools: HassounLab/BAM
- Landmark output files: bam_config.json, molecular_network.graphml, structure_predictions.csv, accuracy_coverage_scores.csv
- Primary expected artifact: `validation_metrics.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the Biotransformation Rules Application Module
- Task kind: `component_reconstruction`
- Task: Implement the biotransformation-rules component from the BAM codebase and apply encoded biotransformation rules to a set of input molecular structures (SMILES format) to generate candidate transformed structures. Output the results as a structured file mapping each input structure to its biotransformation products.
- Inputs:
  - Molecular structures in SMILES format
  - BAM biotransformation rules from codebase
- Expected outputs:
  - Structured file mapping input structures to biotransformation product candidates
- Tools: RDKit, HassounLab/BAM
- Landmark output files: validated_smiles.csv, biotransformation_rules_summary.txt, raw_products.csv
- Primary expected artifact: `transformed_structures.json`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the Global Molecular Networking Annotation Step
- Task kind: `component_reconstruction`
- Task: Execute the global molecular networking component of BAM on candidate transformed structures to generate a molecular network file and annotation table linking metabolite features to putative structures.
- Inputs:
  - Candidate transformed structures from biotransformation-rules module (structures with mass, formula, and SMILES notation)
  - Untargeted metabolomics MS/MS spectral data (feature intensity matrix and MS2 spectra)
- Expected outputs:
  - Molecular network file in standard graph format (GraphML, JSON, or GXF) containing nodes (features) and edges (spectral similarity links)
  - Feature annotation table (CSV or TSV) mapping each MS feature to candidate structure(s), molecular family cluster, and annotation confidence metrics
- Tools: BAM
- Landmark output files: spectral_similarity_matrix.csv, network_edges_filtered.csv, molecular_network.graphml, cluster_assignments.csv
- Primary expected artifact: `annotation_table.csv`

## Final expected outputs

- `Molecular network file in standard graph format (GraphML, JSON, or GXF) containing nodes (features) and edges (spectral similarity links)` (type: file, tolerance: hash)
- `Feature annotation table (CSV or TSV) mapping each MS feature to candidate structure(s), molecular family cluster, and annotation confidence metrics` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: mixed — per-step.** Closed steps must reproduce (rubrics above bind on them); open steps are judged by **SCIENTIFIC_VALIDITY** (below). Invariants bind everywhere; different is not wrong on the open steps.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** intermediate

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
  "workflow_id": "coll_bam_workflow",
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
    "Molecular network file in standard graph format (GraphML, JSON, or GXF) containing nodes (features) and edges (spectral similarity links)": "<locator>",
    "Feature annotation table (CSV or TSV) mapping each MS feature to candidate structure(s), molecular family cluster, and annotation confidence metrics": "<locator>"
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
