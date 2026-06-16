# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Does applying C++ salmon 1.12.0's chain score thresholds (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9) to the Rust salmon port on ERR188044 reduce the mapping count gap and confirm that ~80% of the discrepancy is attributable to the orphan/post-merge pruning default difference?: '~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh ='

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] C++ salmon uses orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9 for chain pruning before alignment, accounting for approximately 80% (~49k reads) of the observed mapping count gap between C++ 1.12.0 and the Rust port.: '~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh ='

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GEUVADIS ERR188044 paired-end RNA-seq reads (76 bp, 36.35M reads): 'Reads: GEUVADIS `ERR188044` (36.35M 76bp PE); default selective alignment'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Byte-identical salmon index built from clean.fa (GRCh38 cDNA, 193,759 transcripts, deterministic N-replacement): 'a **byte-identical** index — both tools' indices built from the same `clean.fa` (deterministic non-ACGT replacement, identical 193,759-transcript set)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] C++ salmon 1.12.0 reference mapping statistics (92.011%, 33,446,029 mapped reads, per-read agreement 99.83%): 'C++ 1.12.0 mapped | 33,446,029 (92.011%); per-read mapping agreement | **99.83%**'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Salmon quantification output directory (quant.sf, aux_info/, lib_format_counts.json) for ERR188044 with orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9: 'salmon quant … -o/--output'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mapping statistics summary table: total mapped reads, mapping rate (%), per-read agreement with C++ 1.12.0, Rust-only and C++-only read counts, NumReads and TPM Pearson correlations: 'C++ 1.12.0 mapped | 33,446,029 (92.011%); per-read mapping agreement | **99.83%**; `NumReads` Pearson | **0.99854**; `TPM` Pearson | **0.99897**'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Classification of residual boundary-case reads (Rust-only, C++-only) by minimap2 full Smith-Waterman alignment quality (strong/weak/unaligned): 'minimap2 (full SW) on these reads gives near-identical quality profiles in **both** directions — Rust-only: 69.7% strong / 29.4% weak / 0.9% unaligned; C++-only: 72.0% strong / 26.4% weak / 1.6%'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] salmon 2.0: 'salmon 2.0 (Rust): a user-facing summary of removed/ignored/new options lives in MIGRATION.md'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] salmon 1.12.0: 'C++ 1.12.0 mapped | 33,446,029 (92.011%)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] minimap2: 'minimap2 (full SW) on these reads gives near-identical quality profiles in both directions'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] piscem-rs: 'The Rust port (built on piscem-rs, which derives orientation correctly) was right all along'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact mapping counts (total mapped reads and percentage) for salmon 1.12.0 C++ on ERR188044 with default thresholds (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9) are not explicitly stated in the discussion section; only the reference to '~80% of ~62k reads' is given indirectly.: '~80% (~49k reads) of the gap is attributable to the orphan/post-merge pruning default difference'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The specific numerical value of per-transcript Pearson correlation between Rust 2.0 and C++ 1.12.0 on ERR188044 is stated as 'approximately 0.999' but no confidence interval, p-value, or sample size (number of transcripts) is provided.: 'selective-alignment quantification reproduces C++ salmon to per-transcript Pearson ≈ 0.999'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The residual ~20% of the mapping gap (after accounting for ~49k reads from pruning threshold differences) is attributed to 'benign symmetric tie-breaks' but no quantitative breakdown, examples of tie-break scenarios, or mechanism description is provided.: 'the entire mapping-rate delta is explained by (1) one describable orphan/post-merge pruning default that is off-by-default in Rust, and (2) benign symmetric tie-breaks'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The discussion claims 'nothing indicates a score-threshold or correctness bug' but does not provide the computational procedure (exact comparison protocol, byte-alignment rules, floating-point tolerance, etc.) used to reach that conclusion.: 'Nothing indicates a score-threshold or correctness bug in either implementation.'
