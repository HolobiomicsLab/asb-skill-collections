# SciTask Card: Reproduce per-transcript quantification agreement between Rust salmon 2.0 and C++ salmon 1.12.0 on ERR188044

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T18:27:16.217915+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_transcriptomics/coll_salmon/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `benchmark-evaluation`, `statistical-analysis`, `data-analysis`
- DOI: `10.1038/nmeth.4197`
- GitHub: `COMBINE-lab/salmon`

## Classification

- Task kind: `reproduction`
- Article type: `research-article`
- Primary domain: `transcriptomics`
- Subdomains: `rna-seq`, `differential-expression`
- Techniques: `quantitative-structure-activity`, `statistical-analysis`

## Research Question
How closely do the quantification results (NumReads and TPM) from salmon 2.0 (Rust rewrite) agree with salmon 1.12.0 (C++ version) when run in selective-alignment mode on the same dataset and index?

## Connected Finding
On a byte-identical index, salmon 2.0 (Rust) and salmon 1.12.0 (C++) achieve per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM, with per-read mapping agreement at 99.83%.

## Task Description
Run salmon 2.0 (Rust) and C++ salmon 1.12.0 in selective-alignment mode on GEUVADIS ERR188044 paired-end reads against a byte-identical GRCh38 cDNA index, then compute per-transcript Pearson correlations (NumReads and TPM), total NumReads difference, and per-read mapping agreement to reproduce reported parity metrics.

## Inputs
- GEUVADIS ERR188044 paired-end reads (36.35M reads, 76 bp)
- GRCh38 cDNA reference (193,759 transcripts after deterministic N-replacement and cleaning)
- salmon 2.0 (Rust implementation)
- C++ salmon 1.12.0

## Expected Outputs
- NumReads Pearson correlation coefficient between salmon 2.0 and C++ 1.12.0 (target: 0.99854)
- TPM Pearson correlation coefficient between salmon 2.0 and C++ 1.12.0 (target: 0.99897)
- Total assigned NumReads difference as percentage (target: −0.19%)
- Per-read mapping agreement percentage (target: 99.83%)
- Comparison table with salmon 2.0 and C++ 1.12.0 metrics and per-read disagreement details

## Expected Output File

- `parity_metrics.csv`

## Landmark Outputs

- `salmon_2_0_index/`
- `salmon_1_12_0_index/`
- `salmon_2_0_quant/quant.sf`
- `salmon_1_12_0_quant/quant.sf`
- `correlation_analysis.csv`
- `per_read_agreement.txt`

## Tools
- salmon 2.0
- salmon 1.12.0
- piscem-rs

## Skills
- rna-seq-quantification-selective-alignment
- transcript-abundance-correlation-analysis
- mapping-agreement-cross-tool-validation
- selective-alignment-parameter-tuning
- paired-end-read-quantification
- index-construction-determinism

## Workflow Description
1. Build a byte-identical GRCh38 cDNA index using both salmon 2.0 and C++ salmon 1.12.0 from the same cleaned FASTA with deterministic non-ACGT replacement (193,759 transcripts). 2. Run salmon 2.0 quant in selective-alignment mode on ERR188044 (36.35M 76 bp PE reads) with `-l A` (auto-detect library type), no bias correction, and default chain-pruning thresholds (orphanChainSubThresh=0.0, postMergeChainSubThresh=0.0). 3. Run C++ salmon 1.12.0 quant in selective-alignment mode on the same reads with `-l A`, no bias correction, and default thresholds (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9). 4. Extract NumReads and TPM columns from quant.sf outputs for both runs. 5. Compute Pearson correlations for NumReads and TPM per transcript across the two tools, and compute total assigned NumReads difference as a percentage. 6. Count per-read mapping agreement by comparing unmapped_names.txt files (fully-unmapped reads only, coded 'u') and report the percentage of reads on which both tools agree.

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
- Exact Pearson correlation values not reported in discussion section; only approximate value '≈ 0.999' stated
- Specific runtime (wall-clock time) and peak memory consumption for salmon 2.0 vs. 1.12.0 on GEUVADIS ERR188044 not provided; only qualitative statements made
- Details on how per-read mapping agreement (99.83%) is computed, including definition of 'agreement' (e.g., same primary transcript, same chain, or same alignment score tier) not specified
- Explanation of what constitutes a 'symmetric tie-break' and how it affects quantification results is referenced but not detailed
- Identity and magnitude of the 'one describable orphan/post-merge pruning default that is off-by-default in Rust' not specified in the discussion section
- Methods section does not provide the exact Pearson correlation coefficients for NumReads (0.99854) and TPM (0.99897) cited in discussion; these appear only in a table not shown in the provided text
- No description of whether 'byte-identical index' refers to exact binary equivalence or semantic equivalence of index contents

