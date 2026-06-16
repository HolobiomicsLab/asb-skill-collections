# Workflow Challenge: `coll_specxplore_workflow`


> specXplore is a Python dashboard tool for interactive exploration of LC-MS/MS spectral data, combining t-SNE embeddings based on ms2deepscore similarities with interactive visualizations including network views and heatmaps.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

specXplore operates through a two-stage workflow: first, users process raw spectral data in Jupyter notebooks using the specXplore importing pipeline to generate a serialized session data object saved to disk; second, this saved session object is loaded into a specXplore dashboard instance for interactive visual exploration. The system implements a t-SNE embedding component that computes a 2-D overview representation from ms2deepscore-derived mass spectral similarities, serving as the foundation for the interactive dashboard visualizations including network views, similarity heatmaps, and fragmentation overview maps.

## Research questions

- What is the input format and processing pipeline architecture for converting raw LC-MS/MS spectral data into a serialized specXplore session data object in the importing stage?
- How does the specXplore dashboard session instance initialize and become accessible after loading a saved session data object from disk?
- How does specXplore compute a t-SNE embedding from ms2deepscore similarity scores to generate a 2-D overview representation of mass spectral data?

## Methods overview

Initialize Python environment and Jupyter notebook with specXplore importing pipeline module. Load raw LC-MS/MS spectral data files into memory using specXplore's data import functions. Parse and normalize spectral records to extract peaks, intensities, and metadata. Apply importing pipeline processing steps to construct the session data object. Serialize the session object to disk in a format compatible with specXplore dashboard consumers. Validation: confirm session file exists, contains expected data structures (spectral arrays, embeddings, metadata), and can be deserialized without error by downstream dashboard application. Load specXplore session data object from disk using Python serialization/deserialization Instantiate the fixed dashboard-session architecture layer with the loaded object Verify initialization completion and absence of runtime errors Confirm interactive application accessibility and responsiveness Validation: Dashboard session initializes without errors and the interactive application is accessible for user interaction Load the specXplore session data object containing processed spectral features and precomputed ms2deepscore pairwise similarity scores. Convert ms2deepscore similarities to distance metric (e.g., 1 − similarity or equivalent dissimilarity representation) as required by t-SNE. Execute t-SNE algorithm with the ms2deepscore distance matrix as input to compute 2-D embedding coordinates for each spectrum. Export the t-SNE coordinates (spectrum identifier, x-coordinate, y-coordinate) to a structured file. Validation: Confirm that the output file contains one row per spectrum with valid numeric coordinates in the 2-D embedding space and matches the spectrum count from the input session data object.

**Domain:** metabolomics

**Techniques:** spectral-library-matching, dimensionality-reduction, deep-learning

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** SpecXplore is a python dashboard tool for adjustable LC-MS/MS spectral data exploration. _[grounded: specXplore_system]_
- **(finding)** SpecXplore uses a t-SNE embedding to serve as an overview representation of mass spectral similarities. _[grounded: specXplore_system]_
- **(finding)** SpecXplore's t-SNE embedding is based on ms2deepscore. _[grounded: specXplore_system]_
- **(finding)** SpecXplore includes network views, similarity heatmaps, and fragmentation overview maps. _[grounded: specXplore_system]_
- **(finding)** The specXplore workflow is separated into two stages. _[grounded: specXplore_system]_
- **(finding)** In the first stage of the specXplore workflow, the user processes spectral data to create a specxplore session data object. _[grounded: specXplore_system]_
- **(finding)** Spectral data processing for specXplore is done in interactive Jupyter notebooks using the specXplore importing pipeline. _[grounded: specXplore_system]_
- **(finding)** The specXplore importing pipeline produces a specXplore session data object that is saved to the hard drive. _[grounded: specXplore_system]_
- **(finding)** The specXplore session data object can be fed directly into a specxplore dashboard session instance for visual exploration. _[grounded: specXplore_system]_

## Steps

### Step `task_001`
- Title: Reconstruct the specXplore importing pipeline to produce a session data object from LC-MS/MS spectral data
- Task kind: `component_reconstruction`
- Task: Load raw LC-MS/MS spectral data using the specXplore importing pipeline in Jupyter notebooks and produce a serialized session data object file saved to disk.
- Inputs:
  - Raw LC-MS/MS spectral data files (e.g., mzML, mzXML, or vendor-specific formats)
- Expected outputs:
  - Serialized specXplore session data object file saved to disk
- Tools: Python, Jupyter notebooks
- Landmark output files: spectral_data_loaded.csv, session_metadata.json
- Primary expected artifact: `specxplore_session.pkl`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the specXplore Dashboard Session instantiation from a saved session data object
- Task kind: `component_reconstruction`
- Task: Load a saved specXplore session data object from disk and launch the specXplore dashboard session instance, verifying correct initialization of the fixed dashboard-session architecture layer and confirming the interactive application becomes accessible.
- Inputs:
  - specXplore session data object file (saved from prior Jupyter notebook processing)
- Expected outputs:
  - Dashboard session instance status report confirming initialization success and application accessibility
- Tools: Python
- Landmark output files: session_object_load.log, dashboard_initialization.log
- Primary expected artifact: `dashboard_session_init_report.txt`

### Step `task_003`
- Depends on: `task_001`
- Title: Implement the ms2deepscore-based t-SNE embedding component within specXplore
- Task kind: `component_reconstruction`
- Task: Compute a 2-D t-SNE embedding of mass spectral data using ms2deepscore similarity scores as input distances, producing coordinate output that serves as the overview representation for specXplore visualization.
- Inputs:
  - specXplore session data object containing processed spectral data and precomputed ms2deepscore similarity scores
- Expected outputs:
  - 2-D t-SNE coordinate file mapping spectrum identifiers to (x, y) positions in embedding space
- Tools: Python, ms2deepscore, Jupyter notebooks
- Landmark output files: ms2deepscore_distance_matrix.npy, tsne_coordinates.csv
- Primary expected artifact: `tsne_coordinates.csv`

## Final expected outputs

- `Dashboard session instance status report confirming initialization success and application accessibility` (type: file, tolerance: hash)
- `2-D t-SNE coordinate file mapping spectrum identifiers to (x, y) positions in embedding space` (type: file, tolerance: hash)

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
  "workflow_id": "coll_specxplore_workflow",
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
    "Dashboard session instance status report confirming initialization success and application accessibility": "<locator>",
    "2-D t-SNE coordinate file mapping spectrum identifiers to (x, y) positions in embedding space": "<locator>"
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
