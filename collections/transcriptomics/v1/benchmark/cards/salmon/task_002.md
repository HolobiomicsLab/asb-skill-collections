# SciTask Card: Reproduce mapping-rate parity between Rust salmon port and C++ salmon after pufferfish orientation fix on ERR458493

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T18:27:16.217915+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_salmon/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `benchmark-evaluation`, `data-analysis`, `information-extraction`
- DOI: `10.1038/nmeth.4197`
- GitHub: `COMBINE-lab/salmon`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `transcriptomics`
- Subdomains: `rna-seq`, `differential-expression`
- Techniques: `quantitative-structure-activity`, `statistical-analysis`

## Research Question
Does the Rust port of salmon achieve equivalent mapping rates and correlation metrics to C++ salmon 1.11.4 after the pufferfish SSHash streaming orientation bug is fixed?

## Connected Finding
After the pufferfish SSHash streaming orientation bug fix, C++ salmon achieved 85.55% mapping rate, matching the Rust port to within 1 read, and NumReads Pearson correlation between C++ and Rust reached 0.99854 on byte-identical index.

## Task Description
Reproduce the mapping-rate and correlation metrics reported for yeast ERR458493 (single-end 51 bp reads, Ensembl R64-1-1 cDNA reference) using C++ salmon 1.11.4 before and after the SSHash k-mer-orientation fix, and the Rust salmon port, verifying the reported parity: C++ pre-fix 83.48%, post-fix 85.55%, Rust 85.55%, NumReads Pearson ≈0.99, EffectiveLength Pearson 0.9996.

## Inputs
- ERR458493 single-end 51 bp reads (1,093,957 reads) from ENA
- Ensembl R64-1-1 cDNA reference (6,612 transcripts)
- C++ salmon 1.11.4 (pre-fix) source code or binary
- pufferfish commit 5dce7f4 (SSHash orientation fix patch)
- Rust salmon port source code or binary

## Expected Outputs
- Mapping rate (percentage of reads mapped) from C++ salmon 1.11.4 pre-fix: 83.48% (913,271 reads)
- Mapping rate from C++ salmon 1.11.4 post-fix: 85.55% (935,851 reads)
- Mapping rate from Rust salmon port: 85.55% (935,850 reads)
- NumReads Pearson correlation between C++ post-fix and Rust (confidently mapped): ≥0.99
- EffectiveLength Pearson correlation between C++ post-fix and Rust: 0.9996
- Summary table with mapping rates, read counts, and Pearson correlations for all three runs

## Expected Output File

- `yeast_err458493_mapping_parity_report.csv`

## Landmark Outputs

- `cpp_salmon_1.11.4_prefix.quant.sf`
- `cpp_salmon_1.11.4_postfix.quant.sf`
- `rust_salmon_port.quant.sf`
- `cpp_prefix_mappings.sam`
- `cpp_postfix_mappings.sam`
- `rust_mappings.sam`

## Tools
- salmon 2.0
- salmon 1.11.4 (C++ version, pre-fix)
- salmon (Rust port)
- pufferfish
- piscem-rs
- minimap2

## Skills
- read-mapping-rate-calculation
- rna-seq-quantification-validation
- k-mer-orientation-bug-diagnosis
- selective-alignment-parameter-tuning
- pearson-correlation-computation-across-tools
- sam-bam-mapping-record-inspection

## Workflow Description
1. Download ERR458493 single-end reads (1,093,957 × 51 bp) from ENA and Ensembl R64-1-1 cDNA reference (6,612 transcripts). 2. Build salmon index using the reference with salmon index command (default k-mer length, single-threaded or default threads). 3. Quantify reads with C++ salmon 1.11.4 using salmon quant in selective-alignment mode with -l U (unstranded), no bias correction, writing mappings with -z flag. 4. Repeat step 3 after applying pufferfish commit 5dce7f4 (SSHash streaming orientation fix) to C++ salmon. 5. Quantify the same reads using the Rust salmon port with identical parameters. 6. Extract mapping rates (percentage of reads mapped) from each run's output. 7. Compute NumReads and EffectiveLength Pearson correlation coefficients between C++ post-fix and Rust outputs using quant.sf files. 8. Cross-check placement of reads identified as differentially mapped (e.g., ERR458493.850) using writeMappings SAM output to confirm strand and locus agreement.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| sra_run | `ERR458493` | https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493 | tion correctly) was right all along.  ## Dataset  - Reads: `ERR458493` (Gierliński/Schurch *S. cerevisiae* benchmark),   1,093,95 |
| sra_run | `ERR188044` | https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044 | set), so the only variable is the mapper. Reads: GEUVADIS `ERR188044` (36.35M 76bp PE); default selective alignment, `-l A`, no |

