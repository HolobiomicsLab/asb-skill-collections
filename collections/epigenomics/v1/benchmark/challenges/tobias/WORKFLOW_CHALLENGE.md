# Workflow Challenge: `coll_tobias_workflow`


> TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data by analyzing local Tn5 insertion patterns to detect transcription factor binding.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Analyses 1 derived result: ATAC-seq data exhibits a visible depletion of Tn5 insertions around chromatin sites bound by transcription factor proteins, a signal pattern known as footprints that distinguishes bound from unbound motif locations. Reconstructs 3 described mechanisms (described in the paper but not separately evaluated there): ATAC-seq generates signal data from Tn5 transposase insertions at accessible chromatin sites, which contain information about transcription factor binding through patterns of insertion depletion (footprints) around protein-bound regions. TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data, which operates by analyzing the local distribution of Tn5 insertions to detect transcription factor binding through characteristic depletion patterns. TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data, enabling detection of transcription factor occupancy through analysis of Tn5 insertion patterns. Extends the paper in 1 task beyond its reported scope: ATAC-seq footprinting analysis can detect transcription factor binding through the visible depletion of Tn5 insertions around protein-bound sites, providing a basis for differential occupancy analysis across conditions.

## Research questions

- How does the TOBIAS ATACorrect module correct for Tn5 transposase insertion bias in ATAC-seq data to produce bias-corrected signal tracks?
- How does TOBIAS compute footprint scores from bias-corrected ATAC-seq signal data across accessible chromatin regions?
- How does TOBIAS identify transcription factor occupancy at specific genomic locations by analyzing ATAC-seq footprint patterns across different conditions?
- What is the characteristic pattern of Tn5 insertion depletion around transcription factor binding sites versus non-binding sites across a genomic region?
- Can the TOBIAS pipeline (bias correction, footprint scoring, and BINDetect) be applied to a two-condition ATAC-seq experiment to identify differential transcription factor occupancy between conditions?

## Methods overview

Load ATAC-seq BAM file and reference genome sequence Quantify and model Tn5 insertion bias from observed insertions across genomic regions and DNA sequence context Apply bias correction to normalized signal by position-weight adjustment Convert corrected signal to bigWig format for visualization and downstream analysis Validation: Corrected signal track exhibits reduced sequence-context bias and preserved footprint visibility at known transcription factor binding sites References: source article (DOI: 10.1038/s41467-020-18035-1) Load bias-corrected bigWig signal file and accessible genomic region coordinates. Apply ScoreBigwig to compute position-wise footprint depletion scores across the genome. Output scored bigWig file encoding footprint strength at each position. Validation: verify output bigWig is valid format and contains non-empty score distributions. References: source article (DOI: 10.1038/s41467-020-18035-1) Load ATAC-seq footprint score files (BIGWIG/HDF5) preprocessed by prior TOBIAS steps. Provide or scan motif database (JASPAR-format PWMs) against genomic peaks. Run TOBIAS BINDetect to compare footprint signal intensity at motif sites across conditions. Extract occupancy predictions (bound/unbound state) and binding confidence scores per motif. Validation: occupancy predictions must pass QC checks on motif-site coverage and footprint signal-to-noise ratio; predictions should show expected condition-specific differences in occupancy for known differentially-regulated transcription factors. References: source article (DOI: 10.1038/s41467-020-18035-1) Load ATAC-seq BAM file and extract Tn5 insertion positions from aligned read 5' ends (or start coordinates). Annotate motif sites as bound or unbound based on chromatin accessibility signal or external binding data. For each motif instance, extract Tn5 insertion counts in fixed-width flanking windows (e.g. ±100 bp) at single-nucleotide or fine-grain bin resolution. Aggregate insertion counts across all motif sites within each binding class and compute positional statistics (mean, standard deviation). Tabulate positional insertion distributions and generate comparative visualization (e.g. line plot) of bound versus unbound profiles to confirm footprint depletion. Validation: footprint signal is confirmed by visual inspection of depletion pattern at bound sites (reduced insertion density flanking the motif) and absence of depletion at unbound sites. References: source article (DOI: 10.1038/s41467-020-18035-1) Retrieve two-condition ATAC-seq BAM alignments and peak annotations from public repository (GEO/SRA). Correct Tn5 transposase insertion bias in both conditions using TOBIAS ATACorrect. Compute footprint enrichment signals genome-wide for each condition using TOBIAS FootprintScores. Perform differential TF occupancy analysis between conditions at known TFBS motif sites using TOBIAS BINDetect. Validation: Differential TF occupancy table and summary plot successfully generated with statistically significant TFs identified (p < 0.05) and footprint patterns visually distinct between conditions. References: source article (DOI: 10.1038/s41467-020-18035-1)

**Domain:** transcriptomics

**Techniques:** enrichment-analysis, statistical-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** ATAC-seq applies a Tn5 Transposase to insert sequencing adapters into accessible chromatin. _[grounded: ATAC_seq_assay]_
- **(finding)** The local distribution of Tn5 insertions contains information about transcription factor binding due to visible depletion of insertions around sites bound by protein, known as footprints.

## Steps

### Step `task_001`
- Title: Reconstruct the Tn5 insertion bias correction step within the TOBIAS ATAC-seq footprinting pipeline
- Task kind: `component_reconstruction`
- Task: Correct Tn5 transposase insertion bias from an ATAC-seq BAM file using the TOBIAS ATACorrect module to produce a bias-corrected bigWig signal track.
- Inputs:
  - ATAC-seq aligned BAM file with Tn5 insertion coordinates
  - Reference genome FASTA sequence
