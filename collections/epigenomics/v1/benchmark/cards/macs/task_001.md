# SciTask Card: Reproduce the CTCF ChIP-Seq peak-calling result using MACS3 callpeak on single-end BED input

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T17:50:49.716879+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_epigenomics/coll_macs/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `statistical-analysis`
- GitHub: `macs3-project/MACS`
- Quality: Score 3/5 — 1 grounding failures

## Classification

- Task kind: `reproduction`

## Research Question
What are the read counts after duplicate filtering and the predicted fragment length d when running MACS3 callpeak on CTCF ChIP-Seq data?

## Connected Finding
MACS3 callpeak performs duplicate filtering as an initial step and predicts fragment length d, which is crucial for ChIP-Seq analysis and used in subsequent peak calling steps.

## Task Description
Run MACS3 callpeak on paired ChIP-Seq and control BED files (CTCF_ChIP_200K.bed.gz and CTCF_Control_200K.bed.gz) to identify transcription factor binding peaks and output narrowPeak format results with associated statistical tracks.

## Inputs
- CTCF_ChIP_200K.bed.gz (treatment ChIP-Seq reads in BED format)
- CTCF_Control_200K.bed.gz (control reads in BED format)

## Expected Outputs
- narrowPeak file containing peak regions with genomic coordinates, enrichment scores, and summit locations
- BEDGRAPH pileup track showing ChIP fragment coverage
- BEDGRAPH q-value score track for statistical enrichment

## Expected Output File

- `CTCF_ChIP_200K_peaks.narrowPeak`

## Landmark Outputs

- `CTCF_ChIP_200K_filterdup.bed`
- `CTCF_Control_200K_filterdup.bed`
- `CTCF_ChIP_200K_filterdup.pileup.bdg`
- `local_lambda.bdg`
- `CTCF_ChIP_200K_qvalue.bdg`
- `CTCF_ChIP_200K_peaks.narrowPeak`

## Tools
- macs3
- macs3 filterdup
- macs3 predictd
- macs3 pileup
- macs3 bdgcmp
- macs3 bdgopt
- macs3 bdgpeakcall

## Skills
- chip-seq-read-alignment-filtering
- fragment-length-estimation-cross-correlation
- chip-seq-signal-pileup-extension
- local-background-estimation-multiple-scales
- poisson-statistical-enrichment-testing
- narrow-peak-calling-score-threshold

## Workflow Description
1. Filter duplicate reads from both ChIP and control BED files using macs3 filterdup with --keep-dup=1, recording final read counts (ChIP: 199,583; Control: 199,867). 2. Predict fragment length d from filtered ChIP data using macs3 predictd with default mfold parameters -m 5 50 and genome size -g hs, yielding d=254 bp. 3. Generate ChIP pileup coverage track using macs3 pileup with --extsize 254 (the predicted fragment length). 4. Build local bias tracks from filtered control data using macs3 pileup with -B option at three scales (d/2=127 bp for d-background, 500 bp for 1 kb slocal, 5000 bp for 10 kb llocal), then normalize slocal and llocal backgrounds with macs3 bdgopt multiply operation (factors 0.254 and 0.0254 respectively). 5. Combine background tracks using macs3 bdgcmp max operation to determine maximum bias, then incorporate genome-wide background (0.0188023) via macs3 bdgopt. 6. Scale combined background by ChIP-to-control ratio (0.99858) using macs3 bdgopt multiply to create local lambda track. 7. Compare ChIP pileup against local lambda using macs3 bdgcmp with -m qpois to generate q-value scores for each base pair. 8. Call narrow peaks from q-value track using macs3 bdgpeakcall with cutoff 1.301 (q-value 0.05 in -log10 format), minimum peak length 245 bp (fragment length d), and gap parameter 100 bp (read length), outputting narrowPeak format.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/callvar_algorithm.jpeg` | figure | False |
| `figures/pileup.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog provided documenting MACS3 version, release date, or modifications

