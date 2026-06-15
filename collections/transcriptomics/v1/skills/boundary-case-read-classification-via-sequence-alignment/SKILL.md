---
name: boundary-case-read-classification-via-sequence-alignment
description: Use when when two mapping implementations (or versions of the same mapper) show disagreement on per-read mapping status—e.g., one mapper leaves reads fully unmapped that the other maps, or one maps with high confidence where the other is uncertain.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0080
  tools:
  - minimap2
  - piscem-rs
  - salmon 1.12.0 (C++)
  - salmon 2.0 (Rust)
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

# boundary-case-read-classification-via-sequence-alignment

## Summary

Classify reads at the boundary of mapping disagreement between two mappers (e.g., C++ vs. Rust salmon) by re-aligning them using full Smith-Waterman alignment to determine whether they should be strong-aligned, weak-aligned, or unmapped. This skill resolves ambiguous mapping decisions and quantifies the symmetry and validity of differences in mapping rates between implementations.

## When to use

When two mapping implementations (or versions of the same mapper) show disagreement on per-read mapping status—e.g., one mapper leaves reads fully unmapped that the other maps, or one maps with high confidence where the other is uncertain. Use this skill to distinguish systematic bugs or parameter differences from legitimate sensitivity trade-offs by testing boundary cases with unbiased, exhaustive alignment scoring.

## When NOT to use

- When the two mappers use fundamentally different reference indices or k-mer parameters—alignment scores will not be directly comparable.
- When mapping disagreement is already known to be a deliberate design choice (e.g., intentional trade-off in seed length or scoring threshold) and you only need to document the difference, not validate correctness.
- When computational budget is very tight and per-read full Smith-Waterman re-alignment is infeasible; use a faster heuristic aligner instead.

## Inputs

- FASTQ or paired-end read files (e.g., 76 bp paired-end RNA-seq reads from GEUVADIS)
- Byte-identical reference index (e.g., GRCh38 cDNA or Ensembl transcriptome in FASTA format)
- Mapping output from both implementations (e.g., salmon quant output with per-read mapping agreement metrics)
- List of boundary-case reads: reads mapped by one implementation but unmapped by the other

## Outputs

- Per-read Smith-Waterman alignment scores and quality metrics
- Classification table: read_id, direction (Rust-only or C++-only), SW alignment class (strong/weak/unaligned), alignment identity, coverage
- Symmetry analysis: count and distribution of strong/weak/unaligned reads in each direction
- Summary statistics: % of disagreement attributable to each class, ratio of Rust-only to C++-only misses

## How to apply

Extract reads that are mapped by one implementation but unmapped (or only partially mapped) by the other, or vice versa. Re-align these boundary-case reads using a reference-standard full Smith-Waterman aligner (e.g., minimap2 with full SW) against the same reference transcriptome index used by both mappers. Score the resulting alignments on quality metrics (e.g., alignment identity, coverage, score) and classify each read into one of three categories: strong-aligned (high-quality consensus alignment), weak-aligned (marginal alignment quality), or unaligned (no strong match). Compare the distribution of classifications across the two directions (Rust-only vs. C++-only reads) to assess whether disagreement is symmetric (both miss similar reads) or biased (one implementation systematically underassigns). This reveals whether differences stem from genuine sensitivity choices or from undetected bugs.

## Related tools

- **minimap2** (Full Smith-Waterman reference aligner for unbiased re-alignment of boundary-case reads to classify alignment quality)
- **salmon 1.12.0 (C++)** (First implementation (baseline mapper) producing mapping output to compare against Rust port) — https://github.com/COMBINE-lab/salmon/tree/cpp
- **salmon 2.0 (Rust)** (Second implementation (test mapper) producing alternative mapping output for disagreement analysis) — https://github.com/COMBINE-lab/salmon

## Examples

```
minimap2 -a -x sr --secondary=no -o boundary_reads.sam GRCh38_cdna.fa boundary_case_reads.fq && samtools view -F 4 boundary_reads.sam | awk '{print $1, $5, length($10)}' > classification_table.txt
```

## Evaluation signals

- Boundary-case reads classified by minimap2 SW should show consistent quality profiles (alignment identity, coverage, CIGAR) in both forward and reverse directions, confirming unbiased reference alignment.
- Residual disagreement (Rust-only + C++-only reads) should drop significantly after applying corrected chain-pruning thresholds to the Rust port (expected: from ~62,966 to <20,000 reads on ERR188044).
- Per-read mapping agreement (fraction of reads classified identically by both implementations) should improve from the pre-correction baseline (99.83%) toward ≥99.8% after re-alignment reclassification.
- Symmetry analysis: distribution of strong/weak/unaligned classes should be similar between Rust-only and C++-only boundary reads, indicating no systematic directional bias in the mappers.
- Validation on byte-identical index: per-read mapping agreement Pearson correlation with NumReads should remain ≥0.998 after boundary reclassification, confirming that re-alignment did not introduce spurious differences.

## Limitations

- Smith-Waterman re-alignment is computationally expensive (O(n²) in query and reference lengths); scaling to millions of boundary-case reads requires parallelization or downsampling.
- Classification into strong/weak/unaligned relies on user-chosen thresholds (e.g., minimum identity %, minimum coverage %) that must be justified a priori and may not capture all nuanced alignment quality.
- This skill detects disagreement but does not directly identify the root cause (e.g., whether it is a k-mer orientation bug, chain pruning default, or alignment scoring difference); must be paired with targeted parameter sweeps or code inspection.
- If both mappers share a common upstream bug (e.g., in reference index generation or read preprocessing), Smith-Waterman re-alignment will not reveal it—validation requires independent reference data.

## Evidence

- [methods] minimap2 full SW: "minimap2 (full SW) on these reads gives near-identical quality profiles in both directions"
- [methods] boundary-case read classification: "assess symmetry via minimap2 full Smith-Waterman re-alignment of boundary-case reads to classify as strong/weak/unaligned"
- [methods] residual disagreement reduction: "residual per-read disagreement (Rust-only + C++-only) must drop from 62,966 to <20,000 reads"
- [methods] Rust-only and C++-only discrepancy: "Rust maps 62,812 reads C++ leaves fully unmapped (u), C++ maps only 154 Rust doesn't"
- [methods] byte-identical index validation: "Per-read mapping agreement between C++ 1.12.0 and Rust is 99.83% on byte-identical index"
