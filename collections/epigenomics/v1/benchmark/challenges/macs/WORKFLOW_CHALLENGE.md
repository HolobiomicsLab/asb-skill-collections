# Workflow Challenge: `coll_macs_workflow`


> MACS3 is a model-based ChIP-Seq peak-calling tool that implements duplicate filtering, fragment-length prediction, and local-background normalization to identify enriched genomic regions.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MACS3 performs ChIP-Seq peak calling through a multi-step pipeline beginning with duplicate filtering of aligned reads and prediction of fragment length d from ChIP data using cross-correlation analysis. The pipeline then generates coverage tracks via pileup, constructs local-background lambda tracks from control data at multiple scales (d, 1kb, 10kb, and genome-wide), and compares ChIP and control signals using a Poisson model to compute p-value or q-value scores at each genomic position. Final peak identification is achieved by applying score cutoffs to identify contiguous enriched regions. MACS3 also provides granular subcommands—filterdup, predictd, pileup, bdgcmp, bdgopt, and bdgpeakcall—that enable users to execute and customize each analysis step independently, supporting both single-end and paired-end sequencing data.

## Research questions

- What are the read counts after duplicate filtering and the predicted fragment length d when running MACS3 callpeak on CTCF ChIP-Seq data?
- How does the MACS3 callpeak pipeline decompose into individual subcommands (filterdup, predictd, pileup, bdgcmp, bdgopt, bdgpeakcall) that progressively transform ChIP-Seq data into peak calls?
- Does MACS3 callpeak correctly estimate the average insertion length (~253 bp) when processing paired-end ChIP-Seq data in the CTCF_PE_ChIP_chr22_50k.bedpe.gz file?

## Methods overview

Filter duplicate reads from ChIP and control samples using macs3 filterdup with --keep-dup=1 to remove PCR artifacts. Estimate fragment length d from filtered ChIP data using macs3 predictd with mfold parameters 5 50. Generate multi-scale background models (d, 1 kb, 10 kb, genome-wide) from control pileup using macs3 pileup with -B extension and macs3 bdgopt normalization. Combine background tracks via maximum operation with macs3 bdgcmp and scale by ChIP-to-control read count ratio. Compute base-pair q-values using macs3 bdgcmp qpois comparing ChIP pileup against local lambda via local Poisson test. Call narrow peaks with macs3 bdgpeakcall using cutoff 1.301 (-log10 q-value 0.05), minimum length 245 bp, and gap 100 bp. Validation: output narrowPeak file exists with non-zero peak count, q-value scores in BedGraph span expected range, and peak intervals do not overlap read artifacts. Filter duplicate reads from ChIP and control samples to remove redundant reads at identical genomic locations, recording final read counts for normalization. Predict the fragment length parameter d from filtered ChIP data using autocorrelation-based fragment length estimation. Generate ChIP pileup BEDGRAPH by extending reads in the 5′→3′ direction to the predicted fragment length. Build multi-scale local background bias tracks from control by computing pileup signals at d, slocal (1 kb), and llocal (10 kb) window sizes, then normalizing by the ratio d/window_size. Combine background tracks by iteratively computing maximum values across all scales and the genome-wide background count. Scale the combined local lambda bias track to match the ChIP sample sequencing depth using the ratio of final read counts. Apply local Poisson test by comparing ChIP pileup against scaled local lambda to generate -log10(q-value) or -log10(p-value) score tracks. Validation: Call narrow peaks using bdgpeakcall with user-specified cutoff (e.g., 1.301 for q≤0.05), minimum peak length equal to fragment length d, and gap parameter set to read length; verify output is in narrowPeak BED format with summit locations. Estimate average insertion length (fragment length d) from paired-end read pairs using macs3 predictd with -f BEDPE flag. Generate ChIP signal pileup track using macs3 pileup with paired-end input (no --extsize needed); pileup automatically spans between read pair 5' positions. Build local background noise tracks from control data at multiple scales (d, slocal=1kb, llocal=10kb) using macs3 pileup with -B option and compute genome-wide background. Normalize and combine background tracks using macs3 bdgopt and macs3 bdgcmp to generate maximum local bias (lambda) track scaled to match ChIP sequencing depth. Compare ChIP pileup to local lambda using macs3 bdgcmp with Poisson model (-m qpois) to generate q-value score track at each genomic position. Call narrow peaks by identifying regions exceeding a q-value cutoff using macs3 bdgpeakcall with read length (-g) and fragment length (-l) parameters; output narrowPeak format with summit coordinates. Validation: confirm narrowPeak file exists, contains proper BED format with 5 required columns plus summit position, and reported average insertion length from predictd matches expected ~253 bp metric.

