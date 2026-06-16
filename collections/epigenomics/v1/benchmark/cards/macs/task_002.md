# SciTask Card: Reconstruct the manual callpeak pipeline: pileup, local-lambda, bdgcmp scoring, and bdgpeakcall

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T17:50:49.716879+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_epigenomics/coll_macs/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `statistical-analysis`
- GitHub: `macs3-project/MACS`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, 2 grounding failures

## Classification

- Task kind: `component_reconstruction`

## Research Question
How does the MACS3 callpeak pipeline decompose into individual subcommands (filterdup, predictd, pileup, bdgcmp, bdgopt, bdgpeakcall) that progressively transform ChIP-Seq data into peak calls?

## Connected Finding
The MACS3 callpeak pipeline operates through sequential subcommands: filterdup removes duplicate reads, predictd estimates fragment length d from ChIP data, pileup generates coverage tracks, bdgcmp compares ChIP and control signals to compute p/q-value scores, bdgopt applies optimization to score tracks, and bdgpeakcall identifies peaks by filtering regions above a score cutoff.

## Task Description
Re-implement the MACS3 callpeak pipeline using individual subcommands (filterdup, predictd, pileup, bdgcmp, bdgopt, bdgpeakcall) on CTCF ChIP-Seq test datasets to produce ChIP pileup, local lambda bias, and p/q-value score BEDGRAPH files.

## Inputs
- CTCF_ChIP_200K.bed.gz (gzipped BED file with ChIP-Seq reads)
- CTCF_Control_200K.bed.gz (gzipped BED file with control reads)

## Expected Outputs
- CTCF_ChIP_200K_filterdup.pileup.bdg (ChIP sample pileup track in BEDGRAPH format with fragment-extended coverage signals)
- local_lambda.bdg (local lambda bias track in BEDGRAPH format scaled to ChIP sequencing depth for statistical comparison)
- CTCF_ChIP_200K_qvalue.bdg or CTCF_ChIP_200K_pvalue.bdg (score track in BEDGRAPH format with -log10(q-values) or -log10(p-values) from local Poisson test)
- CTCF_ChIP_200K_peaks.bed (narrowPeak format BED file with called peak coordinates and summit locations)

## Expected Output File

- `CTCF_ChIP_200K_qvalue.bdg`

## Landmark Outputs

- `CTCF_ChIP_200K_filterdup.bed`
- `CTCF_Control_200K_filterdup.bed`
- `CTCF_ChIP_200K_filterdup.pileup.bdg`
- `d_bg.bdg`
- `1k_bg_norm.bdg`
- `10k_bg_norm.bdg`

## Tools
- MACS3
- macs3 filterdup
- macs3 predictd
- macs3 pileup
- macs3 bdgcmp
- macs3 bdgopt
- macs3 bdgpeakcall

## Skills
- chip-seq-peak-calling-workflow
- bedgraph-file-format-manipulation
- fragment-length-prediction-and-extension
- local-background-bias-estimation
- poisson-test-statistical-scoring
- duplicate-read-filtering-and-normalization
- macs3-subcommand-chaining

## Workflow Description
1. Filter duplicate reads from CTCF ChIP and control BED files using macs3 filterdup with --keep-dup=1, recording the final read counts for each sample. 2. Predict fragment length d from the filtered ChIP sample using macs3 predictd with -g hs and -m 5 50 parameters. 3. Generate ChIP pileup BEDGRAPH by extending filtered ChIP reads to the predicted fragment length d using macs3 pileup with --extsize parameter. 4. Build local bias track from control by creating d, slocal (1kb), and llocal (10kb) background BEDGRAPH files using macs3 pileup with -B option and different --extsize values, then normalize slocal and llocal backgrounds using macs3 bdgopt with multiply mode and d/slocal and d/llocal scaling factors. 5. Combine background tracks by computing maximum bias across d, slocal, and llocal using sequential macs3 bdgcmp -m max operations, then add genome-wide background value using macs3 bdgopt. 6. Scale local lambda bias to ChIP sequencing depth using macs3 bdgopt multiply with the ratio of final ChIP to control read counts. 7. Compare ChIP pileup against scaled local lambda using macs3 bdgcmp with -m qpois or -m ppois to generate q-value or p-value score BEDGRAPH files. 8. Call narrow peaks from score BEDGRAPH using macs3 bdgpeakcall with cutoff value (e.g., -c 1.301 for q-value 0.05), minimum peak length -l set to fragment length d, and gap parameter -g set to read length.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/callvar_algorithm.jpeg` | figure | False |
| `figures/pileup.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history is available for the MACS3 project or this specific tutorial.