- Expected outputs:
  - Bias-corrected bigWig signal track
- Tools: TOBIAS
- Landmark output files: bias_model.pkl, bias_corrected_signal.bw
- Primary expected artifact: `bias_corrected_signal.bw`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the footprint scoring step that converts bias-corrected ATAC-seq signal into per-base footprint scores
- Task kind: `component_reconstruction`
- Task: Compute footprint scores from a bias-corrected bigWig file over accessible genomic regions using ScoreBigwig, producing a scored bigWig output that quantifies transcription factor binding signal depletion at footprint sites.
- Inputs:
  - Bias-corrected bigWig file from ATAC-seq signal normalization
  - Accessible genomic regions (BED or similar format)
- Expected outputs:
  - Scored bigWig file with footprint scores at each genomic position
- Tools: TOBIAS
- Landmark output files: footprint_scores.bw
- Primary expected artifact: `footprint_scores.bw`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the transcription factor occupancy prediction step that classifies TF binding from footprint scores at motif sites
- Task kind: `component_reconstruction`
- Task: Run TOBIAS BINDetect to predict transcription factor occupancy by comparing ATAC-seq footprint scores at motif-matched sites across conditions, producing a structured table of bound/unbound predictions per TF motif.
- Inputs:
  - TOBIAS-preprocessed footprint score files (BIGWIG or HDF5 format) from ATAC-seq data, one per condition or replicate
  - Motif database in JASPAR or compatible format containing transcription factor position-weight matrices
  - Peak or genomic region coordinates (BED or NARROWPEAK format) where motif scanning will be performed
- Expected outputs:
  - Structured table (CSV/TSV) containing transcription factor motif occupancy predictions with columns: motif ID, genomic location, occupancy state (bound/unbound), binding score/probability, and condition-specific metrics
- Tools: TOBIAS
- Landmark output files: motif_scan_results.bed, footprint_vs_motif_match.tsv, tf_occupancy_predictions.csv
- Primary expected artifact: `tf_occupancy_predictions.csv`

### Step `task_004`
- Depends on: `task_003`
- Title: Analyze the distribution of Tn5 insertion events around known transcription factor binding sites from a public ATAC-seq dataset
- Task kind: `analysis`
- Task: Using a public ATAC-seq dataset and a reference set of transcription factor (TF) motif coordinates, quantify and tabulate Tn5 insertion counts in flanking windows (e.g. ±100 bp) around bound versus unbound motif sites to empirically characterize the footprint signal—regions of nucleotide depletion marking protein occupancy.
- Inputs:
  - ATAC-seq BAM alignment file from a public repository (GEO/SRA accession or direct URL)
  - Reference set of transcription factor motif genomic coordinates (BED format or similar)
- Expected outputs:
  - Tabulated positional distribution of Tn5 insertion counts for bound and unbound motif sites
  - Visualization (line plot or heatmap) of insertion profiles showing footprint signal (depletion at bound sites)
- Tools: TOBIAS
- Landmark output files: motif_sites_classified.bed, tn5_insertions_per_site.txt, insertion_counts_by_position.csv, footprint_profile_bound_vs_unbound.png
- Primary expected artifact: `tn5_insertion_distribution_table.csv`

### Step `task_005`
- Depends on: `task_003`
- Title: Extend TOBIAS footprinting to an ATAC-seq dataset deposited in GEO and report TF differential occupancy across two conditions
- Task kind: `extension`
- Task: Apply the complete TOBIAS pipeline (bias correction, footprint scoring, and BINDetect differential analysis) to a publicly available two-condition ATAC-seq dataset from GEO/SRA to identify differential transcription factor occupancy. Produce a differential TF occupancy results table (.tsv) and summary visualization (.pdf or .png).
- Inputs:
  - Raw ATAC-seq BAM alignments (condition 1) from GEO/SRA accession
  - Raw ATAC-seq BAM alignments (condition 2) from GEO/SRA accession
  - Peak annotations (BED or narrowPeak format) for both conditions
  - Known TFBS motif library (PWM or MEME format)
- Expected outputs:
  - Differential TF occupancy results table (.tsv) with TF names, footprint scores per condition, log2 fold-change, and p-values
  - Summary visualization (.pdf or .png) showing top differential TFs and footprint patterns across conditions
- Tools: TOBIAS
- Landmark output files: bias_corrected_condition1.bam, bias_corrected_condition2.bam, footprint_scores_condition1.bw, footprint_scores_condition2.bw, bindetect_results.tsv, summary_visualization.pdf
- Primary expected artifact: `differential_tf_occupancy.tsv`

## Final expected outputs

- `Tabulated positional distribution of Tn5 insertion counts for bound and unbound motif sites` (type: file, tolerance: hash)
- `Visualization (line plot or heatmap) of insertion profiles showing footprint signal (depletion at bound sites)` (type: file, tolerance: hash)
- `Differential TF occupancy results table (.tsv) with TF names, footprint scores per condition, log2 fold-change, and p-values` (type: file, tolerance: hash)
- `Summary visualization (.pdf or .png) showing top differential TFs and footprint patterns across conditions` (type: file, tolerance: hash)

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
  "workflow_id": "coll_tobias_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
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
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Tabulated positional distribution of Tn5 insertion counts for bound and unbound motif sites": "<locator>",
    "Visualization (line plot or heatmap) of insertion profiles showing footprint signal (depletion at bound sites)": "<locator>",
    "Differential TF occupancy results table (.tsv) with TF names, footprint scores per condition, log2 fold-change, and p-values": "<locator>",
    "Summary visualization (.pdf or .png) showing top differential TFs and footprint patterns across conditions": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