## Domain Knowledge
- ChIP-Seq peak calling requires removing PCR duplicates (typically keeping only 1 read per genomic position) to avoid artificial signal inflation and obtain accurate enrichment estimates.
- Fragment length d is the physical DNA fragment length bound by the protein of interest; predicted from read cross-correlation, it is essential for extending single-end reads and normalizing multi-scale background models.
- MACS3 callpeak internally combines four background noise models (d-sized, 1 kb local, 10 kb local, and whole-genome) by taking the maximum at each position to adapt the background to local chromatin complexity.
- The q-value (BH-adjusted p-value) from local Poisson comparison of ChIP pileup against control lambda is the standard statistical metric for peak significance; typical cutoffs range from 0.01 to 0.1 on the -log10 scale (corresponding to q-values 0.1 to 0.01).
- Narrow peaks (CTCF, TFs) require stringent cutoffs and minimum peak length constraints (typically fragment length d), whereas broad peaks (histone marks) use lower cutoffs and larger gap-merging parameters.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: macs3, macs3 filterdup, macs3 predictd, macs3 pileup, macs3 bdgcmp, macs3 bdgopt, macs3 bdgpeakcall, BEDGRAPH pileup track showing ChIP fragment coverage, BEDGRAPH q-value score track for statistical enrichment.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [methods] What are the read counts after duplicate filtering and the predicted fragment length d when running MACS3 callpeak on CTCF ChIP-Seq data?: 'In the initial step of ChIP-Seq analysis with `callpeak`, we read both ChIP and control data and remove redundant reads from each genomic location'
- `ev_002` from `agent2_synthesis` (agent2_traced): [methods] MACS3 callpeak performs duplicate filtering as an initial step and predicts fragment length d, which is crucial for ChIP-Seq analysis and used in subsequent peak calling steps.: 'This is a crucial step for analyzing ChIP-Seq with MACS3, as well as other types of data'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] CTCF_ChIP_200K.bed.gz (treatment ChIP-Seq reads in BED format): 'We'll use two test files, `CTCF_ChIP_200K.bed.gz` and `CTCF_Control_200K.bed.gz`, which you can find in the MACS3 GitHub repository in the `test` directory'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] CTCF_Control_200K.bed.gz (control reads in BED format): 'We'll use two test files, `CTCF_ChIP_200K.bed.gz` and `CTCF_Control_200K.bed.gz`, which you can find in the MACS3 GitHub repository in the `test` directory'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] narrowPeak file containing peak regions with genomic coordinates, enrichment scores, and summit locations: 'The output is essentially a narrowPeak format file (a type of BED file), which includes the locations of peaks with the summit location noted in the last column'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] BEDGRAPH pileup track showing ChIP fragment coverage: 'This command produces a file in BEDGRAPH format, `CTCF_ChIP_200K_filterdup.pileup.bdg`, which contains the fragment pileup signals for the ChIP sample'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] BEDGRAPH q-value score track for statistical enrichment: 'The `CTCF_ChIP_200K_qvalue.bdg` file contains the `-log10(q-values)` for each base pair, derived through a local Poisson test'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] macs3: 'MACS3 does offer a range of subcommands that allow you to customize every step of your analysis'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] macs3 filterdup: 'we'll explain how you can accomplish this using the `filterdup` subcommand'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] macs3 predictd: 'This can also be accomplished using the `predictd` subcommand, which we need to apply only to ChIP data'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] macs3 pileup: 'generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] macs3 bdgcmp: 'using the `bdgcmp` module, which outputs a score for each base pair in the genome'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] macs3 bdgopt: 'apply the `bdgopt` subcommand'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] macs3 bdgpeakcall: 'identify regions that surpass a specific score cutoff using the `bdgpeakcall` function for narrow peak calling'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] No changelog provided documenting MACS3 version, release date, or modifications: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file CTCF_ChIP_200K.bed.gz exists in github:macs3-project__MACS/test directory
- verify file CTCF_Control_200K.bed.gz exists in github:macs3-project__MACS/test directory
- script_runs: macs3 callpeak command completes without error on the two input files
- file_exists: narrowPeak output file is generated
- file_format_is: narrowPeak output follows ENCODE narrowPeak format specification
- verify filterdup read count reported in callpeak log output is numeric and positive
- verify predicted fragment length d value reported in callpeak log output is numeric and positive
- value_in_range: predicted fragment length d is within biologically plausible range for chromatin (typically 100–300 bp), parameter-sensitive to organism and ChIP target

### Expert Review
- assess whether reported filterdup read count (number of reads after duplicate removal) is reasonable relative to input file size and CTCF ChIP-Seq expectations
- assess whether predicted fragment length d aligns with typical nucleosome-scale or protein-DNA interaction lengths for CTCF binding
- assess whether narrowPeak peak calls show expected genomic distribution and enrichment characteristics for CTCF (known motif-driven regulator)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Filter duplicate reads from ChIP and control samples using macs3 filterdup with --keep-dup=1 to remove PCR artifacts.
2. Estimate fragment length d from filtered ChIP data using macs3 predictd with mfold parameters 5 50.
3. Generate multi-scale background models (d, 1 kb, 10 kb, genome-wide) from control pileup using macs3 pileup with -B extension and macs3 bdgopt normalization.
4. Combine background tracks via maximum operation with macs3 bdgcmp and scale by ChIP-to-control read count ratio.
5. Compute base-pair q-values using macs3 bdgcmp qpois comparing ChIP pileup against local lambda via local Poisson test.
6. Call narrow peaks with macs3 bdgpeakcall using cutoff 1.301 (-log10 q-value 0.05), minimum length 245 bp, and gap 100 bp.
7. Validation: output narrowPeak file exists with non-zero peak count, q-value scores in BedGraph span expected range, and peak intervals do not overlap read artifacts.

## Workflow Ports

**Inputs:**

- `chip_reads` — ChIP-Seq treatment reads (BED format)
- `control_reads` — Control reads (BED format)

**Outputs:**

- `narrowpeak` — Called peaks in narrowPeak format
- `chip_pileup` — ChIP pileup coverage BEDGRAPH
- `qvalue_track` — Q-value enrichment scores BEDGRAPH

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:macs3-project__MACS`
- **Synthesized at:** 2026-06-15T17:56:46+00:00

## Extraction Quality
- Score: 3/5
- Coherent: true
- Placeholder detected: false
- Groundedness failures (1):
  - expected_outputs[2]: evidence_span not found in section 'methods' (value='BEDGRAPH q-value score track for statistical enrichment', span='The `CTCF_ChIP_200K_qvalue.bdg` file contains the `-log10(q-')
- Notes: The card exhibits good structural coherence and domain depth (skills, domain_knowledge, methodology_summary are thorough), but the research_question and finding lack specificity in their grounding. The evidence_spans are too generic and don't cite specific outputs or values. The groundedness failure for expected_outputs[2] indicates a truncated evidence span. More critically, the research_question should ask 'What are the specific post-filterdup read counts and predicted fragment length d value when running MACS3 callpeak on CTCF ChIP-Seq data?' to semantically match the task_objective. The finding would be stronger if it cited actual numbers (e.g., '254 bp') or the specific reporting mechanism (e.g., 'callpeak log output'). The workflow_description is excellent and highly specific, suggesting the source material exists but was not adequately reflected in upstream fields.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