## Domain Knowledge
- Fragment length d represents the actual DNA fragment size bound by the protein and must be estimated from short sequencing reads to accurately locate binding sites; this is predicted using autocorrelation on ChIP data alone.
- Local bias calculation requires computing background noise from multiple window sizes (d, slocal=1kb, llocal=10kb) and the genome-wide background, then taking the maximum at each genomic position to account for local sequencing artifacts and control biases.
- Read depth normalization between ChIP and control samples (scaling down the larger sample to match the smaller) is essential to prevent inflation of small signal values and preserve specificity in differential comparisons.
- Score tracks produced by bdgcmp are in -log10 format; a q-value cutoff of 0.05 corresponds to a score of approximately 1.301, and users must select appropriate thresholds based on sensitivity/specificity trade-offs.
- Peak merging after calling requires knowledge of read length to determine the maximum gap between nearby high-scoring regions that should be joined, reflecting the resolution of the underlying sequencing data.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: macs3 filterdup, macs3 predictd, macs3 pileup, macs3 bdgcmp, macs3 bdgopt, macs3 bdgpeakcall, CTCF_ChIP_200K_filterdup.pileup.bdg (ChIP sample pileup track in BEDGRAPH format with fragment-extended coverage signals), local_lambda.bdg (local lambda bias track in BEDGRAPH format scaled to ChIP sequencing depth for statistical comparison), CTCF_ChIP_200K_qvalue.bdg or CTCF_ChIP_200K_pvalue.bdg (score track in BEDGRAPH format with -log10(q-values) or -log10(p-values) from local Poisson test).

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [methods] How does the MACS3 callpeak pipeline decompose into individual subcommands (filterdup, predictd, pileup, bdgcmp, bdgopt, bdgpeakcall) that progressively transform ChIP-Seq data into peak calls?: 'MACS3 does offer a range of subcommands that allow you to customize every step of your analysis'
- `ev_002` from `agent2_synthesis` (agent2_traced): [methods] The MACS3 callpeak pipeline operates through sequential subcommands: filterdup removes duplicate reads, predictd estimates fragment length d from ChIP data, pileup generates coverage tracks, bdgcmp compares ChIP and control signals to compute p/q-value scores, bdgopt applies optimization to score tracks, and bdgpeakcall identifies peaks by filtering regions above a score cutoff.: 'we'll explain how you can accomplish this using the `filterdup` subcommand...This can also be accomplished using the `predictd` subcommand...generate a pileup track for the ChIP sample using the'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] CTCF_ChIP_200K.bed.gz (gzipped BED file with ChIP-Seq reads): 'We'll use two test files, `CTCF_ChIP_200K.bed.gz` and `CTCF_Control_200K.bed.gz`, which you can find in the MACS3 GitHub repository in the `test` directory'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] CTCF_Control_200K.bed.gz (gzipped BED file with control reads): 'We'll use two test files, `CTCF_ChIP_200K.bed.gz` and `CTCF_Control_200K.bed.gz`, which you can find in the MACS3 GitHub repository in the `test` directory'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] CTCF_ChIP_200K_filterdup.pileup.bdg (ChIP sample pileup track in BEDGRAPH format with fragment-extended coverage signals): 'This command produces a file in BEDGRAPH format, `CTCF_ChIP_200K_filterdup.pileup.bdg`, which contains the fragment pileup signals for the ChIP sample'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] local_lambda.bdg (local lambda bias track in BEDGRAPH format scaled to ChIP sequencing depth for statistical comparison): 'The output file is named `local_lambda.bdg`, as it contains values that represent the lambda (or expected value), which can be compared with ChIP signals using the local Poisson test'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] CTCF_ChIP_200K_qvalue.bdg or CTCF_ChIP_200K_pvalue.bdg (score track in BEDGRAPH format with -log10(q-values) or -log10(p-values) from local Poisson test): 'The `CTCF_ChIP_200K_pvalue.bdg` or `CTCF_ChIP_200K_qvalue.bdg` file contains the `-log10(p-values)` or `-log10(q-values)` for each base pair, derived through a local Poisson test'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] CTCF_ChIP_200K_peaks.bed (narrowPeak format BED file with called peak coordinates and summit locations): 'The output is essentially a narrowPeak format file (a type of BED file), which includes the locations of peaks with the summit location noted in the last column'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] macs3 filterdup: 'we'll explain how you can accomplish this using the `filterdup` subcommand'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] macs3 predictd: 'This can also be accomplished using the `predictd` subcommand, which we need to apply only to ChIP data'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] macs3 pileup: 'generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] macs3 bdgcmp: 'using the `bdgcmp` module, which outputs a score for each base pair in the genome'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] macs3 bdgopt: 'apply the `bdgopt` subcommand'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] macs3 bdgpeakcall: 'identify regions that surpass a specific score cutoff using the `bdgpeakcall` function for narrow peak calling'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history is available for the MACS3 project or this specific tutorial.: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file CTCF_ChIP_200K.bed.gz exists in github:macs3-project__MACS/test directory
- verify file CTCF_Control_200K.bed.gz exists in github:macs3-project__MACS/test directory
- script_runs: macs3 filterdup on CTCF_ChIP_200K.bed.gz and CTCF_Control_200K.bed.gz without error
- script_runs: macs3 predictd on filtered ChIP file without error
- script_runs: macs3 pileup on filtered ChIP file with fragment length parameter without error
- file_exists: pileup BEDGRAPH output file with format .bdg
- script_runs: macs3 bdgcmp comparing pileup BEDGRAPH and control lambda track without error
- file_exists: local_lambda.bdg file in output directory
- file_exists: p-value or q-value score BEDGRAPH file in output directory
- script_runs: macs3 bdgopt on score BEDGRAPH without error
- script_runs: macs3 bdgpeakcall on optimized score track without error
- file_format_is: all output BEDGRAPH files conform to BEDGRAPH specification (chromosome, start, end, value columns)
- row_count_equals: pileup BEDGRAPH is non-empty (at least one data row beyond header)

