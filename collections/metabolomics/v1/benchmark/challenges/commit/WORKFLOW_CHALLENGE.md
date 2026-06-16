# Workflow Challenge: `coll_commit_workflow`


> COMMIT is a method that generates consensus metabolic reconstructions and performs community-dependent gap-filling for microbial communities sampled from Arabidopsis thaliana.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 2-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

COMMIT implements two interconnected mechanisms for analyzing microbial communities associated with Arabidopsis thaliana. First, it generates consensus metabolic reconstructions for community members by synthesizing metabolic information across the community. Second, it incorporates a community-dependent gap-filling module that operates on these consensus reconstructions, leveraging shared metabolic context across the community to identify and fill metabolic gaps that individual reconstructions might miss.

## Research questions

- How does COMMIT generate a single consensus metabolic reconstruction from multiple draft reconstructions of organisms in a microbial community?
- How does COMMIT's community-dependent gap-filling procedure use metabolic context from multiple community members to fill gaps in individual consensus reconstructions?

## Methods overview

Load draft metabolic reconstructions for all community member organisms Apply COMMIT consensus algorithm to identify metabolic reactions and metabolites conserved across all input reconstructions per organism Generate consensus metabolic reconstruction containing only agreed-upon reactions and metabolites for each organism Load consensus metabolic models for all community members from prior reconstruction step Initialize COMMIT gap-filling module with community context specification and identified metabolic gaps Execute community-dependent gap-filling algorithm to propose reactions filling gaps using inter-member metabolic dependencies Validate proposed reactions against plant metabolism knowledge and community exchange requirements Validation: Gap-filled models are accepted when all identified gaps have corresponding proposed reactions ranked by confidence, and validation checks confirm consistency with Arabidopsis thaliana metabolism

**Domain:** metabolomics

**Techniques:** flux-analysis, pathway-analysis, multi-omics-integration

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** COMMIT is a tool for generation of consensus metabolic reconstructions and community-dependent gap-filling. _[grounded: SYS_COMMIT]_
- **(finding)** The work applies COMMIT to communities sampled from Arabidopsis thaliana. _[grounded: SYS_COMMIT]_
- **(finding)** The research is sourced from the github repository pwendering__COMMIT. _[grounded: SYS_COMMIT]_
- **(finding)** The document was synthesized on 2026-06-15T09:49:47+00:00.

## Steps

### Step `task_001`
- Title: Reconstruct the COMMIT consensus metabolic reconstruction pipeline for Arabidopsis thaliana communities
- Task kind: `component_reconstruction`
- Task: Apply the COMMIT tool to draft metabolic reconstructions of Arabidopsis thaliana-associated microbial community members to generate a single consensus metabolic reconstruction per organism.
- Inputs:
  - Draft metabolic reconstructions for microbial community members sampled from Arabidopsis thaliana
- Expected outputs:
  - Consensus metabolic reconstruction for each organism
- Tools: COMMIT

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the community-dependent gap-filling step using COMMIT for Arabidopsis thaliana microbial communities
- Task kind: `component_reconstruction`
- Task: Apply COMMIT's community-dependent gap-filling procedure to consensus metabolic reconstructions of plant community members to identify and fill metabolic gaps using shared metabolic context. Produce a gap-filled metabolic model for each community member.
- Inputs:
  - Consensus metabolic reconstructions for community members
- Expected outputs:
  - Gap-filled metabolic models for each community member with filled reactions annotated
- Tools: COMMIT
- Landmark output files: identified_gaps.txt, proposed_reactions.csv, gapfilled_model_<member_id>.xml
- Primary expected artifact: `gapfilled_models.json`

## Final expected outputs

- `Gap-filled metabolic models for each community member with filled reactions annotated` (type: file, tolerance: hash)

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
  "workflow_id": "coll_commit_workflow",
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
    "Gap-filled metabolic models for each community member with filled reactions annotated": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
