# Workflow Challenge: `coll_molnetenhancer_workflow`


> pyMolNetEnhancer is a Python module that integrates chemical class and substructure information within mass spectral molecular networks created through the GNPS platform.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

pyMolNetEnhancer provides mechanisms for mapping MS2LDA substructural information and chemical class information to mass spectral molecular networks. The module supports multiple mapping approaches: classical and feature-based modes for MS2LDA substructural information, chemical class mapping alone, and combined mapping of both chemical class and substructural annotations within networks generated through the Global Natural Products Social Molecular Networking (GNPS) platform.

## Research questions

- How does pyMolNetEnhancer map MS2LDA-derived Mass2Motif substructural information onto nodes in classical-mode GNPS mass spectral molecular networks?
- How does the feature-based mode pipeline map Mass2Motif substructural information from MS2LDA onto a GNPS feature-based molecular network?
- How does pyMolNetEnhancer map chemical class information onto a GNPS mass spectral molecular network?
- How does pyMolNetEnhancer jointly integrate both chemical class annotations and MS2LDA substructural motif information onto a GNPS mass spectral molecular network in a single combined operation?

## Methods overview

Load GNPS classical molecular network and MS2LDA Mass2Motif output. Align motif identifiers to network nodes using precursor m/z and spectral similarity matching. Annotate network nodes with mapped motif metadata and confidence scores. Validation: Confirm all mapped nodes contain motif attributes and output file is valid graph format. Load GNPS feature-based molecular network and MS2LDA substructural motif assignments. Match feature identifiers between the network and MS2LDA motif table. Annotate network nodes with MS2LDA substructural labels and confidence metadata using pyMolNetEnhancer. Export the enriched network graph with embedded annotations in standard graph format. Validation: Verify all feature nodes with matched motifs are annotated and network structure is preserved. Load a GNPS molecular network from a standard file format (graphml or cytoscape). Prepare or retrieve chemical class annotations for network nodes from GNPS library or external metadata source. Apply pyMolNetEnhancer to map chemical class information onto network nodes as attributes. Export the enriched network with embedded chemical class labels in graphml or cytoscape format. Validation: verify that all network nodes containing library matches have corresponding chemical class annotations; check that the output network preserves the original topology and node count. Load GNPS molecular network and organize node/edge structure for annotation Parse and align chemical class assignments from GNPS library to network nodes Parse and align MS2LDA substructural motifs to network features using feature-based mapping Merge both annotation layers into unified node attribute dictionaries Export annotated network with all chemical class and motif metadata preserved Validation: Verify all network nodes carry both chemical class and at least one MS2LDA motif attribute; confirm node count and edge count match original network

**Domain:** metabolomics

**Techniques:** molecular-networking, network-annotation-propagation, database-annotation, chemical-class-annotation

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the GNPS platform. _[grounded: pyMolNetEnhancer]_
- **(finding)** An analogous R package for MolNetEnhancer is available at https://github.com/madeleineernst/RMolNetEnhancer. _[grounded: RMolNetEnhancer]_
- **(hypothesis)** pyMolNetEnhancer enables mapping of MS2LDA substructural information to mass spectral molecular networks using a classical approach. _[grounded: pyMolNetEnhancer]_
- **(hypothesis)** pyMolNetEnhancer enables mapping of MS2LDA substructural information to mass spectral molecular networks using a feature-based approach. _[grounded: pyMolNetEnhancer]_
- **(hypothesis)** pyMolNetEnhancer enables mapping of chemical class information to mass spectral molecular networks. _[grounded: pyMolNetEnhancer]_
- **(hypothesis)** pyMolNetEnhancer enables mapping of both chemical class and MS2LDA substructural information to mass spectral molecular networks simultaneously. _[grounded: pyMolNetEnhancer]_

## Steps