## Domain Knowledge
- Selective alignment is the default mode in salmon 2.0 (Rust); it performs k-mer-based pseudoalignment with full Smith-Waterman alignment for candidate chains, unlike pure pseudoalignment or mapping.
- Chain-pruning thresholds (orphanChainSubThresh and postMergeChainSubThresh) differ by design between C++ salmon 1.12.0 (0.95 and 0.9 for speed) and salmon 2.0 Rust default (0.0 to align all candidates), causing ~80% of the ~62.8k per-read disagreement on this dataset.
- Per-read mapping agreement must be computed on fully-unmapped reads only (coded 'u' in unmapped_names.txt), not the entire file, because salmon's unmapped_names.txt includes orphan-halves and decoy reads which are not comparable to the Rust port's u-only output.
- Pearson correlations for NumReads and TPM should reach ≥0.998 on a byte-identical index with selective alignment; lower correlations (<0.99) suggest index differences, not mapping differences.
- The index format changed in salmon 2.0 (Rust rewrite), requiring separate index builds from the same reference; byte-identity is achieved only if the same cleaned FASTA (deterministic non-ACGT handling) and identical parameters (e.g., k-mer length, decoy sequences) are used.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: salmon 2.0, salmon 1.12.0, piscem-rs, NumReads Pearson correlation coefficient between salmon 2.0 and C++ 1.12.0 (target: 0.99854), TPM Pearson correlation coefficient between salmon 2.0 and C++ 1.12.0 (target: 0.99897), Total assigned NumReads difference as percentage (target: −0.19%), Per-read mapping agreement percentage (target: 99.83%), Comparison table with salmon 2.0 and C++ 1.12.0 metrics and per-read disagreement details.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How closely do the quantification results (NumReads and TPM) from salmon 2.0 (Rust rewrite) agree with salmon 1.12.0 (C++ version) when run in selective-alignment mode on the same dataset and index?: 'This is salmon 2.0 — a from-scratch Rust rewrite of salmon. It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read'
- `ev_002` from `agent2_synthesis` (agent2_traced): [methods] On a byte-identical index, salmon 2.0 (Rust) and salmon 1.12.0 (C++) achieve per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM, with per-read mapping agreement at 99.83%.: 'NumReads Pearson | 0.99854'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] GEUVADIS ERR188044 paired-end reads (36.35M reads, 76 bp): 'Reads: GEUVADIS `ERR188044` (36.35M 76bp PE)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] GRCh38 cDNA reference (193,759 transcripts after deterministic N-replacement and cleaning): 'byte-identical index — both tools' indices built from the same `clean.fa` (deterministic non-ACGT replacement, identical 193,759-transcript set)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] salmon 2.0 (Rust implementation): 'Rust port'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] C++ salmon 1.12.0: 'C++ 1.12.0'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] NumReads Pearson correlation coefficient between salmon 2.0 and C++ 1.12.0 (target: 0.99854): '`NumReads` Pearson | **0.99854**'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] TPM Pearson correlation coefficient between salmon 2.0 and C++ 1.12.0 (target: 0.99897): '`TPM` Pearson | **0.99897**'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Total assigned NumReads difference as percentage (target: −0.19%): 'total assigned `NumReads` diff | **−0.19%**'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Per-read mapping agreement percentage (target: 99.83%): 'per-read mapping agreement | **99.83%**'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] Comparison table with salmon 2.0 and C++ 1.12.0 metrics and per-read disagreement details: '| metric | value |'
- `ev_012` from `agent2_synthesis` (agent2_traced): [methods] salmon 2.0: 'Rust port'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] salmon 1.12.0: 'C++ 1.12.0'
- `ev_014` from `agent2_synthesis` (agent2_traced): [methods] piscem-rs: 'The Rust port (built on piscem-rs, which derives orientation correctly)'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] Exact Pearson correlation values not reported in discussion section; only approximate value '≈ 0.999' stated: 'selective-alignment quantification reproduces C++ salmon to per-transcript Pearson ≈ 0.999'
- `ev_016` from `agent2_synthesis` (agent2_traced): [discussion] Specific runtime (wall-clock time) and peak memory consumption for salmon 2.0 vs. 1.12.0 on GEUVADIS ERR188044 not provided; only qualitative statements made: 'index construction is faster, and peak memory is lower'
- `ev_017` from `agent2_synthesis` (agent2_traced): [discussion] Details on how per-read mapping agreement (99.83%) is computed, including definition of 'agreement' (e.g., same primary transcript, same chain, or same alignment score tier) not specified: 'per-read mapping agreement 99.83%'
- `ev_018` from `agent2_synthesis` (agent2_traced): [discussion] Explanation of what constitutes a 'symmetric tie-break' and how it affects quantification results is referenced but not detailed: 'benign symmetric tie-breaks'
- `ev_019` from `agent2_synthesis` (agent2_traced): [discussion] Identity and magnitude of the 'one describable orphan/post-merge pruning default that is off-by-default in Rust' not specified in the discussion section: 'one describable orphan/post-merge pruning default that is off-by-default in Rust'
- `ev_020` from `agent2_synthesis` (agent2_traced): [discussion] Methods section does not provide the exact Pearson correlation coefficients for NumReads (0.99854) and TPM (0.99897) cited in discussion; these appear only in a table not shown in the provided text: 'NumReads Pearson | 0.99854'
- `ev_021` from `agent2_synthesis` (agent2_traced): [discussion] No description of whether 'byte-identical index' refers to exact binary equivalence or semantic equivalence of index contents: 'On a byte-identical index, SA quantification agrees at Pearson 0.999'

