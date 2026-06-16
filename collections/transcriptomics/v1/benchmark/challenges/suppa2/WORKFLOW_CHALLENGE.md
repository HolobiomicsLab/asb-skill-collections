# Workflow Challenge: `coll_suppa2_workflow`


> SUPPA2 is a tool for fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions that leverages transcript quantification for efficient alternative splicing profiling.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

SUPPA2 implements a workflow for differential splicing analysis consisting of three main computational steps: (1) generation of transcript events and local alternative splicing events from genome annotation GTF files via the generateEvents subcommand, which produces ioi (input-output index), ioe (input-output events), and gtf artifacts; (2) calculation of PSI (percent spliced in) values for transcript events and local alternative splicing events by leveraging transcript quantification data; and (3) differential splicing analysis across multiple conditions by consuming PSI matrices and expression data to generate differential splicing results with uncertainty quantification.

## Research questions

- What are the three distinct output file artifacts produced by the SUPPA2 generateEvents subcommand when parsing a genome annotation GTF file?
- How does SUPPA2 compute PSI (Percent Spliced In) values from transcript quantification data and event definitions to produce a PSI matrix?
- How does the SUPPA2 diffSplice subcommand compute differential splicing statistics (delta PSI and p-values) from per-condition PSI matrices and transcript expression data?

## Methods overview

Load genome annotation in GTF format into SUPPA2 generateEvents subcommand. Extract transcript structures and identify all exonic features, promoter/terminator variants, and isoform-specific junctions. Generate index of events (ioe) file enumerating transcript-level and local splicing events with event definitions. Generate index of isoforms (ioi) file mapping each event to the set of isoforms that include or exclude it. Filter and extract only local alternative splicing events (exon skipping, intron retention, alternative splice sites) into a separate GTF file. Validation: verify that all three output files are produced with correct format and non-empty event/isoform mappings consistent with input annotation complexity. Load transcript quantification output with transcript identifiers and abundance values (TPM or counts). Parse SUPPA2 event definition file (ioe or ioi) to extract event–transcript mappings. Aggregate transcript abundances per event according to inclusion/exclusion isoform sets. Calculate PSI as the ratio of inclusion isoform total to total event abundance. Validation: PSI matrix has one row per event, one column per sample, all values in [0,1]. Load PSI matrices and transcript expression quantification for each condition. Align sample identifiers across PSI and expression files. Apply SUPPA2 diffSplice statistical test with uncertainty-aware variance estimation. Compute ΔPSI (mean difference) and two-sided p-values per event. Validation: output table row count equals total number of events; all p-values fall in [0, 1] and ΔPSI in [−1, 1].

**Domain:** transcriptomics

**Techniques:** statistical-analysis, differential-abundance-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** SUPPA performs fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions. _[grounded: comp_diffSplicing]_
- **(finding)** SUPPA2 was published in Genome Biology in 2018. _[grounded: SUPPA2_system]_
- **(finding)** Transcript quantification can be leveraged for fast computation of alternative splicing profiles. _[grounded: tool_salmon_kallisto]_
- **(finding)** A short SUPPA tutorial on an example dataset is available on GitHub.
- **(finding)** SUPPA has command and subcommand structure. _[grounded: arch_commandSubcommand]_
- **(finding)** SUPPA includes functionality for generation of transcript events and local alternative splicing events.
- **(finding)** SUPPA includes functionality for PSI calculation for Transcripts and Events. _[grounded: comp_psiCalculation]_

## Steps

### Step `task_001`
- Title: Reconstruct the generateEvents command to produce ioe, ioi, and gtf artifacts from a GTF input
- Task kind: `component_reconstruction`
- Task: Implement the SUPPA2 generateEvents subcommand to parse a genome annotation GTF file and produce three named output artifacts: an ioe file (transcript events), an ioi file (event indices), and a gtf file containing local alternative splicing events.
- Inputs:
  - Genome annotation GTF file
- Expected outputs:
  - ioe file (index of events) mapping transcripts to events
  - ioi file (index of isoforms) mapping events to isoforms
  - gtf file containing local alternative splicing events
- Tools: SUPPA2
- Landmark output files: *.ioe, *.ioi, *_local_events.gtf

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the PSI calculation step from transcript quantification and ioe/ioi event files
- Task kind: `component_reconstruction`
- Task: Compute a PSI (Percent Spliced In) matrix by consuming transcript-level quantification output (e.g., from Salmon or kallisto) and a SUPPA2 event definition file (ioe or ioi format), then output a PSI matrix file.
- Inputs:
  - Transcript quantification file (Salmon quant.sf, kallisto abundance.tsv, or equivalent format with transcript IDs and TPM/count values)
  - SUPPA2 event definition file in ioe or ioi format (specifying alternative splicing events and constituent transcripts)
- Expected outputs:
  - PSI (Percent Spliced In) matrix file with events as rows and samples as columns, values in range [0, 1]
- Tools: SUPPA2
- Landmark output files: loaded_quantification.tsv, parsed_events.tsv
- Primary expected artifact: `psi_matrix.tsv`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the differential splicing analysis command from PSI matrices across multiple conditions
- Task kind: `component_reconstruction`
- Task: Implement the SUPPA2 diffSplice statistical test: consume per-condition PSI matrices and transcript expression files to compute differential splicing statistics (ΔPSI and p-value) for each alternative splicing event.
- Inputs:
  - PSI matrix files (one per condition, rows=events, columns=samples)
  - Transcript expression quantification files (TPM or equivalent, per condition)
- Expected outputs:
  - Differential splicing results table (TSV/CSV) with columns: event_id, dpsi, pvalue, and per-condition mean PSI values
- Tools: SUPPA2
- Landmark output files: psi_matrix_condition1.tsv, psi_matrix_condition2.tsv, transcript_expression_condition1.tsv, transcript_expression_condition2.tsv
- Primary expected artifact: `diffsplice_results.tsv`

## Final expected outputs

- `Differential splicing results table (TSV/CSV) with columns: event_id, dpsi, pvalue, and per-condition mean PSI values` (type: file, tolerance: hash)

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
  "workflow_id": "coll_suppa2_workflow",
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
    "Differential splicing results table (TSV/CSV) with columns: event_id, dpsi, pvalue, and per-condition mean PSI values": "<locator>"
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