## Missing Information
- Exact pufferfish commit hash or version tag and the specific nature of the SSHash streaming-orientation bug fix are not fully documented in the discussion section
- The exact command-line flags and parameter settings used for each salmon run (1.11.4, 1.12.0, Rust 2.0.0) are not provided, making reproducibility dependent on defaults
- Statistical significance of the Pearson 0.999 correlation and whether confidence intervals or p-values were computed are not reported
- Whether the byte-identical index refers to a single shared index file or independently built indices that happen to be identical, and the k-mer length used, are not explicitly stated
- The exact definition of 'mapping rate' (percentage of reads with at least one alignment? percentage with alignment passing score threshold? including secondary alignments?) is not provided

## Domain Knowledge
- The SSHash k-mer-lookup streaming overload incorrectly applied canonical-relative orientation correction to query-relative lookups, flipping hitFW for non-canonical k-mers; this caused reads with a single non-canonical seed to be mis-placed on the reverse strand at the wrong locus and subsequently discarded below alignment-score threshold.
- Single-end reads with exactly one error-free k-mer seed near an end are most vulnerable to the orientation bug because they lack multiple correctly-oriented seeds to dominate chain selection; multi-seed reads are masked by correct-orientation seeds winning at chain merging.
- Mapping-rate parity validation requires per-read strand and locus agreement checked via writeMappings SAM output; aggregate count agreement alone can mask orientation errors if reads are shuffled across transcripts of similar length.
- The Rust port's loss-less ref-distance early-break chaining heuristic differs from C++ salmon's 0.75 preMergeChainSubThresh pre-alignment pruning; this accounts for the ~20% residual symmetric tie-breaking disagreement on marginal reads after threshold alignment.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: salmon 1.11.4 (C++ version, pre-fix), pufferfish, piscem-rs, minimap2, Mapping rate (percentage of reads mapped) from C++ salmon 1.11.4 pre-fix: 83.48% (913,271 reads), Mapping rate from C++ salmon 1.11.4 post-fix: 85.55% (935,851 reads), Mapping rate from Rust salmon port: 85.55% (935,850 reads), NumReads Pearson correlation between C++ post-fix and Rust (confidently mapped): ≥0.99, EffectiveLength Pearson correlation between C++ post-fix and Rust: 0.9996, Summary table with mapping rates, read counts, and Pearson correlations for all three runs.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [methods] Does the Rust port of salmon achieve equivalent mapping rates and correlation metrics to C++ salmon 1.11.4 after the pufferfish SSHash streaming orientation bug is fixed?: 'After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read'
- `ev_002` from `agent2_synthesis` (agent2_traced): [methods] After the pufferfish SSHash streaming orientation bug fix, C++ salmon achieved 85.55% mapping rate, matching the Rust port to within 1 read, and NumReads Pearson correlation between C++ and Rust reached 0.99854 on byte-identical index.: 'After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] ERR458493 single-end 51 bp reads (1,093,957 reads) from ENA: 'Reads: `ERR458493` (Gierliński/Schurch *S. cerevisiae* benchmark), 1,093,957 single-end 51 bp reads.'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Ensembl R64-1-1 cDNA reference (6,612 transcripts): 'Reference: Ensembl R64-1-1 cDNA, 6,612 transcripts.'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] C++ salmon 1.11.4 (pre-fix) source code or binary: 'C++ salmon 1.11.4 vs. this Rust port, both selective-alignment mode'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] pufferfish commit 5dce7f4 (SSHash orientation fix patch): 'pufferfish `5dce7f4` (branch `codex/for-salmon`): in the streaming overload'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Rust salmon port source code or binary: 'Rust port, both selective-alignment mode, `-l U`, no bias correction.'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Mapping rate (percentage of reads mapped) from C++ salmon 1.11.4 pre-fix: 83.48% (913,271 reads): 'C++ salmon mapping rate (1.11.4, before fix) | 83.48% (913,271 reads)'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Mapping rate from C++ salmon 1.11.4 post-fix: 85.55% (935,851 reads): 'C++ salmon mapping rate (after pufferfish fix) | **85.55% (935,851 reads)**'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Mapping rate from Rust salmon port: 85.55% (935,850 reads): 'Rust port mapping rate | 85.55% (935,850 reads)'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] NumReads Pearson correlation between C++ post-fix and Rust (confidently mapped): ≥0.99: '`NumReads` Pearson (rust vs salmon, confidently mapped) | 0.9989'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] EffectiveLength Pearson correlation between C++ post-fix and Rust: 0.9996: '`EffectiveLength` Pearson | 0.9996'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] Summary table with mapping rates, read counts, and Pearson correlations for all three runs: '| C++ salmon mapping rate (1.11.4, before fix) | 83.48% (913,271 reads) | ... | C++ salmon mapping rate (after pufferfish fix) | **85.55% (935,851 reads)** |'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] salmon 1.11.4 (C++ version, pre-fix): 'C++ salmon 1.11.4 vs. this Rust port, both selective-alignment mode'
- `ev_015` from `agent2_synthesis` (agent2_traced): [methods] salmon (Rust port): 'Rust port, both selective-alignment mode, `-l U`, no bias correction.'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] pufferfish: 'pufferfish's SSHash k-mer lookup, now fixed upstream'
- `ev_017` from `agent2_synthesis` (agent2_traced): [methods] piscem-rs: 'The Rust port (built on piscem-rs, which derives orientation correctly)'
- `ev_018` from `agent2_synthesis` (agent2_traced): [methods] minimap2: 'minimap2 (full SW) on these reads gives near-identical quality profiles in both directions'
- `ev_019` from `agent2_synthesis` (agent2_traced): [discussion] Exact pufferfish commit hash or version tag and the specific nature of the SSHash streaming-orientation bug fix are not fully documented in the discussion section: 'pufferfish's SSHash streaming lookup'
- `ev_020` from `agent2_synthesis` (agent2_traced): [discussion] The exact command-line flags and parameter settings used for each salmon run (1.11.4, 1.12.0, Rust 2.0.0) are not provided, making reproducibility dependent on defaults: 'selective-alignment quantification reproduces C++ salmon to per-transcript Pearson ≈ 0.999'
- `ev_021` from `agent2_synthesis` (agent2_traced): [discussion] Statistical significance of the Pearson 0.999 correlation and whether confidence intervals or p-values were computed are not reported: 'SA quantification agrees at Pearson 0.999'
- `ev_022` from `agent2_synthesis` (agent2_traced): [discussion] Whether the byte-identical index refers to a single shared index file or independently built indices that happen to be identical, and the k-mer length used, are not explicitly stated: 'byte-identical index'
- `ev_023` from `agent2_synthesis` (agent2_traced): [discussion] The exact definition of 'mapping rate' (percentage of reads with at least one alignment? percentage with alignment passing score threshold? including secondary alignments?) is not provided: 'index construction is faster, and peak memory is lower'

