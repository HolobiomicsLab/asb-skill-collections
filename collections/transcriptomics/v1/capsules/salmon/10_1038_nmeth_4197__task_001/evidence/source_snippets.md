# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How closely do the quantification results (NumReads and TPM) from salmon 2.0 (Rust rewrite) agree with salmon 1.12.0 (C++ version) when run in selective-alignment mode on the same dataset and index?: 'This is salmon 2.0 — a from-scratch Rust rewrite of salmon. It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] On a byte-identical index, salmon 2.0 (Rust) and salmon 1.12.0 (C++) achieve per-transcript Pearson correlations of 0.99854 for NumReads and 0.99897 for TPM, with per-read mapping agreement at 99.83%.: 'NumReads Pearson | 0.99854'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GEUVADIS ERR188044 paired-end reads (36.35M reads, 76 bp): 'Reads: GEUVADIS `ERR188044` (36.35M 76bp PE)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] GRCh38 cDNA reference (193,759 transcripts after deterministic N-replacement and cleaning): 'byte-identical index — both tools' indices built from the same `clean.fa` (deterministic non-ACGT replacement, identical 193,759-transcript set)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] salmon 2.0 (Rust implementation): 'Rust port'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] C++ salmon 1.12.0: 'C++ 1.12.0'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] NumReads Pearson correlation coefficient between salmon 2.0 and C++ 1.12.0 (target: 0.99854): '`NumReads` Pearson | **0.99854**'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] TPM Pearson correlation coefficient between salmon 2.0 and C++ 1.12.0 (target: 0.99897): '`TPM` Pearson | **0.99897**'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Total assigned NumReads difference as percentage (target: −0.19%): 'total assigned `NumReads` diff | **−0.19%**'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Per-read mapping agreement percentage (target: 99.83%): 'per-read mapping agreement | **99.83%**'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Comparison table with salmon 2.0 and C++ 1.12.0 metrics and per-read disagreement details: '| metric | value |'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] salmon 2.0: 'Rust port'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] salmon 1.12.0: 'C++ 1.12.0'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] piscem-rs: 'The Rust port (built on piscem-rs, which derives orientation correctly)'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Exact Pearson correlation values not reported in discussion section; only approximate value '≈ 0.999' stated: 'selective-alignment quantification reproduces C++ salmon to per-transcript Pearson ≈ 0.999'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specific runtime (wall-clock time) and peak memory consumption for salmon 2.0 vs. 1.12.0 on GEUVADIS ERR188044 not provided; only qualitative statements made: 'index construction is faster, and peak memory is lower'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Details on how per-read mapping agreement (99.83%) is computed, including definition of 'agreement' (e.g., same primary transcript, same chain, or same alignment score tier) not specified: 'per-read mapping agreement 99.83%'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Explanation of what constitutes a 'symmetric tie-break' and how it affects quantification results is referenced but not detailed: 'benign symmetric tie-breaks'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Identity and magnitude of the 'one describable orphan/post-merge pruning default that is off-by-default in Rust' not specified in the discussion section: 'one describable orphan/post-merge pruning default that is off-by-default in Rust'

## ev_020

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Methods section does not provide the exact Pearson correlation coefficients for NumReads (0.99854) and TPM (0.99897) cited in discussion; these appear only in a table not shown in the provided text: 'NumReads Pearson | 0.99854'

## ev_021

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No description of whether 'byte-identical index' refers to exact binary equivalence or semantic equivalence of index contents: 'On a byte-identical index, SA quantification agrees at Pearson 0.999'