**Domain:** unknown

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MACS v3 requires Python3, with testing conducted on Python versions 3.9 to 3.12.
- **(finding)** MACS3 requires NumPy version 1.25 or higher. _[grounded: MACS3]_
- **(finding)** MACS3 requires hmmlearn version 0.3.2 or higher. _[grounded: MACS3]_
- **(finding)** MACS3 requires scikit-learn version 1.3 or higher. _[grounded: MACS3]_
- **(finding)** MACS3 requires SciPy version 1.12 or higher. _[grounded: MACS3]_
- **(finding)** Cython version must be 3.0 or higher for MACS3. _[grounded: MACS3]_
- **(finding)** MACS3 requires cykhash version 2. _[grounded: MACS3]_
- **(finding)** In the MACS3 peak calling workflow, ChIP and control samples are filtered to allow only one duplicate read per location by default. _[grounded: MACS3]_
- **(finding)** In the example MACS3 analysis, the ChIP sample retained 199,583 reads after duplicate filtering. _[grounded: MACS3]_
- **(finding)** In the example MACS3 analysis, the control sample retained 199,867 reads after duplicate filtering. _[grounded: MACS3]_
- **(finding)** The ratio of ChIP to control reads in the example MACS3 analysis is approximately 0.99858. _[grounded: MACS3]_
- **(finding)** The predictd subcommand in MACS3 determined a fragment length of 254 base pairs for the CTCF ChIP sample. _[grounded: MACS3]_
- **(finding)** For paired-end data in MACS3, the predictd function reports an average insertion length of 253 base pairs. _[grounded: MACS3]_
- **(finding)** The default slocal window size in MACS3 callpeak is 1 kilobase. _[grounded: MACS3]_
- **(finding)** The default llocal window size in MACS3 callpeak is 10 kilobases. _[grounded: MACS3]_
- **(finding)** In the example MACS3 analysis, the normalization factor for the 1kb background is 0.254, calculated as d/slocal (254/1000). _[grounded: MACS3]_
- **(finding)** In the example MACS3 analysis, the normalization factor for the 10kb background is 0.0254, calculated as d/llocal (254/10000). _[grounded: MACS3]_
- **(finding)** In the example MACS3 analysis, the whole genome background is calculated as 0.0188023, derived from 199,867 reads × 254 bp / 2,700,000,000 bp. _[grounded: MACS3]_
- **(finding)** In the example MACS3 analysis, the control bias is scaled down by a factor of 0.99858 to match the ChIP sequencing depth. _[grounded: MACS3]_
- **(finding)** MACS3 bdgcmp provides a ppois function that calculates Poisson p-value in -log10(pvalue) form. _[grounded: MACS3]_
- **(finding)** MACS3 bdgcmp provides a qpois function that calculates q-value through a Benjamini-Hochberg process for Poisson p-values. _[grounded: MACS3]_
- **(finding)** MACS3 bdgcmp provides an FE function that calculates linear scale fold enrichment. _[grounded: MACS3]_
- **(finding)** MACS3 bdgcmp provides a logFE function that calculates log10 fold enrichment. _[grounded: MACS3]_
- **(finding)** MACS3 bdgcmp provides a logLR function that calculates log10 likelihood between ChIP-enriched and open chromatin models. _[grounded: MACS3]_
- **(finding)** MACS3 bdgcmp provides a slogLR function that calculates symmetric log10 likelihood between two ChIP-enrichment models. _[grounded: MACS3]_
- **(finding)** MACS3 bdgcmp provides a max function that returns the maximum value between two tracks. _[grounded: MACS3]_
- **(finding)** In MACS3 bdgbroadcall, the default cutoff for stronger and narrower peaks is 2. _[grounded: MACS3]_
- **(finding)** In MACS3 bdgbroadcall, the default cutoff for weaker and broader regions is 1. _[grounded: MACS3]_
- **(finding)** In MACS3 bdgbroadcall, the default minimum length for stronger peaks is 200 base pairs. _[grounded: MACS3]_
- **(finding)** In MACS3 bdgbroadcall, the default maximum gap between stronger peaks is 30 base pairs. _[grounded: MACS3]_
- **(finding)** In MACS3 bdgbroadcall, the default maximum gap between weaker peaks is 800 base pairs. _[grounded: MACS3]_
- **(finding)** MACS3 will discard unmapped reads as bad alignments. _[grounded: MACS3]_
- **(finding)** MACS3 will discard non-primary alignments as bad alignments. _[grounded: MACS3]_
- **(finding)** MACS3 will discard reads that fail quality control as bad alignments. _[grounded: MACS3]_
- **(finding)** MACS3 will discard supplementary alignments as bad alignments. _[grounded: MACS3]_
- **(finding)** For paired-end reads in MACS3, the second read in the pair is discarded during processing. _[grounded: MACS3]_
- **(finding)** MACS3 provides a filterdup subcommand for removing duplicate reads. _[grounded: MACS3]_
- **(finding)** MACS3 provides a predictd subcommand for estimating DNA fragment length. _[grounded: MACS3]_
- **(finding)** MACS3 provides a pileup subcommand for generating pileup tracks. _[grounded: MACS3]_
- **(finding)** MACS3 provides a bdgopt subcommand for performing operations on bedGraph files. _[grounded: MACS3]_
- **(finding)** MACS3 provides a bdgcmp subcommand for comparing bedGraph files. _[grounded: MACS3]_
- **(finding)** MACS3 provides a bdgpeakcall subcommand for calling narrow peaks. _[grounded: MACS3]_
- **(finding)** MACS3 provides a bdgbroadcall subcommand for calling broad peaks. _[grounded: MACS3]_
- **(finding)** MACS3 peak calling workflow applies cross-correlation model analysis to estimate fragment length. _[grounded: MACS3]_
- **(finding)** The BED format is widely used to store genome annotations. _[grounded: bed_format]_
- **(finding)** BEDPE format contains three columns: chromosome, leftmost position of read pair, and rightmost position of read pair. _[grounded: bedpe_format]_
- **(finding)** FRAG format contains the chromosome, leftmost position of aligned fragment, rightmost position of aligned fragment, barcode information, and fragment counts. _[grounded: frag_format]_
- **(finding)** Only Linux and Mac OS systems are currently supported for MACS3 installation. _[grounded: MACS3]_
- **(finding)** MACS3 can be installed through PyPI using pip. _[grounded: MACS3]_
- **(finding)** MACS3 can be installed through conda using the bioconda channel. _[grounded: MACS3]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- finding a tool that's more suited to their data type, as `callpeak` is specifically optimized for ChIP-Seq
- use the -B option for DNAse-Seq data or when cutting site is believed to be centrally located
- skip predictd step if you have more accurate estimate of fragment length
- bdgpeakcall for narrow peaks or bdgbroadcall for broad marks
- if you only want to call broader peak and not interested in nested peak structure, simply use `bdgpeakcall` with weaker cutoff

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- bedGraph files from MACS3 are required to use in bdgbroadcall command, as all regions on the same chromosome should be continuous
- for paired-end data in BAM format, must specify -f BAMPE option to get BEDPE format output
- for paired-end data, BAM file for callvar must be sorted and indexed