## Evaluation Strategy
### Direct Checks
- file_exists: salmon 2.0.0 binary (Rust implementation) available from COMBINE-lab/salmon repository releases or cargo install
- file_exists: salmon 1.12.0 binary (C++ implementation) available from COMBINE-lab/salmon cpp branch or salmon-cpp conda package
- file_exists: GEUVADIS ERR188044 dataset (36.35M 76bp paired-end reads) retrievable from ENA/SRA public repository
- file_exists: GRCh38 cDNA reference index (or source transcriptome FASTA) available for index construction
- script_runs: `salmon index` command (both versions) executes without error on GRCh38 cDNA transcriptome with default k-mer length and parameters
- script_runs: `salmon quant` command (both versions) executes in selective-alignment mode on ERR188044 reads against respective indices without error
- file_exists: quant.sf output files generated by both salmon 2.0 and salmon 1.12.0 from same input reads and reference
- file_format_is: quant.sf output files are tab-delimited text with columns Name, Length, EffectiveLength, TPM, NumReads
- value_in_range: NumReads Pearson correlation (per-transcript) between C++ 1.12.0 and Rust 2.0 output equals 0.99854 ± 0.00020 (byte-identical index), robust to rounding precision in correlation calculation
- value_in_range: TPM Pearson correlation (per-transcript) between C++ 1.12.0 and Rust 2.0 output equals 0.99897 ± 0.00020 (byte-identical index), robust to rounding precision in correlation calculation
- value_in_range: total NumReads difference between C++ 1.12.0 and Rust 2.0 equals −0.19% ± 0.05% of total mapped reads
- value_in_range: per-read mapping agreement between C++ 1.12.0 and Rust 2.0 (proportion of reads assigned to same transcript or both unmapped) equals 0.9983 ± 0.0005
- output_matches_reference: NumReads vector from quant.sf (Rust) and C++ output correlates with reported Pearson 0.99854 when computed using Pearson correlation formula on transcript-level counts
- output_matches_reference: TPM vector from quant.sf (Rust) and C++ output correlates with reported Pearson 0.99897 when computed on transcript-level abundances

