---
name: rna-seq-read-mapping-parameter-tuning
description: Use when when comparing two implementations of the same RNA-seq mapping algorithm on identical reference indices and read sets, if per-read mapping agreement is <99.8% or the overall mapping rate differs by >0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0622
  tools:
  - minimap2
  - piscem-rs
  - salmon
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

# RNA-seq read mapping parameter tuning

## Summary

Systematically adjust chain-pruning thresholds and selective-alignment parameters in transcript mappers to resolve discrepancies in mapping rate between implementations and recover reads left unmapped by suboptimal defaults. This skill is essential when a reference implementation (e.g., C++ salmon 1.12.0) and a port (e.g., Rust salmon 2.0) show unexplained mapping-rate gaps on identical inputs.

## When to use

When comparing two implementations of the same RNA-seq mapping algorithm on identical reference indices and read sets, if per-read mapping agreement is <99.8% or the overall mapping rate differs by >0.02%, investigate whether chain-pruning defaults (orphanChainSubThresh, postMergeChainSubThresh, preMergeChainSubThresh) or alignment-score thresholds are causing the divergence. Use this skill to isolate which parameter(s) account for the gap and whether tuning them recovers the missing mapped reads.

## When NOT to use

- Do not use this skill when comparing two independent algorithms on different indices or under different library-type assumptions; parameter tuning will not resolve algorithmic differences.
- Do not apply this skill if the reference implementation uses bias-correction, poly-A clipping, or decoy sequences that the port does not; first harmonize preprocessing before tuning mapping parameters.
- Do not use this skill as a substitute for fixing upstream bugs (e.g., k-mer-orientation errors in k-mer lookup); it is appropriate only for resolving gaps due to parameter defaults, not correctness bugs.

## Inputs

- Byte-identical reference transcriptome index (built with identical k-mer length, deterministic N-replacement)
- Paired-end RNA-seq reads in FASTQ format (or equivalent; test on well-characterized, publicly available datasets)
- Configuration files or parameter sets for both implementations being compared

## Outputs

- Mapping statistics (total mapped reads, mapping rate percentage) for each parameter configuration
- Per-read mapping agreement matrix (% reads mapped by both, by one only, by neither)
- NumReads Pearson correlation coefficient between implementations
- Classification of boundary-case reads (strong/weak/unaligned) from full-alignment re-ranking
- Quantified attribution of mapping gap to specific parameter(s)

## How to apply

First, quantify the magnitude and asymmetry of the mapping gap on a byte-identical reference index using a well-characterized dataset (e.g., GEUVADIS ERR188044, 36.35M 76 bp paired-end reads). Run both implementations with selective alignment enabled and identical flags (no bias correction, deterministic k-mer replacement) and measure per-read mapping agreement, NumReads correlation, and counts of reads mapped by only one implementation. Next, systematically adjust chain-pruning parameters: C++ salmon 1.12.0 uses orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9 as defaults; rerun the Rust port with these same values and re-measure mapping counts and per-read agreement. If tuning reduces the disagreement from ~63k to <20k reads and brings mapping rate within 0.02% of the reference, the gap is attributable to pruning-threshold defaults. For residual discrepancies, use full Smith-Waterman re-alignment (e.g., minimap2) on boundary-case reads to classify them as strong/weak/unaligned and determine whether the remaining gap stems from alignment-score thresholds, k-mer-orientation bugs, or other systematic biases.

## Related tools

- **salmon** (Primary transcript-mapping and quantification engine; tuning applies to both salmon 2.0 (Rust) and salmon 1.12.0 (C++) when invoked with selective alignment (-l A) and chain-pruning flags (--orphanChainSubThresh, --postMergeChainSubThresh).) — https://github.com/COMBINE-lab/salmon
- **minimap2** (Full Smith-Waterman aligner used to re-rank boundary-case reads and classify them as strong/weak/unaligned in order to diagnose source of residual mapping disagreement.)
- **piscem-rs** (Underlying selective-alignment and k-mer-lookup library for salmon 2.0 Rust port; parameter tuning is applied via salmon CLI flags that configure piscem-rs behavior.) — https://github.com/COMBINE-lab/salmon
- **pufferfish** (K-mer index and lookup library used by salmon; bugs in pufferfish k-mer-orientation (e.g., commit 5dce7f4) can cause spurious mapping gaps that must be distinguished from parameter-tuning issues.)

## Examples

```
salmon quant -i salmon_index -l A -1 reads_R1.fastq.gz -2 reads_R2.fastq.gz --orphanChainSubThresh 0.95 --postMergeChainSubThresh 0.9 -p 16 -o quant_tuned
```

## Evaluation signals

- Mapping rate of tuned implementation must be within 0.02% of reference (e.g., 92.011% ± 0.02% for C++ salmon 1.12.0 on ERR188044).
- Per-read mapping agreement must reach ≥99.8% after tuning (measured as % of reads on which both implementations agree, mapped or unmapped).
- Residual per-read disagreement (reads mapped by Rust only + reads mapped by C++ only) must drop from initial gap (~63k reads on ERR188044) to <20k reads after tuning.
- NumReads Pearson correlation between implementations must be ≥0.99854 after parameter adjustment.
- Full Smith-Waterman re-alignment (minimap2) of remaining boundary-case reads should show symmetric disagreement (not skewed toward one implementation) and classify >90% of remaining reads as 'weak' rather than 'strong', confirming they are ambiguous rather than false negatives.

## Limitations

- Parameter tuning assumes both implementations use identical preprocessing (poly-A clipping ≥10 trailing As, deterministic N-replacement) and identical reference indices; if upstream steps differ, tuning will not resolve the gap.
- Chain-pruning parameters are implementation-specific and may not be directly transferable; the exact thresholds (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9) were validated only for salmon C++ 1.12.0 vs. Rust 2.0 on ERR188044.
- Tuning maps only ~80% of the observed gap; the remaining ~20% may stem from k-mer-orientation bugs, alignment-score thresholds, or floating-point rounding differences that require deeper debugging.
- The skill does not address single-cell (alevin) mapping; those parameters are now managed by alevin-fry, not salmon 2.0.
- Validation requires a well-characterized, publicly available dataset (e.g., GEUVADIS) with known ground-truth or consensus mapping profiles; results on other datasets may differ.

## Evidence

- [other] Does applying C++ salmon 1.12.0's chain score thresholds (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9) to the Rust salmon port on ERR188044 reduce the mapping count gap and confirm that ~80% of the discrepancy is attributable to the orphan/post-merge pruning default difference?: "C++ salmon uses orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9 for chain pruning before alignment, accounting for approximately 80% (~49k reads) of the observed mapping count gap between"
- [other] Workflow and metrics described in task card: "Rust mapping rate must be ≥92.03% (within 0.02% of C++ 1.12.0); residual per-read disagreement (Rust-only + C++-only) must drop from 62,966 to <20,000 reads; per-read mapping agreement ≥99.8%."
- [methods] Methods section describing pufferfish k-mer-orientation fix: "After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read"
- [methods] Methods section describing per-read agreement metric: "per-read mapping agreement | 99.83%"
- [methods] Methods section describing boundary-case re-alignment: "minimap2 (full SW) on these reads gives near-identical quality profiles in both directions"
- [readme] README introduction emphasizing breaking changes and index rebuild requirement: "The most important one: **the index format changed, so you must rebuild your index.**"