## Steps

### Step `task_001`
- Title: Reproduce the CTCF ChIP-Seq peak-calling result using MACS3 callpeak on single-end BED input
- Task kind: `reproduction`
- Task: Run MACS3 callpeak on paired ChIP-Seq and control BED files (CTCF_ChIP_200K.bed.gz and CTCF_Control_200K.bed.gz) to identify transcription factor binding peaks and output narrowPeak format results with associated statistical tracks.
- Inputs:
  - CTCF_ChIP_200K.bed.gz (treatment ChIP-Seq reads in BED format)
  - CTCF_Control_200K.bed.gz (control reads in BED format)
- Expected outputs:
  - narrowPeak file containing peak regions with genomic coordinates, enrichment scores, and summit locations
  - BEDGRAPH pileup track showing ChIP fragment coverage
  - BEDGRAPH q-value score track for statistical enrichment
- Tools: macs3, macs3 filterdup, macs3 predictd, macs3 pileup, macs3 bdgcmp, macs3 bdgopt, macs3 bdgpeakcall
- Landmark output files: CTCF_ChIP_200K_filterdup.bed, CTCF_Control_200K_filterdup.bed, CTCF_ChIP_200K_filterdup.pileup.bdg, local_lambda.bdg, CTCF_ChIP_200K_qvalue.bdg, CTCF_ChIP_200K_peaks.narrowPeak
- Primary expected artifact: `CTCF_ChIP_200K_peaks.narrowPeak`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the manual callpeak pipeline: pileup, local-lambda, bdgcmp scoring, and bdgpeakcall
- Task kind: `component_reconstruction`
- Task: Re-implement the MACS3 callpeak pipeline using individual subcommands (filterdup, predictd, pileup, bdgcmp, bdgopt, bdgpeakcall) on CTCF ChIP-Seq test datasets to produce ChIP pileup, local lambda bias, and p/q-value score BEDGRAPH files.
- Inputs:
  - CTCF_ChIP_200K.bed.gz (gzipped BED file with ChIP-Seq reads)
  - CTCF_Control_200K.bed.gz (gzipped BED file with control reads)
