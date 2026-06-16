# Workflow Challenge: `coll_juicer_workflow`


> Juicer is a platform for analyzing kilobase resolution Hi-C data that includes a pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature annotation on Hi-C maps.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Juicer provides a processing pipeline that generates Hi-C maps from fastq raw data files, forming the basis for ENCODE's Hi-C uniform processing pipeline. The platform incorporates command line tools designed for feature annotation on Hi-C maps, enabling users to annotate features on pre-generated Hi-C map artifacts.

## Research questions

- What is the input-to-output operation of the Juicer pipeline when processing Hi-C FASTQ data to generate Hi-C maps?
- Does the ENCODE Hi-C uniform processing pipeline produce output that conforms to the reference format and integrity standards expected for Hi-C maps generated from FASTQ data?
- What command line tools does Juicer provide for annotating features on pre-generated Hi-C maps?

## Methods overview

Select and clone Juicer version (1.6 stable or 2 development) from aidenlab/juicer GitHub repository. Obtain raw Hi-C FASTQ dataset from a public data repository. Configure Juicer pipeline parameters including reference genome, restriction enzyme, and computational resources. Execute Juicer pipeline to process raw reads through alignment, contact matrix construction, and normalization. Validation: verify that .hic output file is generated with non-empty contact matrices and contains required metadata. Obtain Hi-C FASTQ data from a public repository or accession identifier. Clone the ENCODE Hi-C uniform processing pipeline from ENCODE-DCC/hic-pipeline. Execute the pipeline wrapper to align reads, deduplicate, and bin contacts into a kilobase-resolution Hi-C map. Generate and compare checksums of the output .hic file against the ENCODE reference. Validation: Output .hic file exists, matches expected format, and checksum matches reference checksum. Load pre-generated .hic contact map file into Juicer environment Select appropriate feature annotation tool from Juicer CLI (loop detection or domain calling) Execute annotation algorithm on the contact map Output annotated genomic features with coordinates and/or boundary calls Validation: Verify output file exists, contains expected feature records (loops with contact pairs or domains with boundary coordinates), and matches format specifications of the chosen annotation tool

**Domain:** bioinformatics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Juicer 1.6 is the last stable release of Juicer. _[grounded: juicer_system]_
- **(finding)** Cloning the Juicer repository directly from Github will clone Juicer 2, which is under active development. _[grounded: juicer_system]_
- **(finding)** Juicer is a platform for analyzing kilobase resolution Hi-C data. _[grounded: juicer_system]_
- **(finding)** Juicer includes a pipeline for generating Hi-C maps from fastq raw data files. _[grounded: juicer_system]_
- **(finding)** Juicer includes command line tools for feature annotation on the Hi-C maps. _[grounded: juicer_system]_
- **(finding)** The main Juicer repository on Github is now focused on the Juicer 2.0 release and is under active development. _[grounded: juicer_system]_
- **(finding)** A dockerized version of Juicer is hosted by ENCODE. _[grounded: juicer_system]_
- **(finding)** Users should not file an issue to ask a question about Juicer. _[grounded: juicer_system]_
- **(finding)** The 3D-Genomics Official Forum is available for asking questions about Juicer. _[grounded: juicer_system]_
- **(finding)** Questions related to sensitive datasets can be sent to aidenlab@bcm.edu.
- **(finding)** Cosmetic changes that do not add anything to the stability, functionality, or testability of Juicer are still welcome contributions. _[grounded: juicer_system]_
- **(finding)** New features or changes to Juicer should be suggested by creating a Github issue. _[grounded: juicer_system]_
- **(finding)** Juicer is developed by the Center for Genome Architecture at Baylor College of Medicine and Rice University. _[grounded: juicer_system]_

## Steps

### Step `task_001`
- Title: Reconstruct the Juicer Hi-C Processing Pipeline from FASTQ to Hi-C Map
- Task kind: `component_reconstruction`
- Task: Execute the Juicer pipeline end-to-end on a publicly deposited Hi-C FASTQ dataset to generate a .hic Hi-C map output file.
- Inputs:
  - Raw Hi-C FASTQ dataset from a public repository (GEO, SRA, or equivalent)
- Expected outputs:
  - Hi-C map file in .hic format generated from raw FASTQ reads
- Tools: Juicer, Juicer 1.6, Juicer 2
- Landmark output files: aligned_reads.bam, merged_nodups.txt, output.hic
- Primary expected artifact: `output.hic`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the ENCODE Hi-C Uniform Processing Pipeline Output Using the Juicer-Based ENCODE Workflow
- Task kind: `reproduction`
- Task: Execute the ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline) on a publicly available Hi-C FASTQ accession to generate a kilobase-resolution Hi-C map, and verify that the output matches ENCODE reference format and checksum.
- Inputs:
  - Publicly available Hi-C FASTQ accession (e.g., NCBI SRA, GEO, or ENCODE-DCC repository accession)
- Expected outputs:
  - Hi-C contact map in ENCODE reference format (.hic file) with verified checksum matching reference
- Tools: Juicer, ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline)
- Landmark output files: aligned_reads.bam, deduped_reads.bam, contact_matrix.txt, hic_contact_map.hic
- Primary expected artifact: `hic_contact_map.hic`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct Feature Annotation on a Hi-C Map Using Juicer Command Line Tools
- Task kind: `component_reconstruction`
- Task: Apply Juicer command-line tools to a pre-generated .hic contact map to annotate genomic features (loop calls or domain calls) and produce a feature annotation output file.
- Inputs:
  - Pre-generated .hic contact map file
- Expected outputs:
  - Feature annotation output file (loop calls or domain calls)
- Tools: Juicer, juicer_cli_tools
- Primary expected artifact: `features.txt`

## Final expected outputs

- `Hi-C contact map in ENCODE reference format (.hic file) with verified checksum matching reference` (type: file, tolerance: hash)
- `Feature annotation output file (loop calls or domain calls)` (type: file, tolerance: hash)

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
  "workflow_id": "coll_juicer_workflow",
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
    "Hi-C contact map in ENCODE reference format (.hic file) with verified checksum matching reference": "<locator>",
    "Feature annotation output file (loop calls or domain calls)": "<locator>"
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
