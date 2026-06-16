# Workflow Challenge: `coll_mshub_workflow`


> A companion repository enables reproduction of an auto-deconvolution and molecular networking workflow for gas chromatography–mass spectrometry data, as described in the associated Nature Biotechnology 2020 publication.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reproduces 1 reported result: A companion repository (bittremieux/GNPS_GC) has been established to enable re-execution of the auto-deconvolution and molecular networking workflow on the deposited GC-MS dataset associated with the Nature Biotechnology 2020 publication. Reconstructs 2 described mechanisms (described in the paper but not separately evaluated there): The manuscript describes auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis, with implementation available in the companion repository (bittremieux/GNPS_GC). The method integrates auto-deconvolution with molecular networking for gas chromatography–mass spectrometry data, enabling structured network analysis of deconvolved spectra.

## Research questions

- Can the auto-deconvolution and molecular networking pipeline described in the Nature Biotechnology 2020 manuscript be successfully re-run on the companion GC-MS dataset to reproduce the reported network and deconvolved spectra outputs?
- How does the auto-deconvolution method process raw gas chromatography–mass spectrometry data to separate and identify individual chemical components from complex mixtures?
- How does the molecular networking step process deconvolved gas chromatography–mass spectrometry spectra and what network output format does it produce?

## Methods overview

Load GC-MS raw data from the Nature Biotechnology 2020 companion deposit. Apply MSHub auto-deconvolution to separate overlapping chromatographic peaks into individual compound spectra. Export deconvolved spectra in MGF format compatible with GNPS. Execute GNPS molecular networking workflow with cosine similarity clustering and graph construction. Extract network topology metrics and compare node/edge counts and clustering structure to the published results. Validation: verify that the molecular network exhibits the same major cluster structure and number of connected components as reported in the original manuscript; deconvolved spectra should match the reference spectra in the GNPS deposit. References: source article (DOI: 10.1038/s41587-020-0700-3) Load raw GC-MS chromatography data from deposited files. Apply MSHub auto-deconvolution to resolve co-eluting spectral components. Export deconvolved spectra to standardized format (MGF or mzML). Validation: Verify output file exists, contains valid spectrum records, and is compatible with downstream GNPS molecular networking input requirements. References: source article (DOI: 10.1038/s41587-020-0700-3) Prepare deconvolved spectra in GNPS_GC-compatible format (MSP, mzXML, or equivalent). Submit spectra batch to GNPS_GC networking pipeline via web portal or API. Monitor job execution until network computation completes. Retrieve molecular network output in GraphML or JSON serialization. Validation: Confirm network file is well-formed (valid graph structure), contains ≥1 node and ≥0 edges, and edge metadata includes similarity scores or match statistics. References: source article (DOI: 10.1038/s41587-020-0700-3)

**Domain:** metabolomics

**Techniques:** gc-ms, spectral-deconvolution, molecular-networking, feature-detection, metabolite-identification, gnps-workflow

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** This repository is a companion to a manuscript by Aksenov et al. published in Nature Biotechnology in 2020. _[grounded: COMP_AUTO_DECONV]_
- **(finding)** The manuscript describes auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data. _[grounded: COMP_AUTO_DECONV]_
- **(finding)** The source repository is located on GitHub under the identifier bittremieux__GNPS_GC. _[grounded: SYS_GNPS_GC]_
- **(finding)** The document was synthesized on 2026-06-16 at 05:56:15 UTC.

## Steps

### Step `task_001`
- Title: Reproduce the auto-deconvolution and molecular networking workflow for GC-MS data via MSHub and GNPS
- Task kind: `reproduction`
- Task: Re-run MSHub auto-deconvolution on the companion GC-MS dataset from the Nature Biotechnology 2020 manuscript, followed by GNPS molecular networking to reproduce the reported deconvolved spectra and network visualization outputs.
- Inputs:
  - GC-MS raw data files from Nature Biotechnology 2020 companion dataset (GNPS/MassIVE accession or Zenodo deposit)
- Expected outputs:
  - Deconvolved spectra table (MGF or mzTab format) with individual compound mass-to-charge and intensity values
  - Molecular network file and visualization (GraphML, JSON, or PNG) showing spectral clusters and cosine similarity edges
  - Network topology metrics and comparison to reported network structure
- Tools: MSHub, GNPS
- Landmark output files: deconvolved_spectra.mgf, network_edges.csv, network_nodes.csv, network_topology_comparison.txt
- Primary expected artifact: `molecular_network.graphml`

### Step `task_002`
- Title: Reconstruct the MSHub auto-deconvolution module for GC-MS raw data
- Task kind: `component_reconstruction`
- Task: Implement auto-deconvolution of raw GC-MS data using MSHub to resolve co-eluting compounds and produce a file of deconvolved spectra in standard format (MGF or mzML).
- Inputs:
  - Raw GC-MS data files (netCDF or vendor format) from bittremieux/GNPS_GC repository or equivalent deposited dataset
- Expected outputs:
  - File of deconvolved spectra in MGF or mzML format ready for molecular networking
- Tools: MSHub
- Landmark output files: raw_gcms_loaded.txt, deconvolution_log.txt
- Primary expected artifact: `deconvolved_spectra.mgf`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct the GNPS molecular networking module on deconvolved GC-MS spectra
- Task kind: `component_reconstruction`
- Task: Submit deconvolved gas chromatography–mass spectrometry spectra to GNPS_GC molecular networking and retrieve the resulting network file in GraphML or JSON format.
- Inputs:
  - Deconvolved spectra from prior auto-deconvolution step (e.g., peak table or MS/MS records in MSP, mzXML, or vendor-compatible format)
- Expected outputs:
  - Molecular network file in GraphML or JSON format containing nodes (spectra/compounds) and edges (spectral similarity or MS/MS fragmentation matches)
- Tools: GNPS_GC
- Landmark output files: spectra_batch_manifest.txt, gnps_job_status.log, molecular_network.graphml
- Primary expected artifact: `molecular_network.graphml`

## Final expected outputs

- `File of deconvolved spectra in MGF or mzML format ready for molecular networking` (type: file, tolerance: hash)
- `Molecular network file in GraphML or JSON format containing nodes (spectra/compounds) and edges (spectral similarity or MS/MS fragmentation matches)` (type: file, tolerance: hash)

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
  "workflow_id": "coll_mshub_workflow",
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
    "File of deconvolved spectra in MGF or mzML format ready for molecular networking": "<locator>",
    "Molecular network file in GraphML or JSON format containing nodes (spectra/compounds) and edges (spectral similarity or MS/MS fragmentation matches)": "<locator>"
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
