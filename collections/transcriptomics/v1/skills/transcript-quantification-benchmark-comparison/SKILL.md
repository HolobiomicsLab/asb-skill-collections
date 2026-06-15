---
name: transcript-quantification-benchmark-comparison
description: Use when you have two implementations of the same quantification method (or major versions) and observe a persistent disagreement in mapped-read counts, per-read alignment agreement, or abundance correlations on the same reference index and read set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3168
  - http://edamontology.org/topic_0622
  tools:
  - minimap2
  - piscem-rs
  - salmon 2.0
  - salmon 1.12.0
  - pufferfish
derived_from:
- doi: 10.1038/nmeth.4197
  title: salmon
evidence_spans:
- minimap2 (full SW) on these reads gives near-identical quality profiles in both directions
- The Rust port (built on piscem-rs, which derives orientation correctly)
- The Rust port (built on piscem-rs, which derives orientation correctly) was right all along
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_salmon
    doi: 10.1038/nmeth.4197
    title: salmon
  dedup_kept_from: coll_salmon
schema_version: 0.2.0
---

# Transcript-quantification benchmark comparison

## Summary

Systematically compare transcript quantification outputs between two implementations (e.g., C++ salmon 1.12.0 vs. Rust salmon 2.0) on byte-identical indices and real reads to isolate the root cause of mapping-rate discrepancies. This skill surfaces algorithm-level differences (e.g., chain-pruning thresholds, k-mer orientation bugs) that account for observed gaps.

## When to use

You have two implementations of the same quantification method (or major versions) and observe a persistent disagreement in mapped-read counts, per-read alignment agreement, or abundance correlations on the same reference index and read set. The gap is large enough to affect downstream conclusions (e.g., >1% mapping-rate difference, residual per-read disagreement >20k reads) and you need to identify whether it stems from algorithm changes, parameter defaults, or implementation bugs rather than random noise.

## When NOT to use

- The two implementations use different index formats or reference sequences — build a shared, canonical index first to ensure comparability.
- Mapping-rate disagreement is <1% and per-read agreement is >99.8% — the implementations are already sufficiently concordant for practical purposes and detailed root-cause analysis is unlikely to reveal actionable algorithm differences.
- One implementation uses fundamentally different quantification inference (e.g., sketch-based k-mer quantification vs. alignment-based selective alignment) — comparison of mapping counts alone will conflate inference-level with alignment-level differences.

## Inputs

- byte-identical salmon index built from canonical reference transcriptome (k=31, deterministic N-replacement)
- paired-end RNA-seq reads (FASTQ or equivalent; e.g., GEUVADIS ERR188044, 36.35M reads, 76 bp)
- two implementations of the same quantification method (e.g., salmon 1.12.0 C++ and salmon 2.0 Rust)

## Outputs

- per-read mapping agreement matrix (fraction of reads assigned identically)
- quantitative comparison of mapped-read counts and NumReads correlation (e.g., Pearson r)
- set of boundary-case reads (mapped by version A but not B, and vice versa)
- classification of boundary reads by full-SW alignment quality (strong/weak/unaligned)
- residual disagreement statistics (count of Rust-only, C++-only, and fully-unmapped reads)
- quantified impact of parameter changes on mapping-rate gap (e.g., ~49k reads / ~80% attributed to orphan-chain defaults)

## How to apply

First, build a byte-identical reference index from a canonical transcriptome FASTA using both implementations to control for index construction differences. Next, quantify a large, well-characterized read set (e.g., GEUVADIS ERR188044, 36.35M paired-end 76 bp reads) with both versions on the byte-identical index using selective alignment and identical user-facing parameters (disable bias correction and other confounders). Extract per-read mapping statistics: total mapped reads, per-read mapping agreement (fraction of reads assigned to the same transcript set), and NumReads correlation. Identify boundary-case reads (mapped by one version but not the other) and re-align them with a reference-free full Smith-Waterman aligner (e.g., minimap2 full-SW) to classify as strong/weak/unaligned and assess symmetry. Finally, selectively apply suspected algorithm parameters from the reference implementation to the test version (e.g., chain-pruning thresholds orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9) and measure the reduction in residual disagreement. The root cause is confirmed when parameter tuning reduces the gap by ≥80% and residual per-read disagreement drops below ~20k reads.

