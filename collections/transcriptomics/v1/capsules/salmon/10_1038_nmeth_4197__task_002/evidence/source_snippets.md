# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Does the Rust port of salmon achieve equivalent mapping rates and correlation metrics to C++ salmon 1.11.4 after the pufferfish SSHash streaming orientation bug is fixed?: 'After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] After the pufferfish SSHash streaming orientation bug fix, C++ salmon achieved 85.55% mapping rate, matching the Rust port to within 1 read, and NumReads Pearson correlation between C++ and Rust reached 0.99854 on byte-identical index.: 'After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ERR458493 single-end 51 bp reads (1,093,957 reads) from ENA: 'Reads: `ERR458493` (Gierliński/Schurch *S. cerevisiae* benchmark), 1,093,957 single-end 51 bp reads.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Ensembl R64-1-1 cDNA reference (6,612 transcripts): 'Reference: Ensembl R64-1-1 cDNA, 6,612 transcripts.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] C++ salmon 1.11.4 (pre-fix) source code or binary: 'C++ salmon 1.11.4 vs. this Rust port, both selective-alignment mode'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] pufferfish commit 5dce7f4 (SSHash orientation fix patch): 'pufferfish `5dce7f4` (branch `codex/for-salmon`): in the streaming overload'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Rust salmon port source code or binary: 'Rust port, both selective-alignment mode, `-l U`, no bias correction.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mapping rate (percentage of reads mapped) from C++ salmon 1.11.4 pre-fix: 83.48% (913,271 reads): 'C++ salmon mapping rate (1.11.4, before fix) | 83.48% (913,271 reads)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mapping rate from C++ salmon 1.11.4 post-fix: 85.55% (935,851 reads): 'C++ salmon mapping rate (after pufferfish fix) | **85.55% (935,851 reads)**'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Mapping rate from Rust salmon port: 85.55% (935,850 reads): 'Rust port mapping rate | 85.55% (935,850 reads)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NumReads Pearson correlation between C++ post-fix and Rust (confidently mapped): ≥0.99: '`NumReads` Pearson (rust vs salmon, confidently mapped) | 0.9989'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] EffectiveLength Pearson correlation between C++ post-fix and Rust: 0.9996: '`EffectiveLength` Pearson | 0.9996'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Summary table with mapping rates, read counts, and Pearson correlations for all three runs: '| C++ salmon mapping rate (1.11.4, before fix) | 83.48% (913,271 reads) | ... | C++ salmon mapping rate (after pufferfish fix) | **85.55% (935,851 reads)** |'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] salmon 1.11.4 (C++ version, pre-fix): 'C++ salmon 1.11.4 vs. this Rust port, both selective-alignment mode'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] salmon (Rust port): 'Rust port, both selective-alignment mode, `-l U`, no bias correction.'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] pufferfish: 'pufferfish's SSHash k-mer lookup, now fixed upstream'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] piscem-rs: 'The Rust port (built on piscem-rs, which derives orientation correctly)'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] minimap2: 'minimap2 (full SW) on these reads gives near-identical quality profiles in both directions'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact pufferfish commit hash or version tag and the specific nature of the SSHash streaming-orientation bug fix are not fully documented in the discussion section: 'pufferfish's SSHash streaming lookup'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The exact command-line flags and parameter settings used for each salmon run (1.11.4, 1.12.0, Rust 2.0.0) are not provided, making reproducibility dependent on defaults: 'selective-alignment quantification reproduces C++ salmon to per-transcript Pearson ≈ 0.999'

## ev_021

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Statistical significance of the Pearson 0.999 correlation and whether confidence intervals or p-values were computed are not reported: 'SA quantification agrees at Pearson 0.999'

## ev_022

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Whether the byte-identical index refers to a single shared index file or independently built indices that happen to be identical, and the k-mer length used, are not explicitly stated: 'byte-identical index'

## ev_023

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The exact definition of 'mapping rate' (percentage of reads with at least one alignment? percentage with alignment passing score threshold? including secondary alignments?) is not provided: 'index construction is faster, and peak memory is lower'
