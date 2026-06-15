---
name: selective-alignment-parameter-tuning
description: Use when you observe discrepancies in mapping rate or per-transcript quantification between two salmon implementations, or when the default chain-pruning thresholds (orphanChainSubThresh, postMergeChainSubThresh) are leaving a substantial fraction of reads unmapped (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0769
  tools:
  - piscem-rs
  - pufferfish
  - minimap2
  - salmon 2.0
  - salmon 1.12.0 (C++)
derived_from:
- doi: 10.1038/nmeth.4197
  title: salmon
evidence_spans:
- The Rust port (built on piscem-rs, which derives orientation correctly)
- The Rust port (built on piscem-rs, which derives orientation correctly) was right all along
- pufferfish's SSHash k-mer lookup, now fixed upstream
- minimap2 (full SW) on these reads gives near-identical quality profiles in both directions
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

# selective-alignment-parameter-tuning

## Summary

Adjust chain-pruning thresholds and seed-representation strategies in selective-alignment mode to optimize mapping rate and quantification accuracy for RNA-seq transcript abundance estimation. This skill is essential when comparing implementations (C++ vs. Rust salmon) or when default chain-pruning settings leave reads unmapped that alternative thresholds would recover.

## When to use

Apply this skill when you observe discrepancies in mapping rate or per-transcript quantification between two salmon implementations, or when the default chain-pruning thresholds (orphanChainSubThresh, postMergeChainSubThresh) are leaving a substantial fraction of reads unmapped (e.g., >1% difference in mapping rate). Use it to systematically isolate whether differences are due to k-mer lookup bugs (pufferfish orientation), threshold defaults, or seed representation granularity.

## When NOT to use

- Input reads are from a different organism or library type than the baseline — comparison requires the same dataset and index.
- You are comparing salmon 2.0 (Rust) against C++ salmon 1.12.0 without controlling for the pufferfish SSHash streaming orientation bug — apply the pufferfish fix (commit 5dce7f4) first.
- The observed mapping-rate or quantification discrepancy is <0.01% — further parameter tuning is unlikely to be statistically meaningful and may introduce artifacts.

## Inputs

- FASTQ reads (single-end or paired-end)
- salmon reference index (built from transcriptome FASTA on byte-identical basis)
- chain-pruning parameter values (orphanChainSubThresh, postMergeChainSubThresh, preMergeChainSubThresh)
- seed representation strategy (default unitig-constrained, sparse fixed-k, reference-extended, true unitig MEM)

## Outputs

- quant.sf file (per-transcript NumReads, EffectiveLength, TPM)
- mapping rate (percentage of reads mapped)
- per-read mapping agreement summary (percentage of fully unmapped reads on which both tools agree)
- Pearson correlation coefficients (NumReads and EffectiveLength between baseline and variant)
- unmapped_names.txt (fully unmapped read identifiers for cross-comparison)

## How to apply

First, establish a baseline by running selective-alignment quantification with default parameters (salmon quant -l <libType> with default chain thresholds) on a byte-identical reference index and recording per-transcript NumReads, TPM, and mapping rate. Next, identify the source of discrepancies: check if a k-mer lookup orientation bug exists (by comparing against minimap2 full Smith-Waterman), then test alternative chain-pruning thresholds by running salmon quant with modified orphanChainSubThresh and postMergeChainSubThresh values. For seed representation variants, re-run the mapper with sparse fixed-k anchors, reference-extended MEMs, or unitig-constrained uni-MEMs. Calculate Pearson correlation coefficients (NumReads and EffectiveLength) between each variant and the baseline; correlations ≥0.99999995 indicate the variant does not explain observed gaps. Finally, validate that mapping rate changes are within ≤0.01% tolerance and compare per-read mapping agreement (fully unmapped reads coded 'u' in mapping outputs) to confirm the source of the improvement.

## Related tools

- **salmon 2.0** (primary mapper and quantifier; run with varied chain-pruning thresholds and seed representations in selective-alignment mode) — https://github.com/COMBINE-lab/salmon
- **salmon 1.12.0 (C++)** (reference implementation for comparison; use default C++ thresholds (orphanChainSubThresh=0.95, postMergeChainSubThresh=0.9) as baseline) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **pufferfish** (underlying k-mer lookup engine; fix streaming orientation bug (commit 5dce7f4) to ensure fair comparison between C++ and Rust)
- **piscem-rs** (Rust mapper backend; derives k-mer orientation correctly and was validated against C++ after pufferfish fix)
- **minimap2** (full Smith-Waterman alignment for validation; use to confirm strand and locus agreement of differentially mapped reads)

## Examples

```
salmon quant -i salmon_index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz -p 16 -o sample_quant_baseline && salmon quant -i salmon_index -l A -1 reads_1.fastq.gz -2 reads_2.fastq.gz -p 16 --orphanChainSubThresh 0.95 --postMergeChainSubThresh 0.9 -o sample_quant_tuned
```

## Evaluation signals

- Pearson correlation coefficient for NumReads between baseline and tuned variant ≥0.99999995 (variant does not explain observed gap) or <0.99999995 (variant introduces systematic shift requiring investigation).
- Per-read mapping agreement: count fully unmapped reads (coded 'u' in mapping outputs) that both tools agree upon; ≥99% agreement indicates chain-pruning thresholds are not the primary source of discrepancy.
- Mapping rate difference: ≤0.01% tolerance between baseline and variant indicates threshold change did not materially affect sensitivity; >0.01% difference suggests the threshold is a key parameter.
- Byte-identical index validation: confirm that both salmon implementations build indices with identical bytes (hash seeds, bit-vectors, k-mer encoding) to isolate algorithmic from implementation differences.
- Cross-check read placement using SAM/BAM writeMappings output: for reads identified as differentially mapped, verify strand orientation and transcript locus match between variants to rule out spurious placements.

## Limitations

- Chain-pruning parameter tuning is implementation-specific: C++ salmon 1.11.4 uses orphanChainSubThresh=0.95 and postMergeChainSubThresh=0.9 by default, while Rust salmon 2.0 uses orphanChainSubThresh=0.0 and postMergeChainSubThresh=0.0, making direct cross-version comparison require explicit threshold matching.
- ~80% of mapping-rate differences between C++ and Rust implementations are attributable to chain-pruning defaults, not seed-representation granularity; optimizing seed representation alone will not recover the gap.
- Byte-identical index requirement limits practical applicability: indices must be rebuilt with identical FASTA cleaning (e.g., non-ACGT replacement rules, poly-A clipping ≥10 trailing As) to ensure fair comparison; pre-built indices from different sources may not be directly comparable.
- Pearson correlation metric can mask outliers: high overall correlation (r≥0.999) does not guarantee agreement on lowly-expressed transcripts; use supplementary quantile-quantile plots or per-transcript fold-change distributions to detect systematic biases.
- Seed representation variants (sparse fixed-k, reference-extended MEMs, true unitig uni-MEMs) are theoretical constructs tested only on Rust salmon; their behavior on C++ implementation is not characterized in this article.

## Evidence

- [methods] On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup: "On real short reads the Rust port mapped ~2% more reads than C++ salmon. That extra ~2% was not a Rust 'sensitivity choice' — it exposed a k-mer-orientation bug in pufferfish's SSHash streaming lookup"
- [methods] After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read: "After fixing pufferfish (commit 5dce7f4, salmon pin bumped), C++ salmon maps the same reads: 83.48% → 85.55%, matching the Rust port to within 1 read"
- [methods] ~80% (~49k): a chain-sub-optimality default difference (describable, deferred). C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9: "C++ prunes low-coverage chains/orphans before alignment using orphanChainSubThresh = 0.95 and postMergeChainSubThresh = 0.9"
- [methods] NumReads Pearson correlation is 0.99854 between C++ and Rust on byte-identical index: "On byte-identical index, NumReads Pearson correlation is 0.99854 between C++ and Rust"
- [methods] Compute Pearson correlation coefficient (r) between NumReads counts from each variant and the default baseline using correlation analysis, verifying r ≥ 0.99999995 for all variants.: "Calculate Pearson correlation coefficient (r) between NumReads counts from each variant and the default baseline using correlation analysis, verifying r ≥ 0.99999995 for all variants"
- [intro] salmon 2.0 (Rust): from-scratch Rust rewrite of salmon: "This is salmon 2.0 — a from-scratch Rust rewrite of salmon"
- [intro] It keeps the same workflow (salmon index → salmon quant → quant.sf) and the same output formats downstream tools read: "It keeps the same workflow (`salmon index` → `salmon quant` → `quant.sf`) and the same output formats downstream tools read"
