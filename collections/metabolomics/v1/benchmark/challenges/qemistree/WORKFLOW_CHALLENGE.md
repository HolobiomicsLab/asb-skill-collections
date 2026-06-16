# Workflow Challenge: `coll_qemistree_workflow`


> q2-qemistree is a QIIME 2 plugin that builds trees of mass-spectrometry (LC-MS/MS) features to enable chemically-informed comparison of untargeted metabolomic profiles.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 2-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

q2-qemistree implements a pipeline for constructing a tree of mass-spectrometry features from LC-MS/MS data, enabling chemically-informed comparison of untargeted metabolomic profiles. The tool produces a Chemical Feature Tree artifact that represents the hierarchical organization of detected features, facilitating metabolomic profile analysis through chemical similarity relationships.

## Research questions

- What is the process by which q2-qemistree constructs a tree of mass-spectrometry features for chemically-informed metabolomic comparison?
- What are the format, node count, and structural properties of the Chemical Feature Tree artifact produced by the q2-qemistree pipeline?

## Methods overview

Load LC-MS/MS feature table and spectral metadata into QIIME 2 artifact format Invoke q2-qemistree to construct a phylogenetic-style tree integrating spectral similarity and molecular mass relationships Export the Chemical Feature Tree as a Newick-format phylogeny for downstream metabolomic comparison Validation: verify tree artifact contains all input features with correct hierarchical relationships and is compatible with QIIME 2 downstream analyses Load Chemical Feature Tree artifact using QIIME 2 inspection API or format conversion utilities. Detect and validate file format (Newick vs. QIIME 2 serialized object). Parse tree structure and enumerate all nodes (leaf and internal). Compute tree metrics: depth, branching factor, node label coverage. Validate tree connectivity and verify absence of structural defects (cycles, disconnected components, malformed syntax). Validation: tree passes format validation, node count is non-zero and matches expected feature count, and tree is fully connected with valid Newick or QIIME 2 syntax.

**Domain:** metabolomics

**Techniques:** molecular-networking, network-annotation-propagation, clustering

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** q2-qemistree is canonically pronounced as 'chemis-tree'. _[grounded: sys_q2_qemistree]_
- **(finding)** q2-qemistree is a tool to build a tree of mass-spectrometry (LC-MS/MS) features. _[grounded: sys_q2_qemistree]_
- **(finding)** q2-qemistree performs chemically-informed comparison of untargeted metabolomic profiles. _[grounded: sys_q2_qemistree]_
- **(finding)** A manuscript describing q2-qemistree is available in Nature. _[grounded: sys_q2_qemistree]_
- **(finding)** q2-qemistree is developed by the biocore organization and hosted on GitHub. _[grounded: sys_q2_qemistree]_

## Steps

### Step `task_001`
- Title: Reconstruct the LC-MS/MS feature tree construction pipeline in q2-qemistree
- Task kind: `component_reconstruction`
- Task: Invoke the q2-qemistree QIIME 2 plugin to construct a Chemical Feature Tree from LC-MS/MS feature data, producing a phylogenetic-style tree artifact that enables chemically-informed comparison of untargeted metabolomic profiles.
- Inputs:
  - LC-MS/MS feature table (QIIME 2 FeatureTable artifact)
  - Spectral library or molecular feature metadata
- Expected outputs:
  - Chemical Feature Tree artifact (Newick format or QIIME 2 Phylogeny object)
- Tools: q2-qemistree
- Landmark output files: feature_table.qza, feature_tree.qza, tree.nwk
- Primary expected artifact: `feature_tree.qza`

### Step `task_002`
- Depends on: `task_001`
- Title: Analyze the Chemical Feature Tree artifact structure produced by q2-qemistree
- Task kind: `analysis`
- Task: Load the Chemical Feature Tree artifact from q2-qemistree pipeline output and verify its structural integrity, format compliance, and node count as a valid Newick or QIIME 2 artifact file.
- Inputs:
  - Chemical Feature Tree artifact from q2-qemistree pipeline (QIIME 2 .qza or Newick format)
- Expected outputs:
  - Validation report containing tree format type, node count, tree depth, branching statistics, and structural integrity status
- Tools: q2-qemistree
- Landmark output files: tree_format_check.log, tree_node_count.txt, tree_structure_stats.json
- Primary expected artifact: `tree_validation_report.txt`

## Final expected outputs

- `Validation report containing tree format type, node count, tree depth, branching statistics, and structural integrity status` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** implicit

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
  "workflow_id": "coll_qemistree_workflow",
  "agent_order": [
    "task_001",
    "task_002"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Validation report containing tree format type, node count, tree depth, branching statistics, and structural integrity status": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
