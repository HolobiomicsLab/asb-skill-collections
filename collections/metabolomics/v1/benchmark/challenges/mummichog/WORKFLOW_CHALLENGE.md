# Workflow Challenge: `coll_mummichog_workflow`


> Mummichog is a Python program for analyzing high-throughput untargeted metabolomics data by leveraging metabolic network organization to predict functional activity directly from feature tables, bypassing the need for metabolite identification.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 2-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This work describes Mummichog's metabolic network-based feature-table analysis pipeline as a mechanism for functional activity prediction without explicit metabolite identification. The project has been relocated to the metabolomics-cloud GitHub organization; however, the provided documentation does not contain verification that the relocated package installs and runs correctly from its new location.

## Research questions

- How does Mummichog 3 accept untargeted metabolomics feature tables as input and predict functional activity by mapping features onto metabolic networks without requiring metabolite identification?
- Has the Mummichog 3 codebase been successfully relocated to the metabolomics-cloud GitHub organization and verified to install and function correctly in its new location?

## Methods overview

Load feature table with m/z, retention time, and sample intensity data. Initialize metabolic network database and retrieve network structure (nodes = metabolites, edges = reactions). Map feature m/z values to metabolic network nodes using mass-to-charge tolerance matching. Propagate feature signal intensity through connected network pathways to infer metabolic module activity. Aggregate network-level activity signals and generate functional predictions without explicit metabolite identification. Validation: Confirm functional activity predictions are generated and network mapping statistics show connectivity across multiple metabolic modules. Audit current Mummichog 3 structure and dependencies against metabolomics-cloud standards. Adapt package metadata, module structure, documentation, and CI/CD workflows to conform to organization conventions. Create and populate migrated repository at metabolomics-cloud/mummichog with updated codebase. Verify installation from clean environment using pip install. Execute functional prediction workflows on test metabolomics data to confirm runtime correctness. Validation: Installation completes without errors, all unit and integration tests pass, and functional prediction output on test data matches expected metabolic network-based predictions.

**Domain:** metabolomics

**Techniques:** pathway-analysis, database-annotation, metabolite-identification

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Mummichog is a Python program for analyzing data from high throughput, untargeted metabolomics.
- **(finding)** Mummichog leverages the organization of metabolic networks to predict functional activity directly from feature tables.
- **(finding)** Mummichog can predict functional activity by bypassing metabolite identification.
- **(finding)** The last version of Mummichog 2 is under branch mummichog-2.7. _[grounded: mummichog2]_
- **(finding)** Mummichog version 3 is under development.
- **(finding)** The Mummichog project has been moved to the new organization at https://github.com/metabolomics-cloud.
- **(finding)** The Mummichog project move follows examples from https://scverse.org/.

**Informational claims (component_reconstruction — mechanisms the paper described but did not separately validate; NOT binding for CLAIM_VALIDATION):**
- **(finding)** Mummichog is a Python program that leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification. [evidence_step: task_001] _[grounded: mummichog3 under mummichog2]_

## Steps

### Step `task_001`
- Title: Reconstruct the metabolic network-based feature-table analysis pipeline in Mummichog 3
- Task kind: `component_reconstruction`
- Task: Implement the Mummichog 3 core pipeline to predict functional activity from an untargeted metabolomics feature table by mapping features onto metabolic networks without requiring metabolite identification. Output a functional activity prediction report.
- Inputs:
  - Untargeted metabolomics feature table (m/z, retention time, intensity across samples)
- Expected outputs:
  - Functional activity prediction report mapping features to metabolic network modules and pathways
- Tools: Python
- Landmark output files: feature_network_mapping.csv, pathway_activity_scores.csv, network_propagation_results.csv
- Primary expected artifact: `functional_activity_predictions.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Extend Mummichog 3 to incorporate the metabolomics-cloud GitHub organization project structure
- Task kind: `extension`
- Task: Migrate the Mummichog 3 codebase to the metabolomics-cloud GitHub organization, ensure compliance with organization conventions, and verify that the relocated package installs and executes correctly from its new repository location.
- Inputs:
  - Current Mummichog 3 repository source code and configuration files (setup.py, pyproject.toml, requirements.txt, CI/CD workflows, README, documentation)
  - metabolomics-cloud organization repository standards and contribution guidelines
  - Representative metabolomics feature table(s) for functional prediction testing
- Expected outputs:
  - Migrated Mummichog 3 repository at metabolomics-cloud/mummichog with updated package metadata, configuration, and documentation conforming to organization standards
  - Installation verification log confirming successful pip install from the new repository location in a clean Python environment
  - Functional test results demonstrating that core Mummichog workflows (feature table loading, functional activity prediction) execute correctly
  - Migration report documenting conformance changes applied, verification test outcomes, and any breaking changes or deprecations introduced
- Tools: Python
- Landmark output files: conformance_checklist.txt, setup.py, install.log, functional_test_output.json
- Primary expected artifact: `migration_report.md`

## Final expected outputs

- `Migrated Mummichog 3 repository at metabolomics-cloud/mummichog with updated package metadata, configuration, and documentation conforming to organization standards` (type: file, tolerance: hash)
- `Installation verification log confirming successful pip install from the new repository location in a clean Python environment` (type: file, tolerance: hash)
- `Functional test results demonstrating that core Mummichog workflows (feature table loading, functional activity prediction) execute correctly` (type: file, tolerance: hash)
- `Migration report documenting conformance changes applied, verification test outcomes, and any breaking changes or deprecations introduced` (type: file, tolerance: hash)

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
  "workflow_id": "coll_mummichog_workflow",
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
    "Migrated Mummichog 3 repository at metabolomics-cloud/mummichog with updated package metadata, configuration, and documentation conforming to organization standards": "<locator>",
    "Installation verification log confirming successful pip install from the new repository location in a clean Python environment": "<locator>",
    "Functional test results demonstrating that core Mummichog workflows (feature table loading, functional activity prediction) execute correctly": "<locator>",
    "Migration report documenting conformance changes applied, verification test outcomes, and any breaking changes or deprecations introduced": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