## Evaluation Strategy
### Direct Checks
- File exists: yeast ERR458493 dataset (SRA accession ERR458493) retrievable from ENA or SRA
- File exists: Ensembl R64-1-1 S. cerevisiae cDNA reference (6,612 transcripts) retrievable from Ensembl FTP or GitHub release artifact
- Script runs: salmon 1.11.4 (C++ pre-fix version) executable or container image obtainable from COMBINE-lab/salmon cpp branch or conda salmon-cpp package
- Script runs: salmon 1.12.0 (C++ post-fix version) executable or container image obtainable from COMBINE-lab/salmon cpp branch or conda salmon-cpp package
- Script runs: salmon 2.0.0 (Rust port) executable obtainable from GitHub release, cargo, or conda
- Script runs: pufferfish commit 5dce7f4 (with SSHash orientation fix) retrievable and compilable or pinned in salmon 1.12.0
- File exists: salmon index built from Ensembl R64-1-1 cDNA using salmon 1.11.4 (C++ pre-fix), salmon 1.12.0 (C++ post-fix), and salmon 2.0.0 (Rust)
- File exists: salmon quant output (quant.sf) for ERR458493 using each of the three configurations above
- Value in range: C++ salmon 1.11.4 (pre-fix) mapping rate on ERR458493 equals 83.48% (byte-for-byte or within ±0.01 percentage points)
- Value in range: C++ salmon 1.12.0 (post-fix) mapping rate on ERR458493 equals 85.55% (byte-for-byte or within ±0.01 percentage points)
- Value in range: salmon 2.0.0 (Rust) mapping rate on ERR458493 equals 85.55% (byte-for-byte or within ±0.01 percentage points)
- Value in range: NumReads Pearson correlation between C++ 1.12.0 and Rust 2.0.0 quant.sf output ≈ 0.99 (robust to rounding; acceptable range 0.985–0.995)
- Value in range: EffectiveLength Pearson correlation between C++ 1.12.0 and Rust 2.0.0 quant.sf output equals 0.9996 (robust to minor floating-point precision differences; acceptable range 0.999–1.0)
- Output matches reference: byte-identical index (same k-length, same transcripts, same reference) used across all three quantifications to control for index format differences