## Related tools

- **salmon 2.0** (test implementation (Rust rewrite) to be benchmarked against reference) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0** (reference C++ implementation for comparison baseline) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **minimap2** (full Smith-Waterman re-aligner to classify boundary-case reads as strong/weak/unaligned)
- **piscem-rs** (underlying mapper in Rust port used to validate orientation and chain-pruning logic)
- **pufferfish** (k-mer lookup index library; bugs (e.g., SSHash orientation) can be identified by comparing k-mer queries between implementations)

## Examples

```
salmon quant -i salmon_index -l A --orphanChainSubThresh 0.95 --postMergeChainSubThresh 0.9 -1 ERR188044_1.fastq.gz -2 ERR188044_2.fastq.gz -p 16 -o quant_with_c_params && diff -u <(cut -f1,3,4 quant_c++_baseline/quant.sf | sort) <(cut -f1,3,4 quant_with_c_params/quant.sf | sort) | head -20
```

## Evaluation signals

- Mapping rate of test version must fall within 0.02% of reference (e.g., ≥92.03% if reference is 92.011%) to confirm byte-identical index compatibility.
- Per-read mapping agreement ≥99.8% before parameter adjustment; indicates algorithmic similarity.
- NumReads Pearson correlation ≥0.998 across all transcripts; validates equivalence-class quantification agreement.
- After applying suspected parameter changes, residual per-read disagreement (Rust-only + C++-only reads) must drop from initial gap (e.g., 62,966) to <20,000 reads, confirming that parameter defaults account for ≥80% of the discrepancy.
- Full-SW re-alignment of boundary-case reads shows symmetric classification (test-only mapped reads are classified as weak/unaligned by Smith-Waterman, mirroring reference-only reads), ruling out one implementation's correctness in favor of an algorithm choice.

## Limitations

- Byte-identical index construction is not guaranteed if implementations use different k-mer encoding, decoy handling, or deterministic random-number initialization; canonical transcriptome FASTA, k-mer length, and build parameters must be strictly matched.
- Full-SW re-alignment of boundary-case reads is computationally expensive and may not fully resolve ambiguous alignments; reads with multiple near-optimal alignments will be classified as weak regardless of true assignment correctness.
- Parameter tuning may improve agreement on one dataset but not generalize to other read lengths, organisms, or library types (e.g., orphanChainSubThresh=0.95 was empirically derived from C++ 1.12.0 and may not be optimal for Rust or for different sequencing protocols).
- The comparison assumes both implementations expose equivalent user-facing quantification interfaces and inference models; differences in bias correction, fragment-length distribution estimation, or Bayesian priors will introduce disagreement orthogonal to mapping-level alignment differences.

## Evidence

- [methods] C++ salmon uses orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9 for chain pruning before alignment, accounting for approximately 80% (~49k reads) of the observed mapping count gap: "C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9... ~80% (~49k): a chain-sub-optimality default difference"
- [methods] Per-read mapping agreement between C++ 1.12.0 and Rust is 99.83% on byte-identical index with NumReads Pearson correlation 0.99854: "per-read mapping agreement | 99.83%... NumReads Pearson | 0.99854"
- [methods] Rust maps 62,812 reads C++ leaves fully unmapped; only 154 reads mapped by C++ are unmapped by Rust, showing asymmetry in alignment behavior: "Rust maps 62,812 reads C++ leaves fully unmapped (u), C++ maps only 154 Rust doesn't"
- [methods] GEUVADIS ERR188044 paired-end reads (76 bp, 36.35M reads) are the benchmark dataset used to compare C++ and Rust implementations: "Reads: GEUVADIS ERR188044 (36.35M 76bp PE); default selective alignment"
- [methods] minimap2 full Smith-Waterman re-alignment is used to classify boundary-case reads as strong/weak/unaligned to assess symmetry between implementations: "minimap2 (full SW) on these reads gives near-identical quality profiles in both directions"
- [readme] salmon 2.0 maintains the same workflow and output formats but requires index rebuilding due to format changes: "It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read, but... the index format changed, so you must rebuild your index"
- [methods] A pufferfish SSHash k-mer orientation bug caused the Rust port to map ~2% more reads than C++ salmon until the bug was fixed: "That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup"