### Expert Review
- pileup BEDGRAPH coverage values are realistic for ChIP-Seq signal (positive, reasonable magnitude relative to sequencing depth)
- local_lambda.bdg background estimates are appropriate and smaller than or comparable to ChIP pileup signal in non-peak regions
- p/q-value score BEDGRAPH shows expected statistical enrichment pattern (higher scores at true peak regions, lower in background)
- peak calls from bdgpeakcall output align with known or expected CTCF binding sites based on CTCF tutorial dataset documentation

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Filter duplicate reads from ChIP and control samples to remove redundant reads at identical genomic locations, recording final read counts for normalization.
2. Predict the fragment length parameter d from filtered ChIP data using autocorrelation-based fragment length estimation.
3. Generate ChIP pileup BEDGRAPH by extending reads in the 5′→3′ direction to the predicted fragment length.
4. Build multi-scale local background bias tracks from control by computing pileup signals at d, slocal (1 kb), and llocal (10 kb) window sizes, then normalizing by the ratio d/window_size.
5. Combine background tracks by iteratively computing maximum values across all scales and the genome-wide background count.
6. Scale the combined local lambda bias track to match the ChIP sample sequencing depth using the ratio of final read counts.
7. Apply local Poisson test by comparing ChIP pileup against scaled local lambda to generate -log10(q-value) or -log10(p-value) score tracks.
8. Validation: Call narrow peaks using bdgpeakcall with user-specified cutoff (e.g., 1.301 for q≤0.05), minimum peak length equal to fragment length d, and gap parameter set to read length; verify output is in narrowPeak BED format with summit locations.

## Workflow Ports

**Inputs:**

- `chip_bed_input` — CTCF ChIP sample reads in BED format ← `task_001/narrowpeak`
- `control_bed_input` — CTCF control sample reads in BED format

**Outputs:**

- `chip_pileup_bdg` — ChIP pileup track in BEDGRAPH format
- `local_lambda_bdg` — Local lambda bias track scaled to sequencing depth
- `qvalue_score_bdg` — Q-value score track in BEDGRAPH format
- `narrowpeak_bed` — Called peaks in narrowPeak BED format

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:macs3-project__MACS`
- **Synthesized at:** 2026-06-15T17:57:06+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: false
- Groundedness failures (2):
  - finding: evidence_span not found in section 'methods' (value='The MACS3 callpeak pipeline operates through sequential subc', span='we'll explain how you can accomplish this using the `filterd') — The finding makes specific claims about what each subcommand does (e.g., 'filterdup removes duplicate reads', 'predictd estimates fragment length d', 'pileup generates coverage tracks') but the evidence_span only shows fragments mentioning individual subcommands without explaining their sequential decomposition or individual functions.
  - research_question: The evidence_span ('MACS3 does offer a range of subcommands that allow you to customize every step of your analysis') is generic and does not specifically address how the six named subcommands progressively transform ChIP-Seq data into peak calls. The evidence does not match the specificity of the research question.
- Notes: This card demonstrates a significant disconnect between the specificity and detail of the research question/finding and the evidence available to support them. The research_question asks for a detailed explanation of how six subcommands 'progressively transform' data, but the evidence provided is generic ('offer a range of subcommands'). The finding makes six functional claims (one per subcommand) but only three subcommands are mentioned in the evidence_span, and their functions are not explicitly described. The workflow_description contains substantially more detail and specificity than is grounded in the cited evidence. The card would benefit from: (1) providing evidence_spans that explicitly describe each subcommand's function and their sequential order, (2) revising the research_question to match the scope of available evidence, or (3) identifying additional source text that justifies the detailed finding. The rest of the card (inputs, outputs, tools, evaluation_strategy) is well-grounded and detailed, suggesting the source material does contain this information but it was not properly cited for the research_question and finding.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