### Expert Review
- Verify that the ~2% improvement from C++ 1.11.4 to 1.12.0 (83.48% → 85.55%) is causally attributable to the pufferfish SSHash streaming-orientation bug fix (commit 5dce7f4) and not to other changes in salmon 1.11.4 → 1.12.0; cross-check pufferfish changelog and salmon 1.12.0 release notes for confounding fixes
- Verify that the Rust port mapping rate (85.55%) matches C++ post-fix (85.55%) within 1 read as claimed; inspect raw SAM/PAF alignment outputs and count total mapped reads for both to confirm 'within 1 read' statement is accurate
- Verify that the 62,812 reads mapped by Rust but not C++, and the 154 reads mapped by C++ but not Rust, are reproducible and that the documented chain-sub-optimality threshold difference (orphanChainSubThresh = 0.95 in C++, default off in Rust) and benign tie-breaks account for ~80% of this asymmetry as claimed
- Confirm that no score-threshold bug or correctness bug is present in either implementation by spot-checking a random sample of the 62,812 Rust-only and 154 C++-only alignments for alignment correctness, score consistency, and tie-break handling

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Acquire ERR458493 single-end reads and Ensembl R64-1-1 cDNA reference.
2. Build salmon index from reference using default parameters.
3. Quantify reads with C++ salmon 1.11.4 (pre-fix) in selective-alignment mode (-l U, no bias, writeMappings enabled), extract mapping rate and quant.sf abundance table.
4. Apply pufferfish commit 5dce7f4 (SSHash streaming orientation correction) and re-quantify with identical parameters; compare mapping rate and quant.sf to pre-fix run.
5. Quantify reads using Rust salmon port with identical parameters; extract mapping rate and quant.sf.
6. Compute NumReads and EffectiveLength Pearson correlations between C++ post-fix and Rust outputs.
7. Cross-validate strand and locus placement of discordant reads (e.g., ERR458493.850) using SAM writeMappings output to confirm orientation fix causation.
8. Validation: C++ pre-fix mapping rate = 83.48% ± 1 read, C++ post-fix = 85.55% ± 1 read matching Rust, NumReads Pearson ≥ 0.998, EffectiveLength Pearson ≥ 0.999.
9. References: source article (DOI: 10.1038/nmeth.4197); ERR458493 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493); ERR188044 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044)

## Workflow Ports

**Inputs:**

- `reads_err458493` — ERR458493 single-end 51 bp reads (1,093,957 reads) ← `task_001/numreads_pearson`
- `reference_ensembl_r64` — Ensembl R64-1-1 cDNA reference (6,612 transcripts)
- `cpp_salmon_prefix` — C++ salmon 1.11.4 pre-fix binary or source
- `pufferfish_fix_5dce7f4` — pufferfish commit 5dce7f4 patch or diff
- `rust_salmon_port` — Rust salmon port binary or source

**Outputs:**

- `mapping_rate_cpp_prefix` — C++ salmon 1.11.4 pre-fix mapping rate and read count
- `mapping_rate_cpp_postfix` — C++ salmon 1.11.4 post-fix mapping rate and read count
- `mapping_rate_rust` — Rust salmon port mapping rate and read count
- `pearson_numreads` — NumReads Pearson correlation (C++ post-fix vs. Rust)
- `pearson_effectivelength` — EffectiveLength Pearson correlation (C++ post-fix vs. Rust)
- `summary_metrics_table` — Consolidated table with all mapping rates, counts, and Pearson correlations

**Used:** `urn:asb:port:task_001/numreads_pearson`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:COMBINE-lab__salmon`
- **Synthesized at:** 2026-06-15T18:38:25+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