- Expected outputs:
  - CTCF_ChIP_200K_filterdup.pileup.bdg (ChIP sample pileup track in BEDGRAPH format with fragment-extended coverage signals)
  - local_lambda.bdg (local lambda bias track in BEDGRAPH format scaled to ChIP sequencing depth for statistical comparison)
  - CTCF_ChIP_200K_qvalue.bdg or CTCF_ChIP_200K_pvalue.bdg (score track in BEDGRAPH format with -log10(q-values) or -log10(p-values) from local Poisson test)
  - CTCF_ChIP_200K_peaks.bed (narrowPeak format BED file with called peak coordinates and summit locations)
- Tools: MACS3, macs3 filterdup, macs3 predictd, macs3 pileup, macs3 bdgcmp, macs3 bdgopt, macs3 bdgpeakcall
- Landmark output files: CTCF_ChIP_200K_filterdup.bed, CTCF_Control_200K_filterdup.bed, CTCF_ChIP_200K_filterdup.pileup.bdg, d_bg.bdg, 1k_bg_norm.bdg, 10k_bg_norm.bdg
- Primary expected artifact: `CTCF_ChIP_200K_qvalue.bdg`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the genome-background lambda and normalization multiplier metrics for the CTCF tutorial run
- Task kind: `reproduction`
- Task: Run MACS3 callpeak on paired-end ChIP-Seq data (CTCF_PE_ChIP_chr22_50k.bedpe.gz) in paired-end mode to call narrow peaks, confirming the average insertion length metric (~253 bp) and producing a narrowPeak output file.
- Inputs:
  - CTCF_PE_ChIP_chr22_50k.bedpe.gz (paired-end ChIP-Seq alignment file in BEDPE format)
- Expected outputs:
  - narrowPeak format peak file containing called peak locations with summit coordinates
  - Average insertion length metric reported as ~253 bp from predictd step
- Tools: MACS3, macs3 predictd, macs3 callpeak
- Landmark output files: *_treat_pileup.bdg, *_control_lambda.bdg, *_qvalue.bdg
- Primary expected artifact: `peaks.narrowPeak`

## Final expected outputs

- `CTCF_ChIP_200K_filterdup.pileup.bdg (ChIP sample pileup track in BEDGRAPH format with fragment-extended coverage signals)` (type: file, tolerance: hash)
- `local_lambda.bdg (local lambda bias track in BEDGRAPH format scaled to ChIP sequencing depth for statistical comparison)` (type: file, tolerance: hash)
- `CTCF_ChIP_200K_qvalue.bdg or CTCF_ChIP_200K_pvalue.bdg (score track in BEDGRAPH format with -log10(q-values) or -log10(p-values) from local Poisson test)` (type: file, tolerance: hash)
- `CTCF_ChIP_200K_peaks.bed (narrowPeak format BED file with called peak coordinates and summit locations)` (type: file, tolerance: hash)
- `narrowPeak format peak file containing called peak locations with summit coordinates` (type: file, tolerance: hash)
- `Average insertion length metric reported as ~253 bp from predictd step` (type: file, tolerance: hash)

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

- **Composition modularity:** hierarchical

- **Abstraction level:** concrete

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
  "workflow_id": "coll_macs_workflow",
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
    "CTCF_ChIP_200K_filterdup.pileup.bdg (ChIP sample pileup track in BEDGRAPH format with fragment-extended coverage signals)": "<locator>",
    "local_lambda.bdg (local lambda bias track in BEDGRAPH format scaled to ChIP sequencing depth for statistical comparison)": "<locator>",
    "CTCF_ChIP_200K_qvalue.bdg or CTCF_ChIP_200K_pvalue.bdg (score track in BEDGRAPH format with -log10(q-values) or -log10(p-values) from local Poisson test)": "<locator>",
    "CTCF_ChIP_200K_peaks.bed (narrowPeak format BED file with called peak coordinates and summit locations)": "<locator>",
    "narrowPeak format peak file containing called peak locations with summit coordinates": "<locator>",
    "Average insertion length metric reported as ~253 bp from predictd step": "<locator>"
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
