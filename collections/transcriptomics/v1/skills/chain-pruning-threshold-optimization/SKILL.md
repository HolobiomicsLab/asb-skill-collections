---
name: chain-pruning-threshold-optimization
description: Use when when comparing mapped read counts between two RNA-seq quantification implementations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0080
  tools:
  - minimap2
  - piscem-rs
  - salmon 2.0 (Rust)
  - salmon 1.12.0 (C++)
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

# chain-pruning-threshold-optimization

## Summary

Optimize k-mer chain filtering thresholds (orphanChainSubThresh, postMergeChainSubThresh) to reduce spurious read assignments and improve mapping accuracy consistency between RNA-seq quantification implementations. This skill addresses parameter-driven mapping-rate gaps by systematically tuning chain-pruning defaults before selective-alignment scoring.

## When to use

When comparing mapped read counts between two RNA-seq quantification implementations (e.g., C++ vs. Rust ports of the same tool) or between versions, and observing a systematic 1–5% gap in mapping rate on a byte-identical reference index that is not explained by k-mer lookup bugs or index format differences. Chain-pruning threshold divergence is a leading hypothesis when per-read mapping agreement is high (≥99.8%) but total mapped-read counts differ substantially.

## When NOT to use

- Mapping rates already agree to within ≤0.02% on a byte-identical index; chain-pruning optimization is not the bottleneck.
- Per-read mapping agreement is <99% or residual disagreement is symmetric (similar counts of reads mapped by each implementation); suggests a k-mer lookup or index-format bug rather than pruning-threshold divergence.
- Input reads are very long (>300 bp), where chain coverage is typically high and pruning thresholds have minimal effect on mapping rates.

## Inputs

- paired-end FASTQ reads (or any read format compatible with the quantification tool; e.g., ERR188044: 36.35M reads, 76 bp, gzip-compressed)
- byte-identical transcriptome reference index (k=31, deterministic N-replacement, matching both implementations)
- reference implementation's chain-pruning parameters (orphanChainSubThresh, postMergeChainSubThresh, preMergeChainSubThresh values)

## Outputs

- mapping statistics table: total mapped reads, mapping rate (%), per-read mapping agreement (%)
- residual disagreement report: counts of reads mapped by test-only vs. reference-only implementations
- quantified threshold-contribution estimate: proportion of original gap explained by chain-pruning parameter difference (e.g., ~80%, ~49k reads)
- boundary-case read classifications (optional): strong/weak/unaligned annotations from full Smith-Waterman re-alignment via minimap2

## How to apply

First, establish a baseline: run both implementations on a real short-read dataset (e.g., 36.35M paired-end 76 bp reads) with identical index and selective-alignment settings, recording total mapped reads and per-read mapping agreement. If the gap is ≥1% and per-read agreement is ≥99.8%, isolate the reference implementation's chain-pruning parameters (typically orphanChainSubThresh and postMergeChainSubThresh); these are often not exposed in user-facing CLIs. Re-run the test implementation with those exact thresholds explicitly set via command-line flags. Compare mapped counts, residual read disagreement (reads mapped by only one implementation), and per-read agreement. If mapping rate converges to within 0.02% and residual disagreement drops from ~63k to <20k reads, quantify the proportion of the original gap attributable to this parameter difference. Document whether the threshold difference is a conservative default (reducing false positives) or a sensitivity choice (capturing boundary-case reads with weak chains).

## Related tools

- **salmon 2.0 (Rust)** (test implementation; run with optimized chain-pruning thresholds to reproduce reference behavior) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0 (C++)** (reference implementation; source of ground-truth chain-pruning parameters) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **minimap2** (full Smith-Waterman alignment engine for re-scoring boundary-case reads and classifying chain-pruning effects)
- **piscem-rs** (underlying selective-alignment mapper in salmon 2.0 Rust port; implements chain pruning before MEM extraction) — https://github.com/COMBINE-lab/salmon

## Examples

```
salmon quant -i salmon_index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz -p 16 --orphanChainSubThresh 0.95 --postMergeChainSubThresh 0.9 -o sample_quant
```

## Evaluation signals

- Mapping rate of test implementation with optimized thresholds is ≥92.03% (within 0.02% of reference baseline of 92.011% on ERR188044), confirming threshold adoption reproduces reference behavior.
- Per-read mapping agreement (fraction of reads assigned identically by both implementations) reaches ≥99.8% after threshold optimization, indicating consistent read-level decisions.
- Residual read disagreement (reads mapped by only one implementation) drops from initial ~63k to <20k reads, with majority of original gap accounted for by threshold difference.
- Quantified threshold-contribution estimate (proportion of gap explained) aligns with expected range (≥75%); documents whether pruning is primary driver vs. secondary contributor.
- Full Smith-Waterman re-alignment of residual boundary-case reads shows that pruned chains have measurably lower coverage or score, validating that thresholds filter genuinely weak chains rather than arbitrarily discarding valid alignments.

## Limitations

- Chain-pruning threshold optimization only addresses parameter-driven gaps; it does not resolve k-mer lookup bugs (e.g., strand-orientation errors in pufferfish SSHash) or index-format incompatibilities, which require separate fixes.
- Threshold values are tool- and reference-specific; parameters tuned for one transcriptome (e.g., GRCh38 cDNA, 193,759 transcripts) may not transfer to decoy-augmented or genome-scale indices, and empirical re-tuning may be necessary.
- Optimization is most effective for short reads (≤100 bp) where chain coverage is moderate; very long reads typically have high chain coverage and are insensitive to threshold tweaks.
- Pruning thresholds control false-positive reduction but do not improve sensitivity to genuinely difficult reads; residual disagreement after threshold matching still reflects fundamental mapper differences (e.g., MEM extraction strategy, seed selection) that threshold tuning cannot bridge.

## Evidence

- [methods] C++ salmon uses orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9 for chain pruning before alignment: "C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9"
- [methods] ~80% of the observed mapping-count gap is attributable to chain-pruning parameter difference: "~80% (~49k): a chain-sub-optimality default difference (describable, deferred)"
- [methods] Per-read mapping agreement between C++ 1.12.0 and Rust on byte-identical index is 99.83%: "per-read mapping agreement | 99.83%"
- [methods] Rust maps 62,812 reads C++ leaves fully unmapped; C++ maps only 154 Rust doesn't: "Rust maps 62,812 reads C++ leaves fully unmapped (u), C++ maps only 154 Rust doesn't"
- [readme] Salmon 2.0 is a from-scratch Rust rewrite with the same workflow and output formats but breaking changes: "This is salmon 2.0 — a from-scratch Rust rewrite of salmon. It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read, but it is a"