### Step `task_001`
- Title: Reconstruct the Map MS2LDA Substructural Information to Mass Spectral Molecular Network (Classical) component
- Task kind: `component_reconstruction`
- Task: Map Mass2Motif substructural information from MS2LDA onto a GNPS-generated mass spectral molecular network using the classical-mode approach, producing an annotated network artifact with motif-to-node assignments.
- Inputs:
  - GNPS-generated classical molecular network file (graphml or JSON format)
  - MS2LDA Mass2Motif substructural information output (motif assignments and scores)
- Expected outputs:
  - Annotated molecular network file with embedded Mass2Motif substructural information mapped to network nodes
- Tools: pyMolNetEnhancer, GNPS, Python
- Landmark output files: motif_node_mapping.tsv, mapping_statistics.json
- Primary expected artifact: `annotated_network.graphml`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the Map MS2LDA Substructural Information to Mass Spectral Molecular Network (Feature Based) component
- Task kind: `component_reconstruction`
- Task: Map MS2LDA substructural motifs onto a GNPS feature-based molecular network using pyMolNetEnhancer to produce an annotated network artifact with substructural annotations.
- Inputs:
  - GNPS feature-based molecular network file (GraphML or JSON)
  - MS2LDA substructural motif assignments (feature-to-motif mapping table)
- Expected outputs:
  - Annotated feature-based molecular network with MS2LDA substructural motif annotations embedded as node attributes
- Tools: pyMolNetEnhancer, GNPS, Python
- Landmark output files: ms2lda_feature_mapping.csv, annotated_feature_network.graphml
- Primary expected artifact: `annotated_feature_network.graphml`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct the Map Chemical Classes to Mass Spectral Molecular Network component
- Task kind: `component_reconstruction`
- Task: Map chemical class information onto a GNPS mass spectral molecular network using pyMolNetEnhancer to produce a chemically-annotated network artifact.
- Inputs:
  - GNPS mass spectral molecular network file (graphml or cytoscape format)
  - Chemical class metadata or library mapping
- Expected outputs:
  - Chemically-annotated GNPS molecular network file with chemical class information mapped to network nodes
- Tools: pyMolNetEnhancer, GNPS, Python
- Landmark output files: network_input.graphml, chemical_class_mapping.csv, annotated_network.graphml
- Primary expected artifact: `annotated_network.graphml`

### Step `task_004`
- Depends on: `task_003`
- Title: Reconstruct the Map Chemical Classes and MS2LDA Motifs to Mass Spectral Molecular Network component
- Task kind: `component_reconstruction`
- Task: Integrate chemical class annotations and MS2LDA substructural motif information onto a GNPS mass spectral molecular network in a single operation. Produce a fully-enriched network artifact with both annotation types mapped to nodes.
- Inputs:
  - GNPS mass spectral molecular network file (GraphML or JSON format)
  - MS2LDA substructural motif assignments for network features
  - Chemical class annotation table or library matches from GNPS
- Expected outputs:
  - Fully-enriched molecular network with chemical class and MS2LDA motif annotations integrated on all nodes
- Tools: pyMolNetEnhancer, GNPS, Python
- Landmark output files: gnps_network_with_chemical_classes.graphml, gnps_network_with_ms2lda_motifs.graphml, enriched_molecular_network.graphml
- Primary expected artifact: `enriched_molecular_network.graphml`

## Final expected outputs

- `Annotated feature-based molecular network with MS2LDA substructural motif annotations embedded as node attributes` (type: file, tolerance: hash)
- `Fully-enriched molecular network with chemical class and MS2LDA motif annotations integrated on all nodes` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: open — validity-first.** The deterministic match-rubrics above are demoted to *informational*. The binding evaluator is **SCIENTIFIC_VALIDITY** (below). Any scientifically sound method that addresses the research question is valid, and novel findings or unexplored aspects can score positively — **different is not wrong**.

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
  "workflow_id": "coll_molnetenhancer_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004"
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
    },
    "task_004": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Annotated feature-based molecular network with MS2LDA substructural motif annotations embedded as node attributes": "<locator>",
    "Fully-enriched molecular network with chemical class and MS2LDA motif annotations integrated on all nodes": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