### Expert Review
- Verify that the byte-identical index construction (same index format used by both salmon 2.0 and 1.12.0 for fair comparison) is actually achieved: confirm index binaries are identical byte-for-byte or that index format compatibility is explicitly validated before quantification
- Assess whether the reported Pearson correlation thresholds (0.99854, 0.99897) are scientifically appropriate benchmarks for declaring 'agreement' in transcript quantification, or if domain-specific tolerance bounds should be applied
- Evaluate the statistical significance and practical importance of the −0.19% total NumReads difference: determine whether this magnitude of difference is negligible for typical downstream inference (e.g., differential expression analysis)
- Review the breakdown of the ~2% per-read mapping difference attributed to orphan/post-merge pruning defaults and symmetric tie-breaks: confirm the qualitative explanation is sufficient or if deeper audit of edge cases is warranted
- Assess representativeness of benchmarking: confirm whether GEUVADIS ERR188044 (76 bp paired-end) and yeast ERR458493 (51 bp single-end) are sufficient to claim general correctness, or if additional read lengths, library types, or datasets should be tested

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Prepare a cleaned GRCh38 cDNA FASTA with deterministic non-ACGT replacement to ensure byte-identical indices across both salmon versions.
2. Build a selective-alignment index using salmon 2.0 (Rust) with default parameters (k-mer length, threads, no special decoy handling unless documented).
3. Build an identical index using C++ salmon 1.12.0 from the same cleaned FASTA with matching parameters.
4. Quantify ERR188044 paired-end reads (36.35M, 76 bp) using salmon 2.0 in selective-alignment mode with auto-detect library type (-l A), no bias correction, and Rust-default chain-pruning thresholds (orphanChainSubThresh=0.0, postMergeChainSubThresh=0.0).
5. Quantify the same reads using C++ salmon 1.12.0 with identical mapping settings (-l A, no bias) and C++ defaults (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9).
6. Extract NumReads and TPM per transcript from both quant.sf files and compute Pearson correlations; compute total assigned NumReads difference as (Rust total − C++ total) / C++ total × 100%.
7. Compare unmapped_names.txt files from both runs, extracting only fully-unmapped reads (code 'u'), and compute per-read mapping agreement as the fraction of reads on which both tools agree (mapped or unmapped).
8. Validation: Pearson correlations for NumReads and TPM must both exceed 0.998 (reported 0.99854 and 0.99897); per-read mapping agreement must reach ≥99.8% (reported 99.83%); total NumReads difference must stay within ±0.5% (reported −0.19%).
9. References: source article (DOI: 10.1038/nmeth.4197); ERR458493 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR458493); ERR188044 (https://www.ncbi.nlm.nih.gov/sra/?term=ERR188044)

## Workflow Ports

**Inputs:**

- `reads_geuvadis` — GEUVADIS ERR188044 paired-end reads
- `ref_grch38` — GRCh38 cDNA reference (cleaned, 193,759 transcripts)
- `salmon_2_0_bin` — salmon 2.0 (Rust) executable
- `salmon_1_12_0_bin` — C++ salmon 1.12.0 executable

**Outputs:**

- `numreads_pearson` — NumReads Pearson correlation
- `tpm_pearson` — TPM Pearson correlation
- `numreads_diff_pct` — Total assigned NumReads difference (%)
- `mapping_agreement_pct` — Per-read mapping agreement (%)
- `comparison_metrics` — Full parity metrics table

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:COMBINE-lab__salmon`
- **Synthesized at:** 2026-06-15T18:38:25+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
